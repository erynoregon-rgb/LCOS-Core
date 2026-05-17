# Worked Example: Receipt Replay and Tamper Detection

This walkthrough shows the complete path from request to receipt chain to replay,
including what happens under tamper conditions.

---

## 1. Start: a governed request

A `RequestRecord` captures what was requested before any execution begins.

```python
from lcos_toy.execution import RequestRecord, GoverningExecutor

request = RequestRecord.create(
    request_id="req-demo-001",
    actor="demo-agent",
    action="summarize",
    content="audit the receipt ledger",
    timestamp="2026-01-01T09:00:00+00:00",
)
```

## 2. Gate-first admission

`GoverningExecutor` runs intake validation before execution. The admission
receipt is emitted first. If the gate denies, execution does not proceed.

```python
executor = GoverningExecutor(actor="demo-executor")
record = executor.execute(request, timestamp="2026-01-01T09:00:01+00:00")
```

For an accepted request:

```
record.admitted          → True
record.admission_receipt → TransitionReceipt(from_state=OPEN, to_state=ACTIVE, ...)
record.execution_output  → "[executed] summarize: audit the receipt ledger"
record.outcome           → "accepted"
```

For a request with a blocked term (e.g. "credential"):

```
record.admitted          → False
record.admission_receipt → None
record.hold_receipt      → TransitionReceipt(from_state=OPEN, to_state=HELD, ...)
record.execution_output  → None
record.outcome           → "held"
```

The absence of `admission_receipt` is structural proof that execution did not
run — not a logged observation added afterward.

## 3. The receipt chain

Every claim produces an ordered chain of `TransitionReceipt`s.

```python
chain = record.chain

chain.claim_id      # "req-demo-001"
chain.length        # 2 (OPEN→ACTIVE, ACTIVE→COMPLETE)
chain.outcome       # "accepted"
chain.recovery_id   # sha256 of the serialized chain — deterministic
```

**C4 property:** Same `claim_id` + same ordered receipts → same `recovery_id`.
Reconstruction is deterministic. Any agent with the receipt sequence can verify
the chain without access to the original execution environment.

```python
# Rebuild from raw dicts — recovery_id must match
from lcos_toy.claim import TransitionReceipt
from lcos_toy.chain import ClaimReceiptChain

rebuilt_receipts = [TransitionReceipt(**r) for r in chain_dict["receipts"]]
rebuilt_chain = ClaimReceiptChain.build("req-demo-001", rebuilt_receipts)

assert rebuilt_chain.recovery_id == chain.recovery_id  # always true
```

## 4. The append-only ledger

Receipts can be persisted to an append-only JSONL ledger for audit replay.

```python
from lcos_toy.ledger import AppendOnlyLedger
import tempfile, pathlib

with tempfile.TemporaryDirectory() as tmp:
    path = pathlib.Path(tmp) / "demo.jsonl"
    ledger = AppendOnlyLedger(path)

    # Append events from the execution
    ledger.append("INTAKE",    request.to_dict(),                   timestamp="2026-01-01T09:00:00+00:00")
    ledger.append("ADMISSION", record.admission_receipt.to_dict(), timestamp="2026-01-01T09:00:01+00:00")
    ledger.append("COMPLETE",  record.chain.to_dict(),             timestamp="2026-01-01T09:00:02+00:00")

    report = ledger.verify()
    # report.valid  → True
    # report.count  → 3
```

## 5. Replay timeline

```python
from lcos_toy.replay import render_timeline

print(render_timeline(path))
```

Output:

```
seq | event_type | digest_prefix | parent_prefix
1 | INTAKE    | a3f9c1d2e4b5 | ROOT
2 | ADMISSION | 7b2e4d9f1c3a | a3f9c1d2e4b5
3 | COMPLETE  | 2d5f8a1b4c7e | 7b2e4d9f1c3a
valid=true count=3 issues=0
```

## 6. Tamper detection

If any payload is modified after appending, verification detects it.

```python
# Tamper: overwrite a payload field
import json
lines = path.read_text().splitlines()
record_dict = json.loads(lines[0])
record_dict["payload"]["actor"] = "attacker"
lines[0] = json.dumps(record_dict)
path.write_text("\n".join(lines) + "\n")

report = ledger.verify()
# report.valid         → False
# report.issues[0].code → "PAYLOAD_TAMPERED"
# report.issues[0].seq  → 1
```

The ledger does not prevent writes — it detects inconsistency at read time.
It is tamper-aware, not tamper-proof.

## 7. Receipt ID content-addressing

`TransitionReceipt.receipt_id` is derived from the body before timestamp:

```python
# Same claim body → same receipt_id regardless of when it is created
r1 = TransitionReceipt.create(
    claim_id="req-demo-001", actor="demo-executor",
    from_state=ClaimState.OPEN, to_state=ClaimState.ACTIVE,
    reason="intake decision: request is admissible in toy scope",
    timestamp="2026-01-01T09:00:01+00:00",
)
r2 = TransitionReceipt.create(
    claim_id="req-demo-001", actor="demo-executor",
    from_state=ClaimState.OPEN, to_state=ClaimState.ACTIVE,
    reason="intake decision: request is admissible in toy scope",
    timestamp="2099-12-31T23:59:59+00:00",  # different timestamp
)

assert r1.receipt_id == r2.receipt_id  # always true
```

This makes receipt chains reconstructible from content alone, independent of
wall-clock time.

---

## Claim boundary

This worked example uses toy data and a toy executor. It demonstrates the
mechanism class. It does not claim:

- production-grade adversary resistance
- OS-enforced immutability
- cryptographic signing
- real operational trace behavior

See [`CLAIMS.md`](../../CLAIMS.md) and [`docs/release/PUBLIC_DISCLOSURE_NOTICE.md`](../release/PUBLIC_DISCLOSURE_NOTICE.md).
