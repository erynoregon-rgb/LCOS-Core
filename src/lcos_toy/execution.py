"""RequestRecord, ExecutionRecord, and gate-first execution.

The structural guarantee: a TransitionReceipt must exist before execution
proceeds. If the admission check fails, a HOLD receipt is emitted and
execution stops — it does not proceed and log afterward.

This is the toy demonstration of the gate-first vs. post-hoc distinction
the paper argues. The gate check is structural, not observational.

Public toy demonstration only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .claim import ClaimMachine, ClaimState, TransitionReceipt
from .chain import ClaimReceiptChain
from .decision import Decision
from .intake import GovernedIntake, IntakeRequest
from .receipt import stable_digest


@dataclass(frozen=True)
class RequestRecord:
    """Structured record of what was requested before any execution."""
    request_id: str
    actor: str
    action: str
    content: str
    declared_scope: str = "toy"
    submitted_at: str = ""

    @classmethod
    def create(
        cls,
        *,
        request_id: str,
        actor: str,
        action: str,
        content: str,
        declared_scope: str = "toy",
        timestamp: str | None = None,
    ) -> "RequestRecord":
        return cls(
            request_id=request_id,
            actor=actor,
            action=action,
            content=content,
            declared_scope=declared_scope,
            submitted_at=timestamp or datetime.now(timezone.utc).isoformat(),
        )

    def to_intake_request(self) -> IntakeRequest:
        return IntakeRequest(
            request_id=self.request_id,
            actor=self.actor,
            action=self.action,
            content=self.content,
            declared_scope=self.declared_scope,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "actor": self.actor,
            "action": self.action,
            "content": self.content,
            "declared_scope": self.declared_scope,
            "submitted_at": self.submitted_at,
        }


@dataclass(frozen=True)
class ExecutionRecord:
    """Record of what happened: request → admission decision → receipt → outcome.

    admission_receipt is the TransitionReceipt emitted at OPEN→ACTIVE.
    It must exist before execution proceeds — its presence is the structural
    gate, not a logged observation after the fact.

    If admission is denied, hold_receipt is set instead and execution_output
    is None. The chain is still complete: it ends in HELD state.
    """
    request: RequestRecord
    admission_decision: Decision
    admission_receipt: TransitionReceipt | None
    hold_receipt: TransitionReceipt | None
    execution_output: str | None
    chain: ClaimReceiptChain

    @property
    def admitted(self) -> bool:
        return self.admission_receipt is not None and self.hold_receipt is None

    @property
    def outcome(self) -> str:
        return self.chain.outcome

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request.to_dict(),
            "admission_decision": self.admission_decision.to_payload(),
            "admitted": self.admitted,
            "outcome": self.outcome,
            "admission_receipt_id": self.admission_receipt.receipt_id if self.admission_receipt else None,
            "hold_receipt_id": self.hold_receipt.receipt_id if self.hold_receipt else None,
            "execution_output": self.execution_output,
            "chain": self.chain.to_dict(),
        }


class GoverningExecutor:
    """Gate-first executor: admission receipt must exist before execution runs.

    Pattern:
      1. Validate request via GovernedIntake (structural gate check)
      2. If ACCEPT: emit OPEN→ACTIVE TransitionReceipt, execute, emit ACTIVE→COMPLETE
      3. If HOLD/REJECT/ESCALATE: emit OPEN→HELD TransitionReceipt, stop
      4. Return ExecutionRecord with full ClaimReceiptChain

    The gate is not a log entry written after execution. If the admission
    receipt is absent, execution has not happened.
    """

    def __init__(self, actor: str = "GoverningExecutor") -> None:
        self.actor = actor
        self._intake = GovernedIntake()

    def execute(
        self,
        request: RequestRecord,
        *,
        timestamp: str | None = None,
    ) -> ExecutionRecord:
        machine = ClaimMachine(claim_id=request.request_id, actor=self.actor)
        intake_req = request.to_intake_request()
        decision = self._intake.decide(intake_req)

        if decision.kind == "ACCEPT":
            # Gate passed — emit admission receipt, then execute
            admission = machine.activate(
                reason=f"intake decision: {decision.reason}",
                timestamp=timestamp,
            )
            # Execute (toy: echo the content back)
            output = f"[executed] {request.action}: {request.content}"
            completion = machine.complete(
                reason="execution finished",
                metadata={"output_digest": stable_digest({"output": output})},
            )
            chain = ClaimReceiptChain.build(request.request_id, machine.receipts)
            return ExecutionRecord(
                request=request,
                admission_decision=decision,
                admission_receipt=admission,
                hold_receipt=None,
                execution_output=output,
                chain=chain,
            )
        else:
            # Gate failed — emit HOLD receipt, stop; do not execute
            hold = machine.hold(
                reason=f"intake decision: {decision.kind} — {decision.reason}",
                timestamp=timestamp,
            )
            chain = ClaimReceiptChain.build(request.request_id, machine.receipts)
            return ExecutionRecord(
                request=request,
                admission_decision=decision,
                admission_receipt=None,
                hold_receipt=hold,
                execution_output=None,
                chain=chain,
            )
