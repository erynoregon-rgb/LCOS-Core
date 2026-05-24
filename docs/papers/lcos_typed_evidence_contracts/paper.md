# Typed Evidence Contracts for Blocking Unsupported AI-Assisted Claims

**Status:** public proof note  
**Snapshot:** LCOS-native proof pair  

---

## Abstract

AI-assisted artifacts can become downstream operational state before their
claims have been checked against evidence, scope, and authority constraints.
LCOS demonstrates a bounded alternative: a typed evidence contract is declared
before admission, the draft is checked against that contract, and the result is
recorded as either HOLD or accepted receipt. The current proof is intentionally
small. It shows one unsupported draft blocked before admission and one grounded
draft admitted with a replayable receipt.

## 1. Problem

The problem is not prose quality. A polished unsupported claim is worse than an
awkward grounded claim. The problem is claim transition admissibility: whether a
claim is allowed to move from generated text into downstream state.

LCOS treats that transition as a governance event. A draft may sound plausible,
but it should not be admitted unless it satisfies the contract declared for the
artifact.

## 2. LCOS Mechanism

LCOS is a public proof artifact. SKOS is the private originating system where
larger governance and runtime ideas are explored. LCOS claims must be locally
inspectable without SKOS.

The LCOS fixture mechanism has four parts:

| Part | LCOS-local evidence | Role |
|---|---|---|
| Typed contract | `fixtures/adversarial/*/contract.yaml` | Declares deliverable, source boundary, forbidden terms, and stop condition |
| Draft output | `fixtures/adversarial/*/*.txt` | Represents an AI-assisted artifact candidate |
| Gate result | `tests/test_ai_drafting_drift_fixture.py` | Classifies the draft as VALID or INVALID |
| Receipt ledger | `src/lcos_public/ledger.py`; `src/lcos_public/replay.py` | Records HOLD or accepted admission and renders a replayable timeline |

HOLD is a first-class outcome, not an error. It records why admission was
blocked and what must change before the draft can be retried.

## 3. Worked Fixture

The proof pair has two branches.

The adversarial branch uses a public-facing contract that forbids private or
inflated language. The draft violates the contract by using forbidden terms. The
gate emits `HOLD_CONTRACT_VIOLATION`, records failed constraints, and does not
append an accepted admission receipt.

The positive branch uses the same kind of contract with a grounded draft:

```text
LCOS demonstrates a bounded public proof for typed evidence contracts: an
AI-assisted draft is checked against declared terms before it can become
downstream state, and unsupported claims produce a HOLD instead of an accepted
receipt.
```

That draft satisfies the contract. The ledger records `EXECUTION_ACCEPTED`, and
the replay timeline verifies the receipt chain.

## 4. What This Proves

This proof shows that LCOS can distinguish two transition attempts under a
declared contract:

- unsupported draft -> contract violation -> HOLD -> no downstream admission
- grounded draft -> contract satisfied -> accepted receipt -> downstream
  admission allowed

That is stronger than proving rejection alone. Rejection is a filter. The proof
pair demonstrates a small classifier over claim transition attempts.

## 5. What This Does Not Prove

This does not prove semantic truth. It proves only that the checked constraints
were applied and recorded.

This does not prove production readiness, adversarial hardening, cryptographic
attestation, or general AI safety.

This does not prove prose quality. Style and polish are downstream concerns.
The mechanism addresses whether a claim may cross an admission boundary.

This does not disclose or require private SKOS internals.

## 6. Relation to the SKOS-Derived Receipt-Gated Operator Surface Draft

The imported receipt-gated operator surface draft is broader background
research. It discusses a larger operator surface and uses evidence from its
originating workspace.

This LCOS-native note is narrower. It cites only LCOS-local files and tests.
Its contribution is the public proof pair, not the broader private system.

## 7. Next Evidence Needed

The next evidence layer should add more fixtures, not broader claims:

- additional grounded accepts with different contract shapes
- adversarial drafts with unsupported scale or deployment claims
- measurement of false HOLD and false allow behavior under human review
- a small threat model for fixture tampering and public export safety

Until then, LCOS should remain a small, runnable, inspectable proof artifact.
