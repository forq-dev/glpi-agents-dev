from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

EntryKind = Literal["copy", "json_merge", "symlink"]
EntryState = Literal["active", "pending_removal"]


@dataclass(frozen=True, slots=True)
class SyncEntry:
    source: str
    target: str
    kind: EntryKind
    state: EntryState


@dataclass(frozen=True, slots=True)
class SyncManifest:
    source_repo: str
    source_ref: str
    generated_at: str
    entries: tuple[SyncEntry, ...]

