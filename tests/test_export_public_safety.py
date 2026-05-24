"""Safety tests for the LCOS publication export mechanism.

Where ``test_public_boundary.py`` asserts which content is excluded,
these tests assert mechanism-level safety properties: symlink handling,
strict vs. collect mode, determinism, idempotency, non-mutation of
source, and failure modes for malformed inputs.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from lcos_public.publication import (
    PublicationBoundaryViolation,
    export_public_paper_surface,
)


class _SafetyTestBase(unittest.TestCase):
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


class SymlinkSafetyTests(_SafetyTestBase):
    """Symlinks in source_root must never be followed for export."""

    def test_symlink_file_inside_source_emits_hold_and_skips(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")
        target = self.source / "target.md"
        target.write_text("target content\n", encoding="utf-8")
        link = self.source / "link.md"
        link.symlink_to(target)

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / "link.md").is_symlink())
        self.assertFalse((self.destination / "link.md").exists())
        self.assertTrue(any(h.reason.startswith("symlink") for h in result.holds))

    def test_symlink_to_private_substrate_emits_hold(self) -> None:
        """Symlink pointing at a SKOS-style path must be held, not followed."""
        self._write("paper.md", "# Title\nPublic text.\n")
        link = self.source / "secret_link.md"
        link.symlink_to("/SKOS-Core/imaginary/secret.md")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertFalse((self.destination / "secret_link.md").exists())
        self.assertTrue(any(h.reason.startswith("symlink") for h in result.holds))


class StrictVsCollectModeTests(_SafetyTestBase):
    def test_strict_mode_raises_on_any_hold(self) -> None:
        self._write("paper.md", "# Title\nrefs /SKOS-Core/private\n")

        with self.assertRaises(PublicationBoundaryViolation) as ctx:
            export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertGreaterEqual(len(ctx.exception.holds), 1)

    def test_collect_mode_returns_holds_without_raising(self) -> None:
        self._write("paper.md", "# Title\nrefs /SKOS-Core/private\n")
        self._write("clean.md", "# Clean\nPublic only.\n")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertGreaterEqual(len(result.holds), 1)
        self.assertTrue((self.destination / "clean.md").exists())
        self.assertFalse((self.destination / "paper.md").exists())


class DeterminismTests(_SafetyTestBase):
    def test_two_runs_produce_same_outputs(self) -> None:
        self._write("a.md", "# A\nPublic A.\n")
        self._write("b.md", "# B\nPublic B.\n")
        self._write("nested/c.md", "# C\nPublic C.\n")

        result1 = export_public_paper_surface(self.source, self.destination, strict=True)

        out1 = {
            str(p.relative_to(self.destination)): p.read_text(encoding="utf-8")
            for p in self.destination.rglob("*")
            if p.is_file()
        }

        for p in self.destination.rglob("*"):
            if p.is_file():
                p.unlink()

        result2 = export_public_paper_surface(self.source, self.destination, strict=True)

        out2 = {
            str(p.relative_to(self.destination)): p.read_text(encoding="utf-8")
            for p in self.destination.rglob("*")
            if p.is_file()
        }

        self.assertEqual(out1, out2)
        self.assertEqual(result1.exported_files, result2.exported_files)
        self.assertEqual(result1.redacted_lines, result2.redacted_lines)


class IdempotencyTests(_SafetyTestBase):
    def test_repeated_export_to_same_destination_converges(self) -> None:
        self._write("paper.md", "# Title\nPublic text.\n")

        result1 = export_public_paper_surface(self.source, self.destination, strict=True)
        first_snapshot = {
            str(p.relative_to(self.destination)): p.read_text(encoding="utf-8")
            for p in self.destination.rglob("*")
            if p.is_file()
        }

        result2 = export_public_paper_surface(self.source, self.destination, strict=True)
        second_snapshot = {
            str(p.relative_to(self.destination)): p.read_text(encoding="utf-8")
            for p in self.destination.rglob("*")
            if p.is_file()
        }

        self.assertEqual(first_snapshot, second_snapshot)
        self.assertEqual(result1.exported_files, result2.exported_files)


class SourceNonMutationTests(_SafetyTestBase):
    def test_source_files_not_modified_on_clean_export(self) -> None:
        content = "# Title\nPublic text.\n"
        path = self._write("paper.md", content)

        export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_source_files_not_modified_on_held_export(self) -> None:
        content = "# Title\nrefs /SKOS-Core/x\n"
        path = self._write("paper.md", content)

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertGreaterEqual(len(result.holds), 1)
        self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_source_files_not_modified_when_strict_raises(self) -> None:
        content = "# Title\nrefs /SKOS-Core/x\n"
        path = self._write("paper.md", content)

        with self.assertRaises(PublicationBoundaryViolation):
            export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertEqual(path.read_text(encoding="utf-8"), content)


class MalformedInputTests(_SafetyTestBase):
    def test_missing_source_raises_filenotfounderror(self) -> None:
        missing = self.root / "does_not_exist"

        with self.assertRaises(FileNotFoundError):
            export_public_paper_surface(missing, self.destination, strict=True)

    def test_non_utf8_text_suffix_file_is_held(self) -> None:
        binary_bytes = b"\xff\xfe\x00\x00not utf-8"
        path = self.source / "broken.md"
        path.write_bytes(binary_bytes)

        with self.assertRaises(PublicationBoundaryViolation) as ctx:
            export_public_paper_surface(self.source, self.destination, strict=True)

        self.assertTrue(
            any("utf-8" in h.reason for h in ctx.exception.holds)
        )


class HoldDecisionShapeTests(_SafetyTestBase):
    """The HOLD records returned must be Decision-typed and carry evidence."""

    def test_hold_has_decision_kind_and_evidence(self) -> None:
        self._write("paper.md", "# Title\nrefs /SKOS-Core/x\n")

        result = export_public_paper_surface(self.source, self.destination, strict=False)

        self.assertEqual(len(result.holds), 1)
        hold = result.holds[0]
        self.assertEqual(hold.kind, "HOLD")
        self.assertTrue(hold.reason)
        self.assertGreaterEqual(len(hold.evidence), 1)


if __name__ == "__main__":
    unittest.main()
