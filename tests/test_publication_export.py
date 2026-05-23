from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from lcos_public.publication import export_public_paper_surface


class PublicationExportTests(unittest.TestCase):
    def test_export_strips_source_lineage_without_mutating_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "paper_surface"
            destination = root / "exported_public"
            source.mkdir()

            paper = source / "paper.md"
            paper.write_text(
                "\n".join(
                    [
                        "# Title",
                        "**Status:** public research draft",
                        "**Source lineage:** imported into LCOS-Core from the SKOS-Core package on 2026-05-19",
                        "",
                        "## Abstract",
                        "Public text only.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            note = source / "publication_note.md"
            note.write_text("Public note.\n", encoding="utf-8")

            result = export_public_paper_surface(source, destination)

            self.assertEqual(result.exported_files, 2)
            self.assertEqual(result.redacted_lines, 1)
            self.assertEqual(
                paper.read_text(encoding="utf-8"),
                "\n".join(
                    [
                        "# Title",
                        "**Status:** public research draft",
                        "**Source lineage:** imported into LCOS-Core from the SKOS-Core package on 2026-05-19",
                        "",
                        "## Abstract",
                        "Public text only.",
                    ]
                )
                + "\n",
            )
            exported_paper = (destination / "paper.md").read_text(encoding="utf-8")
            self.assertNotIn("Source lineage", exported_paper)
            self.assertIn("# Title", exported_paper)
            self.assertEqual((destination / "publication_note.md").read_text(encoding="utf-8"), "Public note.\n")


if __name__ == "__main__":
    unittest.main()
