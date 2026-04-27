from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from .intake import GovernedIntake, IntakeRequest
from .ledger import AppendOnlyLedger
from .replay import render_timeline
from .router import Capability, ToyRouter


def demo_ledger() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        ledger_path = Path(tmp) / "toy-ledger.jsonl"
        ledger = AppendOnlyLedger(ledger_path)
        ledger.append("INTAKE", {"request_id": "demo-1", "action": "summarize"}, timestamp="2026-01-01T00:00:00+00:00")
        ledger.append("DECISION", {"kind": "ACCEPT", "reason": "toy demo"}, timestamp="2026-01-01T00:00:01+00:00")
        print(render_timeline(ledger_path))
    return 0


def demo_intake(path: str) -> int:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    request = IntakeRequest.from_payload(payload)
    decision = GovernedIntake().decide(request)
    print(json.dumps(decision.to_payload(), indent=2, sort_keys=True))
    return 0


def demo_route(text: str) -> int:
    router = ToyRouter(
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LCOS toy public demo CLI")
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
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())

