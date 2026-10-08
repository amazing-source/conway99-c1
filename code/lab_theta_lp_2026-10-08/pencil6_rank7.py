"""C1, lab session, 2026-10-08. Independent re-computation of the laptop session's table: rank mod 7 of the intersection
matrix of grids around a line in six grids (canonical column solution, NOTE 17.46-17.47).
  python pencil6_rank7.py
NEW FACT USED (laptop session): the Gram matrix of any family of kernel vectors has rank <= 56 - r mod 7 (19 at rank 37).
Grids: the six pencil grids P_k; A(r, d) = grid through theta_r on the columns of the grids of the duad d (when it is a
grid). Intersections: P_k, P_j: 3; A(r,d), P_k: 3 if k in d, else 1; A(r,d), A(r,d'): 3 if d, d' meet, else 1;
A(r,d), A(r',d'), r != r': 1 if d, d' disjoint and the syntheme {d, d', rest} is outside the total, else 0.
For each shape of H (the set of duads at a point) the positions are randomised (permutations of the six grids)."""
import random
from itertools import combinations
pts = range(6); duads = [frozenset(d) for d in combinations(pts, 2)]
synth = [frozenset(a) for a in combinations(duads, 3) if len(frozenset().union(*a)) == 6]
total = next(t for t in combinations(synth, 5) if len(frozenset().union(*t)) == 15)
outside = set(s for s in synth if s not in total)
def rank7(M):
    M = [[x % 7 for x in r] for r in M]; n = len(M); rk = 0
    for c in range(n):
        p = next((i for i in range(rk, n) if M[i][c]), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; inv = pow(M[rk][c], 5, 7); M[rk] = [(x * inv) % 7 for x in M[rk]]
        for i in range(n):
            if i != rk and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % 7 for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def gram(Hs):
    G = [("P", k) for k in pts] + [("A", r, d) for r, H in enumerate(Hs) for d in H]
    def ip(x, y):
        if x == y: return 9
        if x[0] == "P" and y[0] == "P": return 3
        if x[0] == "P": x, y = y, x
        if y[0] == "P": return 3 if y[1] in x[2] else 1
        if x[1] == y[1]: return 3 if x[2] & y[2] else 1
        if x[2] & y[2]: return 0
        return 1 if frozenset([x[2], y[2], frozenset(pts) - x[2] - y[2]]) in outside else 0
    return [[ip(x, y) for y in G] for x in G]
SH = {"perfect matching": [(0, 1), (2, 3), (4, 5)], "hexagon": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
      "K_3,3": [(a, b) for a in (0, 1, 2) for b in (3, 4, 5)], "two triangles": [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)],
      "star": [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)], "K_6": list(combinations(range(6), 2))}
random.seed(1); print("pencil alone: 6 grids, rank mod 7 = %d" % rank7(gram([[], [], []])))
for name, E in SH.items():
    for npts in (1, 2, 3):
        rs = set()
        for _ in range(200):
            Hs = []
            for r in range(3):
                if r < npts: pi = random.sample(range(6), 6); Hs.append([frozenset((pi[a], pi[b])) for a, b in E])
                else: Hs.append([])
            rs.add(rank7(gram(Hs)))
        print("H = %-16s at %d point(s): %2d grids, rank mod 7 in %s  %s" % (name, npts, 6 + npts * len(E), sorted(rs), "ALL positions exceed 19" if min(rs) > 19 else ""))
