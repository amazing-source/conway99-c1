# Mission: re-prove the exclusion of C2 without the computation (lab session, started 13 October 2026)

Target: NOT-EX for the system of `MODEL.md` (no srg(99,14,1,2) with an automorphism of order 2), by arguments a reader
can follow, without the pass over the 156 lattices. Guard rail: the same system with 7 replaced by 2 or 11 has
solutions, so a valid argument must use 7. Every attempt is recorded here, failed ones included, because the mission
also asks for a comparison with the earlier campaigns.

Status of everything below: own derivations and own code of 13/10, not audited by a third party.

## 0. Where the existing proof spends its computation
(`lemma/upstream/AUDIT_REDUCTION.md`; digest by a sub-agent in `DIGEST_T16_T18_T20_ENGINE.md`.)
* Theorem R (hand): a frame (7 h of norm 4, 42 u of norm 3) and y1, y2 of norm 7 in an odd unimodular lattice U of
  rank 24; for v in U, E(v) = 7(v,v) - (v,y1)^2 - (v,y2)^2 is the sum of squares of a sigma-odd integer
  (-4)-eigenfunction; E(v) >= 8 outside J = Z y1 + Z y2 (hand lemma A.5).
* Machine part 1: the 156 lattices, all pairs (y1, y2), an engine with short-vector rules and frame-search rules.
* Machine part 2: inside the lemmas T16, T18, T20 (no eigenfunction with E = 8, 9, 10).
* The digest records that pairs with min E >= 11 exist in large numbers (2,652 among 28 lattices, thousands in
  lattice 003) and are excluded only by the frame search; no lemma T22 exists.

## 1. RESULT 1: a short vector is forced, by modular forms (no lattice list, no frame search)

**Statement.** Let (U; y1, y2) be as in Theorem R. Then some v in U outside J has E(v) <= 12.
Equivalently: there is a sigma-odd integer (-4)-eigenfunction whose sum of squares over the 49 orbits is at most 12.

**Consequence.** NOT-EX follows from Theorem R, this statement, and five lemmas "no sigma-odd integer
(-4)-eigenfunction with sum of squares E" for E = 8, 9, 10, 11, 12. The first three exist (T16, T18, T20); the last
two (they would be T22 and T24) do NOT exist. With them, the pass over the 156 lattices would not be needed at all.
So this is a change of architecture, not yet a proof without computation.

**Proof structure.**
1. N = U n J^perp has rank 22, determinant 49, is odd, and its discriminant form is the anisotropic plane over F_7.
   The theta series of the cosets of its even sublattice form a vector-valued modular form of weight 11 for the Weil
   representation of A = A_2 + A_7 (A_2 = {0, o, s, s'} with q = 0, 1/2, 1/4, 1/4; A_7 = F_7^2, q = 3(x1^2 + x2^2)/7).
   Coarse model: components symmetric under -1 and under s <-> s' (integral vectors by class ((v,y1), (v,y2)) mod 7,
   shadow vectors summed over the two halves). Its dimension is **61** (`weil_dimension.py`; formula
   d + dk/12 - alpha(S) - alpha(ST) - alpha(T), checked on the trivial representation; the fine model has dimension 80).
2. Explicit elements: Theta_{Z^j; y} theta_3^c (16 Delta_8)^i and the same with a part of y in E8, with their shadows
   (Conway-Sloane rule, controlled on E8). 104 generators, rank 61 modulo two primes (`span_rank.py`,
   `forcing_exact.py`): they span the space. Every generator passes the test "the coefficient depends only on E and
   on the class".
3. Shadow condition, from the frame: for a characteristic vector z, the 42 products (z, u_o) are odd and the 7
   products (z, h_c) are even, and E(z) = 6 mod 8, so E(z) >= 46: **no shadow vector with E < 11.5**.
4. Exact linear algebra (`forcing_exact.py`, `extremal_form.py`, logs of 13/10): the forms with no integral
   coefficient at 1 <= E <= T and no shadow coefficient at E < 11.5 form a space of dimension 15, 11, 7, 3, 1 for
   T = 8, 9, 10, 11, 12. For T = 12 it is a line; normalised to constant term 1 its first coefficients are
       shadow, E = 11.5: -2 in each of the four classes;   integral, E = 13: -1 in each of the four classes;
       shadow, E = 13.5: 10;   integral, class 0, E = 14: -20;   integral, E = 15: 26.
   A theta series has non-negative coefficients: contradiction. Hence a vector with 1 <= E <= 12 exists.

**What is exact and what is not.** Step 4 is exact rational arithmetic. Step 2 is exact integer counting. The
dimension 61 of step 1 comes from eigenvalues computed in floating point and rounded to fractions; it agrees with the
rank of the generators, which never exceeds it. The identification "theta series of (U; y1, y2) lies in this space
with these coordinates" is the standard theory of theta series of cosets; I have not written it out line by line.
The statement is NOT in the sources searched (the two agent reports and a search of the C2 repositories for Jacobi
forms); that is not a proof of novelty.

**Without the shadow condition** (floating LP, `forcing_bound.py` with NOSHADOW=1): a vector with E <= 15 is forced.

## 2. FAILED sub-goal: forcing with the three existing lemmas only
Hope: the conditions "no integral vector with 1 <= E <= 10" + shadow would already be contradictory, so that T16, T18,
T20 and Theorem R would suffice. FALSE: the solution space has dimension 7 and contains non-negative tables
(`forcing_bound.py`, `forcing_region.py`); and the records already contain thousands of real pairs with min E >= 11.
In that region (floating LP): number of vectors with E = 11 between 0 and 34.7, with E = 12 between 0 and 52, with
E = 13 at least 16; shadow vectors with E = 11.5 between 12 and 96; norm-3 vectors of N between 592 and 696 (the
frame gives 84); roots of N between 0 and 84. So with the three lemmas, **at least 12 shadow vectors with E = 11.5
are forced**: sigma-odd eigenfunctions with values +-2 on one block, 0 on the other inner vertices and +-1 on all 84
outer vertices (a bipartition of the outer graph exchanged by sigma, each outer vertex having 4 neighbours on its
side and 8 on the other, except around the block). First-order counting of the lines against such a bipartition
closes (number of split outer lines between 123 and 140): no contradiction found by hand.

## 3. Facts re-derived today in passing (probably known; not checked against the old notes one by one)
* W = 2S + I satisfies W^2 = 49 I_49 (49 = size of the matrix only at m = 7).
* T = -N has spectrum 0^7 (the linear functions of the D7 roots), 3^20, (-4)^15; Q = B + 2D has 12, (-2)^6, 3^20, (-4)^15.
* (1/2) sum_c h_c lies in U (norm 7, orthogonal to y1, y2), because sum_c (v,h_c) is even for every v of U.
* The involution is the "opposite corner" map of the vertex chart at its fixed vertex.

## 4. What remains for a proof without computation, in order of what I would try
1. Prove or kill the two missing lemmas (E = 11, 12) by an argument uniform in E (the existing T18, T20 are long and
   partly enumerations; a uniform argument for 8 <= E <= 12 is not known).
2. Or find a further frame-forced condition on the coefficient table that the thousands of real pairs with
   min E >= 11 violate; the shadow condition was of that kind and moved the bound from 15 to 12.
3. Or exclude by hand the forced characteristic eigenfunctions of section 2.

## 5. Process log (for the later comparison with the campaigns)
* The idea came from reading Theorem R as "a lattice of small level with a lower bound on a quadratic form" and
  counting conditions against the dimension of the space of modular forms, not from the graph.
* The first target ("forcing with the existing lemmas") was refuted within the hour by a sub-agent's digest of the old
  proof; the same machinery then gave the weaker true statement of section 1.
* An error made and caught on the way: I used the shadow rule with theta_4(tau) instead of theta_4(2 tau); the
  table showed shadow exponents of the wrong parity, and the control on E8 fixed it. A second one: I first read the
  threshold-12 result as "only the zero form" from a floating rank; the exact rank is 60, the space is a line, and the
  contradiction is the sign of its coefficients.

Files: `weil_dimension.py`, `jacobi_tables.py`, `jacobi_e8.py`, `span_rank.py`, `forcing_exact.py`, `extremal_form.py`,
`forcing_bound.py`, `forcing_region.py`, `forcing_lp.py` (first version, kept), logs `forcing_exact_2026-10-13.log`,
`extremal_form_T12_2026-10-13.log`; agent reports `INVENTORY_C2_CAMPAIGNS.md`, `DIGEST_T16_T18_T20_ENGINE.md`.
