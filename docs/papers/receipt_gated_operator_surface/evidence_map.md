# Evidence Map

**Paper:** Receipt-Gated Operator Surface  
**Purpose:** Map mechanism claims to public repository evidence and claim-safety
tags.

Claim-safety tags follow `docs/papers/TAIGR_CLAIM_SAFETY_TABLE.md`:

- **VERIFIED** — backed by code plus passing tests confirmed in the review pass
- **REPO_IMPLEMENTED** — code exists; implementation confirmed by reading source
- **SPECIFIED** — design or contract artifact only
- **HYPOTHESIS** — interpretation or motivation, not an implementation result

---

## Mechanism Evidence Map

| Mechanism Component | Repo Path | Evidence Type | Claim Safety Tag | Test Path | What the Test Proves | Notes |
|---|---|---|---|---|---|---|
| **Receipt emission — advisory runner** | `tools/inference/tui_advisory_runner.py` | Code: `_append_runner_receipt()`, appends JSONL to `var/coordination/inference/receipts/tui_advisory_runner_receipts.jsonl` | REPO_IMPLEMENTED | `tests/inference/test_tui_advisory_runner.py` | Runner emits a receipt record with `receipt_id`, `receipt_kind`, `action`, `lane`, `payload` after every execution, including held executions | Receipt is emitted on HOLD paths too, not only on success. Receipt ID format: `TUI-ADV-<millis>`. |
| **Receipt emission — governed commit** | `tools/gitops/governed_commit.py` | Code: `finalize_verdict()` → `verdict.receipt_path`; real receipts in `var/coordination/gitops/receipts/` | REPO_IMPLEMENTED | `tests/governance/test_receipt_first_model.py` | Governed commit emits a JSON receipt for ALLOW, HOLD, and COMMIT verdicts | Real HOLD receipt inspected in repo. |
| **Append-only store — ReceiptStore** | `src/skos_core/governance/receipt_store.py` | Code: `save_receipt()` uses `open(path, "a")`; `validate_all()` detects duplicate `receipt_id` | VERIFIED | `tests/governance/test_receipt_first_model.py::TestReceiptStore::test_append_only_validation`, `test_receipt_immutability` | Duplicate IDs are detected and append-only behavior is enforced | 32 tests passed in the revision pass. |
| **Hash-chained receipt ledger — ReceiptChain** | `src/skos_core/runtime/receipt_kernel.py` | Code: `ReceiptChain.append()` computes `chain_hash(previous_hash, entry_json)`; `verify_integrity()` walks the full chain | REPO_IMPLEMENTED | No dedicated test file found in the revision pass | Tampering with any entry produces a chain mismatch | Applies to the canonical receipt layer. |
| **Canonical receipt content-addressing** | `src/skos_core/runtime/receipt_kernel.py` | Code: `canonical_hash(obj)` and `make_canonical_receipt()` derive `receipt_id` from the body before timestamp | REPO_IMPLEMENTED | See above | Same inputs imply same canonical `receipt_id` | Scope this claim to the canonical layer only; the advisory runner uses `TUI-ADV-<millis>`. |
| **Reconstruction query — ClaimReceiptChain** | `src/skos_core/audit/reader.py` | Code: `build_claim_receipt_chain(claim_id)` returns `claim_step`, `receipt_steps`, `acceptance_step`, `outcome`, `recovery_id` | VERIFIED | `tests/audit/test_reader.py` | Reconstruction is deterministic for the same `claim_id` and `repo_root` | `recovery_id` is independently verifiable. |
| **Hold/refusal recording — semantic hold router** | `tools/gitops/semantic_hold_router.py` | Typed hold-code routing and schema-validated responses | REPO_IMPLEMENTED | No dedicated test file found in the revision pass | HOLD decisions are typed rather than silently dropped | Important for refusal accountability. |
| **Hold/refusal recording — governed commit** | `tools/gitops/governed_commit.py` | Code plus real receipts in `var/coordination/gitops/receipts/` | VERIFIED | `tests/governance/test_receipt_first_model.py` | HOLD receipts are recorded with typed codes | Real HOLD receipt with `HOLD_COMMIT_MESSAGE_INVALID` confirmed. |
| **Request record — TUI advisory schema** | `schemas/inference/tui_advisory_request.v1.schema.json` | JSON Schema with bounded fields and required request metadata | REPO_IMPLEMENTED | `tests/inference/test_tui_advisory_runner.py` | Missing required fields are rejected | `additionalProperties: false`. |
| **Execution record — advisory result schema** | `schemas/inference/tui_advisory_result.v1.schema.json` | JSON Schema for bounded result envelopes | REPO_IMPLEMENTED | `tests/inference/test_tui_advisory_runner.py` | Result envelope is validated before being written | `receipt_ref` is nullable until sealing. |
| **Provenance gate — advisory runner prechecks** | `tools/inference/tui_advisory_runner.py` | `_evaluate_prechecks()` enforces admissible profiles and prior admission receipts | REPO_IMPLEMENTED | `tests/inference/test_tui_advisory_runner.py` | Missing or non-ALLOW admission receipts produce HOLD codes | The gate is structural, not a sidecar logger. |
| **Governed intake** | `src/skos_core/intake/governed_acquisition.py` | Intake receipts emitted per artifact and queryable via audit reader | VERIFIED | `tests/intake/test_governed_acquisition.py` | Intake receipts are append-only and queryable | Provides intake-side baseline evidence. |

---

## Summary

| Claim Safety Tag | Count | Components |
|---|---|---|
| VERIFIED | 4 | append-only store, reconstruction query, governed commit HOLD receipts, governed intake |
| REPO_IMPLEMENTED | 9 | runner receipt emission, canonical receipt primitives, hold router, request/result schemas, provenance gate, related execution surfaces |
| SPECIFIED | 0 | — |
| HYPOTHESIS | 0 | — |
| BLOCKED/MISSING | 1 | dedicated tests for canonical `ReceiptChain` integrity were not found in the revision pass |
