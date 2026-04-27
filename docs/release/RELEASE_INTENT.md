# LCOS-Core Release Intent

**Status:** Public research-oriented substrate (pre-license decision)
**Date:** April 2026
**Scope:** Generic, generalized implementation of receipt-gated execution, deterministic routing, and bounded operator kernels

## What is being released

This public release contains:

1. **Generic, implementation-facing research code**
   - Receipt and audit core (append-only verification chains)
   - Governance and decision infrastructure (policy helpers, typed decisions)
   - Typed intake and validation pipeline example
   - Deterministic routing demo with explicit HOLD/ESCALATE behavior
   - Continuous state sketch (research placeholder)
   - Bounded kernel interfaces and mock implementations

2. **Executable examples and tests**
   - Minimal receipt chain demo
   - Governed intake walkthrough
   - Routing decision demo
   - Unit test suite for core components

3. **Implementation-facing documentation**
   - Concepts and design notes
   - Research hypotheses and open questions
   - Example walkthroughs with clear limitations

## What is NOT being released

This release **does not** include:

- Private organizational materials
- Internal symbolic vocabulary or proprietary naming
- Unreleased design methods or meta-architectures
- Employer work product or confidential sources
- Third-party licensed code without attribution

See [SKOS_TO_LCOS_DERIVATION_MAP.md](./SKOS_TO_LCOS_DERIVATION_MAP.md) for separation of public vs. private lineage.

## IP Posture (Pre-Decision)

**Current license:** `All rights reserved.` (placeholder)

This posture is maintained pending decisions on:

- Patent filing windows
- Source-available vs. open-source strategy
- Which core methods should remain private
- Public licensing model (MIT, Apache 2.0, proprietary, etc.)

**No public grants are implied or extended at this time.**

See [IP_POSITION.md](./IP_POSITION.md) for fuller context.

## How to cite this work

If you reference this repository in academic or public contexts:

- Cite the repository URL: `https://github.com/erynoregon-rgb/LCOS-Core`
- Reference specific commits or tags for reproducibility
- Respect the `All rights reserved` license status until a public license is declared

## Public disclosure acknowledgment

This repository constitutes a **public disclosure** of the contents contained within it.

This is intentional and supported by the IP strategy.
However, public disclosure does not grant copying, modification, or distribution rights absent an explicit license.

## Next steps

1. Finalize license decision (likely Q3 2026)
2. Declare patent filing status (if applicable)
3. Transition to selected public license or maintain proprietary status
4. Archive this document; reference `LICENSE` as source of truth

---

**Prepared for:** public-oriented research venue
**Audience:** academic/technical community, potential contributors
**Restrictions:** None beyond license terms (see LICENSE file)
