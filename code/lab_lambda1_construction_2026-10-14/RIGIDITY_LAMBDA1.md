# Why strongly regular graphs with lambda = 1 are rigid, and what that says about asymmetry (C, 14/10/2026)

User (direct, 14/10 ~14:10 UTC): "OUI LANCE b en parallele et ensuite travaille sur C." C = understand why lambda = 1
srgs are rigid and (in all known cases) symmetric; useful for Conway. Codex relays the primary goal: understand the
asymmetry of SRGs fundamentally, lambda = 1 in particular. Everything below is own derivation unless a source is given.

## 1. Trade rigidity (general srg)
**Theorem.** Let G, G' be srg(v,k,lambda,mu) on the same vertex set, G != G', eigenvalues k > r > s, and let T be the
set of vertices incident to a pair on which they differ. For theta in {r, s} let P_theta be the orthogonal projection
onto the theta-eigenvectors of G vanishing outside T. Then:
(a) A(G') - A(G) = (r - s)(P_s - P'_s) = (r - s)(P'_r - P_r) (primes: same objects for G');
(b) P_theta and P'_theta have the same diagonal, and both are nonzero: T carries eigenvectors of BOTH eigenvalues, so
    |T| >= max(sigma_r, sigma_s), sigma_theta = smallest support of a theta-eigenvector of G (an integral vector can be
    taken: the eigenspace is rational, so a minimal-support eigenvector spans a rational line);
(c) every differing pair {i,j} has (P_theta)_ii (P_theta)_jj >= 1/(2(r - s))^2 for theta = r and theta = s;
(d) at most 4 (r - s)^2 (P_theta)_ii pairs differ at the vertex i; and at least 2 when i is in T (degrees are equal).
Proof: NOTE_LAMBDA1 section 4 (the support criterion of NOTE_SPREADFREE section 3 made quantitative). If P_s = 0 then
P'_s has the same (zero) diagonal, so P'_s = 0 and A' = A; likewise for r. QED

## 2. What it says, family by family
| family | r - s | sigma (both eigenvalues) | local moves observed |
|---|---|---|---|
| srg(25,12,5,6) (conference) | 5 | 6 and 6 (MILP, all vertices, exact) | Godsil-McKay switchings with 4-sets, everywhere; asymmetric members one move away |
| srg(243,22,1,2) | 9 | -5 side, BvLS and twin: integral vectors of norm >= 24 (hand argument of 07/10, unrefereed) | trades on thirds (81 vertices), line regions (180) |
| srg(378,52,1,8), S3 hemisystem graph | 15 | -11 side: see section 5 | none below ~280 free vertices (proved for the X_m unions; combinatorially pinned rows down to ~50 kept) |
The conference family has tiny eigenvector supports: switching is cheap there. The lambda = 1 families need large
regions, and inside them the eigenvectors are spread out (concentration fails).

## 3. The microscopic reason: in a lambda <= 1 srg every radius-one structure is forced
* lambda = 1: the local graph G[N(v)] is (k/2)K2 for every v; the mu-graph G[N(x) & N(y)] of a non-adjacent pair is a
  coclique (two adjacent common neighbours z1, z2 would put x and y on the line z1z2, so x = y). lambda = 0: kK1 and
  muK1. So every vertex and every pair "look the same" at radius one: no local invariant varies, colour refinement and
  2-dim WL are blind (checked: 2-WL gives 3 pair colours and one vertex class on the 378 and 243 graphs; exact groups
  needed geometric invariants: prisms, grids).
* The first non-forced data at a vertex x are the matchings pi_a (how the lines through each neighbour a meet the
  lines through x): the 2-factor F_x of note 176 (Codex's skeleton K_x). Everything else is determined by gluing these
  forced pieces, and the gluing is over-determined: a row of a free vertex is pinned by its counts with ~50-60 kept
  vertices (378), ~55 (243).
* lambda = 2 is different: the local graph is 2-regular (a union of cycles) and varies from vertex to vertex; this is
  where asymmetric SRGs abound (Ihringer's switching collections: 68 % of the srg(96,19,2,4) found are asymmetric).

## 4. The three known sources of asymmetric SRGs are closed for lambda = 1
1. Descendants of a regular two-graph at a point of a regular orbit (srg(25,12,5,6), srg(26,10,3,4)): needs k = 2 mu;
   with lambda = mu - 1 = 1 this is only srg(9,4,1,2) (unique, Aut 72).
2. Switching / trades from a symmetric seed (GM, WQH, Pasch switches of Steiner systems, our trades at 243): GM with
   one 4-set needs k <= max(3 mu, lambda + 2 mu + 1, 2 lambda + mu, 3 lambda - 3) (counting identity
   (k - delta)(m - 1) + m n_2m = delta lambda + mu (2m - 1 - delta) - delta(delta - 1) with m = 2); for lambda = 1 this
   fails for every feasible parameter set except the GQ(2,t) (and in the (1,2) family for every set size, k >= 14);
   Pasch configurations do not exist in a partial quadrangle (no triangle of lines); general trades are blocked by
   section 1 (large supports, no concentration).
3. Families with a free combinatorial parameter (Latin squares, nets, Steiner systems, partial geometries): their
   lambda is n - 2 + (m-1)(m-2), (v+3)/2, s - 1 + t(alpha - 1): lambda = 1 only for the 3 x 3 grid and the GQ(2,t).
So the empirical fact "every known lambda = 1 srg is symmetric" is explained by selection: lambda = 1 srgs are only
reachable by global algebraic constructions (GQs and their hemisystems / 3-ovoids, caps and linear representations,
covers), which produce symmetric objects, and none of the three mechanisms that turn symmetric SRGs into asymmetric
ones operates. It is NOT a proof that asymmetric lambda = 1 srgs do not exist.

## 5. Consequences for Conway (srg(99,14,1,2): r = 3, s = -4, r - s = 7)
* Radius-one structures forced (7K2, 2K1); first free data = the matchings (torsion), as in note 176.
* Trade rigidity: two Conway graphs differing on a region T need eigenvectors of both eigenvalues supported in T
  (|T| >= sigma_3 and sigma_-4; integral 3-eigenvectors with entries <= 2 have support >= 12, D4; norm-14
  -4-eigenvectors are co-Heawood configurations on 14 vertices, D2), and a differing pair needs P_ii P_jj >= 1/196.
* With B5 (Aut = 1), an asymmetric Conway graph would be an object of a kind never seen among SRGs: not a two-graph
  descendant, not obtainable by switching from a symmetric one (none exists), not from a free-parameter family. It
  would have to come from a global construction that produces asymmetric objects, which is unknown for lambda = 1.

## 6. The shortest eigenvectors are the trivial ones: pair vectors and relabellings
**Pair vectors (any srg).** On 1-perp, E_s = (A - rI)/(s - r). Hence for two vertices u, w,
x_uw = (A - rI)(e_u - e_w) = 1_N(u) - 1_N(w) - r(e_u - e_w) is an s-eigenvector supported on {u,w} u (N(u) xor N(w)):
support 2 + 2(k - mu) for non-adjacent u, w (378: 90; 243: 42; Conway: 26) and 2(k - lambda) for adjacent ones.
Likewise (A - sI)(e_u - e_w) is an r-eigenvector with the same support. The trade they carry is TRIVIAL: exchanging
the rows of u and w (the transposition (u w), a relabelling) changes exactly the pairs between {u,w} and
N(u) xor N(w).
**Observation (378).** The exact MILP (minsupport.py, HiGHS) on the S3 hemisystem graph returns, for the eigenvalue -11,
vectors of support 90 with entries 4 and 1 (i.e. -11 = s and a = (k - mu)/|s| = 44/11 = 4): exactly the pair vectors
of non-adjacent pairs; nothing shorter within 250 s per anchor (a longer run to prove optimality is in progress).
In the conference family srg(25,12,5,6) the shortest eigenvectors have support 6 for both eigenvalues, far below the
pair support 14: there the short eigenvectors are NON-trivial, and that is where the Godsil-McKay switchings live.
**Correction (15:12 UTC).** The same MILP on BvLS and on the sixth 243-graph (eigenvalue -5, anchor 0, 1200 s each)
returns pair vectors as well (support 42 = 2 + 2(k - mu), entries 5 and 1: an adjacent pair), although trades EXIST
at 243 (thirds, line regions). So "only pair vectors are short" does not by itself mean rigidity. What separates
the cases is CONCENTRATION: there are two ways to carry a trade, (a) short non-trivial eigenvectors (srg(25,12,5,6):
support 6 < 14, Godsil-McKay switchings), (b) regions that carry MANY eigenvectors of both eigenvalues (a third of a
243-graph: 81 vertices carry 10 (-5)-eigenvectors and 20 4-eigenvectors, density 10/81 = 0.12 against the threshold
1/(2(r-s)) = 1/18). The S3 hemisystem graph has neither: its shortest -11-vectors are pair vectors (support 90) and no
region below ~280 vertices carries enough of them (X_m unions: density at most 0.016 against 1/30).

## 7. Rank-2 trades: the simplest genuine trades, and why they are absent here
If the s-eigenvectors supported in the changed region form a line Y = <x>, the theorem forces Y' = <y> with
|y_i| = |x_i| (equal diagonals), y = eps o x (signs flipped on a part S- of the support), and
Delta_ij = 2(r-s) x_i x_j / |x|^2 on the pairs across the split, 0 elsewhere. For a {0,+-1} vector this is integral
iff |x|^2 = 2(r-s) (support 2(r-s): 30 at 378, 18 at 243, 14 at 99, 10 at 25). Conversely such an x, a split, and
(i) A_ij = 0 when x_i x_j = +1 and A_ij = 1 when x_i x_j = -1 across the split, (ii) (A - rI) x_S- = -(|S-|/2) x,
give a new srg A + Delta (its eigenprojections are E_s - xx^T/|x|^2 + yy^T/|y|^2 and the complement).
* 378: shortest -11-vectors have support 90 (pair vectors), so no +-1 vector of norm 30: no rank-2 trade.
* 243 (BvLS, twin): integral -5-vectors have norm >= 24 (hand argument 07/10), so none of norm 18: no rank-2 trade; the
  observed trades have rank 20 (thirds) to 64 (BvLS -> twin).
* Conway: the +-1 vectors of norm 14 are exactly the co-Heawood configurations (D2). Condition (i) on a co-Heawood
  set (points P, blocks Q of the 2-(7,4,2) biplane, x = 1_P - 1_Q) asks that every point of S- n P lie in every block
  of S+ n Q and every block of S- n Q contain every point of S+ n P; with blocks of 4 points, two points in exactly 2
  blocks, this forces S- = empty or S- = P u Q. So a co-Heawood configuration never carries a rank-2 trade: Conway
  graphs are rigid at that scale too.
* Conway, 3-side. Taking as acquired Codex's classification (night journal 14/10): the +-1 integral 3-eigenvectors of
  norm 14 are x = 1_H - 1_H' with H, H' two disjoint H7 configurations (7 vertices, 11 edges, degrees 4,3^6) whose
  centres are adjacent, no other edge between them. On the 3-side the cross pairs get Delta_ij = -x_i x_j, so a cross
  pair inside H (or H') must be an edge and a cross pair between H and H' a non-edge. A split of H into two non-empty
  parts would need a complete bipartite K_{p,7-p} inside H7 (impossible: degrees <= 4 and 11 edges); so H and H' each
  lie on one side, and on different sides the centre edge would be a cross pair: only the trivial split remains.
  Hence a Conway graph carries no rank-2 trade on a {0,+-1} eigenvector of either sign. A rank-2 trade could still use
  a vector with two entry sizes, a on S+ and b on S- with |S+|(a/b) + |S-|(b/a) = 2(r-s) = 14: the pair vectors
  (a = 1 on 24 vertices, b = 3 on u, w) are of this kind and give the transposition (u w); the other two-size vectors
  are not classified here.

## 8. Symmetry from scarcity: why the known lambda = 1 srgs are symmetric
All known lambda = 1 srgs are solutions of an exact problem inside a HOST with a large automorphism group: hemisystems
of a GQ(25,5), 3-ovoids / caps of an affine or projective space, Z3-voltages on Brouwer-Haemers, trades of a fixed
symmetric graph. If H has group K and the problem has N labelled solutions, the orbit of a solution has at most N
elements, so its stabiliser has order >= |K|/N: when N < |K| EVERY solution is symmetric (orbit-stabiliser; the same
principle as the extension lemma of note 171).
| host | |K| | labelled solutions N (exhaustive) | consequence |
|---|---|---|---|
| FTWKB(5), hemisystems | 2^6 3^2 5^6 = 9 000 000 | 2(9e6/600) + 2(9e6/120) + 2(9e6/6) = 3 180 000 (BGR classification) | every hemisystem has a stabiliser of order >= 3 (observed: 6, 120, 600) |
| H(3,25), hemisystems | 2^9 3^4 5^6 7 13 ~ 5.9e10 | ~ 7.7e6 | stabilisers >= 7000 (observed 15120, 15600) |
| Brouwer-Haemers, Z3-voltages | 233 280 | 1154 up to sign (THEOREM_Z3_COVERS) | stabilisers >= 200 (observed >= 864) |
For lambda = 1 the exact problems have very few solutions (the same over-determination as in section 3), far fewer
than the symmetries of their hosts: scarcity forces symmetry. Hemisystems become profuse only for larger q (Bamberg-
Giudici-Royle), where lambda = (q-3)/2 > 1 and small stabilisers do appear (order 3 for K2(7)).
**Consequence for constructions.** An asymmetric lambda = 1 srg cannot come out of a host whose group exceeds the number
of its solutions; it needs a host-free construction, or a host with fewer symmetries than solutions. For Conway no
host is known at all, and B5 says that a Conway graph would be asymmetric: it would be exactly such a host-free,
isolated object.
**Faithfulness (Codex, bridge 14/10, taken as acquired).** The stabiliser of a solution S acts on the induced graph
through K_S / K_(S) (K_(S) = pointwise stabiliser). For a hemisystem it acts faithfully: a hemisystem line through each
point recovers the point as an intersection of two concurrent hemisystem lines (my argument), equivalently every point
outside S has 78 neighbours in S and two points share at most 26 (Codex). General form (Codex): an m-ovoid of a GQ(s,t)
determines the host as soon as m(t+1) > max(s-1, t+1). So scarcity (N < |K|) gives a non-trivial automorphism of the
induced graph itself; an asymmetric induced graph needs a regular orbit of solutions (N >= |K| is only necessary), and
a regular orbit still allows "internal" automorphisms that do not extend to the host.
