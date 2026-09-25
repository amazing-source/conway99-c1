"""Hamming point x: M_x (Schur complement of A - 3I at B_1(x), mod 7) splits as
(N - 3I) on the 56 character dimensions orthogonal to Z, plus a FIXED block on
S = <1_P (21 pairs), Z_m (7 classes)>, independent of the generic matchings phi.
This script computes that fixed block: its 7-rank c0 and the discriminant of its
non-degenerate part, so that k = r + c0 with r = rank_7 (N - 3I) on Z^perp."""
import itertools
from fractions import Fraction

p = 7
classes = range(7)
pairs = [P for P in itertools.combinations(classes, 2)]
verts = [(P, (e1, e2)) for P in pairs for e1 in (0, 1) for e2 in (0, 1)]   # 84
vid = {v: n for n, v in enumerate(verts)}
labels = [(m, e) for m in classes for e in (0, 1)]                           # 14
X = ['x'] + labels                                                           # 15

def lab(v):
    (i, j), (a, b) = v
    return {(i, a), (j, b)}

# N_XX = A_W - 3I on the windmill
nX = len(X)
NXX = [[0] * nX for _ in range(nX)]
for s in range(nX):
    NXX[s][s] = -3
for s in range(1, nX):
    NXX[0][s] = NXX[s][0] = 1
for s in range(1, nX):
    for t in range(1, nX):
        if s != t and X[s][0] == X[t][0]:
            NXX[s][t] = 1

def inv_mod(M, p):
    n = len(M)
    A = [[M[i][j] % p for j in range(n)] + [int(i == j) for j in range(n)] for i in range(n)]
    for c in range(n):
        r = next(r for r in range(c, n) if A[r][c] % p)
        A[c], A[r] = A[r], A[c]
        iv = pow(A[c][c], p - 2, p)
        A[c] = [a * iv % p for a in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                f = A[r][c]
                A[r] = [(a - f * b) % p for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]

NXXi = inv_mod(NXX, p)

def NXY(vec):   # vec on 84 -> on 15
    out = [0] * nX
    for n, v in enumerate(verts):
        for c in lab(v):
            out[X.index(c)] += vec[n]
    return out

def NYX(w):     # w on 15 -> on 84
    return [sum(w[X.index(c)] for c in lab(v)) for v in verts]

def H_on_S(vec, kind, key):
    """H = Sib + H_gen applied to a basis vector of S (valid under (Z))."""
    if kind == 'Z':
        return [0] * 84
    P = key
    out = [0] * 84
    for n, v in enumerate(verts):
        Q = v[0]
        if Q == P:
            out[n] += 2                      # Sib 1_P = 2 * 1_P
        elif not set(Q) & set(P):
            out[n] += 1                      # H_gen 1_P = sum of 1_R over disjoint R
    return out

basis = []
for P in pairs:
    basis.append(('1', P, [1 if v[0] == P else 0 for v in verts]))
for m in classes:
    vec = []
    for v in verts:
        (i, j), (a, b) = v
        if m == i:
            vec.append((-1) ** a)
        elif m == j:
            vec.append((-1) ** b)
        else:
            vec.append(0)
    basis.append(('Z', m, vec))

def Mx(kind, key, vec):
    h = H_on_S(vec, kind, key)
    t = NXY(vec)
    w = [sum(NXXi[s][u] * t[u] for u in range(nX)) % p for s in range(nX)]
    c = NYX(w)
    return [(h[n] - 3 * vec[n] - c[n]) % p for n in range(84)]

# form F = S^T M_x S (28 x 28) mod 7
imgs = [Mx(k, key, vec) for k, key, vec in basis]
F = [[sum(b[2][n] * im[n] for n in range(84)) % p for im in imgs] for b in basis]
assert all(F[a][b] == F[b][a] for a in range(28) for b in range(28)), 'not symmetric'

def rank_disc(M, p):
    """rank and discriminant (as Legendre symbol) of the non-degenerate part of a symmetric form."""
    n = len(M)
    A = [[x % p for x in row] for row in M]
    # symmetric Gaussian elimination: diagonalise
    diag = []
    idx = list(range(n))
    A = [row[:] for row in A]
    active = list(range(n))
    while active:
        piv = next((i for i in active if A[i][i] % p), None)
        if piv is None:
            # find off-diagonal nonzero, make diagonal nonzero by i <- i + j
            pr = next(((i, j) for i in active for j in active if i != j and A[i][j] % p), None)
            if pr is None:
                break
            i, j = pr
            for t in range(n):
                A[i][t] = (A[i][t] + A[j][t]) % p
            for t in range(n):
                A[t][i] = (A[t][i] + A[t][j]) % p
            piv = i
        d = A[piv][piv] % p
        diag.append(d)
        iv = pow(d, p - 2, p)
        rest = [i for i in active if i != piv]
        for i in rest:
            f = A[i][piv] * iv % p
            if f:
                for t in range(n):
                    A[i][t] = (A[i][t] - f * A[piv][t]) % p
                for t in range(n):
                    A[t][i] = (A[t][i] - f * A[t][piv]) % p
        active = rest
    disc = 1
    for d in diag:
        disc = disc * d % p
    leg = pow(disc, (p - 1) // 2, p)
    return len(diag), (1 if leg == 1 else -1)

r0, s0 = rank_disc(F, p)
print('fixed block on S (21 constants + 7 Z-vectors): rank_7 =', r0, ' disc Legendre =', s0)
Fc = [row[:21] for row in F[:21]]
Fz = [row[21:] for row in F[21:]]
print('  constants part alone: rank/disc', rank_disc(Fc, p), '; Z part alone:', rank_disc(Fz, p))
print('  cross block nonzero entries:', sum(1 for a in range(21) for b in range(21, 28) if F[a][b]))
# is M_x S inside S?  project imgs onto S and compare
nz = sum(1 for im in imgs for c in im if c % p)
print('nonzero coordinates of M_x v over the 28 basis vectors of S (mod 7):', nz)
