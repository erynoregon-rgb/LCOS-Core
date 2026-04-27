from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    action: str
    subject: str
    payload: dict[str, Any]
    created_at: str
    parent_receipt_id: str | None = None
    prev_hash: str | None = None

    @staticmethod
    def build(action: str, subject: str, payload: dict[str, Any], parent_receipt_id: str | None, prev_hash: str | None) -> "Receipt":
        created_at = utc_now()
        digest_input = f"{action}|{subject}|{created_at}|{parent_receipt_id}|{prev_hash}|{payload}"
        receipt_id = sha256(digest_input.encode("utf-8")).hexdigest()[:16]
        return Receipt(
            receipt_id=receipt_id,
            action=action,
            subject=subject,
            payload=payload,
            created_at=created_at,
            parent_receipt_id=parent_receipt_id,
            prev_hash=prev_hash,
        )

    def entry_hash(self) -> str:
        data = f"{self.receipt_id}|{self.action}|{self.subject}|{self.created_at}|{self.parent_receipt_id}|{self.prev_hash}|{self.payload}"
        return sha256(data.encode("utf-8")).hexdigest()
