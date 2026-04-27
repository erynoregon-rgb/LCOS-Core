from pathlib import Path

from lcos.intake.models import IntakeRequest
from lcos.intake.pipeline import run_intake
from lcos.receipts.ledger import ReceiptLedger


def test_run_intake_accepts_and_extracts(tmp_path: Path) -> None:
    ledger = ReceiptLedger(tmp_path / "receipts.jsonl")
    req = IntakeRequest(
        request_id="r1",
        goal="extract",
        content="Runtime governance can be modeled as explicit decisions.",
        source_type="demo",
    )
    decision, packet = run_intake(req, ledger)
    assert decision.status == "ACCEPT"
    assert packet is not None
    assert packet.request_id == "r1"


def test_run_intake_holds_short_content(tmp_path: Path) -> None:
    ledger = ReceiptLedger(tmp_path / "receipts.jsonl")
    req = IntakeRequest(request_id="r2", goal="extract", content="too short", source_type="demo")
    decision, packet = run_intake(req, ledger)
    assert decision.status == "HOLD"
    assert packet is None
