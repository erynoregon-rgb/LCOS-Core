import json
import unittest

from lcos_toy.ledger import AppendOnlyLedger


class LedgerTests(unittest.TestCase):
    def test_append_only_chain_verifies(self):
        with self.subTest("valid chain"):
            import tempfile
            from pathlib import Path

            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "ledger.jsonl"
                ledger = AppendOnlyLedger(path)
                ledger.append("A", {"value": 1}, timestamp="2026-01-01T00:00:00+00:00")
                ledger.append("B", {"value": 2}, timestamp="2026-01-01T00:00:01+00:00")
                report = ledger.verify()
                self.assertTrue(report.valid)
                self.assertEqual(report.count, 2)

    def test_payload_tamper_is_detected(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            ledger = AppendOnlyLedger(path)
            ledger.append("A", {"value": 1}, timestamp="2026-01-01T00:00:00+00:00")
            record = json.loads(path.read_text().strip())
            record["payload"]["value"] = 99
            path.write_text(json.dumps(record) + "\n")
            report = ledger.verify()
            self.assertFalse(report.valid)
            self.assertEqual(report.issues[0].code, "PAYLOAD_TAMPERED")

    def test_missing_ledger_can_fail_in_strict_mode(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.jsonl"
            report = AppendOnlyLedger(path).verify(strict=True)
            self.assertFalse(report.valid)
            self.assertEqual(report.issues[0].code, "MISSING_LEDGER")

    def test_malformed_json_returns_structured_issue(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            path.write_text("{not-json}\n", encoding="utf-8")
            report = AppendOnlyLedger(path).verify()
            self.assertFalse(report.valid)
            self.assertEqual(report.issues[0].code, "MALFORMED_JSON")


if __name__ == "__main__":
    unittest.main()
