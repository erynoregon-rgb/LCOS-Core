# Typed Evidence Contracts Paper Package

This package is the LCOS-native public proof note. It is intentionally smaller
than the imported receipt-gated operator surface draft: the claim here is not a
full governance runtime, but a bounded executable proof that LCOS can distinguish
grounded from unsupported AI-assisted claim transitions.

## Files

- `paper.md` — short public proof note
- `claim_ledger.yaml` — claim safety classifications
- `evidence_map.md` — LCOS-local evidence references
- `worked_example.md` — adversarial and positive fixture walkthrough
- `review_response_matrix.md` — anticipated reviewer objections
- `venue_fit_matrix.md` — publication path and evidence gaps
- `publication_boundary_closeout.md` — bounded closeout receipt for the hardened export boundary slice

## Proof Pair

```text
unsupported draft -> contract violation -> HOLD -> no downstream admission
grounded draft -> contract satisfied -> accepted receipt -> downstream admission allowed
```

The package uses only LCOS-local evidence. Background lineage from SKOS is
described as context, not as proof for LCOS claims.
