"""Spectral label blocks for the R8 route (LAB 20/10/2026), my own implementation.

srg(n,k,1,2), eigenvalues r > s (r = (-1+d)/2, s = (-1-d)/2, d^2 = 4k-7), multiplicities f (of r), g (of s).
P_s = projector on the s-eigenspace = a I + b A + c J,  P_r = projector on the r-eigenspace = a' I + b' A + c' J.
Vertex v, N = N[v] = {v} + k letters, labels = the other vertices.  For a set S of labels:
   T_S = (r-s) * [Schur complement of P_s on the labels, eliminating N]  restricted to S  = T0_S - A_SS
   U_S = (r-s) * [Schur complement of P_r on the labels]                 restricted to S  = U0_S + A_SS
T0, U0 depend only on the labels (letters), not on Gamma.  In every srg: T, U are PSD (Schur complements of PSD
matrices), with eigenvalues in [0, r-s], rank T = g - k and rank U = f - k (inertia additivity, N-block ranks k, k),
and T + U = (r-s) Pi with Pi the orthogonal projector on ker B (B = letter-label incidence).  For S: principal
submatrices, so T_S, U_S >= 0, T_S, U_S <= (r-s) I, rank T_S <= g - k, rank U_S <= f - k.
These identities are VERIFIED numerically on real srg(243,22,1,2) graphs by verify_spectral() below."""
import itertools
import math

import numpy as np

MATE = lambda y: y ^ 1


def params(k):
    d = int(round(math.sqrt(4 * k - 7)))
    assert d * d == 4 * k - 7
    r, s = (-1 + d) // 2, (-1 - d) // 2
    n = 1 + k + k * (k - 2) // 2
    # multiplicities: f + g = n - 1, k + f r + g s = 0
    g = (k + (n - 1) * r) // (r - s)
    f = n - 1 - g
    return n, r, s, f, g


def proj_coeffs(k, theta, other):
    """projector on the theta-eigenspace: (A - other I)(A - k I) / ((theta - other)(theta - k)) with
    A^2 = (k-2) I - A + 2 J  (lambda = 1, mu = 2).  Returns (a, b, c) with P = a I + b A + c J."""
    den = (theta - other) * (theta - k)
    # (A - oI)(A - kI) = A^2 - (o+k) A + o k I = (k-2) I - A + 2J - (o+k) A + o k I
    a = ((k - 2) + other * k) / den
    b = (-1 - other - k) / den
    c = 2.0 / den
    return a, b, c


def label_blocks(K, S):
    """T0_S, U0_S (floats) and Pi_S for the labels S (frozensets of letters) of a vertex with K letters."""
    n, r, s, f, g = params(K)
    t = r - s
    out = []
    for theta, other in ((s, r), (r, s)):
        a, b, c = proj_coeffs(K, theta, other)
        PNN = np.zeros((K + 1, K + 1))
        for i in range(K + 1):
            for j in range(K + 1):
                adj = 1 if i != j and (i == 0 or j == 0 or MATE(i - 1) == j - 1) else 0
                PNN[i, j] = a * (i == j) + b * adj + c
        P2N = np.zeros((len(S), K + 1))
        for x, l in enumerate(S):
            P2N[x, 0] = c
            for y in range(K):
                P2N[x, 1 + y] = b * (y in l) + c
        P22_0 = a * np.eye(len(S)) + c * np.ones((len(S), len(S)))
        out.append((t * (P22_0 - P2N @ np.linalg.pinv(PNN) @ P2N.T), t * b))
    (T0, bt), (U0, bu) = out
    assert abs(bt + 1) < 1e-12 and abs(bu - 1) < 1e-12, (bt, bu)     # T = T0 - A, U = U0 + A
    allL = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]
    B = np.zeros((K, len(allL)))
    for j, l in enumerate(allL):
        for y in l:
            B[y, j] = 1
    Pi = np.eye(len(allL)) - B.T @ np.linalg.solve(B @ B.T, B)
    pos = {l: j for j, l in enumerate(allL)}
    ix = [pos[l] for l in S]
    return T0, U0, Pi[np.ix_(ix, ix)], t, g - K, f - K


def integral_scale(Mx, maxd=200):
    """smallest D <= maxd with D * Mx integral (within 1e-9)."""
    for D in range(1, maxd + 1):
        if np.abs(D * Mx - np.round(D * Mx)).max() < 1e-9:
            return D
    raise ValueError("no small denominator")


def verify_spectral(edges_path, v=0):
    """Full-graph check of the identities on a real srg(n,k,1,2)."""
    E = [tuple(map(int, l.split()[:2])) for l in open(edges_path) if l.strip()]
    n = 1 + max(max(e) for e in E)
    A = np.zeros((n, n))
    for x, y in E:
        A[x, y] = A[y, x] = 1
    K = int(A[0].sum())
    _, r, s, f, g = params(K)
    t = r - s
    nb = [int(x) for x in np.nonzero(A[v])[0]]
    # letters: lines through v, numbered 2i, 2i+1
    order, seen = [], set()
    for y in nb:
        if y in seen:
            continue
        m = [z for z in nb if A[y, z]][0]
        order += [y, m]
        seen |= {y, m}
    letter = {y: i for i, y in enumerate(order)}
    far = [x for x in range(n) if x != v and not A[v, x]]
    lab = {x: frozenset(letter[y] for y in nb if A[x, y]) for x in far}
    S = [lab[x] for x in far]
    Nv = [v] + order
    res = {}
    for name, theta, other in (("T", s, r), ("U", r, s)):
        a, b, c = proj_coeffs(K, theta, other)
        P = a * np.eye(n) + b * A + c * np.ones((n, n))
        assert np.allclose(P @ P, P)
        Sch = t * (P[np.ix_(far, far)] - P[np.ix_(far, Nv)] @ np.linalg.pinv(P[np.ix_(Nv, Nv)]) @ P[np.ix_(Nv, far)])
        res[name] = Sch
    T0, U0, Pi, t2, rkT, rkU = label_blocks(K, S)
    Af = A[np.ix_(far, far)]
    evT, evU = np.linalg.eigvalsh(res["T"]), np.linalg.eigvalsh(res["U"])
    return {"graph": edges_path.replace("\\", "/").split("/")[-1], "K": K, "r": r, "s": s, "f": f, "g": g,
            "T_local_err": float(np.abs(res["T"] - (T0 - Af)).max()),
            "U_local_err": float(np.abs(res["U"] - (U0 + Af)).max()),
            "T+U-tPi_err": float(np.abs(res["T"] + res["U"] - t * Pi).max()),
            "T_eig": [round(float(evT.min()), 9), round(float(evT.max()), 9)], "rankT": int((evT > 1e-7).sum()),
            "U_eig": [round(float(evU.min()), 9), round(float(evU.max()), 9)], "rankU": int((evU > 1e-7).sum()),
            "expected_ranks": [g - K, f - K], "D(T0)": integral_scale(T0), "D(U0)": integral_scale(U0)}


if __name__ == "__main__":
    import json
    import sys
    for p in sys.argv[1:]:
        print(json.dumps(verify_spectral(p)), flush=True)
