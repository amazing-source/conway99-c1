"""Checks for NOTE_RESIDU_GLOBAL.md (LAB 20/10/2026).  One process, numpy + exact integers, < 1 min.

T1  bordered determinant: det M[{t0} u near] = det [[-3, 1_C0^T], [1_C0, G - 3I]] = 144 tau  (exact, c = 1)
T2  discriminant of the near block: chi(disc_nd M_NN mod 7) = (-1)^(c+1) prod_i (tau_i | 7), rank 38 - c  (d = c)
T3  splitting rule in the engine's formalism (random symmetric M over F_7, X = reflexive g-inverse of M_UU):
    if rank M[:, U] = rank M_UU (balanced) then rank M = rank M_UU + rank S and
    chi(disc_nd S) = chi(disc_nd M) * chi(disc_nd M_UU),  S = M_FF - M_FU X M_UF
T4  Schur identity behind 'H = 7 Pi_T' for ARBITRARY far-far values:  B^T Y^+ B = E^T Z E  (names only), with
    Y = 3I - A_ball + J/9 (39 x 39), B = -E_ext + J/9, Z = (3I - G + J)^-1; also Y >= 0 of rank 36 and range condition
T5  mod-7 form of the same:  e_w^T X e_w' = 4 - e_w^T Z e_w'  (mod 7), i.e. 7 Pi_T = -Res_T (mod 7)
usage: python residu_checks.py <out.json>
"""
import json
import os
import random
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
sys.path.insert(0, os.path.join(HERE, "..", "treasure_2026-10-19"))
from ll_test import block_gt, components, gt_matrix, pairs_of, random_gt  # noqa: E402
from rank7_line import ginv_mod, rank_mod  # noqa: E402

P = 7
n, N = 12, 36
SQ = {1, 2, 4}


def chi(a):
    a %= P
    return 0 if a == 0 else (1 if a in SQ else -1)


def bareiss_det(M):
    A = [[int(x) for x in row] for row in M]
    k = len(A)
    sign, prev = 1, 1
    for c in range(k - 1):
        if A[c][c] == 0:
            sw = next((r for r in range(c + 1, k) if A[r][c] != 0), None)
            if sw is None:
                return 0
            A[c], A[sw] = A[sw], A[c]
            sign = -sign
        for i in range(c + 1, k):
            for j in range(c + 1, k):
                A[i][j] = (A[i][j] * A[c][c] - A[i][c] * A[c][j]) // prev
        prev = A[c][c]
    return sign * A[k - 1][k - 1]


def tau_of(G):
    L = 3 * np.eye(G.shape[0], dtype=np.int64) - G
    return bareiss_det(L[1:, 1:])


def disc_nd(S):
    """(rank, discriminant of the non-degenerate part) of a symmetric matrix over F_7 (congruence diagonalisation)"""
    A = np.array(S, dtype=np.int64) % P
    k = A.shape[0]
    d, rk = 1, 0
    idx = list(range(k))
    while idx:
        piv = next((i for i in idx if A[i, i] % P), None)
        if piv is None:
            pair = next(((i, j) for i in idx for j in idx if i < j and A[i, j] % P), None)
            if pair is None:
                break
            i, j = pair
            A[i, :] = (A[i, :] + A[j, :]) % P          # e_i -> e_i + e_j: diagonal becomes 2 a_ij != 0
            A[:, i] = (A[:, i] + A[:, j]) % P
            piv = i
        a = int(A[piv, piv])
        inv = pow(a, P - 2, P)
        rest = [i for i in idx if i != piv]
        for i in rest:
            f = A[i, piv] * inv % P
            if f:
                A[i, :] = (A[i, :] - f * A[piv, :]) % P
                A[:, i] = (A[:, i] - f * A[:, piv]) % P
        d = d * a % P
        rk += 1
        idx = rest
    return rk, d


def near_block(G):
    A = np.zeros((3 + N, 3 + N), dtype=np.int64)
    for a in range(3):
        for b in range(3):
            if a != b:
                A[a, b] = 1
    for c in range(3):
        for i in range(n):
            A[c, 3 + c * n + i] = A[3 + c * n + i, c] = 1
    A[3:, 3:] = G
    return A


def comp_taus(G):
    nc, comp = components(G)
    out = []
    for c in range(nc):
        idx = [i for i in range(N) if comp[i] == c]
        out.append(tau_of(G[np.ix_(idx, idx)]))
    return nc, out


def random_names(rng):
    P_ = pairs_of(n)
    pp, qq, ss = rng.choice(P_), rng.choice(P_), rng.choice(P_)
    e = np.zeros(N, dtype=np.int64)
    e[[pp[0], pp[1], n + qq[0], n + qq[1], 2 * n + ss[0], 2 * n + ss[1]]] = 1
    return e


def main():
    out_path = sys.argv[1]
    rng = random.Random(20261020)
    res = {}
    # ---------------- T1 + T2 (c = 1)
    t1_ok = t1_n = 0
    t2_ok = t2_n = 0
    tau_hist = {"0": 0, "+1": 0, "-1": 0}
    for _ in range(150):
        s01, s12, s20, _t = random_gt(n, rng, 1)
        G = gt_matrix(n, s01, s12, s20)
        tau = tau_of(G)
        A = near_block(G)
        M = A - 3 * np.eye(3 + N, dtype=np.int64)
        idx = [0] + list(range(3, 3 + N))
        dB = bareiss_det(M[np.ix_(idx, idx)])
        t1_n += 1
        t1_ok += int(dB == 144 * tau)
        c = chi(tau)
        tau_hist["0" if c == 0 else ("+1" if c > 0 else "-1")] += 1
        if c != 0:
            rk, d = disc_nd(M)
            t2_n += 1
            t2_ok += int(rk == 37 and chi(d) == c)
    res["T1_det_eq_144tau"] = [t1_ok, t1_n]
    res["T2_c1_rule"] = [t2_ok, t2_n]
    res["tau_mod7_classes_c1"] = tau_hist
    # ---------------- T2 for c = 2, 3 without torsion
    for sizes in ([3, 3], [2, 4], [1, 5], [2, 2, 2], [1, 1, 4], [1, 2, 3]):
        ok = tot = skipped = 0
        for _ in range(40):
            s01, s12, s20, _t = block_gt(n, rng, sizes)
            G = gt_matrix(n, s01, s12, s20)
            nc, taus = comp_taus(G)
            if any(t % P == 0 for t in taus):
                skipped += 1
                continue
            M = near_block(G) - 3 * np.eye(3 + N, dtype=np.int64)
            rk, d = disc_nd(M)
            pred = (-1) ** (nc + 1)
            for t in taus:
                pred *= chi(t)
            tot += 1
            ok += int(rk == 38 - nc and chi(d) == pred)
        res["T2_blocks_" + "+".join(str(6 * s) for s in sizes)] = [ok, tot, "torsion skipped", skipped]
    # ---------------- T3 splitting rule, engine formalism
    t3 = {"balanced": 0, "rank_additive": 0, "rule_ok": 0}
    nprng = np.random.default_rng(7)
    for trial in range(300):
        nn, r, u = 60, int(nprng.integers(20, 50)), int(nprng.integers(5, 30))
        Bm = nprng.integers(0, P, size=(r, nn))
        Q = nprng.integers(0, P, size=(r, r))
        Q = (Q + Q.T) % P
        if rank_mod(Q, P) < r:
            continue
        M = (Bm.T @ Q @ Bm) % P
        U = list(range(u))
        F = list(range(u, nn))
        MUU = M[np.ix_(U, U)]
        if rank_mod(M[:, U], P) != rank_mod(MUU, P):
            continue
        t3["balanced"] += 1
        X = ginv_mod(MUU, P)
        X = (X @ MUU % P @ X.T) % P
        S = (M[np.ix_(F, F)] - M[np.ix_(F, U)] @ X % P @ M[np.ix_(U, F)]) % P
        rM, dM = disc_nd(M)
        rU, dU = disc_nd(MUU)
        rS, dS = disc_nd(S)
        if rM == rU + rS:
            t3["rank_additive"] += 1
            t3["rule_ok"] += int(chi(dS) == chi(dM) * chi(dU))
    res["T3_splitting"] = t3
    # ---------------- T4 + T5 Schur identity (real) and its mod-7 form
    t4 = {"lines": 0, "Y_psd_rank36": 0, "range_ok": 0, "identity_maxerr": 0.0, "T5_ok": 0, "T5_n": 0}
    for _ in range(20):
        s01, s12, s20, _t = random_gt(n, rng, 1)
        G = gt_matrix(n, s01, s12, s20)
        tau = tau_of(G)
        A = near_block(G).astype(float)
        Y = 3 * np.eye(3 + N) - A + np.ones((3 + N, 3 + N)) / 9
        ev = np.linalg.eigvalsh(Y)
        t4["lines"] += 1
        t4["Y_psd_rank36"] += int(ev.min() > -1e-9 and int((ev > 1e-9).sum()) == 36)
        Yp = np.linalg.pinv(Y, rcond=1e-10)
        L = 3 * np.eye(N) - G
        Z = np.linalg.inv(L + np.ones((N, N)))
        Es = np.array([random_names(rng) for _ in range(12)]).T          # 36 x 12 name vectors
        Eext = np.vstack([np.zeros((3, Es.shape[1])), Es])
        Bm = -Eext + np.ones(Eext.shape) / 9
        resid = (np.eye(3 + N) - Y @ Yp) @ Bm
        t4["range_ok"] += int(np.abs(resid).max() < 1e-8)
        lhs = Bm.T @ Yp @ Bm
        rhs = Es.T @ Z @ Es
        t4["identity_maxerr"] = max(t4["identity_maxerr"], float(np.abs(lhs - rhs).max()))
        if tau % P:
            Mi = (near_block(G) - 3 * np.eye(3 + N, dtype=np.int64)) % P
            X = ginv_mod(Mi, P)
            X = (X @ Mi % P @ X.T) % P
            Lj = (L.astype(np.int64) + 1) % P
            # inverse of L + J mod 7 by solving with the g-inverse routine (L + J is invertible mod 7 when 7 ∤ 36 tau)
            Zi = ginv_mod(Lj, P)
            assert ((Lj @ Zi) % P == np.eye(N, dtype=np.int64)).all()
            Eext_i = np.vstack([np.zeros((3, Es.shape[1]), dtype=np.int64), Es])
            beta = (Eext_i.T @ X @ Eext_i) % P
            green = (4 - Es.T @ Zi @ Es) % P
            t4["T5_n"] += 1
            t4["T5_ok"] += int((beta == green).all())
    res["T4_T5"] = t4
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
