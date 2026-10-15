"""Line invariants in REAL srg(243,22,1,2) graphs (LAB 15/10/2026, calibration of the four-star laws):
for a vertex x and each of its 11 lines l = {x,a,a'}: c(l) = (|X_l| - 1) - rank T_{X_l} (X_l = the 40 labels meeting
a, a'; T = 4I - Gamma - K, K from stars_gen.Model(22, 4, -5)), t(l) = number of letters y off l with {a,y} ~ {a',y}
(transversals), and whether M_a and M_{a'} are mate-aligned.  usage: python lines243.py <edges> [vertices]"""
import itertools
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, '.')
from stars_gen import Model

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in E)
adj = [set() for _ in range(nv)]
for i, j in E:
    adj[i].add(j)
    adj[j].add(i)
nvert = int(sys.argv[2]) if len(sys.argv) > 2 else 3
M = Model(22, 4, -5)
cs, ts = Counter(), Counter()
for x in range(nvert):
    Nx = sorted(adj[x])
    mate = {a: [y for y in adj[a] if y in adj[x]][0] for a in Nx}
    lines = sorted({tuple(sorted((a, mate[a]))) for a in Nx})
    letter = {}
    for t, (a, b) in enumerate(lines):
        letter[a], letter[b] = 2 * t, 2 * t + 1
    inv = {v: k for k, v in letter.items()}

    def vert(l):
        p, q = sorted(l)
        return [z for z in adj[inv[p]] & adj[inv[q]] if z != x][0]

    for t, (a, b) in enumerate(lines):
        la, lb = 2 * t, 2 * t + 1
        X = [l for l in M.labels if l & {la, lb}]
        V = [vert(l) for l in X]
        n = len(X)
        G = np.array([[1.0 if V[j] in adj[V[i]] else 0.0 for j in range(n)] for i in range(n)])
        ii = [M.pos[l] for l in X]
        T = 4 * np.eye(n) - G - M.Kfull[np.ix_(ii, ii)]
        rk = int(np.sum(np.abs(np.linalg.eigvalsh(T)) > 1e-8))
        c = (n - 1) - rk
        tr = sum(1 for y in Nx if y not in (a, b) and [z for z in adj[a] & adj[y] if z != x][0] in
                 adj[[z for z in adj[b] & adj[y] if z != x][0]])
        cs[c] += 1
        ts[tr] += 1
print("%s: %d vertices x 11 lines | c(l) histogram %s | transversals t(l) histogram %s"
      % (sys.argv[1], nvert, dict(sorted(cs.items())), dict(sorted(ts.items()))))
