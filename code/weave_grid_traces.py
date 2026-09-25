# Exact check of the holonomy trace inequality used for the {2,9} case.
# Grid K3xK3 on Z3^2, A = rook adjacency. V+ = eigenvalue 1 (4-dim), V- = eigenvalue -2 (4-dim).
# For every automorphism g: alpha = tr(g|V+), beta = tr(g|V-).  Claim: beta - alpha/2 <= 2.
# Also: every anti-isomorphism (A -> J-I-A) has trace 0 on V+ and on V- (it swaps them).
import itertools
from fractions import Fraction as F
pts = [(r, c) for r in range(3) for c in range(3)]
n = 9
A = [[int(p != q and (p[0] == q[0] or p[1] == q[1])) for q in pts] for p in pts]
I = [[int(i == j) for j in range(n)] for i in range(n)]
def mm(X, Y): return [[sum(X[i][k] * Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def lin(a, X, b, Y): return [[a * X[i][j] + b * Y[i][j] for j in range(n)] for i in range(n)]
# P+ = (A-4I)(A+2I)/(-9), P- = (A-4I)(A-I)/18
Pp = [[F(v, -9) for v in row] for row in mm(lin(1, A, -4, I), lin(1, A, 2, I))]
Pm = [[F(v, 18) for v in row] for row in mm(lin(1, A, -4, I), lin(1, A, -1, I))]
assert sum(Pp[i][i] for i in range(n)) == 4 and sum(Pm[i][i] for i in range(n)) == 4
def tr_on(P, perm):  # tr(P g), g = permutation matrix g[i][perm[i]]... use g e_j = e_perm[j]
    return sum(P[j][perm[j]] for j in range(n))  # tr(P G) with G[perm[j]][j] = 1
Abar = [[int(i != j) - A[i][j] for j in range(n)] for i in range(n)]
auts, antis = [], []
for perm in itertools.permutations(range(n)):
    ok_aut = all(A[perm[i]][perm[j]] == A[i][j] for i in range(n) for j in range(i + 1, n))
    ok_anti = all(A[perm[i]][perm[j]] == Abar[i][j] for i in range(n) for j in range(i + 1, n))
    if ok_aut: auts.append(perm)
    if ok_anti: antis.append(perm)
print("automorphisms:", len(auts), " anti-isomorphisms:", len(antis))
types = {}
for g in auts:
    a, b = tr_on(Pp, g), tr_on(Pm, g)
    fix = sum(g[i] == i for i in range(n))
    assert fix == 1 + a + b
    types[(a, b)] = types.get((a, b), 0) + 1
for (a, b), c in sorted(types.items()):
    print(f"  (alpha, beta) = ({a}, {b})  count {c}  beta - alpha/2 = {b - a / 2}")
print("max beta - alpha/2 over automorphisms:", max(b - a / 2 for (a, b) in types))
print("anti-isos: traces on V+, V- :", {(tr_on(Pp, g), tr_on(Pm, g)) for g in antis})
print("mod-7 checks: 7 | 220 ?", 220 % 7 == 0, "; n with 7 | 12n+88 :", [k for k in range(12) if (12 * k + 88) % 7 == 0])
