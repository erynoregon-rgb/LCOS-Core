"""Claim state machine and transition receipts.

ClaimState: four-state machine for a governed claim lifecycle.
TransitionReceipt: receipt emitted at each state transition.

Receipt IDs are content-addressed: sha256 of the body before timestamp
is added. Same claim_id + same body → same receipt_id. This makes
receipt chains deterministic and reconstructible.

Public toy demonstration only. Does not expose private SKOS internals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from .receipt import canonical_json, stable_digest


class ClaimState(Enum):
    OPEN = "OPEN"
    ACTIVE = "ACTIVE"
    HELD = "HELD"
    COMPLETE = "COMPLETE"


# Legal transitions: (from, to)
_ALLOWED_TRANSITIONS: frozenset[tuple[ClaimState, ClaimState]] = frozenset({
    (ClaimState.OPEN,   ClaimState.ACTIVE),
    (ClaimState.OPEN,   ClaimState.HELD),     # gate denial before activation
    (ClaimState.ACTIVE, ClaimState.HELD),
    (ClaimState.ACTIVE, ClaimState.COMPLETE),
    (ClaimState.HELD,   ClaimState.ACTIVE),   # resume after hold
    (ClaimState.HELD,   ClaimState.COMPLETE),  # close from hold
})


@dataclass(frozen=True)
class TransitionReceipt:
    """Receipt emitted at each legal state transition.

    receipt_id is content-addressed: sha256(body_before_timestamp).
    Same inputs → same receipt_id. Timestamp is carried separately
    so the ID is independent of wall-clock time.
    """
    receipt_id: str
    claim_id: str
    actor: str
    from_state: str
    to_state: str
    reason: str
    timestamp: str
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "claim_id": self.claim_id,
            "actor": self.actor,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    @classmethod
    def _body(
        cls,
        *,
        claim_id: str,
        actor: str,
        from_state: str,
        to_state: str,
        reason: str,
        metadata: dict[str, object],
    ) -> dict[str, object]:
        """Canonical body before timestamp — this is what gets hashed for receipt_id."""
        return {
            "claim_id": claim_id,
            "actor": actor,
            "from_state": from_state,
            "to_state": to_state,
            "reason": reason,
            "metadata": metadata,
        }

    @classmethod
    def create(
        cls,
        *,
        claim_id: str,
        actor: str,
        from_state: ClaimState,
        to_state: ClaimState,
        reason: str,
        timestamp: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> "TransitionReceipt":
        meta = metadata or {}
        body = cls._body(
            claim_id=claim_id,
            actor=actor,
            from_state=from_state.value,
            to_state=to_state.value,
            reason=reason,
            metadata=meta,
        )
        receipt_id = stable_digest(body)
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        return cls(
            receipt_id=receipt_id,
            claim_id=claim_id,
            actor=actor,
            from_state=from_state.value,
            to_state=to_state.value,
            reason=reason,
            timestamp=ts,
            metadata=meta,
        )


class ClaimMachine:
    """Minimal state machine for one claim's lifecycle.

    Raises ValueError on illegal transitions.
    Records all TransitionReceipts in order.
    """

    def __init__(self, claim_id: str, actor: str = "system") -> None:
        self.claim_id = claim_id
        self.actor = actor
        self._state = ClaimState.OPEN
        self._receipts: list[TransitionReceipt] = []

    @property
    def state(self) -> ClaimState:
        return self._state

    @property
    def receipts(self) -> tuple[TransitionReceipt, ...]:
        return tuple(self._receipts)

    def transition(
        self,
        to: ClaimState,
        *,
        reason: str,
        actor: str | None = None,
        timestamp: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> TransitionReceipt:
        edge = (self._state, to)
        if edge not in _ALLOWED_TRANSITIONS:
            raise ValueError(
                f"illegal transition {self._state.value} → {to.value} for claim {self.claim_id}"
            )
        receipt = TransitionReceipt.create(
            claim_id=self.claim_id,
            actor=actor or self.actor,
            from_state=self._state,
            to_state=to,
            reason=reason,
            timestamp=timestamp,
            metadata=metadata,
        )
        self._state = to
        self._receipts.append(receipt)
        return receipt

    def activate(self, *, reason: str = "claim activated", **kw: object) -> TransitionReceipt:
        return self.transition(ClaimState.ACTIVE, reason=reason, **kw)  # type: ignore[arg-type]

    def hold(self, *, reason: str, **kw: object) -> TransitionReceipt:
        return self.transition(ClaimState.HELD, reason=reason, **kw)  # type: ignore[arg-type]

    def complete(self, *, reason: str = "claim completed", **kw: object) -> TransitionReceipt:
        return self.transition(ClaimState.COMPLETE, reason=reason, **kw)  # type: ignore[arg-type]

    def resume(self, *, reason: str = "hold released", **kw: object) -> TransitionReceipt:
        return self.transition(ClaimState.ACTIVE, reason=reason, **kw)  # type: ignore[arg-type]
