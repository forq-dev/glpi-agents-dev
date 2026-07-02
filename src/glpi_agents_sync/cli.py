from __future__ import annotations

import argparse
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
from glpi_agents_sync.source import (
    DEFAULT_SOURCE_REF,
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
    except (ConfigError, SourceFetchError, RuntimeError) as exc:
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
        help="Ref do repositorio-fonte. Padrao: main.",
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

    raise RuntimeError(f"Comando desconhecido: {args.command}")


def run_bootstrap(project_root: Path, source_repo: str | None, source_ref: str | None) -> int:
    project_root.mkdir(parents=True, exist_ok=True)
    effective_source_repo = source_repo if source_repo is not None else DEFAULT_SOURCE_REPOSITORY
    effective_source_ref = source_ref if source_ref is not None else DEFAULT_SOURCE_REF
    source_tree = clone_source_tree(effective_source_repo, effective_source_ref)
    try:
        entries = list_source_entries(source_tree.root)
        manifest = build_manifest(effective_source_repo, effective_source_ref, entries)
        plan = SyncPlan(actions=build_initial_actions(entries, project_root), manifest=manifest)
        result = apply_sync_plan(project_root, source_tree, plan, confirm_removals=True)
        final_manifest = stamp_manifest(result.manifest)
        write_manifest(project_root, final_manifest)
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
