# Digest of T16, T18, T20 and the pair engine (read-only, 2026-10-13)

Purpose: the owner wants to re-prove "no srg(99,14,1,2) has an automorphism of order 2" without computation. To plan that, this digest
says which parts of the present proof are hand arguments, which are machine enumerations, and what the mechanism of contradiction is
in each part. I read the sources listed in section 0.1. I ran no program and opened no program source. I did not judge whether any
proof is correct; I report what the texts say, with their own reservations. I upgraded no status: every status word below is the
source's own.

## 0. Conventions

### 0.1 Tags for files (all under `C:\Users\RESEARCHER\Desktop\Recherche_Conway\t20-codex\lemma\` unless noted)

| Tag | File | Lines |
|---|---|---|
| AR | `upstream\AUDIT_REDUCTION.md` (Theorem R, sections A.0 to A.9, B to G) | 350 |
| AE | `upstream\AUDIT_ENGINE_RULES.md` (rule-by-rule audit of the engine, holes H1 to H5) | 380 |
| PS | `upstream\PROOF_SKELETON_C2.md` (auto-generated 2026-10-01; status of that date) | 186 |
| L143 | `upstream\LATTICE_143.md` | 111 |
| T16 | `T16_PROOF.md` (index of the T16 proof) | 59 |
| TEG | `t16\dossier_2026-10-04\LEMME_EGALITE_8_SUR_7_C2.txt` (French) | 259 |
| TCU | `t16\dossier_2026-10-04\C2_PROLONGEMENT_SUPPORT16_PREUVE_CUBE.txt` (French) | 269 |
| TWA | `t16\dossier_2026-10-04\C2_WAGNER_BORNE_9_SUR_7.txt` (French) | 458 |
| VC | `t16\lab_check\VERIF_CUBE_OBSTRUCTION_2026-10-04.md` | 180 |
| R16 | `t20_CODEX\REFEREE_T16_PROOF.md` | 79 |
| T18 | `T18_PROOF.md` (read lines 1-1947 only; appendices 1948-2206 not read) | 2206 |
| T20 | `T20_PROOF.md` (read in full) | 2886 |
| R20 | `t20_CODEX\REFEREE_T20_PROOF.md` | 332 |
| ART | `ARTIFACTS_T18_T20.md` | 63 |
| BR | `BRIDGE.md` | 473 |
| PA2, PA3, PB, PM | `PROOF_C2\A2_BRIDGE.md`, `A3_LEMMAS.md`, `B_LATTICES.md`, `MAIN.md` | 88, 79, 204, 59 |
| FS | `FINAL_STATEMENT_DRAFT.md` | 129 |
| CK | `t20_CODEX\CHECKPOINT_156.md` | 224 |
| IP | `t20_CODEX\INDEPENDENT_PACKING.md` | 134 |
| RR | `t20_CODEX\REFEREE_REDUCTION.md` | 41 |
| BOARD | `T20_BOARD.md` (lines 1-70 only) | - |

A citation `T18:200-228` means that file, those lines. Quotes are exact; the three T16 dossier files are in French and I quote them in
French when the exact words matter.

### 0.2 Kinds of sentences

A plain sentence followed by a citation reports what the source says. A sentence starting "My reading:" is mine and is not in the
source; I use it only for the questions the owner asked that the sources do not answer in so many words (mainly: where the involution
sigma is used, and whether a step survives without it).

### 0.3 Vocabulary shared by T16, T18, T20

- Gamma = srg(99,14,1,2), adjacency matrix A, so A^2 = 12 I - A + 2 J (T18:91). Lambda = 1: two adjacent vertices have exactly one
  common neighbour. Mu = 2: two distinct non-adjacent vertices have exactly two. Eigenvalues: 14 (once), 3 (54 times), -4 (44 times)
  (T18:95-97).
- sigma: an automorphism of order 2. It has exactly one fixed vertex p; AR A.0 proves this for any involution, by hand
  (AR:56-88), so that Makhnev-Minakova is not needed. The "mate" of x is sigma x; there are 49 orbits of size 2.
- N(p) is a perfect matching of 7 "mate edges"; the 84 vertices outside N[p] are called words or outer vertices; each word has exactly
  2 neighbours in N(p), lying in two different mate pairs (T18:150-192; T20:200-257).
- phi: a sigma-odd integer function with A phi = -4 phi. All three lemmas first show phi takes only the values 0, +1, -1. Then
  S+ = {phi = 1}, S- = sigma S+, S = S+ u S-. |S+| = 8, 9, 10 for T16, T18, T20.
- d+(v), d-(v): numbers of neighbours of v in S+, S-. The eigen-equation reads d-(x) = d+(x) + 4 on S+ and d+(v) = d-(v) =: d(v)
  outside S (T18:243-246). k = d(p) = number of S+ vertices in N(p) (the active inner orbits); e = number of edges inside S+.
  X_d = vertices outside S with d(v) = d.
- Orbit graph B (case k = 0, e = 0): vertices are the orbits of S+, i ~ j iff x_i ~ y_j (y_j = sigma x_j). It is a simple graph
  because of sigma (the relation is symmetric), 4-regular, and any two vertices have at most 2 common neighbours (T18:427-435).
- Budget test: in any graph all of whose edges are edges of Gamma, two vertices have at most 2 - [adjacent] common neighbours
  (T18:683-690). Uses lambda and mu only.
- PSD test: M1 = 27 I - 9 A + J = 63 E_{-4} and M2 = 44 I + 11 A - 2 J = 77 E_3 are positive semidefinite, so every principal
  submatrix on a set of vertices with decided adjacencies is PSD; a "PSD violation" is an integer vector x with x^T M1 x < 0 or
  x^T M2 x < 0 (T18:660-679). Uses the spectrum only.
- Rank bound (sigma-specific): for a sigma-invariant set of orbits, the 23 x 23 matrix G_odd = 3I - A[R,R] + A[R, sigma R] has rank
  at most 22 (the sigma-odd part of V_{-4} has dimension 22, from trace(P E_{-4}) = 0), and G_even has rank at most 22 (T18:786-837;
  repeated T20:945-994).
- Lattice dictionary: for v in the envelope U, the 49 products (v,h_c), (v,u_o) are the values of a sigma-odd integer phi_v with
  A phi_v = -4 phi_v and sum phi_v^2 = 2 E(v), where E(v) = 7(v,v) - (v,y_1)^2 - (v,y_2)^2 (AR:44-54, item R-vii; BR:195-201).
  So T16, T18, T20 forbid E(v) = 8, 9, 10.
- Rejection discipline stated by both T18 and T20: only exact rejections (an integer count, or an integer vector with negative
  quadratic form, or an exact rank) are used; "kept" decisions of the programs are floating-point and are never used as a proof
  (T18:737-763; T20:918-943).

---

## 1. T16 (no sigma-odd integer (-4)-eigenfunction of squared norm 16)

### 1.1 Exact statement

T16:10-14: "Gamma = srg(99,14,1,2), sigma an automorphism of order 2 with exactly one fixed vertex p. There is no sigma-odd integer
function phi on the vertices with A phi = -4 phi and sum phi^2 = 16 (i.e. the dual of the frame lattice N has minimum >= 9/7).
Consequently, with Theorem R of `lemma/upstream/AUDIT_REDUCTION.md`: in the chosen envelope U, E(v) = 7 (v,v) - (v,y_1)^2 - (v,y_2)^2
is never 8, so E(v) >= 9 for v outside Z y_1 + Z y_2."

The referee changed "Equivalently" to "Consequently": the eigenfunction statement is equivalent to min N* >= 9/7, but the statement on
a fixed U only goes one way, because the projection of U may be a proper sublattice of N* (R16:33-40; T16:12-14).

Where it is used: the engine rule FD_MIN97 ("norm-3 x with (x,y_1)^2 + (x,y_2)^2 = 13", E = 21 - 13 = 8) and the quick deferral path
(T16:18-20). T18 and T20 do not use T16 (T16:21-22; T20:2566-2568).

### 1.2 Setting inside the dossier

P = {phi = +1}, Q = {phi = -1} = sigma(P), |P| = |Q| = 8. After numbering Q by the mates of P, B = A[P,Q] is an 8 x 8 matrix; sigma makes
it symmetric ("L'involution rend B symétrique", TEG:122-123; TCU:32-34). The dossier works with the 49-vector frame (7 h of norm 4,
42 u of norm 3, Gram H = 3I - S, H^2 = 7H) and a dual vector v with v^2 = 8/7; the integers a_i = (v,f_i) satisfy S a = -4a and
sum a_i^2 = 7 v^2 = 8 (TEG:31-78). All of this is the graph statement in disguise (BR:195-201, 270-274).

### 1.3 The chain, step by step

Each step says: what it does, hand or machine, where.

**Step 0 (the bound E >= 8; hand).** No sigma-odd integer (-4)-eigenfunction has sum of squares <= 14 (AR A.5, AR:152-167; T16:28).
An entry +-2 is impossible (the row equation would need an off-diagonal absolute sum of 6 or 8 but at most 3 is available); so
entries are 0, +-1 with support m <= 7. With e = edges inside P and d_i = degrees in P, the equation gives deg_Q(i) = d_i + 4, and
counting the common neighbours of the pairs of P gives the leftover D = m(m-7) - 7e - sum d_i^2 >= 0 for the vertices outside
P u Q; this forces m = 7, e = 0, D = 0. Then B has B^2 = 2I + 2J, eigenvalues 4 and +-sqrt(2) with equal multiplicities, so trace B = 4:
four vertices of P are adjacent to their mates, hence lie in N(p); then p sees four vertices of P and contributes C(4,2) = 6 to D = 0.
Contradiction at AR:163-166. (In AR the fixed vertex is called x.)

**Step 1 (E = 8 gives eight +1 and eight -1; hand; TEG:60-78).** If some |a_i| = 2 the other coefficients have squared sum 4, so
absolute sum at most 4, but row i of H a = 7a needs an off-diagonal absolute sum 6 (an h) or 8 (a u) with Gram entries of absolute
value <= 1: impossible. |a_i| >= 3 is excluded by sum a_i^2 = 8. So a has eight entries +-1; lifted to the graph it is phi with
eight +1 (set P), eight -1 (set Q = sigma P), and phi(p) = 0.

**Step 2 (active inner orbits; hand; TEG:80-96).** Write S = [-I, C; C^t, T]. The inner rows of S a = -4a give C a_u = -3 a_h.
Every column of C has two non-zero entries +-1, so column sums are even, so sum of a_h is even, so the number k of active h is even.
Each active h needs at least 3 incidences with active u, each u supplies at most 2, there are 8 - k active u: 3k <= 2(8 - k), so
k <= 3, hence k = 0 or 2.

**Step 3 (P and Q are independent; hand; TEG:98-118).** Same double count as in step 0, now with m = 8: D = 8 - 7e - sum d_i^2
<= 8 - 9e, so e = 0. Thus P and Q are independent and each vertex of P has exactly four neighbours in Q.

**Step 4 (k = 2 is impossible; hand; TEG:120-169).** B is binary, symmetric, row sums 4, any two rows share at most 2 indices (common
neighbours in Q). With k = 2 exactly two diagonal entries of B equal 1 (the two active inner orbits, indices 0 and 1). B_01 = 0, and
rows 0 and 1 share at most one index because p is already a common neighbour of those two vertices. Write rows {0} u A and {1} u C
with A, C triples among the six other indices, |A n C| <= 1. If A n C is empty, each a in A needs exactly one neighbour in A, i.e. a
1-regular graph on 3 vertices: impossible by parity (TEG:139-148). If |A n C| = 1, the argument ends with rows of a and b equal to
{0,s,t,d} and {0,t,c,d}, three common indices, against mu = 2 (TEG:163-167). Computed controls (a recursion over 2^15 graphs, zero
matrices) are cited as support, "sans la remplacer" (TEG:205-209), not as part of the proof.

**Step 5 (k = 0: the complement of B is a cubic triangle-free graph; hand; TCU:198-222).** With k = 0, B is symmetric with zero
diagonal and row sums 4 on 8 vertices. Its complement C = J - I - B is cubic. For i != j, (B^2)_ij = 2 C_ij + (C^2)_ij, and the bound
(B^2)_ij <= 2 forbids a triangle in C. The triangle-free cubic graphs on 8 vertices are the cube and the Wagner graph: fix v with three
independent neighbours a, b, c; the four other vertices R carry three edges (each of a, b, c has two neighbours in R); the edges form
a star K_{1,3} (then the cube) or a path P_4 (then Wagner; the 8-cycle with the four antipodal chords). The referee checked this
classification and notes it does not assume a catalogue (R16:46-52).

**Step 6 (global counts, common to cube and Wagner; hand; TCU:42-77).** For z outside P u Q the numbers of neighbours in P and in Q are equal,
d_z, and d_z <= 2 (three vertices of P would have at least 12 - 3 = 9 distinct neighbours in the 8-set Q). Counting: sum d_z = 80
(each vertex of P has 10 neighbours outside the support) and sum C(d_z,2) = 8 (the pairs of P have 56 common neighbours, Q supplies 48,
P none). So |X_0|, |X_1|, |X_2| = 11, 64, 8. Counting paths of length 2 from z in X_d to the 16 support vertices gives
b_z + 2 a_z = 16 - 5d and c_z = a_z + 3d - 2 (a, b, c = neighbours in X_2, X_1, X_0). With t = e(X_2): sum over X_0 of (a_z - 2) =
10 + 2t >= 10 (TCU:74-77). The text says these identities are old (Wave 81, section 5; TCU:76-77).

**Step 7 (the cube; hand; TCU:79-144).** If B is the complement of the cube Q_3, the pairs of P with fewer than two common neighbours
in B are the four antipodal pairs, so the eight X_2 vertices have as P-neighbours the four antipodal pairs, each exactly twice, and
the same on the Q side. Sigma sends a vertex seeing T_i in P and T_j in Q to a vertex seeing T_j in P and T_i in Q, so the four sigma-orbits
of X_2 give a 2-regular multigraph on the four labels; no loop (it would give z and sigma z four common neighbours) and no repeated edge
(mu = 2), so it is a single 4-cycle (TCU:79-107). Identify X_2 with the 8 arcs; two arcs have two common support neighbours iff same
origin or same end; this gives two disjoint 4-cycles of "concurrency" on X_2 (TCU:109-121). A vertex z in X_0 has no neighbour in the
support and cannot be adjacent to two consecutive vertices of either cycle, so N(z) n X_2 is independent in each (TCU:123-126). If z
has r and s neighbours in the two cycles (r + s = a_z, each <= 2), the number of diagonals of the cycles it sees completely is
q_z = C(r,2) + C(s,2) >= a_z - 2. Hence sum over X_0 of q_z >= 10 + 2t >= 10. But the two cycles have four diagonals in all, each
diagonal is a pair of vertices of the real graph and has at most 2 common neighbours, so sum q_z <= 8. **Contradiction: "au moins 10,
au plus 8" (TCU:11, 128-142).** The text adds that in the C2 frame with one fixed vertex the lower bound strengthens to 12 (TCU:11-12).

**Step 8 (Wagner, structural reductions; hand; TCU:146-196, TWA:57-107).** Same counts. From sum a_z = 80, sum a_z^2 = 160 - 2t, and
a^2 >= 5a - 6 on X_0 (where a >= 2), a^2 >= a elsewhere, one gets 160 - 2t >= 142 + 8t, so t <= 1 (the bound is old, Wave 81;
TCU:160-162). The fixed vertex p lies in X_0 and has a_p >= 2 (since c_p = a_p - 2 >= 0); the neighbours of p are the sigma-pairs,
which are edges, so the X_2 neighbours of p give internal edges of X_2: t >= a_p/2 >= 1. Hence t = 1, a_p = 2, b_p = 12, c_p = 0
(TCU:164-169). The defect budget sum_{X_0}(a-2)(a-3) + sum_{X_1 u X_2} a(a-1) = 8 leaves exactly two "profiles" A and B
(multiplicities counted in vertices; TCU:173-189; TWA:89-102).

**Step 9 (Wagner, finite classification of the configuration on 35 vertices; machine; TWA:109-207).** The eight "deficient" pairs
{i, i+2} of the Wagner complement each need one common neighbour outside the support, in X_2. The four sigma-orbits of X_2 pair the
eight deficient pairs: 7 x 5 x 3 x 1 = 105 matchings. The conditions "each row and each column of B[U,V] has at most one 1", "two
rectangles have at most two common support neighbours", "cell budgets 2 - B_ij" keep 31 matchings (TWA:126-139). Choosing which orbit is
the unique X_2 edge {x,y} (U n V must be empty) gives 76 cases. The induced graph is on Y = P u Q u X_0 u X_2 (35 vertices). The
10 x 8 incidence matrix C (X_0 without p to X_2, column sums 4) and the graph G on X_0 without p (six edges in sigma-orbits) are
enumerated. Counts, profile A / profile B (TWA:196-207): 105/105 matchings, 31/31 admissible, 76/76 marked, **48/16 matrices C, 48/18 graphs G,
640/32 valid couples (C,G)**. The formula (C^t C)_st = 2 - [s~t] - R_st - [p sees s and t] - E_st is used to build the rows (TWA:164-174).
The text says the arguments before justify "la couverture des boucles finies des deux scripts" (TWA:206-207).

**Step 10 (Wagner profile B; machine-found Hall obstruction; TWA:209-244).** The vertex x sees four vertices of X_1; each has a = 1 and
c = 2, so sees two vertices of X_0. For z in X_0 the number of common neighbours of x and z still to be supplied outside Y is
F_z = 2 - [x~z] - |N_Y(x) n N_Y(z)|; in each of the 32 tableaux F is eight 1's and three 0's. The four X_1 neighbours of x must "match"
these eight demands (each demanded vertex used once). A superset of the possible partner pairs is obtained by adding a provisional
vertex adjacent to x, z, z' (TWA:221-226). **Obstruction: in each of the 32 tableaux there are three demanded vertices W, pairwise
non-adjacent, with only two possible partners (|N(W)| = 2 < 3); a Hall violation (TWA:227-231).** The certificate lists W, N(W), the
allowed graph and the data to rebuild Y.

**Step 11 (Wagner profile A; hand identities plus machine; TWA:246-315).** Hand: applying A^2 = 12 I + 2J - A to the indicator of X_2 at
x gives sum over T = N(x) n (X_0 minus p) of (a_z - 2) = 4 - q (q = number of the two exceptional X_1 vertices of a = 2 that lie in
N(x)); since a_z >= 3 on X_0 minus p in profile A, q = 0 and a_z = 3 on T (TWA:253-264). N(x) induces a perfect matching (lambda = 1);
with e, f = numbers of edges inside the 4 support neighbours O and inside T, the remaining 4 - 2e + 4 - 2f vertices must be matched to
the four vertices of Z = N(x) n X_1, so 8 - 2e - 2f <= 4, i.e. e + f >= 2 (TWA:266-276). Computed: on the 640 tableaux e = 1 always;
f = 0 in 400 of them, which the inequality kills; the remaining 240 have e = f = 1 (TWA:278-282). For each of the 240, the vertex z in Z
is a word with prescribed neighbours in Y; all candidate orbits {z, sigma z} are enumerated (17 to 36 per tableau, **6,544 in all**,
"candidats locaux, pas des solutions du graphe", TWA:290-299); two candidates are joined if their four vertices, added together with no
edge between the two orbits, still respect all budgets (a safe relaxation, TWA:301-307). **Obstruction: each of the 240
compatibility graphs has no clique of size 4, whereas x needs four vertices of Z in four distinct orbits (TWA:309-312).**

**Step 12 (conclusion; hand; TWA:354-380).** Therefore no dual vector has norm exactly 8/7; since 7 v^2 is an integer and min >= 8/7
(Step 0), the minimum is at least 9/7. The text stresses that this does not need the "n <= 8" bound of the witness route of the
lab's note 54 (TWA:376-380).

### 1.4 Precise places where a contradiction appears (summary)

| Branch | Contradiction | Lines |
|---|---|---|
| E <= 7 (Step 0) | p adds C(4,2) = 6 to a leftover budget that must be 0 | AR:163-166 |
| k = 2, A n C empty | 1-regular graph on 3 vertices | TEG:139-148 |
| k = 2, |A n C| = 1 | two vertices of P with three common neighbours in Q (mu = 2) | TEG:163-167 |
| cube | at least 10 diagonals seen, at most 8 possible | TCU:128-142 |
| Wagner, profile B | Hall violation: 3 demands, 2 partners, in 32 tableaux | TWA:227-244 |
| Wagner, profile A | e + f >= 2 kills 400 tableaux; no 4-clique in 240 compatibility graphs | TWA:278-315 |

### 1.5 Machine part of T16: what is enumerated and how big

- Only Step 9, Step 10 and the last half of Step 11. Everything else is hand.
- Programs: `ENUMERER_WAGNER_PROFIL_A.py`, `ENUMERER_WAGNER_PROFIL_B.py` (Python standard library), certificates
  `WAGNER_PROFIL_{A,B}_CERTIFICATS.json` (2.06 MB and 50 KB), verifier `VERIFIER_WAGNER_CERTIFICATS.py` (NumPy, integer matrices)
  (TWA:317-335; T16:34).
- Time: profile A enumeration about 153 seconds; another recursive assembly of the neighbourhood 26,608 nodes, 8 seconds; integer
  verifier about 6 seconds for 240 + 32 certificates and 6,544 candidates (TWA:338-345). A re-run elsewhere took 1,229 seconds for the A
  enumeration (BR:435-437).
- Independent checks: the lab's own re-implementation from the mathematical text alone (folder `t16\independent_check\`,
  `work/indep_wagner_check/`) reproduces 105 / 31 / 76 / 48-16 / 48-18 / 640-32, finds all of profile B dies by a 3-against-2
  argument, and for profile A uses "a different argument from ChatGPT's, with zero survivors" (VC:146-170); the referee reran the
  verifier's check functions on all 240 + 32 + 6,544 in about 5.4 seconds, not the coverage enumerators (R16:61-73).
- Independent fact: the 363 of 400 stored pairs of lattice 011 with a witness Y = 13 (TWA:402-424) concerns the pair rule, not T16.

### 1.6 Where sigma is used, and whether the argument survives without it

Sigma-uses as written:

1. The function is sigma-odd and P, Q are linked by Q = sigma(P); B = A[P, sigma P] is symmetric because the numbering of Q is by mates
   (TEG:122-123). Steps 4, 5 use B symmetric (the "graph" C = J - I - B, the "1-regular graph on A", the symmetric rows).
2. N(p) is the set of the seven sigma-pairs (adjacent pairs); "inner" and "outer" orbits (TEG:33-35; TCU:23-29). Step 2 and Step 4
   depend on inner orbits.
3. Step 7: the sigma-orbits of X_2 and their action swapping P-side and Q-side labels (TCU:94-107).
4. Step 8: p is the unique fixed vertex and lies in X_0; its neighbours are sigma-pairs that are edges, which gives t >= 1 (TCU:164-169).
5. Step 9: the rows of C come in sigma-pairs; the matchings of deficient pairs are by sigma-orbits; mates are non-adjacent (TWA:121-124,
   160-162, 183-189).

My reading: the counting in Steps 0, 3 (the budget identity D) is mostly lambda/mu/eigen-equation counting, but it uses sigma where the
Q side is treated as the mirror of the P side (the vertices of Q contribute C(d_i + 4, 2) as mirror of P; TEG:105-113). The cube and Wagner
classification and everything after it use a symmetric B. Without sigma, B = A[P,Q] would be a general 8 x 8 0/1 matrix with no bijection
P -> Q, so I do not see that Steps 4 to 11 make sense as written; I do not claim that no sigma-free variant exists.

### 1.7 Reservations stated by the sources

- "STATUT : preuve avec classification finie calculée exactement ... Ce n'est pas une preuve intégralement à la main, ni une
  formalisation Lean." (TWA:12-16). TEG:15: "Elle ne constitue pas une vérification formelle Lean." For the cube alone TCU:143-144
  says the proof "ne dépend ni de l'énumération des 156 réseaux, ni d'un solveur, ni d'une liste d'étiquetages de racines", and
  TCU:240-241 that no spectral approximation is used.
- T4 (graph reconstruction from a solution of the model) and F0 are not used for the graph statement; F0 only for passing from
  one-fixed-vertex involutions to all involutions (TCU:259-264; TEG:22-27). Now replaced by AR A.0 (hand).
- The profile-B verifier omitted the test W subset of set(V); all 32 shipped witnesses satisfy it; the dossier is left as received
  (R16:14-31).
- The coverage enumerators were reviewed as source but not rerun by the referee; "this report does not claim a third independent
  enumeration" (R16:69-73).
- The lab could not store the text of the cube note; its control file was not on the PC at the time (VC:1-4).
- The input min L* >= 8/7 was an "ENTRÉE EXTERNE" in the dossier (TWA:362-363); it is now proved by hand in AR A.5.

---

## 2. T18 (no sigma-odd integer (-4)-eigenfunction of squared norm 18)

### 2.1 Exact statement and logical chain

T18:116-119: "Theorem T18. Let G be a strongly regular graph with parameters (99,14,1,2) and sigma an automorphism of G of order 2 with
exactly one fixed vertex. There is no function phi from the vertex set of G to the integers such that (i) phi(sigma x) = -phi(x) for
every vertex x, (ii) A phi = -4 phi, (iii) sum over all vertices of phi(x)^2 = 18."

The text says what it uses of sigma: "This is all that is assumed about sigma ... nothing from the lattice or 'frame' picture that
motivated the lemma is used" (T18:104-107). The lattice dictionary is outside the document (T18:138-145).

The chain written in the text (T18:121-131): integer phi -> values 0, +1, -1, nine vertices at +1 -> S+ independent, no support vertex in
N[p], orbit graph B in {B0, B1, B2} (Computation 4.10) -> no outside vertex with 3 neighbours in S+, profile of N(p) in
{(2,5,0), (3,3,1), (4,1,2)}, profile (4,1,2) impossible -> (3,3,1) impossible by section 7 -> (2,5,0) impossible by section 8.

### 2.2 Tree of cases

```
T18
|-- Sec 3   values 0,+-1, nine orbits at +1                         (Prop 3.1)              hand
|-- Sec 4   support
|     |-- k in {0,2}                                                 (Lemma 4.2)             hand
|     |-- e <= 2                                                     (Lemma 4.3)             hand (spectral bound)
|     |-- identities (I1),(I2); parity e = C(k,2) mod 2              (Lemmas 4.4, 4.5)       hand
|     |        => (k,e) in {(0,0),(0,2),(2,1)}
|     |-- (0,2) impossible                                           (Lemma 4.6)             hand
|     |-- e = 1 impossible: Case C, Case A, Case B                   (Lemma 4.7)             hand
|     |        => k = 0, e = 0: S+ independent, support avoids N[p]  (Cor 4.8)
|     `-- B is B0, B1 or B2                                          (Comp 4.10, Cor 4.11)   MACHINE (1,024,380 graphs)
|-- Sec 5   outside vertices
|     |-- path count, class sizes                                    (Lemmas 5.1, 5.2)       hand
|     |-- X_3 empty                                                  (Thm 5.3)               hand
|     |-- identities (a_0, a_1 in terms of a_2), quadratic identity  (Lemma 5.4)             hand
|     |-- profiles (2,5,0),(3,3,1),(4,1,2)                           (Lemma 5.5)             hand
|     `-- profile (4,1,2) impossible                                 (Lemma 5.6, Prop 5.7)   hand
|-- Sec 7   profile (3,3,1), each of B0,B1,B2                        (Comp 7.3, 7.6)         MACHINE (stage 1 + four steps)
`-- Sec 8   profile (2,5,0), each of B0,B1,B2                        (Comp 8.4, 8.5, 8.6/8.8) MACHINE
            B0: no stage-C survivor;  B2: none;  B1: 4 survivors, each killed by the rank bound (or by stage D)
```

### 2.3 Case by case

For each case: what kills it, kind, size, facts used, sigma.

**Case 3. Values 0, +1, -1 and nine orbits at +1 (Prop 3.1; T18:200-228; hand).** Put kappa_O = |phi| on an orbit; sum of kappa_O^2 over
the 49 orbits is 9. Claim: if kappa_O = kappa > 0 the other orbits' kappa sum to at least 3 kappa (eigen-equation at x with phi(x) = kappa:
every other orbit contributes at least -kappa_O', the mate contributes -kappa if adjacent). The partitions {3}, {2,2,1}, {2,1,1,1,1,1}
fail the claim (0 < 9, 3 < 6, 5 < 6). Kills: a counting inequality. Uses: eigen-equation, sigma-oddness, orbits, phi(p) = 0.
Sigma: used for the orbit structure and for phi(sigma x) = -phi(x). My reading: the proof as written needs the orbit pairing and oddness;
it does not seem to use that sigma preserves adjacency. Without an involution the value patterns would not be organised in orbits.

**Case 4.2. k in {0,2} (Lemma 4.2; T18:258-279; hand).** For an active inner orbit the 12 outer neighbours of a_c carry phi-sum
-3 phi(a_c), so n_c >= 3 and n_c is odd; for inactive orbits n_c is even. Counting pairs (s, v), s in S minus N(p), v in N(p): each s has
exactly 2 neighbours in N(p) (Cor 2.2, mu = 2), so sum n_c = 18 - 2k. Parity gives k even; size gives 3k <= 18 - 2k, k <= 3. Uses: mu,
lambda (structure of N(p)), eigen-equation. Sigma: N(p) = 7 sigma-pairs (Lemma 2.1) and "by sigma b_c has the same number n_c as a_c". Not
as written without sigma (the pairs a_c, b_c are mates).

**Case 4.3. e <= 2 (Lemma 4.3; T18:281-292; hand, a positivity/eigenvalue argument).** The number of S+ to S- edges is
sum over x in S+ of d-(x) = 2e + 36 (eigen-equation), edges inside S- number e "by sigma", so 1_S^T A 1_S = 8e + 72. But
A <= 14 E_0 + 3 (I - E_0) as quadratic forms and 1_S^T E_0 1_S = 18^2/99, so 1_S^T A 1_S <= 90. Hence e <= 2. Uses: spectrum (the eigenvalue
-4 is dropped), eigen-equation. Sigma: for the count of edges in S-. T20 does not use this bound (it uses (I3)): "gives only e <= 3 here"
(T20:425-426).

**Case 4.4-4.5. Identities (I1), (I2) and the parity law (T18:294-319; hand).** (I2): sum over z outside S of d(z) = 90 - 4e. (I1):
sum C(d(z),2) = 18 - 7e - Q, obtained by counting common neighbours of the 36 pairs of S+ (72 - e triples) using
C(d,2) + C(d+4,2) = d^2 + 3d + 6; the term C(d-(x),2) = C(d+(x)+4,2) for the vertex sigma x is where sigma enters (T18:309-311). Parity law:
the 80 vertices z != p outside S are paired by sigma with d(sigma z) = d(z), so sum of C(d,2) over them is even, so e = C(k,2) mod 2;
(k,e) in {(0,0),(0,2),(2,1)}. Kills: parity of a count. Sigma: essential (pairing of the 80 vertices by sigma, uniqueness of p).

**Case 4.6. (0,2) impossible (Lemma 4.6; T18:325-330; hand).** With e = 2, Q is 4 or 6. Q = 6 makes (I1) negative. Q = 4 gives d(z) <= 1
everywhere outside S, but (I2) demands sum d = 82 > 81, the number of vertices outside S. Kills: counting.

**Case 4.7. e = 1 impossible (Lemma 4.7; T18:347-402; hand case analysis).** Let the unique edge inside S+ be {x_a, x_b}; (4.5) says
x_j ~ y_i iff x_i ~ y_j, so M_j = {i : x_j ~ y_i} are "symmetric" index sets with |M_j| = d+(x_j) + 4 - eps_j. Case C (both ends inner): adjacent
vertices of N(p) are mates, but the mate of x_a is in S-: impossible (T18:351-355). Case A (both outer): |M_0| = |M_1| = 5 and common
neighbourhood bound |M_0 n M_1| <= 1 force a unique r with r in no M_j; then M_r is inside {0,1}, |M_r| <= 2, against |M_r| >= 3
(T18:356-389). Case B (a outer, b inner, uses k = 2): M_0 (5 elements) and M_7 (4 elements) lie in a 7-set, so |M_0 n M_7| >= 2, against
the single common neighbour of an adjacent pair (T18:391-402). Kills: pigeonhole with mu = 2 / lambda = 1. Sigma: through (4.5) and the
mate structure of N(p). My reading: the M_j are a codification of the sigma-mirror; without sigma there is no relation between the
S- neighbourhoods of different x_j.

**Case 4.8-4.11. B is B0, B1 or B2 (T18:406-489).** Hand: Cor 4.8 (k = 0, e = 0, so S+ and S- independent, every vertex of S has exactly 4
neighbours, all on the other side); Lemma 4.9 (B 4-regular, codegrees <= 2). Machine (Computation 4.10; T18:441-483): up to
isomorphism there are exactly three 4-regular graphs on 9 vertices with all codegrees <= 2; in each, every pair has codegree 1 or 2;
Cor 4.11 (hand): 18 pairs of codegree 1 ("deficient") and 18 of codegree 2. Size: 1,024,380 labelled 4-regular graphs on 9 vertices,
16 isomorphism classes, all connected; 13 classes contain a pair with 3 or 4 common neighbours; the three that survive have
5040 + 30240 + 20160 = 55,440 labelled copies. Four programs (`ref1_quartic9.py`, second referee's `q9.py` written from the text,
`enum_S.py`, `verify_S.py`; the last imports the isomorphism routine of the third) (T18:462-483, 1731-1736). Kills: a graph-theoretic
classification (no hand proof; "Hand remark" only that a 4-regular graph on 9 vertices is connected, T18:482-483). Sigma: B exists
and is symmetric because of sigma.

**Case 5.1-5.3. Path count, class sizes, X_3 empty (T18:517-550; hand).** For z outside S with d(z) = d: the sum of d(w) over the
neighbours w of z outside S is 18 - 5d, so d <= 3; n_0 = 9 - n_3, n_1 = 54 + 3 n_3, n_2 = 18 - 3 n_3. Theorem 5.3: if z in X_3 had its 8 outside
neighbours with d-sum 3, at least 5 are in X_0; the same for z' = sigma z; n_3 >= 2 so |X_0| <= 7; two sets of >= 5 inside a 7-set meet in
>= 3, so z and z' have 3 common neighbours: mu = 2 violated. Kills: counting. Sigma: z' = sigma z is a distinct vertex of X_3 with the
same properties (p is the only fixed vertex and has d(p) = 0). The text stresses this uses neither B nor N(p) nor computation
(T18:550).

**Case 5.4. Identities when X_3 is empty (Lemma 5.4; T18:558-600; hand).** For z in X_0: a_0 = a - 4, b = 18 - 2a; in X_1: a_0 = a - 1,
b = 13 - 2a; in X_2: a_0 = a + 2, b = 8 - 2a (a = neighbours in X_2, b in X_1, a_0 in X_0). Every vertex of S has exactly 4 neighbours in X_2
and 6 in X_1. Quadratic identity (*): sum_{X_0}(a-4)^2 + sum_{X_1}(a-2)(a-3) + sum_{X_2} a(a-1) = 36. The text says (*) is used only as
a filter inside some programs, where it "removes nothing" (T18:602-603).

**Case 5.5-5.7. Profile of N(p); (4,1,2) killed (T18:605-649; hand).** Each of the 9 vertices of S+ has exactly 2 neighbours in N(p),
so sum over c of delta_c = 9 with delta_c = d(a_c) = d(b_c) in {0,1,2} (equal on mates, by sigma): h_2 = 2 + h_0, h_1 = 5 - 2 h_0, profiles
(2,5,0), (3,3,1), (4,1,2). Count: the sum over the 14 neighbours of p of a_2(w) equals 36 - 2 h_2 (common neighbours of p with the 18 vertices of
X_2), while the structure forces a_2 >= 1 on N(p) n X_2 (the mate is a neighbour in X_2), a_2 >= 2 on N(p) n X_1, a_2 >= 6 on N(p) n X_0.
For h_0 = 2 the lower bounds add to 36, the exact value is 36 - 8 = 28: impossible. For h_0 = 1 all lower bounds are equalities
(this is used in section 7). Kills: counting inequality; "pure hand proof ... nothing computed" (T18:649). Sigma: mates inside N(p)
and equality of d on mates are essential.

**Case 7. Profile (3,3,1), for each of B0, B1, B2 (T18:839-1242; hand model + MACHINE).** Hand: Lemma 7.1 (each deficient pair U has a unique
outside common neighbour s_U in X_2; there is a fixed-point-free involution tau of the 18 deficient pairs with sigma s_U = s_{tau U}, so
X_2 is organised in 9 "rectangles"), Lemma 7.2 (stage-1 tests (R1), (R2), (R3)), Lemma 7.4 (forced adjacencies, all inequalities of Lemma
5.6 become equalities), Lemma 7.5 (the 39-, 45-, 51-vertex sets are determined by finite data). Machine:
- Computation 7.3 (stage 1): for each B, 99 admissible rectangles, 63 usable in N(p); admissible matchings tau 25,514 / 13,799 / 9,229; orbits
  under Aut(B) 425 / 1,259 / 528 (Aut orders 72, 12, 18) (T18:916-926). Four programs agree.
- Computation 7.6 (four steps; T18:1098-1111; counts T18:1150-1159), B0 / B1 / B2: pairs (tau,F) passing budgets on 25 vertices 3,510 / 7,224 /
  2,406; 39-vertex survivors 383 / 481 / 7; tables with no budget violation on 45 vertices 8,639 / 27,203 / 0; of which PSD 23 / 164 / 0;
  graphs on 51 vertices without budget violation 52 / 1,839 / -; with PSD **0 / 0**. So B2 dies at the budget test on 45 vertices;
  B0, B1 die at the PSD test on 51 vertices. In the direct step 4, 1,829 of 1,839 graphs of B1 are rejected by M1 and exactly 10 by M2 only, so
  both matrices are needed (T18:1187-1202).
- Second confirmation for B1: the rank bound on 47 vertices (Y u {w, sigma w}) kills all 164 tables (295,200 candidates, 16,334 without
  budget violation; none survives both rank conditions) (T18:1179-1183).
- Programs: I1 (first implementation, reads `types.json`), I2 (`t18_VERIF331`, written from the description, shares no code), I3 for B2 only,
  referee REF1 and second referee REF2 as count checks; exact rejections (T18:1133-1163).
Kills: the property that makes every candidate fail is a budget violation (lambda, mu) or a PSD violation (spectrum); the text gives no
structural reason beyond these counts. Sigma: the matching tau, the 9 rectangles, the mate-closed sets and the sigma-invariant determined sets
are all sigma-structure; the rank bound is sigma-specific. My reading: without sigma this whole section has no meaning (no tau, no orbits
of X_2).

**Case 8. Profile (2,5,0), for each of B0, B1, B2 (T18:1244-1647; hand model + MACHINE).** Hand: Lemma 8.1 (forced structure: N(p) = A_p u W,
W has 5 orbits with distinct unordered types), Lemma 8.2 (sets Y37 and Y47 are determined by tau, F, H, types, K_c), Lemma 8.3 (forced numbers
(C1) to (C8)), Lemma 8.7 (forced numbers for stage D). Machine:
- Computation 8.4, stage B on the 37 vertices S u {p} u X_2 (T18:1364-1377): pairs (tau,F) with no budget violation on 23 vertices
  5,545 / 12,366 / 4,347 (PSD on these: 4,904 / 11,509 / 3,863); **stage-B triples (tau,F,H): 5,595 / 4,977 / 196**. Two exact implementations
  (ENUM, VERIF) with identical sets plus referee counts; the second referee verified each triple exactly PSD.
- Computation 8.5, stage C on 47 vertices Y47 = Y37 u W (T18:1425-1480): **B0: no survivor, B2: no survivor, B1: exactly 4.** Work sizes
  (program CMINE): B0 132,132 types tested, 603,053 sets K without budget violation on 39 vertices, 52,580 without PSD violation, 3,165 cover nodes, none
  reaches the 47-vertex test; B1 115,473 types, 905,578 / 75,295 sets K, 9,248 cover nodes, 43 tests on 47 vertices, 4 survivors; B2 4,222 types,
  39,107 / 1,535 sets K, 173 cover nodes, no 47-vertex test (T18:1503-1509). Stage C for B0 and B2 therefore dies on budgets, on PSD violations at 39 vertices, and on the exact cover of the numbers req(s) by one set K per orbit of W (condition (C8), T18:1346-1347, 1450-1452).
- The 4 survivors of B1 (matching #813 with F = [2,9] and [3,6]; matching #975 with F = [1,2] and [3,6]) satisfy every budget and both M1,
  M2 are exactly PSD on 47 vertices (ranks 46 and 45) (T18:1516-1536). They are killed in two independent ways:
  (i) rank bound (Computation 8.6, T18:1538-1563): det G_odd (23 x 23) = 47,684 for #813 and 874,944 for #975, and rank G_even = 23 > 22; five codes agree;
  the smallest eigenvalue of G_odd is about 0.011-0.012, so G_odd is positive definite and "a PSD test cannot see the obstruction";
  (ii) stage D (Computation 8.8, T18:1565-1623): for every admissible neighbourhood Z of a vertex z in X_0 minus p (678, 678, 846, 846 pairs {Z, sigma Z})
  the graph on 49 vertices has a PSD violation (3,048 integer certificates; the violated matrix is always M1).
Kills: budgets and PSD for B0, B2 and for the non-survivors of B1; the rank bound (a sigma-specific linear-algebra fact) for the last four.
Sigma: tau, rectangles, orbits of W, the rank bound.

**Alternative killing of the four B1 survivors proposed but not used (T18:1934-1941; unrefereed).** The second referee remarks that
rank M1[Y47] = 46 > 44 = rank M1 would already exclude the four survivors by Lemma 6.1 alone, without sigma and without the rank bound of
Prop 6.4 and without stage D. "They are his own and have not been refereed, and nothing in this document uses them."

### 2.4 What T18 uses of the graph (by case)

| Case | lambda | mu | eigen-equation | involution | fixed vertex p | PSD (M1, M2) | rank bound | frame |
|---|---|---|---|---|---|---|---|---|
| Prop 3.1 | no | no | yes | oddness | phi(p) = 0 | no | no | no |
| 4.2 k | yes | yes | yes | yes | yes | no | no | no |
| 4.3 e <= 2 | no | no | yes | yes | no | spectrum of A | no | no |
| 4.4-4.5 | yes | yes | yes | yes | yes | no | no | no |
| 4.6, 4.7 | yes | yes | yes | yes | yes (N(p)) | no | no | no |
| 4.10 B | no | no | no | graph only | no | no | no | no |
| 5.1-5.7 | yes | yes | yes | yes | yes | no | no | no |
| 7, 8 searches | yes | yes | yes | yes | yes | yes | at 4 survivors / 164 tables | no |

(T18:104-107 says the frame is not used. The table is my condensation of the cited lemmas.)

### 2.5 Machine summary for T18

Six finite computations: 4.10, 7.3, 7.6, 8.4 + 8.5 (stage B and C), 8.6 (with 8.8 as an alternative) (T18:1663-1665). Implementations: several per
line (two exact implementations sharing no code for most lines, three for B2; referee counts; second referee reproduced every line from the text alone)
(T18:1669-1697, 1822-1895). The hand part "was audited by a referee who re-derived every statement ... every load-bearing hand statement was
found correct" (T18:1689-1692), and by a second referee (T18:1822-1832).

### 2.6 Reservations stated by T18 itself (T18:1699-1787, 1896-1906)

- Programs were not audited line by line; agreement of programs sharing no code is the support, "not a proof" (T18:1720-1726).
- "Kept" decisions are floating-point; only rejections are exact and only they are used (T18:1701-1715; T18:737-763).
- Some programs read `types.json`, produced with a filter depending on the lemma "H16" (no configuration of squared norm <= 16) not proved in the
  document; the entries used were recomputed from budgets alone by the second referee, and every computed line has an implementation that does not read
  the file (T18:1737-1759).
- Only samples of the PSD certificates were saved (50,000 for B1, 12,000 for B2; the 3,048 of stage D complete); those of B0 not rechecked
  (T18:1760-1764).
- Several runs were cut by time limits and completed by bookkeeping scripts; scripts were patched during the sessions and the stored outputs'
  provenance by exactly the current versions was not verified (T18:1765-1771).
- "Not verified at all, and not used": the dictionary between T18 and the lattice statement, H16, and the analogous statement for norm 20
  (T18:1777-1778).
- Passages written for the last revision (listed at T18:1905-1932) were read by no referee.

---

## 3. T20 (no sigma-odd integer (-4)-eigenfunction of squared norm 20)

### 3.1 Exact statement, and a status warning inside the file

T20:154-157: "T20. Let G be a strongly regular graph with parameters (99,14,1,2) and sigma an automorphism of G of order 2 with exactly one
fixed vertex. There is no function phi from the vertex set of G to the integers such that (i) phi(sigma x) = -phi(x) for every vertex x, (ii) A phi
= -4 phi, (iii) sum over all 99 vertices of phi(x)^2 = 20."

Status warning (the file has stale and current statements side by side): the box at T20:3-21 says "Every case of the proof is closed" and lists the
second programs; but T20:33-36 still says "This text does not prove T20. It proves ... Theorem 10.1 ... The exclusion of that last sub-case is Computation
9.29", T20:63-74 (section 0.2) still says some lines have one program only and that section 9.B "has not yet been refereed", and T20:2514-2518 states Theorem
10.2 (T20) as proved from Theorem 10.1 plus Computation 9.29. The box at T20:13 itself says "Sections 0.2, 7.3, 7.4, 10.2 and 10.3 still say 'one program'".
Current status per the later files: ART:41-52 (all runs and branches), BOARD:13-14, 26-27, 35-36, R20:224-243 (route-B addendum: "No blocking error"),
FS:34-42.

### 3.2 Tree of cases

```
T20
|-- Sec 3   values 0,+-1, ten orbits at +1                           (Lemmas 3.1, 3.2, Prop 3.3)     hand
|-- Sec 4   k in {0,2,4}; e <= 1; parity; three cases                (Lemmas 4.1-4.4, Cor 4.5)       hand
|     |-- case II extra: plus edge joins two outer indices           (Lemmas 4.6-4.8)                hand
|     |-- case III extra: outer indices = 2-subsets of K, K4         (Lemma 4.9)                     hand
|     `-- the nine support structures I.0-I.5, IIa.0, III.0, III.1   (Comp 4.12)                     MACHINE
|-- Case III (k=4): III.0, III.1   Sec 7                             (Lemmas 7.1-7.3, Comp 7.4, 7.5) hand model + MACHINE
|-- Case II  (k=2): IIa.0          Sec 8                             (Lemmas 8.1-8.7, Comp 8.8, 8.9) hand model + MACHINE
`-- Case I   (k=0): I.0-I.5        Sec 9
      |-- no vertex of N(p) has d=3; n_3 in {0,2}                    (Lemmas 9.1, 9.2)               hand
      |-- profiles (3,4,0),(4,2,1),(5,0,2); (5,0,2) impossible       (Lemma 9.3, Prop 9.4)           hand
      |-- n_3 = 0: 12 cases (6 graphs x 2 profiles)  Sec 9.A         (Lemma 9.18, Comp 9.19, 9.20)  hand model + MACHINE (615,405 bases)
      `-- n_3 = 2: 50 cases (25 types of z x 2 profiles) Sec 9.B.6   (Lemmas 9.22-9.28, Comp 9.29)   hand model + MACHINE (64,528 bases)
```

### 3.3 Case by case

**Case 3. Values 0, +1, -1, ten orbits (T20:260-325; hand).** Lemma 3.1: if kappa_O = kappa > 0 the other orbits' kappa sum to at least 3 kappa
for an inner orbit and 4 kappa for a word orbit, with equality only if x has exactly one neighbour in each other active orbit and the value is
-kappa'. Lemma 3.2 kills {2,1^6}: the orbit with kappa = 2 must be inner, equality holds, x is adjacent to y_1..y_6, sigma x to x_1..x_6;
then x_1 and x have common neighbours sigma x and at most one y_i, and the eigen-equation at x_1 gives a sum at least -2 - 1 = -3 > -4
(T20:286-300). Partitions {3,1} and {2,2,1,1} fail Lemma 3.1. The file says the proof of Lemma 3.2 "uses only lambda = 1, mu = 2 and the
eigen-equation" (T20:302), while the displayed proof also uses sigma x, the inner structure of N(p) and Lemma 2.1(c) (T20:289-300). I record this
without adjudicating.

**Case 4.1-4.5. k in {0,2,4}; e <= 1; parity; the three cases (T20:370-441; hand).** Same count as T18 Lemma 4.2: sum of n_c = 20 - 2k; if k = 4
then n_c = 3 on the four active inner orbits and the three inactive inner orbits have no neighbour in S (T20:370-392). New identity (I3):
sum over z of C(d(z)-1, 2) = 9 - 3e - Q, with Q >= 2e, gives e <= 1 (T20:396-423) without the spectral bound used in T18. Parity: e = C(k,2) mod 2, so
(k,e) is (0,0) case I, (2,1) case II, (4,0) case III (T20:430-441). Kills: counting and parity. Sigma: orbit pairing of the 78 vertices z != p
outside S (parity); N(p) mates.

**Case II sub-lemmas (T20:448-494; hand).** Plus edge not between two inner indices (mate edges only); not between inner and outer: after the usual
sets M_j one finds a graph on a 3-set U_0 in which every vertex has degree exactly 1, impossible (an even number of odd-degree vertices) (T20:453-486);
so the plus edge joins two outer indices and forms a 4-cycle x_a - x_b - y_a - y_b (Lemma 4.8, not needed). Kills: pigeonhole and a parity of degrees.
Sigma: the symmetric relation (4.5) again.

**Case III sub-lemma (Lemma 4.9; T20:501-520; hand).** For k = 4 every active inner vertex has exactly 3 neighbours in S minus N(p) (all in S-); every outer index j has
two neighbours y_c, y_c' in N(p); kappa(j) = {c,c'} is a bijection from the six outer indices to the six 2-subsets of K = four inner indices
(uses that x_c, x_c' in N(p) are non-adjacent with p already a common neighbour). So the outer words are the edges of K_4.

**Case 4.12. Support structures (T20:544-709; MACHINE).** A support structure of type (K,P) is a graph on the 21 vertices x_i, y_i, p satisfying (S1)-(S5)
(sigma-invariance, p/inner pattern, plus edges, eigen-equation, budgets). Computation 4.12: labelled counts 27,720 (type I, normalised at index 0), 2,880 (IIa),
0 (IIb), 10,080 (III); up to isomorphism 6 of type I, 1 of IIa, 2 of III, i.e. nine graphs (T20:579-589). Completeness of the list is argued from the
totals and the automorphism orders via orbit-stabiliser counts (T20:591-606). Two programs (enumerator 1: 1,841,249 / 6,414,667 / 1,463,867 / 469,755 search
nodes; enumerator 2 without isomorphism test, sorting by an invariant) agree on the four totals; the nine automorphism orders (16, 4, 10, 4, 4, 20; 1; 3, 4) come
from enumerator 1 only (T20:608-631). Sigma: (S1) builds sigma into the objects.

**Case III: III.0, III.1 (k = 4; T20:1054-1237; hand model + MACHINE).** Hand (Lemma 7.1): X_4 = {p}, X_3 empty, X_0 = the six inactive inner vertices,
|X_2| = 24, |X_1| = 48, each s in X_2 is a word and has exactly 2 - r(s) neighbours in X_0 and in X_2 (r(s) <= 2 = neighbours among the eight active inner
vertices); every vertex of X_0 has exactly 4 neighbours in X_2. Search (Lemma 6.5): the 12 orbits of X_2 are placed one at a time, always filling a
unit {i,j} (pair of indices with remaining multiplicity need(i,j)); Lemma 6.5 proves that a true configuration yields a node at every level, whatever
unit is chosen; Lemma 7.3 adds the symmetry group H_0 of order 48 on X_0 (T20:996-1051, 1126-1144).
- Computation 7.4 (III.0; T20:1148-1158): levels 0 to 10: 1, 13, 116, 881, 7,109, 30,102, 54,327, 31,126, 6,086, 243, 0 nodes; 130,004 nodes,
  4,094,709 candidates: 671,315 rejected by budget, 3,293,391 by PSD, 130,003 kept; no rank rejection.
- Computation 7.5 (III.1; T20:1160-1173): 1, 13, 208, 2,156, 21,165, 132,172, 492,124, 764,789, 211,921, 4,315, 0 nodes; 1,628,864 nodes, 75,949,406
  candidates: 17,487,147 by budget, 56,833,395 by PSD; **one** candidate at a node of level 9 survives both and is killed by the rank bound
  (G_odd of rank 23 on 47 vertices). The independent verifier re-traversed the tree and also finds that node dead without the rank bound
  (T20:8-12; `lemma/t20_III1/VERIF.md`), but shares `cases.py` and parts of the skeleton (R20:131-143).
Kills: PSD violations (about three quarters) and budgets; the text gives no structural reason beyond these counts. Sigma: orbits placed in pairs; four
"patterns" per pair of orbits; V(s) = U(sigma s); rank bound; H_0 commutes with sigma.

**Case II: IIa.0 (k = 2; T20:1239-1430; hand model + MACHINE).** Hand (Lemmas 8.1-8.6): X_3 empty (n_0 = 4, n_1 = 54, n_2 = 21); the ten vertices of N(p) minus S all have d = 1
(called W, five mate pairs), X_0 is two word orbits; each W pair has a type {i,l} of outer indices, the five types form a simple graph on the eight outer
indices with degrees (2,1,2,1,1,1,1,1), exactly 180 such graphs (T20:1294-1311). Machine: Computation 8.8 (180 -> 63 budget violations, 30 PSD, 87 kept; two programs
with identical lists) and Computation 8.9 (search from the 87 roots: 45,497 nodes, 898,945 candidates, 201,918 budget, 651,617 PSD, 45,410 kept, deepest level 7, no node of
level 8 where 10 orbits are needed; no rank bound) (T20:1374-1386). Second program `iian_verify.py follows`: 45,497 nodes, same kept counts (T20:1408-1429).

**Case I common hand lemmas (T20:1432-1535; hand).** Lemma 9.1: no vertex of N(p) has d = 3 (if z in N(p), d(z) = 3, then sigma z in X_3 is adjacent to z so a_3(z) >= 1, a_0(z) >= 5,
and |X_0| >= 9 against |X_0| = 9 - n_3 <= 7). Lemma 9.2: n_3 is 0 or 2: n_3 <= 4 and even; n_3 = 4 needs four pairwise disjoint 3-subsets U, V, U', V' of {0,...,9}: 12 > 10
(T20:1471-1498). Lemma 9.3: sum delta_c = 10, profiles (3,4,0), (4,2,1), (5,0,2). Proposition 9.4: profile (5,0,2) impossible: the four vertices of Z_p have a_2 >= 8 - 2 a_3
and their X_2-neighbourhoods have a union of at least 28 (n_3 = 0) or 20 (n_3 = 2) elements inside X_2' of size 20 or 14 (T20:1519-1535). Kills: counting. Sigma: Z_p pairs are mates, disjointness of mates' neighbourhoods (Lemma 2.1(c)).

**Case I, n_3 = 0: twelve cases (Sec 9.A; T20:1905-2119; hand model + MACHINE).** The model (Lemma 9.18): the seven pairs of N(p) have "types" forming an N-configuration
(h_2 A-types = pairs {U,V} of disjoint deficient pairs of B with at most one B-neighbour of each index in the other; h_1 W-types {i,l}; pairwise "compatible" rows; every
index in exactly two sets); the 35-vertex set Y_0 = S u N[p] is determined by B and the N-configuration; the 11 or 12 orbits of X_2' are the free vertices (T20:1917-1974).
- Computation 9.19 (stage 1; T20:1978-1998): totals 17,396,042 N-configurations, 3,130,401 orbits under Aut(B), **615,405 bases kept** (so 2,514,996 orbits are rejected on the 35-vertex test; in the
  cloud summaries read, "no representative is rejected by a budget violation on the 35 vertices; all the rejections are PSD violations", T20:2046-2049). Per case, N-configurations / orbits / bases,
  e.g. I.1 (3,4,0): 3,508,550 / 878,137 / 219,589; I.0 (4,2,1): 178,768 / 11,322 / 3,022.
- Computation 9.20 (stage 2; T20:2005-2027): **15,762,181 nodes** in all (case totals from 27,524 for I.5 (4,2,1) to 7,279,961 for I.1 (3,4,0)); **no node of level 6 or more** (11 or 12 orbits are
  needed); the deepest level with a node is 4 or 5; 15 candidates rejected by the rank bound, all for I.1 (2 for (4,2,1), 13 for (3,4,0)).
Programs: first program `stage1c.py`, `run_stage2.py` with `eng6.py` and model `cases6.py`; second program `in_verify.py` (own model, own enumeration of N-configurations, own tests; follows the first program's
unit choice); both complete on all 12 cases per ART:41-51 and BOARD:35-36. Where the second program replaces the rank bound by its own search, the rank nodes of I.1 die (T20:2053-2060; ART:48-52).
Sigma: N(p) pairs, types (U;V) with V(s) = U(sigma s), orbits placed in pairs, Aut(B) quotient. My reading: the model is built on sigma.

**Case I, n_3 = 2: fifty cases (Sec 9.B; T20:2122-2484; hand model + MACHINE).** Hand (Lemma 9.22): z in X_3 is a word, z' = sigma z, N(z) n N(z') is one word orbit; four sub-cases (i-S), (i-X1), (ii), (iii).
Lemma 9.23: the number of vertices s of X_2 with U(s) = {i,j} is exactly need_z(i,j) = 2 - codeg_B(i,j) - [i,j in U] - [i,j in V] (sum 24), and a_0(s) <= 4. Lemmas 9.27, 9.28 define the 37-vertex base Y_z = S u N[p] u {z, z'} and
its exhaustiveness (T20:2330-2419). Machine (Computation 9.29; T20:2421-2477): (a) ordered types (U;V) of z that pass the budget test on 23 vertices: 8, 46, 30, 24, 24, 50 for I.0 to I.5, forming 1, 9, 3, 4, 5, 3 = 25 classes;
(b) N-configurations 1,173,102 (profile (4,2,1)) and 12,557,760 ((3,4,0)) over the 25 types, 686,675 and 7,461,476 representatives under G_z, each tried with all attachments of z to N(p) (84, or 72 with a Z-pair; 362,754,336
attachments tested by the second program) -> **bases kept 8,557 and 55,971, 64,528 in all**; (c) stage 2 nodes with 0,1,2,3 added orbits: 8,557 / 1,494 / 190 / 8 and 55,971 / 17,994 / 2,646 / 108, 86,968 nodes; **no node has four added orbits**
whereas 8 or 9 are needed; rank bound never used; about 7 CPU-hours on one laptop. Second program `in_verify.py` (modes `basesz`, `follow`, `mergez`) finds the same classes of bases and the same kept count at every node (1,950,773 integer
PSD vectors in stage 1 and 1,978,816 in stage 2; exact rational elimination 0 times) (T20:2459-2477). The hand lemmas of 9.B.3 to 9.B.5 (Lemmas 9.24-9.26) "are kept for the record and are used by nothing" (T20:2125-2126, 2338).

**Hand lemmas of case I that no computation uses (T20:1753-1902, 1540-1752; hand).** Lemma 9.7 (slots), Lemmas 9.9-9.13 (cells, edge counts, identity (9.6)), Theorem 9.14 (in profile (4,2,1) the two inner X_0 vertices u, u' are adjacent to no vertex of R_0:
the proof counts neighbourhoods in X_2' and ends with v and sigma v having four common neighbours against mu = 2), Corollary 9.15, Theorem 9.16 (e(X_0) <= 8: equality case of Cauchy-Schwarz forces a psi-eigenvector structure and then a mate edge inside
an independent set; "No enumeration"), Corollary 9.17, Lemma 9.24 (triangle reduction). The text says they come from the Codex session, were re-read by the lab, and are "not used by the enumeration of section 9.A" (T20:1755-1757, 1719, 2044-2052).

### 3.4 Which statements rest on the ~615,000 and ~64,000 enumerations of bases, what is enumerated, what makes each case fail

- ~615,405 bases (Computation 9.19): the stage-1 bases of case I with n_3 = 0 (T20:1998). What is enumerated: for each of the 6 graphs B and 2 profiles, every N-configuration, i.e. every way to assign to the h_2 A-pairs and h_1 W-pairs
  of N(p) (seven pairs, h_0 of them Z-pairs) pairwise-compatible types so that every index lies in exactly two types (T20:1917-1925); one representative per Aut(B) orbit is built on 35 vertices S u N[p]. Bases = representatives with no budget violation and
  both M1, M2 PSD. Each base is then the root of the stage-2 search (Computation 9.20) that places orbits of X_2' one unit at a time. They rest on: Proposition 9.21 (n_3 = 0 impossible), hence on Theorem 10.1 item 4 (n_3 = 2 is forced) (T20:2029-2036, 2499-2512).
- ~64,528 bases (Computation 9.29(b)): the n_3 = 2 case; same structure but with the orbit {z, z'} of X_3 added to the base (37 vertices) and the type (U;V) of z and its attachment to N(p) enumerated (T20:2421-2457). They rest on Proposition 9.30 and
  hence on Theorem 10.2 (T20).
- What makes each case fail: in every search the rejection is exact and of one of the kinds budget violation (common neighbours exceed 2 - [adjacent]), PSD violation (an integer vector x with x^T M1 x < 0 or x^T M2 x < 0), a violated forced upper bound ("caps",
  unit multiplicities), or, at 16 nodes in the whole proof (1 in III.1, 15 in I.1) the rank bound (T20:900-909, 2569-2577). The numbers show PSD violations dominate: III.0 3,293,391 PSD vs 671,315 budget; III.1 56,833,395 vs 17,487,147; IIa.0 651,617 vs 201,918;
  case I stage 1 "all rejections are PSD" in the summaries read. No further structural invariant that separates dying from surviving branches is stated in the text.

### 3.5 What T20 uses of the graph (by case)

| Part | lambda | mu | eigen-eq | involution | fixed vertex p | PSD | rank bound | frame |
|---|---|---|---|---|---|---|---|---|
| Sec 3 values | yes | yes | yes | oddness, mates | yes | no | no | no |
| Sec 4 support | yes | yes | yes | yes | yes | no | no | no |
| Comp 4.12 | yes | yes | yes | structure (S1) | yes | no (remark: PSD exact on supports) | no | no |
| Sec 7, 8, 9.A, 9.B.6 searches | yes | yes | yes | yes | yes | yes | at 16 nodes | no |
| Hand lemmas 9.7-9.17, 9.24-9.26 (unused) | yes | yes | yes | yes | yes | no | no | no |
| Lemma 10.2 (dual-norm rule; conditional, unused) | no | no | yes | oddness | no | no | no | uses statement for norm <= 14 |

(T20:2555-2619 gives the dependencies: T18, the 04/10 lemma, H16, AUDIT_NORME1 and the dual-norm rule are all "not used".)

### 3.6 Sigma in T20, in one place

Sigma enters the framework of T20 in these places (all as written): Lemma 2.1 and its corollaries (every word has two neighbours in N(p) in two different pairs; mates adjacent iff in N(p); T20:200-257); the
definition of orbits and of S- = sigma S+; the parity law (T20:430-441); the symmetric relation (4.5) defining M_j (T20:357-363) used in Lemma 4.7; the orbit graph B (symmetric); the support structures (S1) invariance (T20:549-561); types U(s), V(s) = U(sigma s)
(T20:809-815); the search of Lemma 6.5: states are graphs with involution, orbits are added in pairs, adjacency between two added orbits has four patterns (T20:1010-1016); the symmetry group H_0 (T20:1126-1144); the rank bound (T20:945-994).
My reading: sigma is built into the objects that are enumerated (orbit graphs, types of pairs of N(p), unit multiplicities for X_2 vertices, orbit placement). The budget and PSD tests themselves do not use sigma; they are applied to induced subgraphs.

### 3.7 Reservations stated by T20 itself and by its referee

- Floating-point "kept" decisions never used as proof (T20:921-943, 2623-2632).
- Programs not audited line by line; second programs follow the first program's choice of unit, so node counts were never reproduced by a search with another order (T20:2633-2652). Referee G2: equal counts do not identify the kept decisions; "A complete second traversal
  of its own tree with valid unit choices suffices by Lemma 6.5. Say that explicitly" (R20:85-112).
- III.1 second verification shares the model file `cases.py` and part of the enumeration skeleton (T20:8-12; R20:131-143).
- Provenance (G1): some outputs only in session scratch directories; source revisions inferred (R20:62-83; ART:57-62).
- Saved certificates are samples only (15,000 for III.0; 6,358 for IIa.0; ten for I.0 (4,2,1)) (T20:2653-2655).
- Table of Computation 9.20 copied from `final_table.out`; the script that wrote it is not in the repository folder (T20:2664-2667).
- Parts only the author of T20_PROOF.md has checked: listed at T20:2673-2684.
- No human referee; "AI sessions only" (FS:6; CK:76-81).

---

## 4. The bridge and the engine

### 4.1 Theorem R (the source of the engine's rules)

AR:44-54 (Theorem R): if (Gamma, sigma) exists, there are an odd unimodular lattice U of rank 24 without vector of norm 1 and vectors y_1, y_2, h_1..h_7, u_1..u_42 of U with
(R-i) (y_a,y_b) = 7 delta_ab and y_a orthogonal to every h_c, u_o;
(R-ii) (h_c,h_d) = 4 delta_cd, (u_o,u_o) = 3, (u_o,u_o') in {0, +-1} with exactly ten non-zero off-diagonal per u;
(R-iii) (h_c,u_o) = -C_co with the 42 columns of C the vectors e_i + e_j and e_i - e_j (i < j) of Z^7;
(R-iv) 3 h_c + sum_o C_co u_o = 0;
(R-v) for every real v, sum_c (v,h_c)^2 + sum_o (v,u_o)^2 + (v,y_1)^2 + (v,y_2)^2 = 7 (v,v) (identity (F));
(R-vi) Z y_1 + Z y_2 is primitive in U and E(v) = 7(v,v) - (v,y_1)^2 - (v,y_2)^2 >= 8 for v outside it;
(R-vii) for every v of U the 49 integers (v,h_c), (v,u_o) are the values of a sigma-odd integer phi with A phi = -4 phi and sum phi^2 = 2 E(v).
U is one of Borcherds' 156 lattices (AR:184-188; cited). Proof by hand in AR A.0-A.9 (AR:56-215) with the oddity formula and classification of forms over F_7 as cited theorems; referee: "No mathematical error found in section A" (RR:9-20, 28-40). No rule of the engine uses g or the index
[Nmax : N] (AR:244-249; AE:9-14, 372-379).

### 4.2 The bridge theorem (R-vii) and the witness rules

BR:186-310 proves (R-vii) by hand: with a_i(v) = (v, f_i), phi_v lifted (value a_i on a representative, -a_i on its mate, 0 on p), A phi_v = -4 phi_v and sum phi_v^2 = 2 E(v) = 14 N(pi v), using Lemmas 0-4 (BR:229-268: x ~ sigma x iff x ~ p; the odd functions
form a 49-dimensional space on which A acts by S with S^2 + S = 12I, multiplicities 22 and 27, H = 3I - S has H^2 = 7H and rank 22; tight frame; projection). Uses on the graph side only A^2 = 12I - A + 2J and an involutive automorphism with exactly one fixed vertex
(BR:298-306). Rank 24 is "used once and is essential" (BR:301-302). Sigma is essential here (the lift, the 49-dimensional odd space, trace P = 1).

Coset reduction: E(v) depends only on v modulo Z y_1 + Z y_2; every class has a representative with |(v,y_a)| <= 3, so N(v_0) = (E + a^2 + b^2)/7 is an integer >= 2 (BR:277-296; PA2:34-50):

| E | forced representative | sum of squares of the two normal products |
|---|---|---|
| 8 | norm 3 (norm 2 needs 6, a non-sum of two squares; norm 4 needs 20 > 18) | 13: {abs(a), abs(b)} = {2, 3} |
| 9 | norm 2 | 5: {1, 2} |
| 10 | norm 2, or norm 4 | 4: {0, 2}; or 18: {3, 3} |
| 11 | norm 3 | 10: {1, 3} |
| 14 | norm 2 (a root orthogonal to both normals) | 0 |

Four tests are therefore complete for E <= 10 (PA2:46-52; FS:30 "complete for E <= 10 (hand remark of 07/10)"): (W8) a norm-3 vector with Y = 13 (T16); (W9) a root with Y = 5 (T18); (W10) a root with Y = 4, or a norm-4 vector with abs((x,y_1)) = abs((x,y_2)) = 3 (T20). Corollary Y1: given T18 and T20, every
root has abs((r,y_1)) <= 1 and abs((r,y_2)) <= 1 (E(r) = 14 - a^2 - b^2 >= 8 gives a^2 + b^2 <= 6; if abs(a) = 2 then E is 9 or 10); so a root with (r,y_1) = +-2 kills y_1 whatever y_2 (BR:211-222; PA2:60-75).

A pair with no witness has E >= 11 for all vectors outside Z y_1 + Z y_2. The lemmas say nothing about it; "such pairs exist in the swept lattices in large numbers (for instance 2,652 pairs among the 28 small lattices of section B.6, and thousands in lattice 003), and they are excluded only by the frame search of Part B.
A lemma T22 would move that boundary by one step; none is claimed" (PA3:72-76; PB:175-179).

### 4.3 Table of engine rules: how a pair (y_1, y_2) is excluded

Source for the rows: AE:46-87 (one row per rule, audited by Codex against Theorem R), with AR A.8 (AR:190-197). Kind: S = excludes by exhibiting a vector whose energy is too small (or too large a normal product); F = excludes inside the frame search by showing the frame cannot be completed; B = budget or counting
on the whole lattice or pair; X = symmetry or bookkeeping (never excludes by itself).

| # | Rule (code location) | Exact mathematical content | Kind | Line |
|---|---|---|---|---|
| 1 | Normal norms and orthogonality (FD:186-187, Y2:191) | (y_a,y_b) = 7 delta_ab, from R-i. Input certification must hold ("early consumer traps run before these assertions") | pre-condition | AE:48 |
| 2 | Root pair filter (YP header, Y2:201-203) | for a root a, E(a) = 14 - Y >= 8, so Y <= 6, and Y in {0,1,2,4,5} (3 and 6 are not sums of two squares) | S | AE:49; AR:243-246 |
| 3 | Norm-three pair filter (Y2:197-199) | E(x) = 21 - Y >= 8, so Y <= 13: both heights at most 3, not both 3 | S | AE:50 |
| 4 | New-root pair filter (FD:188-190, Y2:192-195) | at a shadow root beta (beta = z/2, z characteristic of norm 8) the y_1, y_2 and 42 u have half-odd pairings; baseline energy 11 of 14; one absolute value 3/2 costs 2, 5/2 costs 6; so abs((beta,y)) <= 3/2 and not both | S | AE:51; AR:190-195 |
| 5 | Exact dual trap, represented by rules 2-3 | a non-zero short vector of K* = proj_K U has a lift with normal heights in [-3,3], norm < 8/7 + 18/7 < 4, so is a root or norm-3 vector | S | AE:52 |
| 6 | Characteristic trap (FD:1415-1428) | characteristic z of norm 16: E(z) = 112 - Y with Y = 2 mod 8, and E(z) = (42 odd squares) + 4 sum b_c^2 with sum b_c^2 odd, so E >= 46, Y <= 66 | S (energy of a characteristic vector) | AE:55; AR:196-197 |
| 7 | MIN97, Y = 13 (FD:1431-1453) | a norm-3 witness with Y = 13 has E = 8, an odd integer eigenfunction of norm 16; excluded by T16 | S + T16 | AE:56; BR:224-225 |
| 8 | Deferral witnesses (q/defer_consumer) | root with Y = 5 (T18) or Y = 4 / norm-4 with (3,3) (T20), with exact per-pair certificate (norms 7, orthogonality, witness) | S + T18/T20 | BR:444-454; PA2:77-87; FS:30 |
| 9 | Corollary Y1 | root with abs((r,y_1)) = 2 kills y_1 for every y_2 | S + T18/T20 | BR:211-222 |
| 10 | Candidate h and u norms and perpendicularity (FD:191-194) | h among norm-4 vectors perpendicular to both y; u among norm-3 vectors perpendicular to both y | F (set-up) | AE:57 |
| 11 | h-admissibility at shadow roots (FD:192-193) | remaining energy 3 at beta allows only integer h heights 0, +-1 | F | AE:58; AR:190-195 |
| 12 | Coverage targets exact/flex (FD:199-204) | a y-hit has h coverage 1 and no word hitter; with no eligible hitter coverage 3; otherwise 1 or 3 | F | AE:60 |
| 13 | Boundary points (FD:1456-1472) | characteristic z norm 16, Y = 58: 4 sum a_i^2 + sum(b_u^2 - 1) = 12; h coverage 3 with no hitter, or 1 with exactly one word of height 3 | F | AE:61 |
| 14 | WPRUNE (FD:1473-1490) | for Y >= 50, 4 sum a_i^2 + sum(b_u^2 - 1) = 70 - Y; no word height >= 5; h height bounds 2 at Y = 58, 4 at Y = 50 | F (opt-in) | AE:62 |
| 15 | Endpoint confinement (FD:1533-1544) | if u hits a point s, both s and s - u have one signed-unit h footprint; a covering h is one of two endpoints | F | AE:63 |
| 16 | Pairwise h compatibility (FD:1298-1325, 1370-1412) | chosen h orthogonal, cannot share an exact target-1 point, need non-empty Same and Opp word cells | F | AE:64 |
| 17 | Word validity, Lemma U+ (FD:1016-1020, 1193-1203) | delete words with forbidden h products, more than two endpoints, a y-hit, or a hit at a point already covered twice | F | AE:65 |
| 18 | Empty cells (FD:1205-1216) | each chosen h pair needs a Same and an Opp word orthogonal to all other chosen h | F | AE:66 |
| 19 | Common-zero and star counts (FD:1217-1226) | with l h remaining, l(l-1) distinct words have both endpoints among them; each chosen h needs 2l words with other endpoint unchosen | F | AE:67 |
| 20 | Coverage capacity and saturation (FD:1079-1103, 1236-1245) | remaining required covers cannot exceed remaining h or candidates through the point | F | AE:68 |
| 21 | Flex leaf hitter (FD:1052-1066) | coverage 1 needs an actual word hitter with exactly two h endpoints | F | AE:69 |
| 22 | General branching, sibling deletion (FD:1133-1253) | branch on a required point; every completion has a first chosen member through it | F (search control) | AE:70 |
| 23 | Generic non-flex branching (FD:349-365) | needs "an extra impossibility/precondition proof"; Codex marks HOLE H2 (see 4.5) | F, flagged | AE:71 |
| 24 | Lemma Z (FD:255-258, 449-452) | sum R-iv: 3 sum h is an even integral combination of u (every column of C has even sum); so sum h is in 2U | F | AE:75 |
| 25 | Local star sums (FD:252-312, 433-507) | for each h its 12 endpoint words (oriented to pair +1) sum to 3h; partial shadow-height sums must reach the target with odd increments +-1 and at most one +-2 at a flex point | F | AE:76 |
| 26 | Joint cells, distinct words, hitter counts (FD:1659-1706) | choose one word per Same/Opp cell, 42 distinct lines, all seven star equations, exactly one hitter on each coverage-1 flex point; cap of 1000 joint solutions = HOLE H1 | F, flagged | AE:77 |
| 27 | Final T identity and frame operator (FD:1709-1722) | with word Gram G_u = 3I - T, polarising (F) gives G_u^2 + C^t C = 7 G_u, i.e. T^2 + T = 12I - C^t C; outer products must sum to 7 G^-1 | F (final check) | AE:78 |
| 28 | Node and stored-leaf limits | node stop gives INCOMPLETE; leaf overflow gives INVALID; neither is an exclusion | control flow | AE:79 |
| 29 | Lattice component budgets (CB) | trace of (F) on each root component and its perpendicular space; total projected energy is 7 times dimension; relaxed nonnegative normal energies must meet them | B; solver status = HOLE H4 | AE:80 |
| 30 | Pair root-class budgets (PB pair_test) | sum (F) over roots sharing (component, Y): h/u energy equals (14 - Y) times the class size; trace the remaining orthogonal space; 42 u, 7 h | B; solver status = HOLE H4 | AE:81 |
| 31 | Packing and packing-admissible words (EP:80-132) | the 42 word hit sets on shadow roots are pairwise disjoint in each shadow coset, so the 42 smallest hit counts m(x) = r/8 - E_roots(x) must be at most the number of new roots | B | AE:82; PB:26-32 |
| 32 | Packing connectivity/span/dual trap (EP:133-164) | the word graph is connected; all words in one component of rank >= 22; every vector of the integer span with norm < 8/7 lies in the normal plane, so span of short dual vectors plus perpendicular space has dimension <= 2 | B | AE:83, 106-110 |
| 33 | Weyl dominance / diagram subgroup | reflections in roots preserve U; a chamber representative loses no orbit | X | AE:53 |
| 34 | Swap (HS:44-48, 86-89) | (R) is symmetric in y_1, y_2; invariant I(y) = sum (alpha,y)^2 plus sorted shadow-coset hit counts; keep I(y_1) <= I(y_2) | X | AE:54; AR:275-280 |
| 35 | Reflection symmetry at depth 0, 1, later (FD:1106-1174, 1551-1601) | fix y_1, y_2 and a target-1 point; its unique covering h can be moved to a reflection-orbit representative | X | AE:72-74 |
| 36 | Twin construction, transfer, root catalogue, deferral, canonical rule (TT, HS) | replacing the normal residue gluing by R = [[2,2],[-2,2]] preserves K and the frame vectors and gives another odd unimodular U; a pair is deferred to a twin only when all classes of the computed root type are excluded; dependency graph must be well-founded | X (conditional) | AE:84-87 |

Not in the AE table but part of the lattice-level exclusions (20 lattices, no pairs enumerated): C1's packing test (rule 31) for 10 lattices; criterion (E) with packing for 3; "Sol 0836" with packing for 5 and alone for 153 (second proof by AR A.9); lattice 143 by the hand proof L143; all
"cited from the project's notes" (PB:26-34; FS:69-81). L143: sum of |P_V u|^2 over the 42 u is at most 7 dim V (from (R-v) alone); with the table of the 4,096 norm-3 vectors in three kinds, c <= 28 vectors of the third kind and at least 14 others with squared projection >= 9/16 on a line of budget 7: 63/8 > 7
(L143:46-53); the table is proved by an exact glue description (L143:79-95) and refereed by Codex (L143:3-6).

### 4.4 Which rules exhibit a short vector, which show the frame cannot be built

Short-vector rules (a vector of U with an impossible energy): 2, 3, 4, 5, 6, 7, 8, 9. All reduce to "E(v) >= 8 (hand, AR A.5)", or to the three lemmas T16, T18, T20 (E = 8, 9, 10), or to the characteristic-vector energy bound (hand, AR A.8). A single exact witness suffices; completeness of
any list is not needed for the exclusion (BR:321 H6; PB:139-140). The completeness of the lists of norm 2, 3, 4 matters only for the claim that rules 2-3 and the witness rules lose nothing; it was certified by the theta identity N4 + 24 N2 + 24 N3 = 196,560 and exact acceptance for all 156 lattices
(AE:286-318).

Frame-cannot-be-built rules: 10-27 in the search; 29-32 as budgets and packing. The search (rules 10-27) is a finite subset enumeration: choose 7 vectors h of norm 4 covering the "targets" at shadow roots (verdict text "stage 1 empty: no 7 h"); then for each h the 12 endpoint words summing to 3h
("no local star sums"); then one word per cell with all star equations and the final identity T^2 + T = 12I - C^t C (verdict "joint star sums, but (F) fails"). Verdict texts in the records: "char trap / stage 1 with EC + boundary points / star sums / twin transfer" (PB table lines such as B_TABLE_156.md:239; "EC" is not defined in any file I read).

### 4.5 Where sigma is used in the engine

The engine is lattice-only: it uses (R-i)-(R-vi) and never sigma directly. Sigma enters through Theorem R: the seven h and 42 u, the D7 columns of C (R-iii), the star-sum identity (R-iv), the identity (F) are all consequences of the sigma-odd quotient (AR A.1-A.3). T16, T18, T20 (E = 8, 9, 10 forbidden) are graph statements
that use sigma as shown in sections 1.6, 2.3, 3.6. My reading: the engine and the pair enumeration are not relevant to a sigma-free statement; the E <= 10 rules are the part of the engine that is "hand plus T16/T18/T20".

### 4.6 What the sweep produced (figures from the sources)

- 156 lattices: 20 by lattice-level arguments, 136 at pair level (PB:26-52). Pair level: S 91, SD 11, GD 2, G 2, O 1 (000), H/F/H3 29 (PB:36-52).
- Stream sweep of 91 lattices: 220,260,576 pairs: 97,628,147 excluded at once, 22,702,398 by search, 93,822,540 swap-covered, 6,107,330 twin-transferred (plus 161 first-INCOMPLETE pairs resolved) (PB:58; CK:104-112).
- Deferred sweep of 13 lattices: 5,190,752 pairs rest on T18 and 2,508,295 on T20, each with an exact certificate (7,762 stream records; Golay 17,983 pairs) (PB:59-60; FS:85-89).
- The 28 old pair-list lattices: with Corollary Y1 and the E-witnesses alone, 17 lattices have no pair left; 2,652 pairs in 11 lattices have min E >= 11 and need the engine (PB:129-179).
- Pair enumeration completeness was compared with an independent enumerator on 4 lattices (140, 135, 141, 064): equal sets (PB:41-47; FS:25).
- "There is no certificate for a pair excluded by search (25,775,627 such pairs in the rows of the table that have the number)" (PB:200-201).

### 4.7 Reservations flagged in the sources for the engine and the bridge

AR:29-37 lists five conditions; AE:118-370 and FS:44-52 record their later handling:

- H1: silent cap of 1000 joint solutions (real in the code; the one verdict it could falsify occurs in no stored record: 17,676 + 356 + 57 files; importer refuses it) (AE:120-147).
- H2: rigid kernel never builds a frame containing an h with zero footprint; no proof of the precondition; exposure checked by re-search: 25 of 25 lattices covered, 147,475,940 pairs read, 10,267 without flex point, 8,432 exposed, 0 not excluded again (AE:149-247; FS:49). "H2 remains open globally" at the level of a proof (AE:194).
- H3: floating-point enumeration of the catalogues; closed by the theta identity for all 156 (AE:249-318).
- H4: "EXCLUDED (pair budget)" rests on an LP solver status; 12,620 such pairs in lab-local files; lattice 105 re-run without the test (56,544 pairs), lattice 143 replaced by L143 (AE:320-351; FS:51).
- H5: the 9/7 rule needs T16; T16 refereed (AE:353-370).
- Pair-enumeration completeness (producer) not independently compared except on 4 lattices; "the lattice-level arguments P, EP, SP, So: cited from the project's notes" (PB:195-203).
- Provenance of old records: 39 lattices partly on a lab version (recovered), 26 partly without code version, repaired by Y1 certificates and a v10 re-run of 713 representatives (PB:68-114; CK:131-190).
- The upstream sections BR:456-473 (weak points: upstream reduction not on that machine; T20 open) are superseded by AR and T20; they are stale text.
- PS (skeleton) says "Status: excluded 93, open 62, partial 1" (PS:3): that is the 2026-10-01 state (`upstream\README.md:8` warns: "Its status line and table are those of 01/10, not current").

---

## 5. Hand or machine: every ingredient

Size is given when there is a machine part. File references use the tags of section 0.1.

| # | Ingredient | Hand / machine / cited | Machine size | File |
|---|---|---|---|---|
| 1 | A.0 an involution fixes exactly one vertex (replaces Makhnev-Minakova) | hand | - | AR:56-88 |
| 2 | A.1 sigma flips the seven blocks; 49 orbits | hand | - | AR:90-104 |
| 3 | A.2 signed quotient S, S^2 + S = 12I | hand | - | AR:106-113 |
| 4 | A.3 frame, H = 3I - S, N, N* | hand | - | AR:115-123 |
| 5 | A.4 discriminant form is the anisotropic plane for every g | hand + oddity formula (cited) | - | AR:125-150 |
| 6 | A.5 min N* >= 8/7 (no phi of squared norm <= 14) | hand | - | AR:152-167 |
| 7 | A.6 envelope U exists, unimodular odd rank 24, no norm 1 | hand + F_7 form classification (cited) | - | AR:169-182 |
| 8 | A.7 classification of the 156 lattices | cited (Borcherds) | - | AR:184-188 |
| 9 | A.8 new roots, characteristic trap | hand | - | AR:190-197 |
| 10 | A.9 U indecomposable (excludes 153, 152) | hand | - | AR:199-215 |
| 11 | D: the 156 Gram matrices are the 156 lattices | machine recomputation of invariants (det, oddness, norm 1, roots, even neighbours); mass check not done | 156 lattices | AR:282-303; FS:24 |
| 12 | Bridge theorem (R-vii), E <-> phi_v | hand | numerical checks on Paley(9), srg(243,22,1,2) | BR:186-310, 388-402 |
| 13 | T16 hand part (E = 8 steps 1-8, 12) | hand | - | TEG, TCU, TWA |
| 14 | T16 finite classification (Wagner) | machine | 105 matchings -> 31 -> 76; 48/16 matrices C, 48/18 graphs G, 640/32 tableaux; 240 + 32 certificates; 6,544 candidates | TWA:196-207, 309-315 |
| 15 | T18 hand part (sections 2 to 6, Lemmas 7.1-7.5, 8.1-8.3, 8.7, Prop 6.4) | hand | - | T18:148-838, 855-1094, 1259-1360, 1569-1584 |
| 16 | T18 Computation 4.10 (three graphs B0, B1, B2) | machine | 1,024,380 labelled graphs, 16 classes | T18:441-483 |
| 17 | T18 Computation 7.3, 7.6 (profile (3,3,1)) | machine | 25,514 / 13,799 / 9,229 matchings; 425 / 1,259 / 528 orbits; 39-vertex survivors 383 / 481 / 7; tables 8,639 / 27,203 / 0 -> 23 / 164 / 0; 51-vertex graphs 52 / 1,839 -> 0 | T18:916-926, 1098-1163 |
| 18 | T18 Computation 8.4, 8.5 (profile (2,5,0), stages B and C) | machine | stage B 5,595 / 4,977 / 196 triples; stage C survivors 0 / 4 / 0 | T18:1364-1480 |
| 19 | T18 Computation 8.6 (rank bound on the 4 survivors) or 8.8 (stage D) | machine (exact determinants; exact PSD vectors) | 4 graphs; det 47,684 and 874,944; 3,048 certificates | T18:1538-1623 |
| 20 | T20 hand part (sections 2 to 6, 7.1-7.3, 8.1-8.7, 9.1-9.5, 9.18, 9.22-9.23, 9.27-9.28) | hand | - | T20:200-1051, 1054-1144, 1239-1370, 1432-1535, 1926-1974, 2141-2419 |
| 21 | T20 Computation 4.12 (nine support structures) | machine | 27,720 / 2,880 / 0 / 10,080 labelled; 9 classes | T20:579-631 |
| 22 | T20 Computation 7.4, 7.5 (III.0, III.1) | machine | 130,004 nodes, 4.09 million candidates; 1,628,864 nodes, 75.9 million candidates | T20:1148-1236 |
| 23 | T20 Computation 8.8, 8.9 (IIa.0) | machine | 180 -> 87 roots; 45,497 nodes, 898,945 candidates | T20:1374-1429 |
| 24 | T20 Computation 9.19, 9.20 (case I, n_3 = 0) | machine | 17,396,042 N-configurations -> 3,130,401 orbits -> 615,405 bases; 15,762,181 nodes; 15 rank nodes | T20:1978-2119 |
| 25 | T20 Computation 9.29 (case I, n_3 = 2) | machine | 25 types, 686,675 + 7,461,476 representatives, 362,754,336 attachments, 64,528 bases, 86,968 nodes (about 7 CPU-hours) | T20:2421-2477 |
| 26 | T20 hand lemmas not used by any computation (Thms 9.14, 9.16, Lemmas 9.7, 9.11-9.13, 9.24-9.26) | hand | - | T20:1579-1902, 2255-2328 |
| 27 | Energy tables, witness rules W8-W10, Corollary Y1 | hand | - | BR:276-296; PA2:34-75 |
| 28 | Per-pair certificates of deferred pairs | machine (exact re-computation) | 7,762 stream records (5,179,532 + 2,501,532 pairs), Golay 17,983 pairs | PB:59-60 |
| 29 | Producer: enumeration of pairs (y_1,y_2) up to Aut(U) and signs | machine | e.g. 1,050,528 canonical pairs for 064; compared with an independent enumerator on 4 lattices | PB:36-47; FS:25 |
| 30 | Engine frame search (rules 10-27) | machine (rules are hand, execution is machine) | 22,702,398 pairs by search in the stream lattices; 25,775,627 quoted at PB:200 | PB:58, 200 |
| 31 | Immediate rules 2-9 | hand rules, machine execution | 97,628,147 pairs excluded at once in the stream lattices | PB:58 |
| 32 | Swap and twin rules | hand rules, machine bookkeeping | 93,822,540 swap-covered, 6,107,330 twin, 1,622 dependencies without cycle | PB:58; FS:83 |
| 33 | Rigid-kernel (H2) audit | machine | 147,475,940 pairs read, 8,432 exposed, 0 not excluded again | FS:49; AE:196-247 |
| 34 | Lattice 143 | hand (two lines) + exact glue table | 4,096 norm-3 vectors in 3 kinds; exact check by Codex | L143:46-95 |
| 35 | Lattices 153, 152 | hand (AR A.9) | - | AR:199-215 |
| 36 | Packing (10 lattices), criterion (E) and packing (3), "Sol 0836" and packing (5) | cited from project notes; packing independently recomputed by Codex for 18 lattices (22 s) | 42 smallest m versus capacity; 4 dual-trap cases (short dual spans 8, 9, 8, 24) | PB:26-32; IP:77-123 |
| 37 | Lattice 000 (odd Leech) | machine | 141 pair classes: 86 LP certificates verified in integers, 55 searched | PB:50; FS:75 |
| 38 | Old lab runs on C1's pair lists (28 lattices, 044 unfinished at the time) | machine, now replaced by Y1 + E-witness route (17 lattices with no pair left) + v10 re-run | 173,708 pairs, 171,056 with witness, 2,652 survivors, 1,168,349 pairs re-run | PB:124-193 |
| 39 | Whole assembly | AI sessions only, no human reader, nothing formalised | - | PM:46-49; FS:6; CK:76-81 |

---

## 6. Unclear or not read

I did not smooth over any of the following.

**Files or parts not read.**
- T18_PROOF.md lines 1948-2206 (Appendices A to D: commands, the explicit four survivors of B1, label correspondence, vertex numbering).
- All working folders `lemma\t18*`, `lemma\t20*`, `lemma\t16\independent_check`, `lemma\bridge*`, `lemma\cloud`: only their file lists and the summaries quoted in T18, T20, ART and the referee texts were read. In particular no program was opened, so what a program does is known only from the proof texts' descriptions.
- `t18_REFEREE\REPORT.md`, `t18_REFEREE2\REPORT.md`, `t20_CODEX\HAND.md`, `PROFILE_421.md`, `EDGE_BOUND.md`, `TRIANGLE_REDUCTION.md`, `REFEREE_TWIN_DEPENDENCIES.md`, `FIXED_Y1_003.md`, `EXACT_LATTICE_IDENTITY.md`, `REFEREE_143_PROOF.md`, `t20_HAND\NOTES.md`, `SPEC_N3.md`, `t20_R3_I\SPEC_ROUTE_B_N3.txt`, `t20_R3_I\REPORT.md`, `t18\T18_REPORT.md`, `t20\T20_REPORT.md`, `T20_WORK.md`, `bridge\BRIDGE.txt`, `bridge_REFEREE\REPORT.md`, `upstream\MODEL.md`, `LATTICE_143.md`'s companion scripts, `PROOF_C2\A1_REDUCTION.md` (I read AR instead and did not compare), `PROOF_C2\B_TABLE_156.md` except lines 225-260.
- `AUDIT_ENGINE_SOURCES.json`, `theta_odd24.py`, `budget_143.py`; the dossier's JSON certificates and Python enumerators; the engine sources (`frame_dfs_next.py`, `hstage_stream_next.py`, `y_pairs*.py`, `envelope_pack.py` ...) which live outside `lemma\`. The rule contents in section 4.3 are those of AE, not of the code.
- C1 notes 139-145 (criterion (E), Sol's argument, frame identity at new roots, Lemma U+), the Astra dossiers, "Sol 0836": cited by the sources, not in the folders I read.

**Things I could not follow or did not re-derive.**
- I re-derived nothing. In particular I did not re-check the arithmetic of the Wagner profile formulas (TWA:164-174, the identity for (C^t C)_st with the E_st term), the count of 105 -> 31 -> 76, or the table of 25,514 / 13,799 / 9,229 matchings.
- The abbreviation "EC" in the verdict text "stage 1 with EC + boundary points" is not defined in any file I read.
- The meaning of "flex point", "exact target-1 point", "Same/Opp cell", "hitter" in rules 12-26 is only as stated in AE; I did not find a self-contained definition.
- TCU:150-155: the phrase "chaque sommet du support voit deux X_2 : la somme de ses déficits est 14 - 4*3 = 2" is used without derivation in the text; I took it as given.
- The computed controls quoted in TEG:200-211 (recursive generation of 8 x 8 matrices; the 2^15 graphs; "six matrices" when the bound on the two inner rows is relaxed to 2) were not examined; the text itself says they support the hand proof "sans la remplacer".

**Inconsistencies between files that the sources themselves do not reconcile.**
- T20_PROOF.md says both "This text does not prove T20" (T20:33) and states Theorem 10.2 as T20 (T20:2514-2518); the first is stale text (box at T20:3-21, R20:224-243, BOARD:14, 44).
- T20_PROOF.md line 302 says Lemma 3.2 "uses only lambda = 1, mu = 2 and the eigen-equation", although its proof uses sigma x and Lemma 2.1 (T20:289-300); T20:1810 says Theorem 9.14 uses "(9.1), the sizes of the classes, the profile, and lambda = 1, mu = 2", although its proof uses u' = sigma u and sigma-invariance of L.
- PB:58 gives 22,702,398 pairs "by search" for the 91 stream lattices; PB:200-201 says 25,775,627 such pairs "in the rows of the table that have the number". The two counts have different scopes; I did not find the reconciliation.
- AR:316 still quotes 212,825,691 pairs for the stream sweep; FS:71 and CK:89-90 replace it by 220,260,576 ("a count that I cannot reproduce").
- AR:282-303 and FS:24 say the 156 Gram matrices were recomputed; the "mass check" (sum of 1/|Aut| against SPLAG Table 17.1) was not done; the count 156 relies on Borcherds (cited).
- BR:456-473 (sections 9.1-9.2: upstream reduction not available, T20 open) and BR:323 (H8 "Open") are stale; AR and T20 supersede them.
- PS (skeleton) is explicitly the state of 2026-10-01 (PS:3; upstream README lines 8-9).

**Open reservations the sources themselves keep** (not my judgement): no human reader; nothing formalised; second programs follow the first program's unit choice; III.1 verification shares a model file; T16, T18, T20 and the engine were produced and refereed by AI sessions only; producer completeness compared on 4 lattices; lattice-level arguments (packing, criterion (E), Sol 0836) cited from notes, packing independently recomputed on 18 lattices; H2 "open globally" as a proof statement though audited by re-search (AE:194); the 2,652 survivors of E >= 11 and the engine's search verdicts have no certificate other than the search itself (PB:200-201).
