"""The 59-vertex induced graph H = {v} + 14 letters + the 44 labels of S (LAB 15/10/2026).
Schur complements: U_S is the Schur complement of 4I + A_H on S (4I + W > 0, W = windmill, lambda_min(W) = -3.27), and
T_S that of 3I - A_H (3I - W has exactly one negative eigenvalue).  Hence  U >= 0 <=> lambda_min(H) >= -4,
T >= 0 <=> lambda_2(H) <= 3,  nu = multiplicity of 3 in H  (checked numerically here).  For each structure: the
spectrum ends of H, multiplicities of 3 and -4, and the weights of the lowest eigenvector on v / star letters /
outer letters / l-labels / m-labels / C4.
usage: python h59.py <json or dir> [...]"""
import glob, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, '..')
from stars_rank import kval
files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
tab = Counter(); out = []
for f in files:
    d = json.load(open(f))
    if "edges" not in d:
        continue
    S = [frozenset(l) for l in d["labels"]]; n = len(S)
    N = 15 + n
    A = np.zeros((N, N))
    for y in range(14):
        A[0, 1 + y] = A[1 + y, 0] = 1
        A[1 + y, 1 + (y ^ 1)] = 1
    for i, s in enumerate(S):
        for y in s:
            A[1 + y, 15 + i] = A[15 + i, 1 + y] = 1
    for a, b in d["edges"]:
        A[15 + a, 15 + b] = A[15 + b, 15 + a] = 1
    w, V = np.linalg.eigh(A)
    m3 = int(np.sum(np.abs(w - 3) < 1e-8)); m4 = int(np.sum(np.abs(w + 4) < 1e-8))
    K = np.array([[kval(a, b) for b in S] for a in S])
    G = A[15:, 15:]
    T = 3 * np.eye(n) - G - K
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    x = V[:, 0] ** 2
    grp = {"v": x[0], "star letters": x[1:5].sum(), "outer letters": x[5:15].sum()}
    for i, s in enumerate(S):
        k = "C4" if (s & {0, 1}) and (s & {2, 3}) else ("l-labels" if s & {0, 1} else "m-labels")
        grp[k] = grp.get(k, 0) + x[15 + i]
    key = (nu, m3, "lam2 %.3f" % w[-2], "lmin %.4f" % w[0], "m(-4) %d" % m4)
    tab[key] += 1
    out.append((f, w[0], grp))
for k, v in sorted(tab.items(), key=lambda kv: -kv[1]):
    print("  (nu from T, mult of 3 in H, lambda_2, lambda_min, mult of -4):", k, v)
for f, l0, g in out[:3]:
    print("  %s lowest eigenvector weights:" % f.split('/')[-1], {k: round(v, 3) for k, v in g.items()})
