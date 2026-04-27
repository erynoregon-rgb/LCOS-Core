from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Iterable

from .receipt import Receipt, canonical_json, stable_digest


@dataclass(frozen=True)
class VerificationIssue:
    seq: int
    code: str
    detail: str


@dataclass(frozen=True)
class VerificationReport:
    valid: bool
    count: int
    issues: tuple[VerificationIssue, ...]


class AppendOnlyLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(
        self,
        event_type: str,
        payload: dict[str, Any],
        *,
        metadata: dict[str, Any] | None = None,
        timestamp: str | None = None,
    ) -> Receipt:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        records = list(self.records())
        prev = Receipt.from_record(records[-1]).digest if records else None
        receipt = Receipt.create(
            seq=len(records) + 1,
            event_type=event_type,
            payload=payload,
            prev_digest=prev,
            timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
            metadata=metadata,
        )
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(canonical_json(receipt.to_record(payload)) + "\n")
        return receipt

    def records(self) -> Iterable[dict[str, Any]]:
        if not self.path.exists():
            return ()
        return tuple(json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip())

    def verify(self, *, strict: bool = False) -> VerificationReport:
        issues: list[VerificationIssue] = []
        prev_digest: str | None = None
        count = 0

        if not self.path.exists():
            if strict:
                issues.append(VerificationIssue(0, "MISSING_LEDGER", "ledger path does not exist"))
            return VerificationReport(valid=not issues, count=0, issues=tuple(issues))

        for line_no, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            count += 1
            try:
                record = json.loads(line)
            except JSONDecodeError as error:
                issues.append(VerificationIssue(line_no, "MALFORMED_JSON", f"invalid JSON line: {error.msg}"))
                continue
            receipt = Receipt.from_record(record)
            payload = record.get("payload", {})

            if receipt.seq != count:
                issues.append(VerificationIssue(receipt.seq, "SEQ_MISMATCH", f"expected {count}, got {receipt.seq}"))
            if receipt.prev_digest != prev_digest:
                issues.append(VerificationIssue(receipt.seq, "PARENT_MISMATCH", "previous digest linkage does not match"))
            if receipt.payload_digest != stable_digest(payload):
                issues.append(VerificationIssue(receipt.seq, "PAYLOAD_TAMPERED", "payload digest does not match payload"))
            if receipt.digest != receipt.expected_digest():
                issues.append(VerificationIssue(receipt.seq, "RECEIPT_TAMPERED", "receipt digest does not match receipt fields"))

            prev_digest = receipt.digest

        return VerificationReport(valid=not issues, count=count, issues=tuple(issues))
