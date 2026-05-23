from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_REDACTION_MARKERS = (
    "**Source lineage:**",
    "imported into LCOS-Core from the SKOS-Core",
)


@dataclass(frozen=True)
class ExportResult:
    source_root: Path
    destination_root: Path
    exported_files: int
    redacted_lines: int


def _sanitize_text(text: str, markers: tuple[str, ...]) -> tuple[str, int]:
    kept: list[str] = []
    removed = 0
    for line in text.splitlines():
        if any(marker in line for marker in markers):
            removed += 1
            continue
        kept.append(line)
    sanitized = "\n".join(kept)
    if text.endswith("\n") and sanitized:
        sanitized += "\n"
    return sanitized, removed


def export_public_paper_surface(
    source_root: Path,
    destination_root: Path,
    redaction_markers: tuple[str, ...] = DEFAULT_REDACTION_MARKERS,
) -> ExportResult:
    """Copy a public paper surface into a sanitized export tree.

    The source tree is left untouched. Textual files are copied with any line
    containing a redaction marker removed from the exported copy.
    """

    source_root = source_root.resolve()
    destination_root = destination_root.resolve()
    exported_files = 0
    redacted_lines = 0

    if not source_root.is_dir():
        raise FileNotFoundError(source_root)

    for path in source_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source_root)
        target = destination_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix.lower() in {".md", ".txt", ".rst", ".yaml", ".yml", ".tex"}:
            sanitized, removed = _sanitize_text(path.read_text(encoding="utf-8"), redaction_markers)
            target.write_text(sanitized, encoding="utf-8")
            redacted_lines += removed
        else:
            target.write_bytes(path.read_bytes())
        exported_files += 1

    return ExportResult(
        source_root=source_root,
        destination_root=destination_root,
        exported_files=exported_files,
        redacted_lines=redacted_lines,
    )
