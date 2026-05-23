---
title: Receipt-Gated Operator Surface
status: public_research_draft
version: "A2 snapshot"
updated: 2026-05-19
---

# Receipt-Gated Operator Surface

This directory is the stable public paper surface for the receipt-gated operator
surface manuscript family inside LCOS-Core.

The contents here should be read as a **research draft plus evidence bundle**,
not as final canonical truth and not as a claim about full SKOS deployment or
full LCOS production readiness.

## Public posture

This surface is intentionally bounded.

It describes a mechanism class packaged for public inspection in this
repository:

- request and result records
- runner receipts emitted on the execution path
- canonical receipt integrity primitives
- deterministic claim-to-receipt reconstruction
- evidence mapping and claim-safety tagging

It does **not** claim:

- production deployment
- adversarial hardening
- disclosure of private SKOS implementation details
- cryptographically signed transparency infrastructure
- general AI-system safety

## Package contents

| File | Role |
|---|---|
| `paper.md` | Public research-draft snapshot of the current paper text |
| `worked_example.md` | Concrete operator/reviewer scenario with request/result/receipt fields |
| `evidence_map.md` | Mechanism-to-repo evidence map with claim-safety tags |
| `claim_ledger.yaml` | Claim-by-claim safety ledger for the paper |
| `references.bib` | Public bibliography for the paper surface |
| `review_response_matrix.md` | Reviewer criticism to revision-action mapping |
| `publication_note.md` | Public-claims boundary for this package |
| `venue_fit_matrix.md` | Venue strategy for Paper A and Paper B |

## Provenance

This stable package was imported from the SKOS-Core paper workspace on the base
machine and mirrored here as the LCOS-Core public paper surface.

The LCOS package is the public inspection surface. It preserves the draft,
evidence bundle, and venue-planning artifacts without claiming that all cited
source paths are implemented inside LCOS-Core itself.

## Related surfaces

- `publication_note.md` — boundary note for this mirrored public draft
- `../../release/PUBLIC_SCOPE.md` — LCOS public-scope boundary
- `../../release/SKOS_TO_LCOS_BOUNDARY.md` — concept-sharing boundary between SKOS and LCOS
- `../../../PUBLIC_DISCLOSURE_NOTICE.md` — root disclosure posture for LCOS-Core
