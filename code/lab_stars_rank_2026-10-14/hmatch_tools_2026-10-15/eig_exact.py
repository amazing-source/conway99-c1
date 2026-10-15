"""Exact rational pencil eigenspaces of T relative to 7 Pi (four-star objects), 15/10/2026."""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval, LABELS, MATE

def rref_null(A):
    A = [r[:] for r in A]; m = len(A); n = len(A[0]); piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
        if r == m: break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * n; v[f] = Fr(1)
        for i, c in enumerate(piv): v[c] = -A[i][f]
        basis.append(v)
    return basis

d = json.load(open(sys.argv[1])); k = int(sys.argv[2])
s = d["structures"][k]; S = [frozenset(l) for l in d["labels"]]; n = len(S)
# exact Pi on S
Dm = [[1 if y in l else 0 for l in S] for y in range(14)]
def Qinv(y, z):
    v = Fr(0)
    if y == z: v += Fr(1, 20) + Fr(1, 24)
    if z == MATE(y): v += Fr(1, 20) - Fr(1, 24)
    return v - Fr(1, 240)
PiS = [[(Fr(1) if a == b else Fr(0)) - sum(Qinv(y, z) for y in S[a] for z in S[b]) for b in range(n)] for a in range(n)]
G = [[0] * n for _ in range(n)]
for i, j in s["edges"]: G[i][j] = G[j][i] = 1
T = [[(3 if a == b else 0) - G[a][b] - Fr(kval(S[a], S[b])).limit_denominator(8) for b in range(n)] for a in range(n)]
print("structure", k, "c", s["c"])
for lam in (Fr(0), Fr(3, 7), Fr(5, 7), Fr(1), Fr(1, 2), Fr(9, 14)):
    A = [[T[a][b] - 7 * lam * PiS[a][b] for b in range(n)] for a in range(n)]
    B = rref_null(A)
    print("lambda", lam, "eigenspace dim (incl. 4 star vectors)", len(B))
    if 0 < lam and len(B) > 4:
        # show vectors orthogonal to stars: pick basis vectors, clear denominators
        import math
        for v in B[:8]:
            den = 1
            for x in v: den = den * x.denominator // math.gcd(den, x.denominator)
            w = [int(x * den) for x in v]
            g = 0
            for x in w: g = math.gcd(g, x)
            w = [x // g for x in w]
            sup = [(sorted(S[i]), w[i]) for i in range(n) if w[i]]
            print("   ", len(sup), sup[:24])
