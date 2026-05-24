# LCOS Primitives

LCOS-Core exposes eight primitives. They are the public vocabulary the proof
kit operates in. The list is intentionally short — anything that cannot be
expressed as one of these primitives, or a direct composition of them,
belongs outside LCOS.

## 1. Contract

A declared rulebook that applies before any AI-assisted generation begins.
A contract names what the model may produce, which terms are forbidden,
which claims are permitted and forbidden, and what the gate does on
failure. The contract is fixed; the model may not modify it.

Fixture form: `fixtures/adversarial/ai_drafting_drift/contract.yaml`.

## 2. Claim

A verifiable assertion made by an AI-assisted artifact (a draft, a request,
an output). A claim must be grounded in evidence to be admissible. Claims
without supporting evidence are not admissible regardless of how plausible
they sound.

Code form: `lcos_public.claim`.

## 3. Evidence

The grounded source supporting a claim — a quoted file line, a repo
artifact, a referenced receipt, a primary source. Evidence is what makes
a claim verifiable without trusting the agent's account.

The boundary rule: a claim with no evidence may not enter downstream
operational state.

## 4. Decision

A typed verdict over a claim or request: ACCEPT, HOLD, REJECT, or
ESCALATE. Each decision must produce a visible reason and a list of
evidence items. There is no implicit decision; absence of a decision is
treated as HOLD.

Code form: `lcos_public.decision` (the `DecisionKind` literal).

## 5. Receipt

A tamper-aware append-only ledger entry. A receipt carries a sequence
number, an event type, a payload digest, a previous-receipt digest, and
a self-digest. The chain of receipts is verifiable — any tampered entry
breaks the chain in a way that `ledger.verify()` reports specifically.

Code form: `lcos_public.ledger.AppendOnlyLedger`, `lcos_public.receipt.Receipt`.

## 6. HOLD

A typed blocked-output state. A HOLD record carries a `hold_code`, the
list of failed constraints, the actor responsible for resolving it, and
the condition under which the deliverable may resume. A HOLD is not a
suggestion — the deliverable is not released until a corrected attempt
passes the gate.

Fixture form: `fixtures/adversarial/ai_drafting_drift/expected_hold.json`.

## 7. Replay

Deterministic rendering of the receipt timeline. Replay walks the ledger
in order, prints each receipt's identity and parent digest, and verifies
the chain. The replay output is the artifact a reviewer reads to
reconstruct what happened — including why a HOLD was emitted.

Code form: `lcos_public.replay.render_timeline`.

## 8. Export

A sanitizing boundary surface that produces a public-safe copy of source
artifacts while leaving the source intact. The export silently strips
declared redaction-marker lines, but it does not silently pass broader
boundary violations: forbidden content patterns, forbidden filename
fragments, symlinks, and invalid utf-8 text-suffix inputs produce typed
HOLD decisions with evidence. The walk is deterministic and skips known
non-public directories by default.

Code form: `lcos_public.publication.export_public_paper_surface`.

---

## What is NOT in this vocabulary

LCOS deliberately does not expose: agents, planners, orchestrators,
prompt templates, model routing, knowledge graphs, semantic layers,
runtime services, memory systems, cognitive architecture, or anything
else that would require importing the private SKOS substrate vocabulary.

Each of those concepts may exist elsewhere. None of them are LCOS
primitives. If a public proof claim requires one of them to be true,
that claim does not belong in LCOS — see `docs/SKOS_LCOS_BOUNDARY.md`.

## Composition

The primitives compose, but only into shapes that remain public-claimable:

```
contract + claim + evidence + decision + receipt
  -> if decision is ACCEPT: admit to ledger, replay shows admission
  -> if decision is HOLD:   block downstream state, replay shows reason
```

Anything more elaborate than that should be tested as a fixture before it
is treated as a working composition.
