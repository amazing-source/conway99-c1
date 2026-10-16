# Outline (not written yet): "The asymmetric case of Conway's 99-graph problem reduces to a local symmetry law"

Prepared 16/10 night as the basis for option 1 of the 08:00 report.  Nothing here is new mathematics.  It lists what
is proved, what is conditional, and what is evidence, with sources and statuses.  To be written only on the user's go.

1. Setting.
   - srg(99, 14, 1, 2); the campaign's prior exclusions of automorphisms of orders 2, 3, 7 (C2, C3, C7; papers and
     reviews in work/).  Hence a Conway graph would be asymmetric (C1).  The citation chain for "all prime orders
     excluded" must be checked before writing.
   - Four-star blocks at a vertex v for two lines l, m:
     * 44 labels, T = 3I - Gamma - K, U = 7 Pi - T, both PSD;
     * nullity >= 14 (rank T_S <= 30, from T^2 = 7T).  CONWAY_CONSTRAINTS P1 and G1; P10 spectral form.
2. Proved statements (sources):
   - Side-relation lemma G21: the component vectors are h-homogeneous (H_MATCH_REDUCTION section 6d).
   - Nullity formula nu = 1 + c(l) + dim P, the V4 sign lemma and the V4 reduction (N9NG_ATTACK R1, R5, R6).
   - Proposition: (H-MATCH) at the 21 pairs of one vertex => that vertex is a Hamming point => contradiction with L8
     (Codex note 105, status P), or with Makhnev 1988, or with rho <= 191 (H_MATCH_REDUCTION section 2; adversarially
     reviewed 15/10 06:45).
   - Contrapositive G18 (modulo L10, at most 17 grids per vertex): every vertex of a Conway graph has at least 4 pairs
     of lines whose block is PSD, of nullity >= 14, with star matchings not h-related.
3. Conjecture (H-MATCH) = the 13-wall: a PSD block of nullity >= 14 has h-related star matchings.
   Equivalent forms: broken => nullity <= 13; the sign-lemma form; the contraction form
   (nu = nu(A) + nu(C) + n_1(K) with ||K|| <= 1 and ||Phi_A K Phi_C|| <= 1).
4. Evidence (finite, exact where stated; SAT completeness without certificates):
   - About 700 complete kernel classes: 287 on 15/10, and 413 of the 416 classes of the night of 16/10 (80 at nullity
     13, 10 of 13 at nullity 12, 8 KHOMOG classes of the known broken lineages, 100 + 215 harvested at nullity 14).
     Broken members of nullity >= 14 occur only in obj53, and none of them is PSD.  Broken members of nullity <= 13
     occur in the nullity-12 classes and in the KHOMOG classes, PSD or not.
   - Walks: about 10^5 PSD visits; broken PSD structures reach nullity 13 at most (lineages HB_1, oddw_o9b, sum_hb1,
     fake46), and 11 at most without any h-type symmetry.
   - Closest near-miss: near53/n_45, U at -0.0486.  Codex's integer certificates close all its relabellings.
   - Caveat: the PSD world is reached only near symmetric seeds; no uniform sampling exists.
5. What is missing.
   - A binary / C1 / C2 argument excluding the simultaneous saturation of the two contractions (Codex).
   - Or an exhaustive enumeration, whose size is unknown.
