"""Lab session, 2026-10-13. Type II over Z_3^4 closed by the trace condition (NOTE_SPREADFREE.md section 6k).
For a tri-Cayley graph of type II over Z_3^4, D_ii = +-{a_i, b_i} (two projective points of PG(3,3)). For a non-trivial
character chi with kernel the hyperplane h, chi(D_ii) = 3 n_i - 2 with n_i = number of the points a_i, b_i in h, and the
3x3 matrix (chi(D_ij)) has eigenvalues in {4, -5}, so its trace 3 (n_0 + n_1 + n_2) - 6 is 12, 3, -6 or -15: every
hyperplane contains 0, 3 or 6 of the six points (with multiplicity). Exhaustive check: with D_00 = {e1, e2} fixed,
which pairs (D_11, D_22) satisfy this for the 40 hyperplanes?   python -I type2_trace.py"""
import itertools
V = [v for v in itertools.product(range(3), repeat=4) if any(v)]
pts = [v for v in V if v < tuple((-x) % 3 for x in v)]                 # 40 projective points
hyps = pts                                                            # hyperplanes y^perp, y a projective point
inc = {(p, h): sum(a * b for a, b in zip(p, h)) % 3 == 0 for p in pts for h in hyps}
P0 = [(0, 0, 0, 1), (0, 0, 1, 0)]                                      # any two points; the general linear group is 2-transitive on points
base = [sum(inc[(p, h)] for p in P0) for h in hyps]
pairs = list(itertools.combinations(pts, 2)); cnt = {pr: [inc[(pr[0], h)] + inc[(pr[1], h)] for h in hyps] for pr in pairs}
good = []
for p1 in pairs:
    c1 = [b + x for b, x in zip(base, cnt[p1])]
    for p2 in pairs:
        if all((a + b) % 3 == 0 for a, b in zip(c1, cnt[p2])): good.append((p1, p2))
print("pairs (D_11, D_22) compatible with the trace condition on all 40 hyperplanes: %d" % len(good))
for g in good: print("   D_11 = %s, D_22 = %s  (D_00 = %s)" % (g[0], g[1], tuple(P0)))
