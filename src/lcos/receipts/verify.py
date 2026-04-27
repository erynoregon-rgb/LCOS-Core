from __future__ import annotations

from .ledger import ReceiptLedger


def verify_chain(ledger: ReceiptLedger) -> tuple[bool, str]:
    receipts = ledger.read_all()
    prev_hash = None
    for idx, receipt in enumerate(receipts):
        if receipt.prev_hash != prev_hash:
            return False, f"receipt {idx} has invalid prev_hash"
        prev_hash = receipt.entry_hash()
    return True, "chain valid"
