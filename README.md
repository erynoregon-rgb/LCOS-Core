# LCOS-Core

**LCOS-Core** is a Layered Cognitive Operations Substrate for governed agentic systems.

It is a research-oriented runtime for governed inference. The repository explores receipt-gated execution, deterministic routing, bounded operator kernels, and continuous state handling. It includes generic infrastructure, research notes, and runnable examples designed to make runtime claims auditable and implementation-facing.

## Scope

This public repository contains independent, generalized research and example code released as a public substrate. It is not a mirror of any private repository, employer work product, or unreleased internal architecture.

The public surface focuses on three stable slices:

1. **Receipt and audit core**
   - append-only receipt objects
   - parent-linked receipt chain
   - verification utilities
   - minimal CLI demo
2. **Governed intake example**
   - typed intake request
   - validation
   - admissibility decision
   - extraction packet example
   - receipts on every stage
3. **Routing research demo**
   - small deterministic router
   - registry of kernel capabilities
   - example bounded models or mock kernels
   - explicit `HOLD` / `ESCALATE` behavior

## Repository layout

```text
src/lcos/
  receipts/      append-only receipts and verification
  governance/    decision types and policy helpers
  intake/        typed request/intake example
  routing/       deterministic routing demo
  state/         continuous state placeholders
  kernels/       bounded kernel interfaces and mocks

examples/
  minimal_receipt_chain/
  governed_intake_demo/
  routing_demo/

docs/
  concepts/      implementation-facing notes
  research/      hypothesis/spec/research notes
  examples/      walkthroughs
  release/       IP and release documentation

tests/
  receipts/
  intake/
  routing/
```

## Claim safety

See [CLAIMS.md](./CLAIMS.md).

External implementation claims are supported by code, tests, or public docs in this repository. Public implementation claims are limited to the contents of this repository. Research notes are not implementation claims.

## IP and Release

This repository is released with `All rights reserved.` pending license finalization. See [`docs/release/`](./docs/release/) for:

- [RELEASE_INTENT.md](./docs/release/RELEASE_INTENT.md) — What is being released
- [PUBLIC_SCOPE.md](./docs/release/PUBLIC_SCOPE.md) — Public surface definition
- [IP_POSITION.md](./docs/release/IP_POSITION.md) — Patent and licensing strategy
- [SKOS_TO_LCOS_DERIVATION_MAP.md](./docs/release/SKOS_TO_LCOS_DERIVATION_MAP.md) — Lineage and separation from SKOS
- [THIRD_PARTY_AND_ATTRIBUTION_REVIEW.md](./docs/release/THIRD_PARTY_AND_ATTRIBUTION_REVIEW.md) — Dependency and attribution audit

## Milestones

### Milestone 1 — public seed
- README
- LICENSE
- CLAIMS.md
- repo structure
- receipt-chain example
- one governed-intake example

### Milestone 2 — generic runtime core
- `src/lcos/receipts`
- `src/lcos/governance`
- `src/lcos/intake`
- tests for all three

### Milestone 3 — research lane
- operator kernel note
- routing graph note
- continuous state note
- one minimal runnable routing demo

## Quick start

```bash
python -m pip install -e .
python examples/minimal_receipt_chain/demo.py
python examples/governed_intake_demo/demo.py
python examples/routing_demo/demo.py
pytest
```

## Status

This repository contains a mix of implemented examples and research notes.

- `src/` and `tests/` are the primary basis for runtime claims.
- `docs/research/` contains definitions, hypotheses, and open questions.
- `examples/` are illustrative unless backed by tests.
