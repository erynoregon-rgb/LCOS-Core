# Worked Example

**Paper:** Receipt-Gated Operator Surface  
**Purpose:** Concrete operator/reviewer scenario with real field names and a
runner-receipt-centered example.

Field names throughout are drawn directly from:

- `schemas/inference/tui_advisory_request.v1.schema.json`
- `schemas/inference/tui_advisory_result.v1.schema.json`
- `src/skos_core/runtime/receipt_kernel.py::CanonicalReceipt`
- real receipt material under `var/coordination/gitops/receipts/`

---

## Scenario

An AI coding agent operating in a repository asserts: "I validated the change
at commit `a3f891b` against governance policy and the result was ALLOW."

A human reviewer — call them R — wants to check that claim. R does not trust
the agent's own summary of the execution. R has access to the repository root.

The question is: does enough evidence exist in the repository to verify or
refute the agent's claim, independently of the agent's narration?

---

## Step 1 — Request Submission (RequestRecord)

The agent submitted a request to the advisory runner. The request was
schema-validated at submission time and written to
`var/coordination/inference/requests/`.

```json
{
  "$schema": "schemas/inference/tui_advisory_request.v1.schema.json",
  "request_id": "req-20260506T031944Z-a3f891b",
  "source_request_id": null,
  "prompt": "Validate change at a3f891b against HOLD_COMMIT_MESSAGE_INVALID policy",
  "evidence_paths": [
    "tools/gitops/governed_commit.py",
    "schemas/gitops/semantic_git_hold_response.v1.schema.json"
  ],
  "resource_profile": "lean",
  "provenance_profile": "governed_commit/pre-commit",
  "allow_test_bypass": false,
  "endpoint_admission_receipt": "var/coordination/gitops/admission/ep-admit-20260506.json",
  "model": "qwen3:8b",
  "created_at": "2026-05-06T03:19:44.000Z"
}
```

**What this shows R:** the request named specific evidence paths and required a
prior admission receipt. The schema's `additionalProperties: false` constraint
means there are no hidden fields.

---

## Step 2 — Provenance Gate (Precheck)

Before executing, the runner checked `endpoint_admission_receipt`. The file
`var/coordination/gitops/admission/ep-admit-20260506.json` was found and
contained `"decision": "ALLOW-lean"`.

The `resource_profile` was `lean` (allowed). Both prechecks passed.

If either had failed, the result would still be recorded as a HOLD:

```json
{
  "status": "held",
  "hold_code": "HOLD_ENDPOINT_ADMISSION_FAILED",
  "receipt_ref": "var/coordination/inference/receipts/tui_advisory_runner_receipts.jsonl",
  "safe_next_action": "Obtain a valid endpoint admission receipt before retrying",
  "text": null
}
```

---

## Step 3 — Execution and Result (ExecutionRecord)

The runner completed execution and wrote an `ExecutionRecord` to disk.

```json
{
  "$schema": "schemas/inference/tui_advisory_result.v1.schema.json",
  "request_id": "req-20260506T031944Z-a3f891b",
  "status": "completed",
  "summary": "Governance check passed. Commit message authorship footer is present and valid.",
  "text": "ALLOW. The commit message contains a valid Co-authored-by footer...",
  "hold_code": null,
  "model": "qwen3:8b",
  "backend": "ollama",
  "authority_class": "L1-governed",
  "receipt_ref": null,
  "telemetry_ref": "var/telemetry/runs/run-20260506T031947Z.jsonl",
  "result_path": "var/coordination/inference/results/result-20260506T031947Z.json",
  "safe_next_action": null,
  "emitted_at": "2026-05-06T03:19:47.000Z"
}
```

At this point `receipt_ref` is still null. The execution exists but is not yet
sealed.

---

## Step 4 — Receipt Emission (Runner Receipt)

The runner called `_append_runner_receipt()` and appended a receipt to the
runner receipt log.

```json
{
  "receipt_id": "TUI-ADV-1746503987432",
  "receipt_kind": "ShellSessionReceipt",
  "action": "local_model_advisory_result",
  "lane": "LocalModel",
  "payload": {
    "request_id": "req-20260506T031944Z-a3f891b",
    "status": "completed",
    "summary": "local advisory execution completed",
    "hold_code": null,
    "result_path": "var/coordination/inference/tui_advisory_results/req-20260506T031944Z-a3f891b.json",
    "request_path": "var/coordination/inference/requests/req-20260506T031944Z-a3f891b.json",
    "authority_class": "advisory",
    "telemetry_ref": "var/telemetry/cortex_inference.jsonl"
  }
}
```

After appending, the runner updated the `ExecutionRecord` on disk to set
`receipt_ref` to the emitted `receipt_id`.

This runner receipt is the concrete LocalModel artifact used in the public
worked example. The canonical receipt kernel defines the stronger normalized
integrity model: content-addressed receipt identifiers and hash-chained storage
for ledgers that require independent integrity verification.

---

## Step 5 — What Is Not Verifiable Without This Structure

Suppose instead the agent used a post-hoc audit logger — a separate process
that reads the agent's log and writes a separate audit trail. The agent could:

1. execute with `resource_profile: archive`
2. omit the `endpoint_admission_receipt` check
3. write a summary claiming "ALLOW" after the fact
4. rely on the logger to record that summary rather than the input conditions

In that architecture, R cannot verify:

- which `resource_profile` was actually used
- whether the admission receipt existed at execution time
- whether the `evidence_paths` named in the request match the paths actually read
- whether the execution happened at all

With the receipt-gated surface:

- the request schema is validated before execution
- the `endpoint_admission_receipt` must exist before the gate opens
- the receipt is emitted by the same code path that performs execution
- the runner receipt is appended on every execution outcome
- the canonical receipt kernel adds chain verification where that stronger
  integrity model is required

R can refute the agent's claim by asking: does a receipt with
`receipt_id = TUI-ADV-1746503987432` exist in the runner receipt log, and does
the corresponding `ExecutionRecord` point to it?

---

## Step 6 — Reconstruction Query

R calls `build_claim_receipt_chain("req-20260506T031944Z-a3f891b")`.

```json
{
  "claim_step": {
    "claim_id": "req-20260506T031944Z-a3f891b",
    "claim_text": "Validate change at a3f891b against HOLD_COMMIT_MESSAGE_INVALID policy",
    "branch": "main",
    "basis_commit": "a3f891b",
    "submitted_at": "2026-05-06T03:19:44.000Z"
  },
  "receipt_steps": [
    {
      "receipt_id": "TUI-ADV-1746503987432",
      "transition_type": "EVAL",
      "outcome_code": null,
      "timestamp": "2026-05-06T03:19:47.432Z"
    }
  ],
  "acceptance_step": {
    "acceptance_id": "acc-a3f891b-20260506",
    "accepted_at": "2026-05-06T03:21:10.000Z"
  },
  "timeline": [
    {"event": "claim_submitted",    "at": "2026-05-06T03:19:44.000Z"},
    {"event": "eval_receipt_added", "at": "2026-05-06T03:19:47.432Z"},
    {"event": "accepted",           "at": "2026-05-06T03:21:10.000Z"}
  ],
  "branch": "main",
  "basis_commit": "a3f891b",
  "outcome": "ACCEPT",
  "recovery_id": "sha256:7b9c3d5a2e8f1b4c6e0d9a3f2c7b5e1a4d8c6f0b3e9d2a5c7f4b1e6d3a0c8f5",
  "trail_id": "trail-20260506-a3f891b"
}
```

The `recovery_id` is a SHA256 of the full reconstruction payload. A second
reviewer who runs the same query gets the same `recovery_id`. This confirms the
reconstruction is deterministic.

**Outcome for R:** the claim is ACCEPTED. The receipt trail is intact at the
reconstruction layer, and the execution evidence shows the prechecks passed.

---

## Contrast With Post-Hoc Audit

| Property | Post-hoc audit logger | Receipt-gated operator surface |
|---|---|---|
| Receipt emitted by | Separate process, reads agent logs | Same code path as execution |
| Can be omitted | Yes | No |
| Input conditions recorded | No | Yes |
| Tampering detectable | Only if logger has its own integrity | Append-only runner log; canonical layer adds chain verification |
| Fabrication possible | Yes | Harder: receipt emission is in the execution path |
| Independent reconstruction | Depends on log completeness | Yes |
