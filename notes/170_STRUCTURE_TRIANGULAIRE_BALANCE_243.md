# 170 — Origin of balance at 243: the triangle theorem (11/10, evening)

*Continuation of note 169 (§1, balance). Notation as in notes 168–169: Z = ⊕ Z_A (sum-zero functions on each grid),
R/S = line functions / mixed functions, K = +1 on R and −1 on S, U = (2/(2r+1))(A + ½) restricted to Z (a reflection),
C = Π_R U Π_R. At 243: r = 4, U = K/3 + N, where N is the "between grids" part. Code and data: scratchpad scripts,
summarised in §6.*

## 0. Summary
Balance (Σ_paired cos 2θ = 0, i.e. m − m′ = 36) is **neither an accident of the 4 known graphs nor a consequence of
the coarse linear algebra**. It comes from a precise structure that is specific to the **three-part** quotient
K_{9,9,9}:

> **Triangle theorem (proved).** Let N₊ be the part of N going from part p+1 to part p (cyclic orientation of the
> three parts) and α = Π_R N₊ Π_R. Then:
> 1. α is **normal**;
> 2. its spectrum lies in the **equilateral triangle** T with vertices −2/3 and (2/3)e^{±iπ/3};
> 3. the spectrum of C is the union of the triples (1/3 + 2 Re ωᵏz)_{k=0,1,2}, one for each orbit {z, ωz, ω²z},
>    each triple summing to 1;
> 4. **Σ_paired cos 2θ = number of orbits strictly inside T**. This is a **nonnegative integer**, and balance holds
>    ⇔ spec(α) ⊂ ∂T.

Remaining lemma (**observed everywhere, not yet proved**): spec(α) ⊂ ∂T. Equivalently, X = N₊ᵀN₊ − 4/9
**anticommutes with K**. In graph terms (§4): for two grids B ≠ B′ of the same part, the "line × line" component of the
matrix of common neighbours located in the **preceding** part vanishes.

## 1. Balance is not a consequence of coarse linear algebra
**"Part-level" abstract model.** Take W = ⊕_{p=1..3}(R_p ⊕ S_p) and a half-dimensional subspace E whose compression on
each part is 2/3 on R_p and 1/3 on S_p. This model satisfies all the block identities and the three-part structure.
Yet it admits **unbalanced** solutions:
- for d = 1, an explicit Z₃-symmetric family a = (x, 0, z), b = (u, v, w) (rotations by 120°), checked to 10⁻¹⁵;
- the least-squares solutions (d = 1, 2) all have m = m′ = 0 and Σ cos 2θ = d.

Hence balance is not a consequence of the identities of note 168 alone.

## 2. The "orthogonal-block" model and the deformations of the known graphs
In a grid cover, each block N_AB is (2/9)·O_AB, where O_AB ∈ O(8) is the matching compressed to Z. The **real
relaxation** replaces the permutations by arbitrary orthogonal matrices while keeping U² = I.

**Linearisation at the known graphs** (unknowns X_AB ∈ so(8); gauge = O(R_A) × O(S_A) per grid, dimension 324):

| configuration | tangent | gauge orbit | stabiliser | non-trivial deformations H¹ | 2nd order |
|---|---|---|---|---|---|
| twin, partition 0 | 324 | 322 | 2 | 2 | obstruction = **one** indefinite quadratic form (q₁₁ = −q₀₀, q₀₁ ∥ q₀₀): 2 unobstructed lines |
| Γ₃, partition 2 (deck = 1) | 343 | 324 | 0 | **19** | obstruction **identically zero** (10⁻¹⁶) |
| Γ₄, partition 0 | 384 | 322 | 2 | **62** | not computed |

- The stabiliser of the twin (2) comes from Mon = 3-group of order 81 and deck Z₃. Each complex-type summand of the
  monodromy representation contributes one dimension.
- **Continuation** (Gauss–Newton, minimum-norm steps): it converges to machine precision (residual 10⁻¹⁴) along the
  twin's lines and along a random direction of Γ₃'s family, up to |U − U₀| = 0.22. Gauge-invariant quantities change
  (triangle holonomy traces), so these are genuinely new configurations, and they are no longer graphs.
- **Balance persists everywhere.** On Γ₃'s family, (m, m′) goes from (56, 20) to (50, 14): eigenvalues leave ±1 in
  pairs. Throughout, **m − m′ = 36**, and the inner spectrum stays **exactly symmetric** (λ ↔ −λ, to 10⁻¹⁵).
- **Every inner eigenvector has weight exactly 1/3 on each part.** This was the clue that led to §3.

## 3. The triangle theorem (proofs)
**Cyclic decomposition.** Let D = ωᵖ on part p. Since N has no block inside a part, N = N₊ + N₊ᵀ with DN₊D⁻¹ = ω̄N₊.
Splitting U² = I by degree gives:
- (a) N₊N₊ᵀ + N₊ᵀN₊ = 8/9 (degree 0);
- (b) N₊² = −(1/3)(KN₊ᵀ + N₊ᵀK) (degree 1).

Equivalently: U + DUD⁻¹ + D²UD⁻² = K, i.e. four reflections whose sum is zero.

**Blocks.** Write N₊ = [[α, β], [γ, δ]] in (R, S). Then (b) reads:
- α² + βγ = −(2/3)αᵀ;
- δ² + γβ = (2/3)δᵀ;
- αβ = −βδ;
- γα = −δγ.

**(i) α is normal.** αᵀ = −(3/2)(α² + βγ), so [α, αᵀ] = −(3/2)[α, βγ]. Moreover αβγ = −βδγ = βγα. Hence
ααᵀ = αᵀα. The same argument shows δ is normal. ∎

**(ii) spec α ⊂ T.** Let V_z be an eigenspace of α (also of αᵀ, with eigenvalue z̄) and W_{−z} the eigenspace of δ for
−z.
- The intertwinings αβ = −βδ and γα = −δγ (and their transposes) show that β, γᵀ: W_{−z} → V_z and γ, βᵀ: V_z → W_{−z}.
- On V_z: βγ = b := −(2/3)z̄ − z²; on W_{−z}: γβ = b; and by (a), ββ* + γ*γ = s := 8/9 − 2|z|².
- If b ≠ 0, then β = bγ⁻¹, and M = γ*γ satisfies M² − sM + |b|² = 0. This requires s ≥ 2|b|.
- Writing z = (2/3)w, the inequality s ≥ 2|b| becomes 1 − 3|w|² − 2 Re(w³) ≥ 0, i.e.
  **8 ∏_{k}(1/2 − Re ωᵏw) ≥ 0**. Inside the disc |w| ≤ 1 (forced by s ≥ 0), this is exactly T.
- If b = 0, then z is 0 (the centre) or a vertex. ∎

**(iii) Triples.** C = 1/3 + α + αᵀ equals 1/3 + 2 Re z on V_z. D maps V_z isometrically onto V_{ωz}. So the spectrum
of C splits into triples (1/3 + 2 Re ωᵏz)_k, and each triple sums to 1 (since 1 + ω + ω² = 0). ∎

**(iv) Counting.**
- An orbit on an **edge** (Re ωᵏz = 1/3 for some k) gives the triple (1, x, −x).
- A **vertex** gives (1, 1, −1).
- An **interior** orbit gives three inner eigenvalues summing to 1.

Hence Σ_paired cos 2θ = #(interior orbits) ∈ ℤ_{≥0}, and m − m′ = 36 − #(interior orbits). ∎

**(v) Characterisation.** Let X := N₊ᵀN₊ − 4/9 (degree 0). Then balance ⇔ Π_R X Π_R = 0 ⇔ γᵀγ = ββᵀ ⇔ M = s/2 on every
V_z ⇔ s = 2|b| ⇔ spec α ⊂ ∂T. (The centre z = 0 is excluded: there βγ = 0 contradicts the invertibility of β and γ.)

**(vi) Algebraic properties of X (proved).**
- {N₊, X} = 0. This follows from (a) alone: N₊X + XN₊ = (N₊N₊ᵀ + N₊ᵀN₊ − 8/9)N₊ = 0.
- Y := XK + KX commutes with N₊, N₊ᵀ, K and D. X commutes with N₊², which by (b) gives YN₊ᵀ = N₊ᵀY. So Y lies in the
  **centre** of the algebra 𝒜 generated by (K, N₊, N₊ᵀ, part projections).
- **Per-cell orthogonality** (each O_AB orthogonal) ⇒ the cell-diagonal blocks of N₊ᵀN₊ equal 4/9 ⇒ **X_BB = 0 and
  Y_BB = 0 for every grid B**.
- Balance (R side and S side) ⇔ Y = 0.

**Where the proof stands.** Y is central with zero cell-diagonal blocks. If the cell projections belong to 𝒜, then Y
commutes with them and is therefore zero; this covers the "irreducible" configurations. In general (graphs with
symmetry), more work is needed. Numerically: |Y| < 10⁻¹⁴ on all 4 graphs and on every deformed configuration.

## 4. Combinatorial form of the remaining lemma
Let B ≠ B′ be two grids of the same part, and n₋(x, y) the number of common neighbours of x ∈ B and y ∈ B′ lying in the
preceding part (n₋ + n₊ = μ = 2). **Lemma (conjectured):** the matrix n₋ has zero component in R_B ⊗ R_{B′} and zero
component in S_B ⊗ S_{B′}.
- Check: BvLS splits 1 + 1 everywhere (n₋ ≡ 1).
- The twin, Γ₃ and Γ₄ have 1296 to 2592 pairs whose split is not 1 + 1. Even so, the lemma holds for all of them
  (Y = 0).

## 5. What this means for 99
- The mechanism relies on the **Z₃ grading of the three parts** of K_{9,9,9}. K₁₁ (sub-case A) has no such grading, so
  the triangle theorem **does not transfer as it stands**. At 99 the trace identity forces imbalance anyway
  (note 169). The general principle "balance ⇒ (A) impossible" is therefore **not** the right route.
- **What does transfer is the method.** Decompose the algebra of the configuration (A, K, partition) by degree, then
  read off the spectrum of the line-function compression from a normal operator with a geometric spectral locus.
  For K₁₁, the analogue would use the structure of the 11 grids. The tool to look for is an "orientation" (tournament
  or cyclic decomposition) that is compatible with the gluing laws.
- **Real relaxation of (A) (orthogonal blocks on K₁₁): inconclusive.** Levenberg–Marquardt from random starts finds no
  solution (residual ≈ 0.25). But the same method also fails on K₅, where an explicit solution exists (O_AB = −K). So
  these failures prove nothing.

## 6. Reproduction (`code/asym243/balance/`, run from `code/asym243/`)
- `abstract.py`, `z3family.py`: part-level model (§1).
- `deform.py`, `second.py`, `h1dirs.py`: tangent space, gauge, stabiliser, 2nd-order obstruction (§2).
- `follow.py`, `invariants.py`: continuation and gauge invariants (§2).
- `chiral.py`, `pairing.py`, `normal.py`, `xstruct.py`: tripartite identities, part-weights, normality of α, triangle
  spectrum, structure of X and Y (§3).
- `orthomodel.py`, `relax.py`: real relaxations (§5).
