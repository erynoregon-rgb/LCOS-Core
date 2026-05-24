# Publication Boundary Closeout

status: COMPLETE
claim_safety_tag: VERIFIED
scope: hardened LCOS public export boundary
owner: local operator

## Surfaces changed

- `src/lcos_public/publication.py`
- `src/lcos_public/cli.py`
- `tests/test_public_boundary.py`
- `tests/test_export_public_safety.py`
- `tests/test_publication_export.py`
- `docs/papers/lcos_typed_evidence_contracts/evidence_map.md`
- `docs/LCOS_PRIMITIVES.md`
- `docs/SKOS_LCOS_BOUNDARY.md`

## What closed

- redaction markers are stripped silently
- forbidden substrate content patterns produce typed `HOLD` decisions with evidence
- symlinks are never followed and always hold
- known non-public directories are skipped deterministically
- invalid utf-8 text-suffix files hold instead of exporting garbage
- forbidden filename fragments hold
- strict mode raises `PublicationBoundaryViolation`
- collect mode returns holds in the result surface
- CLI emits structured `HOLD` JSON on blocked export and `OK` JSON on clean export

## Evidence

- `tests/test_public_boundary.py`
- `tests/test_export_public_safety.py`
- `tests/test_publication_export.py`

## Verification

```text
95/95 tests pass in the LCOS suite
clean export smoke: status=OK, file exported
dirty export smoke: status=HOLD, evidence emitted, file not exported
```

## Non-claims

- this does not claim cryptographic immutability
- this does not claim production deployment safety
- this does not claim the broader SKOS control plane is public in LCOS
- this does not claim global repo mutation interception

## Boundary note

This closeout records a public LCOS form of a queue-centric gate pattern:
producer-side export attempts may propose output, but forbidden content does not
cross the public boundary. The public claim is the LCOS-local boundary behavior,
not the private SKOS runtime that informed it.
