# Pipeline Run — LCOS Typed Evidence Contracts paper

**Pipeline ID:** `lcos_typed_evidence_contracts_paper_a1`
**Pipeline type:** `research` (Block 4B of `GOVERNED_OUTPUT_PIPELINE_v1`)
**Operator:** local operator
**Started:** 2026-05-22 (paper draft produced as part of session)
**Closed:** 2026-05-23 (audit + run trace attached)

This file is the first real governed-output-pipeline run trace produced as
an artifact rather than only as conversation. Its purpose is to make the
pipeline's discipline empirically inspectable on a real case before the
script that automates it is built.

The pipeline did not run from a YAML driver. The steps were executed
manually, in order, with the gate applied at each step boundary. This trace
reconstructs the run from the artifacts it produced. Every cited file is
LCOS-local; no SKOS context is required to verify the trace.

---

## Context packet (Block 0)

```yaml
pipeline_id: lcos_typed_evidence_contracts_paper_a1
pipeline_type: research
target: LCOS-native public proof note replacing the SKOS-derived imported draft
operator: local operator

evidence_sources:
  primary:
    - type: repo
      location: /home/eryn/LCOS-Core/src/lcos_public
      admissible_claims:
        - typed contract loads from YAML
        - gate emits HOLD on contract violation
        - ledger appends receipts with hash-chain integrity
        - replay renders the receipt timeline
    - type: repo
      location: /home/eryn/LCOS-Core/fixtures/adversarial/ai_drafting_drift
      admissible_claims:
        - adversarial draft contains forbidden terms
        - expected HOLD record shape is declared
    - type: repo
      location: /home/eryn/LCOS-Core/fixtures/adversarial/grounded_accept
      admissible_claims:
        - grounded draft satisfies contract
        - expected ALLOW record shape is declared
    - type: test
      location: /home/eryn/LCOS-Core/tests/test_ai_drafting_drift_fixture.py
      admissible_claims:
        - the proof pair runs deterministically
        - the chain is verifiable end-to-end
  forbidden:
    - private SKOS internals
    - private-path references into the originating substrate
    - production deployment claims
    - unverifiable scale claims
    - AI-OS / AGI / generalized cognitive architecture framing

pipeline_constraints:
  forbidden_terms:
    - private substrate name
    - private implementation path
    - private inference path
    - private coordination path
    - AGI
    - AI OS
    - cognitive architecture
  required_framing:
    - LCOS public proof artifact
    - SKOS as private originating substrate
    - bounded inspectable claims
  max_deliverables_per_step: 1
  gate_required_before_handoff: true
  receipt_required_before_persistence: true

target_description: >
  Produce an LCOS-native paper that cites only LCOS-local files, demonstrates
  one unsupported draft blocked before admission and one grounded draft
  admitted with a replayable receipt, and explicitly disclaims private SKOS
  internals.
```

---

## Step S1 — claim_inventory

**Input:** context packet evidence_sources.primary
**Deliverable:** typed claim ledger with safety tags (VERIFIED / REPO_IMPLEMENTED / SPECIFIED / HYPOTHESIS / REMOVE)
**Stop after:** ledger committed; each tracked claim has an evidence_path

**Artifact:** `claim_ledger.yaml` (5 tracked claims at initial draft)

**Forbidden-evidence check applied:**
```
rg -n "<private-substrate-paths>" claim_ledger.yaml
→ zero matches
```

**S1 audit (S1 applied to its own output):** `claim_ledger_audit.md`

**Audit findings:**
- 5 tracked claims (L1–L5) — all paper sections cite at least one tracked claim
- 3 orphan claims surfaced (in paper.md, not in ledger):
  - P-1 (paper.md:20–21) — "polished unsupported claim is worse than awkward grounded claim" — should be HYPOTHESIS
  - M-4 (paper.md:43) — "HOLD is a first-class outcome, not an error" — should be SPECIFIED
  - R-2 (paper.md:97–98) — "cites only LCOS-local files and tests" — should be VERIFIED (grep is the test)
- 0 stale claims
- 1 untracked category: §5 non-claims — recommend adding `non_claims:` section

**Gate decision:** **ALLOW with conditions.** The paper is not blocked from
S2/S3/S4 use because orphans are additive. But L6/L7/L8 must be added to the
ledger before the paper's claim coverage is VERIFIED-complete.

**Receipt:**
```yaml
step_id: S1
gate_verdict: ALLOW_WITH_CONDITIONS
artifact_refs:
  - docs/papers/lcos_typed_evidence_contracts/claim_ledger.yaml
  - docs/papers/lcos_typed_evidence_contracts/claim_ledger_audit.md
evidence_used:
  - src/lcos_public/ledger.py
  - src/lcos_public/replay.py
  - fixtures/adversarial/ai_drafting_drift/
  - fixtures/adversarial/grounded_accept/
  - tests/test_ai_drafting_drift_fixture.py
follow_up_required:
  - add L6 (P-1) as HYPOTHESIS
  - add L7 (M-4) as SPECIFIED
  - add L8 (R-2) as VERIFIED
  - add non_claims section to ledger
receipt_id: lcos_typed_evidence_contracts_paper_a1_s1
```

---

## Step S2 — evidence_map

**Input:** S1 ledger (claims with safety tags)
**Locked until:** S1.gate == ALLOW (satisfied — ALLOW_WITH_CONDITIONS)
**Deliverable:** evidence_map linking each claim to a local artifact with citation
**Stop after:** evidence map produced

**Artifact:** `evidence_map.md`

**Gate decision:** **ALLOW.** Evidence map cites only LCOS-local paths; no
forbidden sources required. (Verified by forbidden-path grep over the paper
directory, which returns zero matches.)

**Receipt:**
```yaml
step_id: S2
gate_verdict: ALLOW
artifact_ref: docs/papers/lcos_typed_evidence_contracts/evidence_map.md
evidence_used: S1.tracked_claims with evidence_path
receipt_id: lcos_typed_evidence_contracts_paper_a1_s2
```

---

## Step S3 — paper_draft

**Input:** S1.VERIFIED + S1.REPO_IMPLEMENTED + S1.SPECIFIED claims (5 of 5
admissible after S1)
**Locked until:** S2.gate == ALLOW (satisfied)
**Deliverable:** paper draft citing only locally verified evidence
**Stop after:** §7 Next Evidence Needed

**Artifact:** `paper.md` (7 sections, ~110 lines)

**Gate checks applied:**
- forbidden-path grep over paper.md: zero matches ✓
- §5 non-claims declared ✓
- §6 SKOS-derived draft relation declared as positioning only ✓
- §7 future work scoped as "more fixtures, not broader claims" ✓

**Gate decision:** **ALLOW with the same conditions as S1.** Paper is admitted
to the run; the 3 orphan claims surfaced in the S1 audit do not block
admission because each is reframeable as an additive ledger entry (not a
removal of established claim).

**Receipt:**
```yaml
step_id: S3
gate_verdict: ALLOW_WITH_CONDITIONS
artifact_ref: docs/papers/lcos_typed_evidence_contracts/paper.md
evidence_used: S2.evidence_map
follow_up_required: same as S1 (L6/L7/L8 + non_claims section)
receipt_id: lcos_typed_evidence_contracts_paper_a1_s3
```

---

## Step S4 — review_response_matrix

**Input:** S3.paper
**Locked until:** S3.gate == ALLOW (satisfied)
**Deliverable:** anticipated reviewer objections + grounded responses
**Stop after:** matrix complete

**Artifact:** `review_response_matrix.md`

**Gate decision:** **ALLOW.** Matrix grounds each response in the paper or
the cited LCOS-local artifacts.

**Receipt:**
```yaml
step_id: S4
gate_verdict: ALLOW
artifact_ref: docs/papers/lcos_typed_evidence_contracts/review_response_matrix.md
evidence_used: S3.paper + cited LCOS-local artifacts
receipt_id: lcos_typed_evidence_contracts_paper_a1_s4
```

---

## Pipeline outcome (initial run, 2026-05-23 pre-close)

| Step | Verdict | Artifact | Receipt |
|---|---|---|---|
| S1 claim_inventory | ALLOW_WITH_CONDITIONS | claim_ledger.yaml + claim_ledger_audit.md | s1 |
| S2 evidence_map | ALLOW | evidence_map.md | s2 |
| S3 paper_draft | ALLOW_WITH_CONDITIONS | paper.md | s3 |
| S4 review_response_matrix | ALLOW | review_response_matrix.md | s4 |

## Closure pass (2026-05-23 post-close)

After the initial run, the four follow-up conditions surfaced by S1 were
addressed in a closure pass:

- L6 (P-1) added to `claim_ledger.yaml` as HYPOTHESIS
- L7 (M-4) added to `claim_ledger.yaml` as SPECIFIED
- L8 (R-2) added to `claim_ledger.yaml` as VERIFIED
- `non_claims:` section added to `claim_ledger.yaml` with 4 entries

Also resolved: the rule-encoding self-reference surfaced during the initial
run (forbidden-path strings appearing in receipt artifacts that document
the rule itself). The placeholder convention is now documented in
`docs/SKOS_LCOS_BOUNDARY.md` under "Rule encoding scope and placeholder
convention." The forbidden-path grep now returns zero matches across the
entire paper package — both evidence-bearing and receipt-bearing artifacts.

| Step | Final Verdict | Artifact | Closure note |
|---|---|---|---|
| S1 claim_inventory | **ALLOW** | claim_ledger.yaml + claim_ledger_audit.md | orphans closed |
| S2 evidence_map | ALLOW | evidence_map.md | unchanged |
| S3 paper_draft | **ALLOW** | paper.md | conditions resolved |
| S4 review_response_matrix | ALLOW | review_response_matrix.md | unchanged |

**Final pipeline conformance status:** VERIFIED_COMPLETE for the current
proof pair scope. All gates ALLOW, all follow-up conditions closed, the
rule encoding is consistent across artifact classes, and the test suite
passes (7 passed).

## What this trace proves

This trace is itself the first piece of evidence for the
`empirical_by_construction` framing: the pipeline ran on a real case, every
step boundary was gated, the audit caught orphan claims that informal review
would have missed, and the artifacts produced (paper + ledger + audit) are
inspectable from LCOS alone without any SKOS context.

The trace is not the gate. The gate was applied at each step. The trace is
the receipt.

## What this trace does not prove

- it does not prove the pipeline runs without an operator (mechanization is
  deferred)
- it does not prove the gate catches every drift mode (the audit only
  exercised orphan-claim detection)
- it does not prove the rulebook is calibrated for non-research deliverables
  (other pipeline types untested in this run)

Those concerns remain SPECIFIED until pipeline runs are produced for them.
