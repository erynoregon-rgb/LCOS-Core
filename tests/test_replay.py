import tempfile
from pathlib import Path
import unittest

from lcos_toy.ledger import AppendOnlyLedger
from lcos_toy.replay import render_timeline


class ReplayTests(unittest.TestCase):
    def test_replay_renders_timeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            ledger = AppendOnlyLedger(path)
            ledger.append("INTAKE", {"id": "one"}, timestamp="2026-01-01T00:00:00+00:00")
            timeline = render_timeline(path)
            self.assertIn("seq | event_type", timeline)
            self.assertIn("INTAKE", timeline)
            self.assertIn("valid=true", timeline)


if __name__ == "__main__":
    unittest.main()

