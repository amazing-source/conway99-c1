# Small sigma-odd eigenfunctions, 8 <= E <= 12: common skeleton, new lemmas, and where E = 11, 12 stop

Agent report, 13 October 2026. Own derivations and own code of this session; nothing here was audited by a third party.
Labels: PROVED (complete proof written below), CHECKED (computation, exact scope stated), CONJECTURE, FAILED (with the reason).

## 0. Result in one page

**Not reached:** the lemmas for E = 11 and E = 12 ("T22", "T24") are NOT proved, and the characteristic eigenfunctions are NOT
excluded. No machine step of T16, T18 or T20 was replaced by a hand argument (one hand step of T16 is shortened, S16 below).

**What is proved here (all by hand, complete proofs in sections 2 to 6):**

| # | Statement | Status | Where |
|---|---|---|---|
| L1 | For E <= 12 every entry of a is 0, +1 or -1. In particular the patterns 4+7 = 11 and 4+8 = 12, 4+4+4 = 12 do not occur. One proof for all of 8 <= E <= 12; it replaces Prop. 3.1 of T18 and Lemmas 3.1, 3.2, Prop. 3.3 of T20. | PROVED (uses A.5) | 2 |
| L2 | k (number of active inner orbits) is even and k <= 2E/5: k in {0,2} for E = 8, 9 and k in {0,2,4} for E = 10, 11, 12, with the numbers n_c. | PROVED (same proof as T18 4.2 / T20 4.1, any E) | 3.1 |
| L3 | Counting identities (I1), (I2), (I3) for every E, the parity law e = C(k,2) mod 2, the bound d(z) <= 2E/5 outside the support, the list of possible (k, e): four pairs for E = 11, six for E = 12. | PROVED | 3.2-3.4 |
| S16 | A shortening of T16: at E = 8 the case k = 2 is excluded by the parity law in two lines (the dossier uses a page, lines 120-170 of `LEMME_EGALITE_8_SUR_7_C2.txt`). | PROVED | 3.4 |
| L4 | For k = e = 0: the class sizes n_0, n_1, n_2 as functions of n_3, n_4 for every E; n_4 = 0 for E = 11; at E = 12, n_1 = 3 n_3 + 8 n_4, and if n_3 = n_4 = 0 the partition (support, X_2, X_0) = (24, 60, 15) is equitable with quotient matrix [[4,10,0],[4,7,3],[0,12,2]]. | PROVED | 3.5, 3.6 |
| L5 | The dual-norm rule of the project (NOTES H6, T20 Lemma 10.2) for every E, with its congruence: the sizes split into two families, {8, 9, 11, 15, 16, 18, ...} and {10, 12, 13, 17, 19, 20, ...}. Through this rule T18 may use T16; a proof of E = 11 may use T16 and T18; a proof of E = 12 may use T20 only. Explicit consequences, e.g. at E = 11 every 5 support orbits span at least 2 edges of the orbit graph B. | PROVED (the rule itself is not new; the general form and the two families are what is added) | 4 |
| L6 | Characteristic eigenfunctions: the chosen set P induces (cubic graph) + (perfect matching) away from the block; the line counts close with one free odd parameter; a characteristic eigenfunction lies in the family of E = 11; five chosen vertices forming a "clean pentagon" would give an eigenfunction of size 11. | PROVED (structure only; no exclusion) | 6 |

**What is computed (microscope, not proof steps), section 5.3:** for k = e = 0 the orbit graph B is a 4-regular graph on E
vertices with all codegrees <= 2. Number of isomorphism classes: 2, 3, 6, 33, 211 for E = 8, 9, 10, 11, 12 (the first three
agree with T16, T18, T20). The dual-norm rule on the support alone kills nothing for E = 8, 9, 10 (as NOTES H6 found for
E = 10), but it kills 10 of the 33 classes at E = 11 (they would contain an eigenfunction of size 8 or 9) and 37 of the 205
positive semidefinite classes at E = 12 (size 10). Left: 23 classes at E = 11, 168 at E = 12. One level further (support
plus the inner orbits, partial sample for one graph at E = 11) the rule kills only 8 of 1,500 configurations: no sign that
it collapses the search. Control on the 243-vertex graph: the uniform identities hold there (section 10).

**Where it stops (section 5.4):** after L1-L5 the two missing lemmas are reduced to a finite list of support types: for
k = e = 0, 23 orbit graphs at E = 11 and 168 at E = 12, against 6 in T20 (which already needed about 17 million
configurations), plus three, resp. five, other pairs (k, e). I found no uniform argument that replaces the extension
search, and no hand proof of any single case. The smallest additional statements that would close C2 are in section 7.

**Errors in the existing proofs:** none found in the parts I read line by line (T16: the three dossier texts in full; T18:
sections 2 to 5; T20: sections 3 to 4.8). Two presentation remarks are in section 8. I did NOT reread T18 sections 6-8 nor
T20 sections 5-10; for them I rely on the digest, which is a reading aid and not a check.

---

## 1. Setting and notation

Sources read first: `MODEL.md`; `lemma/upstream/AUDIT_REDUCTION.md` A.0-A.9; `NOTE_MISSION_C2.md`; the inventory of campaigns.
Everything below is derived from the following facts of A.1-A.3 and A.5 (hand proofs in that file), which I use as given.

- (F1) S = [[-I_7, C],[C^t, T]] is symmetric, S^2 + S = 12 I. An inner row c has diagonal -1 and exactly 12 other non-zero
  entries, +-1 (the 12 outer orbits "touching" the block c). An outer row o has diagonal 0 and exactly 12 non-zero entries,
  +-1 (2 in C, 10 in T). Every column of C has two non-zero entries, so its sum is 0 or +-2.
- (F2) H := 3I - S satisfies H^2 = 7H. K := {a in Z^49 : S a = -4 a} = {a : H a = 7 a}. For every i the vector H e_i lies in
  K, and for a in K: (a, H e_i) = 7 a_i, (H e_i, H e_j) = 7 H_ij; in particular |H e_o|^2 = 21 (outer), |H e_c|^2 = 28 (inner).
- (F3) Lift: a in K is the same thing as a sigma-odd integer function phi on the 99 vertices with A phi = -4 phi; the value of
  the orbit o is phi at the representative with label the column o of C, and E := |a|^2 = (1/2) sum phi^2. In the graph:
  N(x) is seven blocks {c+, c-}; an outer vertex has exactly two inner neighbours, in two different blocks; outer mates are
  not adjacent; for an outer u, N(u) n N(sigma u) is one outer orbit; lambda = 1, mu = 2. For an outer orbit o touching the
  block c, exactly one vertex of o is adjacent to c+, and C_co a_o = phi(that vertex).
- (F4) sum_c a_c is even for a in K. (Inner rows: C a_out = -3 a_in; multiply by the all-ones row: the left side is even.)
- (F5) = A.5: K has no non-zero vector with |a|^2 <= 7.

For a in K with entries 0, +-1 and E = m non-zero entries: P = S+ = {phi = 1}, Q = S- = sigma P, S = P u Q; d+(v), d-(v) =
numbers of neighbours of v in P, Q; for v outside S, d(v) := d+(v) = d-(v); k = d(x) = number of active inner orbits;
e = number of edges inside P; Q2 := sum over P of d+^2 (the "Q" of T18 and T20); X_d = {z outside S : d(z) = d}, n_d = |X_d|.
"Gauge": choose as representative of each support orbit its vertex in P; then a = 1_P and, for i, j in the support,
-S_ij = [p_i ~ q_j] - [p_i ~ p_j] (q_j = sigma p_j).

---

## 2. L1: for E <= 12 the entries are 0, +1, -1  (PROVED)

**Lemma 1.** Let a in K, a != 0, E = |a|^2 <= 12. Then every entry of a is 0, +1 or -1.

*Proof.* Step 1, outer entries. Let o be outer with |a_o| >= 2. Then E - 14 |a_o| + 21 is the squared norm of
a - sign(a_o) H e_o, a vector of K (F2: |a|^2 - 2 sign(a_o)(a, H e_o) + |H e_o|^2 = E - 14 |a_o| + 21). For |a_o| = 2 this is
E - 7, an integer between 1 and 5 (E >= 8 by F5): a non-zero vector of K of norm <= 5, against (F5). For |a_o| >= 3 it is
<= E - 21 < 0, impossible. So outer entries are 0, +-1.

Step 2, inner entries. Let c be inner with |a_c| >= 2; replace a by -a so that a_c > 0. The inner row gives
sum_o C_co a_o = -3 a_c (F1), a sum of at most 12 terms +-1 by step 1. If a_c >= 3 at least 9 outer entries are non-zero and
E >= 9 + 9. So a_c = 2. Let O- (resp. O+) be the set of outer orbits o touching c with C_co a_o = -1 (resp. +1). Then
|O-| - |O+| = 6 and |O-| + |O+| <= E - 4 <= 8, so (|O-|, |O+|) is (6,0) or (7,1).

*(7,1) is impossible.* Then E = 12 and the support is c and eight outer orbits, all touching c. A block c' != c has a_c' = 0, so
sum_o C_c'o a_o = 0; only two outer orbits touch both c and c' (labels e_c + e_c' and e_c - e_c' up to order), so either none
or both are in the support. Hence four blocks c' have both. For such a c' let a_1, a_2 be the two entries; the row c' reads
+-a_1 +- a_2 = 0 and the two orbits contribute C_c,1 a_1 + C_c,2 a_2 to the row c. With the columns e_i + e_j, e_i - e_j (i < j):
if c < c' the row c' gives a_1 - a_2 = 0 and the contribution to the row c is a_1 + a_2 = +-2; if c' < c the row c' gives
a_1 + a_2 = 0 and the contribution is a_1 - a_2 = +-2. So sum_o C_co a_o is a sum of four terms +-2, which is 0, +-4 or +-8, never -6.

*(6,0) is impossible.* The remaining entries have squares summing to E - 10 <= 2: at most two more support orbits, each with
entry +-1, none of them touching c (those touching c are the six of O-). By (F4) the number of odd inner entries is even, so
the extra orbits are: none (E = 10); one outer (E = 11); two outer, or two inner (E = 12). Two inner extra orbits c_1, c_2 would
each need at least three outer support orbits touching them (row c_1: sum = -3 a_c1), but the outer support is O-, whose orbits
touch c and one other block, and only two orbits touch both c and c_1. So every extra orbit is outer and does not touch c.

In the graph (F3): phi(c+) = 2, phi(c-) = -2; the six orbits of O- have their vertex adjacent to c+ at value -1. Let Q_c be
these six vertices (neighbours of c+) and P_c = sigma Q_c (six neighbours of c-, value +1). All other inner vertices have value 0.

- E = 10. Take u in P_c. Its inner neighbours are c- (value -2) and one vertex of value 0; the non-zero outer vertices are
  P_c u Q_c. The eigen-equation at u reads -2 + d+(u) - d-(u) = -4, so d-(u) = d+(u) + 2 >= 2, where d- counts neighbours in Q_c.
  But u is not adjacent to c+ (its two inner neighbours lie in different blocks), so u and c+ have exactly two common
  neighbours; one is c-, and x is not adjacent to u; so u has exactly one neighbour among the 12 outer neighbours of c+, and
  Q_c is contained in them: d-(u) <= 1. Contradiction.
- E = 11 or 12. Let p be the vertex of value +1 of an extra orbit. It is outer and adjacent to neither c+ nor c-, so its two
  inner neighbours have value 0 and the eigen-equation at p reads d+(p) - d-(p) = -4, i.e. d-(p) >= 4 (outer vertices only).
  The outer vertices of value -1 are Q_c, sigma p, and (if E = 12) one vertex of the second extra orbit. p is not adjacent to
  sigma p (outer mates). And p is not adjacent to c+, so p and c+ have exactly two common neighbours, hence p has at most two
  neighbours in Q_c. So d-(p) <= 2 + 0 + 1 = 3 < 4. Contradiction.   QED

*Remarks.* (1) The case E = 10 of the proof is Lemma 3.2 of T20 (same idea, shorter); the cases E = 11, 12 are new. (2) The
proof uses the fixed vertex only through (F3) and uses (F5) only in step 1. (3) It is a local statement; I do not claim an
analogue at 11 blocks, where the row sums and the thresholds are different (eigenvalue -5, 20 outer neighbours of an inner
vertex): it does not conflict with the Berlekamp-van Lint-Seidel graph.

**Consequence.** For 8 <= E <= 12 a sigma-odd integer (-4)-eigenfunction of size E is a pair (P, Q = sigma P) of disjoint
E-sets with d-(v) = d+(v) + 4 on P and d+(v) = d-(v) off P u Q. So "T22" and "T24" are statements about 11 or 12 orbits with
values +-1, exactly like T16, T18, T20.

---

## 3. L2-L4: the hand skeleton common to T16, T18, T20, written for every E = m

In this section a in K has entries 0, +-1 and m = E non-zero entries (8 <= m <= 12 in the applications).

### 3.1 Active inner orbits (PROVED; T18 Lemma 4.2 and T20 Lemma 4.1 for every m)

For a block c let n_c be the number of support orbits among the 12 outer orbits touching c. The inner row gives
sum_o C_co a_o = -3 a_c, so n_c is odd and >= 3 if c is active, even otherwise. Each outer support orbit touches two blocks:
sum_c n_c = 2 (m - k). Hence k is even (F4, or parity of the sum) and 3k <= 2(m - k): **k <= 2m/5**.
k in {0, 2} for m = 8, 9; k in {0, 2, 4} for m = 10, 11, 12.

### 3.2 Three identities and the parity law (PROVED; T18 Lemmas 4.4, 4.5 and T20 Lemmas 4.2, 4.4 for every m)

Sums over the 99 - 2m vertices z outside S (x included, d(x) = k):

    (I2)  sum d(z) = 10 m - 4 e
    (I1)  sum C(d(z), 2) = m (m - 7) - 7 e - Q2
    (I3)  sum C(d(z) - 1, 2) = m^2 - 19 m + 99 - 3 e - Q2            ( = n_0 + n_3 + 3 n_4 + 6 n_5 + ... )

*Proof.* (I2): a vertex of P has d+ neighbours in P, d+ + 4 in Q, so 10 - 2 d+ outside S. (I1): the pairs of P have
m(m-1) - e common neighbours in all (1 for an adjacent pair, 2 otherwise); a vertex v contributes C(d+(v), 2); for v in P and
its mate in Q this is C(d+,2) + C(d+ + 4, 2) = d+^2 + 3 d+ + 6, total Q2 + 6e + 6m. (I3) = (I1) - (I2) + (99 - 2m).  QED

m^2 - 19 m + 99 = 11, 9, 9, 11, 15 for m = 8, 9, 10, 11, 12 (it is never 0: the equality argument of A.5 has no analogue).

**Parity law:** e = C(k, 2) (mod 2). *Proof.* The vertices z != x outside S are paired by sigma with equal d, and d(x) = k;
so the left side of (I1) is congruent to C(k,2). m(m-7) is even and Q2 = sum d+ = 2e = 0 (mod 2).  QED

**Bound on e:** Q2 >= 2e, so (I3) gives 5 e <= m^2 - 19 m + 99: e <= 2 (m = 8, 11; and e = 0 for m = 8 by (I1)), e <= 1
(m = 9, 10), e <= 3 (m = 12). For m = 9 this replaces Lemma 4.3 (spectral bound e <= 2) and Lemma 4.6 (e != 2) of T18 by
the one identity (I3), which T20 introduced for m = 10.

### 3.3 The path count and d(z) <= 2m/5 (PROVED; T18 Lemma 5.1 for every m, without assuming e = 0)

Let z be outside S, d = d(z). Count the pairs (w, s), s in P, w a common neighbour of z and s. By s: d + 2(m - d) = 2m - d.
By w: sum over the neighbours w of z of d+(w); a neighbour w in Q has d+(w) = d-(sigma w) = d+(sigma w) + 4 >= 4. Hence
2m - d >= 4d: **d(z) <= 2m/5 for every vertex outside the support** (3, 3, 4, 4, 4 for m = 8..12). If k = e = 0 the count is
exact: the sum of d(w) over the neighbours w of z outside S is 2m - 5d.

Example: at m = 12 a support equal to the 12 orbits touching one block c is impossible, because then d(c+) = 6.

### 3.4 The possible pairs (k, e) (PROVED)

From 3.1, 3.2 and one more remark: if k = 4, x contributes C(3,2) = 3 to (I3).

| m | (k, e) possible | comment |
|---|---|---|
| 8 | (0,0) only: (I1) gives 8 - 7e - Q2 >= 0, so e = 0, and then the parity law gives k = 0 | the dossier of T16 kills k = 2 by a page of case analysis instead |
| 9 | (0,0), (2,1) | T18 reaches the same list through Lemmas 4.3, 4.5, 4.6, then kills (2,1) by hand (Lemma 4.7) |
| 10 | (0,0), (2,1), (4,0) | T20: three cases, all three need the machine |
| 11 | (0,0), (0,2), (2,1), (4,0) | (4,2) is impossible: (I3) would give 11 - 6 - Q2 >= 3 with Q2 >= 4 |
| 12 | (0,0), (0,2), (2,1), (2,3), (4,0), (4,2) | |

**A shortening of T16 (PROVED).** For m = 8: e = 0 by (I1), so the left side of (I1) is 8; x contributes C(k,2) and the other
outside vertices an even number; so C(k,2) is even and k != 2. These two lines replace section 5 of
`LEMME_EGALITE_8_SUR_7_C2.txt` (lines 120-170, the matrix "with two diagonals"). The dossier's own proof is correct (section
8); it predates the parity law, which appears in T18 (Lemma 4.5) and is applied there to E = 9 only.

Further exact data, same method: m = 11, (0,2): Q2 = 4 (two disjoint edges), X_0 = {x}, n_3 = n_4 = 0.
m = 11, (4,0): the path count at x gives sum over the three inactive blocks of n_c = 2, so (n_c) = (3,3,3,3 | 2,0,0).
m = 12, (2,3): Q2 = 6 (three disjoint edges) and n_0 = n_3 = n_4 = 0.

### 3.5 Class sizes when k = e = 0 (PROVED)

With d <= 4 (3.3), the three identities give, for every m:

    n_2 = m (m - 7) - 3 n_3 - 6 n_4,     n_1 = 2 m (12 - m) + 3 n_3 + 8 n_4,     n_0 = m^2 - 19 m + 99 - n_3 - 3 n_4.

| m | n_0 | n_1 | n_2 | known restriction |
|---|---|---|---|---|
| 8 | 11 - n_3 | 64 + 3 n_3 | 8 - 3 n_3 | n_3 = 0 (T16, hand) |
| 9 | 9 - n_3 | 54 + 3 n_3 | 18 - 3 n_3 | n_3 = 0 (T18 Thm 5.3, hand) |
| 10 | 9 - n_3 - 3 n_4 | 40 + 3 n_3 + 8 n_4 | 30 - 3 n_3 - 6 n_4 | n_4 = 0 (as below: 6 neighbours in X_0, n_0 <= 3); n_3 in {0, 2} (T20 Lemma 9.2, hand) |
| 11 | 11 - n_3 - 3 n_4 | 22 + 3 n_3 + 8 n_4 | 44 - 3 n_3 - 6 n_4 | n_4 = 0 (below) |
| 12 | 15 - n_3 - 3 n_4 | 3 n_3 + 8 n_4 | 60 - 3 n_3 - 6 n_4 | none found |

**n_4 = 0 for m = 11** (PROVED). Let z be in X_4. Its 6 neighbours outside S have d-values summing to 22 - 20 = 2 (3.3), so at
least 4 of them are in X_0. The same holds for sigma z, and sigma z != z because d(x) = k = 0. So n_4 >= 2, n_0 <= 5, and two
4-subsets of a set of at most 5 elements meet in at least 3 elements: z and sigma z have three common neighbours.  QED

### 3.6 E = 12 is the balanced size (PROVED)

(I1) and (I2) give, for every m, sum over z outside S of d(z)(d(z) - 2) = 2 m (m - 12) - 10 e - 2 Q2. For m <= 12 this is <= 0
and the only negative term is d = 1. At m = 12 with k = e = 0 it reads n_1 = 3 n_3 + 8 n_4.

**Proposition.** Let m = 12, k = e = 0, n_3 = n_4 = 0. Then every vertex outside S has d = 0 or 2, and the partition
(S, X_2, X_0) of sizes (24, 60, 15) is equitable with quotient matrix

    [ 4 10  0 ]
    [ 4  7  3 ]      (eigenvalues 14, 3, -4).
    [ 0 12  2 ]

X_0 induces a 2-regular graph, one component of which is the triangle {x, c0+, c0-} for one block c0; the six other blocks
lie in X_2 (delta = 2), and none of the 12 support orbits touches c0.

*Proof.* A 1_S = 4 1_S + 4 1_{X_2} (a vertex of S has 4 neighbours in S; a vertex of X_2 has 2 + 2). Apply A and use
A^2 = 12 I - A + 2 J: 4 A 1_{X_2} = (12 I - A + 2J) 1_S - 4 A 1_S = 12 1_S + 48 1 - 5 A 1_S, so
A 1_{X_2} = 10 1_S + 7 1_{X_2} + 12 1_{X_0}. The rows follow from the degree 14. x is in X_0 and has two neighbours in X_0; they
form a sigma-invariant 2-subset of N(x), i.e. one block.  QED

I could not exclude this configuration by hand (interlacing, the matchings in the neighbourhoods and the line counts are all
consistent with the quotient matrix). It is recorded because it is the most rigid sub-case of E = 12.

---

## 4. L5: the dual-norm rule for every E, and the two families of sizes

**The rule is not mine.** It is "H6" of `lemma/t20_HAND/NOTES.md` and Lemma 10.2 of T20_PROOF.md (lab session and Codex,
7 October), stated there for E = 10, "conditional, not used", with the remark that at E = 10 it depends on A.5 only and that
"the test does not fire" on the support. What follows is the same rule for every E, and what changes with E.

**Lemma 5 (PROVED).** Let a in K with |a|^2 = m, k an integer, c in Z^49. Then w = k a - H c is in K and

    |w|^2 = k^2 m - 14 k (a, c) + 7 c^t H c,          |w|^2 = k^2 m  (mod 7).

If 7 does not divide m and 7 does not divide k, then w != 0. If c is supported on the support of a, in the gauge a = 1_P:
|w|^2 = 7 (c - (k/7) 1)^t H_PP (c - (k/7) 1), with H_PP = 3I - S_PP (so only the support structure enters).

*Proof.* (F2). If w = 0 then k^2 m = |H c|^2 = 7 c^t H c is divisible by 7. The last formula is the expansion, using
H_PP 1 = 7 1.  QED

**The two families.** The squares mod 7 are 1, 2, 4. So the non-zero classes k a + H Z^49 of one vector a carry the sizes
m, 4m, 2m (mod 7):

| m | sizes possible in the classes k = +-1, +-2, +-3 (mod 7) |
|---|---|
| 8 | 1, 4, 2: {8, 15, ..}, {4, 11, 18, ..}, {2, 9, 16, ..} |
| 9 | 2, 1, 4: {9, 16, ..}, {1, 8, 15, ..}, {4, 11, ..} |
| 11 | 4, 2, 1: {11, 18, ..}, {2, 9, 16, ..}, {1, 8, 15, ..} |
| 10 | 3, 5, 6: {10, 17, ..}, {5, 12, ..}, {6, 13, ..} |
| 12 | 5, 6, 3: {12, 19, ..}, {6, 13, ..}, {3, 10, 17, ..} |
| 46 (characteristic) | 4, 2, 1: {11, 18, .., 46}, {9, 16, ..}, {8, 15, ..} |

Hence (PROVED, by Lemma 5 and the lemma named in each line):
- m = 9: |2a - Hc|^2 is never 8 (T16), so it is >= 15; |3a - Hc|^2 >= 11 (A.5). **T18 may use T16.**
- m = 11: |2a - Hc|^2 >= 16 (T18) and |3a - Hc|^2 >= 15 (T16). **A proof of E = 11 may use T16 and T18.**
- m = 12: |2a - Hc|^2 >= 13 (A.5) and |3a - Hc|^2 >= 17 (T20). **A proof of E = 12 may use T20.**
- m = 10: only A.5 can be used (this is the remark of Codex). m = 8: A.5, and T18 for the classes of +-3a (size 9; T18
  does not depend on T16).
- A characteristic eigenfunction is in the family of 8, 9, 11.

**Explicit consequences (PROVED; each is one evaluation of the formula with c the indicator of a set I of support orbits, in
the gauge a = 1_P; j = |I|; for k = e = 0, c^t H c = 3j + 2 e_B(I), e_B(I) = number of edges of the orbit graph B inside I).**

1. m = 9. Two outer support orbits i, j with p_i ~ p_j and p_i not adjacent to q_j are impossible: H_ij = -1 and
   |2a - He_i - He_j|^2 = 36 - 56 + 28 = 8. (This is the first half of case A of T18 Lemma 4.7, in one line, from T16.)
2. m = 9, k = e = 0. B has no independent 4-set: |2a - Hc|^2 = 36 - 112 + 84 = 8. (True for B0, B1, B2: no gain.)
3. m = 11, k = e = 0. Every 5-set I has e_B(I) >= 2 and every 6-set has e_B(I) >= 4:
   |3a - Hc|^2 = 14 e_B(I) - 6 for j = 5 (value 8 if e_B = 1), |4a - Hc|^2 = 14 e_B(I) - 34 for j = 6 (value 8 if e_B = 3).
4. m = 12, k = e = 0. Every 5-set has e_B(I) >= 1 and every 6-set has e_B(I) >= 3:
   |3a - Hc|^2 = 14 e_B(I) + 3 for j = 5 (value 3: A.5), 14 e_B(I) - 18 for j = 6 (value 10 if e_B = 2: T20).
5. m = 11, k = 0, an edge p_i ~ p_j inside P with p_i not adjacent to q_j (so H_ij = -1). For every other support orbit l:
   |2a - He_i - He_j - He_l|^2 = 44 - 84 + 7 (9 - 2 + 2 (H_il + H_jl)) = 9 + 14 (H_il + H_jl). The value 9 is excluded by T18
   and a negative value is impossible, so **H_il + H_jl >= 1 for every l.** The rows of H_PP sum to 7, so the sum over the 9
   other orbits of (H_il + H_jl) is 10: eight of them have exactly one of p_i ~ q_l, p_j ~ q_l, and one has both (q_l is then
   the common neighbour of p_i and p_j). This describes the edges of the case (k, e) = (0, 2) at m = 11.

**What the rule does not do (FAILED as a route to a hand proof).** On the support alone it gives no contradiction for
m = 8, 9, 10 (computed, section 5.3; for m = 10 this is NOTES H6). I tried by hand to combine the support with one or two
orbits of X_2 for the complement of the Wagner graph (m = 8): every instance of the formula I evaluated is allowed (the
resulting conditions on B, such as "every 4-set containing V(z) and avoiding U(z) has two B-edges", hold in the Wagner
complement). So I have no hand replacement for the Wagner enumeration of T16.

---

## 5. E = 11 and E = 12: what is reduced, what is computed, where it stops

### 5.1 Reduction (PROVED, sections 2-4)

A sigma-odd integer (-4)-eigenfunction of size 11 or 12 has entries 0, +-1 (L1), k in {0, 2, 4} (L2), (k, e) in the list of
3.4, outside degrees d <= 4 (3.3), and satisfies the dual-norm inequalities of section 4 (with T16, T18 for E = 11; with T20
for E = 12).

### 5.2 The case k = e = 0 (PROVED reduction)

P and Q are independent, every vertex of P has exactly 4 neighbours in Q, and the orbit graph B (i ~ j iff p_i ~ q_j) is a
simple 4-regular graph on m vertices with all codegrees <= 2 (same proof as T18 Lemma 4.9: the common neighbours of p_i, p_j
inside S are the q_l with l adjacent to both). 3I + B and 4I - B are positive semidefinite (principal submatrices of H and
7I - H). The conditions of section 4 apply.

### 5.3 Microscope (CHECKED; scripts in `lemmas_agent/`, exact arithmetic for the tests)

`support_k0.py` (plain enumeration, m <= 11) and `support_k0_v2.py` (stronger normalisation, m <= 12) enumerate the labelled
4-regular graphs with codegrees <= 2 and reduce them to isomorphism classes by an exact canonical form;
`descent_singular.py` is a second implementation of the dual-norm test (rational elimination, Hermite normal form, short
vectors) that also treats the classes where 3I + B is singular. Scope: ONLY k = e = 0; ONLY the support (no outside
vertex); the dual-norm test looks for a vector of norm 1..min(m-1, 10) in the lattice Z a + sum_i Z H e_i (i in the support),
all such vectors, not only indicator vectors. (For m = 8 the size 9 is therefore not tested at this level; it is tested
in the level-two runs below, without effect.) Running time: 10 seconds for m = 12; one process; a few MB.

| m | isomorphism classes of B | with 3I+B, 4I-B positive semidefinite | killed by the dual-norm test | left |
|---|---|---|---|---|
| 8 | 2 (cube complement, Wagner complement) | 2 | 0 | 2 |
| 9 | 3 (B0, B1, B2 of T18) | 3 | 0 | 3 |
| 10 | 6 (I.0 - I.5 of T20) | 6 | 0 | 6 |
| 11 | 33 | 33 | 10 (norm 8: 3 classes; norm 9: 4; both: 3) | 23 |
| 12 | 211 | 205 | 37 (norm 10; 14 of them have 3I+B singular) | 168 |

Controls: the two enumerators agree for m = 8..11; the counts 2, 3, 6 are those of T16, T18 (Computation 4.10) and T20
(Computation 4.12, type I); the two implementations of the test agree on every class where both apply. The lists of the
classes left are in `support_k0_m11_survivors.txt` (23 lines) and `support_k0_m12_survivors.txt` (182 lines, of which the 14
marked SINGULAR are the ones killed afterwards by `descent_singular.py`; log `descent_singular_2026-10-13.log`).

Reading: at E = 11 the rule has real force already on the support (30 % of the classes die at once, each by an explicit
vector of size 8 or 9), which it does not have at E = 8, 9, 10. This is the family effect of section 4.

**One level further (CHECKED, partial sample only; `level2_labels.py`).** Support plus the seven inner orbits: the D7 labels
of the support orbits are enumerated up to the signed permutations of the blocks, under the budgets, then tested for
positivity (floating point, tolerance 1e-9) and by the dual-norm rule (exact). Each run is stopped after a fixed number of
tested configurations, so the counts are those of the first branches of the search, not of the whole list, and they are
not a statistical sample (log `level2_labels_2026-10-13.log`).
- m = 11, first of the 23 graphs: 2,866 label configurations, the 1,500 that pass positivity tested, **8** killed by the rule (188 s).
- m = 8 (both graphs) and m = 9 (first graph): 600 configurations tested each, none killed (for m = 8, 9 the size m itself is of course allowed).
So at this level the rule is weak again (0.5 % in the sample at E = 11). I have no evidence that it collapses the search for
E = 11; the force seen on the support does not persist one level up in this sample.

### 5.4 Where the argument stops

- For E = 11: the 23 orbit graphs of (k, e) = (0, 0), and the three other pairs (0,2), (2,1), (4,0). For E = 12: the 168
  orbit graphs of (0,0), and five other pairs. T20 has 6 + 1 + 2 = 9 support structures and needed about 17 million
  configurations and 16 million search nodes to close them. I have no argument that closes even one of the 23 graphs by hand.
- What a continuation by machine would look like (NOT launched, cost plan only): the search of T20 section 6.5 (orbits of
  X_2 placed one unit at a time) with the dual-norm rule as an additional exact rejection at every node (for E = 11 it
  uses T16 and T18). Whether the rule shortens that search is unknown: strong on the support, weak one level up in the
  sample of 5.3. The size to expect is therefore that of T20 multiplied by the number of base graphs (23 against 6 for
  E = 11, 168 against 6 for E = 12), i.e. of the order of 10^8 configurations for E = 11 and 10^9 for E = 12 if each
  graph behaves like a graph of T20; this is an extrapolation, not a measurement. It would be a computer proof, not
  the hand proof asked for.
- The equitable sub-case of 3.6 (E = 12, d in {0, 2} everywhere) is the place where I would look first for a hand
  argument at E = 12; I did not find one.

---

## 6. Characteristic eigenfunctions (structure PROVED; exclusion NOT reached)

Let a = (2 e_c ; eps), eps in {+-1}^42, S a = -4 a; phi its lift, P = the 42 outer vertices of value +1, Q = sigma P.

**6.1 Degrees (PROVED).** c+ has 3 neighbours in P and 9 in Q; every other inner vertex except c- has 6 and 6. An outer u in
P has 4 neighbours in P and 8 in Q if it is adjacent to neither c+ nor c-; 3 and 9 if adjacent to c+ (3 such vertices);
5 and 7 if adjacent to c- (9 such vertices). (Eigen-equation at each vertex.) So P has 87 inner edges and there are 330
edges between P and Q.

**6.2 Cubic graph plus perfect matching (PROVED).** For outer u, N(u) n N(sigma u) = {v, sigma v} is one outer orbit, and
exactly one of v, sigma v is in P. The map u -> (that vertex) is a fixed-point-free involution of P (if u ~ v and u ~ sigma v
then v ~ u and v ~ sigma u). So the graph induced on P is the union of a perfect matching and a graph that is cubic at the
30 vertices away from the block (degree 2 or 4 at the 12 others); equivalently, in the gauge eps = 1, every row of T away
from the block has three entries +1 and seven entries -1.

**6.3 The line counts close (PROVED; this is the "first-order counting" of the mission note, with its free parameter).**
Let N_PPP, N_PPQ be the numbers of outer triangles with 3, resp. 2 vertices in P, and I_PP the number of triangles
{inner vertex, u, u'} with u, u' in P. Every outer-outer edge lies in exactly one triangle, there are 140 outer triangles
and 84 triangles with one inner vertex, and sigma exchanges P and Q. So 2 N_PPP + 2 N_PPQ = 140, 87 = 3 N_PPP + N_PPQ + I_PP,
330 = 4 N_PPQ + 84 - 2 I_PP. The three equations have rank 2: N_PPP = (17 - I_PP)/2, N_PPQ = (123 + I_PP)/2. I_PP is odd
(consistent: the 12 ordinary inner vertices contribute an even number in sigma-pairs, and c+, c- contribute
e_PP(c+) + e_QQ(c+), which is odd because 2 e_PP + e_PQ = 3 and e_PP + e_PQ + e_QQ = 6). No contradiction: 1 <= I_PP <= 17.

**6.4 Family, and links with size 11 (PROVED).** |a|^2 = 46 = 4 (mod 7): by Lemma 5, |a - Hc|^2 is in {11, 18, 25, ...},
|2a - Hc|^2 in {16, 23, ...} (9 excluded by T18), |3a - Hc|^2 in {15, 22, ...} (8 excluded by T16). With c the indicator
(in the gauge) of a set I of j outer orbits and tau(I) = sum over the pairs of I of ([p_i ~ p_i'] - [p_i ~ q_i']):
|a - Hc|^2 = 46 + 7j - 14 tau(I). Examples: five vertices of P inducing a pentagon, with no edge from one of them to the
mate of another, give tau = 5 and an eigenfunction of size 11; four such vertices inducing a 4-cycle give size 18. So
"T22" forbids clean pentagons in P. The characteristic eigenfunctions and the eigenfunctions of size 11 belong to classes
of the same type (sizes 4 mod 7); I do not know whether they share a class.

**6.5 Two characteristic eigenfunctions (PROVED).** If a, a' are characteristic and a' != +-a, then (a + a')/2 and (a - a')/2
are in K, with sizes summing to 46. If their blocks differ these are eigenfunctions with entries 0, +-1 and k = 2, whose
outer supports partition the 42 outer orbits; so each has size >= 11 and the outer sign patterns of a and a' differ in at
least 9 and at most 33 orbits.

**6.6 Why I stopped.** Given the identities of the mission note (s = 12 + N_2 >= 12 once E <= 10 is excluded), every
hypothetical graph carries at least six pairs of characteristic eigenfunctions. So there is no local obstruction to look
for: a direct exclusion has to be a global statement about a bipartition of all 84 outer vertices, and any proof of it
is (given T16, T18, T20 and the modular argument) a proof of C2 itself. The degree counts and the line counts above are consistent;
the mod 2 class of a is always present in K (it is the characteristic class of K); the question is only whether that
class has a vector of norm 46 rather than 54 or more, and I found no handle on this minimum.

---

## 7. The smallest additional statements that would close C2 (given T16, T18, T20 and the mission note)

1. (T22 and T24) No eigenfunction with entries +-1 on 11 or 12 orbits. After this report: 23 + 168 orbit graphs for
   (k, e) = (0, 0), and the pairs (0,2), (2,1), (4,0) for E = 11; (0,2), (2,1), (2,3), (4,0), (4,2) for E = 12.
2. Weaker, and sufficient by the identities of the mission note as I read them (I(12) = 4 - n11 + s/2 and I0(14) = s - 12 >= 0
   give n11 + I(12) >= 10 in that note's counting): **"at most 9 eigenfunctions of size 11 or 12 in the classes seen by the
   envelope"** (i.e. at most four pairs +-a). I did not check the counting convention of the note (signs, classes), so this
   line is a reading, not a result.
3. Or: no characteristic eigenfunction (section 6), i.e. the characteristic class of K has minimum > 46.

---

## 8. The three existing proofs: what they share, where the machine is, remarks

**Common skeleton (all three, and now E = 11, 12 up to step 3).**
1. Values 0, +-1 (hand; here L1 for all sizes at once).
2. k, e, the identities (I1)-(I3), the parity law (hand; here section 3 for all sizes).
3. The support structure: the symmetric matrix B = A[P, sigma P] (symmetric because of sigma), its codegree bound. By hand
   at E = 8 (cube, Wagner). By machine at E = 9 (Computation 4.10: 1,024,380 labelled graphs, 3 classes) and E = 10
   (Computation 4.12: 9 structures). In my estimate the classification at E = 9 (three graphs) is small enough for a
   hand proof; I did not write one.
4. The classes X_d, the path count, the profile of N(x) (hand).
5. Extension of the support by the orbits of X_2 (and X_3, N(x)), each partial graph rejected exactly by a common-neighbour
   budget, a negative vector for M1 or M2 (positivity of the eigenprojectors), or, at a few nodes (the 4 survivors of B1 in
   T18, 16 nodes in T20, figures of the digest), the rank bound. Machine; this is where almost all the work is. Sizes as
   the texts and the digest give them: T16 672 tableaux; T18 some 10^4 matchings and tables per graph; T20 17,396,042
   configurations of N(x) and 15,762,181 search nodes for k = 0 alone.
What none of the three uses: the frame or lattice language (T18 and T20 say so explicitly), hence neither the dual-norm
rule nor an induction on E. T20 cannot gain from T16 or T18 through that rule (two families, section 4); T18 could have
used T16, and a proof of E = 11 can use both.

**Where each needs a machine, and whether I could replace it.**
- T16: only the Wagner complement (the 105 -> 31 -> 76 matchings, 640 + 32 tableaux, 6,544 candidates). Not replaced (section 4, last paragraph).
- T18: Computation 4.10 and everything after section 5.6. Not replaced. Lemma 4.7 case A, first half, is one line from T16 (section 4, item 1); this does not shorten the document in any significant way.
- T20: Computation 4.12 and sections 7, 8, 9.A, 9.B.6. Not replaced. Section 3 (two lemmas and a proposition) is covered by L1.

**Remarks on the texts (no error found).**
- T16, `LEMME_EGALITE_8_SUR_7_C2.txt` section 5 (k = 2 impossible): I rechecked every line of both cases; correct. It is
  also a consequence of the parity law (3.4), which the dossier does not use.
- T16, `C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt` lines 151-152 ("chaque sommet du support voit deux X_2 : la somme de ses
  déficits est 14 - 4*3 = 2"): terse but correct (count the pairs (w, s), s in P other than the vertex: 2*7 = 14, the four
  neighbours in Q give 3 each, an outside neighbour gives d(w) - 1).
- T20_PROOF.md line 302: "The proof uses only lambda = 1, mu = 2 and the eigen-equation." The proof of Lemma 3.2 also uses
  sigma (the mate, Lemma 2.1 (c)). Wording only; already noted in the digest.
- T18 sections 2-5 and T20 sections 3-4.8: every statement I rederived (in general form, section 3) agrees.

---

## 9. Attempts that failed, and why

1. **A uniform positivity or rank argument on the support.** For k = e = 0 the constraints on B are: 4-regular, codegrees
   <= 2, spectrum in [-3, 4], and R_P + G' = (4I - B)(3I + B) where R_P is the Gram matrix of the eight to twelve D7 roots
   labelling the support (they sum to zero) and G' a Gram matrix of 0, +-1 vectors. These conditions are satisfiable:
   labellings that pass the budgets and positivity on the support plus the inner orbits exist for both graphs at E = 8,
   for the first graph at E = 9 and for the first graph at E = 11 (runs of 5.3; the other graphs were not run). So the
   obstruction is not at this level. Reason: these are principal-minor conditions of the kind the existing searches
   already apply, and they need larger sets to fail.
2. **Descent on the support (dual-norm rule), hoping that E = 9 follows from E = 8 and so on.** It kills nothing at
   E = 8, 9, 10 and only part of the list at E = 11, 12 (5.3). Reason: the lattice Z a + sum Z He_i of a support has large
   determinant; short vectors in the other classes are forced only by the whole lattice (this is what the modular argument
   of the mission note measures), not by 8 to 12 frame vectors.
3. **Mod 2 classes.** K/2K is a binary code of dimension 22; if a, a' in K are congruent mod 2 and a' != +-a, then
   (a + a')/2 and (a - a')/2 are non-zero vectors of K and |a|^2 + |a'|^2 = 2 (sum of their sizes) >= 32. The only known
   lattice vectors with a small support mod 2 that I found are the H e_c (the 12 orbits touching a block, size 28): a
   size-12 eigenfunction supported on the star of a block would give one of size 10. But such a support is impossible
   anyway (3.3). For H e_o (support 13 mod 2) and H e_o +- H e_o' (support at least 14 in the cases I examined) I found
   no coincidence with a support of size <= 12; this last point is an inspection, not a proof.
4. **Vectors of K with a_in != 0 reduced to a_in = 0.** K contains K_7 + K_0 (K_7 = the vectors (a_in ; -C^t a_in / 4) with
   a_in in 4 D7^*, K_0 = the integer (-4)-eigenvectors of T), E = (7/4)|a_in|^2 + |a_0|^2, and the glue is D7 / 4 D7^*
   (own derivation, not written out: nothing rests on it). Subtracting H e_o for the orbit o joining two active blocks
   turns a k = 2 vector of size m into a vector of K_0 of size m + 7 with an entry +-2: longer, no reduction. I found no
   way to deduce the cases k = 2, 4 from k = 0.
5. **The Wagner complement by hand, using the D7 labels.** The labels give a path-and-cycle structure on the eight indices
   (six blocks of X_1 = six edges, the block of X_2 = four leaves, no multiple edge), but I found no short contradiction;
   a hand proof would be a case analysis of the size of the present enumeration.
6. **Characteristic eigenfunctions by counting.** Degrees and lines close (6.1-6.3). Second-order counts are consequences
   of A phi = -4 phi and A^2 + A = 12 I + 2 J and cannot contradict the existence of the vector of K in that class.

## 10. Where 7 is used; control on the graph with 11 blocks

- Section 3 (identities, parity, path count) is uniform in the parameters. Control on the Berlekamp-van Lint-Seidel graph
  (CHECKED, `lemmas_agent/bvls_control.py` on the edge list supplied, log `bvls_control_2026-10-13.log`, a few seconds):
  the opposite-corner map at a vertex is an automorphism of order 2 with one fixed vertex; the signed quotient is
  121 x 121 with S^2 + S = 20 I, inner block -I_11, outer rows with 2 + 18 non-zero entries; the analogue of Lemma 5
  (H = 4I - S, H^2 = 9H, |k a - H c|^2 = k^2 |a|^2 - 18 k (a,c) + 9 c^t H c) holds on 200 random triples; and for the
  eigenfunctions [w.x = 1] - [w.x = 2] of eigenvalue -5 (coordinates in F_3^5 recovered from the graph; m = 81, e = 162,
  Q2 = 1296) the analogue of (I1), sum C(d(z),2) = m^2 - 11 m - 9 e - Q2, reads 2916 = 2916 (also by hand: the 81 vertices
  with w.x = 0 have d = 9). So these identities hold there, as they must; they exclude nothing by themselves.
- L1 uses the numbers of this graph (row sums 8 and 6, twelve outer neighbours, E <= 12) and A.5.
- Section 4 uses H^2 = 7 H (7 = 3 - (-4)), the squares mod 7, and A.5, T16, T18, T20, which are statements about the
  99-vertex graph only. At 11 blocks H^2 = 9 H and the classes are mod 9.
- No statement of this report asserts the non-existence of an object that exists at 11 blocks. I did not compute the
  short sigma-odd (-5)-eigenfunctions of the 243-vertex graph (a lattice of rank 55; no reduction code at hand): the
  analogue of L1 was therefore not tested there, and L1 is not claimed for 11 blocks.

## 11. Files

- This report: `work/c2_elegant_2026-10-13/LEMMAS_AGENT_REPORT.md`.
- `lemmas_agent/support_k0.py`, `support_k0_v2.py`: enumeration of the orbit graphs B (k = e = 0), positivity, dual-norm test.
- `lemmas_agent/descent_singular.py`: second implementation of the dual-norm test, valid when 3I + B is singular.
- `lemmas_agent/support_k0_v2_2026-10-13.log`, `descent_singular_2026-10-13.log`: outputs.
- `lemmas_agent/bvls_control.py`, `bvls_control_2026-10-13.log`: control on the 243-vertex graph (section 10).
- `lemmas_agent/level2_labels.py`, `level2_labels_2026-10-13.log`: support plus inner orbits, labels, positivity and
  dual-norm rule (the partial runs of 5.3).
- `lemmas_agent/support_k0_m{8,9,10,11,12}_survivors.txt`: edge lists of the classes that pass positivity and the first
  implementation of the test (for m = 12 subtract the 14 lines marked SINGULAR, all killed by the second implementation).
No existing file was modified.
