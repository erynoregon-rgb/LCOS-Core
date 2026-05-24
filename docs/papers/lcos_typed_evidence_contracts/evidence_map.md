# Evidence Map

**Paper:** Typed Evidence Contracts for Blocking Unsupported AI-Assisted Claims

This evidence map uses LCOS-local files only. Background SKOS lineage is not
treated as proof for LCOS claims.

| Mechanism Component | LCOS Path | Evidence Type | Claim Safety Tag | Test Path | What the Test Proves |
|---|---|---|---|---|---|
| Adversarial contract | `fixtures/adversarial/ai_drafting_drift/contract.yaml` | Fixture contract | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | Contract loads with declared fields and forbidden terms |
| Adversarial draft | `fixtures/adversarial/ai_drafting_drift/adversarial_output.txt` | Fixture draft | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | Forbidden terms are detected |
| Expected HOLD | `fixtures/adversarial/ai_drafting_drift/expected_hold.json` | Expected outcome | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | HOLD record shape matches expectation |
| Grounded contract | `fixtures/adversarial/grounded_accept/contract.yaml` | Fixture contract | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | Contract admits grounded draft |
| Grounded draft | `fixtures/adversarial/grounded_accept/grounded_output.txt` | Fixture draft | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | Draft avoids forbidden terms and receives accepted receipt |
| Expected accept | `fixtures/adversarial/grounded_accept/expected_accept.json` | Expected outcome | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | Accepted event is recorded with receipt |
| Append-only ledger | `src/lcos_public/ledger.py` | Implementation | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | HOLD and accepted paths produce verifiable ledger records |
| Replay timeline | `src/lcos_public/replay.py` | Implementation | VERIFIED | `tests/test_ai_drafting_drift_fixture.py` | Replay shows event sequence and ledger validity |
| Public export | `src/lcos_public/publication.py` | Implementation | VERIFIED | `tests/test_publication_export.py`, `tests/test_public_boundary.py`, `tests/test_export_public_safety.py` | Public export sanitizes redaction-marker lines, skips non-public directories deterministically, holds forbidden filenames/content/symlinks/non-utf-8 text inputs, and never mutates the source tree |

## Blocked Claims

No LCOS-native claim in this package may cite private implementation paths as
evidence. Broader runtime claims belong in the imported receipt-gated operator
surface draft or future SKOS-derived background notes.
