from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DecisionKind = Literal["ACCEPT", "HOLD", "REJECT", "ESCALATE"]


@dataclass(frozen=True)
class Decision:
    kind: DecisionKind
    reason: str
    evidence: tuple[str, ...] = ()

    def to_payload(self) -> dict[str, object]:
        return {"kind": self.kind, "reason": self.reason, "evidence": list(self.evidence)}

