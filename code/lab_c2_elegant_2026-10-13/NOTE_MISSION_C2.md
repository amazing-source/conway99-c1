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
In that region (floating LP; numbers of PAIRS +-v, see the correction in 6.2): vectors with E = 11 between 0 and 34.7, with
E = 12 between 0 and 52, with E = 13 at least 16; shadow vectors with E = 11.5 between 12 and 96; norm-3 vectors of N between 592 and 696 (the
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

## 6. Addendum, 13 October 2026, 20:29 UTC

### 6.1 Independent control of the 61-dimensional space (passed)
`validate_d12.py`, log `validate_d12_2026-10-13.log`: the coefficient table of a lattice of another kind,
U = D12+ + Z^12 with y1 = ((1/2)^12; 1,1,1,1), y2 = ((1/2)^6, (-1/2)^6; 1,1,-1,-1), computed by direct enumeration
(with the shadow of D12+), lies in the span of the generators: 125 table entries tested, rank 61 before and after.
The generators use only Z^j and E8, so this tests the dimension, the labelling of the classes and the shadow rule.

### 6.2 RESULT 2: exact identities once the three existing lemmas are used
Assume Theorem R, the shadow condition, and no integral vector with 1 <= E <= 10 (lemmas A.5, T16, T18, T20).
Then every total below is an affine function of TWO numbers (`exact_identities.py`, exact rationals, log
`exact_identities_T10_2026-10-13.log`):
   n11 = number of integral vectors with E = 11,     s = number of shadow vectors with E = 11.5.
With I(E), S(E) the numbers of integral and shadow vectors (one per class representative) and I0 = class 0 only:

    I(12) = 4 - n11 + s/2          I(13) = 8 - n11 + 3s/2        S(13.5) = 48 - 2 n11 + s
    I0(14) = s - 12                I(15) = 96 - n11 - s          S(15.5) = 240 + 6 n11 - s
    I(16) = 164 + 2 n11 + s        I(17) = 312 + n11 + s/2       S(17.5) = 224 - 4 n11
    I(18) = 592 + 4 n11 - 2s       I(19) = 1040 - 4 n11 - s      S(19.5) = 2656 - 4 n11 - s
    I(20) = 1716 - 3 n11 - 5s/2    I0(21) = 688 + 2 n11 - s

I0(14) is the number N_2 of roots of U orthogonal to y1, y2. So **s = 12 + N_2 >= 12**. CORRECTION (13/10, 20:49 UTC):
the totals I(E), S(E), n11, s count ONE class of each pair of opposite classes, i.e. they are numbers of PAIRS +-a
(I0 alone counts both signs). So at least TWELVE pairs +-a of
"characteristic" eigenfunctions a = (+-2 on one block, 0 on the six others; +-1 on all 42 outer orbits), of sum of
squares 46. Equivalently: a choice of one vertex in each outer orbit such that the 42 chosen vertices induce a graph
of degree 4, except 3 vertices of degree 3 and 9 of degree 5 around one block. In that gauge N 1 = 4.1 + 2 eps R e_c.
Other consequences: n11 <= 56, n11 + s <= 96, n11 <= 4 + s/2 (from I(12) >= 0).
These identities are specific to 7 (they come from the rank-24 envelope): they are equations of the kind the trace
and moment campaigns could not produce (inventory, class "trace, moment and counting identities").

### 6.3 What the records say about this region (sub-agent report `KILL_STATISTICS_156.md`)
* 135 of the 156 lattices have pair-level records (600,910,595 ordered pairs); by the first rule that fired:
  characteristic trap 45.0 %, swap-covered 41.0 %, twin bookkeeping 6.1 %, "stage 1 empty" 4.3 %, E = 8 witness 2.2 %,
  T18 0.9 %, T20 0.4 %. The characteristic trap is the shadow condition used here.
* Among the 28 lattices with a lemma-only census, 2,652 pairs have no witness with E <= 10; 1,610 of them violate
  the characteristic trap; the 1,042 others lie in the region of 6.2 and are closed by the frame search, almost all
  at its FIRST stage: "no 7 h" (no seven orthogonal vectors of norm 4 hitting every shadow root as required).
* So in the old proof the frame search is, in practice, the search for the seven vectors h. The lattices of the
  region of 6.2 do not even contain the heptad.

### 6.4 Next step chosen
Put the heptad into the modular argument: Jacobi forms whose index contains H+ = sum Z h_c + Z (1/2) sum h_c next to
J, symmetrised under the signed permutations of the h_c. The frame forces, for every shadow vector b,
E(b) >= 10.5 + sum_c (b,h_c)^2 with sum_c (b,h_c) odd, which is stronger than the condition used so far for every
class type except one. If the resulting linear system is infeasible with the three lemmas (or with A.5 alone), NOT-EX
follows without the lattice list and without new lemmas. Cost: a larger space (a few hundred dimensions by a rough
count) and generators with half-integer coordinates (E8, D12+ blocks) so that odd products with the h_c occur.
Not done yet. A cheaper first probe: one vector h only (index J + <4>).

## 7. Step 2, first probe: one vector h of the heptad in the index. NEGATIVE (13 October 2026, 20:49 UTC)

Model: Jacobi forms in three variables for (U; y1, y2, h), h of norm 4 orthogonal to y1, y2 (`heptad1.py`); table
entries indexed by the class ((v,y1), (v,y2)) mod 7, (v,h) mod 4 and D = 4E - 7 (v,h)^2.
* Generators: 449 patterns in Z^j and 560 with a part in E8 (`heptad1_gen.py`, `heptad1_e8.py`): rank 234, stable
  over the last 300 generators. No dimension formula computed for this space; control: the table of
  (D12+ + Z^12; y1, y2, h) obtained by direct enumeration lies in the span (`validate_d12_h.py`, 485 entries tested).
* Conditions on the AVERAGE of the seven tables (one per h_c), all linear (`heptad1_lp.py`): N, I (E <= 10), the
  refined shadow condition E >= 10.5 + t^2 + [t even] for t = (b,h), positivity, and the three conditions coming
  from the sum over the seven orthogonal vectors (H1: sum of t^2 <= E - 10.5 on shadow vectors; H2: at least one odd
  product; H3: sum of t^2 <= 4E/7 and even on integral vectors).
* Verdict (floating LP): FEASIBLE at T = 10. The ranges of the totals are exactly those of the model without h
  (pairs with E = 11: 0 to 34.7; shadow pairs with E = 11.5: 12 to 96; E = 13: at least 16). The only effect of the
  heptad rows is on the distribution of t (for instance shadow vectors with E = 11.5 and t = +-1: one seventh).
* Reading: second moments of the products with the h_c carry no information beyond the model of section 1.
  If the heptad obstructs, it is through the JOINT distribution of the seven products (index J + H+, nine variables),
  which this probe does not see. Not computed.

## 8. A tempting idea that is NOT new information (13 October 2026, 21:09 UTC; nothing computed)
Idea: mark a minimal characteristic vector z (norm 8, E(z) = 46, forced by section 6.2) as a third elliptic variable.
Its eigenfunction a_z has entries +-1 on the 42 outer orbits and +-2 on one block, so for every v of U
|E(v,z)| = |<a_v, a_z>| <= 2|a_c| + sum_o |a_o| <= E(v) (an l1 bound; the parity of sum_c a_c removes the value E + 1).
This looks like about forty new vanishing conditions in a space of about 135 dimensions.
It is not: every shadow vector is b = v + z/2 with v in U, and E(b) = E(v) + E(v,z) + 11.5, so the shadow condition
"E(b) >= 11.5 for all b" IS "|E(v,z)| <= E(v) for all v". The l1 bound is the characteristic trap rewritten. The real
lattices of the region of 6.2 have such vectors z and satisfy it. Model not built. General lesson: any condition that
only involves y1, y2 and vectors the real lattices of that region already have cannot exclude them; what excludes
them in the records is the absence of the seven vectors h.

## 9. Where the obstruction must be, and what is running (13 October 2026, 21:15 UTC)
* Everything that involves only y1, y2 (section 1), one vector h with averaged heptad conditions (section 7), or a
  minimal characteristic vector (section 8) is satisfied by real lattices of the region of 6.2, or adds nothing.
  In the records these lattices are excluded because the seven vectors h do not exist in them.
* So the next information needed is concrete: in a real region pair, WHY is there no heptad? (how many norm-4 vectors
  orthogonal to y1, y2 are admissible, how they hit the s pairs of minimal shadow vectors, what the largest orthogonal
  admissible set is). A sub-agent is extracting this from the stored lattices for a few region pairs, and at the same
  time checks the identities of 6.2 on them (report expected in `region_pairs/REGION_PAIRS_REPORT.md`).
* In parallel an Opus sub-agent rereads T16, T18, T20, tries to shorten and link them, and attacks E = 11, 12 and the
  characteristic eigenfunctions (report expected in `LEMMAS_AGENT_REPORT.md`).
* Not started: the nine-variable model (index J + H+). A second-moment (Venkov-type) variant with one frame vector u_o
  was considered and not built: the one-h probe suggests single-vector refinements do not cut.

## 10. Report of the Opus sub-agent on the lemmas (13 October 2026, received 21:42 UTC): `LEMMAS_AGENT_REPORT.md`
Not reread line by line by me; its own labels are kept.
* NOT obtained: T22, T24, the exclusion of the characteristic eigenfunctions; no machine step of T16, T18, T20 was
  replaced by a hand argument. No error found in the parts of the three proofs it read line by line.
* PROVED there (hand): for E <= 12 every entry of an eigenfunction is 0, +1 or -1 (one proof for the five sizes); a
  common skeleton for every size (active inner orbits k <= 2E/5, three identities, a parity law, the possible pairs
  (k, e)); two real shortenings (E = 8: the case k = 2 in two lines; E = 9: one identity replaces two lemmas of T18);
  the sizes split into two families modulo 7, {8, 9, 11, ...} and {10, 12, 13, ...}, so a proof for 11 may use T16 and
  T18, a proof for 12 only T20.
* Where the old method stops: for (k, e) = (0, 0) there are 23 orbit graphs left at E = 11 and 168 at E = 12, plus
  the other pairs (k, e); T20 had 6 such graphs and needed about 17 million configurations. So T22 and T24 by the
  method of T20 are machine enumerations, larger than T20's.
* One rigid sub-case recorded at E = 12: an equitable partition of the 99 vertices of sizes (24, 60, 15) with
  quotient [[4,10,0],[4,7,3],[0,12,2]]; not excluded.
* A useful rewording of section 6.2: I(12) = 4 - n11 + s/2 and s = 12 + N_2 give
      (pairs of eigenfunctions of size 11) + (pairs of size 12) = 10 + N_2/2 >= 10.
  So, with T16, T18, T20, AT LEAST TEN PAIRS +-a of eigenfunctions of size 11 or 12 must coexist in the graph (in the
  classes seen by the envelope); "at most nine" would close C2.
