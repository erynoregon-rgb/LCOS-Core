from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KernelDescriptor:
    kernel_id: str
    capability: str
    schema: str
    priority: int = 0
