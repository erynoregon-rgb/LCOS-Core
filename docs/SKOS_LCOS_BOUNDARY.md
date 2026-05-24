# SKOS / LCOS Boundary

LCOS-Core is the public proof kit. SKOS is the private research substrate.
This document defines what may cross the boundary and what may not.

## Architectural split

```
LCOS = public proof kit
SKOS = private substrate
```

LCOS may demonstrate principles that originate in SKOS, but must not depend
on SKOS internals to be understood, tested, or trusted. A reviewer who has
never seen SKOS must be able to clone LCOS, read it in roughly an hour, run
the tests, and verify every public claim from the artifact alone.

## Allowed claims (public-safe)

Claims LCOS may make from this repository:

- the toy ledger detects simple receipt-chain tampering in an append-oriented JSONL log
- the toy intake workbench produces typed ACCEPT / HOLD / REJECT / ESCALATE decisions
- the toy router is deterministic and returns a visible reason for each routing decision
- the toy replay tool renders a timeline from receipt JSONL
- a typed prompt-contract gate can block adversarial AI-assisted drafts before downstream admission
- public/private disclosure boundaries can be enforced by a sanitizing export surface
- the package demonstrates a class of governance mechanism, not a specific deployed system

## Forbidden claims (require SKOS context to be true)

Claims LCOS may NOT make from this repository alone:

- that LCOS implements the private SKOS system
- production routing quality from the toy router
- adversary-proof auditability or cryptographic immutability of the receipt ledger
- enterprise deployment, scale claims, or production reliability
- AGI relevance, generalized cognitive architecture, AI-operating-system framing
- patent coverage from this repository alone
- real operational validation from synthetic fixtures

These claims may or may not be defensible from SKOS evidence. They are not
defensible from LCOS evidence, which is what the public artifact must stand on.

## Influence ledger pattern

When LCOS demonstrates a principle that originated in SKOS, the influence
should be recorded explicitly so the boundary is auditable. Format:

```yaml
principle: <name of the underlying invariant or mechanism>
public_lcos_form: <how the principle is expressed in LCOS code/fixtures>
private_skos_origin: <where the principle was discovered or refined in SKOS>
public_claim_allowed: yes | no
requires_skos_internal_context: yes | no
```

`public_claim_allowed: yes` requires `requires_skos_internal_context: no`.
The two must be consistent — a claim that cannot stand without private
context is not a public claim.

### Example entries

```yaml
principle: receipt-gated decision provenance
public_lcos_form: contract + receipt + HOLD fixture (fixtures/adversarial/ai_drafting_drift/)
private_skos_origin: governed agent/runtime work in the private substrate
public_claim_allowed: yes
requires_skos_internal_context: no
```

```yaml
principle: typed evidence contracts block unsupported AI-assisted claims
public_lcos_form: ai_drafting_drift fixture + grounded_accept fixture + replay timeline
private_skos_origin: prompt-contract gate primitive, refined across multiple substrate experiments
public_claim_allowed: yes
requires_skos_internal_context: no
```

```yaml
principle: queue-centric public-boundary export gating
public_lcos_form: lcos_public.publication export emits typed HOLD decisions for forbidden content, symlinks, invalid utf-8 text inputs, and forbidden filename fragments while preserving strict source non-mutation
private_skos_origin: governed queue and gate-rectifier discipline refined in the SKOS control-plane and publication-boundary work
public_claim_allowed: yes
requires_skos_internal_context: no
```

```yaml
principle: governed multi-agent execution with mutation guards
public_lcos_form: NOT PUBLIC — no LCOS form exists
private_skos_origin: SKOS mutation_guard / hold_transition_registry / EXPERIMENT_GATE
public_claim_allowed: no
requires_skos_internal_context: yes
```

The third example illustrates a principle that is real in SKOS but does not
have a public form. LCOS may not make claims about it.

## How to add a new influence ledger entry

When a new fixture or primitive lands in LCOS and was influenced by SKOS work:

1. Write an entry in the format above.
2. Confirm `public_claim_allowed` and `requires_skos_internal_context` are
   consistent.
3. Append the entry to this file or a structured ledger file referenced
   from this file.
4. If a reviewer cannot verify the public form from LCOS alone, the entry
   must be marked `public_claim_allowed: no` regardless of how strong the
   SKOS evidence is.

## Rule encoding scope and placeholder convention

The forbidden-path rule is encoded mechanically as a grep over LCOS files for
private-substrate path strings. This encoding has a self-reference subtlety
that was surfaced empirically by the first real pipeline run trace
(`docs/papers/*/pipeline_run.md`): a receipt artifact that documents the rule
must be able to refer to the forbidden patterns without itself tripping the
rule.

The convention used in LCOS:

- **Evidence-bearing artifacts** — `paper.md`, `claim_ledger.yaml`,
  `evidence_map.md`, `worked_example.md`, `review_response_matrix.md`,
  `venue_fit_matrix.md`, and any paper-package `README.md` — contain the
  affirmative claims and must be free of the literal forbidden path
  strings. The grep applies in full strength here.

- **Receipt-bearing artifacts** — `claim_ledger_audit.md`, `pipeline_run.md`,
  and any future audit or run-trace files — document the rule and must
  refer to the forbidden patterns to be intelligible. Convention is to use
  placeholders (e.g., `<private-substrate-paths>`, "private substrate name",
  "private implementation path") in place of the literal strings.

The effect is that the same grep can be run unmodified across the entire
artifact set and return zero matches, regardless of artifact class. The
boundary holds without requiring scope-restricted variants of the rule.

This is an empirical finding from running the pipeline on its own first
case — the receipt artifact for the first real run had to describe a rule
that its own contents would have violated under naive encoding. The
placeholder convention resolves the tension without weakening the rule.

## What to do if a public claim drifts

If LCOS source or documentation starts implying claims that require SKOS
context — for example, "this implements a generalized agent runtime" — the
correct response is:

- treat the drifted claim as an `HOLD_CONTRACT_VIOLATION` against the
  LCOS public-claim boundary
- restore the bounded language from the allowed-claims list above
- if the drifted claim is in fact provable from LCOS, add it to the
  allowed-claims list with the verifying fixture cited

Doing this through receipts and fixtures, rather than through informal
revision, keeps the boundary itself auditable.
