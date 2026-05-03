# Proof Boundary

LCOS-Core is a public proof-of-mechanism scaffold.

## What this repo demonstrates

This repository provides a reduced example of:

- append-oriented receipt ledgers
- hash-chain verification
- typed decision states
- deterministic toy routing
- replay and timeline rendering
- schema-light intake validation
- adversarial synthetic fixtures
- public/private release boundaries

## What this repo does not prove

This repository does not prove:

- general AI safety
- production reliability
- adversary-proof auditability
- OS-enforced immutability
- full SKOS-Core capability
- real-world agent adoption
- broad external validity

## How to inspect the proof

Run:

```bash
python -m unittest discover -s tests
python -m lcos_toy.cli demo-ledger
python -m lcos_toy.cli demo-route "audit this receipt"
```

## Claim boundary

The safe claim is:

> LCOS-Core demonstrates selected mechanism classes for governed, auditable agent workflows in a reduced public scaffold.

The unsafe claim is:

> LCOS-Core proves the full private system is safe or production-ready.
