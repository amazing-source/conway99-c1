# Two local conjectures that would exclude Conway's 99-graph (LAB, 15/10/2026, night; Codex out of usage)

Status tags: PROVED (written argument below), VERIFIED (exact computation), EVIDENCE, OPEN. Nothing here excludes
Conway: both conjectures are open. Notation as in NOTE_PROOFS_1410.md: v a vertex, l = {v,a,a'}, m = {v,b,b'} two
lines through v, X_l = L_a u L_a' (24 labels), S4 = X_l u X_m (44 labels), C4 = X_l n X_m, T = 3I - Gamma - K,
U = 7 Pi - T, c(l) = number of components of H_l (lines through v other than l, grouped by components), grid(l,m) = 1
iff C4 is a closed (straight) square, i.e. l, m span a 3 x 3 grid. "Admissible" = (C1), (C1'), (C2) of the generator.

## 1. Forced facts used (all PROVED earlier, with sources)
- G9 (LAB 14/10): in a Conway graph, rank T_S4 = 30 - delta(v,l,m), delta = multiplicity of -4 of the graph induced
  on the 40 outer labels (proof: rank = 30 - dim(V n R^O) and V n R^O = -4-eigenvectors supported on O, -4 being the
  least eigenvalue).
- P3 (Codex, sum of squares): rank T_X_l = 23 - c(l) for every line, in every admissible structure.
- P8/P9: components of H_l correspond to a partition of the 6 other lines at v; a singleton part is a 3 x 3 grid
  (no twisted squares), so g(l) := number of grids containing l = number of singleton parts; c(l) <= g + floor((6-g)/2)
  and g != 5.
- Grids: each grid has 6 lines, so sum over lines of g(l) = 6 rho. Codex's census certificate (exact rational, order-9
  census, not independently reproduced by LAB): 1386 - P - 5 rho >= 0 and P >= 6 rho, hence rho <= 126.

## 2. Conjecture (N9) and its consequence
(N9) For every admissible four-star structure with T_S4 >= 0 and U_S4 >= 0:
        nullity(T_S4) <= 9 + min(c(l), c(m)),   equivalently   rank T_S4 - rank T_X_l >= 12 and the same for m.

Consequence (PROVED, given (N9) and the census bound): in a Conway graph every four-star structure is admissible and
PSD (P1, P10), so 14 + delta = nullity <= 9 + min(c(l), c(m)) gives c(l) >= 5 + delta >= 5 for every line l (choose any
m). A line with c(l) >= 5 has at least four singleton parts, so g(l) >= 4; then 6 rho >= 4 x 231 = 924, rho >= 154,
contradicting rho <= 126. Only proved bounds would give rho <= 191 (6 rho <= P <= 1151), which does not suffice.

EVIDENCE for (N9) (15/10 00:00-00:40 UTC):
- about 83 000 PSD structures visited by PSD-first walks designed to LOWER rank T_S4 - rank T_X (sym4g.py mode
  schur; groups <(0 1)(2 3)>, identity, <(2 3)(outer mates)>; seeds c11, c31, c55, c44), plus about 10 000 saved
  structures: the minimum is exactly 12, never below;
- equality is attained by very different exact witnesses: night_urep_PSD_100.json (c = (5,5), rank 30),
  fourstar_psd_c11_mix6.json (c = (1,1), rank 34), fourstar_psd_c31_mix4.json, and fourstar_psd_asym_c31.json (not
  h-symmetric, VERIFIED exactly);
- U >= 0 is essential: sc_2_null14.json has T >= 0, c = (6,6), nullity 16 > 15, and U has eigenvalue 3 - sqrt 10.
- Weakness: every seed descends from structures of the symmetric family G1; cold starts in small groups do not reach
  positivity, so the PSD set explored may be one connected region.

Structure (EVIDENCE, h-symmetric structures, h = (a a')(b b')): the 12 splits as 9 + (>= 3): the m-odd vectors
f_y = 1_by - 1_b'y (y outer) always add exactly 9 (equivalently no relation has an h-odd part beyond the two star
differences, 'ODD-h'), the m-even vectors add 3 to 6. ODD-h is a statement about a signed graph A^- on 24 vertices
whose spectrum lies in [-4, 3] (odd_quotient.py); it holds on all data but the third odd eigenvalue can be pushed to
0.002 (mode oddgap), so it may fail; (N9) could survive through the even part.

## 3. Conjecture (NOGRID) and a census-free exclusion
(NOGRID) No admissible four-star structure with T, U >= 0 has grid(l,m) = 1.
(LOW) Every admissible four-star structure with T, U >= 0 and c(l), c(m) <= 3 has nullity <= 13 (rank >= 31).

Consequence (PROVED, given (NOGRID) and (LOW)): in a Conway graph every pair of lines at every vertex gives a PSD
four-star structure, so by (NOGRID) no two lines through a vertex span a grid: rho = 0 and every line has c <= 3
(no singleton part). Then (LOW) gives nullity <= 13 at every pair, against nullity = 14 + delta >= 14 (G9). No census
input is used. Also (N9) + (NOGRID) is contradictory (N9 forces grids).

EVIDENCE: (NOGRID): no PSD structure with a grid on (l,m) was ever found (earlier forced-grid searches best -0.35;
15/10: cold forced-grid walks -0.21, repaired seeds -0.51 to -0.57, walks from them about -0.40 after minutes).
(LOW): all PSD data with c <= 3 on both lines have nullity <= 12 ((3,3): 12, (2,3): 11, (1,1): 10); (N9) would give 12.

## 4. What would make this a proof
- (N9), (NOGRID), (LOW) are statements about finitely many 59-vertex configurations; no exhaustive method is in sight.
- Feasible partial goals: (N9) or ODD-h in the h-symmetric family (sector decomposition, signed-graph formulation);
  (NOGRID) using the rigidity a grid imposes (C4 isolated from A u B, equitable partition of P11).
- Independent reproduction of the census bound rho <= 126 (only needed for the (N9) route).
