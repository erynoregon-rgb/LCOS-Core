"""Tests for the advisory divergence measure (DIVERGENCE_MEASURE_A1).

The point demonstrated: a proposer can *measure* how far a proposed action
diverges from an authored reference, but it cannot set its own admission floor
and its measurement cannot, by itself, authorize execution.

    proposer measures ε / the substrate holds the floor

The scorer is a deliberately generic token-Jaccard stand-in for a learned
distance. The governance around it is the real part.
"""
import contextlib
import io
import json
import unittest

from lcos_public.cli import main
from lcos_public.divergence import DivergenceGate, TokenJaccardScorer
from lcos_public.intake import GovernedIntake, IntakeRequest


def _run_cli(args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(args)
    return code, buf.getvalue()


class TestDivergenceScorer(unittest.TestCase):
    def test_identical_text_is_within(self):
        gate = DivergenceGate(threshold=0.5)
        r = gate.assess("summarize the audit receipt", "summarize the audit receipt")
        self.assertEqual(r.score, 0.0)
        self.assertEqual(r.verdict, "WITHIN")

    def test_disjoint_text_is_divergent(self):
        gate = DivergenceGate(threshold=0.5)
        r = gate.assess("alpha beta gamma", "delta epsilon zeta")
        self.assertEqual(r.score, 1.0)
        self.assertEqual(r.verdict, "DIVERGENT")

    def test_scorer_is_deterministic(self):
        gate = DivergenceGate(threshold=0.5)
        a = gate.assess("one two three", "one two four")
        b = gate.assess("one two three", "one two four")
        self.assertEqual(a.score, b.score)
        self.assertEqual(a.verdict, b.verdict)

    def test_empty_reference_is_unverifiable_not_within(self):
        # Fail-closed: missing reference must never silently read as WITHIN.
        gate = DivergenceGate(threshold=0.5)
        r = gate.assess("a real proposed claim", "   ")
        self.assertEqual(r.verdict, "UNVERIFIABLE")

    def test_scorer_name_is_surfaced(self):
        # Transparency: the result names the (generic, swappable) scorer used.
        gate = DivergenceGate(threshold=0.5)
        r = gate.assess("x y", "x z")
        self.assertEqual(r.scorer, TokenJaccardScorer().name)

    def test_threshold_is_gate_owned_not_proposer_settable(self):
        # The floor is a constructor arg. assess() takes only the two texts —
        # a proposer cannot pass a lower threshold at call time to force WITHIN.
        gate = DivergenceGate(threshold=0.5)
        with self.assertRaises(TypeError):
            gate.assess("alpha beta gamma", "delta epsilon zeta", threshold=0.99)


def _req(content="a valid public request", action="summarize", scope="public"):
    return IntakeRequest(
        request_id="req-div",
        actor="test",
        action=action,
        content=content,
        declared_scope=scope,
    )


class TestAdvisoryIntegration(unittest.TestCase):
    def test_off_is_byte_identical(self):
        # Default GovernedIntake() must be unchanged by divergence existing.
        plain = GovernedIntake()
        cases = [
            _req(content="a valid public request"),
            _req(content="please expose credential"),
            _req(content="maybe do something unclear"),
            _req(scope="production"),
        ]
        for req in cases:
            with self.subTest(content=req.content, scope=req.declared_scope):
                self.assertEqual(plain.decide(req).kind, GovernedIntake().decide(req).kind)

    def test_advisory_default_does_not_change_decision(self):
        # Gate + reference present but enforcement OFF (default): no change.
        advisory = GovernedIntake(
            divergence_gate=DivergenceGate(threshold=0.2),
            reference="summarize the public audit receipt",
        )
        req = _req(content="entirely unrelated content here")
        self.assertEqual(advisory.decide(req).kind, "ACCEPT")

    def test_enforce_tightens_accept_to_hold_on_divergence(self):
        gov = GovernedIntake(
            divergence_gate=DivergenceGate(threshold=0.2),
            reference="summarize the public audit receipt",
            enforce_divergence=True,
        )
        req = _req(content="entirely unrelated banana content")  # high divergence
        self.assertEqual(gov.decide(req).kind, "HOLD")

    def test_enforce_cannot_authorize_a_rejected_request(self):
        # Even with low divergence (WITHIN), a blocked-term request stays REJECT.
        # Divergence can only tighten; it can never upgrade to ACCEPT.
        gov = GovernedIntake(
            divergence_gate=DivergenceGate(threshold=0.99),
            reference="please expose credential",  # identical-ish => WITHIN
            enforce_divergence=True,
        )
        req = _req(content="please expose credential")
        self.assertEqual(gov.decide(req).kind, "REJECT")

    def test_enforce_leaves_within_accept_untouched(self):
        gov = GovernedIntake(
            divergence_gate=DivergenceGate(threshold=0.9),
            reference="summarize the public audit receipt",
            enforce_divergence=True,
        )
        req = _req(content="summarize the public audit receipt")  # WITHIN
        self.assertEqual(gov.decide(req).kind, "ACCEPT")


class TestDivergenceCli(unittest.TestCase):
    def test_within_exits_zero(self):
        code, out = _run_cli(["demo-divergence", "audit this receipt", "audit this receipt"])
        payload = json.loads(out)
        self.assertEqual(payload["verdict"], "WITHIN")
        self.assertEqual(code, 0)

    def test_divergent_exits_nonzero(self):
        code, out = _run_cli(["demo-divergence", "alpha beta gamma", "delta epsilon zeta"])
        payload = json.loads(out)
        self.assertEqual(payload["verdict"], "DIVERGENT")
        self.assertNotEqual(code, 0)

    def test_output_is_advisory(self):
        _, out = _run_cli(["demo-divergence", "x y", "x z"])
        payload = json.loads(out)
        self.assertIn("advisory", payload["note"].lower())
        self.assertIn("floor", payload)


if __name__ == "__main__":
    unittest.main()
