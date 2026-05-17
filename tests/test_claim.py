"""Tests for lcos_toy.claim — ClaimState machine and TransitionReceipt."""
import unittest

from lcos_toy.claim import ClaimMachine, ClaimState, TransitionReceipt


class TestClaimState(unittest.TestCase):
    def test_initial_state_is_open(self):
        m = ClaimMachine("c-001")
        self.assertEqual(m.state, ClaimState.OPEN)

    def test_open_to_active(self):
        m = ClaimMachine("c-001")
        r = m.activate(reason="start")
        self.assertEqual(m.state, ClaimState.ACTIVE)
        self.assertEqual(r.from_state, "OPEN")
        self.assertEqual(r.to_state, "ACTIVE")

    def test_active_to_complete(self):
        m = ClaimMachine("c-001")
        m.activate(reason="start")
        r = m.complete(reason="done")
        self.assertEqual(m.state, ClaimState.COMPLETE)
        self.assertEqual(r.to_state, "COMPLETE")

    def test_active_to_held(self):
        m = ClaimMachine("c-001")
        m.activate(reason="start")
        r = m.hold(reason="waiting for proof")
        self.assertEqual(m.state, ClaimState.HELD)
        self.assertEqual(r.to_state, "HELD")

    def test_held_to_active_resume(self):
        m = ClaimMachine("c-001")
        m.activate(reason="start")
        m.hold(reason="blocked")
        r = m.resume(reason="unblocked")
        self.assertEqual(m.state, ClaimState.ACTIVE)

    def test_held_to_complete(self):
        m = ClaimMachine("c-001")
        m.activate(reason="start")
        m.hold(reason="blocked")
        r = m.complete(reason="resolved")
        self.assertEqual(m.state, ClaimState.COMPLETE)

    def test_illegal_transition_raises(self):
        m = ClaimMachine("c-001")
        with self.assertRaises(ValueError):
            m.complete(reason="skip directly to complete")  # OPEN → COMPLETE is illegal

    def test_open_to_held_is_legal_gate_denial(self):
        # OPEN→HELD represents a gate denial before activation — claim assessed but not started
        m = ClaimMachine("c-001")
        r = m.hold(reason="gate denied before activation")
        self.assertEqual(m.state, ClaimState.HELD)
        self.assertEqual(r.from_state, "OPEN")
        self.assertEqual(r.to_state, "HELD")

    def test_receipts_accumulate_in_order(self):
        m = ClaimMachine("c-001")
        m.activate(reason="a")
        m.hold(reason="b")
        m.resume(reason="c")
        m.complete(reason="d")
        self.assertEqual(len(m.receipts), 4)
        states = [(r.from_state, r.to_state) for r in m.receipts]
        self.assertEqual(states, [
            ("OPEN", "ACTIVE"),
            ("ACTIVE", "HELD"),
            ("HELD", "ACTIVE"),
            ("ACTIVE", "COMPLETE"),
        ])


class TestTransitionReceiptContentAddressing(unittest.TestCase):
    def test_same_inputs_produce_same_receipt_id(self):
        r1 = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="start",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        r2 = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="start",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        self.assertEqual(r1.receipt_id, r2.receipt_id)

    def test_different_reason_produces_different_receipt_id(self):
        r1 = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="start",
        )
        r2 = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="different",
        )
        self.assertNotEqual(r1.receipt_id, r2.receipt_id)

    def test_receipt_id_is_independent_of_timestamp(self):
        # Receipt ID is computed from body before timestamp — timestamps should not affect it
        r1 = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="start",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        r2 = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="start",
            timestamp="2099-12-31T23:59:59+00:00",
        )
        self.assertEqual(r1.receipt_id, r2.receipt_id)

    def test_receipt_carries_claim_id(self):
        r = TransitionReceipt.create(
            claim_id="c-xyz", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="x",
        )
        self.assertEqual(r.claim_id, "c-xyz")

    def test_to_dict_has_required_fields(self):
        r = TransitionReceipt.create(
            claim_id="c-001", actor="test", from_state=ClaimState.OPEN,
            to_state=ClaimState.ACTIVE, reason="start",
        )
        d = r.to_dict()
        for key in ("receipt_id", "claim_id", "actor", "from_state", "to_state", "reason", "timestamp"):
            self.assertIn(key, d)


if __name__ == "__main__":
    unittest.main()
