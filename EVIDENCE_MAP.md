# Evidence Map

What is implemented, where to find it, and what the tests prove.

All claims are limited to the contents of this repository.
This is a toy demonstration package — see CLAIMS.md for the full boundary.

---

## Receipt chain

**Claim:** The ledger is append-oriented and detects payload tampering.

| | |
|---|---|
| Implementation | `src/lcos_toy/receipt.py`, `src/lcos_toy/ledger.py` |
| Tests | `tests/test_ledger.py` |
| CLI demo | `python -m lcos_toy.cli demo-ledger` |

What the tests prove:
- Valid chain verifies (`test_append_only_chain_verifies`)
- Payload tamper produces `PAYLOAD_TAMPERED` issue (`test_payload_tamper_is_detected`)
- Missing ledger fails in strict mode (`test_missing_ledger_can_fail_in_strict_mode`)
- Malformed JSON returns structured issue (`test_malformed_json_returns_structured_issue`)

---

## Typed decision states

**Claim:** Decisions are typed (`ACCEPT / HOLD / REJECT / ESCALATE`), not free strings.

| | |
|---|---|
| Implementation | `src/lcos_toy/decision.py`, `src/lcos_toy/intake.py` |
| Tests | `tests/test_intake.py` |
| CLI demo | `python -m lcos_toy.cli demo-intake examples/requests/simple_accept.json` |

What the tests prove:
- Valid requests accept
- Blocked terms reject
- Ambiguous requests hold
- Out-of-scope requests escalate

---

## Deterministic routing

**Claim:** The router is deterministic — same input, same routing decision, visible reasons.

| | |
|---|---|
| Implementation | `src/lcos_toy/router.py` |
| Tests | `tests/test_router.py` |
| CLI demo | `python -m lcos_toy.cli demo-route "summarize this receipt"` |

What the tests prove:
- Router is deterministic across calls
- Unknown requests escalate
- Unmatched requests hold

---

## Claim state machine

**Claim:** Claims follow a governed four-state lifecycle with transition receipts at each step.

| | |
|---|---|
| Implementation | `src/lcos_toy/claim.py` |
| Tests | `tests/test_claim.py` |

States: `OPEN → ACTIVE → HELD | COMPLETE`

Legal transitions:
- `OPEN → ACTIVE` (activation)
- `OPEN → HELD` (gate denial before activation)
- `ACTIVE → HELD` (blocked mid-execution)
- `ACTIVE → COMPLETE` (normal completion)
- `HELD → ACTIVE` (resume)
- `HELD → COMPLETE` (close from hold)

What the tests prove:
- All legal transitions succeed
- Illegal transitions raise `ValueError`
- Receipts accumulate in order
- `TransitionReceipt.receipt_id` is content-addressed: same body → same ID, regardless of timestamp

---

## Claim receipt chain

**Claim:** Same ordered receipts for the same claim → same `recovery_id` (deterministic reconstruction).

| | |
|---|---|
| Implementation | `src/lcos_toy/chain.py` |
| Tests | `tests/test_chain.py` |

What the tests prove:
- Same inputs produce same `recovery_id`
- Different outcomes produce different `recovery_id`
- `recovery_id` is a 64-char hex SHA256
- Mismatched claim IDs in receipt list raise `ValueError`

---

## Gate-first execution

**Claim:** The admission receipt must exist before execution proceeds. If the gate
denies admission, `execution_output` is `None` and a HOLD receipt is emitted instead.
This is a structural guarantee, not a logged observation after the fact.

| | |
|---|---|
| Implementation | `src/lcos_toy/execution.py` |
| Tests | `tests/test_execution.py` |

What the tests prove:
- Accepted requests have `admission_receipt` and `execution_output`
- Denied requests have `hold_receipt`, `admission_receipt=None`, `execution_output=None`
- Gate is structural: if `admission_receipt is None` then `execution_output is None` (always)
- Admission receipt ID is content-addressed

---

## Replay / timeline

**Claim:** A receipt ledger can be replayed to produce an audit timeline.

| | |
|---|---|
| Implementation | `src/lcos_toy/replay.py` |
| Tests | `tests/test_replay.py` |
| CLI demo | `python -m lcos_toy.cli replay <path-to-ledger.jsonl>` |

---

## Schemas

| Schema | File |
|---|---|
| Receipt | `schemas/receipt.schema.json` |
| Intake request | `schemas/intake_request.schema.json` |
| Routing decision | `schemas/routing_decision.schema.json` |

---

## Adversarial fixtures

`fixtures/adversarial/` contains malformed, ambiguous, out-of-scope, and
private-trace requests. Each should produce a non-ACCEPT decision from
`GovernedIntake`.
