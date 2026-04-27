# SKOS-to-LCOS Derivation Map

This document clarifies the relationship between SKOS-Core (private) and LCOS-Core (public).

## High-level relationship

```
SKOS-Core (private)
  ├─ contains full multi-layer governance system
  ├─ contains continuity + consent infrastructure
  ├─ contains artifact envelope + receipt chain
  ├─ contains confidential partner integrations
  └─ serves as proof-of-concept for principles

LCOS-Core (public)
  ├─ extracts receipt and decision patterns
  ├─ generalizes routing and intake models
  ├─ provides generic, self-contained implementations
  ├─ documents design rationale
  └─ serves as academic/open-source substrate
```

## What LCOS-Core uses from SKOS-Core principles

**Receipt chain design**
- SKOS-Core implements receipt chains in `src/skos_core/artifact/envelope.py`
- LCOS-Core implements generic receipt model in `src/lcos/receipts/models.py`
- **Difference:** LCOS receipts are minimal and schema-independent; SKOS receipts carry governance authority

**Governance decisions**
- SKOS-Core uses multi-authority decision model in `src/skos_core/governance/`
- LCOS-Core implements simplified decision types in `src/lcos/governance/`
- **Difference:** LCOS decisions are illustrative; SKOS decisions enforce policy across layers

**Routing**
- SKOS-Core routes through kernel-like components in multi-layer system
- LCOS-Core implements deterministic router in `src/lcos/routing/`
- **Difference:** LCOS router is synchronous and explicit; SKOS routing is policy-driven and multi-stage

**Bounded operators**
- SKOS-Core models bounded kernels as constrained computation units
- LCOS-Core sketches kernel interfaces in `src/lcos/kernels/`
- **Difference:** LCOS kernel model is research-level; SKOS kernels are production-integrated

## What LCOS-Core does NOT use

**Confidential materials:**
- SKOS continuity infrastructure (private partner agreements)
- SKOS artifact authority model (strategic organizational design)
- SKOS symbolic vocabulary (internal naming conventions)
- SKOS multi-layer orchestration (not released)

**Strategic components:**
- SKOS multi-AI coordination (not generalized)
- SKOS governance audit trail system (still in development)
- SKOS consent gate enforcement (organizational-specific)
- SKOS recovery and replay infrastructure (proprietary methods)

## Code inventory

### Parallel implementations (same concept, separate code)

| Concept | SKOS | LCOS | Note |
|---------|------|------|------|
| Receipt | `src/skos_core/artifact/envelope.py` | `src/lcos/receipts/models.py` | Different implementation; LCOS is minimal |
| Receipt chain | `src/skos_core/artifact/envelope.py` | `src/lcos/receipts/ledger.py` | LCOS append-only; SKOS authority-linked |
| Decision | `src/skos_core/governance/` | `src/lcos/governance/decision.py` | LCOS is illustrative; SKOS enforces policy |
| Intake | (exists internally) | `src/lcos/intake/pipeline.py` | LCOS example; SKOS uses different model |
| Routing | (exists internally) | `src/lcos/routing/router.py` | LCOS is deterministic demo; SKOS is policy-driven |

### Unique to LCOS (generalized)

- Bounded kernel interfaces (`src/lcos/kernels/`)
- Schema-independent intake request model (`src/lcos/intake/models.py`)
- Mock kernel implementations (for demos)

### Unique to SKOS (not released)

- Multi-layer artifact composition
- Authority verification and monotonicity enforcement
- Continuity + consent gates
- Multi-AI orchestration
- Partner integration infrastructure

## Attribution and lineage

**LCOS-Core authors**
- Eryn Eldvar (primary)

**Acknowledgments**
- SKOS-Core development team (context + iterative feedback)
- Academic literature on formal verification
- Open-source community (best practices)

**Why separate?**
1. LCOS is self-contained (no SKOS dependencies)
2. SKOS remains private (no LCOS constraints)
3. Each can evolve independently
4. Clean boundary prevents accidental disclosure

## Licensing and IP

**SKOS-Core:** Private; no public license
**LCOS-Core:** Public; pending license decision (see [RELEASE_INTENT.md](./RELEASE_INTENT.md))

**Patent considerations:**
- SKOS-Core may be subject to patent filings
- LCOS-Core is public disclosure (may affect patent windows)
- See [IP_POSITION.md](./IP_POSITION.md) for strategic considerations

**Code reuse:**
- No SKOS code is copied into LCOS
- No LCOS code is copied into SKOS
- Both can reference each other's design principles

## Verification

To verify that LCOS is genuinely separate from SKOS:

1. **Code review:** LCOS contains no SKOS imports or references
   ```bash
   grep -r "skos_core\|SKOS\|from skos" src/lcos tests/
   # Should return: (nothing)
   ```

2. **Vocabulary check:** LCOS uses only generic terms (Receipt, Decision, Kernel, Router)
   ```bash
   grep -r "Capsule\|Vessel\|Authority\|Continuity\|Artifact" src/lcos tests/
   # Should return: (nothing)
   ```

3. **Dependency check:** LCOS pyproject.toml has no SKOS dependency
   ```bash
   grep skos pyproject.toml
   # Should return: (nothing)
   ```

---

**Maintained by:** Public release coordinator
**Last updated:** April 2026
**Next review:** Upon license finalization or major SKOS update
