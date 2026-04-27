from __future__ import annotations

from dataclasses import dataclass

from .decision import Decision


@dataclass(frozen=True)
class Capability:
    kernel_id: str
    capability: str
    priority: int = 0


@dataclass(frozen=True)
class Route:
    decision: Decision
    kernel_id: str | None

    def to_payload(self) -> dict[str, object]:
        payload = self.decision.to_payload()
        payload["kernel_id"] = self.kernel_id
        return payload


class ToyRouter:
    def __init__(self, capabilities: list[Capability]):
        self.capabilities = sorted(capabilities, key=lambda item: (-item.priority, item.kernel_id))

    def route(self, text: str) -> Route:
        lowered = text.lower()
        for capability in self.capabilities:
            if capability.capability.lower() in lowered:
                return Route(
                    Decision("ACCEPT", f"matched capability: {capability.capability}", (capability.kernel_id,)),
                    capability.kernel_id,
                )
        if "unknown" in lowered or "novel" in lowered:
            return Route(Decision("ESCALATE", "no bounded toy kernel matches request"), None)
        return Route(Decision("HOLD", "insufficient evidence to choose a bounded toy kernel"), None)

