# Venue Fit Matrix

This matrix separates the current manuscript family into two publishable shapes:

- **Paper A:** receipt-gated operator surface
- **Paper B:** runtime bindings for agent work

The goal is not to rank venues abstractly, but to record what evidence each
venue would require before the paper would be credible there.

| Venue | Paper version | Required evidence to be credible there | Next missing artifact |
|---|---|---|---|
| AIES | Paper A — governance/accountability paper | Concrete mechanism, worked example, explicit governance framing, bounded real-repo evidence, clear limitations | Public research-draft package and submission-ready venue framing |
| FAccT | Paper A — archival governance/accountability paper | Mechanism clarity plus stronger empirical or institutional grounding for accountability claims | Small empirical layer or reviewer/operator study showing how reconstruction changes auditability in practice |
| Governance / responsible AI workshops | Paper A — workshop paper | Concrete data structures, evidence map, worked example, honest claim-safety posture | Stable public inspection surface and concise workshop-specific framing |
| NeurIPS Evaluations \& Datasets | Paper B — runtime bindings / evaluation protocol paper | Measured byte/token reduction, task-scoped hydration protocol, comparison baseline, reproducible evaluation setup | Public measurement bundle for active-surface custody and task-scoped hydration outcomes |
| NeurIPS Position Papers | Paper A — disciplined position version | Strong argument plus repo-grounded technical evidence; position framing rather than system-overclaim | Position-paper rewrite arguing for operator-surface evidence emission as a governance norm |
| USENIX PEPR | Paper A or B — practice-facing talk | Clear system lesson, operational framing, concrete design pattern, implementation caveats | Talk-oriented narrative and practice-facing figures rather than archival apparatus |
| USENIX Security / IEEE S\&P / NDSS / CCS | Paper A only after security hardening | Threat model, tamper-resistance story, adversarial testing, external attestation or signing story, stronger integrity proof | Adversarial hardening packet with tests and deployment threat model |
| OSDI / ATC / SOSP | Paper B — systems/runtime paper | Broader evaluation, overhead measurements, failure modes, baselines, artifact-quality runtime system | Measured runtime-binding artifact with repeatable benchmarks and system comparisons |
| ICSE / FSE / ASE | Paper B — software-engineering paper | Agentic developer-workflow framing, evidence-bound coding workflow, workflow evaluation or artifact study | Evaluation showing how task-scoped hydration and custody controls affect coding-agent work |

## Immediate recommendation

Near-term:

1. Keep **Paper A** pointed at AIES/FAccT-style venues and governance workshops.
2. Hold **Paper B** until the runtime-binding measurements are packaged as a
   reproducible evaluation artifact.

## Non-goal

Do not reuse the current receipt paper unchanged for top systems or top security
venues. The current public evidence is mechanism-strong but not yet
evaluation- or hardening-complete for those audiences.
