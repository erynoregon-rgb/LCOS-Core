from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .decision import Decision


@dataclass(frozen=True)
class IntakeRequest:
    request_id: str
    actor: str
    action: str
    content: str
    declared_scope: str = "toy"

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "IntakeRequest":
        missing = [key for key in ("request_id", "actor", "action", "content") if not payload.get(key)]
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        return cls(
            request_id=str(payload["request_id"]),
            actor=str(payload["actor"]),
            action=str(payload["action"]),
            content=str(payload["content"]),
            declared_scope=str(payload.get("declared_scope", "toy")),
        )


class GovernedIntake:
    blocked_terms = ("credential", "secret", "private trace")
    ambiguous_terms = ("maybe", "unknown", "unclear")

    def decide(self, request: IntakeRequest) -> Decision:
        text = f"{request.action} {request.content}".lower()
        if any(term in text for term in self.blocked_terms):
            return Decision("REJECT", "request contains blocked toy-safety term", (request.request_id,))
        if any(term in text for term in self.ambiguous_terms):
            return Decision("HOLD", "request needs more context before execution", (request.request_id,))
        if request.declared_scope != "toy":
            return Decision("ESCALATE", "scope is outside public toy boundary", (request.request_id,))
        return Decision("ACCEPT", "request is admissible in toy scope", (request.request_id,))

