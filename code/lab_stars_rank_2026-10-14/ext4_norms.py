"""Print the exact norms p^T T_S^+ p (and U-side values) of the (Tr)-survivor profiles for one outer label.
usage: python ext4_norms.py <json> x,y"""
import sys, json, itertools
import numpy as np
from fractions import Fraction as Fr
import ext4
d = json.load(open(sys.argv[1])); u = frozenset(int(t) for t in sys.argv[2].split(","))
S = [frozenset(l) for l in d["labels"]]; n = len(S)
Gl = [[0]*n for _ in range(n)]
for i, j in d["edges"]: Gl[i][j] = Gl[j][i] = 1
G = np.array(Gl, dtype=np.int64)
T = [[(3 if i == j else 0) - Gl[i][j] - ext4.kval(S[i], S[j]) for j in range(n)] for i in range(n)]
U = [[7*ext4.Pi(S[i], S[j]) - T[i][j] for j in range(n)] for i in range(n)]
rT, kT = ext4.rref_kernel(T); rU, kU = ext4.rref_kernel(U)
KTi = ext4.int_rows(kT)
star = {s: [i for i in range(n) if s in S[i]] for s in ext4.STARS}
Lmat = np.array([[1 if z in S[i] else 0 for z in range(14)] for i in range(n)], dtype=np.int64)
rest2 = [i for i in range(n) if 2 in S[i] and not (S[i] & {0, 1})]
rest3 = [i for i in range(n) if 3 in S[i] and not (S[i] & {0, 1})]
K8 = np.array([int(8*ext4.kval(S[i], u)) for i in range(n)], dtype=np.int64)
shared = np.array([len(S[i] & u) for i in range(n)], dtype=np.int64)
needv = np.array([ext4.need(u, z) for z in range(14)], dtype=np.int64)
allX = []
for A0 in itertools.combinations(star[0], 2):
    for A1 in itertools.combinations(star[1], 2):
        base = np.zeros(n, dtype=np.int64); base[list(A0)] = 1; base[list(A1)] = 1
        c2 = int(sum(base[i] for i in star[2])); c3 = int(sum(base[i] for i in star[3]))
        if c2 > 2 or c3 > 2: continue
        for b2 in itertools.combinations(rest2, 2-c2):
            for b3 in itertools.combinations(rest3, 2-c3):
                x = base.copy(); x[list(b2)] = 1; x[list(b3)] = 1
                if np.any((x @ Lmat)[4:] > needv[4:]): continue
                if np.any(x @ G + shared > 2 - x): continue
                allX.append(x)
X = np.array(allX)
R = (8*X + K8[None, :]) @ KTi.T
tr = np.all(R == 0, axis=1)
print("profiles", len(X), "Tr", int(tr.sum()))
# distribution of the number of violated kernel equations
viol = np.sum(R != 0, axis=1)
from collections import Counter
print("number of violated (Tr) equations per profile:", sorted(Counter(viol.tolist()).items()))
for x in X[tr]:
    p = [-int(x[i]) - ext4.kval(S[i], u) for i in range(n)]
    nT = ext4.exact_norm(T, kT, p)
    q = [7*ext4.Pi(S[i], u) - p[i] for i in range(n)]
    nU = ext4.exact_norm(U, kU, q)
    print("nb", [sorted(S[i]) for i in range(n) if x[i]], " 8*normT =", 8*nT, "(target 20);  normU - target =", nU - (7*ext4.Pi(u, u) - (3 - ext4.kval(u, u))))
