"""ClaimReceiptChain: ordered, content-addressed chain of transition receipts.

Same claim_id + same receipts (in same order) → same recovery_id.
This is the paper's C4 claim: the chain is deterministic and reconstructible.

Public toy demonstration only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .claim import TransitionReceipt
from .receipt import canonical_json, stable_digest


@dataclass(frozen=True)
class ClaimReceiptChain:
    """Immutable ordered chain of TransitionReceipts for one claim.

    recovery_id: SHA256 of the serialized chain (canonical JSON).
    Same claim_id + same ordered receipts → same recovery_id every time.
    """
    claim_id: str
    receipts: tuple[TransitionReceipt, ...]
    recovery_id: str

    @classmethod
    def build(cls, claim_id: str, receipts: Sequence[TransitionReceipt]) -> "ClaimReceiptChain":
        ordered = tuple(receipts)
        if not all(r.claim_id == claim_id for r in ordered):
            mismatched = [r.claim_id for r in ordered if r.claim_id != claim_id]
            raise ValueError(f"receipt claim_id mismatch: {mismatched}")
        chain_body = {
            "claim_id": claim_id,
            "receipts": [r.to_dict() for r in ordered],
        }
        recovery_id = stable_digest(chain_body)
        return cls(claim_id=claim_id, receipts=ordered, recovery_id=recovery_id)

    @property
    def length(self) -> int:
        return len(self.receipts)

    @property
    def final_state(self) -> str | None:
        return self.receipts[-1].to_state if self.receipts else None

    @property
    def outcome(self) -> str:
        if not self.receipts:
            return "empty"
        last = self.receipts[-1].to_state
        if last == "COMPLETE":
            return "accepted"
        if last == "HELD":
            return "held"
        return "in_progress"

    def to_dict(self) -> dict[str, object]:
        return {
            "claim_id": self.claim_id,
            "recovery_id": self.recovery_id,
            "outcome": self.outcome,
            "length": self.length,
            "receipts": [r.to_dict() for r in self.receipts],
        }
