from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DecisionStatus = Literal["ACCEPT", "REJECT", "HOLD", "ESCALATE"]


@dataclass(frozen=True)
class Decision:
    status: DecisionStatus
    reason: str
    confidence: float
