"""Per-sector spectra of T and U for a four-star structure invariant under a Klein group (14/10/2026).
Generators: two commuting involutions given as cycle strings (default: the G1 family). For each character sector
(++, -+, +-, --) prints the dimension, the exact nullity of T (Fractions), and the three smallest eigenvalues of T and
of U = 7 Pi_S - T; also the component structure c(l), c(m).
usage: python sector_spec.py <json with labels, edges> [gen1] [gen2]"""
import json
import sys

import numpy as np

from stars_rank import kval, LABELS
from z5_enum import exact_rank


def perm_of(cyc, S, idx):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    return {i: idx[frozenset(h[y] for y in S[i])] for i in range(len(S))}


d = json.load(open(sys.argv[1]))
g1 = sys.argv[2] if len(sys.argv) > 2 else "0,1;4,5;6,7;8,9;10,11;12,13"
g2 = sys.argv[3] if len(sys.argv) > 3 else "2,3;4,5;6,7;8,9;10,11;12,13"
S = [frozenset(l) for l in d["labels"]]
n = len(S)
idx = {l: i for i, l in enumerate(S)}
G = np.zeros((n, n))
for i, j in d["edges"]:
    G[i, j] = G[j, i] = 1
T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
ix = [pos[l] for l in S]
U = 7 * Pi[np.ix_(ix, ix)] - T
a, b = perm_of(g1, S, idx), perm_of(g2, S, idx)
P = lambda m: np.array([[1.0 if m[j] == i else 0.0 for j in range(n)] for i in range(n)])
Pa, Pb = P(a), P(b)
assert np.allclose(Pa @ T, T @ Pa) and np.allclose(Pb @ T, T @ Pb), "structure is not invariant"
M8 = np.rint(8 * T).astype(np.int64)
tot = 0
for sa, sb, name in ((1, 1, "++"), (-1, 1, "-+"), (1, -1, "+-"), (-1, -1, "--")):
    Proj = (np.eye(n) + sa * Pa) @ (np.eye(n) + sb * Pb) / 4
    ev, V = np.linalg.eigh(Proj)
    B = V[:, ev > 0.5]
    # integer basis of the sector: orbit vectors with signs
    rows, seen = [], set()
    for i in range(n):
        orb = (i, a[i], b[i], a[b[i]])
        key = frozenset(orb)
        if key in seen:
            continue
        seen.add(key)
        v = np.zeros(n, dtype=np.int64)
        v[i] += 1
        v[a[i]] += sa
        v[b[i]] += sb
        v[a[b[i]]] += sa * sb
        if np.any(v):
            rows.append(v)
    Bi = np.array(rows).T
    blk = (Bi.T @ M8 @ Bi).tolist()
    nul = len(blk) - exact_rank(blk)
    tot += nul
    eT = np.linalg.eigvalsh(B.T @ T @ B)
    eU = np.linalg.eigvalsh(B.T @ U @ B)
    print("sector %s: dim %d, exact nullity of T %d; T smallest %s; U smallest %s"
          % (name, B.shape[1], nul, ["%.4f" % x for x in eT[:3]], ["%.4f" % x for x in eU[:3]]))
print("total nullity %d" % tot)
