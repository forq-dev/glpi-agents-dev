from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from glpi_agents_sync.models import SyncEntry, SyncManifest

CONFIG_FILENAME = ".agents-sync.json"


class ConfigError(RuntimeError):
    """Erro ao ler ou escrever a configuracao de sincronizacao."""


def config_path_for(project_root: Path) -> Path:
    return project_root / CONFIG_FILENAME


def manifest_to_dict(manifest: SyncManifest) -> dict[str, Any]:
    return {
        "version": 1,
        "source_repo": manifest.source_repo,
        "source_ref": manifest.source_ref,
        "generated_at": manifest.generated_at,
        "entries": [asdict(entry) for entry in manifest.entries],
    }


def manifest_from_dict(payload: dict[str, Any]) -> SyncManifest:
    version = payload.get("version")
    if version != 1:
        raise ConfigError(f"Versao de manifesto nao suportada: {version!r}")

    source_repo = payload.get("source_repo")
    source_ref = payload.get("source_ref")
    generated_at = payload.get("generated_at")
    entries_payload = payload.get("entries")

    if not isinstance(source_repo, str) or not isinstance(source_ref, str):
        raise ConfigError("Manifesto invalido: source_repo/source_ref ausentes")

    if not isinstance(generated_at, str):
        raise ConfigError("Manifesto invalido: generated_at ausente")

    if not isinstance(entries_payload, list):
        raise ConfigError("Manifesto invalido: entries deve ser uma lista")

    entries: list[SyncEntry] = []
    for raw_entry in entries_payload:
        if not isinstance(raw_entry, dict):
            raise ConfigError("Manifesto invalido: entrada de entries nao e objeto")

        source = raw_entry.get("source")
        target = raw_entry.get("target")
        kind = raw_entry.get("kind")
        state = raw_entry.get("state")

        if not isinstance(source, str) or not isinstance(target, str):
            raise ConfigError("Manifesto invalido: source/target ausentes")

        if not isinstance(kind, str) or not isinstance(state, str):
            raise ConfigError("Manifesto invalido: kind/state ausentes")

        if kind not in {"copy", "json_merge", "symlink"}:
            raise ConfigError(f"Manifesto invalido: kind desconhecido {kind!r}")

        if state not in {"active", "pending_removal"}:
            raise ConfigError(f"Manifesto invalido: state desconhecido {state!r}")

        entries.append(SyncEntry(source=source, target=target, kind=kind, state=state))

    return SyncManifest(
        source_repo=source_repo,
        source_ref=source_ref,
        generated_at=generated_at,
        entries=tuple(entries),
    )


def load_manifest(project_root: Path) -> SyncManifest:
    path = config_path_for(project_root)
    if not path.exists():
        raise ConfigError(
            f"Arquivo de configuracao nao encontrado: {path}. Execute bootstrap primeiro."
        )

    content = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"JSON invalido em {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise ConfigError(f"Manifesto invalido em {path}: esperava um objeto JSON")

    return manifest_from_dict(payload)


def write_manifest(project_root: Path, manifest: SyncManifest) -> None:
    path = config_path_for(project_root)
    payload = manifest_to_dict(manifest)
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(rendered, encoding="utf-8")
