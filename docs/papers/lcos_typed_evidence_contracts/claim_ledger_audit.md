# Claim Ledger Audit — LCOS Typed Evidence Contracts paper

**Audit class:** S1 follow-up — verify that the typed claim ledger fully covers
the substantive claims actually made in `paper.md`. An orphan claim (in paper,
not in ledger) is an untracked admission — the exact failure mode the pipeline
discipline exists to catch. The audit is itself the gate applied to S1's own
output.

**Method:** read `paper.md` end-to-end, enumerate substantive claims per
section with line citations, cross-check against the 5 entries in
`claim_ledger.yaml`, flag orphans and stales.

---

## Paper claim enumeration

### §Abstract (paper.md:8–16)
- A-1: AI-assisted artifacts can become downstream operational state before
  claims are checked — **framing**, not LCOS claim
- A-2: LCOS demonstrates contract → check → HOLD-or-receipt mechanism
  (paper.md:11–14) — covered by L1 + L2 + L3
- A-3: the current proof is intentionally small (paper.md:14) — covered by L4
- A-4: one unsupported draft blocked, one grounded draft admitted with
  replayable receipt (paper.md:14–16) — covered by L1 + L2 + L3

### §1 Problem (paper.md:18–26)
- **P-1**: "A polished unsupported claim is worse than an awkward grounded
  claim." (paper.md:20–21) — **load-bearing thesis line**, not in ledger
- P-2: the problem is claim transition admissibility (paper.md:21–22) —
  framing/definition, not a verifiable LCOS claim
- P-3: LCOS treats the transition as a governance event (paper.md:24) —
  positioning, loosely covered by L4

### §2 LCOS Mechanism (paper.md:28–44)
- M-1: LCOS is the public artifact, SKOS is the private originating system
  (paper.md:30–31) — covered by L4
- M-2: LCOS claims must be locally inspectable without SKOS (paper.md:31–32)
  — covered by L4
- M-3: four-part mechanism (contract/draft/gate/ledger) (paper.md:36–41) —
  covered by L1 + L2 + L3
- **M-4**: "HOLD is a first-class outcome, not an error" (paper.md:43) —
  definitional claim, not in ledger

### §3 Worked Fixture (paper.md:46–65)
- F-1: adversarial branch uses public-facing contract forbidding private/
  inflated language — covered by L1
- F-2: draft violates contract; gate emits `HOLD_CONTRACT_VIOLATION`; no
  admission receipt (paper.md:52–53) — covered by L1
- F-3: positive branch uses same contract shape with grounded draft —
  covered by L2
- F-4: grounded draft → `EXECUTION_ACCEPTED` → replay verifies receipt chain
  (paper.md:64–65) — covered by L2 + L3

### §4 What This Proves (paper.md:67–77)
- W-1: LCOS distinguishes two transition attempts under one contract
  (paper.md:69–70) — covered by L1 + L2
- W-2: the unsupported→HOLD and grounded→accepted bullets (paper.md:72–74)
  — covered by L1 + L2
- W-3: stronger than rejection alone; small classifier over claim
  transition attempts (paper.md:76–77) — covered by L5 (HYPOTHESIS)

### §5 What This Does Not Prove (paper.md:79–90)
- §5 is the **non-claims declaration**. Not tracked as affirmative claims
  because each is an explicit negative limit. Pipeline note: non-claims are
  a separate concern from the ledger; they belong in a non_claims section if
  tracked at all.

### §6 Relation to SKOS-Derived Draft (paper.md:92–99)
- R-1: imported draft is broader background research (paper.md:94–96) —
  provenance claim, loosely covered by L4
- **R-2**: "This LCOS-native note is narrower. It cites only LCOS-local
  files and tests." (paper.md:97–98) — **mechanically verifiable**, not in
  ledger. The forbidden-path grep is the test.
- R-3: contribution is the public proof pair (paper.md:98–99) — covered by L4

### §7 Next Evidence Needed (paper.md:101–110)
- §7 is **future-looking**. Not tracked as current-state claims. No orphans.

---

## Audit findings

### Orphan claims (in paper, not in ledger): 3

| Orphan | Paper location | Suggested ledger entry |
|---|---|---|
| **P-1** "polished unsupported claim is worse than awkward grounded claim" | paper.md:20–21 | Add as L6 with `claim_safety_tag: HYPOTHESIS` — value judgment, not test-verifiable, but load-bearing for the paper's argument. |
| **M-4** "HOLD is a first-class outcome, not an error" | paper.md:43 | Add as L7 with `claim_safety_tag: SPECIFIED` — design property documented in the ledger schema (`hold_record` shape in `expected_hold.json`) and enforced by the gate, but framed here as a definition. |
| **R-2** "This LCOS-native note... cites only LCOS-local files and tests" | paper.md:97–98 | Add as L8 with `claim_safety_tag: VERIFIED` — mechanically verifiable by the forbidden-path grep over private-path placeholders (`rg -n "<private-substrate-paths>" docs/papers/lcos_typed_evidence_contracts/` returns zero matches). The grep is the test. |

### Stale claims (in ledger, not in paper): 0

All 5 ledger entries (L1–L5) appear in the paper at the section they cite.

### Untracked categories: 1

§5 (paper.md:79–90) declares non-claims — explicit limits on what the proof
does not show. Currently the ledger has no non-claims section. The pipeline
spec (Block 4C governance template) lists `non_claims` as a required output.
Recommend adding a `non_claims` section to `claim_ledger.yaml` for
completeness.

---

## Disposition

The paper is in good shape — 5 tracked claims plus 3 orphans, all of which
are addressable by adding ledger entries rather than removing paper content.
Two orphans are positioning/framing claims that benefit from being made
typed (P-1 as HYPOTHESIS, M-4 as SPECIFIED). One orphan (R-2) is
mechanically verifiable and should be added as VERIFIED.

**Recommended ledger updates** (not made by this audit; surfaced as gaps):

1. Add L6 (P-1) as HYPOTHESIS
2. Add L7 (M-4) as SPECIFIED
3. Add L8 (R-2) as VERIFIED, with the forbidden-path grep as the test_path
4. Add `non_claims:` section listing the §5 limits

After those updates, the summary would be: `verified: 4, repo_implemented: 0,
specified: 2, hypothesis: 2, remove: 0` — and the paper would be fully
covered by typed claims.

**This audit is itself an S1 output.** It exercises the typed-claim
discipline on S1's own deliverable. The pipeline doesn't trust an unaudited
claim ledger any more than it trusts an ungrounded paper claim.

**Initial audit verdict (2026-05-23, pre-close):** ALLOW with 3 orphan gaps
to close. The paper was not blocked from S2/S3/S4 use because the orphans
were additive (extend the ledger) rather than removing established claims.

## Closure (2026-05-23, post-close)

All three orphans have been closed in `claim_ledger.yaml`:

- **L6** (P-1, HYPOTHESIS) — present at `claim_ledger.yaml` line 52, citing
  paper.md as evidence_path.
- **L7** (M-4, SPECIFIED) — present at `claim_ledger.yaml` line 60, citing
  `expected_hold.json` as evidence_path and the drafting-drift test as
  `test_path`.
- **L8** (R-2, VERIFIED) — present at `claim_ledger.yaml` line 68, citing
  the paper package as evidence_path and the drafting-drift test as
  `test_path`.

The `non_claims:` section is also now present at `claim_ledger.yaml` lines
83–87, listing the four §5 limits from paper.md.

Updated summary (now matches the predicted counts above): `verified: 4,
repo_implemented: 0, specified: 2, hypothesis: 2, remove: 0` plus
`non_claims: 4`. Total tracked claims: 8.

The rule-encoding self-reference that this audit and `pipeline_run.md`
originally surfaced has been resolved by the placeholder convention now
documented in `docs/SKOS_LCOS_BOUNDARY.md` under "Rule encoding scope and
placeholder convention." The forbidden-path grep now returns zero matches
across the entire paper package — both evidence-bearing and receipt-bearing
artifacts.

**Final audit verdict:** ALLOW. The paper's claim coverage is
**VERIFIED-complete for the current proof pair scope**, and the rule
encoding is consistent across artifact classes.
