from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntakeRequest:
    request_id: str
    goal: str
    content: str
    source_type: str


@dataclass(frozen=True)
class ExtractionPacket:
    packet_id: str
    request_id: str
    claim_text: str
    provenance: str
