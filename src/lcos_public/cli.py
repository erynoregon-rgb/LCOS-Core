from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from .intake import GovernedIntake, IntakeRequest
from .ledger import AppendOnlyLedger
from .publication import PublicationBoundaryViolation, export_public_paper_surface
from .replay import render_timeline
from .router import Capability, PublicRouter


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
    if args.command == "verify":
        return verify(args.path)
    if args.command == "replay":
        return replay(args.path)
    if args.command == "export-paper":
        return export_paper(args.source, args.destination)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
