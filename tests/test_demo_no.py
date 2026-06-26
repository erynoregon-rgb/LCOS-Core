"""Tests for the adversarial 'no' demo.

The load-bearing public claim: an agent can *assert* it did something, but the
gate admits execution only if the claim is supported. An unsupported claim is
held — no admission receipt, no execution output. This demo makes that visible.

inference proposes / verification disposes / the gate can return no.
"""
import contextlib
import io
import json
from pathlib import Path
import unittest

from lcos_public.cli import main


def _run_cli(args: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(args)
    return code, buf.getvalue()


class TestAdversarialNoDemo(unittest.TestCase):
    def test_demo_no_default_holds_unsupported_claim(self):
        _, out = _run_cli(["demo-no"])
        payload = json.loads(out)
        # inference proposed, verification disposed: nothing ran, claim is held
        self.assertIsNone(payload["admission_receipt_id"])
        self.assertIsNone(payload["execution_output"])
        self.assertIsNotNone(payload["hold_receipt_id"])
        self.assertEqual(payload["outcome"], "held")
        self.assertFalse(payload["admitted"])
        self.assertIn(payload["admission_decision"], ("REJECT", "HOLD", "ESCALATE"))

    def test_demo_no_exit_code_is_nonzero_when_held(self):
        # The 'no' is the load-bearing output. A held claim is a non-zero exit:
        # `echo $?` after the demo is the machine-checkable refusal.
        code, _ = _run_cli(["demo-no"])
        self.assertNotEqual(code, 0)

    def test_demo_no_reports_the_claim_and_a_plain_verdict(self):
        _, out = _run_cli(["demo-no"])
        payload = json.loads(out)
        self.assertIn("claim", payload)
        self.assertTrue(payload["claim"], "the asserted claim must be echoed back")
        self.assertIn("verdict", payload)
        self.assertIn("held", payload["verdict"].lower())

    def test_bundled_adversarial_fixture_is_held(self):
        fixture = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "requests"
            / "adversarial_no_receipt.json"
        )
        self.assertTrue(fixture.exists(), "bundled adversarial-no fixture must exist")
        _, out = _run_cli(["demo-no", str(fixture)])
        payload = json.loads(out)
        self.assertEqual(payload["outcome"], "held")
        self.assertIsNone(payload["execution_output"])

    def test_structural_guarantee_no_receipt_no_output(self):
        # If the admission receipt is absent, execution output must be absent too.
        # There is no path where execution ran without admission.
        _, out = _run_cli(["demo-no"])
        payload = json.loads(out)
        if payload["admission_receipt_id"] is None:
            self.assertIsNone(payload["execution_output"])


if __name__ == "__main__":
    unittest.main()
