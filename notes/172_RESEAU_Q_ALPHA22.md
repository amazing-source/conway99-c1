# 172 — The Q-lattice route for α = 22: what arithmetic gives, and what it cannot give

11 Oct 2026. This note follows up §7.1 of note 171: does the lattice of the Gram Q = 9I − 3D − N + J give an
obstruction to the α = 22 sub-case? Short answer: **no, at the level of discriminants.**
- Every condition I could derive is necessary.
- They are mutually consistent.
- All of them hold on the 271 designs of the ChatGPT dossier.

A contradiction, if one exists, needs finer information than the genus.

Scripts are in `code/asym243/hoffman/lattice/`. `lamc.py` and `r3.py` read the `.inst` files of the dossier
HOFFMAN_UPDATE_20261011; those files are not in this repo.

## 1. Clean identification of the lattices
Notation: C is the coclique (22 vertices), F the other 77, and Y, D, N = YᵀY are as in note 171.
- Q = (D − 3I)(D + I) − J = 21·P₋₄(D). Here P₋₄(D) is the projector onto the (−4)-eigenspace V of D, with dim V = 22.
  The first form follows from N = 12I + 2J − D² − D.
- **Λ := Z⁷⁷ ∩ V, the integer (−4)-eigenvectors of D.** Λ is even, because Λ ⊥ 𝟏. Its dual is Λ* = P₋₄Z⁷⁷.
- The lattice L = ⟨vᵢ⟩ of note 171 is √21·Λ*. The map x ↦ (vᵢ·x)ᵢ is an isometry from √21·L* onto Λ, because
  Σvᵢvᵢᵀ = 21I.
- The level of Λ divides 21, and det Λ = 3^{r₃}·7^{r₇} with r_p = rank_p(Q).

## 2. General facts for any srg(99,14,1,2), with no α hypothesis
Let K = Z⁹⁹ ∩ E₋₄(A), of rank 44, and Γ₃ = Z⁹⁹ ∩ E₃(A), of rank 54.
- 63P₋₄(A) = 27I − 9A + J and 77P₃(A) = 11A + 44I − 2J. So the level of K divides 63 and that of Γ₃ divides 77.
- Γ := Z⁹⁹ ∩ (E₁₄ ⊕ E₃) contains Γ₃ ⊕ ⟨𝟏⟩ with index exactly **11**. Indeed, for x ∈ Γ, (A − 3I)x = (Σx/9)𝟏 forces
  9 | Σx, and (A + 4I)e_x has Σ = 18.
- So |disc K| = |disc Γ| = |disc Γ₃|·99/11². This forces **|disc K| = 9·7^m**, and **disc(K)₃ ≅ Z/9**, coming from
  𝟏 with 𝟏·𝟏 = 99. The 7-part is (Z/7)^m.
- K is even of rank 44, so det K ≡ 1 (mod 4). Hence **m is even**.
- **ker₇(A + 4I) = K̄ + Γ̄₃.** The proof inverts 9 and 11 modulo 7. Also 𝟏 ∉ ker₇(A + 4I), since 7 ∤ 18. Together these
  give **rank₇(A + 4I) = m + 1, which is odd, and ≤ 45** (since m ≤ rank K = 44).

**Control** (`prank_test.py`). The identity rank_p(A − sI) = 1 + p-rank(disc K) holds on:
- Petersen and its complement (p = 3);
- T(7) (p = 5);
- T(8) and T(11) (p = 3).

It fails on T(10), which is expected, since p = 3 divides n = 45 and k − s = 18 there.

The parity "rank₇(A + 4I) odd" is probably known in substance (Brouwer–van Eijl 1992 work with these lattices). I have
not checked their table. Ducey et al. (arXiv 1910.07686) fully determine the *critical group* of the 99-graph, where the
prime 7 does not occur. That is another matrix.

## 3. The sub-case α = 22: gluing inside K
- The coclique side, U = span{P₋₄(A)e_c : c ∈ C}, depends **only on the design**, since Ae_c = column of Yᵀ.
- The lattice is Λ_C = Z⁹⁹ ∩ U ≅ {s ∈ Z²² : 7 | Σs, (Y − J)ᵀs ≡ 0 (mod 3)}.
  - The F-coordinates are (S′ − σᵢ)/3, where S′ = Σs/7 and σᵢ = Σ_{c∈Bᵢ}s_c.
  - The norm is 7(|s|² − S′²)/3.
  - det Λ_C = 7²²·3^{2k−19}, with k = rank₃(Y − J).
- Λ (the F side) and Λ_C are primitive in K, orthogonal to each other, and of total rank 44. Gluing gives
  |disc Λ|·|disc Λ_C| = |H|²·|disc K|. Consequences:
  1. **r₇ is even**, and r₇ ≥ 22 − m = 23 − rank₇(A + 4I).
  2. **r₃ is odd.** Moreover r₃ = rank₃(Yᵀ(J − I)Y) = w − h − 1, which depends on the design only. Here w = rank₃ Y and
     h = dim(W ∩ W^⊥) for the F₃-code W of the blocks. For a design of full 3-rank, w = 22, h = 0 and r₃ = 21.
  3. For r₃ = 21, the 3-part of the gluing is total. So disc(Λ_C)₃ must be **(Z/3)²¹ ⊕ Z/9**, with disc(Λ_C)₇ = (Z/7)²².
  4. The Schur complement of 4I gives rank₇(A + 4I) = 22 + r₇ + ε with ε ∈ {−1, 0, 1}. Combined with 1. and §2, this
     forces ε = ±1.

**Test on the 271 dossier designs** (`r3.py`, `lamc.py`). All 271 have full 3-rank (w = 22, h = 0, k = 21, r₃ = 21).
All have disc(Λ_C) = (Z/3)²¹ ⊕ Z/9 ⊕ (Z/7)²², exactly as predicted. **No design is excluded.**

## 4. Verdict
- These conditions are consistency conditions of the genus of a sublattice of Z⁷⁷ / Z⁹⁹. They hold as soon as the design
  is "normal" (full 3-rank). This explains why nothing breaks.
- A design of deficient 3-rank must satisfy w − h ≡ 0 (mod 2). That is the only design filter obtained, and it is
  probably rare.
- **The discriminant arithmetic of the Q route does not obstruct α = 22.** An obstruction would need finer data than the
  genus:
  - the actual vectors, i.e. the 77 norm-6 vectors with prescribed inner products;
  - or the theta series. Λ is even of level 21, so θ is in M₁₁(Γ₀(21), χ₋₃), but we know too few coefficients.
- I recommend not investing further in this route without a new idea. For α = 22, the covering route remains an exact
  search, with cubes or with the dossier's row domains, on a machine that does not restart.
