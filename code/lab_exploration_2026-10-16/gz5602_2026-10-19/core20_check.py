"""Independent check (LAB 19/10/2026) of the 20-vertex level of Codex's 5602 analysis: core S = Q03 + Q12 (8 labels)
plus the 12 labels of the three C3 grids G45, G46, G56.  Facts (proved here, see NUIT_2026-10-19.md section 7):
  * outside S only the C3-grid labels have 2 neighbours in S (the 48 Q_aj labels have 1, the C4-grid labels 0), so for
    two core vertices y != z the common neighbours outside S that are not letters all lie in C3 grids:
        T_yz := 2 - K_yz - (K^2)_yz - (common letters) = number of C3-grid labels adjacent to both  (equality);
  * each C3 grid dominates S perfectly: its 4 labels pair S into 4 pairs (a perfect matching P_g of the 8 vertices);
    hence P45 + P46 + P56 = T off the diagonal;
  * a grid label sits at a corner (s_a, s_b) of its grid; the 4 corners form the 4-cycle 00-01-11-10;
  * (opp) if a core vertex z in the pair E is K-adjacent to both ends of the pair F of the same grid, the corners of E
    and F are opposite (mu(z, g_F) = 2 would be exceeded by g_E);
  * (let) two C3-grid labels of different grids sharing a letter (same s on the common line) are not adjacent and have
    that letter as a common neighbour, so their core pairs share at most one vertex.
Counts the labelled 20-vertex configurations and their orbits under the 128 letter exchanges (one per line).
Codex (19/10): 4 core orbits survive, 1328 representatives in all at 20 vertices."""
import json
import sys
from itertools import combinations, permutations, product
from collections import Counter

sys.setrecursionlimit(10000)
V = [("A", a, b) for a in (0, 1) for b in (0, 1)] + [("B", a, b) for a in (0, 1) for b in (0, 1)]


def letters(v):
    return {(0, v[1]), (3, v[2])} if v[0] == "A" else {(1, v[1]), (2, v[2])}


pairs8 = list(combinations(range(8), 2))


def cubic_cores():
    out = []
    deg = [0] * 8
    adj = [[0] * 8 for _ in range(8)]

    def check():
        nb = [set(j for j in range(8) if adj[i][j]) for i in range(8)]
        for i, j in pairs8:
            c = len(nb[i] & nb[j]); share = bool(letters(V[i]) & letters(V[j]))
            if c > ((0 if share else 1) if adj[i][j] else (1 if share else 2)):
                return False
        for i in range(8):
            own = {l[0] for l in letters(V[i])}
            for line in range(4):
                for s in (0, 1):
                    if sum(1 for j in nb[i] if (line, s) in letters(V[j])) > (1 if line in own else 2):
                        return False
        return True

    def rec(p):
        if p == len(pairs8):
            if all(d == 3 for d in deg) and check():
                eA = sum(adj[i][j] for i, j in pairs8 if i < 4 and j < 4)
                if eA == 2:                         # e = 2 forced: e = 3 by E3, e = 4 by non-grid, e <= 1 impossible
                    out.append(frozenset((i, j) for i, j in pairs8 if adj[i][j]))
            return
        i, j = pairs8[p]
        for val in (1, 0):
            if val and (deg[i] == 3 or deg[j] == 3):
                continue
            adj[i][j] = adj[j][i] = val; deg[i] += val; deg[j] += val
            left = [0] * 8
            for (a, b) in pairs8[p + 1:]:
                left[a] += 1; left[b] += 1
            if all(deg[v] + left[v] >= 3 for v in range(8)):
                rec(p + 1)
            deg[i] -= val; deg[j] -= val; adj[i][j] = adj[j][i] = 0
    rec(0)
    return out


def matchings(support):
    """perfect matchings of {0..7} using only pairs in support"""
    res = []

    def rec(left, cur):
        if not left:
            res.append(frozenset(cur)); return
        a = min(left)
        for b in left:
            if b != a and (min(a, b), max(a, b)) in support:
                rec(left - {a, b}, cur + [(min(a, b), max(a, b))])
    rec(frozenset(range(8)), [])
    return res


GRIDS = [(4, 5), (4, 6), (5, 6)]
CORNERS = [(0, 0), (0, 1), (1, 1), (1, 0)]                  # 4-cycle order; opposite = index differs by 2


def adjacent_corners(c, d):
    return (c[0] == d[0]) != (c[1] == d[1])


cores = cubic_cores()
print("cores e=2:", len(cores), flush=True)
configs = []
for K in cores:
    nb = [set() for _ in range(8)]
    for i, j in K:
        nb[i].add(j); nb[j].add(i)
    T = {}
    for i, j in pairs8:
        T[(i, j)] = 2 - (1 if (i, j) in K else 0) - len(nb[i] & nb[j]) - len(letters(V[i]) & letters(V[j]))
    if any(v < 0 for v in T.values()):
        continue
    sup = {p for p, v in T.items() if v > 0}
    M1s = matchings(sup)
    for P1 in M1s:
        T1 = {p: T[p] - (p in P1) for p in T}
        for P2 in matchings({p for p, v in T1.items() if v > 0}):
            T2 = {p: T1[p] - (p in P2) for p in T1}
            P3 = frozenset(p for p, v in T2.items() if v > 0)
            if any(v not in (0, 1) for v in T2.values()) or len(P3) != 4 or len(set(x for p in P3 for x in p)) != 8:
                continue
            # corner assignments per grid: bijection pairs -> corners with (opp)
            per_grid = []
            for P in (P1, P2, P3):
                Pl = sorted(P)
                opts = []
                for perm in permutations(range(4)):
                    corner = {Pl[k]: CORNERS[perm[k]] for k in range(4)}
                    ok = True
                    for E in Pl:
                        for F in Pl:
                            if E == F:
                                continue
                            if any(F[0] in nb[z] and F[1] in nb[z] for z in E) and adjacent_corners(corner[E], corner[F]):
                                ok = False; break
                        if not ok:
                            break
                    if ok:
                        opts.append(corner)
                per_grid.append(opts)
            for assign in product(*per_grid):
                ok = True
                for (g1, g2) in combinations(range(3), 2):
                    common = set(GRIDS[g1]) & set(GRIDS[g2])
                    (line,) = common
                    k1 = GRIDS[g1].index(line); k2 = GRIDS[g2].index(line)
                    for E, c in assign[g1].items():
                        for F, d in assign[g2].items():
                            if c[k1] == d[k2] and len(set(E) & set(F)) > 1:
                                ok = False; break
                        if not ok:
                            break
                    if not ok:
                        break
                if ok:
                    configs.append((K, assign))
print("labelled 20-vertex configurations:", len(configs), flush=True)


# orbits under the 128 letter exchanges: exchange of line a maps s_a -> 1 - s_a in every vertex using line a
def act(flip, K, assign):
    def mv(i):
        t, a, b = V[i]
        if t == "A":
            a ^= flip[0]; b ^= flip[3]
        else:
            a ^= flip[1]; b ^= flip[2]
        return V.index((t, a, b))
    K2 = frozenset(tuple(sorted((mv(i), mv(j)))) for i, j in K)
    A2 = []
    for g, corner in enumerate(assign):
        la, lb = GRIDS[g]
        A2.append(tuple(sorted((tuple(sorted((mv(E[0]), mv(E[1])))), (c[0] ^ flip[la], c[1] ^ flip[lb])) for E, c in corner.items())))
    return (tuple(sorted(K2)), tuple(A2))


flips = list(product((0, 1), repeat=7))
canon = Counter()
for K, assign in configs:
    canon[min(act(f, K, assign) for f in flips)] += 1
print("orbits under the 128 letter exchanges:", len(canon))
core_orbits = Counter(min(tuple(sorted(act(f, K, ({}, {}, {}))[0])) for f in flips) for K, _ in configs)
print("distinct core orbits among surviving configurations:", len(core_orbits))
