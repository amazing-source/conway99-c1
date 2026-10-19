"""Independent fast count of the K3-universal 20-vertex level (LAB 19/10/2026), for cross-checking Codex's enumeration.
Normal form: pair core S = Q01 + Q02 (one of the 114 labelled cores of paircores8.json, vertices 0..3 = Q01 corners
(s0, s1), 4..7 = Q02 corners (s0, s2)), D-grids 45, 46, 56.  For each grid, (M, corner map): a perfect matching M of S
inside supp(T) and a bijection of its 4 pairs to the 4 corners satisfying (opp) [a vertex of a pair E K-adjacent to both
ends of a pair F forces E, F to opposite corners].  Triples are combined under M45 + M46 + M56 <= T (each pair at most
T times) and (let) [two labels of grids sharing a line, with the same letter on it, do not carry the same pair].
No residual or other condition: this counts the plain labelled level-20 states, to compare with an enumeration that
uses exactly these conditions.
usage: python k3_level20_fast.py <core indices comma separated | all>"""
import json
import sys
from itertools import combinations, permutations

cores = json.load(open("paircores8.json"))
sel = range(len(cores)) if sys.argv[1] == "all" else [int(x) for x in sys.argv[1].split(",")]
CORN = [(0, 0), (0, 1), (1, 1), (1, 0)]


def adjacent(c, d):
    return (c[0] == d[0]) != (c[1] == d[1])


def matchings(sup, left):
    if not left:
        yield ()
        return
    u = min(left)
    for v in left:
        if v != u and (min(u, v), max(u, v)) in sup:
            for r in matchings(sup, left - {u, v}):
                yield ((min(u, v), max(u, v)),) + r


grand = 0
for ci in sel:
    core = cores[ci]
    nb = [set() for _ in range(8)]
    for i, j in core["edges"]:
        nb[i].add(j); nb[j].add(i)
    T = {tuple(map(int, k.split("-"))): v for k, v in core["T"].items()}
    sup = {p for p, v in T.items() if v > 0}
    opts = []                                   # (M, {pair: corner})
    for M in matchings(sup, frozenset(range(8))):
        for perm in permutations(range(4)):
            cm = {M[i]: CORN[perm[i]] for i in range(4)}
            ok = True
            for E in M:
                for F in M:
                    if E != F and any(F[0] in nb[z] and F[1] in nb[z] for z in E) and adjacent(cm[E], cm[F]):
                        ok = False; break
                if not ok:
                    break
            if ok:
                opts.append((M, cm))
    # letter on shared lines: grid 45 corner (s4, s5), 46 (s4, s6), 56 (s5, s6)
    # 45 & 46 share 4 (coord 0, coord 0); 45 & 56 share 5 (coord 1, coord 0); 46 & 56 share 6 (coord 1, coord 1)

    def let_ok(x, y, kx, ky):
        for E, c in x[1].items():
            d = y[1].get(E)
            if d is not None and c[kx] == d[ky]:
                return False
        return True

    count = 0
    for x in opts:
        T1 = dict(T)
        for p in x[0]:
            T1[p] -= 1
        for y in opts:
            if any(T1[p] < 1 for p in y[0]) or not let_ok(x, y, 0, 0):
                continue
            T2 = dict(T1)
            for p in y[0]:
                T2[p] -= 1
            for z in opts:
                if any(T2[p] < 1 for p in z[0]):
                    continue
                if let_ok(x, z, 1, 0) and let_ok(y, z, 1, 1):
                    count += 1
    grand += count
    print(ci, core["e"], "grid options", len(opts), "level-20 states", count, flush=True)
print("total", grand)
