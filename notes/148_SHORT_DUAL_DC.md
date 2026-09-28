# 148 — Short-dual-class obstruction (DC) in the rank-17 engine, and what it cuts (28/09 morning, C1)

Source: the user's short-dual handoff (`code/dual_class_filter.py` is the handoff's checker, unchanged). The theorem is
PROVEN there. Its statement: no class [7κ], with κ ∈ K* and 7|κ|² ∈ {2,4,6,8,10,14}, lies in the span of the skeleton.

## Implementation
- `rank17_z4export.short_dual_forbidden`:
  - enumerates κ with 7|κ|² ≤ 14 as short vectors of 49·G_K⁻¹;
  - checks every record with the handoff's `validate_K` / `dual_record`;
  - writes the forbidden classes as export trailer 2 (55–168 classes per pair).
- **Zero-class witnesses exist** and are skipped. For κ = 2m with m ∈ K* and |m|² = 2/7, n = 8 with [7κ] = 0. The theorem
  needs β ≠ 0, so they carry no constraint; the handoff's `build_forbidden` raises on them.
- **Engine** (`rank17_z4.c`, Z4_DC, on by default outside the list/skel validation modes): a candidate g is rejected when
  g ⊕ s is forbidden for some s in the current span. DC is H-invariant and linear, so it is compatible with the canonical
  enumeration.

## Measured (Knuth, the 32 surveyed MOD4_FEASIBLE pairs, 300 walks, noisy)
- Leaves reached: D8²⁺ ×2.8, A15⁺ ×2.3, A11E6⁺ ×2.5.
- E7²⁺: only 3 comparable pairs (#20 1.4e8 → 9.3e7, #26 3.8e6 → 8.7e5).
- structures reports ×1 on ℤ¹⁷.
- **DC is a real but small tree cut: about 2–3×.**

## Findings (C1)
- **DFS bias.** All 1,206 recorded first mod-4 survivors were DC-forbidden, because the first branches use root classes (the
  LLL basis vectors). With DC on, the first DC-allowed leaf is already a mod-4 survivor (A11E6⁺ #0, E7²⁺ #20, D8²⁺ #26), and
  it passes the pairwise integer-φ check. So "mod-4 feasible ⇒ DC-forbidden" is FALSE.
- **κ-energy forcing** (the exact tight-frame energy along κ, slack 2n − #odd). Nothing is forced on A11E6⁺ #0: its only short
  dual has n = 3, slack 6.
- **structures' budget (b).** For κ with class in the span, s_u = ((κ,w_u) + t·r_u)/4 ∈ ℤ and Σs_u² = (n + 3|t|²)/4. It does
  NOT kill at the ρ level, on either DC-forbidden or DC-allowed survivors.
- **DERIVED:** at a prefix, the ±2 count j of the lift is unknown (φ fixes it), and the minimum of the IB bound over j is
  exactly DC. So single-vector IB yields nothing beyond DC at partial ρ.
- **(ρ,φ) level.** φ fixes j (the lift's outside parities are fixed up to complement by the signature condition).
  - Boundary classes (n = 12, ℓ = 4, j = 0; n = 16, ℓ = 4, j = 1; n = 18, ℓ = 2, j ≥ 1; n = 18, ℓ = 6) then force every s_u
    exactly: structures' (a), generalised.
  - This gives a cheap unary leaf filter, not a tree cut.
  - All three DC-allowed survivors carry such boundary classes (n = 16/18) in their spans. CONJECTURE (3 data points): every
    DC-allowed mod-4 survivor does.
- **Bottom line:** no ≥10⁴ partial-ρ cut found. The tree-cutting lemma must use more than one vector x at a time, or a global
  argument.
