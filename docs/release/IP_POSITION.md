# IP Position Statement — LCOS-Core

**Current status:** `All rights reserved.` (pre-license decision)
**Decision horizon:** Q3 2026
**Scope:** Patent and licensing strategy

## What this statement covers

This document outlines:
- Current IP posture
- Patent filing considerations
- Licensing decision framework
- Public disclosure risk/benefit
- Path to final decision

## Current IP posture

### License status (TODAY)
- **Current license:** `All rights reserved.`
- **Rights granted:** None (no public copying, modification, or distribution rights)
- **Exceptions:** Academic citation and reference permitted under fair use
- **Rationale:** Preserve flexibility pending strategic decisions

### Why not choose a license now?

1. **Patent filing windows:** Public disclosure may affect patent eligibility
   - Need to assess which methods/algorithms are novel and defensible
   - Patent window typically closes 1 year after public disclosure
   - LCOS release is a deliberate public disclosure event

2. **Licensing strategy not finalized:**
   - Undecided between open-source (MIT/Apache) and proprietary
   - May want dual licensing (open for research, proprietary for commercial)
   - May want source-available (GitHub visible but restricted use)

3. **Organizational context:**
   - Depends on partner agreements and strategic partnerships
   - May need executive/legal review before committing to open source
   - SKOS-Core remains private; LCOS relationship still evolving

4. **Market/community assessment pending:**
   - Need to gauge academic interest and contribution patterns
   - Need to assess commercial interest before choosing strategy
   - Current posture allows pivoting based on feedback

## Patent considerations

### Current position
- **Patent filing:** Not yet filed (as of April 2026)
- **Disclosure status:** This repository is public disclosure
- **Patent clock:** ~12 months remain for U.S. patent filing (or ~30 months for PCT)

### Methods that may be novel
- Receipt chain verification for policy enforcement
- Deterministic routing with explicit HOLD/ESCALATE
- Bounded kernel model for operator-gated execution
- Intake validation with schema-independent decisions

### Methods that are likely prior art
- General append-only ledgers
- Policy decision frameworks
- Schema validation pipelines

## Licensing decision framework

### Options on the table

| Option | License | Community | Risk |
|--------|---------|-----------|------|
| **A** | MIT | High; forking risk | Patent licensing |
| **B** | Apache 2.0 | High; trusted reuse | Patent licensing |
| **C** | Proprietary | Low; controlled growth | Market risk |
| **D** | Dual (MIT + Proprietary) | Medium; dual maintenance | Confusion |

## Public disclosure risk/benefit

### Benefits of public release NOW
✅ Establishes priority date for any future patents
✅ Builds academic credibility and citations
✅ Enables early community feedback and validation
✅ Demonstrates SKOS-derived principles in practice
✅ Separates LCOS (public) from SKOS (private) cleanly

### Risks of public release NOW
⚠️ Starts patent clock (12 months to file in U.S.)
⚠️ Enables others to implement/extend freely
⚠️ Precludes trade-secret protection for released code
⚠️ May complicate future proprietary licensing

---

## Timeline for decision

### Now (April 2026)
- Release LCOS-Core publicly
- Maintain `All rights reserved` placeholder license
- Document this IP position

### 90 days (July 2026)
- Assess community feedback and adoption
- Make patent decision (file? abandon?)
- Decide licensing strategy

### 180 days (October 2026)
- Finalize license (MIT? Apache? Proprietary?)
- Update LICENSE file
- Announce to community

---

## References

- [RELEASE_INTENT.md](./RELEASE_INTENT.md) — What is being released
- [PUBLIC_SCOPE.md](./PUBLIC_SCOPE.md) — Public surface definition
- [SKOS_TO_LCOS_DERIVATION_MAP.md](./SKOS_TO_LCOS_DERIVATION_MAP.md) — SKOS/LCOS separation
- [../LICENSE](../../LICENSE) — Current license statement
- [../CLAIMS.md](../../CLAIMS.md) — Claim safety policy

---

**Author:** IP Position Coordinator
**Date:** April 2026
**Status:** Pre-decision; awaiting organizational input
