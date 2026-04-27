from pathlib import Path

from lcos.intake.models import IntakeRequest
from lcos.intake.pipeline import run_intake
from lcos.receipts.ledger import ReceiptLedger
from lcos.receipts.verify import verify_chain


def main() -> None:
    ledger = ReceiptLedger(Path(__file__).parent / "receipts.jsonl")
    request = IntakeRequest(
        request_id="req-001",
        goal="extract one bounded claim",
        content="Receipt chains make runtime claims auditable. This is a simple example.",
        source_type="demo_text",
    )
    decision, packet = run_intake(request, ledger)
    valid, message = verify_chain(ledger)
    print({"decision": decision.status, "packet": packet, "receipt_chain_valid": valid, "message": message})


if __name__ == "__main__":
    main()
