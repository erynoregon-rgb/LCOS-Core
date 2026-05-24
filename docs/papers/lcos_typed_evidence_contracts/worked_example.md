# Worked Example

The LCOS proof note uses one adversarial fixture and one positive fixture.

## Shared Contract Shape

```yaml
mode: draft
deliverable: one-paragraph research agenda statement
claim_source: LCOS-Core repository (public)
forbidden_terms:
  - AI OS
  - substrate
  - private repository name
stop_after: end of first paragraph
```

## Branch A: Unsupported Draft

The adversarial draft uses forbidden public framing. The gate detects forbidden
terms and returns:

```json
{
  "hold_code": "HOLD_CONTRACT_VIOLATION",
  "deliverable_blocked": true,
  "failed_constraints": ["forbidden_terms_absent"],
  "forbidden_terms_found": ["AI OS", "substrate"],
  "next_actor": "user",
  "resume_condition": "corrected deliverable passes gate",
  "nothing_promoted": true
}
```

The ledger records `CONTRACT_HOLD` and does not record
`EXECUTION_ACCEPTED`.

## Branch B: Grounded Draft

The grounded draft stays inside the public LCOS claim boundary:

```text
LCOS demonstrates a bounded public proof for typed evidence contracts: an
AI-assisted draft is checked against declared terms before it can become
downstream state, and unsupported claims produce a HOLD instead of an accepted
receipt.
```

The gate returns `VALID`, the ledger records `EXECUTION_ACCEPTED`, and replay
renders a valid timeline.

## Interpretation

The pair proves distinction, not general truth. LCOS can reject one unsupported
transition attempt and admit one grounded transition attempt under a declared
contract.
