"""Independent C1 re-verification of C2's characteristic test (conway99-rank17 r17_char, 452c304). No C2 code is used.
Test: chi characteristic of V  =>  (chi,y1)^2 + (chi,y2)^2 <= 7|chi|^2 - 21   (equivalently |P_K chi|^2 >= 3).
(a) every C2 witness: chi in V, characteristic (exact, on the V basis), norm, heights from the ypairs y's, y Gram 7I, violation;
(b) completeness: my own enumeration of ALL characteristic vectors of norm <= 9 (own LLL + Fincke-Pohst on chi0 + 2V), then the
    killed set is recomputed and must equal C2's set exactly.
Usage: python code/rank17_char_verify.py <path to rank17_char_kills_2909.json>"""
import sys, os, json, math, collections
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank17_cores as RC
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rank17')
VN = {'E8': 'E8', 'D12p': 'D12+', 'E72p': 'E7^2+', 'A15p': 'A15+', 'D82p': 'D8^2+', 'A11E6p': 'A11E6+'}

def lll(G, delta=0.99):
    """LLL on an integer Gram matrix; returns unimodular integer T (rows = new basis in old coords)."""
    n = len(G); T = np.eye(n, dtype=object); Gi = np.array(G, dtype=object)
    def gso():
        Gf = np.array(T.dot(Gi).dot(T.T), dtype=float)
        mu = np.zeros((n, n)); Bs = np.zeros(n)
        for i in range(n):
            for j in range(i):
                mu[i, j] = (Gf[i, j] - sum(mu[j, k] * mu[i, k] * Bs[k] for k in range(j))) / Bs[j]
            Bs[i] = Gf[i, i] - sum(mu[i, k] ** 2 * Bs[k] for k in range(i))
        return mu, Bs
    k = 1
    while k < n:
        mu, Bs = gso()
        for j in range(k - 1, -1, -1):
            q = int(round(mu[k, j]))
            if q: T[k] = T[k] - q * T[j]; mu, Bs = gso()
        if Bs[k] >= (delta - mu[k, k - 1] ** 2) * Bs[k - 1]: k += 1
        else: T[[k, k - 1]] = T[[k - 1, k]]; k = max(k - 1, 1)
    return T

def solve_mod2(G, rhs):
    n = len(G); A = [[int(G[i][j]) & 1 for j in range(n)] + [int(rhs[i]) & 1] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c]); A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c]: A[r] = [x ^ y for x, y in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]

def close_vectors(Gr, t, R2):
    """all integer x with (x-t)^T Gr (x-t) <= R2 (Fincke-Pohst, float with margin; exact recheck by caller)"""
    n = len(Gr); L = np.linalg.cholesky(np.array(Gr, dtype=float)); Q = L.T  # Gr = Q^T Q, Q upper
    d = np.diag(Q) ** 2; mu = Q / np.diag(Q)[:, None]
    out = []; x = [0] * n
    def rec(i, rem):
        c = t[i] - sum(mu[i, j] * (x[j] - t[j]) for j in range(i + 1, n))
        r = math.sqrt(max(rem, 0) / d[i]) + 1e-9
        for xi in range(math.ceil(c - r), math.floor(c + r) + 1):
            x[i] = xi; used = d[i] * (xi - c) ** 2
            if i == 0: out.append(list(x))
            else: rec(i - 1, rem - used)
        x[i] = 0
    rec(n - 1, R2 + 1e-7)
    return out

W = json.load(open(sys.argv[1]))['killed']
wit = collections.defaultdict(dict)
for w in W: wit[w['V']][w['id']] = w
opened = collections.defaultdict(set)
for s in json.load(open(os.path.join(D, 'open_after_sol.json'))):
    v, i = s.split(':'); opened[v].add(int(i))
cores = RC.cores(); tot_ok = 0; tot_kill = 0; mism = []
for Vn, cn in VN.items():
    d = json.load(open(os.path.join(D, 'ypairs_%s.json' % Vn))); m = d['units']; gens, dim = cores[cn]
    Bc = RC.int_basis(gens)
    B = [row + [F(0)] * m for row in Bc] + [[F(0)] * dim + [F(int(i == j)) for j in range(m)] for i in range(m)]
    n = len(B); assert n == 17
    G = [[sum(a * b for a, b in zip(B[i], B[j])) for j in range(n)] for i in range(n)]
    assert all(x.denominator == 1 for r in G for x in r); G = [[int(x) for x in r] for r in G]
    assert round(abs(np.linalg.det(np.array(G, dtype=float)))) == 1
    amb = lambda cf: [sum(int(cf[i]) * B[i][j] for i in range(n)) for j in range(len(B[0]))]
    ip = lambda u, v: sum(a * b for a, b in zip(u, v))
    def yvec(p, k):
        v = [F(x) for x in p['y%d_core' % k]] + [F(u) for u in p['y%d_units' % k]]
        # membership in V: exact coefficients (float solve, then exact reconstruction)
        cf = np.rint(np.linalg.lstsq(np.array([[float(x) for x in r] for r in B]).T, np.array([float(x) for x in v]), rcond=None)[0]).astype(int)
        assert amb(cf) == v, 'y not in V'
        return v
    # (a) witnesses
    ok = 0
    for i, w in wit[Vn].items():
        assert i in opened[Vn]
        cf = w['chi_coef']; chi = amb(cf)
        assert all((sum(cf[a] * G[a][b] for a in range(n)) - G[b][b]) % 2 == 0 for b in range(n)), 'not characteristic'
        N = ip(chi, chi); p = d['pairs'][i]; assert p['id'] == i
        y1, y2 = yvec(p, 1), yvec(p, 2)
        assert ip(y1, y1) == 7 and ip(y2, y2) == 7 and ip(y1, y2) == 0
        h1, h2 = ip(chi, y1), ip(chi, y2)
        assert N == w['chi_norm'] and [h1, h2] == w['heights'] and h1 * h1 + h2 * h2 > 7 * N - 21
        ok += 1
    # (b) completeness: all characteristic chi of norm <= 9
    c0 = solve_mod2(G, [G[i][i] for i in range(n)])
    T = lll(G); Ti = np.array(np.round(np.linalg.inv(np.array(T, dtype=float))), dtype=object)
    assert (Ti.dot(T) == np.eye(n, dtype=object)).all()
    Gr = [[int(x) for x in r] for r in T.dot(np.array(G, dtype=object)).dot(T.T)]
    t = -np.array(c0, dtype=float) @ np.array(Ti, dtype=float) / 2        # c0/2 + v = 0 target, in reduced coords
    chis = []
    for x in close_vectors(Gr, t, F(9, 4)):
        v = np.array(x, dtype=object).dot(T); chi = [c0[i] + 2 * v[i] for i in range(n)]
        N = sum(chi[a] * G[a][b] * chi[b] for a in range(n) for b in range(n))
        if N <= 9: chis.append((chi, N))
    assert all(N % 8 == 1 for _, N in chis)
    CH = np.array([amb(c) for c, _ in chis], dtype=object); NN = np.array([N for _, N in chis], dtype=object)
    killed = set()
    for i in sorted(opened[Vn]):
        p = d['pairs'][i]; y1, y2 = yvec(p, 1), yvec(p, 2)
        h1 = CH.dot(np.array(y1, dtype=object)); h2 = CH.dot(np.array(y2, dtype=object))
        if any(h1 * h1 + h2 * h2 > 7 * NN - 21): killed.add(i)
    same = killed == set(wit[Vn])
    if not same: mism.append((Vn, sorted(killed - set(wit[Vn])), sorted(set(wit[Vn]) - killed)))
    print('%-7s shell %5d  witnesses ok %3d/%3d  recomputed kills %3d  equal=%s' % (Vn, len(chis), ok, len(wit[Vn]), len(killed), same), flush=True)
    tot_ok += ok; tot_kill += len(killed)
print('TOTAL witnesses ok', tot_ok, '/', len(W), ' recomputed kills', tot_kill, ' mismatches', mism)
