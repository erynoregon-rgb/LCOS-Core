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
    declared_scope: str = "public"

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
            declared_scope=str(payload.get("declared_scope", "public")),
        )


class GovernedIntake:
    blocked_terms = ("credential", "secret", "private trace")
    ambiguous_terms = ("maybe", "unknown", "unclear")

    def __init__(
        self,
        *,
        divergence_gate: "DivergenceGate | None" = None,
        reference: str | None = None,
        enforce_divergence: bool = False,
    ) -> None:
        # Divergence is advisory and OFF by default: a default GovernedIntake()
        # behaves exactly as it did before divergence existed. When enabled it
        # can only TIGHTEN (ACCEPT -> HOLD); it can never authorize execution.
        self._divergence_gate = divergence_gate
        self._reference = reference
        self._enforce_divergence = enforce_divergence

    def decide(self, request: IntakeRequest) -> Decision:
        decision = self._base_decide(request)

        if self._divergence_gate is not None and self._reference is not None:
            result = self._divergence_gate.assess(
                f"{request.action} {request.content}", self._reference
            )
            # One-directional: only an ACCEPT can be tightened to HOLD, and only
            # when enforcement is on. A non-ACCEPT decision is never upgraded.
            if (
                self._enforce_divergence
                and decision.kind == "ACCEPT"
                and result.verdict == "DIVERGENT"
            ):
                return Decision(
                    "HOLD",
                    f"advisory divergence tighten: {result.reason}",
                    (request.request_id,),
                )
        return decision

    def _base_decide(self, request: IntakeRequest) -> Decision:
        text = f"{request.action} {request.content}".lower()
        if any(term in text for term in self.blocked_terms):
            return Decision("REJECT", "request contains blocked public-safety term", (request.request_id,))
        if any(term in text for term in self.ambiguous_terms):
            return Decision("HOLD", "request needs more context before execution", (request.request_id,))
        if request.declared_scope != "public":
            return Decision("ESCALATE", "scope is outside public boundary", (request.request_id,))
        return Decision("ACCEPT", "request is admissible in public scope", (request.request_id,))
