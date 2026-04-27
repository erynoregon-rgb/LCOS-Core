from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .models import Receipt


class ReceiptLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def append(self, action: str, subject: str, payload: dict, parent_receipt_id: str | None = None) -> Receipt:
        last = self.last_receipt()
        prev_hash = last.entry_hash() if last else None
        receipt = Receipt.build(action=action, subject=subject, payload=payload, parent_receipt_id=parent_receipt_id, prev_hash=prev_hash)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(receipt), sort_keys=True) + "\n")
        return receipt

    def read_all(self) -> list[Receipt]:
        receipts: list[Receipt] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                receipts.append(Receipt(**json.loads(line)))
        return receipts

    def last_receipt(self) -> Receipt | None:
        receipts = self.read_all()
        return receipts[-1] if receipts else None
