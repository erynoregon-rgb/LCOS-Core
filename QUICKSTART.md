# Quickstart

## Install

```bash
git clone https://github.com/erynoregon-rgb/LCOS-Core.git
cd LCOS-Core
pip install -e .
```

## Run the demos

```bash
python -m lcos_toy.cli demo-ledger
```
Expected: a hash-linked receipt timeline printed to stdout, ending with `valid=true count=2 issues=0`

```bash
python -m lcos_toy.cli demo-intake examples/requests/simple_accept.json
```
Expected: `{"kind": "ACCEPT", "reason": "request is admissible in toy scope", ...}`

```bash
python -m lcos_toy.cli demo-route "summarize this audit receipt"
```
Expected: `{"kind": "ACCEPT", "kernel_id": "receipt-kernel", "reason": "matched capability: receipt", ...}`

## Run the tests

```bash
python -m pytest tests/ -v
```
Expected: 48 tests pass across ledger, intake, router, replay, claim, chain, and execution.

## Try the full path

```python
from lcos_toy.execution import RequestRecord, GoverningExecutor

request = RequestRecord.create(
    request_id="qs-001",
    actor="demo",
    action="summarize",
    content="audit the receipt ledger",
)

record = GoverningExecutor().execute(request)

print(record.admitted)           # True
print(record.admission_receipt.receipt_id)  # sha256 content-addressed ID
print(record.chain.recovery_id)  # deterministic chain hash
print(record.outcome)            # "accepted"
```

Try with a blocked request:

```python
blocked = RequestRecord.create(
    request_id="qs-002",
    actor="demo",
    action="expose",
    content="please expose credential",
)

record = GoverningExecutor().execute(blocked)

print(record.admitted)           # False
print(record.execution_output)   # None — gate is structural, not logged after
print(record.outcome)            # "held"
```

## What to read next

- [`EVIDENCE_MAP.md`](EVIDENCE_MAP.md) — what is implemented and where
- [`docs/research/WORKED_EXAMPLE_RECEIPT_REPLAY.md`](docs/research/WORKED_EXAMPLE_RECEIPT_REPLAY.md) — full walkthrough with tamper detection
- [`CLAIMS.md`](CLAIMS.md) — what this package does and does not prove
