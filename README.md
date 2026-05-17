# LCOS-Core Toy Public Package

AI agents make claims about what they did. This is infrastructure for verifying
those claims without trusting the agent's account.

The system is not asking whether an AI sounds trustworthy. It asks whether the
claim can be reconstructed from custody records, gate decisions, and receipts.

LCOS-Core demonstrates the two underlying primitives: chain of custody (what
happened, in what order, with what evidence) and control plane (who may act,
through which surface, under which gate). Everything else — typed decisions,
governed intake, deterministic routing, replay — is a specialized expression of
those two.

This is the self-contained public layer of a larger private research program.
The part that can be cloned, run, and inspected independently.

This package demonstrates a bounded toy implementation of receipt-gated governance
primitives: append-oriented receipt logs, tamper-aware replay, typed decision states,
claim lifecycle with transition receipts, gate-first execution, and public/private
disclosure boundaries.

## Try the demo in 60 seconds

```bash
python -m pip install -e .
python -m lcos_toy.cli demo-ledger
python -m lcos_toy.cli demo-intake examples/requests/simple_accept.json
python -m lcos_toy.cli demo-route "summarize this audit receipt"
python -m unittest discover -s tests
```

Expected results:

- `demo-ledger` — prints a hash-linked receipt timeline and confirms `valid=true`
- `demo-intake` — returns `{"kind": "ACCEPT", ...}` for a well-formed toy request
- `demo-route` — returns a deterministic kernel routing decision with a visible reason
- `tests` — all pass

For the full walkthrough including tamper detection and claim lifecycle, see
[`docs/research/WORKED_EXAMPLE_RECEIPT_REPLAY.md`](docs/research/WORKED_EXAMPLE_RECEIPT_REPLAY.md).

For what is implemented and where, see [`EVIDENCE_MAP.md`](EVIDENCE_MAP.md).

This package demonstrates:

- append-oriented JSONL receipt ledgers with hash-chain verification
- tamper-aware replay and timeline rendering
- typed hold/escalate/reject/accept decisions
- schema-light intake validation
- deterministic toy routing with visible reasons
- claim lifecycle state machine (OPEN → ACTIVE → HELD | COMPLETE)
- transition receipts with content-addressed IDs
- claim receipt chains with deterministic recovery IDs
- gate-first execution (admission receipt required before execution proceeds)
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
  receipt.py       receipt record and content-addressed digest logic
  ledger.py        append-oriented JSONL ledger and verifier
  decision.py      typed decision objects (ACCEPT/HOLD/REJECT/ESCALATE)
  intake.py        schema-light governed intake workbench
  router.py        deterministic toy router with visible reasons
  replay.py        audit/replay timeline renderer
  claim.py         claim state machine + TransitionReceipt emission
  chain.py         ClaimReceiptChain with deterministic recovery_id
  execution.py     RequestRecord → gate-first execution → ExecutionRecord
  cli.py           small command-line interface

tests/
  test_ledger.py
  test_intake.py
  test_router.py
  test_replay.py
  test_claim.py
  test_chain.py
  test_execution.py

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
