"""Even absorption test (LAB 15/10/2026).  For a four-star structure (stars 0,1 = line l, 2,3 = line m), put
B = X_l + span(f_y) (f_y = 1_{2y} - 1_{3y}, y outer) and g_y = 1_{2y} + 1_{3y} (m-even, y outer).  With T >= 0, the
T-Gram of the g's splits as G_g = E_g + S_g, E_g = explained part (Gram of the T-projections of the g's onto B) and
S_g >= 0 the Schur complement; rank S_g = even gain beyond B.  ||g_y||^2_T = 5/2 if {2,y} ~ {3,y} (transversal of m at
y), 9/2 otherwise.  Question: is the explained part bounded (diag E_g <= 5/2?), so that full absorption forces
transversals?  Prints, per structure: c, t(m), even gain, max diag E_g, max eigenvalue of E_g, and for transversal /
non-transversal letters the range of diag E_g.
usage: python even_explained.py <json> [...]  (structures: top-level 'edges' or a 'structures' list)"""
import json
import sys

import numpy as np

from stars_rank import kval


def items(f):
    d = json.load(open(f))
    if "edges" in d:
        yield f, d["labels"], d["edges"]
    else:
        for k, st in enumerate(d.get("structures", [])):
            yield "%s[%d]" % (f, k), d["labels"], st["edges"]


for f in sys.argv[1:]:
    for name, labels, edges in items(f):
        S = [frozenset(l) for l in labels]
        n = len(S)
        idx = {s: i for i, s in enumerate(S)}
        G = np.zeros((n, n))
        for i, j in edges:
            G[i, j] = G[j, i] = 1
        K = np.array([[kval(a, b) for b in S] for a in S])
        T = 3 * np.eye(n) - G - K
        Xl = [i for i in range(n) if S[i] & {0, 1}]
        Bv = [np.eye(n)[i] for i in Xl]
        F, Gv, trans = [], [], []
        for y in range(4, 14):
            a, b = idx[frozenset((2, y))], idx[frozenset((3, y))]
            v = np.zeros(n); v[a] = 1; v[b] = -1; F.append(v)
            w = np.zeros(n); w[a] = 1; w[b] = 1; Gv.append(w)
            trans.append(G[a, b] == 1)
        B = np.array(Bv + F).T
        Gm = np.array(Gv).T
        GB = B.T @ T @ B
        wB, VB = np.linalg.eigh(GB)
        keep = wB > 1e-9
        C = B.T @ T @ Gm
        W2 = VB[:, keep].T @ C
        E = W2.T @ (W2 / wB[keep][:, None])
        Gg = Gm.T @ T @ Gm
        Sg = Gg - E
        gain = int(np.sum(np.linalg.eigvalsh(Sg) > 1e-7))
        dE = np.diag(E)
        tr = [dE[k] for k in range(10) if trans[k]]
        nt = [dE[k] for k in range(10) if not trans[k]]
        print("%s: t(m) %d, even gain %d, max diag E %.4f, lambda_max E %.4f | diag E transversal %s | non-transversal %s"
              % (name, sum(trans), gain, dE.max(), np.linalg.eigvalsh(E).max(),
                 ("[%.3f, %.3f]" % (min(tr), max(tr))) if tr else "-", ("[%.3f, %.3f]" % (min(nt), max(nt))) if nt else "-"))
