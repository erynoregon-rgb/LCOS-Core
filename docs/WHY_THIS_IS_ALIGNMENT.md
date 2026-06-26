# Why this is an alignment problem

One page. Read `CLAIMS.md` for the claim boundary; nothing here exceeds it.

## The problem

An AI agent finishes a task and reports what it did: *"I migrated the table and
verified it."* Downstream systems — and people — usually act on the **account**.
The account is the agent's own narration. When the narration is wrong, whether
from confabulation or from an unverifiable shortcut, the error is admitted before
anyone can catch it.

The failure has one shape: **inference substituted for verification.** A claim is
treated as true because it was asserted fluently, not because it can be
reconstructed from evidence.

## What LCOS-Core demonstrates

A reduced, runnable pattern where admission does not depend on the agent's
account:

- **inference proposes** — the agent submits a claim/request.
- **verification disposes** — a gate decides admission from typed rules and
  required evidence, not from how convincing the claim sounds.
- **the gate can return no** — if the required admission evidence is absent, the
  claim is *held*. No admission receipt is emitted, and execution does not run.

The "no" is the load-bearing output. A gate that can only say yes verifies
nothing.

## See it refuse a claim

```bash
python -m lcos_public.cli demo-no
echo $?
```

An agent asserts it did the work and points at evidence the public gate cannot
inspect. The gate refuses admission:

```text
admission_decision:   REJECT
admitted:             false
admission_receipt_id: null      # no admission → no authority to execute
execution_output:     null      # nothing ran
outcome:              held
exit code:            1          # the refusal, as a machine-checkable signal
```

This is a **structural** guarantee, not a logged observation after the fact: in
`src/lcos_public/execution.py`, if the admission receipt is absent the execution
output is `None` by construction. `tests/test_execution.py` proves there is no
path where execution ran without an admission receipt.

## Where to look

| Concern | File |
|---|---|
| Gate-first execution (the structural "no") | `src/lcos_public/execution.py` |
| Adversarial "no" demo | `python -m lcos_public.cli demo-no` |
| What each claim is backed by | `EVIDENCE_MAP.md` |
| What is and is not claimed | `CLAIMS.md`, `PROOF.md` |

## What this does and does not say

It **says**: unsupported AI-assisted claims can be held before downstream
execution when required admission evidence is absent, and you can verify that
property by cloning this repository and running the tests.

It **does not say**: that this prevents hallucination, proves general AI safety,
detects every unsupported claim, or implements the private SKOS substrate. Those
are out of scope for this package by design — see `CLAIMS.md`.

LCOS-Core demonstrates a mechanism *class*. The decisive internal strategy is not
published here.
