from __future__ import annotations

from pathlib import Path

from .ledger import AppendOnlyLedger
from .receipt import Receipt


def render_timeline(path: str | Path) -> str:
    ledger = AppendOnlyLedger(path)
    lines = ["seq | event_type | digest_prefix | parent_prefix"]
    for record in ledger.records():
        receipt = Receipt.from_record(record)
        lines.append(
            f"{receipt.seq} | {receipt.event_type} | {receipt.digest[:12]} | "
            f"{receipt.prev_digest[:12] if receipt.prev_digest else 'ROOT'}"
        )
    report = ledger.verify()
    lines.append(f"valid={str(report.valid).lower()} count={report.count} issues={len(report.issues)}")
    for issue in report.issues:
        lines.append(f"issue seq={issue.seq} code={issue.code} detail={issue.detail}")
    return "\n".join(lines)

