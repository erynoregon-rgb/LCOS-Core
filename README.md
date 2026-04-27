# LCOS-Core Toy Public Package

LCOS-Core Toy is a small, deterministic public scaffold for governed agentic
runtime primitives. It is designed to show the engineering spine without
publishing private strategy.

This package demonstrates:

- append-oriented JSONL receipt ledgers with hash-chain verification
- tamper-aware replay
- typed hold/escalate/reject/accept decisions
- schema-light intake validation
- deterministic toy routing with visible reasons
- adversarial fixture tests
- release/IP boundary documentation

It intentionally does not include:

- non-public implementation details
- production configuration
- real operational traces
- private source code, vocabulary, or architecture

## Public posture

Public equals mechanism class. Private equals mechanism advantage.

This toy repository is a reduced example for review, hiring, grant, and
research-facing evaluation. It is not the full private system and should not be
read as a publication of the decisive internal strategy.

The current license file is `All rights reserved` while patent/copyright and
future licensing posture are evaluated.

## Layout

```text
src/lcos_toy/
  receipt.py       receipt record and digest logic
  ledger.py        append-oriented JSONL ledger and verifier
  decision.py      typed decision objects
  intake.py        schema-light governed intake workbench
  router.py        deterministic toy router with explanations
  replay.py        audit/replay timeline renderer
  cli.py           small command-line interface

tests/
  test_ledger.py
  test_intake.py
  test_router.py
  test_replay.py

schemas/
  receipt.schema.json
  intake_request.schema.json
  routing_decision.schema.json

fixtures/adversarial/
  malformed_request.json
  ambiguous_request.json
  private_trace_reject_request.json
  out_of_scope_escalate_request.json

docs/release/
  RELEASE_INTENT.md
  PUBLIC_SCOPE.md
  IP_POSITION.md
  SKOS_TO_LCOS_BOUNDARY.md
  THIRD_PARTY_AND_ATTRIBUTION_REVIEW.md
  PUBLIC_DISCLOSURE_NOTICE.md

docs/research/
  hold_as_first_class_state.md
  deterministic_routing_for_auditability.md
  bounded_kernels_as_governance_surface.md
```

## Quick start

```bash
python -m pip install -e .
python -m lcos_toy.cli demo-ledger
python -m lcos_toy.cli demo-intake examples/requests/simple_accept.json
python -m lcos_toy.cli demo-route "summarize this audit receipt"
python -m unittest discover -s tests
```

## Claim safety

Implementation claims are limited to the contents of this repository. Research
notes are design discussion, not proof of private system capability.

See [PUBLIC_DISCLOSURE_NOTICE.md](./PUBLIC_DISCLOSURE_NOTICE.md) and
[`docs/release/`](./docs/release/) before publishing this repository.
