"""Boundary tests for the LCOS publication export surface.

These tests assert that content which requires SKOS-private context never
crosses the public publication boundary. The companion safety tests in
``test_export_public_safety.py`` cover mechanism-level guarantees
(symlinks, determinism, non-mutation, strict vs. collect mode).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from lcos_public.publication import (
    PublicationBoundaryViolation,
    export_public_paper_surface,
)


class _BoundaryTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.source = self.root / "paper_surface"
        self.destination = self.root / "exported_public"
        self.source.mkdir()

    def _write(self, relative: str, content: str) -> Path:
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


class SkippedDirectoryBoundaryTests(_BoundaryTestBase):
    """Hidden / generated directories under source_root must not be exported."""

    def test_git_directory_is_skipped(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write(".git/config", "[remote]\n    url = https://example/x\n")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / ".git" / "config").exists())
        self.assertTrue((self.destination / "paper.md").exists())
        self.assertEqual(result.exported_files, 1)
        self.assertGreaterEqual(len(result.warnings), 1)

    def test_skos_audit_directory_is_skipped(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write(".skos-audit/event.jsonl", '{"kind": "internal"}\n')

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / ".skos-audit" / "event.jsonl").exists())
        self.assertEqual(result.exported_files, 1)

    def test_claude_directory_is_skipped(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write(".claude/SESSION_HYDRATION.md", "private session frame\n")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / ".claude" / "SESSION_HYDRATION.md").exists())
        self.assertEqual(result.exported_files, 1)

    def test_worktrees_directory_is_skipped(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write(".worktrees/wip/file.md", "private worktree\n")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / ".worktrees").exists())
        self.assertEqual(result.exported_files, 1)

    def test_pycache_directory_is_skipped(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write("__pycache__/x.cpython-313.pyc", "bytecode")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / "__pycache__").exists())
        self.assertEqual(result.exported_files, 1)


class ForbiddenFilenameBoundaryTests(_BoundaryTestBase):
    """Filenames containing substrate-identifying fragments must not export."""

    def test_filename_containing_source_lineage_holds(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write("source_lineage_notes.md", "Notes about lineage.\n")

        with self.assertRaises(PublicationBoundaryViolation) as ctx:
            export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertTrue(any("source_lineage" in (h.reason + " ".join(h.evidence)) for h in ctx.exception.holds))

    def test_filename_containing_skos_audit_holds(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        self._write("skos_audit_log.txt", "audit trail\n")

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)


class ForbiddenContentBoundaryTests(_BoundaryTestBase):
    """Content matching forbidden substrate patterns must not cross.

    Patterns are checked AFTER redaction-marker stripping so the existing
    Source-lineage redaction behavior is unchanged.
    """

    def test_skos_core_path_in_markdown_holds(self) -> None:
        self._write(
            "paper.md",
            "# Title\nSee /SKOS-Core/private/note for details.\n",
        )

        with self.assertRaises(PublicationBoundaryViolation) as ctx:
            export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertTrue(
            any("/SKOS-Core/" in tuple(h.evidence) for h in ctx.exception.holds)
        )

    def test_skos_audit_path_in_content_holds(self) -> None:
        self._write("paper.md", "# Title\nrefs .skos-audit/event.jsonl\n")

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_workboard_packets_path_holds(self) -> None:
        self._write("paper.md", "# Title\nfrom workboard/packets/stability/X.md\n")

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_var_governance_path_holds(self) -> None:
        self._write("paper.md", "# Title\nsee var/governance/parsed/x.json\n")

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_tools_governance_path_holds(self) -> None:
        self._write("paper.md", "# Title\nrun tools/governance/foo.py\n")

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_worktrees_path_in_content_holds(self) -> None:
        self._write("paper.md", "# Title\nsee .worktrees/wip\n")

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)


class JsonAndCodeFileSanitizationTests(_BoundaryTestBase):
    """File types beyond .md/.txt/.rst/.yaml/.tex must also be scanned.

    The pre-hardening implementation passed .json, .py, .html etc. through
    as bytes — any SKOS-internal path inside them would leak verbatim.
    """

    def test_json_file_with_skos_path_holds(self) -> None:
        self._write(
            "data.json",
            '{"ref": "/SKOS-Core/secret"}\n',
        )

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_py_file_with_skos_audit_path_holds(self) -> None:
        self._write(
            "example.py",
            "PATH = '.skos-audit/event.jsonl'\n",
        )

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_html_file_with_forbidden_path_holds(self) -> None:
        self._write(
            "page.html",
            "<a href=\"/SKOS-Core/x\">link</a>\n",
        )

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

    def test_toml_file_with_skos_path_holds(self) -> None:
        self._write(
            "config.toml",
            'path = "/SKOS-Core/x"\n',
        )

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)


class CleanContentPassthroughTests(_BoundaryTestBase):
    """Public-safe content must still export successfully without holds."""

    def test_clean_markdown_exports_with_no_holds(self) -> None:
        self._write("paper.md", "# Title\nPublic text only.\n")
        self._write("note.md", "Public note.\n")

        result = export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertEqual(result.exported_files, 2)
        self.assertEqual(result.redacted_lines, 0)
        self.assertEqual(result.holds, ())

    def test_redacted_lineage_alone_is_not_a_hold(self) -> None:
        """A Source-lineage line gets stripped silently. It is NOT a hold."""
        self._write(
            "paper.md",
            "# Title\n"
            "**Source lineage:** imported into LCOS-Core from the SKOS-Core package on 2026-05-19\n"
            "Public text.\n",
        )

        result = export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertEqual(result.exported_files, 1)
        self.assertEqual(result.redacted_lines, 1)
        self.assertEqual(result.holds, ())


if __name__ == "__main__":
    unittest.main()
