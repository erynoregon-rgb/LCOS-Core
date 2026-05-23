# Receipt-Gated Operator Surfaces for Verifying Claims About AI Agent Behavior

**Status:** public research draft  
**Snapshot:** A2 public packaging surface  
**Source lineage:** imported into LCOS-Core from the SKOS-Core receipt-gated operator surface package on 2026-05-19
---

## Abstract

AI governance frameworks require that claims made about AI systems be verifiable after the fact. We describe a receipt-gated operator surface: an interface through which AI systems both execute operations and emit evidence of those executions. The surface is instantiated as a schema-validated inference runner that writes request and result records, appends runner receipts on the execution path, and exposes a canonical receipt kernel as the normalized integrity model. We show that this design, rather than adding an audit layer on top of an existing interface, makes evidence emission a structural property of the interface itself. A reviewer who doubts an agent's claim can reconstruct the relevant execution evidence deterministically from the repository without re-running the system. We present the architecture, a concrete worked example using field-level record content, and a comparison with post-hoc audit logging.

---

## 1. Introduction

Consider an AI coding agent that operates in a repository and emits a summary: "I validated the change against governance policy and the result was ALLOW." A human reviewer wants to check that claim. The reviewer does not trust the agent's narration. What evidence exists in the repository?

If the agent used a post-hoc audit logger (a separate process that reads the agent's output and writes a separate record), the answer is: whatever the logger chose to record. The logger may have been added or removed; it may record only the outcome, not the input conditions; and its records can be fabricated or omitted without breaking the execution path.

A receipt-gated operator surface is one in which evidence emission is not an optional add-on but a structural property of the execution path: an operation cannot complete without also emitting a receipt. We instantiate this design as an inference advisory runner with a schema-validated request record, a typed execution result, a runner receipt appended on every execution path, and a deterministic reconstruction function. The receipt kernel defines the stronger canonical receipt model—content-addressed and hash-chained—used in this paper as the normalized integrity abstraction. A reviewer can verify a claim by checking repository evidence rather than relying on the agent's own account. A post-hoc logger, by contrast, is a separate module that can be removed without altering the execution path; in a receipt-gated surface, receipt emission is in the execution path and cannot be omitted without breaking the operation.

---

## 2. Mechanism

The operator surface consists of five stages with one primary record type each.

The agent submits a `RequestRecord` (JSON Schema `tui_advisory_request.v1`). Required fields include `request_id`, `prompt`, `evidence_paths`, `resource_profile` (one of `lean | promotion | archive`), and `endpoint_admission_receipt` — a pointer to an admission receipt that must already exist on disk. The schema sets `additionalProperties: false`; no undeclared fields are accepted. The request is written to disk before execution begins.

Before executing, the runner checks two typed preconditions: (a) `resource_profile ∈ {lean, promotion}`, and (b) the file named by `endpoint_admission_receipt` exists and contains a decision starting with `ALLOW`. If either check fails, the runner emits a HOLD runner receipt with a typed hold code (`HOLD_ENDPOINT_ADMISSION_MISSING` or `HOLD_ENDPOINT_ADMISSION_FAILED`) and terminates. The HOLD is recorded to the receipt log exactly as a completed execution would be.

The runner executes and writes an `ExecutionRecord` (JSON Schema `tui_advisory_result.v1`). The status field is an enum: `completed | held | refused | error`. The `receipt_ref` field is null at this point, to be populated after receipt emission.

The runner calls `_append_runner_receipt()`, which appends a runner receipt to the receipt log. On the LocalModel path, this record uses a monotonic identifier of the form `TUI-ADV-<millis>` and stores the execution outcome in a bounded payload. After appending, the runner updates the `ExecutionRecord` to set `receipt_ref`. The record is now sealed.

The receipt kernel separately defines a `CanonicalReceipt` whose `receipt_id` is content-addressed and whose entries can be appended to a hash-chained ledger. In this paper, the worked example uses runner-receipt fields because they are the concrete mechanism exercised by `tui_advisory_runner.py`; the canonical model explains the stronger integrity property the implementation is converging toward.

A reviewer calls `build_claim_receipt_chain(claim_id)`, which returns a `ClaimReceiptChain` containing the full timeline, the basis commit, an ordered list of receipts, and a `recovery_id` (SHA256 of the reconstruction payload). Two reviewers who call this function with the same `claim_id` and `repo_root` receive the same `recovery_id`, confirming determinism.

| Stage | Record Type | Schema source | Key integrity property |
|---|---|---|---|
| Request submission | `RequestRecord` | `tui_advisory_request.v1.schema.json` | `additionalProperties: false`; written before execution |
| Provenance gate | Runner HOLD receipt | `tui_advisory_runner.py` | Typed hold codes; HOLD is recorded, not silently dropped |
| Execution | `ExecutionRecord` | `tui_advisory_result.v1.schema.json` | `receipt_ref` null until sealed; status enum bounded |
| Receipt emission | `RunnerReceipt`; canonical `Receipt` | `tui_advisory_runner.py`; `receipt_kernel.py::CanonicalReceipt` | Runner path records every outcome; canonical layer defines content-addressed hash-chained verification |
| Reconstruction | `ClaimReceiptChain` | `audit/reader.py` | Deterministic; `recovery_id` independently verifiable |

**Receipt layers.** The implementation contains two receipt layers. The advisory runner (`tui_advisory_runner.py`) emits runner receipts for all execution outcomes on the LocalModel path; these receipts use the concrete fields shown in the worked example. The receipt kernel (`receipt_kernel.py`) defines a canonical hash-chained receipt type used as the paper's normalized model for integrity claims. The paper distinguishes these layers explicitly: the worked example is runner-receipt-based, while content-addressed and chain-verification claims refer to the canonical layer.

---

## 3. Worked Example

An agent submits a `RequestRecord` with `request_id = "req-20260506T031944Z-a3f891b"`, `resource_profile = "lean"`, and `endpoint_admission_receipt = "var/.../ep-admit-20260506.json"`. The provenance gate checks that the file exists and that its decision is `"ALLOW-lean"` — both pass. The runner executes and writes an `ExecutionRecord` with `status = "completed"`. The runner then appends a runner receipt:

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

This example uses the concrete runner receipt emitted by `_append_runner_receipt()`. A reviewer who doubts the agent's claim calls `build_claim_receipt_chain("req-20260506T031944Z-a3f891b")` and receives a `ClaimReceiptChain` with `outcome = "ACCEPT"`, a `recovery_id`, and the full timeline. The reviewer confirms that the runner receipt exists, that the `ExecutionRecord` points to it via `receipt_ref`, and that the prechecks passed.

**The counterfactual:** If the agent had fabricated its summary after the fact — writing `status = "completed"` without executing — there would be no receipt in the chain for this `request_id`. The design makes absence of a receipt detectable: `build_claim_receipt_chain` returns zero `receipt_steps` for that `request_id`. We have not evaluated this property under adversarial conditions.

---

## 4. Related Work

The EU AI Act [eu_ai_act] and NIST AI RMF [nist_ai_rmf] specify audit requirements but do not prescribe implementation. Reuel et al. [reuel2024openproblems] survey evaluation challenges for advanced models; governance trace mechanisms address the "post-deployment" gap they identify.

Documentation of model properties (Mitchell et al. [mitchell2019modelcards]; Gebru et al. [gebru2021datasheets]) is a narrative product, not a verification mechanism. The receipt-gated surface produces structured evidence that complements documentation.

Append-only log implementations (Waltersdorfer et al. [waltersdorfer2025provenance]; Hyperledger Fabric; Apache Kafka log compaction) provide tamper-evidence at the storage layer but do not integrate with the execution gate. Our design integrates receipt emission into the same code path as the execution.

Governance monitoring platforms (IBM watsonx.governance [ibm_watsonx] and similar) provide monitoring dashboards and audit trails as post-hoc overlays: they can be added or removed without changing the execution path. We demonstrate that a gate-first design eliminates this optionality.

ML provenance systems (MLflow [mlflow2018]; DVC; W3C PROV [w3cprov2013]) track model artifacts and training lineage. These systems focus on dataset and model provenance rather than per-operation governance evidence, and do not model the claim-to-receipt-to-reconstruction cycle.

Chen [chen2025evibound] introduces a dual-gate architecture for autonomous research agents: a pre-execution approval gate checks acceptance criteria before code runs, and a post-execution verification gate queries MLflow artifacts before results are promoted. EviBound and receipt-gated operator surfaces share the premise that governance should be architectural rather than prompt-level. They differ in mechanism: EviBound verifies against an external artifact store after execution, whereas the receipt-gated surface makes evidence emission part of the execution path itself.

Recent governance commentary also emphasizes the accountability gap around verifiable audit logs and external requests for AI influence records [stevens2025verifiableauditlogs, aivo2025externalinfluence]. We cite these as adjacent operator-facing problem statements, not as implementation evidence.

The Model Context Protocol (MCP) [mcp2024] defines a standard for AI tool use but does not specify evidence emission as a surface requirement. LlamaIndex and LangChain provide agent orchestration without built-in receipt gating. Receipt gating could be applied as a constraint on any MCP-compatible surface.

Proof-carrying code (Necula [necula1997]) provides a precedent for programs carrying safety proofs as data structures. The receipt-gated surface is analogous: receipts are evidence attached to the execution, enabling post-hoc verification of governance properties rather than safety properties.

Model evaluations (Shevlane et al. [shevlane2023extremerisks]) serve as governance inputs. A receipt-gated surface provides the per-operation evidence substrate that evaluation frameworks assume exists but do not specify.

---

## 5. Governance Requirements Mapping

The following table maps mechanism properties to governance obligations recognised in current frameworks. This mapping is direct: each property was designed to satisfy a specific audit or accountability requirement, not inferred from it post-hoc.

| Governance Obligation | Mechanism Property | Framework Reference |
|---|---|---|
| Audit obligation | Request and execution records written to disk before completion; append-only store preserves all outcomes including refusals | EU AI Act Art. 12 [eu_ai_act]; NIST AI RMF GV-6 [nist_ai_rmf] |
| Incident traceability | `build_claim_receipt_chain` reconstructs the full execution timeline from `claim_id` and `repo_root` without re-running the system; `recovery_id` is independently computable | Supports post-incident review; NIST AI RMF MG-3 |
| Non-repudiation / evidence integrity | Runner receipts preserve emitted outcomes in append-only logs; the canonical receipt kernel defines content-addressed identifiers and hash chaining for the normalized integrity model | W3C PROV provenance principles [w3cprov2013] |
| Hold accountability | HOLD decisions are recorded with typed codes in the same append-only store as completions; governance refusals are not silently dropped from the evidentiary record | Satisfies audit requirements where denials must be documented alongside approvals |

---

## 6. Conclusion and Limitations

A receipt-gated operator surface makes evidence emission a structural property of execution: receipts are emitted by the same code path that performs the operation, not by a separate logging layer.

**Limitations.** The current implementation is not production-hardened for adversarial settings. A sufficiently privileged actor who can modify the codebase directly can alter the receipt emission logic. The hash chain detects tampering with the receipt store, but not with the emitter itself. A deployment-ready version would require code-signing or an external audit oracle to attest that the emitter has not been modified. In forked or independently modified repositories, reviewers may compute different `recovery_id` values because the reconstruction depends on `repo_root` and basis commit; cross-repository reconciliation requires an additional attestation layer. The reconstruction function (`build_claim_receipt_chain`) assumes a consistent `repo_root`; receipts from forked repositories are not automatically reconciled. Finally, the approach addresses structural verifiability, not semantic correctness: a receipt proves that a governance check ran, not that the check was adequate.

---

## Impact Statement

This paper presents infrastructure for governance verification of AI systems. The direct application is improving the quality of evidence available to reviewers and regulators. There is no immediate risk of harm from the architecture itself. The claim that a receipt-gated surface improves governance accountability is an interpretive claim, not an empirically measured one; we present the architecture and its structural properties, not a deployment study.
