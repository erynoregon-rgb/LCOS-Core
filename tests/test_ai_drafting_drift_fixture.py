"""Adversarial fixture: AI drafting drift.

Proves the mechanism-change claim of the prompt-contract gate primitive:

  bad AI draft
    -> violates declared contract
      -> HOLD emitted
        -> no accepted receipt in the ledger
          -> replay timeline shows why

This test is self-contained. It does NOT import the portable prompt-contract
gate package — the gate logic is inlined here as the smallest validator that
can demonstrate the mechanism, so the fixture stands as a public proof
artifact without inheriting external complexity. LCOS-Core ships with zero
external dependencies (see pyproject.toml); the YAML loader below is a
deliberately narrow parser scoped to this fixture's contract shape.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from lcos_public.ledger import AppendOnlyLedger
from lcos_public.replay import render_timeline


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "adversarial" / "ai_drafting_drift"


def _load_contract_yaml(path: Path) -> dict:
    """Parse the fixture's minimal YAML contract.

    Handles only the shape this fixture uses: top-level scalar keys and a
    single nested list (forbidden_terms). LCOS-Core has no YAML dependency;
    this parser intentionally does not generalize beyond the fixture.
    """
    contract: dict = {}
    current_list_key: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError(f"list item with no parent key: {line!r}")
            contract.setdefault(current_list_key, []).append(line[4:].strip())
            continue
        if ":" not in line:
            raise ValueError(f"unparseable line: {line!r}")
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list_key = key
            contract.setdefault(key, [])
        else:
            contract[key] = value
            current_list_key = None
    return contract


def _run_gate(contract: dict, deliverable_text: str) -> dict:
    """Inline minimal gate.

    The point is mechanism demonstration, not contract surface coverage.
    A single check (forbidden_terms_absent) is enough to prove that an
    adversarial draft is converted into a HOLD before downstream admission.
    """
    forbidden = [str(t) for t in contract.get("forbidden_terms", [])]
    lowered = deliverable_text.lower()
    found = [term for term in forbidden if term.lower() in lowered]

    if not found:
        return {
            "verdict": "VALID",
            "constraint_check": {"forbidden_terms_absent": "pass"},
        }

    return {
        "verdict": "INVALID",
        "constraint_check": {
            "forbidden_terms_absent": "fail",
            "forbidden_terms_found": found,
        },
        "hold_record": {
            "hold_code": "HOLD_CONTRACT_VIOLATION",
            "deliverable_blocked": True,
            "failed_constraints": ["forbidden_terms_absent"],
            "forbidden_terms_found": found,
            "next_actor": "user",
            "resume_condition": "corrected deliverable passes gate",
            "nothing_promoted": True,
        },
    }


class AiDraftingDriftFixtureTests(unittest.TestCase):
    """End-to-end chain assertion for the AI-drafting-drift fixture."""

    def setUp(self) -> None:
        self.contract = _load_contract_yaml(FIXTURE_DIR / "contract.yaml")
        self.adversarial = (FIXTURE_DIR / "adversarial_output.txt").read_text(encoding="utf-8")
        self.expected_hold = json.loads((FIXTURE_DIR / "expected_hold.json").read_text(encoding="utf-8"))

    def test_contract_loads_with_declared_fields(self) -> None:
        self.assertEqual(self.contract["mode"], "draft")
        self.assertEqual(self.contract["claim_source"], "LCOS-Core repository (public)")
        self.assertIn("AI OS", self.contract["forbidden_terms"])
        self.assertIn("substrate", self.contract["forbidden_terms"])

    def test_adversarial_output_violates_contract(self) -> None:
        result = _run_gate(self.contract, self.adversarial)
        self.assertEqual(result["verdict"], "INVALID")
        self.assertEqual(result["constraint_check"]["forbidden_terms_absent"], "fail")
        found = set(result["constraint_check"]["forbidden_terms_found"])
        self.assertEqual(found, {"AI OS", "substrate"})

    def test_hold_record_matches_expected_shape(self) -> None:
        result = _run_gate(self.contract, self.adversarial)
        actual = result["hold_record"]
        self.assertEqual(actual["hold_code"], self.expected_hold["hold_code"])
        self.assertEqual(actual["deliverable_blocked"], self.expected_hold["deliverable_blocked"])
        self.assertEqual(actual["failed_constraints"], self.expected_hold["failed_constraints"])
        self.assertEqual(set(actual["forbidden_terms_found"]), set(self.expected_hold["forbidden_terms_found"]))
        self.assertEqual(actual["next_actor"], self.expected_hold["next_actor"])
        self.assertEqual(actual["resume_condition"], self.expected_hold["resume_condition"])
        self.assertEqual(actual["nothing_promoted"], self.expected_hold["nothing_promoted"])

    def test_no_downstream_admission_after_hold(self) -> None:
        """The HOLD must prevent any downstream ACCEPTED receipt for this draft."""
        result = _run_gate(self.contract, self.adversarial)
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.jsonl"
            ledger = AppendOnlyLedger(ledger_path)
            draft_id = "ai_drafting_drift_001"

            ledger.append(
                "DRAFT_INTAKE",
                {"draft_id": draft_id, "contract_mode": self.contract["mode"]},
                timestamp="2026-01-01T00:00:00+00:00",
            )

            if result["verdict"] == "INVALID":
                ledger.append(
                    "CONTRACT_HOLD",
                    {"draft_id": draft_id, **result["hold_record"]},
                    timestamp="2026-01-01T00:00:01+00:00",
                )
            else:
                ledger.append(
                    "EXECUTION_ACCEPTED",
                    {"draft_id": draft_id, "deliverable_released": True},
                    timestamp="2026-01-01T00:00:01+00:00",
                )

            event_types = [r["receipt"]["event_type"] for r in ledger.records()]
            self.assertIn("CONTRACT_HOLD", event_types)
            self.assertNotIn("EXECUTION_ACCEPTED", event_types)

            report = ledger.verify()
            self.assertTrue(report.valid, msg=f"ledger verification failed: {report.issues}")

    def test_replay_renders_why_blocked(self) -> None:
        """The replay timeline must surface the HOLD event with a verifiable digest."""
        result = _run_gate(self.contract, self.adversarial)
        self.assertEqual(result["verdict"], "INVALID")
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.jsonl"
            ledger = AppendOnlyLedger(ledger_path)
            ledger.append(
                "DRAFT_INTAKE",
                {"draft_id": "ai_drafting_drift_001"},
                timestamp="2026-01-01T00:00:00+00:00",
            )
            ledger.append(
                "CONTRACT_HOLD",
                {"draft_id": "ai_drafting_drift_001", **result["hold_record"]},
                timestamp="2026-01-01T00:00:01+00:00",
            )

            timeline = render_timeline(ledger_path)

            self.assertIn("DRAFT_INTAKE", timeline)
            self.assertIn("CONTRACT_HOLD", timeline)
            self.assertIn("valid=true", timeline)


if __name__ == "__main__":
    unittest.main()
