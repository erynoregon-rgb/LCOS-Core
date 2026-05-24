from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .decision import Decision


DEFAULT_REDACTION_MARKERS: tuple[str, ...] = (
    "**Source lineage:**",
    "imported into LCOS-Core from the SKOS-Core",
)

DEFAULT_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "/SKOS-Core/",
    ".skos-audit",
    ".worktrees/",
    "workboard/packets/",
    "workboard/artifacts/",
    "var/governance/",
    "tools/governance/",
)

DEFAULT_SKIP_DIRECTORIES: frozenset[str] = frozenset({
    ".git",
    ".skos-audit",
    ".claude",
    ".worktrees",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "node_modules",
})

DEFAULT_SANITIZE_SUFFIXES: frozenset[str] = frozenset({
    ".md", ".txt", ".rst", ".yaml", ".yml", ".tex",
    ".json", ".jsonl", ".html", ".htm", ".css", ".js",
    ".py", ".toml", ".ini", ".cfg", ".sh", ".env",
    ".csv", ".tsv", ".xml",
})

DEFAULT_FORBIDDEN_FILENAME_FRAGMENTS: tuple[str, ...] = (
    "source_lineage",
    "skos_audit",
)


class PublicationBoundaryViolation(Exception):
    """Raised when strict-mode export detects forbidden content.

    The ``holds`` attribute carries the typed Decision records that
    triggered the failure so the caller can route them into a receipt.
    """

    def __init__(self, message: str, holds: tuple[Decision, ...]) -> None:
        super().__init__(message)
        self.holds = holds


@dataclass(frozen=True)
class ExportResult:
    source_root: Path
    destination_root: Path
    exported_files: int
    redacted_lines: int
    skipped_files: tuple[Path, ...] = ()
    holds: tuple[Decision, ...] = ()
    warnings: tuple[Decision, ...] = ()


def _has_skip_directory_in_path(relative: Path, skip_directories: frozenset[str]) -> str | None:
    for part in relative.parts:
        if part in skip_directories:
            return part
    return None


def _filename_has_forbidden_fragment(name: str, fragments: tuple[str, ...]) -> str | None:
    lowered = name.lower()
    for fragment in fragments:
        if fragment in lowered:
            return fragment
    return None


def _sanitize_text(
    text: str, redaction_markers: tuple[str, ...]
) -> tuple[str, int]:
    kept: list[str] = []
    removed = 0
    for line in text.splitlines():
        if any(marker in line for marker in redaction_markers):
            removed += 1
            continue
        kept.append(line)
    sanitized = "\n".join(kept)
    if text.endswith("\n") and sanitized:
        sanitized += "\n"
    return sanitized, removed


def _scan_for_forbidden_patterns(
    text: str, patterns: tuple[str, ...]
) -> list[str]:
    matched: list[str] = []
    for pattern in patterns:
        if pattern in text:
            matched.append(pattern)
    return matched


def export_public_paper_surface(
    source_root: Path,
    destination_root: Path,
    redaction_markers: tuple[str, ...] = DEFAULT_REDACTION_MARKERS,
    forbidden_patterns: tuple[str, ...] = DEFAULT_FORBIDDEN_PATTERNS,
    skip_directories: frozenset[str] = DEFAULT_SKIP_DIRECTORIES,
    sanitize_suffixes: frozenset[str] = DEFAULT_SANITIZE_SUFFIXES,
    forbidden_filename_fragments: tuple[str, ...] = DEFAULT_FORBIDDEN_FILENAME_FRAGMENTS,
    strict: bool = True,
) -> ExportResult:
    """Copy a public paper surface into a sanitized export tree.

    The source tree is left untouched. Files are walked in sorted order for
    deterministic output.

    Lines matching ``redaction_markers`` are stripped silently from text
    files (the existing happy-path behavior). Content matching
    ``forbidden_patterns`` after redaction generates a typed HOLD Decision.

    Symlinks, files inside ``skip_directories``, and files whose names
    contain ``forbidden_filename_fragments`` generate HOLD or warning
    Decisions and are not exported.

    File types in ``sanitize_suffixes`` are sanitized as text. Other file
    types are copied as bytes only if the path is not held; their content
    is not scanned.

    In ``strict=True`` mode (default) any HOLD raises
    ``PublicationBoundaryViolation`` after the walk completes.
    In ``strict=False`` mode the export proceeds and returns the holds in
    the result for the caller to route.
    """

    source_root = source_root.resolve()
    destination_root = destination_root.resolve()

    if not source_root.is_dir():
        raise FileNotFoundError(source_root)

    exported_files = 0
    redacted_lines = 0
    skipped: list[Path] = []
    holds: list[Decision] = []
    warnings: list[Decision] = []

    all_paths: Iterable[Path] = sorted(source_root.rglob("*"))

    for path in all_paths:
        relative = path.relative_to(source_root)

        if path.is_symlink():
            holds.append(
                Decision(
                    kind="HOLD",
                    reason="symlink encountered in publication source",
                    evidence=(str(relative),),
                )
            )
            skipped.append(relative)
            continue

        if not path.is_file():
            continue

        skip_match = _has_skip_directory_in_path(relative, skip_directories)
        if skip_match is not None:
            warnings.append(
                Decision(
                    kind="HOLD",
                    reason=f"path under skipped directory '{skip_match}'",
                    evidence=(str(relative),),
                )
            )
            skipped.append(relative)
            continue

        filename_fragment = _filename_has_forbidden_fragment(
            path.name, forbidden_filename_fragments
        )
        if filename_fragment is not None:
            holds.append(
                Decision(
                    kind="HOLD",
                    reason=f"filename contains forbidden fragment '{filename_fragment}'",
                    evidence=(str(relative),),
                )
            )
            skipped.append(relative)
            continue

        target = destination_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix.lower() in sanitize_suffixes:
            try:
                raw_text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                holds.append(
                    Decision(
                        kind="HOLD",
                        reason="text-suffix file is not valid utf-8",
                        evidence=(str(relative),),
                    )
                )
                skipped.append(relative)
                continue

            sanitized, removed = _sanitize_text(raw_text, redaction_markers)
            redacted_lines += removed

            forbidden_hits = _scan_for_forbidden_patterns(sanitized, forbidden_patterns)
            if forbidden_hits:
                holds.append(
                    Decision(
                        kind="HOLD",
                        reason="forbidden substrate patterns detected in sanitized content",
                        evidence=(str(relative), *forbidden_hits),
                    )
                )
                skipped.append(relative)
                continue

            target.write_text(sanitized, encoding="utf-8")
        else:
            target.write_bytes(path.read_bytes())

        exported_files += 1

    holds_t = tuple(holds)
    warnings_t = tuple(warnings)

    if strict and holds_t:
        raise PublicationBoundaryViolation(
            f"publication boundary violations detected: {len(holds_t)} hold(s)",
            holds_t,
        )

    return ExportResult(
        source_root=source_root,
        destination_root=destination_root,
        exported_files=exported_files,
        redacted_lines=redacted_lines,
        skipped_files=tuple(skipped),
        holds=holds_t,
        warnings=warnings_t,
    )
