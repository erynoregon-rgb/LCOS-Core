# Review Response Matrix

**Paper:** Verifying Claims About AI Systems: A Receipt-Gated Operator Surface for Operationalising Governance  
**Purpose:** Preserve the review-driven cleanup logic behind the public draft.

---

## Positive Signal — Preserve

One reviewer noted that the fundamental contribution — receipt emission as part
of the operator surface, not post-hoc audit — is novel and significant enough
for publication after cleanup.

**Preservation rule:** keep this distinction sharp and stated once, clearly, in
the introduction. Later sections should use the claim, not re-announce it.

---

## Response Matrix

| # | Reviewer Criticism | Location in Paper | Revision Action | Status |
|---|---|---|---|---|
| R1 | **Repetition** — the same contribution was restated in nearly every section | Abstract, §1, §3, §4, §5, §6 | State the contribution once in the introduction; remove trailing restatements | Addressed |
| R2 | **Abstraction** — no concrete example with actual fields or records | Entire paper | Replace abstract flow prose with a concrete worked example using real field names | Addressed |
| R3 | **No worked example** — the original example section showed no record content | §3 | Show a request record, execution record, receipt, and reconstruction query | Addressed |
| R4 | **Underspecified data structures** — RequestRecord, ExecutionRecord, Receipt were named but not defined | §2 and §3 | Add a mechanism table and support note with field-level detail | Addressed |
| R5 | **Unclear use case** — the operator/reviewer was not clearly identified | §1, §3, §5 | Open with an AI coding agent claim and a human reviewer who distrusts narration | Addressed |
| R6 | **Insufficient adjacent work** — related work missed audit-log, compliance, provenance, and agentic-tooling context | §4 | Expand related work and add reviewer-named prior work | Addressed in the public draft surface |

---

## Revision Scope Boundaries

The public draft intentionally excludes:

- claims about full SKOS architecture
- performance metrics without a measurement bundle
- claims unsupported by `src/`, `tests/`, `schemas/`, or real receipts
- deployment or adversarial-hardening claims

---

## Claim Safety Rule

From `docs/papers/TAIGR_CLAIM_SAFETY_TABLE.md`:

> If a sentence cannot point to a repo file, a test, or a receipt, rewrite it as a hypothesis, not a result.

The public paper surface is packaged to make that rule inspectable through the
evidence map and claim ledger.
