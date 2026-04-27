from pathlib import Path

from lcos.receipts.ledger import ReceiptLedger
from lcos.receipts.verify import verify_chain


def test_receipt_chain_verifies(tmp_path: Path) -> None:
    ledger = ReceiptLedger(tmp_path / "receipts.jsonl")
    first = ledger.append("start", "x", {"n": 1})
    ledger.append("finish", "x", {"n": 2}, parent_receipt_id=first.receipt_id)
    ok, _ = verify_chain(ledger)
    assert ok is True
