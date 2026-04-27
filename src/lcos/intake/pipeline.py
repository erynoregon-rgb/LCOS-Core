from __future__ import annotations

from hashlib import sha256

from lcos.governance.decision import Decision
from lcos.receipts.ledger import ReceiptLedger

from .models import ExtractionPacket, IntakeRequest


def validate_request(req: IntakeRequest) -> None:
    if not req.request_id.strip():
        raise ValueError("request_id required")
    if not req.goal.strip():
        raise ValueError("goal required")
    if not req.content.strip():
        raise ValueError("content required")
    if not req.source_type.strip():
        raise ValueError("source_type required")


def admissibility_decision(req: IntakeRequest) -> Decision:
    lowered = req.content.lower()
    if "forbidden" in lowered:
        return Decision(status="REJECT", reason="contains forbidden marker", confidence=0.95)
    if len(req.content.strip()) < 20:
        return Decision(status="HOLD", reason="content too short for extraction", confidence=0.55)
    return Decision(status="ACCEPT", reason="admissible for demo extraction", confidence=0.85)


def build_extraction_packet(req: IntakeRequest) -> ExtractionPacket:
    claim_text = req.content.strip().split(".")[0].strip()
    packet_id = sha256(f"{req.request_id}|{claim_text}".encode("utf-8")).hexdigest()[:16]
    return ExtractionPacket(packet_id=packet_id, request_id=req.request_id, claim_text=claim_text, provenance=req.source_type)


def run_intake(req: IntakeRequest, ledger: ReceiptLedger) -> tuple[Decision, ExtractionPacket | None]:
    validate_request(req)
    ledger.append("intake.request.validated", req.request_id, {"goal": req.goal, "source_type": req.source_type})
    decision = admissibility_decision(req)
    decision_receipt = ledger.append(
        "intake.request.admissibility",
        req.request_id,
        {"status": decision.status, "reason": decision.reason, "confidence": decision.confidence},
    )
    if decision.status != "ACCEPT":
        return decision, None
    packet = build_extraction_packet(req)
    ledger.append(
        "intake.request.extracted",
        packet.packet_id,
        {"request_id": packet.request_id, "claim_text": packet.claim_text, "provenance": packet.provenance},
        parent_receipt_id=decision_receipt.receipt_id,
    )
    return decision, packet
