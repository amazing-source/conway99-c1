"""Per-class minimal characteristic shell of K* (C1, 29/09). K = V cap <y1,y2>^perp, rank 15, det 49.
In dual coordinates z_i = (xi, k_i) (k = integer basis of K), Char(K*) = {z : z_i == (G_K)_ii mod 2}, |xi|^2 = z^T G_K^{-1} z.
Complete enumeration (own LLL + Fincke-Pohst) of Char(K*) up to norm 33/7; 7|xi|^2 = ||Phi(xi)||^2 in {21, 25, 29, 33, ...}.
Output data/rank17/charshell.json: per class mu7 = 7 min Char(K*), line counts per level, Gram 7C of the minimal lines.
Usage: python code/rank17_charshell.py [V:id ...]"""
import sys, os, json, math, collections
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank17_cores as RC
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rank17')
VN = {'E8': 'E8', 'D12p': 'D12+', 'E72p': 'E7^2+', 'A15p': 'A15+', 'D82p': 'D8^2+', 'A11E6p': 'A11E6+', 'Z17': None}

def lll(G, delta=0.99):
    n = len(G); T = np.eye(n, dtype=object); Gi = np.array(G, dtype=object)
    def gso():
        L = np.linalg.cholesky(np.array(T.dot(Gi).dot(T.T), dtype=float)); dg = np.diag(L)
        return L / dg[None, :], dg ** 2
    k = 1; mu, Bs = gso()
    while k < n:
        for j in range(k - 1, -1, -1):
            q = int(round(mu[k, j]))
            if q: T[k] = T[k] - q * T[j]; mu, Bs = gso()
        if Bs[k] >= (delta - mu[k, k - 1] ** 2) * Bs[k - 1]: k += 1
        else: T[[k, k - 1]] = T[[k - 1, k]]; k = max(k - 1, 1); mu, Bs = gso()
    return T

def close_vectors(Gr, t, R2):
    n = len(Gr); Q = np.linalg.cholesky(np.array(Gr, dtype=float)).T
    d = np.diag(Q) ** 2; mu = Q / np.diag(Q)[:, None]; out = []; x = [0] * n
    def rec(i, rem):
        c = t[i] - sum(mu[i, j] * (x[j] - t[j]) for j in range(i + 1, n)); r = math.sqrt(max(rem, 0) / d[i]) + 1e-9
        for xi in range(math.ceil(c - r), math.floor(c + r) + 1):
            x[i] = xi
            if i == 0: out.append(list(x))
            else: rec(i - 1, rem - d[i] * (xi - c) ** 2)
        x[i] = 0
    rec(n - 1, R2 + 1e-7); return out

def int_kernel(A, n):
    """integer basis of {v in Z^n : A v = 0} (rows), by unimodular row reduction of [A^T | I]"""
    M = [[A[r][i] for r in range(len(A))] + [int(i == j) for j in range(n)] for i in range(n)]; m = len(A); piv = 0
    for c in range(m):
        while True:
            rows = [r for r in range(piv, n) if M[r][c]]
            if not rows: break
            p = min(rows, key=lambda r: abs(M[r][c])); M[piv], M[p] = M[p], M[piv]
            done = True
            for r in range(piv + 1, n):
                if M[r][c]:
                    q = M[r][c] // M[piv][c]; M[r] = [a - q * b for a, b in zip(M[r], M[piv])]
                    if M[r][c]: done = False
            if done: piv += 1; break
    return [row[m:] for row in M[piv:]]

def vbasis(Vn):
    d = json.load(open(os.path.join(D, 'ypairs_%s.json' % Vn))); m = d['units']
    if VN[Vn] is None: B = [[F(int(i == j)) for j in range(17)] for i in range(17)]
    else:
        gens, dim = RC.cores()[VN[Vn]]; Bc = RC.int_basis(gens)
        B = [row + [F(0)] * m for row in Bc] + [[F(0)] * dim + [F(int(i == j)) for j in range(m)] for i in range(m)]
    G = [[int(sum(a * b for a, b in zip(B[i], B[j]))) for j in range(17)] for i in range(17)]
    Bf = np.array([[float(x) for x in r] for r in B]).T
    def coef(p, k):
        v = [F(x) for x in p['y%d_core' % k]] + [F(u) for u in p['y%d_units' % k]]
        cf = [int(x) for x in np.rint(np.linalg.lstsq(Bf, np.array([float(x) for x in v]), rcond=None)[0])]
        assert [sum(cf[i] * B[i][j] for i in range(17)) for j in range(len(v))] == v
        return cf
    return d, G, coef

def shell(G, y1, y2, R7=33):
    A = [[sum(y[i] * G[i][j] for i in range(17)) for j in range(17)] for y in (y1, y2)]
    Kb = int_kernel(A, 17); assert len(Kb) == 15
    GK = [[sum(Kb[a][i] * G[i][j] * Kb[b][j] for i in range(17) for j in range(17)) for b in range(15)] for a in range(15)]
    import sympy as sp
    GKs = sp.Matrix(GK); assert GKs.det() == 49
    D7 = [[int(x) for x in r] for r in (7 * GKs.inv()).tolist()]       # 7 Gram(K*) in dual coords, integral
    c0 = [GK[i][i] % 2 for i in range(15)]
    T = lll(D7); Ti = np.array(np.round(np.linalg.inv(np.array(T, dtype=float))), dtype=object)
    assert (Ti.dot(T) == np.eye(15, dtype=object)).all()
    Gr = [[int(x) for x in r] for r in T.dot(np.array(D7, dtype=object)).dot(T.T)]
    t = -np.array(c0, dtype=float) @ np.array(Ti, dtype=float) / 2
    Z = []
    for x in close_vectors(Gr, t, F(R7, 4)):
        v = np.array(x, dtype=object).dot(T); z = [c0[i] + 2 * v[i] for i in range(15)]
        n7 = sum(z[a] * D7[a][b] * z[b] for a in range(15) for b in range(15))
        if n7 <= R7: Z.append((n7, z))
    return Z, D7

if __name__ == '__main__':
    todo = sys.argv[1:] or json.load(open(os.path.join(D, 'open_after_char.json')))
    byV = collections.defaultdict(list)
    for s in todo: v, i = s.split(':'); byV[v].append(int(i))
    res = {}; hist = collections.Counter()
    for Vn, ids in byV.items():
        if Vn == 'Z17': print('Z17 skipped', ids); continue
        d, G, coef = vbasis(Vn)
        for i in ids:
            p = d['pairs'][i]; Z, D7 = shell(G, coef(p, 1), coef(p, 2))
            lev = collections.Counter(n for n, _ in Z)
            assert all(n % 4 == 1 and n >= 21 for n in lev), (Vn, i, lev)   # char test holds; ||Phi||^2 == 1 mod 4
            key = '%s:%d' % (Vn, i)
            if not Z: res[key] = {'mu7': None}; hist['>33'] += 1; continue
            m = min(lev); lines = []
            for n, z in Z:
                if n == m and [-a for a in z] not in lines: lines.append(z)
            C7 = [[sum(a[r] * D7[r][s] * b[s] for r in range(15) for s in range(15)) for b in lines] for a in lines]
            res[key] = {'mu7': m, 'lines_per_level': {str(k): v // 2 for k, v in sorted(lev.items())}, 'gram7_min': C7}
            hist[m] += 1
        print(Vn, 'done', flush=True)
    out = os.path.join(D, 'charshell.json') if not sys.argv[1:] else os.path.join(D, 'charshell_partial.json')
    json.dump(res, open(out, 'w'), indent=0)
    print('7*min Char(K*) histogram:', dict(sorted(hist.items(), key=str)))
    for k in sys.argv[1:]: print(k, res[k])
