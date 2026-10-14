"""Sector analysis of symmetric three-star structures with an extra relation (14/10/2026): for each saved structure,
the smallest eigenvalues of T and U restricted to the even and odd sectors of the swap h (stars removed).
usage: python sector_view.py <found json> ..."""
import json
import sys
import numpy as np
from stars_rank import kval, LABELS

D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    idx = {l: i for i, l in enumerate(S)}
    h = {i: i for i in range(14)}
    for c in d["h"].split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    P = np.zeros((n, n))
    for i in range(n):
        P[idx[frozenset(h[y] for y in S[i])], i] = 1
    Pe, Po = (np.eye(n) + P) / 2, (np.eye(n) - P) / 2
    ix = [pos[l] for l in S]
    PiS = Pi[np.ix_(ix, ix)]
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2)]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    for rec in d["found"]:
        G = np.zeros((n, n))
        for i, j in rec["edges"]:
            G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
        U = 7 * PiS - T
        out = []
        for name, M in (("T", T), ("U", U)):
            for sname, Ps in (("even", Pe), ("odd", Po)):
                Q = Pp @ Ps
                ev, V = np.linalg.eigh(Q @ M @ Q.T)
                # keep eigenvectors living in the sector and off the stars
                keep = [k for k in range(n) if np.linalg.norm(Q @ V[:, k] - V[:, k]) < 1e-6
                        and np.linalg.norm(V[:, k]) > 0.5]
                vals = sorted(ev[keep])
                nz = [x for x in vals if abs(x) > 1e-9]
                out.append("%s-%s min %.4f" % (name, sname, nz[0] if nz else float('nan')))
        print("%s move %d: %s" % (f, rec["move"], ", ".join(out)))
