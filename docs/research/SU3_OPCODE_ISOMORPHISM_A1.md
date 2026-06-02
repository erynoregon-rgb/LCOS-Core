# Unique 3-Bit Opcode Labeling of the Gell-Mann su(3) Commutation Table Under Fixed Convention — Public Marker A1

**Date:** 2026-06-01
**DOI:** https://doi.org/10.5281/zenodo.20499960
**Verification:** `docs/research/su3_verification.py` (standalone, numpy only)
**Script SHA-256:** `520a5bf02979715d31239aea2baf2880f2a9b6979babbd6999a11a9ce90e9d34`
**Commit:** `973d58088a264ed80444d0a7b7525cff9104f53a`
**numpy version tested:** 1.26.4

---

## Verified claim

Under a fixed Gell-Mann generator table, normalization, sign convention, and
structure-constant convention, the natural binary 3-bit opcode ordering 000–111
uniquely preserves the full su(3) commutation table among all 8! = 40,320 pure
relabelings tested.

Formally:

```
[λ_a, λ_b] = 2i f_{abc} λ_c
```

All 28 nontrivial pairs (a < b, a,b ∈ {0..7}) satisfied at machine precision
(max error: 4.44e-16). Unique among all 8! pure permutations; next best
satisfies 20/28.

The 28 nontrivial relations are the C(8,2) = 28 ordered pairs with a < b
under the fixed generator table and sign convention in `su3_verification.py`.

---

## Three-tier claim structure

```
Tier 1 — Verified:
  3-bit opcode labels can index the eight Gell-Mann generators.
  Natural binary order uniquely preserves the fixed commutation table
  under 8! permutation search.

Tier 2 — Suggested by this result:
  The opcode ordering may encode nontrivial structure, because arbitrary
  permutations fail. The uniqueness rules out a merely arbitrary relabeling
  within the tested pure-permutation search space.

Tier 3 — Not claimed here:
  That 3-bit operations themselves generate su(3).
  That LCOS implements gauge invariance.
  That the bit structure, rather than the chosen basis labeling, generates
  the bracket structure.
```

---

## The mapping

Under natural binary ordering (opcode bit value n → Gell-Mann generator λ_{n+1}):

```
000  →  λ₁
001  →  λ₂
010  →  λ₃
011  →  λ₄
100  →  λ₅
101  →  λ₆
110  →  λ₇
111  →  λ₈
```

Under this ordering, the opcode labels inherit the su(3) generator partition:
six off-diagonal/color-changing generators (λ₁ λ₂ λ₄ λ₅ λ₆ λ₇) and two
diagonal/color-neutral generators (λ₃ λ₈).

---

## What uniqueness means here

The uniqueness result shows that the natural binary ordering is rigid with
respect to the fixed su(3) commutation table used here. It rules out a merely
arbitrary relabeling within the tested pure-permutation search space.

Further work is required to show that the bit structure itself, rather than the
chosen basis labeling, generates the bracket structure. That question is open
and is not claimed here.

The result is not that bitstrings alone form su(3). The result is that, once
the bracket, basis table, normalization, and convention are fixed, the natural
3-bit ordering is uniquely compatible with the complete Gell-Mann commutation
table under exhaustive pure-permutation search. This makes the opcode ordering
a non-arbitrary basis-labeling candidate, not a standalone Lie-algebra
construction.

---

## Convention robustness

Uniqueness holds across four tested sign conventions:

| Convention | Natural order | Unique | Next best |
|---|---|---|---|
| Standard Gell-Mann | 28/28 | Yes | 20/28 |
| Negated imaginary generators (λ₂,λ₅,λ₇ → −λ₂,−λ₅,−λ₇) | 28/28 | Yes | 20/28 |
| Swapped diagonal ordering (λ₃↔λ₈) | 28/28 | Yes | 20/28 |
| Full sign flip (all generators negated) | 28/28 | Yes | 20/28 |

Note: these tests cover pure-permutation relabeling and sign flips within the
fixed-table framework. Lie-algebra automorphisms and basis changes beyond pure
permutation are outside the tested search space unless explicitly stated.

---

## What this does not cover

- Lie-algebra automorphisms or basis changes beyond pure permutation
- Whether the bracket structure is derivable from bit predicates alone
- Any implementation claim about LCOS or its governance substrate

---

## Negative controls

Tested in script section [7] under the same fixed convention as the main result.

| Ordering | Score |
|---|---|
| Natural binary (000..111) | **28/28** |
| Gray code (000,001,011,010,...) | 0/28 |
| Hamming weight ascending | 11/28 |
| Hamming weight descending | 1/28 |
| Bit-reversed (000,100,010,...) | 2/28 |
| Random control A | 0/28 |
| Random control B | 0/28 |

All controls score below the 20/28 next-best threshold established by the
exhaustive permutation search. Gray code and random controls score 0/28.

Hamming weight ascending (11/28) is the only non-natural structural ordering
to score above 0/28. Diagnostic run identifies this as a single-transposition
artifact, not partial structural overlap: the hw-ascending ordering differs
from natural binary only by swapping opcodes 011 and 100 (positions 3 and 4).
The 11 passing relations are exactly those not involving either swapped position
— the intact su(2) isospin subalgebra {λ1,λ2,λ3} and the GB pair {λ6,λ7,λ8}.
Every failing relation involves at least one swapped position. Thread closed;
no deep structural signal. Removes the Hamming-weight thread from
BIT_STRUCTURE_AUDIT_A1 open questions.

The negative controls rule out the interpretation that any compact or sequential
ordering of 8 elements would produce high scores. The uniqueness is specific to
the natural binary counting order.

---

## Next verification (open)

**BIT_STRUCTURE_AUDIT_A1:** Which parts of the su(3) commutation table are
predictable from bit-level structure alone, without using generator lookup?

Open questions:
- **Diagonal generator predicate:** positions 2 (010) and 7 (111) are the two
  diagonal generators (λ₃, λ₈). In 3-bit space, 010 has Hamming weight 1 and
  111 has Hamming weight 3 — the two extremes of the non-zero range. Test:
  "diagonal generators sit at Hamming weight 1 and Hamming weight 3." If this
  predicate holds without lookup, it is the first bit-derived structural fact
  about the mapping.
- **Output index prediction:** can the output index c in [λa,λb] = 2i f_{abc} λc
  be predicted from bitwise operations on a and b? Pure XOR fails for the
  su(2) subalgebra (0 XOR 1 = 1 ≠ 2). Test XOR-with-carry and other modified
  bit operations systematically.
- **Sign prediction:** can the sign of f_{abc} be predicted from bit/chirality
  relations among a, b, c?
- **Hamming-weight overlap:** CLOSED — single-transposition artifact (swap
  positions 3,4). No deep structural signal. See negative controls section.
- **Separation:** distinguish "basis label uniqueness" (current result) from
  "bit-derived bracket operation" (open).

---

## Safe claim boundary

**This document claims:**
- The algebraic rigidity result: natural binary ordering is the unique
  pure-permutation labeling compatible with the fixed Gell-Mann commutation
  table under the stated convention
- Convention robustness across four tested sign variants
- The priority date (2026-06-01) and DOI
- The verification method (exhaustive, standalone, reproducible)

**This document does not claim:**
- That LCOS-Core implements su(3) gauge invariance
- That bitstrings alone form a Lie algebra
- That the correspondence holds under all automorphisms beyond tested variants
- Any production capability beyond what LCOS-Core tests demonstrate
- That the bit structure generates the bracket (this is open — BIT_STRUCTURE_AUDIT_A1)

---

## Verification

```bash
python3 docs/research/su3_verification.py
```

Expected summary lines include:
```
su(3) commutation check (natural binary ordering): 28/28 passed (max error: 4.44e-16)
Natural binary ordering: UNIQUE — 28/28 (next best: 20/28 over 40,320 tested)
[λ0, λ1] = 2i λ2: HOLDS (error: 0.00e+00)
RESULT: VERIFIED
```

Requires numpy only. No LCOS or SKOS dependencies.
