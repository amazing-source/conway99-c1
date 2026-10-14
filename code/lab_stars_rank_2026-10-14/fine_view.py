"""Fine-space analysis of a four-star structure (14/10/2026).
On F = ker D_S (label vectors on S with zero sum on every letter), K vanishes, so T = 3 - Gamma and U = 4 + Gamma
there; T, U >= 0 force the compression Gamma_F to have its spectrum in [-4, 3].  Prints that spectrum's extremes,
the negative directions of T and U and their split between the fine space and its complement (star space of S),
and how the most negative eigenvector of T distributes over label classes.
usage: python fine_view.py <json with labels and edges> [stars, default 0,1,2,3]"""
import json
import sys
import numpy as np
from stars_rank import kval, LABELS

d = json.load(open(sys.argv[1]))
stars = [int(t) for t in (sys.argv[2] if len(sys.argv) > 2 else "0,1,2,3").split(",")]
S = [frozenset(l) for l in d["labels"]]
n = len(S)
G = np.zeros((n, n))
for i, j in d["edges"]:
    G[i, j] = G[j, i] = 1
T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
D = np.array([[1.0 if y in l else 0.0 for l in S] for y in range(14)])
U_, s_, Vt = np.linalg.svd(D)
r = int(np.sum(s_ > 1e-9))
F = Vt[r:].T            # orthonormal basis of ker D_S
GF = F.T @ G @ F
ev = np.linalg.eigvalsh(GF)
print("dim F = %d; spectrum of Gamma_F: min %.4f, max %.4f; eigenvalues > 3: %s"
      % (F.shape[1], ev[0], ev[-1], ["%.4f" % x for x in ev if x > 3 + 1e-9]))
evT, VT = np.linalg.eigh(T)
neg = [k for k in range(n) if evT[k] < -1e-9]
print("negative eigenvalues of T: %s" % ["%.4f" % evT[k] for k in neg])
for k in neg:
    v = VT[:, k]
    fine = float(np.linalg.norm(F.T @ v) ** 2)
    cls = {"C4": 0.0, "A (X_l outer)": 0.0, "B (X_m outer)": 0.0}
    for i in range(n):
        l = S[i]
        inl, inm = bool(l & {0, 1}), bool(l & {2, 3})
        key = "C4" if (inl and inm) else ("A (X_l outer)" if inl else "B (X_m outer)")
        cls[key] += v[i] ** 2
    print("  eigenvalue %.4f: fine part %.3f, mass by class %s" % (evT[k], fine, {a: round(b, 3) for a, b in cls.items()}))
