"""Exact mod-7 checks of the identities of PROMPT_CHATGPT_CORE37_2026-10-20.md (section 5.1), LAB 20/10/2026.
On six random connected admissible G_T with 7 not dividing tau: Omega 1 = 1, Omega 1_Ci = 1 + 5 1_Ci, K = -L^2 + 3J - J_cl,
det(3I - G + J) = tau, 1_Ci^T Omega e_W = 2, x = -Omega e + 3.1 solves Sigma x = e (Green form), e^T Omega K Omega e' = 5 - |W cap W'|.
usage: python check_identities.py [seed]   (under 2 s)"""
import random
import sys
import numpy as np
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
from ll_test import gt_matrix, k_matrix, components, pairs_of  # noqa: E402
P = 7


def inv_mod(M):
    n = M.shape[0]
    A = np.concatenate([M % P, np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        piv = [r for r in range(c, n) if A[r, c] % P]
        if not piv:
            return None
        r = piv[0]
        A[[c, r]] = A[[r, c]]
        A[c] = A[c] * pow(int(A[c, c]), P - 2, P) % P
        for r2 in range(n):
            if r2 != c and A[r2, c]:
                A[r2] = (A[r2] - A[r2, c] * A[c]) % P
    return A[:, n:]


def det_mod(M):
    M = M.copy() % P
    n, d = M.shape[0], 1
    for c in range(n):
        piv = [r for r in range(c, n) if M[r, c]]
        if not piv:
            return 0
        r = piv[0]
        if r != c:
            M[[c, r]] = M[[r, c]]
            d = -d
        d = d * int(M[c, c]) % P
        iv = pow(int(M[c, c]), P - 2, P)
        for r2 in range(c + 1, n):
            if M[r2, c]:
                M[r2] = (M[r2] - M[r2, c] * iv * M[c]) % P
    return d % P


rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
n, N = 12, 36
done = 0
while done < 6:
    s = [rng.sample(range(n), n) for _ in range(3)]
    G = gt_matrix(n, *s)
    K = k_matrix(n, G)
    if (K < 0).any() or components(G)[0] != 1:
        continue
    I, J = np.eye(N, dtype=np.int64), np.ones((N, N), dtype=np.int64)
    L = (3 * I - G + J) % P
    Om = inv_mod(L)
    if Om is None:
        continue
    done += 1
    Jcl = np.zeros((N, N), dtype=np.int64)
    one_c = []
    for c in range(3):
        Jcl[c * n:(c + 1) * n, c * n:(c + 1) * n] = 1
        v = np.zeros(N, dtype=np.int64)
        v[c * n:(c + 1) * n] = 1
        one_c.append(v)
    ok = {}
    ok["Om1=1"] = ((Om @ np.ones(N, dtype=np.int64)) % P == 1).all()
    ok["Om1Ci=1+5*1Ci"] = all(((Om @ v - 1 - 5 * v) % P == 0).all() for v in one_c)
    ok["K=-L^2+3J-Jcl"] = ((K - (-(L @ L) + 3 * J - Jcl)) % P == 0).all()
    lap = (3 * I - G)[1:, 1:]
    tau7 = det_mod(lap)
    ok["det(3I-G+J)=tau"] = det_mod(L) == tau7
    # triples (2 names per class), random sample: 1_Ci^T Om e = 2, e^T Om K Om e' = 5 - |W cap W'|, Green vs Schur
    Pp = pairs_of(n)
    Sig = ((G - 3 * I) + 2 * (Jcl + J)) % P            # (J_cl + J)/4 with 1/4 = 2 mod 7
    OKO = (Om @ K % P) @ Om % P
    good = [True, True, True]
    trip = []
    for _ in range(200):
        p, q, r = rng.choice(Pp), rng.choice(Pp), rng.choice(Pp)
        e = np.zeros(N, dtype=np.int64)
        e[[p[0], p[1], n + q[0], n + q[1], 2 * n + r[0], 2 * n + r[1]]] = 1
        trip.append(e)
        good[0] &= all(int(v @ Om @ e) % P == 2 for v in one_c)
        x = (-(Om @ e) + 3) % P
        good[1] &= ((Sig @ x - e) % P == 0).all()
    for a in range(0, 200, 2):
        e, f = trip[a], trip[a + 1]
        good[2] &= int(e @ OKO @ f) % P == (5 - int(e @ f)) % P and int(e @ OKO @ e) % P == 6
    ok["1Ci.Om.e=2"], ok["Schur x=-Om e+3.1"], ok["eOKOe'=5-|WnW'|"] = good
    print({k: bool(v) for k, v in ok.items()}, "tau mod 7 =", tau7)
