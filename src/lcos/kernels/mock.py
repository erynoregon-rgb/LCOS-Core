from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MockKernel:
    kernel_id: str
    schema: str

    def process(self, content: str) -> dict:
        return {"kernel_id": self.kernel_id, "schema": self.schema, "content": content}
