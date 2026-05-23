# LCOS-Core Paper Surface

This directory contains bounded public paper artifacts mirrored into LCOS-Core.

These documents should be read as **research drafts and evidence bundles**, not
as final canonical truth and not as claims about non-public SKOS
implementation.

## Public paper packages

- [Receipt-Gated Operator Surface](receipt_gated_operator_surface/README.md) —
  public draft, worked example, evidence map, claim ledger, publication note,
  and venue-fit matrix

## Public export

Use the packaging command to produce a sanitized public export without editing
the source draft in place:

```bash
python -m lcos_public.cli export-paper docs/papers/receipt_gated_operator_surface build/public_papers/receipt_gated_operator_surface
```

## Boundary references

- [`../release/PUBLIC_SCOPE.md`](../release/PUBLIC_SCOPE.md)
- [`../release/SKOS_TO_LCOS_BOUNDARY.md`](../release/SKOS_TO_LCOS_BOUNDARY.md)
- [`../../PUBLIC_DISCLOSURE_NOTICE.md`](../../PUBLIC_DISCLOSURE_NOTICE.md)
