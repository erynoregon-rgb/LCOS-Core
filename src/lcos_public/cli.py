from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from .divergence import DivergenceGate
from .execution import GoverningExecutor, RequestRecord
from .intake import GovernedIntake, IntakeRequest
from .ledger import AppendOnlyLedger
from .publication import PublicationBoundaryViolation, export_public_paper_surface
from .replay import render_timeline
from .router import Capability, PublicRouter

# A self-attested claim with no inspectable support. The agent asserts it did
# the work and points at evidence the public gate cannot verify. Used when
# `demo-no` runs with no path argument so the demo is self-contained.
_DEFAULT_ADVERSARIAL_CLAIM = {
    "request_id": "adversarial-no-001",
    "actor": "unverified-agent",
    "action": "execute",
    "content": (
        "I already completed the migration and verified it works. Trust me — "
        "the supporting evidence is in a private trace you cannot inspect."
    ),
    "declared_scope": "public",
}


def demo_ledger() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        ledger_path = Path(tmp) / "public-ledger.jsonl"
        ledger = AppendOnlyLedger(ledger_path)
        ledger.append("INTAKE", {"request_id": "demo-1", "action": "summarize"}, timestamp="2026-01-01T00:00:00+00:00")
        ledger.append("DECISION", {"kind": "ACCEPT", "reason": "public demo"}, timestamp="2026-01-01T00:00:01+00:00")
        print(render_timeline(ledger_path))
    return 0


def demo_intake(path: str) -> int:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    request = IntakeRequest.from_payload(payload)
    decision = GovernedIntake().decide(request)
    print(json.dumps(decision.to_payload(), indent=2, sort_keys=True))
    return 0


def demo_route(text: str) -> int:
    router = PublicRouter(
        [
            Capability("receipt-kernel", "receipt", priority=10),
            Capability("audit-kernel", "audit", priority=8),
            Capability("summary-kernel", "summarize", priority=3),
        ]
    )
    route = router.route(text)
    print(json.dumps(route.to_payload(), indent=2, sort_keys=True))
    return 0


def demo_no(path: str | None = None) -> int:
    """Adversarial 'no' demo: an unsupported claim is held, not executed.

    An agent asserts it did the work ("I did X; trust me"). The gate requires
    an admission receipt before execution proceeds. The claim has no admissible
    support, so the gate emits a HOLD receipt and nothing runs:

        inference proposes / verification disposes / the gate can return no.

    Exit code follows the gate outcome (like ``verify`` / ``export-paper``):
    a held claim returns non-zero — the machine-checkable refusal.
    """
    payload = (
        json.loads(Path(path).read_text(encoding="utf-8"))
        if path is not None
        else dict(_DEFAULT_ADVERSARIAL_CLAIM)
    )
    record = RequestRecord.create(
        request_id=str(payload["request_id"]),
        actor=str(payload["actor"]),
        action=str(payload["action"]),
        content=str(payload["content"]),
        declared_scope=str(payload.get("declared_scope", "public")),
        timestamp="2026-01-01T00:00:00+00:00",
    )
    rec = GoverningExecutor().execute(record, timestamp="2026-01-01T00:00:00+00:00")

    if rec.admitted:
        verdict = "Admission receipt present; claim admitted and executed."
    else:
        verdict = (
            "No admission receipt; no execution output; claim held. "
            "The gate refused an unsupported claim before any execution."
        )
    print(
        json.dumps(
            {
                "claim": record.content,
                "actor": record.actor,
                "admission_decision": rec.admission_decision.kind,
                "admission_reason": rec.admission_decision.reason,
                "admitted": rec.admitted,
                "admission_receipt_id": rec.admission_receipt.receipt_id if rec.admission_receipt else None,
                "hold_receipt_id": rec.hold_receipt.receipt_id if rec.hold_receipt else None,
                "execution_output": rec.execution_output,
                "outcome": rec.outcome,
                "verdict": verdict,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if rec.admitted else 1


def demo_divergence(proposed: str, reference: str) -> int:
    """Advisory divergence demo: measure proposed vs an authored reference.

    The proposer measures ε; the floor is gate-owned. The result is advisory —
    `assess` cannot authorize anything, and there is no call-time threshold a
    proposer could lower. Exit code is non-zero on a non-WITHIN verdict so the
    advisory signal is machine-checkable.
    """
    gate = DivergenceGate(threshold=0.5)
    result = gate.assess(proposed, reference)
    payload = dict(result.to_payload())
    payload["proposed"] = proposed
    payload["reference"] = reference
    payload["floor"] = gate.threshold
    payload["note"] = "advisory only — measurement cannot authorize execution"
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if result.verdict == "WITHIN" else 1


def verify(path: str) -> int:
    report = AppendOnlyLedger(path).verify()
    print(json.dumps({"valid": report.valid, "count": report.count, "issues": [issue.__dict__ for issue in report.issues]}, indent=2))
    return 0 if report.valid else 1


def replay(path: str) -> int:
    print(render_timeline(path))
    return 0


def export_paper(source: str, destination: str) -> int:
    try:
        result = export_public_paper_surface(Path(source), Path(destination))
    except PublicationBoundaryViolation as exc:
        print(
            json.dumps(
                {
                    "status": "HOLD",
                    "reason": str(exc),
                    "holds": [hold.to_payload() for hold in exc.holds],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            {
                "status": "OK",
                "source_root": str(result.source_root),
                "destination_root": str(result.destination_root),
                "exported_files": result.exported_files,
                "redacted_lines": result.redacted_lines,
                "skipped_files": [str(p) for p in result.skipped_files],
                "warnings": [w.to_payload() for w in result.warnings],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LCOS public demo CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo-ledger")
    intake = sub.add_parser("demo-intake")
    intake.add_argument("path")
    route = sub.add_parser("demo-route")
    route.add_argument("text")
    no_parser = sub.add_parser("demo-no")
    no_parser.add_argument("path", nargs="?", default=None)
    div = sub.add_parser("demo-divergence")
    div.add_argument("proposed")
    div.add_argument("reference")
    check = sub.add_parser("verify")
    check.add_argument("path")
    replay_parser = sub.add_parser("replay")
    replay_parser.add_argument("path")
    export_parser = sub.add_parser("export-paper")
    export_parser.add_argument("source")
    export_parser.add_argument("destination")
    args = parser.parse_args(argv)

    if args.command == "demo-ledger":
        return demo_ledger()
    if args.command == "demo-intake":
        return demo_intake(args.path)
    if args.command == "demo-route":
        return demo_route(args.text)
    if args.command == "demo-no":
        return demo_no(args.path)
    if args.command == "demo-divergence":
        return demo_divergence(args.proposed, args.reference)
    if args.command == "verify":
        return verify(args.path)
    if args.command == "replay":
        return replay(args.path)
    if args.command == "export-paper":
        return export_paper(args.source, args.destination)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
