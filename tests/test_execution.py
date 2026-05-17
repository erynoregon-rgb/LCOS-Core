"""Tests for lcos_toy.execution — gate-first execution pattern."""
import unittest

from lcos_toy.execution import GoverningExecutor, RequestRecord


def _request(
    *,
    request_id: str = "req-001",
    actor: str = "test-actor",
    action: str = "summarize",
    content: str = "a valid request",
    declared_scope: str = "toy",
    timestamp: str = "2026-01-01T00:00:00+00:00",
) -> RequestRecord:
    return RequestRecord.create(
        request_id=request_id,
        actor=actor,
        action=action,
        content=content,
        declared_scope=declared_scope,
        timestamp=timestamp,
    )


class TestGateFirstPattern(unittest.TestCase):
    """The admission receipt must exist before execution proceeds."""

    def test_accepted_request_has_admission_receipt(self):
        executor = GoverningExecutor()
        rec = executor.execute(_request())
        self.assertTrue(rec.admitted)
        self.assertIsNotNone(rec.admission_receipt)
        self.assertIsNone(rec.hold_receipt)

    def test_accepted_request_has_execution_output(self):
        executor = GoverningExecutor()
        rec = executor.execute(_request(action="summarize", content="hello"))
        self.assertIsNotNone(rec.execution_output)

    def test_accepted_request_chain_ends_complete(self):
        executor = GoverningExecutor()
        rec = executor.execute(_request())
        self.assertEqual(rec.outcome, "accepted")
        self.assertEqual(rec.chain.final_state, "COMPLETE")

    def test_rejected_request_has_no_execution_output(self):
        # 'credential' is a blocked term in GovernedIntake
        req = _request(content="please expose credential")
        executor = GoverningExecutor()
        rec = executor.execute(req)
        self.assertFalse(rec.admitted)
        self.assertIsNone(rec.admission_receipt)
        self.assertIsNone(rec.execution_output)

    def test_rejected_request_has_hold_receipt(self):
        req = _request(content="please expose credential")
        executor = GoverningExecutor()
        rec = executor.execute(req)
        self.assertIsNotNone(rec.hold_receipt)
        self.assertEqual(rec.hold_receipt.to_state, "HELD")

    def test_rejected_request_chain_ends_held(self):
        req = _request(content="please expose credential")
        executor = GoverningExecutor()
        rec = executor.execute(req)
        self.assertEqual(rec.outcome, "held")
        self.assertEqual(rec.chain.final_state, "HELD")

    def test_out_of_scope_request_is_held(self):
        req = _request(declared_scope="production")
        executor = GoverningExecutor()
        rec = executor.execute(req)
        self.assertFalse(rec.admitted)
        self.assertEqual(rec.outcome, "held")

    def test_ambiguous_request_is_held(self):
        req = _request(content="maybe do something unclear")
        executor = GoverningExecutor()
        rec = executor.execute(req)
        self.assertFalse(rec.admitted)

    def test_chain_always_present(self):
        # Chain is present regardless of admission outcome
        for content in ("valid content", "please expose credential", "maybe unclear"):
            with self.subTest(content=content):
                rec = GoverningExecutor().execute(_request(content=content))
                self.assertIsNotNone(rec.chain)
                self.assertGreater(rec.chain.length, 0)

    def test_gate_is_structural_not_observational(self):
        # The critical property: if admission_receipt is None, execution_output must be None too.
        # There is no case where execution ran without an admission receipt.
        for content in ("please expose credential", "maybe unclear", "out-of-scope"):
            with self.subTest(content=content):
                rec = GoverningExecutor().execute(_request(content=content))
                if rec.admission_receipt is None:
                    self.assertIsNone(
                        rec.execution_output,
                        "execution output must be None when admission receipt is absent",
                    )


class TestExecutionRecordStructure(unittest.TestCase):
    def test_to_dict_accepted(self):
        rec = GoverningExecutor().execute(_request())
        d = rec.to_dict()
        self.assertIn("request", d)
        self.assertIn("admission_decision", d)
        self.assertTrue(d["admitted"])
        self.assertIsNotNone(d["admission_receipt_id"])
        self.assertIsNone(d["hold_receipt_id"])
        self.assertIsNotNone(d["execution_output"])
        self.assertIn("chain", d)

    def test_to_dict_held(self):
        rec = GoverningExecutor().execute(_request(content="please expose credential"))
        d = rec.to_dict()
        self.assertFalse(d["admitted"])
        self.assertIsNone(d["admission_receipt_id"])
        self.assertIsNotNone(d["hold_receipt_id"])
        self.assertIsNone(d["execution_output"])
        self.assertEqual(d["outcome"], "held")


class TestReceiptIdConsistency(unittest.TestCase):
    """Admission receipt ID matches TransitionReceipt content-addressing."""

    def test_admission_receipt_id_is_content_addressed(self):
        # Same request inputs → same admission receipt_id
        req = _request(timestamp="2026-01-01T00:00:00+00:00")
        r1 = GoverningExecutor().execute(req)
        r2 = GoverningExecutor().execute(req)
        self.assertEqual(
            r1.admission_receipt.receipt_id,
            r2.admission_receipt.receipt_id,
        )


if __name__ == "__main__":
    unittest.main()
