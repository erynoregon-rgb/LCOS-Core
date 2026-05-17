"""Tests for lcos_toy.chain — ClaimReceiptChain and deterministic recovery_id (C4)."""
import unittest

from lcos_toy.claim import ClaimMachine, ClaimState, TransitionReceipt
from lcos_toy.chain import ClaimReceiptChain


def _make_receipts(claim_id: str) -> tuple[TransitionReceipt, ...]:
    m = ClaimMachine(claim_id)
    m.activate(reason="start", timestamp="2026-01-01T00:00:00+00:00")
    m.complete(reason="done", timestamp="2026-01-01T00:00:01+00:00")
    return m.receipts


class TestClaimReceiptChain(unittest.TestCase):
    def test_build_from_receipts(self):
        receipts = _make_receipts("c-001")
        chain = ClaimReceiptChain.build("c-001", receipts)
        self.assertEqual(chain.claim_id, "c-001")
        self.assertEqual(chain.length, 2)

    def test_outcome_complete(self):
        chain = ClaimReceiptChain.build("c-001", _make_receipts("c-001"))
        self.assertEqual(chain.outcome, "accepted")

    def test_outcome_held(self):
        m = ClaimMachine("c-002")
        m.activate(reason="start", timestamp="2026-01-01T00:00:00+00:00")
        m.hold(reason="blocked", timestamp="2026-01-01T00:00:01+00:00")
        chain = ClaimReceiptChain.build("c-002", m.receipts)
        self.assertEqual(chain.outcome, "held")

    def test_mismatched_claim_id_raises(self):
        m1 = ClaimMachine("c-001")
        m1.activate(reason="x", timestamp="2026-01-01T00:00:00+00:00")
        m2 = ClaimMachine("c-002")
        m2.activate(reason="y", timestamp="2026-01-01T00:00:00+00:00")
        with self.assertRaises(ValueError):
            ClaimReceiptChain.build("c-001", (*m1.receipts, *m2.receipts))


class TestRecoveryIdDeterminism(unittest.TestCase):
    """C4: same claim_id + same ordered receipts → same recovery_id."""

    def test_same_inputs_same_recovery_id(self):
        r1 = _make_receipts("c-001")
        r2 = _make_receipts("c-001")
        chain1 = ClaimReceiptChain.build("c-001", r1)
        chain2 = ClaimReceiptChain.build("c-001", r2)
        # Both chains were built with identical inputs (same timestamps, same reasons)
        self.assertEqual(chain1.recovery_id, chain2.recovery_id)

    def test_different_outcomes_different_recovery_id(self):
        m_accept = ClaimMachine("c-003")
        m_accept.activate(reason="start", timestamp="2026-01-01T00:00:00+00:00")
        m_accept.complete(reason="done", timestamp="2026-01-01T00:00:01+00:00")

        m_hold = ClaimMachine("c-003")
        m_hold.activate(reason="start", timestamp="2026-01-01T00:00:00+00:00")
        m_hold.hold(reason="blocked", timestamp="2026-01-01T00:00:01+00:00")

        chain_accept = ClaimReceiptChain.build("c-003", m_accept.receipts)
        chain_hold = ClaimReceiptChain.build("c-003", m_hold.receipts)
        self.assertNotEqual(chain_accept.recovery_id, chain_hold.recovery_id)

    def test_recovery_id_is_64_char_hex(self):
        chain = ClaimReceiptChain.build("c-001", _make_receipts("c-001"))
        self.assertEqual(len(chain.recovery_id), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in chain.recovery_id))

    def test_to_dict_structure(self):
        chain = ClaimReceiptChain.build("c-001", _make_receipts("c-001"))
        d = chain.to_dict()
        self.assertIn("claim_id", d)
        self.assertIn("recovery_id", d)
        self.assertIn("outcome", d)
        self.assertIn("receipts", d)
        self.assertEqual(len(d["receipts"]), 2)


if __name__ == "__main__":
    unittest.main()
