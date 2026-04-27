from pathlib import Path

from lcos.receipts.ledger import ReceiptLedger
from lcos.receipts.verify import verify_chain


def main() -> None:
    ledger = ReceiptLedger(Path(__file__).parent / "receipts.jsonl")
    r1 = ledger.append("demo.start", "example", {"step": 1})
    ledger.append("demo.finish", "example", {"step": 2}, parent_receipt_id=r1.receipt_id)
    ok, msg = verify_chain(ledger)
    print({"valid": ok, "message": msg, "count": len(ledger.read_all())})


if __name__ == "__main__":
    main()
