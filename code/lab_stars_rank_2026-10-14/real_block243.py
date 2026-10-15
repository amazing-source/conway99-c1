"""Extract the six-star block of a REAL srg(243,22,1,2) at a vertex and three of its lines, in the canonical labelling
of stars_gen.Model(22, 4, -5) (stars 0..5 = the three lines), and check: admissible (SAT with all edge variables fixed),
T and U PSD, nullity, h-relations of the star matchings (h_lm = mate swap on l and m).  Writes the block as json.
usage: python real_block243.py <edges> <vertex> <line indices a,b,c (in sorted order of the lines)> <out json>"""
import itertools
import json
import random
import sys

import numpy as np
from pycryptosat import Solver

from stars_gen import Model

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
x = int(sys.argv[2])
pick = [int(t) for t in sys.argv[3].split(",")]
out = sys.argv[4]
nv = 1 + max(max(e) for e in E)
adj = [set() for _ in range(nv)]
for i, j in E:
    adj[i].add(j)
    adj[j].add(i)
Nx = sorted(adj[x])
mate = {a: [y for y in adj[a] if y in adj[x]][0] for a in Nx}
lines = sorted({tuple(sorted((a, mate[a]))) for a in Nx})
order = [lines[q] for q in pick] + [ln for q, ln in enumerate(lines) if q not in pick]
letter = {}
for t, (a, b) in enumerate(order):
    letter[a], letter[b] = 2 * t, 2 * t + 1
inv = {v: kk for kk, v in letter.items()}
M = Model(22, 4, -5)
S, idx, e, F = M.build([0, 1, 2, 3, 4, 5], random.Random(1))
n = len(S)


def vert(l):
    p, q = sorted(l)
    w = [z for z in adj[inv[p]] & adj[inv[q]] if z != x]
    assert len(w) == 1
    return w[0]


V = [vert(l) for l in S]
G = np.zeros((n, n), dtype=int)
for i, j in itertools.combinations(range(n), 2):
    if V[j] in adj[V[i]]:
        G[i, j] = G[j, i] = 1
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
ok, _ = sol.solve([e[(i, j)] if G[i, j] else -e[(i, j)] for i, j in itertools.combinations(range(n), 2)])
K, Pi = M.matrices(S)
T = 4 * np.eye(n) - G - K
U = 9 * Pi - T
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in range(6)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
lu = float(np.linalg.eigvalsh(Pp @ U @ Pp + 50 * (np.eye(n) - Pp))[0])
nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
rels = []
for (a, a2), (b, b2) in itertools.combinations([(0, 1), (2, 3), (4, 5)], 2):
    hm = {a: a2, a2: a, b: b2, b2: b}
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    starp = [(i, j) for i, j in itertools.combinations(range(n), 2) if S[i] & S[j] & {a, a2, b, b2}]
    rels.append(sum(1 for i, j in starp if G[i, j] != G[hp[i], hp[j]]))
print("vertex %d lines %s: admissible %s, |S| %d, nullity %d, lambda_T %.4f, lambda_U %.4f, star-matching "
      "h-asymmetry for the pairs (lm, ln, mn): %s" % (x, [order[q] for q in range(3)], ok, n, nul, lt, lu, rels))
json.dump({"k": 22, "r": 4, "s": -5, "stars": [0, 1, 2, 3, 4, 5], "labels": [sorted(l) for l in S],
           "edges": [[i, j] for i, j in itertools.combinations(range(n), 2) if G[i, j]], "source": sys.argv[1]},
          open(out, "w"))
