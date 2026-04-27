from __future__ import annotations

from dataclasses import dataclass

from lcos.governance.decision import Decision

from .registry import KernelDescriptor


@dataclass(frozen=True)
class RouteResult:
    decision: str
    kernel_id: str | None
    reason: str


class DeterministicRouter:
    def __init__(self, registry: list[KernelDescriptor]):
        self.registry = sorted(registry, key=lambda k: (-k.priority, k.kernel_id))

    def route(self, content: str) -> RouteResult:
        lowered = content.lower()
        for kernel in self.registry:
            if kernel.capability in lowered:
                return RouteResult(decision="ROUTE", kernel_id=kernel.kernel_id, reason=f"matched capability '{kernel.capability}'")
        if "novel" in lowered or "unknown" in lowered:
            return RouteResult(decision="ESCALATE", kernel_id=None, reason="no bounded kernel match")
        return RouteResult(decision="HOLD", kernel_id=None, reason="insufficient routing confidence")
