# Review Response Matrix

**Paper:** Typed Evidence Contracts for Blocking Unsupported AI-Assisted Claims

| Reviewer concern | Response | Paper handling |
|---|---|---|
| Too small or toy-like | Correct. LCOS is intentionally small so the proof is runnable and inspectable. | State as design constraint, not weakness. |
| Not an empirical study | Correct. This is a proof note over fixtures and receipts, not a user study. | Move empirical claims to future evidence. |
| Does not prove semantic correctness | Correct. The receipt proves a constraint check ran and was recorded. | Explicit non-claim in section 5. |
| Depends on private SKOS | The LCOS-native package cites only LCOS-local evidence. | Evidence map excludes private implementation paths. |
| Style quality is not governance | Correct. The mechanism checks claim transition admissibility, not polish. | Keep style tooling out of the proof claim. |
| HOLDs may be too conservative | Possible. False HOLD and false allow rates require follow-up measurement. | Listed under next evidence needed. |

## Preservation Rules

- Keep the paper shorter than the imported background draft.
- Keep claims LCOS-local.
- Treat polished unsupported claims as worse than awkward grounded claims.
- Do not promote future evaluation work into current results.
