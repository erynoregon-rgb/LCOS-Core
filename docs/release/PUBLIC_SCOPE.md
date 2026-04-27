# Public Scope — LCOS-Core

This document defines what is and is not in the public release.

## Public Surface (This Repository)

### Code that is public
- `src/lcos/receipts/` — append-only receipt models, verification, ledger storage
- `src/lcos/governance/` — decision types and policy decision helpers
- `src/lcos/intake/` — typed intake request, validation pipeline, example
- `src/lcos/routing/` — deterministic router, kernel registry, mock kernels
- `src/lcos/state/` — continuous state placeholders and transition examples
- `src/lcos/kernels/` — bounded kernel interfaces and mock implementations

### Tests that are public
- `tests/receipts/` — receipt chain and verification tests
- `tests/governance/` — decision type tests
- `tests/intake/` — intake validation pipeline tests
- `tests/routing/` — deterministic routing tests

### Examples that are public
- `examples/minimal_receipt_chain/demo.py` — receipt chain instantiation
- `examples/governed_intake_demo/demo.py` — intake request + policy decision flow
- `examples/routing_demo/demo.py` — deterministic router with HOLD/ESCALATE
- `examples/minimal_continuous_state/` — state transition sketches

### Docs that are public
- `docs/concepts/` — implementation-facing architectural notes
- `docs/examples/` — walkthroughs tied to runnable examples
- `docs/research/` — research hypotheses and design questions

## What is NOT public (Kept separate)

### Private (not in this repo)
- SKOS-Core internals (governance, continuity, artifact systems)
- Organizational design language or symbolic vocabulary
- Strategic architectural decisions not generalized to LCOS
- Private lineage notes or decision records
- Unreleased empirical results or datasets
- Confidential partner collaborations

### Intentionally generic
- This repository uses no SKOS-specific naming or methods
- Receipt model is intentionally simple and generic
- Routing model is intentionally deterministic and explicit
- Intake model is intentionally schema-independent
- No reliance on SKOS-specific infrastructure

## Claim Boundaries

### Implementation claims (backed by code + tests)
- Receipt chain construction and verification
- Intake request validation and decision flow
- Deterministic routing with bounded kernels
- Append-only state transition storage

### Example claims (illustrative, not general)
- Governed intake demo (specific, not a general intake framework)
- Routing demo (small, deterministic, not a production router)
- Continuous state demo (sketch, not a production system)

### Research claims (hypotheses, not proof)
- Operator kernel bounding strategies
- Routing graph optimization approaches
- Continuous state modeling approaches

All research claims are in `docs/research/` and clearly marked as exploratory.

## Attribution

### LCOS-Core original work
- Receipt model architecture
- Governance decision framework
- Bounded kernel interface
- Deterministic routing implementation
- Example implementations and walkthroughs

### Lineage acknowledged
- SKOS-Core development provided context and iterative feedback
- Academic literature on formal verification influenced design
- See [SKOS_TO_LCOS_DERIVATION_MAP.md](./SKOS_TO_LCOS_DERIVATION_MAP.md) for fuller lineage

### No embedded proprietary material
- No verbatim copying from SKOS
- No embedded organizational code
- No reliance on unreleased third-party work
- All code written for this public release

## Public-First Discipline

To maintain clean boundaries:

1. **No private vocabulary in public code**
   - Use generic terms (`Receipt`, `Decision`, `Kernel`, not `Capsule`, `Authority`, `Vessel`)
   - Document why generic terms are chosen

2. **No back-reference to SKOS methods**
   - LCOS is self-contained
   - SKOS can reference LCOS, but not vice versa

3. **Example limitations are explicit**
   - Every demo includes "This is illustrative; production use requires..."
   - No secret dependencies on SKOS infrastructure

4. **Research notes are not implementation**
   - `docs/research/` is for ideas, not proofs
   - Running code is the proof

---

**Scope Owner:** Public release coordinator
**Last reviewed:** April 2026
**Next review:** Upon license finalization
