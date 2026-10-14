# The asymmetry window: forced local symmetry against rigidity (14/10/2026, LAB)

Direction from the user (14/10, about 16:00 UTC): "selon moi comprendre a fond l'asymetrie c'est la methode", then
"attaquez ca" (Codex and me, no heavy computation; the solver campaign is parked, `SOLVER_CAMPAIGN_STATE.md`).
Split agreed with Codex (bridge 684-685): Codex = when does the rooted skeleton K_x determine G; me = the general frame.
Theory only in this note; nothing was run except reading earlier logs.

Family: G = srg(2m^2+1, 2m, 1, 2), m lines through each vertex (m = 2 Paley 9, m = 7 Conway, m = 11 the eight graphs
at 243). Notation of note 176 / NOTE_ASYM_PALEY section 11: x a vertex, N(x) = m lines {x, a, a'}, the far vertex z_uv
is the unique vertex with inner neighbours u, v (u, v non-mates; "labels"), pi_u the transition matching at u.

## 1. Tools and their status

**1.1 Extension lemma** (known: note 171 section 7, 11/10; NOTE_ASYM_PALEY 7.1). For a partial structure P (decided
pairs, the rest free), Aut(P) permutes the completions, and the stabiliser of a completion G is Aut(P) n Aut(G). For a
Conway graph (Aut = 1, by C2/C3/C7 and Behbahani-Lam) the completions of every P come in free Aut(P)-orbits: their
number is a multiple of |Aut(P)|. A rigid P (one completion) with Aut(P) != 1 is impossible.

**1.2 Eigen-rigidity lemma** (any srg; the general form of the trade lemma of NOTE_LAMBDA1 section 4). Let G, G' be srg
with the same parameters that agree on every pair meeting a vertex set S, and let theta be r or s. If no
theta-eigenvector of G vanishes on S, then G' = G.
*Proof.* A = theta I + c J + (theta' - theta) E', with E' the projection onto the other eigenvalue theta'... more
directly: E_theta is an affine function of A (A = theta' I + (k - theta')J/v + (theta - theta') E_theta), so E_theta and
E'_theta agree on the rows of S. Put U_S = span{E_theta e_i : i in S}; then U = U_S (+) W and U' = U_S (+) W', where W
(resp. W') is the space of theta-eigenvectors of G (resp. G') vanishing on S. W = 0 gives dim U_S = dim U = dim U', so
W' = 0 and E'_theta = E_theta, hence A' = A. QED
Known in substance: it is the star-complement reconstruction theorem (Cvetkovic-Rowlinson-Simic) in srg form; for Conway
it is Codex's route Omega (note 157, 06/10: H = N[v] plus 30 labels, |H| = 45, determines G).

## 2. The window

**2.1 The forced symmetric piece.** For mu = 2 the frame Phi_x (all pairs meeting N[x]) is the same in every graph of
the family up to relabelling (far vertex = label), and Aut(Phi_x) = W(B_m), of order 2^m m!.

**2.2 Rank of the frame.** (A - theta I) e_x is orthogonal to E_theta and supported on N[x], so the rows of N[x] give at
most 2m independent coordinates on E_theta. For Conway the rank on E_(-4) is exactly 14 (Codex, note 157, lemma 1 and its
consequence: the only vectors supported on N[x] in span(1) + E_3 are the multiples of (A + 4I) e_x). The DEFICIT
(dimensions missing for 1.2) is the smaller multiplicity minus 2m:

| m | graph | frame rows | smallest multiplicity | deficit |
|---|---|---|---|---|
| 2 | srg(9,4,1,2) | 5 | 4 (both) | 0 on theta = 1 |
| 7 | srg(99,14,1,2) | 15 | 44 (theta = -4) | 30 |
| 11 | srg(243,22,1,2) | 23 | 110 (theta = -5) | 88 |

The 30 and 88 are Codex's ranks of the Schur complement T on the labels (note 157 section 2.2: T^2 = 7T, rank 30;
BvLS: rank 88). So the window between "forced and symmetric" and "rigid" is exactly the rank-30 tight frame of route Omega.

**Proposition 1 (Paley 9: symmetry forced by rigidity).** In srg(9,4,1,2) the 4 far vertices induce a 4-cycle (k - mu = 2),
which has no eigenvalue 1; so no 1-eigenvector vanishes on N[x], and the frame determines G (1.2). Every element of
W(B2) is then an automorphism (1.1 with a unique completion), and the frames at two vertices are isomorphic, so G is
vertex-transitive: |Aut| >= 9 x 8 = 72. (The combinatorial version is NOTE_ASYM_PALEY 7.3; this is the spectral reason.)

**Proposition 2 (m = 7).** The frame of Conway misses 30 dimensions. In a Conway graph it has at least 99 x 645 120
labelled completions (each vertex of the graph gives one free W(B7)-orbit: the 99 rooted graphs are pairwise
non-isomorphic because Aut = 1). Nothing like Paley 9 can happen at a single vertex.

## 3. Local symmetries that never extend: the flip theorem (proof by hand, new as far as `grep flip` shows)

For a line l = {x, a, a'} the flip s_l fixes x and N(x) - l pointwise, swaps a and a', and sends z_uv to z_(s u)(s v)
(NOTE_ASYM_PALEY section 11; the point reflection sigma_x of Codex's idea F12 is a different element).

**Theorem.** For m >= 3, no flip s_l is an automorphism of an srg(2m^2+1, 2m, 1, 2).
*Proof.* Suppose s_l in Aut(G). It preserves the first-order data, so by the flip lemma (NOTE_ASYM_PALEY 11 (i))
pi_c(a) = a' for every c in N(x) - l: the vertices z_ac and z_a'c are adjacent (their triangle is {c, z_ac, z_a'c}).
Fix such a c. The label neighbours of z_ac are 2m - 2; exactly one contains a (lambda with a) and exactly one contains
a' (mu with a': the second common neighbour of z_ac and a' after a), and the latter is z_a'c. So 2m - 4 >= 2 label
neighbours w of z_ac contain neither a nor a', and s_l fixes each of them. Then w is adjacent to s_l(z_ac) = z_a'c as
well, and the edge z_ac z_a'c lies in two triangles, {c, z_ac, z_a'c} and {w, z_ac, z_a'c}: lambda >= 2. QED
(For m = 2 there is no such w, and the flips are automorphisms of Paley 9, as Proposition 1 requires.)

**Consequences.**
(a) It proves the observation of NOTE_ASYM_PALEY 11 ("the flip is never an automorphism") for the whole family.
(b) At a vertex x on a flat line with condition (ii), the skeleton K_x has at least two completions, G and s_l(G),
    for every m >= 3: first-order data never determines the graph there. This is a negative answer to Codex's question
    on that family of vertices (BvLS, the twin, Gamma3 and Gamma4 all have such vertices).
(c) So "saturation" (every symmetry of K_x extends: |class of x| x |Aut(K_x,x)| = |Aut(G)|, Codex's products for Gamma6,
    Gamma8, hemi378) can only hold away from flat lines. Conjecture S: if no line through x is flat, Aut(K_x, x) =
    Aut(G)_x. True at the four spread-free graphs at 243 (Codex's data); open.
(d) Codex, same day (bridge, `skeleton_completion_theory.json`): BvLS and the twin both have a root with the maximal
    local group W(B11), which forces the same all-flat skeleton; so that skeleton has two NON-ISOMORPHIC completions.
    Stronger than (b) at that skeleton (non-isomorphic, not only relabelled). Codex also: the uniqueness of the
    completions of K_0 in Gamma6 / Gamma8 is OPEN (no certificate found); all eight graphs at 243 have even transport
    circuits (the twin has circuits of length 30, so "multiple of 4" is false).

## 4. What asymmetry can and cannot do for Conway

**Can (proved).**
- Exclude any configuration that is forced, has a symmetry, and is rigid (1.1).
- In any search for completions of a piece P, the group Aut(P) can be broken completely, with STRICT lex-leader
  constraints: no completion of a Conway graph is fixed by a nontrivial element.
- Lemma (99 distinct skeletons). If every skeleton is essentially rigid (its completions form one Aut(K_x, x)-orbit),
  then in a Conway graph the 99 skeletons are pairwise non-equivalent. *Proof.* An equivalence phi: K_x -> K_y gives a
  completion phi(G) of K_y, so phi(G) = tau(G) with tau in Aut(K_y, y); then tau^-1 phi is an automorphism of G sending x
  to y. QED

**Cannot, at the level of one vertex.** The only forced symmetric piece (the frame) is 30 dimensions short of rigidity,
and the simplest first-order symmetries (flips) never extend. So no Paley-9-type forcing exists at a vertex of Conway;
an exclusion through asymmetry needs a mechanism that carries a forced symmetry across those 30 dimensions.

## 5. Targets (theory, no computation)
- T1 (Codex): when does K_x determine G away from flat lines (Conjecture S); flat-line vertices are settled negatively
  by 3(b).
- T2 (me): second order. Is there a forced configuration of several vertices whose pieces carry a common symmetry and
  together reach the rigidity rank (deficit 30)? First candidates: the three points of a line (rows of N[l], 39 vertices,
  rank on E_(-4) at most 36: deficit at least 8), and a grid if one exists (group of order 72).
- T3: a global count: route Omega's first level has 10^11 to 10^12 two-star structures up to symmetry (note 157), and a
  Conway graph forces at least 99 free orbits of rooted solutions; any upper bound below that is an exclusion (no
  method in sight).

# Part 2 (14/10, evening): second order, and Codex's majority theorem

## 6. Codex's extension of the flip theorem (bridge, `pure_flip_majority_theorem.json`; proof re-read, correct)
If g fixes x and every line through x setwise and flips q > 0 of the t = m lines, then q >= ceil(t/2).
Proof: take y = z_ac with a on a flipped line and c on a fixed one; g(y) = z_a'c. Among the 2t - 2 label neighbours of
y, the incidences with the 2q flipped letters number 1 (for a) + 1 (for a') + 2(2q - 2) = 4q - 2, so at least
2t - 4q of them avoid the flipped letters; they are fixed by g, hence common neighbours of y and g(y), and so is c.
Since y and g(y) have at most 2 common neighbours, 2t - 4q <= 1. QED (It does not need the flip lemma; q = 1 is the
flip theorem of section 3.) Consequence: the flip patterns of the automorphisms fixing x and all lines form a binary
code of length t and minimum distance ceil(t/2), of size at most 8 for t = 7 and t = 11.

## 7. Second order: the three points of a line
Notation: l = {x, a, a'}, N[l] = N[x] u L_a u L_a' (39 vertices; L_u = the 12 labels containing u).

**7.1 What is forced.** On L_a u L_a' the graph is tau_a u tau_a' u sigma (Codex note 157 section 2.4): every label of
L_a has one neighbour in L_a, one in L_a', and 10 among the 60 labels that avoid a and a'; every one of those 60 has
exactly 2 neighbours in L_a and 2 in L_a' (mu with a and with a'), and 8 among the 60. Everything else is data of G:
the matchings tau_a, tau_a', the bijection sigma, and the bipartite graph between the 24 labels and the 60.

**7.2 Rank.** The vectors supported on a vertex set Q and orthogonal to E_(-4) form a space of dimension at least
|Q| - 44 (span(1) + E_3 has codimension 44), and it contains (A + 4I) e_u for every u with N[u] in Q. For Q = N[l]:
the three vectors of x, a, a', generically nothing else (Codex: rank 22 on the 24 labels in 99.97 % of random
admissible structures), so the rows of N[l] have rank 36 on E_(-4): deficit 8. Adding one more star, Q = N[l] u N[b]
(49 vertices, b in N(x) - l): at least 49 - 44 = 5 such vectors, four of them from x, a, a', b; with exactly five, the
rank is 44, the full rank, and by 1.2 the rows of these 49 vertices determine G. (This is the forced "extra relation" of
three stars in note 157 section 2.5: it is the 49 - 44 count, a 3-eigenvector supported on N[x] u N[a] u N[a'] u N[b].)

**7.3 Forced symmetry dies at the first gluing.** The forced part of N[l] is three frames, each with a group W(B7); what
glues them (tau_a, tau_a', sigma) is data of G, and the group of the glued piece is the stabiliser of that data. The only
gluing forced to be symmetric is the flat one (flat line with (ii): sigma = rungs z_ac -> z_a'c, tau_a' = sigma tau_a),
whose symmetry is the flip; and the flip already fails on the next layer: z_ac and z_a'c are adjacent, so their 10
neighbours among the 60 are disjoint sets, which the flip would have to exchange with themselves. So in Conway the
window is closed at the first two orders: forced symmetry lives only in single frames (deficit 30), rigidity needs
glued data (deficit 8 for a line, 0 for a line plus one star), and glued data carries no forced symmetry.

**7.4 Two dead ends checked (do not redo).**
- "Near-symmetries must be exact": false. For a transposition sigma = (u w), G and sigma(G) differ on 48 pairs only
  (N(u) and N(w) differ in 24 vertices), and both are Conway graphs: relabelling trades are small, so a small defect
  |G - sigma(G)| forces nothing.
- "Rigid pieces are pairwise non-isomorphic, so their types must be numerous": true whenever the pieces are rigid
  (8316 = 99 x 7 x 12 rooted three-star pieces per graph, pairwise non-isomorphic by 1.1), but the type space of a piece
  with full rows is astronomically larger; no count.

## 8. What is left of the asymmetry lever
Local forcing is excluded at orders 1 and 2 (sections 2, 3, 6, 7). What remains is ABUNDANCE: an asymmetric Conway graph
gives at least 99 x 645 120 labelled completions of the frame, 8316 pairwise distinct rigid three-star pieces, and free
orbits everywhere. The mechanism that makes the known lambda = 1 graphs symmetric is the opposite, SCARCITY (378: about
3.18 million hemisystems under a host group of about 9 million, so every hemisystem has a nontrivial stabiliser). An
exclusion of C1 along this line needs an upper bound on the number of solutions of a symmetric host problem below its
group order; no such bound is in sight without enumeration.
