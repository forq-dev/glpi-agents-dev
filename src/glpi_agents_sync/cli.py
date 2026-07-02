from __future__ import annotations

import argparse
import os
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from glpi_agents_sync.config import (
    ConfigError,
    load_manifest,
    write_manifest,
)
from glpi_agents_sync.models import SyncEntry, SyncManifest
from glpi_agents_sync.runtime import (
    RuntimeConfigError,
    RuntimeProbeError,
    RuntimeReport,
    create_runtime_config,
    ensure_runtime_ready,
    load_runtime_config,
    probe_runtime,
    render_runtime_report,
    runtime_config_path_for,
    write_runtime_config,
)
from glpi_agents_sync.source import (
    DEFAULT_SOURCE_REPOSITORY,
    SourceFetchError,
    cleanup_source_tree,
    clone_source_tree,
    list_source_entries,
)
from glpi_agents_sync.sync import (
    SyncAction,
    SyncPlan,
    apply_sync_plan,
    build_sync_plan,
)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run_command(args)
    except (ConfigError, RuntimeConfigError, RuntimeProbeError, SourceFetchError, RuntimeError) as exc:
        print(f"[ERRO] {exc}")
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glpi-agents-sync",
        description="Bootstrap e sincronizacao do framework glpi-agents-dev na raiz do plugin.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_common_options(subparsers.add_parser("bootstrap", help="Instala o framework no projeto"))
    add_common_options(subparsers.add_parser("sync", help="Atualiza arquivos gerenciados"))
    add_common_options(
        subparsers.add_parser("status", help="Mostra o que precisa ser atualizado sem aplicar")
    )
    add_common_options(subparsers.add_parser("doctor", help="Valida configuracao e origem"))
    setup_parser = subparsers.add_parser("setup", help="Prepara gh, Playwright e Chrome localmente")
    setup_parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Raiz do plugin. Padrao: diretorio atual.",
    )
    setup_parser.add_argument(
        "--install-playwright-browsers",
        action="store_true",
        help="Instala Chromium via Playwright antes de validar o ambiente.",
    )
    setup_parser.add_argument(
        "--print-env",
        action="store_true",
        help="Mostra exports de shell para o ambiente atual.",
    )
    return parser


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Raiz do plugin. Padrao: diretorio atual.",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Repositorio remoto do framework. Padrao: origem oficial embutida.",
    )
    parser.add_argument(
        "--ref",
        type=str,
        default=None,
        help="Ref do repositorio-fonte. Padrao: branch padrao do repositorio-fonte.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Aplica remoções pendentes sem pedir confirmacao.",
    )


def run_command(args: argparse.Namespace) -> int:
    plugin_root = resolve_plugin_root(args.root)

    if args.command == "bootstrap":
        return run_bootstrap(plugin_root, args.source, args.ref)
    if args.command == "sync":
        return run_sync(plugin_root, args.source, args.ref, args.yes, dry_run=False)
    if args.command == "status":
        return run_sync(plugin_root, args.source, args.ref, args.yes, dry_run=True)
    if args.command == "doctor":
        return run_doctor(plugin_root, args.source, args.ref)
    if args.command == "setup":
        return run_setup(plugin_root, args.install_playwright_browsers, args.print_env)

    raise RuntimeError(f"Comando desconhecido: {args.command}")


def run_bootstrap(project_root: Path, source_repo: str | None, source_ref: str | None) -> int:
    project_root.mkdir(parents=True, exist_ok=True)
    ensure_runtime_ready(project_root)
    effective_source_repo = source_repo if source_repo is not None else DEFAULT_SOURCE_REPOSITORY
    source_tree = clone_source_tree(effective_source_repo, source_ref)
    try:
        entries = list_source_entries(source_tree.root)
        effective_source_ref = source_tree.ref
        manifest = build_manifest(effective_source_repo, effective_source_ref, entries)
        plan = SyncPlan(actions=build_initial_actions(entries, project_root), manifest=manifest)
        result = apply_sync_plan(project_root, source_tree, plan, confirm_removals=True)
        final_manifest = stamp_manifest(result.manifest)
        write_manifest(project_root, final_manifest)
        runtime_config = create_runtime_config(False)
        write_runtime_config(project_root, runtime_config)
        print_summary("Bootstrap concluido", result.actions, final_manifest)
        return 0
    finally:
        cleanup_source_tree(source_tree)


def run_sync(
    project_root: Path,
    source_repo: str | None,
    source_ref: str | None,
    confirm_removals: bool,
    dry_run: bool,
) -> int:
    ensure_runtime_ready(project_root)
    manifest = load_manifest(project_root)
    effective_source_repo = source_repo if source_repo is not None else manifest.source_repo
    effective_source_ref = source_ref if source_ref is not None else manifest.source_ref
    effective_manifest = replace(
        manifest,
        source_repo=effective_source_repo,
        source_ref=effective_source_ref,
    )
    source_tree = clone_source_tree(effective_source_repo, effective_source_ref)
    try:
        plan = build_sync_plan(project_root, source_tree, effective_manifest)
        if dry_run:
            print_report("Status do sync", plan.actions, plan.manifest)
            return 0

        needs_confirmation = any(action.kind == "warn" for action in plan.actions)
        if needs_confirmation and not confirm_removals:
            print_report("Atualizacao pendente", plan.actions, plan.manifest)
            print(
                "Use --yes para confirmar a remocao dos arquivos que sumiram no repositorio-fonte."
            )
            return 2

        result = apply_sync_plan(project_root, source_tree, plan, confirm_removals)
        final_manifest = stamp_manifest(result.manifest)
        write_manifest(project_root, final_manifest)
        print_summary("Sincronizacao concluida", result.actions, final_manifest)
        return 0
    finally:
        cleanup_source_tree(source_tree)


def run_doctor(project_root: Path, source_repo: str | None, source_ref: str | None) -> int:
    print_runtime_status(project_root)
    manifest = load_manifest(project_root)
    effective_source_repo = source_repo if source_repo is not None else manifest.source_repo
    effective_source_ref = source_ref if source_ref is not None else manifest.source_ref
    effective_manifest = replace(
        manifest,
        source_repo=effective_source_repo,
        source_ref=effective_source_ref,
    )
    source_tree = clone_source_tree(effective_source_repo, effective_source_ref)
    try:
        plan = build_sync_plan(project_root, source_tree, effective_manifest)
        print_report("Diagnostico", plan.actions, plan.manifest)
        print(f"Configuração carregada em: {project_root / '.agents-sync.json'}")
        return 0
    finally:
        cleanup_source_tree(source_tree)


def run_setup(project_root: Path, install_playwright_browsers: bool, print_env: bool) -> int:
    project_root.mkdir(parents=True, exist_ok=True)
    runtime_config = create_runtime_config(install_playwright_browsers)
    write_runtime_config(project_root, runtime_config)
    report = probe_runtime(runtime_config)
    print_runtime_summary(report)
    if print_env:
        export_script = build_export_script(report)
        if export_script:
            print(export_script)
    print(f"Configuração de runtime carregada em: {runtime_config_path_for(project_root)}")
    if report.has_errors():
        raise RuntimeProbeError(render_runtime_report(report))
    return 0


def build_manifest(source_repo: str, source_ref: str, entries: tuple[SyncEntry, ...]) -> SyncManifest:
    generated_at = datetime.now(tz=UTC).isoformat()
    return SyncManifest(
        source_repo=source_repo,
        source_ref=source_ref,
        generated_at=generated_at,
        entries=entries,
    )


def stamp_manifest(manifest: SyncManifest) -> SyncManifest:
    generated_at = datetime.now(tz=UTC).isoformat()
    return replace(manifest, generated_at=generated_at)


def build_initial_actions(entries: tuple[SyncEntry, ...], project_root: Path) -> tuple[SyncAction, ...]:
    actions: list[SyncAction] = []
    for entry in entries:
        actions.append(
            SyncAction(
                target=entry.target,
                kind="create" if not (project_root / entry.target).exists() else "update",
                detail="bootstrap inicial do projeto consumidor",
            )
        )
    return tuple(actions)


def print_summary(title: str, actions: tuple[SyncAction, ...], manifest: SyncManifest) -> None:
    print(f"[OK] {title}")
    print_report(title, actions, manifest)


def print_report(title: str, actions: tuple[SyncAction, ...], manifest: SyncManifest) -> None:
    creates = [action for action in actions if action.kind == "create"]
    updates = [action for action in actions if action.kind == "update"]
    removes = [action for action in actions if action.kind == "remove"]
    warnings = [action for action in actions if action.kind == "warn"]

    print(f"[INFO] {title}")
    print(f"[INFO] origem={manifest.source_repo} ref={manifest.source_ref}")
    print_action_group("Criar", creates)
    print_action_group("Atualizar", updates)
    print_action_group("Remover", removes)
    print_action_group("Avisos", warnings)


def print_action_group(label: str, actions: Iterable[SyncAction]) -> None:
    action_list = list(actions)
    if not action_list:
        print(f"[OK] {label}: nenhum")
        return

    print(f"[{label.upper()}] {len(action_list)} item(ns)")
    for action in action_list:
        print(f"- {action.target} :: {action.detail}")


def resolve_plugin_root(root: Path | None) -> Path:
    if root is None:
        return Path.cwd()
    return root.resolve()


def print_runtime_status(project_root: Path) -> None:
    runtime_config = load_runtime_config(project_root)
    report = probe_runtime(runtime_config)
    print_runtime_summary(report)


def print_runtime_summary(report: RuntimeReport) -> None:
    print("[INFO] Ambiente local")
    print(f"[INFO] github_enabled={report.config.github_enabled}")
    print(f"[INFO] playwright_enabled={report.config.playwright_enabled}")
    print(f"[INFO] chrome_devtools_enabled={report.config.chrome_devtools_enabled}")
    print(f"[INFO] install_playwright_browsers={report.config.install_playwright_browsers}")
    print(f"[INFO] chrome_channel={report.config.chrome_channel}")
    print(
        "[INFO] chrome_executable_path="
        f"{report.config.chrome_executable_path if report.config.chrome_executable_path is not None else 'ausente'}"
    )
    if not report.issues:
        print("[OK] Ambiente local: nenhum problema")
        return

    print(f"[AVISO] {len(report.issues)} problema(s) de ambiente")
    for issue in report.issues:
        print(f"- {issue.tool} :: {issue.message} :: {issue.detail}")


def build_export_script(report: RuntimeReport) -> str:
    lines: list[str] = []
    if os.getenv("GITHUB_TOKEN") is None and os.getenv("GH_TOKEN") is None:
        lines.append('export GITHUB_TOKEN="$(gh auth token)"')
        lines.append('export GH_TOKEN="$GITHUB_TOKEN"')
    if report.config.chrome_executable_path is not None:
        lines.append(
            f'export PLAYWRIGHT_CHROME_EXECUTABLE_PATH="{report.config.chrome_executable_path}"'
        )
        lines.append(
            f'export CHROME_DEVTOOLS_EXECUTABLE_PATH="{report.config.chrome_executable_path}"'
        )
    return "\n".join(lines)
