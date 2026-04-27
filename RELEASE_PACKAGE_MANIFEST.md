# LCOS-Core Toy Public Package Manifest

## Package rule

Show the engineering spine. Hide the decisive strategy.

## Included public surfaces

- Append-only receipt ledger
- Receipt-chain verification
- Audit/replay timeline renderer
- Governed intake workbench
- Deterministic toy router with visible reasons
- Contract-first JSON schemas
- Synthetic adversarial fixtures
- Unit tests for ledger, intake, routing, and replay
- Release/IP boundary documentation
- Research notes on design tradeoffs

## Explicit exclusions

- No non-public implementation details
- No production configuration
- No private system internals
- No real operational traces
- No SKOS imports or source code
- No private method couplings

## Validation commands

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m lcos_toy.cli demo-ledger
PYTHONPATH=src python3 -m lcos_toy.cli demo-intake examples/requests/simple_accept.json
PYTHONPATH=src python3 -m lcos_toy.cli demo-route "audit this receipt"
```

## Current validation result

- Unit tests: 10 passed
- CLI smoke demos: passed
- Dependency posture: Python standard library only
- License posture: All rights reserved

## Intended use

This zip is a public-safe toy repository seed. It can be inspected, copied into
a public repository, or used as a review artifact after the release decision is
confirmed.
