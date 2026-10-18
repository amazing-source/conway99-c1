"""Pair core + six D-grids (LAB 19/10/2026): templates whose grid graph contains a K4 on D = {0,1,2,3} and exactly one
edge (b, c) = (4, 5) of the complementary triangle, so that the universal relations give H_46 = -H_56 (pair core
S = Q46 + Q56, shared line a = 6) and all six rectangles avoiding a, b, c are grids (7063, 9386, 9419, 9843, 9849,
9958, 9978 among the open c3 templates).
Facts (paircore8_check.py and NUIT_2026-10-19.md section 7): S induces a 2-regular graph (114 labelled cores); every
outside label of a D-rectangle has exactly 2 neighbours in S, the others at most 1; so the deficits
T_yz = 2 - K_yz - (K^2)_yz - (common letters) of the pairs of S are covered EXACTLY by the 24 D-grid labels; each
D-grid dominates S perfectly (its labels pair S: a perfect matching M_jk), hence sum_jk M_jk = T.
Corner conditions inside each grid (opp) and between grids sharing a line (let), as in core20_check.py.
Counts the labelled 32-vertex configurations (core + the six D-grids).
usage: python paircore32_k4.py [max_cores]"""
import json
import sys
from itertools import combinations, permutations

a, b, c = 6, 4, 5
D = [0, 1, 2, 3]
DGRIDS = list(combinations(D, 2))
cores = json.load(open("paircores8.json"))
V = [("A", s, t) for s in (0, 1) for t in (0, 1)] + [("B", s, t) for s in (0, 1) for t in (0, 1)]   # A(s_a, s_b), B(t_a, s_c)
CORNERS = [(0, 0), (0, 1), (1, 1), (1, 0)]


def adjacent_corners(x, y):
    return (x[0] == y[0]) != (x[1] == y[1])


def matchings(T, left):
    if not left:
        yield []
        return
    u = min(left)
    for v in left:
        if v != u and T.get((min(u, v), max(u, v)), 0) > 0:
            for rest in matchings(T, left - {u, v}):
                yield [(min(u, v), max(u, v))] + rest


def decompositions(T, k):
    """ordered lists of k perfect matchings with sum T"""
    if k == 0:
        if all(v == 0 for v in T.values()):
            yield []
        return
    for M in matchings(T, frozenset(range(8))):
        T2 = dict(T)
        for p in M:
            T2[p] -= 1
        for rest in decompositions(T2, k - 1):
            yield [M] + rest


maxc = int(sys.argv[1]) if len(sys.argv) > 1 else len(cores)
total = 0
per_core = []
for ci, core in enumerate(cores[:maxc]):
    K = {tuple(e) for e in core["edges"]}
    nb = [set() for _ in range(8)]
    for i, j in K:
        nb[i].add(j); nb[j].add(i)
    T = {tuple(map(int, k.split("-"))): v for k, v in core["T"].items()}
    if any(v < 0 for v in T.values()):
        per_core.append(0); continue
    count = 0
    for dec in decompositions(T, 6):
        # corner options per grid
        opts = []
        for M in dec:
            Ms = sorted(M)
            ok_list = []
            for perm in permutations(range(4)):
                corner = {Ms[i]: CORNERS[perm[i]] for i in range(4)}
                good = True
                for E in Ms:
                    for F in Ms:
                        if E != F and any(F[0] in nb[zv] and F[1] in nb[zv] for zv in E) and adjacent_corners(corner[E], corner[F]):
                            good = False; break
                    if not good:
                        break
                if good:
                    ok_list.append(corner)
            opts.append(ok_list)
        if any(not o for o in opts):
            continue
        # backtracking over grids with the (let) condition between grids sharing a line
        def rec(g, chosen):
            global count
            if g == 6:
                return 1
            n = 0
            for corner in opts[g]:
                ok = True
                for h in range(g):
                    common = set(DGRIDS[g]) & set(DGRIDS[h])
                    if not common:
                        continue
                    (line,) = common
                    kg, kh = DGRIDS[g].index(line), DGRIDS[h].index(line)
                    for E, x in corner.items():
                        for F, y in chosen[h].items():
                            if x[kg] == y[kh] and len(set(E) & set(F)) > 1:
                                ok = False; break
                        if not ok:
                            break
                    if not ok:
                        break
                if ok:
                    n += rec(g + 1, chosen + [corner])
            return n
        count += rec(0, [])
    per_core.append(count)
    total += count
    print("core", ci, "e", core["e"], "configurations", count, flush=True)
print("total labelled 32-vertex configurations over", len(per_core), "cores:", total)
