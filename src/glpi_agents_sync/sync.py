from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from glpi_agents_sync.config import ConfigError
from glpi_agents_sync.models import SyncEntry, SyncManifest
from glpi_agents_sync.source import SourceTree, list_source_entries

SyncActionKind = Literal["create", "update", "remove", "keep", "warn"]


@dataclass(frozen=True, slots=True)
class SyncAction:
    target: str
    kind: SyncActionKind
    detail: str


@dataclass(frozen=True, slots=True)
class SyncPlan:
    actions: tuple[SyncAction, ...]
    manifest: SyncManifest


@dataclass(frozen=True, slots=True)
class SyncResult:
    actions: tuple[SyncAction, ...]
    manifest: SyncManifest


def build_sync_plan(
    project_root: Path,
    source_tree: SourceTree,
    manifest: SyncManifest,
) -> SyncPlan:
    current_entries = list_source_entries(source_tree.root)
    current_by_target = {entry.target: entry for entry in current_entries}

    actions: list[SyncAction] = []
    next_entries: list[SyncEntry] = []

    for entry in current_entries:
        target_path = project_root / entry.target
        if entry.kind == "json_merge":
            desired_payload = _merged_json_payload(source_tree.root / entry.source, target_path)
            if not target_path.exists():
                actions.append(
                    SyncAction(
                        target=entry.target,
                        kind="create",
                        detail="arquivo JSON gerenciado por merge",
                    )
                )
            else:
                current_payload = _load_json_object(target_path)
                if current_payload != desired_payload:
                    actions.append(
                        SyncAction(
                            target=entry.target,
                            kind="update",
                            detail="arquivo JSON gerenciado por merge",
                        )
                    )
        elif entry.kind == "symlink":
            if _needs_symlink_update(source_tree.root / entry.source, target_path):
                action_kind = "create" if not target_path.exists() else "update"
                actions.append(
                    SyncAction(
                        target=entry.target,
                        kind=action_kind,
                        detail="atalho simbolico para AGENTS.md",
                    )
                )
        else:
            source_bytes = _read_bytes(source_tree.root / entry.source)
            if not target_path.exists():
                actions.append(
                    SyncAction(
                        target=entry.target,
                        kind="create",
                        detail="arquivo ausente no projeto consumidor",
                    )
                )
            else:
                target_bytes = target_path.read_bytes()
                if target_bytes != source_bytes:
                    actions.append(
                        SyncAction(
                            target=entry.target,
                            kind="update",
                            detail="conteudo divergiu do repositorio-fonte",
                        )
                    )

        next_entries.append(
            SyncEntry(
                source=entry.source,
                target=entry.target,
                kind=entry.kind,
                state="active",
            )
        )

    for entry in manifest.entries:
        if entry.target in current_by_target:
            continue

        target_path = project_root / entry.target
        if target_path.exists():
            actions.append(
                SyncAction(
                    target=entry.target,
                    kind="warn",
                    detail="arquivo nao existe mais no repositorio-fonte e precisa de confirmacao para remover",
                )
            )
        next_entries.append(
            SyncEntry(
                source=entry.source,
                target=entry.target,
                kind=entry.kind,
                state="pending_removal",
            )
        )

    ordered_entries = _merge_entries(current_entries, next_entries)
    next_manifest = SyncManifest(
        source_repo=manifest.source_repo,
        source_ref=manifest.source_ref,
        generated_at=manifest.generated_at,
        entries=ordered_entries,
    )

    return SyncPlan(actions=tuple(actions), manifest=next_manifest)


def apply_sync_plan(
    project_root: Path,
    source_tree: SourceTree,
    plan: SyncPlan,
    confirm_removals: bool,
) -> SyncResult:
    result_actions: list[SyncAction] = []
    for action in plan.actions:
        if action.kind == "warn":
            if confirm_removals:
                result_actions.append(
                    SyncAction(
                        target=action.target,
                        kind="remove",
                        detail="arquivo removido apos confirmacao",
                    )
                )
            else:
                result_actions.append(action)
            continue

        entry = _find_entry(plan.manifest.entries, action.target)
        if entry is None:
            continue

        if entry.kind == "json_merge":
            _apply_json_merge(project_root, source_tree.root, entry)
            result_actions.append(action)
            continue

        if entry.kind == "symlink":
            _apply_symlink(project_root, source_tree.root, entry)
            result_actions.append(action)
            continue

        if action.kind == "remove":
            _remove_target(project_root, entry.target)
            result_actions.append(action)
            continue

        _copy_file(project_root, source_tree.root, entry)
        result_actions.append(action)

    if confirm_removals:
        pending_removals = [entry for entry in plan.manifest.entries if entry.state == "pending_removal"]
        for entry in pending_removals:
            _remove_target(project_root, entry.target)

    updated_entries: list[SyncEntry] = []
    for entry in plan.manifest.entries:
        if entry.state == "pending_removal" and not confirm_removals:
            updated_entries.append(entry)
            continue
        if entry.state == "pending_removal" and confirm_removals:
            continue
        updated_entries.append(
            SyncEntry(
                source=entry.source,
                target=entry.target,
                kind=entry.kind,
                state="active",
            )
        )

    next_manifest = SyncManifest(
        source_repo=plan.manifest.source_repo,
        source_ref=plan.manifest.source_ref,
        generated_at=plan.manifest.generated_at,
        entries=tuple(updated_entries),
    )

    return SyncResult(actions=tuple(result_actions), manifest=next_manifest)


def _merge_entries(
    current_entries: tuple[SyncEntry, ...],
    next_entries: list[SyncEntry],
) -> tuple[SyncEntry, ...]:
    merged: dict[str, SyncEntry] = {entry.target: entry for entry in current_entries}
    for entry in next_entries:
        merged[entry.target] = entry
    ordered_targets = list(merged)
    ordered_targets.sort()
    return tuple(merged[target] for target in ordered_targets)


def _find_entry(entries: tuple[SyncEntry, ...], target: str) -> SyncEntry | None:
    for entry in entries:
        if entry.target == target:
            return entry
    return None


def _copy_file(project_root: Path, source_root: Path, entry: SyncEntry) -> None:
    source_path = source_root / entry.source
    target_path = project_root / entry.target
    _ensure_parent(target_path)
    shutil.copy2(source_path, target_path)


def _apply_symlink(project_root: Path, source_root: Path, entry: SyncEntry) -> None:
    source_path = source_root / entry.source
    target_path = project_root / entry.target
    _ensure_parent(target_path)
    if target_path.exists() or target_path.is_symlink():
        target_path.unlink()

    relative_target = Path("AGENTS.md")
    try:
        os.symlink(relative_target, target_path)
    except OSError:
        shutil.copy2(source_path, target_path)


def _apply_json_merge(project_root: Path, source_root: Path, entry: SyncEntry) -> None:
    source_path = source_root / entry.source
    target_path = project_root / entry.target
    _ensure_parent(target_path)

    merged_payload = _merged_json_payload(source_path, target_path)
    rendered = json.dumps(merged_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    target_path.write_text(rendered, encoding="utf-8")


def _merge_mcp_json(source_payload: dict[str, Any], target_payload: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(target_payload)
    source_servers = source_payload.get("mcpServers")
    if not isinstance(source_servers, dict):
        raise ConfigError("mcp.json invalido: mcpServers deve ser um objeto")

    target_servers = merged.get("mcpServers")
    if target_servers is None:
        target_servers = {}
    if not isinstance(target_servers, dict):
        raise ConfigError("mcp.json invalido: mcpServers local deve ser um objeto")

    merged_servers = dict(target_servers)
    for key, value in source_servers.items():
        merged_servers[key] = value

    merged["mcpServers"] = merged_servers
    return merged


def _merged_json_payload(source_path: Path, target_path: Path) -> dict[str, Any]:
    source_payload = _load_json_object(source_path)
    target_payload: dict[str, Any] = {}
    if target_path.exists():
        target_payload = _load_json_object(target_path)
    return _merge_mcp_json(source_payload, target_payload)


def _load_json_object(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    payload = json.loads(content)
    if not isinstance(payload, dict):
        raise ConfigError(f"JSON invalido em {path}: esperava um objeto")
    return payload


def _needs_symlink_update(source_path: Path, target_path: Path) -> bool:
    if not target_path.exists() and not target_path.is_symlink():
        return True

    if not target_path.is_symlink():
        return True

    current_target = Path(os.readlink(target_path))
    return current_target != Path("AGENTS.md")


def _remove_target(project_root: Path, target: str) -> None:
    target_path = project_root / target
    if target_path.is_symlink() or target_path.is_file():
        target_path.unlink(missing_ok=True)
        return
    if target_path.exists():
        shutil.rmtree(target_path)


def _ensure_parent(target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()
