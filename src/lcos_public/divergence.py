"""Advisory divergence measure — proposer measures ε, the substrate holds the floor.

A proposer can measure how far a proposed action diverges from an authored
reference. It cannot set its own admission floor (the threshold is gate-owned,
not a call-time argument), and the measurement is advisory: by itself it can
only *tighten* a gate decision, never authorize one.

The scorer is a deliberately generic token-Jaccard stand-in for a learned
embedding distance — transparent, deterministic, and swappable. The governance
semantics around it are the load-bearing part, not the scorer internals.

Public proof demonstration only.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

DivergenceVerdict = Literal["WITHIN", "DIVERGENT", "UNVERIFIABLE"]

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> set[str]:
    return set(_TOKEN.findall(text.lower()))


@dataclass(frozen=True)
class DivergenceResult:
    """Advisory measurement. ``score`` is 0.0 (identical) .. 1.0 (disjoint)."""
    score: float
    verdict: DivergenceVerdict
    reason: str
    scorer: str

    def to_payload(self) -> dict[str, object]:
        return {
            "score": self.score,
            "verdict": self.verdict,
            "reason": self.reason,
            "scorer": self.scorer,
        }


@runtime_checkable
class DivergenceScorer(Protocol):
    """A distance in [0, 1]: 0.0 identical, 1.0 fully disjoint."""
    name: str

    def distance(self, proposed: str, reference: str) -> float: ...


class TokenJaccardScorer:
    """Generic, dependency-free stand-in: 1 - Jaccard(token sets).

    Order- and frequency-insensitive on purpose. Swap in a learned distance
    behind the same interface; the governance does not change.
    """
    name = "token_jaccard_v0"

    def distance(self, proposed: str, reference: str) -> float:
        a, b = _tokens(proposed), _tokens(reference)
        if not a and not b:
            return 0.0
        union = a | b
        if not union:
            return 0.0
        return 1.0 - len(a & b) / len(union)


class DivergenceGate:
    """Advisory divergence assessment with a gate-owned floor.

    The threshold (floor) is fixed at construction. ``assess`` takes only the
    two texts — there is no call-time threshold argument, so a proposer cannot
    lower the floor to force a WITHIN verdict.
    """

    def __init__(self, *, threshold: float = 0.5, scorer: DivergenceScorer | None = None) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be in [0, 1]")
        self._threshold = threshold
        self._scorer: DivergenceScorer = scorer or TokenJaccardScorer()

    @property
    def threshold(self) -> float:
        return self._threshold

    def assess(self, proposed: str, reference: str) -> DivergenceResult:
        # Fail-closed: an absent/empty reference is UNVERIFIABLE, never WITHIN.
        if not proposed.strip() or not reference.strip():
            return DivergenceResult(
                score=1.0,
                verdict="UNVERIFIABLE",
                reason="empty proposed text or reference; cannot measure divergence",
                scorer=self._scorer.name,
            )
        score = self._scorer.distance(proposed, reference)
        verdict: DivergenceVerdict = "WITHIN" if score <= self._threshold else "DIVERGENT"
        return DivergenceResult(
            score=score,
            verdict=verdict,
            reason=f"divergence {score:.3f} vs gate-owned floor {self._threshold:.3f}",
            scorer=self._scorer.name,
        )
