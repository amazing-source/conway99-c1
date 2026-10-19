"""Independent check (LAB 19/10/2026) of Codex's Q_bc-factor lemma for a pair core S = Q01 + Q02 with Q12 a grid.
Every D-label (24, covering the deficits T exactly) has exactly one neighbour in the grid Q12 (perfect domination: it is
not adjacent to the letters of lines 1, 2), at a corner h = (s1, s2).  For a core vertex v and a corner h, v !~ h and the
common neighbours of v and h are the shared letters and D-labels only (a label adjacent to h has no letter on 1 or 2,
so it is a D-label, or it is in Q0j with no core neighbour), hence deg_{T_h}(v) = 2 - |letters(v) cap letters(h)|.
Two D-labels with the same core pair and the same corner h would give v, v', h as three common neighbours: each T_h is
simple.  So T = T_00 + T_01 + T_10 + T_11 with prescribed degrees and simple factors.
Counts, for the 114 cores, how many admit such a decomposition (exhaustive backtracking).  Codex (19/10): all but the
orbits 20 and 23 (6 labelled cores).
usage: python q12_factor_check.py"""
import json
from itertools import combinations

cores = json.load(open("paircores8.json"))
orb = json.load(open("paircore_orbits16.json"))["orbit_of"]
V = [("A", s, t) for s in (0, 1) for t in (0, 1)] + [("B", s, t) for s in (0, 1) for t in (0, 1)]
H = [(s1, s2) for s1 in (0, 1) for s2 in (0, 1)]


def need(v, h):
    side, s0, t = V[v]
    share = (side == "A" and t == h[0]) or (side == "B" and t == h[1])
    return 2 - (1 if share else 0)


ok_cores, bad = [], []
for ci, core in enumerate(cores):
    T = {tuple(map(int, k.split("-"))): v for k, v in core["T"].items()}
    units = [p for p, v in T.items() for _ in range(v)]
    deg = {(v, h): need(v, H[h]) for v in range(8) for h in range(4)}
    used = set()
    found = [False]

    def rec(i):
        if found[0]:
            return
        if i == len(units):
            found[0] = all(deg[k] == 0 for k in deg); return
        u, w = units[i]
        for h in range(4):
            if deg[(u, h)] > 0 and deg[(w, h)] > 0 and ((u, w), h) not in used:
                deg[(u, h)] -= 1; deg[(w, h)] -= 1; used.add(((u, w), h))
                rec(i + 1)
                deg[(u, h)] += 1; deg[(w, h)] += 1; used.discard(((u, w), h))
                if found[0]:
                    return
    rec(0)
    (ok_cores if found[0] else bad).append(ci)
print("cores with a Q12-factor decomposition:", len(ok_cores), "without:", len(bad), bad)
print("orbits (order-16 group) of the cores without:", sorted({orb[str(c)] if isinstance(next(iter(orb)), str) else orb[c] for c in bad}))
