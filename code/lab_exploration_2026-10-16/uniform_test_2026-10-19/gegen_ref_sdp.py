"""Projected Gegenbauer positivity with an m-vertex reference graph H, counts from subgraph_counts.py (LAB 19/10/2026).
For every labelled embedding of H and every k >= 1, the matrix indexed by the adjacency patterns T (subsets of V(H)) of
outside vertices,
    M_k[T1, T2] = sum_{u in T1, v in T2} G_k^(d)(<x^_u, x^_v>)        (u = v included, G_k(1) = 1),
is PSD (Schoenberg), where x^ is the normalised projection of the unit vertex vector onto span(H)^perp (d = n - m) and
the inner product depends only on (T1, T2, A_uv).  Summing over embeddings, the entries are exact embedding counts of
(m+1)- and (m+2)-vertex labelled graphs, i.e. affine functions of the free parameters of subgraph_counts.py.
Here the parameter is written as P = number of induced triangular prisms.
For each reference H and each representation (E_-4: n = 44, inner products -2/7, 1/28; E_3: n = 54, 3/14, -1/21)
this prints the interval of P in [0, 1386] on which M_k(P) >= 0 for all k <= K.
usage: python gegen_ref_sdp.py <counts json> <m> [K=60]"""
import json
import sys
from fractions import Fraction as Fr
from itertools import combinations

import mpmath as mp

mp.mp.dps = 30
CNT, M, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 60
sys.argv = ['x', '1', '-']
exec(open(__file__.replace('gegen_ref_sdp.py', 'subgraph_counts.py'), encoding='utf-8').read().split(
    "if __name__ == '__main__':")[0])
D = json.load(open(CNT))
assert D['params'] == ['N[((4, 5),)]'], D['params']
LV = {int(k): {tuple(map(tuple, c['edges'])): ([Fr(x) for x in c['N']], c['aut']) for c in v}
      for k, v in D['levels'].items()}
# reparametrise by P: prism count = -30596874 + p/9  =>  p = 9 P + 275371866
P_OFF, P_SCALE = Fr(275371866), Fr(9)
REPS = {'E-4': (44, Fr(-2, 7), Fr(1, 28)), 'E3': (54, Fr(3, 14), Fr(-1, 21))}


def emb(n, E):
    """number of labelled embeddings of the labelled graph (n, E), as (const, coef of P)."""
    if not feasible(n, E):
        return (Fr(0), Fr(0))
    enc, aut = canon(n, E)
    N, a = LV[n][enc]
    assert a == aut
    c0 = N[0] + (N[1] * P_OFF if len(N) > 1 else 0)
    c1 = (N[1] * P_SCALE if len(N) > 1 else Fr(0))
    return (c0 * aut, c1 * aut)


def gegen(d, t, K):
    g = [mp.mpf(1), t]
    for k in range(1, K):
        g.append(((2 * k + d - 2) * t * g[k] - k * g[k - 1]) / (k + d - 2))
    return g


def solve(Gm, b):
    n = len(Gm)
    A = [list(Gm[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [A[r][i] - f * A[c][i] for i in range(n + 1)]
    return [A[i][n] / A[i][i] for i in range(n)]


def det(Mx):
    n = len(Mx)
    A = [list(r) for r in Mx]
    d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            A[r] = [A[r][i] - f * A[c][i] for i in range(n)]
    return d


def analyse(Henc, rep):
    n, a, b = REPS[rep]
    m = M
    HE = list(Henc)
    Hadj = adjsets(m, HE)
    ip = lambda x, y: a if y in Hadj[x] else b
    Gm = [[Fr(1) if i == j else ip(i, j) for j in range(m)] for i in range(m)]
    if det(Gm) == 0:
        return None
    pats = []
    for r in range(m + 1):
        for T in combinations(range(m), r):
            if emb(m + 1, HE + [(t, m) for t in T]) != (0, 0):
                pats.append(T)
    gv = {T: [a if i in T else b for i in range(m)] for T in pats}
    sol = {T: solve(Gm, gv[T]) for T in pats}
    pr = lambda T1, T2, base: base - sum(gv[T1][i] * sol[T2][i] for i in range(m))
    nrm = {T: pr(T, T, Fr(1)) for T in pats}
    pats = [T for T in pats if nrm[T] != 0]
    d = n - m
    size = {T: emb(m + 1, HE + [(t, m) for t in T]) for T in pats}
    pair = {}
    for T1 in pats:
        for T2 in pats:
            for adjuv in (0, 1):
                E = HE + [(t, m) for t in T1] + [(t, m + 1) for t in T2] + ([(m, m + 1)] if adjuv else [])
                pair[(T1, T2, adjuv)] = emb(m + 2, E)
    tval = {}
    for (T1, T2, adjuv) in pair:
        num = pr(T1, T2, a if adjuv else b)
        tval[(T1, T2, adjuv)] = (mp.mpf(num.numerator) / num.denominator) / mp.sqrt(
            mp.mpf(nrm[T1].numerator) / nrm[T1].denominator * mp.mpf(nrm[T2].numerator) / nrm[T2].denominator)
    G = {key: gegen(d, t, K) for key, t in tval.items()}
    np_ = len(pats)
    lo, hi = mp.mpf(0), mp.mpf(1386)
    binding = []
    for k in range(1, K + 1):
        M0 = mp.matrix(np_, np_); M1 = mp.matrix(np_, np_)
        for i, T1 in enumerate(pats):
            for j, T2 in enumerate(pats):
                s0 = mp.mpf(0); s1 = mp.mpf(0)
                if i == j:
                    s0 += mp.mpf(size[T1][0].numerator) / size[T1][0].denominator
                    s1 += mp.mpf(size[T1][1].numerator) / size[T1][1].denominator
                for adjuv in (0, 1):
                    c0, c1 = pair[(T1, T2, adjuv)]
                    gk = G[(T1, T2, adjuv)][k]
                    s0 += gk * c0.numerator / c0.denominator
                    s1 += gk * c1.numerator / c1.denominator
                M0[i, j] = s0; M1[i, j] = s1
        scale = max(abs(M0[i, j]) for i in range(np_) for j in range(np_)) + 1

        def mineig(P):
            return min(mp.eigsy(M0 + P * M1)[0]) / scale
        tol = mp.mpf(10) ** (-20)
        vals = [(P, mineig(mp.mpf(P))) for P in (0, 346.5, 693, 1039.5, 1386)]
        if all(v > -tol for _, v in vals):
            continue
        # min eigenvalue is concave in P: find the feasible interval by bisection around the best sample
        Pb, vb = max(vals, key=lambda t: t[1])
        if vb < -tol:
            # golden search for the max of the concave function
            l, r = mp.mpf(0), mp.mpf(1386)
            for _ in range(70):
                m1, m2 = l + (r - l) / 3, r - (r - l) / 3
                if mineig(m1) < mineig(m2):
                    l = m1
                else:
                    r = m2
            Pb, vb = l, mineig(l)
            if vb < -tol:
                return {'pats': len(pats), 'd': d, 'empty_at_k': k, 'max_min_eig': mp.nstr(vb, 8), 'at_P': mp.nstr(Pb, 8)}
        newlo, newhi = lo, hi
        if mineig(lo) < -tol:
            l, r = lo, mp.mpf(Pb)
            for _ in range(70):
                mid = (l + r) / 2
                if mineig(mid) < -tol:
                    l = mid
                else:
                    r = mid
            newlo = r
        if mineig(hi) < -tol:
            l, r = mp.mpf(Pb), hi
            for _ in range(70):
                mid = (l + r) / 2
                if mineig(mid) < -tol:
                    r = mid
                else:
                    l = mid
            newhi = l
        if newlo > lo or newhi < hi:
            binding.append((k, mp.nstr(newlo, 10), mp.nstr(newhi, 10)))
        lo, hi = max(lo, newlo), min(hi, newhi)
        if lo > hi:
            return {'pats': len(pats), 'd': d, 'empty_at_k': k, 'binding': binding}
    return {'pats': len(pats), 'd': d, 'P_interval': [mp.nstr(lo, 12), mp.nstr(hi, 12)], 'binding': binding[:6]}


if __name__ == '__main__':
    for Henc in sorted(LV[M]):
        for rep in REPS:
            res = analyse(Henc, rep)
            print(json.dumps({'H': [list(e) for e in Henc], 'rep': rep, 'result': res}), flush=True)
