"""'Odd' test vectors at four stars (14/10/2026). e_x = 1_{0x} - 1_{1x} (x off l), f_y = 1_{2y} - 1_{3y} (y off m).
Their T-Gram matrix is [[G_e, -C], [-C^T, G_f]] with G_e = 6I - J/2 - P_tau0 - P_tau1 + P_sigma + P_sigma^T
(diagonal 11/2 + 2 t_x, t_x = 1 at a transversal) and C_xy = G(0x,2y) - G(0x,3y) - G(1x,2y) + G(1x,3y).
In a Conway graph this 24 x 24 matrix is PSD (T >= 0 globally); so ||C||_* <= sqrt((66 + 2 t(l)) (66 + 2 t(m))).
usage: python odd_gram.py <json with labels and edges> ..."""
import json
import sys
import numpy as np
from stars_rank import kval

for f in sys.argv[1:]:
    d = json.load(open(f))
    edges = d["edges"] if "edges" in d else (d["structures"][0]["edges"] if "structures" in d else d["best"]["edges"])
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    idx = {l: i for i, l in enumerate(S)}
    G = np.zeros((n, n))
    for i, j in edges:
        G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    xs = [x for x in range(14) if x not in (0, 1)]
    ys = [y for y in range(14) if y not in (2, 3)]
    vecs = []
    for x in xs:
        v = np.zeros(n)
        v[idx[frozenset((0, x))]] = 1
        v[idx[frozenset((1, x))]] = -1
        vecs.append(v)
    for y in ys:
        v = np.zeros(n)
        v[idx[frozenset((2, y))]] = 1
        v[idx[frozenset((3, y))]] = -1
        vecs.append(v)
    V = np.array(vecs).T
    Gr = V.T @ T @ V
    tl = sum(1 for x in xs if G[idx[frozenset((0, x))], idx[frozenset((1, x))]])
    tm = sum(1 for y in ys if G[idx[frozenset((2, y))], idx[frozenset((3, y))]])
    C = -Gr[:12, 12:]
    nuc = np.linalg.svd(C, compute_uv=False).sum()
    ev = np.linalg.eigvalsh(Gr)
    print("%-26s t = (%d,%d): lambda_min of the odd Gram %.4f; ||C||_* = %.3f vs bound %.3f"
          % (f, tl, tm, ev[0], nuc, np.sqrt((66 + 2 * tl) * (66 + 2 * tm))))
