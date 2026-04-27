import json
from pathlib import Path
import unittest

from lcos_toy.intake import GovernedIntake, IntakeRequest


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "adversarial"


class IntakeTests(unittest.TestCase):
    def test_valid_request_accepts(self):
        request = IntakeRequest.from_payload(
            {
                "request_id": "ok-1",
                "actor": "tester",
                "action": "summarize",
                "content": "summarize public toy receipt",
                "declared_scope": "toy",
            }
        )
        self.assertEqual(GovernedIntake().decide(request).kind, "ACCEPT")

    def test_malformed_request_rejects_at_validation(self):
        payload = json.loads((FIXTURES / "malformed_request.json").read_text())
        with self.assertRaises(ValueError):
            IntakeRequest.from_payload(payload)

    def test_ambiguous_request_holds(self):
        payload = json.loads((FIXTURES / "ambiguous_request.json").read_text())
        decision = GovernedIntake().decide(IntakeRequest.from_payload(payload))
        self.assertEqual(decision.kind, "HOLD")

    def test_private_trace_request_rejects(self):
        payload = json.loads((FIXTURES / "private_trace_reject_request.json").read_text())
        decision = GovernedIntake().decide(IntakeRequest.from_payload(payload))
        self.assertEqual(decision.kind, "REJECT")

    def test_out_of_scope_request_escalates(self):
        payload = json.loads((FIXTURES / "out_of_scope_escalate_request.json").read_text())
        decision = GovernedIntake().decide(IntakeRequest.from_payload(payload))
        self.assertEqual(decision.kind, "ESCALATE")


if __name__ == "__main__":
    unittest.main()
