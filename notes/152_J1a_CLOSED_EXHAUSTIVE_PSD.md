# 152 — J1a is CLOSED: exhaustive PSD enumeration plus rank-deficient shell completion (28/09 late night, C1)

**Result.** R6's cell J1a has no realisation. J1a means n = 6 and cut size 1: twelve ±1 on star(c) and three ±2 labels off
star(c).
- Types (i), (ii), (iv) and (vi) were killed by hand (notes/151 §2.7–2.9).
- Types (v) (triangle) and (iii) (P₄) are killed here by an exhaustive exact computation. The user authorised it on 28/09
  late night: no SAT/LP, the whole machine, no second reader.
- **R6 now has only J2 and J3 open.**

Code: conway99-c1 code/r6/j1av/.
- Kernels: j1av_psd.c and j1a_psd_gen.c.
- Generators: gen_base.py and gen_base_iii.py.
- Pipeline: postfilter.py, pipeline_gen.py, mshell_run.py, mshell_strict.py and shell2_iii.py.
- Validation: validate.py and validate_gen.py.

## 1. The model (all hand-derived; references in notes/151)
Labels are the 12 star labels (K, s), with rep e_c + s e_K, plus V₁, V₂, V₃. Positive representatives are used throughout.
- **(v).** Every cell is S-type, α_L = a_K, Σa = 0. v₁ = e₁ − e₂, v₂ = e₂ − e₃, v₃ = e₃ − e₁ (blocks 1–3 = triangle).
- **(iii).** Cells d, g are X-type with a_d = −1, a_g = +1, so α = a_K·s there; cells e, f, h, i are S-type with Σa = 0.
  v₁ = (d⁺, e⁻), v₂ = (e⁺, f⁻), v₃ = (f⁺, g⁻).
- **Q and P.** Q is a bijection between the α = +1 and α = −1 labels (reps adjacent in O_{c+}). P is a perfect matching
  inside each α-class. Same-cell edges are allowed.
- **Groups.** Each G_k (the star neighbours of v_k) has 2 labels with α = +1 and 2 with α = −1.
- **Line rules.** The A-root of L lies in O_{K^{−α_L s}}. If that inner vertex belongs to v_k and v_k's Q-partner there is an
  S-vertex, then L ∉ G_k. In (iii) the partners Q_d(v₁) and Q_g(v₃) are not S-vertices, so at most one of (d,±) is in G₁
  and at most one of (g,±) is in G₃.
- G on U has the Q and P edges, the edges L–V_{g(L)}, and a K₃ on the V's. D_UU = 0 (free star; the D-partners of the V's
  are zeros).

## 2. The tests (every one is a necessary condition, derived in notes/151 §7 and in this note)
- **Odd.** 12I + 4G − RRᵀ = 28P₋₄|_U must be PSD.
- **Even.** 6I − 2G − |R||R|ᵀ + J = 14P⁺|_U must be PSD, where P⁺ is the σ-even (−4)-projector with 14P⁺ = 6I − 2Q − MMᵀ + J.
  This formula is re-derived here.
- **Complement and P₃ tests.** Also 8I + 2G + |R||R|ᵀ − J ⪰ 0, 21P₃|_U = 12I − 3G − RRᵀ ⪰ 0, and
  105P₃⁺|_U = 60I + 15G − 3|R||R|ᵀ − 4J ⪰ 0.
- **Support λ/μ rules.**
  - R7: for a label W of group j and k ≠ j, #(G_star-neighbours of W in G_k) + [the positive rep of W shares an inner vertex
    with v_k] ≤ 1. This is μ(w⁺, v_k) with the common neighbour σv_j.
  - R7′: the same with k = j, bound ≤ 2.
  - C4: two labels of one group whose A-roots lie on opposite c-sides have at most 1 common G_star-neighbour or shared inner
    vertex. This is μ with the common neighbour v_k.
- **Shell completion (NEW, decisive).** M_full = 12I − 4T − RRᵀ = 28P₋₄ on all 42 labels has rank exactly 15 and
  M_full² = 28M_full.
  - For the support U, let r = rank M_U and P = M_U⁺. Every other label Y has a row m_Y = −4T_{YU} − R_U r_Y.
  - **(K)** z ∈ ker M_U implies z ∈ ker M_full, so m_Y·z = 0 EXACTLY (in integers).
  - **(B)** Σ_{Y∉U} m_Y m_Yᵀ = 28M_U − M_U². So any partial sum is ⪯ this matrix.
  - **(S)** For any set of added labels, S = M_WW − m_Wᵀ P m_W must be PSD of rank ≤ 15 − r. Equivalently, the residuals of
    the non-support labels form a tight frame of R^{15−r} with constant 28.
  - **The m-zeros.** m_jk is the second common neighbour of v_j and v_k. By the no-hub lemma, T(m) = {v_j, v_k}. Its 4
    corners are A-roots: 1 in G_j, 1 in G_k, and 2 in G_l on opposite c-sides (pair cover in O_{c+}). T = 0 between
    distinct m's.
  - **Cells of the m's.** In (v), m lies in a cell inside {s,t,u}. In (iii), m₁₂ ⊂ {d⁻,h,i}, m₂₃ ⊂ {g⁺,h,i} and
    m₁₃ ⊂ {d⁻,g⁺,h,i}.
  - **The (iii) apex.** a₁₃ is the common neighbour of v₁ and σv₃; it is a zero with T = {v₁, σv₃}. It has 2 A-corners and
    2 σA-corners, c₁ = σc₃ = 0 (λ-lines saturated), c₂ ≤ 1 and σc₂ ≤ 1. Its cell avoids d⁺, e⁻, f⁻ and g⁺. Its T to the
    m's is left free in {0, ±1}.

## 3. Runs (exact integer inputs; shifted Cholesky with robust margin 1e-3; marginal cases never used as kills)
| stage | J1a (v) | J1a (iii) |
|---|---|---|
| support configurations (a or α, groups, Q, P) | 2 741 040 000 (160 s, 16 threads) | 1 400 328 000 (116 s) |
| pass odd + even + complement | 133 056 (+21 312 marginal) | 125 408 (+17 456 marginal) |
| after R7, R7′, C4 and the P₃ tests | 103 968 | — (one pipeline) |
| after the M-shell completion (lenient tolerances) | 288 | 16 |
| after the strict M-shell (exact (K) + (B) + (S)) | **0** (no m₁₂ option is orthogonal to the 3-dimensional kernel) | 16, each with a unique m-triple |
| after shell 2 (apex, u's, D's; exact (K) + (B) + joint rank ≤ 2) | — | **0**: the apex a₁₃ has no admissible row |

**Checks.**
- The kernel was validated against numpy eigenvalues on 400 random configurations and on structures' 13 sampled survivors
  (all 13 are in the base list; verdicts identical).
- The generic kernel checks the identities M_o a = 28a, M_o κ = 0, G a = 4a and Rᵀa = 0.
- The (v) kernel kill was re-verified on 4 survivors with sympy integer kernels: min over options of max |m·z| = 4 or 24.

## 4. What made it work, and what it implies for J2, J3 and R8
- **Support-level tests alone never close a cell.** In (v), 98 784 configurations pass everything local; they are the
  symmetric ones.
- **The decisive ingredient is global.** The full 42-label Gram has rank exactly 15. So once the support Gram is
  rank-deficient, every other label is pinned: its row must be exactly orthogonal to the support kernel, and the residuals
  must tile R^{15−r} as a tight frame with constant 28.
- For R8 k=1 (same shape) this should transfer directly (sent to structures).
- For J2 and J3 the support has 21 and 24 labels. There the support Gram itself must have rank ≤ 15, so its nullity is at
  least 6 or 9. The same exact kernel and budget machinery applies, but the support graph needs a new parametrisation (next
  target).
