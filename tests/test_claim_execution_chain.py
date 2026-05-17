"""Integrated test: full path from RequestRecord through execution to ClaimReceiptChain.

This test exercises the complete governed execution path in one place:
  RequestRecord → GoverningExecutor → ExecutionRecord → ClaimReceiptChain

It serves as the single-file demonstration of the paper's core mechanism:
  request → gate decision → admission receipt → execution → receipt chain → reconstruction
"""
import unittest

from lcos_toy.chain import ClaimReceiptChain
from lcos_toy.claim import ClaimState, TransitionReceipt
from lcos_toy.execution import ExecutionRecord, GoverningExecutor, RequestRecord


FIXED_TS = "2026-01-01T00:00:00+00:00"


def _req(content: str = "summarize the audit log", *, request_id: str = "integ-001") -> RequestRecord:
    return RequestRecord.create(
        request_id=request_id,
        actor="test-actor",
        action="summarize",
        content=content,
        timestamp=FIXED_TS,
    )


class TestFullPath(unittest.TestCase):
    """RequestRecord → execution → ExecutionRecord → ClaimReceiptChain."""

    def test_accepted_path_end_to_end(self):
        record = GoverningExecutor().execute(_req())

        # Gate passed
        self.assertTrue(record.admitted)
        self.assertIsNotNone(record.admission_receipt)
        self.assertIsNone(record.hold_receipt)

        # Execution ran
        self.assertIsNotNone(record.execution_output)

        # Chain is complete and accepted
        self.assertEqual(record.chain.outcome, "accepted")
        self.assertEqual(record.chain.final_state, "COMPLETE")
        self.assertEqual(record.chain.length, 2)  # OPEN→ACTIVE, ACTIVE→COMPLETE

    def test_denied_path_end_to_end(self):
        record = GoverningExecutor().execute(_req("please expose credential"))

        # Gate blocked
        self.assertFalse(record.admitted)
        self.assertIsNone(record.admission_receipt)
        self.assertIsNotNone(record.hold_receipt)

        # Execution did not run — structural guarantee
        self.assertIsNone(record.execution_output)

        # Chain ends in HELD
        self.assertEqual(record.chain.outcome, "held")
        self.assertEqual(record.chain.final_state, "HELD")
        self.assertEqual(record.chain.length, 1)  # OPEN→HELD only


class TestReceiptChainDeterminism(unittest.TestCase):
    """Same inputs → same receipt IDs → same recovery_id."""

    def test_admission_receipt_id_is_deterministic(self):
        r1 = GoverningExecutor().execute(_req())
        r2 = GoverningExecutor().execute(_req())
        self.assertEqual(
            r1.admission_receipt.receipt_id,
            r2.admission_receipt.receipt_id,
        )

    def test_recovery_id_is_deterministic(self):
        r1 = GoverningExecutor().execute(_req())
        r2 = GoverningExecutor().execute(_req())
        self.assertEqual(r1.chain.recovery_id, r2.chain.recovery_id)

    def test_different_requests_different_recovery_id(self):
        r1 = GoverningExecutor().execute(_req("summarize the audit log", request_id="a"))
        r2 = GoverningExecutor().execute(_req("summarize something else", request_id="b"))
        self.assertNotEqual(r1.chain.recovery_id, r2.chain.recovery_id)


class TestReconstructionFromReceipts(unittest.TestCase):
    """Reconstruct the chain from raw receipt dicts — recovery_id must match."""

    def test_chain_reconstructible_from_dicts(self):
        record = GoverningExecutor().execute(_req())
        original_recovery_id = record.chain.recovery_id

        # Serialize to dicts (as a reviewer or external system would receive them)
        raw_dicts = [r.to_dict() for r in record.chain.receipts]

        # Reconstruct
        rebuilt_receipts = [TransitionReceipt(**d) for d in raw_dicts]
        rebuilt_chain = ClaimReceiptChain.build(record.request.request_id, rebuilt_receipts)

        self.assertEqual(rebuilt_chain.recovery_id, original_recovery_id)

    def test_tampered_receipt_changes_recovery_id(self):
        record = GoverningExecutor().execute(_req())
        receipts = list(record.chain.receipts)

        # Tamper: create a receipt with a different reason — this produces a
        # different receipt_id (content-addressed), which changes recovery_id.
        original = receipts[0]
        tampered = TransitionReceipt.create(
            claim_id=original.claim_id,
            actor=original.actor,
            from_state=ClaimState(original.from_state),
            to_state=ClaimState(original.to_state),
            reason="tampered reason",
            timestamp=original.timestamp,
        )
        self.assertNotEqual(tampered.receipt_id, original.receipt_id)
        receipts[0] = tampered

        tampered_chain = ClaimReceiptChain.build(record.request.request_id, receipts)
        self.assertNotEqual(tampered_chain.recovery_id, record.chain.recovery_id)


class TestGateIsStructuralNotObservational(unittest.TestCase):
    """The paper's core claim: admission receipt must exist before execution output exists."""

    def test_no_output_without_admission_receipt(self):
        blocked_cases = [
            "please expose credential",
            "maybe do something unclear",
            "out of scope request",
        ]
        for content in blocked_cases:
            with self.subTest(content=content):
                rec = GoverningExecutor().execute(_req(content))
                if rec.admission_receipt is None:
                    self.assertIsNone(
                        rec.execution_output,
                        f"execution_output must be None when admission_receipt is None: {content}",
                    )

    def test_output_always_present_when_admitted(self):
        rec = GoverningExecutor().execute(_req())
        self.assertTrue(rec.admitted)
        self.assertIsNotNone(rec.execution_output)


if __name__ == "__main__":
    unittest.main()
