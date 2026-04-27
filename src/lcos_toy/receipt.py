from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def stable_digest(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Receipt:
    seq: int
    event_type: str
    payload_digest: str
    prev_digest: str | None
    timestamp: str
    metadata: dict[str, Any] = field(default_factory=dict)
    digest: str = ""

    def unsigned_record(self) -> dict[str, Any]:
        return {
            "seq": self.seq,
            "event_type": self.event_type,
            "payload_digest": self.payload_digest,
            "prev_digest": self.prev_digest,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    def expected_digest(self) -> str:
        return stable_digest(self.unsigned_record())

    def to_record(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "receipt": {**self.unsigned_record(), "digest": self.digest},
            "payload": payload,
        }

    @classmethod
    def create(
        cls,
        *,
        seq: int,
        event_type: str,
        payload: dict[str, Any],
        prev_digest: str | None,
        timestamp: str,
        metadata: dict[str, Any] | None = None,
    ) -> "Receipt":
        receipt = cls(
            seq=seq,
            event_type=event_type,
            payload_digest=stable_digest(payload),
            prev_digest=prev_digest,
            timestamp=timestamp,
            metadata=metadata or {},
        )
        return cls(**receipt.unsigned_record(), digest=receipt.expected_digest())

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "Receipt":
        data = record["receipt"]
        return cls(
            seq=data["seq"],
            event_type=data["event_type"],
            payload_digest=data["payload_digest"],
            prev_digest=data.get("prev_digest"),
            timestamp=data["timestamp"],
            metadata=data.get("metadata", {}),
            digest=data["digest"],
        )

