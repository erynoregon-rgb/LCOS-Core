# Public Prospectus

## What this is

LCOS-Core is a bounded public demonstration of receipt-gated AI governance
primitives. It is the public layer of a larger private research program.

The private substrate contains the full implementation depth. This package
shows the mechanism class — enough to evaluate the engineering discipline,
the claim-safety posture, and the governance design.

## What it demonstrates

**Receipt-gated execution.** Every admission decision emits a receipt before
execution proceeds. If the gate denies admission, execution does not run and
no output is produced. The absence of an admission receipt is structural
proof execution did not happen — not a logged observation added afterward.

**Append-oriented audit trail.** Receipts are written to an append-only JSONL
ledger. The ledger is hash-chained: each entry links to its predecessor.
Payload tampering is detectable at replay time.

**Claim lifecycle.** A claim progresses through governed states:
`OPEN → ACTIVE → HELD | COMPLETE`. A `TransitionReceipt` is emitted at each
state transition. Receipt IDs are content-addressed: same inputs produce the
same receipt ID regardless of when it is created.

**Deterministic reconstruction.** A `ClaimReceiptChain` with a given
`claim_id` and ordered receipts always produces the same `recovery_id`.
Any agent with the receipt sequence can verify and reconstruct the chain
without access to the original execution environment.

**Typed decisions.** Decisions carry explicit kinds (`ACCEPT / HOLD / REJECT /
ESCALATE`) and visible reasons. No free-form string outcomes.

## What it does not expose

- Private implementation depth or routing tactics
- Full semantic-git machinery
- Raw workboard or workflow internals
- Real operational traces or private receipts
- Production configuration or private model routing
- The decisive substrate that gives this research its edge

## Audience

This package is designed for:

- Technical reviewers evaluating AI governance engineering
- Fellowship, grant, and research-facing evaluation
- Hiring signals in AI safety, reliability, and agentic systems
- Open-source community reference on receipt-gated governance patterns

## Research connection

The mechanisms demonstrated here — receipt emission at operator boundaries,
append-only audit trails, typed hold states, and deterministic chain
reconstruction — appear as governance primitives in research on auditable
agentic systems. The private substrate extends these into a full governed
runtime. LCOS shows the proof of mechanism; SKOS retains the proof of scale.

## Claim boundary

All implementation claims are limited to the contents of this repository.
See [`CLAIMS.md`](CLAIMS.md) and [`EVIDENCE_MAP.md`](EVIDENCE_MAP.md).
