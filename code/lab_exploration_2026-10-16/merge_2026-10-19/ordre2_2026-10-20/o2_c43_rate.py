"""Rate of the rank-43 order-2 rule (C43) on realistic partial stars (LAB, NOTE_ORDRE2_7ADIQUE §2.4, 20/10/2026).

(C43) For a generic line at rank 43 and 7 far vertices X with rank_7(H_XX) = 6 and det H_XX != 0: v_7(det H_XX) odd.
Sampling: star of x (star39_prep filters: L2, K(x, .) >= 1, real unary H_aa >= 0), 7 distinct y, distinct q and s
pairs, overlap <= 2; R = a random partial matching on pairs sharing exactly x (star edges), else 0.  H computed
EXACTLY (Z = (3I - G + J)^{-1} over Q).  No PSD requirement (a PSD 7-block of random triples has probability ~1e-4).
Reported: among samples with rank_7 = 6 (the rank-43 first-layer condition at depth 7), the histogram of v_7(det).
usage: python o2_c43_rate.py <seed> <x> <samples>"""
import json
import os
import random
import sys
from fractions import Fraction

import numpy as np
import sympy as sp

MERGE = r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19"
sys.path.insert(0, MERGE)
sys.path.insert(0, os.path.join(MERGE, "..", "reduction_2026-10-19"))
from star_csp import line_graph, n, N  # noqa: E402
from ll_test import pairs_of  # noqa: E402

P = 7


def rank_mod(A):
    A = [row[:] for row in A]
    rows, cols, r = len(A), len(A[0]), 0
    for c in range(cols):
        piv = [i for i in range(r, rows) if A[i][c] % P]
        if not piv:
            continue
        i = piv[0]
        A[r], A[i] = A[i], A[r]
        iv = pow(A[r][c], -1, P)
        A[r] = [v * iv % P for v in A[r]]
        for i2 in range(rows):
            if i2 != r and A[i2][c] % P:
                f = A[i2][c]
                A[i2] = [(a - f * b) % P for a, b in zip(A[i2], A[r])]
        r += 1
    return r


def det_frac(M):
    M = [row[:] for row in M]
    k, d = len(M), Fraction(1)
    for c in range(k):
        piv = next((i for i in range(c, k) if M[i][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, k):
            if M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d


def v7(x):
    a, b, v = x.numerator, x.denominator, 0
    while a % P == 0:
        a //= P; v += 1
    while b % P == 0:
        b //= P; v -= 1
    return v


def main():
    seed, x, samples = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(4300 + seed)
    gt, G, Om, K, leg = line_graph(seed, 0)
    Gi = [[int(v) for v in row] for row in G]
    L = sp.Matrix(N, N, lambda i, j: (3 if i == j else 0) - Gi[i][j] + 1)
    DL = int(L.det())
    assert DL % P, "7 | det L: not a generic line"
    Zs = L.inv() * DL
    Zi = [[int(Zs[i, j]) for j in range(N)] for i in range(N)]   # adj(L) = det(L) Z, integer
    nb = [set(int(z) for z in np.nonzero(G[v])[0]) for v in range(N)]
    xb = x ^ 1
    ys = [y for y in range(n) if y not in (x, xb)]
    P1 = [(n + a, n + b) for a, b in pairs_of(n)]
    P2 = [(2 * n + a, 2 * n + b) for a, b in pairs_of(n)]
    cands = {}
    for y in ys:
        lst = []
        for qi, q in enumerate(P1):
            if K[x, q[0]] == 0 or K[x, q[1]] == 0:
                continue
            for si, s_ in enumerate(P2):
                if K[x, s_[0]] == 0 or K[x, s_[1]] == 0:
                    continue
                W = (x, y) + q + s_
                Ws = set(W)
                if any(len(nb[v] & Ws) > 1 for v in W):
                    continue
                cnt = {}
                for v in W:
                    for z in nb[v]:
                        if z not in Ws:
                            cnt[z] = cnt.get(z, 0) + 1
                if any(c > 2 for c in cnt.values()):
                    continue
                zz = sum(Zi[a][b] for a in W for b in W)
                if 9 * DL * 3 + DL - 9 * zz < 0 if DL > 0 else 9 * DL * 3 + DL - 9 * zz > 0:
                    continue
                cap = 1 - len(nb[x] & Ws)
                lst.append((W, qi, si, cap))
        cands[y] = lst
    hist, n_rank6, n_tot = {}, 0, 0
    for _ in range(samples):
        yy = rng.sample(ys, 7)
        sel = [rng.choice(cands[y]) for y in yy]
        if len({c[1] for c in sel}) < 7 or len({c[2] for c in sel}) < 7:
            continue
        if any(len(set(sel[i][0]) & set(sel[j][0])) > 2 for i in range(7) for j in range(i)):
            continue
        Rm = [[0] * 7 for _ in range(7)]
        idx = [i for i in range(7) if sel[i][3] == 1]
        rng.shuffle(idx)
        for t in range(0, len(idx) - 1, 2):
            a, b = idx[t], idx[t + 1]
            if len(set(sel[a][0]) & set(sel[b][0])) == 1 and rng.random() < 0.5:
                Rm[a][b] = Rm[b][a] = 1
        Hm = [[None] * 7 for _ in range(7)]
        for i in range(7):
            for j in range(7):
                zz = sum(Zi[a][b] for a in sel[i][0] for b in sel[j][0])
                Hm[i][j] = 9 * DL * ((3 if i == j else 0) - Rm[i][j]) + DL - 9 * zz   # = 9 det(L) H_ij
        n_tot += 1
        Hmod = [[v % P for v in row] for row in Hm]
        if rank_mod(Hmod) != 6:
            continue
        d = int(sp.Matrix(Hm).det(method="bareiss"))
        if d == 0:
            continue
        n_rank6 += 1
        e = v7(Fraction(d))
        hist[e] = hist.get(e, 0) + 1
    odd = sum(c for e, c in hist.items() if e % 2 == 1)
    print(json.dumps({"seed": seed, "x": x, "tau_leg": leg, "samples_valid": n_tot, "rank_7=6": n_rank6,
                      "v7(det) histogram": {str(k): v for k, v in sorted(hist.items())},
                      "fraction passing (C43) (v7 odd)": (odd / n_rank6 if n_rank6 else None)}))


if __name__ == "__main__":
    main()
