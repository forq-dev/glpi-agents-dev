from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from glpi_agents_sync.models import SyncEntry

DEFAULT_SOURCE_REPOSITORY = "https://github.com/msouza10/glpi-agents-dev.git"


class SourceFetchError(RuntimeError):
    """Erro ao obter a arvore do repositorio-fonte."""


@dataclass(frozen=True, slots=True)
class SourceTree:
    root: Path
    ref: str


def clone_source_tree(source_repo: str, source_ref: str | None) -> SourceTree:
    temp_dir = Path(tempfile.mkdtemp(prefix="glpi-agents-sync-"))
    clone_command = ["git", "clone", "--depth", "1"]
    if source_ref is not None:
        clone_command.extend(["--branch", source_ref])
    clone_command.extend([source_repo, str(temp_dir)])

    try:
        completed = subprocess.run(
            clone_command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise SourceFetchError("Git nao encontrado no PATH do ambiente atual.") from exc

    if completed.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise SourceFetchError(
            "Falha ao clonar o repositorio-fonte "
            f"{source_repo!r} na ref {source_ref!r}: {completed.stderr.strip()}"
        )

    effective_ref = source_ref if source_ref is not None else detect_checked_out_ref(temp_dir)
    return SourceTree(root=temp_dir, ref=effective_ref)


def detect_checked_out_ref(source_root: Path) -> str:
    command = [
        "git",
        "-C",
        str(source_root),
        "symbolic-ref",
        "--short",
        "HEAD",
    ]

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SourceFetchError("Git nao encontrado no PATH do ambiente atual.") from exc

    if completed.returncode != 0:
        raise SourceFetchError(
            "Nao foi possivel detectar a ref padrao do repositorio-fonte "
            f"em {source_root}: {completed.stderr.strip()}"
        )

    detected_ref = completed.stdout.strip()
    if not detected_ref:
        raise SourceFetchError(
            f"Ref padrao vazia detectada para o repositorio-fonte em {source_root}"
        )

    return detected_ref


def cleanup_source_tree(source_tree: SourceTree) -> None:
    shutil.rmtree(source_tree.root, ignore_errors=True)


def list_source_entries(source_root: Path) -> tuple[SyncEntry, ...]:
    entries: list[SyncEntry] = []

    agents_root = source_root / ".agents"
    if agents_root.exists():
        entries.extend(_walk_tree_entries(agents_root, ".agents"))

    entries.append(
        SyncEntry(
            source="system-prompts/AGENTS.md",
            target="AGENTS.md",
            kind="copy",
            state="active",
        )
    )
    entries.append(
        SyncEntry(
            source="system-prompts/AGENTS.md",
            target="CLAUDE.md",
            kind="symlink",
            state="active",
        )
    )
    entries.append(
        SyncEntry(
            source="mcp.json",
            target="mcp.json",
            kind="json_merge",
            state="active",
        )
    )
    entries.append(
        SyncEntry(
            source="mcp.json",
            target=".mcp.json",
            kind="json_merge",
            state="active",
        )
    )

    return tuple(entries)


def _walk_tree_entries(root: Path, prefix: str) -> list[SyncEntry]:
    entries: list[SyncEntry] = []
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        relative_path = file_path.relative_to(root)
        source = str(Path(prefix) / relative_path)
        entries.append(
            SyncEntry(
                source=source,
                target=source,
                kind="copy",
                state="active",
            )
        )
    return entries
