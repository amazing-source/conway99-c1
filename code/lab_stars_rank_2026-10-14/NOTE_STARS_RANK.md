# The star condition of route Omega, measured (14/10/2026, LAB, evening)

Mandate (user, about 17:00 UTC): attack the 49-vertex object (closed neighbourhood of a line plus one more star), split
with Codex (Codex: the 50 remaining columns). Lab PC free, small computations allowed. All scripts in this folder.

## Setting (checked)
Conway rooted at v; letters 0..13 (mates i, i^1); labels = 84 non-mate pairs. T = 3I - Gamma - K on the labels is the
Schur complement of 3I - A after eliminating N[v]. K_ll' = -1/4 + 3/8 |l n l'| + 1/8 m(l,l'): re-derived by hand from
P^-1 (P = 3I - windmill; letter block Q_yz = -1/16 + 6/16 delta + 2/16 [mates]) and checked numerically (check_K).
T^2 = 7T re-proved (Schur identity plus P^-1 1 = -2 e_v - 1/2 1_N(v)), so T = 7 x projector of rank 30: every principal
submatrix T_S satisfies 0 <= T_S <= 7I and rank T_S <= 30. The star vectors 1_{L_y} lie in ker T_S as soon as the star
counts (C1) hold (checked by hand for the three cases, and asserted in the code).
Admissible structure on a union of stars S: (C1) |N(l) n L_y| = 1 if y or y' is a letter of l, else 2; (C2) shared
letters + common neighbours inside S <= 1 (adjacent) or 2 (not adjacent). These are necessary conditions only, so any
impossibility proved for admissible structures holds for Conway graphs.

## Results
| stars | labels | forced kernel | extra relations needed | random admissible (SAT, random polarity): T_S PSD |
|---|---|---|---|---|
| {0,1} (mates) | 24 | 2 | 0 | 40/40, rank 22 (as Codex, twostar_psd.py) |
| {0,2} | 23 | 2 | 0 | 36/40 (lambda_min down to -0.065) |
| {0,1,2} | 34 | 3 | 1 | 0/40 (lambda_min from -0.94 to -0.28), rank 31 |
| {0,1,2,3} | 44 | 4 | 10 | (search below) |

- Continuous relaxation (lp_cuts.py, Kelley cuts): fractional admissible points with T_S > 0 exist (lambda_perp = 0.36
  at iteration 20). Codex gave the explicit fractional witness T0 = 3 Pi (rank 31). So no exclusion can come from the
  relaxation; integrality is essential.
- Integral, three stars: a large-neighbourhood search (psd_lns.py: SAT re-completion of the pairs touching 6 random
  labels, annealing on lambda_perp = smallest eigenvalue off the star directions) finds PSD admissible structures
  (lns3_psd_found.json: lambda_perp = 0.0028, exact rank 31, 68 edges; nothing special: no rungs, sigma without fixed
  points). Targeting rank 30 (score -|lambda_perp|), three seeds reach |lambda_perp| = 9e-6 to 2e-5 but the exact rank
  (rational elimination of 8 T_S) stays 31: the rank-30 condition is a codimension-one "needle"; not hit by local search.
- Integral, four stars: no PSD structure found. Direct search (four runs, 3000-8000 moves): best lambda_perp -0.26 to
  -0.46. Extension of two PSD three-star bases (psd_extend.py: only the pairs touching the 10 new labels {3,x} move):
  best -0.36 and -0.40 so far.
- The negative directions are spread over the four big classes {a,x}, {a',x}, {b,x}, {b',x} (no rank-one block-letter
  pattern), so no single universal test vector is visible.

## Grid lemma (the mechanism of the extra relation; hand proof, checked exactly on 30 random structures)
Let l = {v,a,a'} and m = {v,b,b'} be two lines through v, and X = {ab, ab', a'b, a'b'} the four "cross" labels.
If l and m span a 3x3 grid, i.e. ab ~ ab' (via a), ab ~ a'b (via b), ab' ~ a'b' (via b'), a'b ~ a'b' (via a'), then
every star count of a cross label towards L_a, L_a', L_b, L_b' is already filled inside X, and T 1_X = 0:
on a cross label, 5/2 - (1 + 1/4) - (1 + 1/4) - (0 + 0) = 0; on a label {a,x}, {a',x}, {b,x} or {b',x} (x outside the two
lines) the four values of K against X are 1/8, 1/8, -1/8, -1/8 and there is no edge to X. So every star set containing
L_a, L_a', L_b gets the relation sum_X eta = 0: three stars have rank 30 as soon as the grid is there.
Check: 30 random admissible three-star structures with the grid square imposed: T 1_X = 0 and exact rank 30 in all 30
(none PSD: positivity is a separate condition).
Why lns3_psd_found has rank 31: it has no grid on (l, m) and no other mechanism: its only relations are the three star
sums. Without a grid, local search reaches |lambda_perp| ~ 1e-5 but never 0 exactly.

## Exact witnesses (z5_enum.py)
Z5 = cyclic shift of the five mate pairs outside l and m. Invariant structures cannot join a fixed label to a 5-orbit
(star counts are 1 or 2), so the cross labels pair among themselves and the grid is forced. Exhaustive enumeration
(first 10 000 invariant structures): ALL have exact rank 30; 595 are also PSD. Three PSD rank-30 examples saved in
z5_psd_rank30_examples.json (69 edges each; in them the three matchings tau pair mates). Sent to Codex for the
column level. So the three-star condition is satisfiable.

## Four stars (two pairs of mate stars, 44 labels, needs 10 relations beyond the stars)
A grid on (l, m) gives one (T 1_X = 0 also holds at four stars: the cross labels' four star counts are filled inside X).
The nine or more others must come from elsewhere; and a Hamming point (all 21 pairs of lines in grids) is excluded in
Conway (Codex's L8), so at every vertex some pairs of lines carry no grid. Searches for a PSD four-star structure:
direct annealing (best lambda_perp -0.35, -0.42), extension of PSD three-star bases (best -0.25, -0.25), Z5-invariant
enumeration (running; none PSD in the first 1500, best -0.16).

## Codex's second condition: T <= 7 Pi (bridge 708; checked)
D = letter-label incidence (14 x 84), Pi = projector onto ker D (rank 70). The star relations say D T = 0, so
im T (in ker D), P = T/7 <= Pi, and U = 7 Pi - T = 7 x (projector of rank 40) is PSD: every principal U_S >= 0, and the
star vectors are also in ker U_S. Effect: my Z5 examples 1 and 2 violate it (lambda_min(U) = -1.37; example 1 is the
one Codex excluded by his sign-vector cut, message 700); example 0, lns3_psd_found and the ten seeds S61-S70 pass.
Z5, first 10 000 three-star structures: 595 with T >= 0, 572 with T >= 0 and U >= 0 (all rank 30 by the grid);
three valid witnesses V0, V7, V15 sent to Codex (message 709), stored in z5_valid_TU.json. On random admissible
structures (2 and 3 stars) U is always PSD: the condition only bites on special structures.
Clean reformulation: on ker D the label graph has exactly two eigenvalues, Pi Gamma Pi = 3 Pi - 7 P (3 with
multiplicity 40, -4 with multiplicity 30), because K = D^T Q D vanishes on ker D. So Gamma is "srg-like" on the
70-dimensional space of zero-letter-sum vectors.

## Two hypotheses that would each exclude C1 (both open; evidence only)
- (H3) If an admissible three-star structure has T_S >= 0 and rank 30, then (l, m) carries the grid.
  With L8 (no Hamming point) this excludes Conway: every three-star set of a Conway graph has rank <= 30.
  Evidence: no non-grid rank-30 structure found (annealing to |lambda| ~ 1e-5; eps = 1 with the square incomplete:
  23/23 rank 31; Codex's exact rank-2 rectangle sweep on lns3_psd_found: 115 admissible rectangles, no PSD rank 30,
  200 PSD-31 states explored). Ten more non-grid seeds S61-S70 (seeds_psd_rank31_nogrid.json) sent to Codex.
- (H4) No admissible four-star structure has T_S >= 0. Evidence: random, annealing, extension of PSD three-star bases,
  Z5 enumeration (42 500 invariant structures, none PSD, best lambda_perp -0.0445, stagnant since 12 000).
  Heuristic reason: within four stars an E-label has about 6 neighbours, so the fine spectrum of Gamma has RMS about
  sqrt(6) ~ 2.45, while T >= 0 caps the fine eigenvalues at 3 (difference directions), 2 or 1 (sum directions) after K;
  at three stars the degree is 4-5 and there is room.
A proof of either needs more than search: the continuous relaxation is feasible (Codex's T0 = 3 Pi), and an exhaustive
enumeration is out of reach (two-star level 1e11-1e12 structures).

## Reading
1. The three-star condition is very selective (random structures are never PSD), but PSD three-star structures exist;
   the exact rank-30 condition is a further codimension-one equation that local search does not hit.
2. Four stars (two pairs of mate stars, 44 labels, rank <= 30: ten relations beyond the stars) look much harder: not
   even PSD so far. IF no admissible four-star structure is PSD, no srg(99,14,1,2) exists (the argument uses only
   lambda = 1, mu = 2 and the spectrum, not the asymmetry). This is EVIDENCE ONLY: local search proves nothing, and an
   exhaustive search is out of reach (two-star level alone: 1e11 to 1e12 structures, Codex note 157). A proof would need
   either a structural argument or an exhaustive search with a much stronger pruning.
3. For route Omega: the three-star filter prunes hard, but its first level (two stars) cannot be enumerated, so the
   route stays unaffordable by brute force; a usable route needs a description of the PSD (rank-30) three-star
   structures, or a direct proof at four stars.
