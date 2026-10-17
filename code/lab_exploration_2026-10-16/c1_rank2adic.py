"""The rank condition read at the prime 2 (exploration, LAB 17/10/2026).
M = 8 T_S = -K8 + 8 X, X = 3I - Gamma, K8 = 3|a n b| + m(a,b) - 2 (fixed).  Local Smith form of K8 at 2 (computed below):
U K8 V = Delta with 6 units, one 2, one 4, six 8*odd and 30 zeros (U, V invertible over Z_(2)).  Eliminating the 8 pivots of
valuation <= 2 changes the rest only by multiples of 16, so
    rank_Q(T_S) = 8 + rank_Q2(N),   N = -Delta_r/8 + (U X V)_rr + 2 W,      r = the 36 other positions,
    N mod 2 = D' + U_r (I + Gamma) V_r (mod 2),   D' = diag(1 x 6, 0 x 30).
Conway (rank_Q T_S <= 30) => rank_F2(N mod 2) <= 22, i.e. N mod 2 (36 x 36, AFFINE in Gamma over F_2) has a radical of
dimension >= 14.  Equivalently: at most 22 invariant factors of 8 T_S have 2-adic valuation exactly 3.
Data (val2_data.py, 400 positive blocks with a c = 1 side): 22 (5 blocks), 24, 26, 28 for all the others.
This module: (1) the local Smith transforms U, V of K8 mod 2^K, verified; (2) N mod 2 for a structure; (3) check that
rank_F2(N mod 2) equals the number of valuation-3 invariant factors on data blocks.
usage: python c1_rank2adic.py <distinct cache.jsonl> [blocks]"""
import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402

KBITS = 40
MOD = 1 << KBITS


def v2(x):
    k = 0
    while x % 2 == 0:
        x //= 2
        k += 1
    return k


def smith2(M):
    """local Smith form at 2 with transforms: returns (U, V, d) with U M V = diag(d) mod 2^KBITS (lists of ints)."""
    n = len(M)
    A = [[int(x) % MOD for x in row] for row in M]
    U = [[int(i == j) for j in range(n)] for i in range(n)]
    V = [[int(i == j) for j in range(n)] for i in range(n)]
    d = [0] * n
    for t in range(n):
        best = None
        for i in range(t, n):
            for j in range(t, n):
                if A[i][j]:
                    v = v2(A[i][j])
                    if best is None or v < best[0]:
                        best = (v, i, j)
        if best is None:
            break
        v, r, c = best
        A[t], A[r] = A[r], A[t]
        U[t], U[r] = U[r], U[t]
        for row in A:
            row[t], row[c] = row[c], row[t]
        for row in V:
            row[t], row[c] = row[c], row[t]
        p = A[t][t]
        uinv = pow(p >> v, -1, MOD)
        for i in range(t + 1, n):
            if A[i][t]:
                f = ((A[i][t] >> v) * uinv) % MOD
                A[i] = [(a - f * b) % MOD for a, b in zip(A[i], A[t])]
                U[i] = [(a - f * b) % MOD for a, b in zip(U[i], U[t])]
        for j in range(t + 1, n):
            if A[t][j]:
                f = ((A[t][j] >> v) * uinv) % MOD
                for i in range(n):
                    A[i][j] = (A[i][j] - f * A[i][t]) % MOD
                    V[i][j] = (V[i][j] - f * V[i][t]) % MOD
        d[t] = A[t][t]
    return U, V, d


K8 = [[int(x) for x in row] for row in C.K8]
U, V, DIAG = smith2(K8)
VALS = [v2(x) if x else None for x in DIAG]
REST = [t for t in range(C.n) if VALS[t] is None or VALS[t] >= 3]
assert len(REST) == 36 and sum(1 for t in REST if VALS[t] == 3) == 6, VALS
U2 = np.array([[U[t][i] % 2 for i in range(C.n)] for t in REST], dtype=np.int64)        # 36 x 44
V2 = np.array([[V[i][t] % 2 for t in REST] for i in range(C.n)], dtype=np.int64)        # 44 x 36
DP = np.diag([1 if VALS[t] == 3 else 0 for t in REST]).astype(np.int64)


def verify():
    n = C.n
    Ui = np.array(U, dtype=object)
    Vi = np.array(V, dtype=object)
    P = (Ui.dot(np.array(K8, dtype=object)).dot(Vi)) % MOD
    off = sum(1 for i in range(n) for j in range(n) if i != j and P[i, j] != 0)
    return off == 0 and all(P[i, i] == DIAG[i] % MOD for i in range(n))


def n_mod2(G):
    """N mod 2 for the 0/1 adjacency G (44 x 44 numpy)."""
    X = (np.eye(C.n, dtype=np.int64) + G) % 2
    return (DP + U2 @ X @ V2) % 2


def rank2(A):
    A = [list(map(int, row)) for row in np.array(A) % 2]
    r = 0
    n, m = len(A), len(A[0])
    for c in range(m):
        pv = next((i for i in range(r, n) if A[i][c]), None)
        if pv is None:
            continue
        A[r], A[pv] = A[pv], A[r]
        for i in range(n):
            if i != r and A[i][c]:
                A[i] = [a ^ b for a, b in zip(A[i], A[r])]
        r += 1
    return r


def main():
    print("Smith transforms verified mod 2^%d: %s ; valuations: %s" % (
        KBITS, verify(), {k: VALS.count(k) for k in set(VALS)}), flush=True)
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
    from stars_rank import kval
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    ok = bad = 0
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for i, j in itertools.combinations(range(C.n), 2):
            if frozenset((C.S[i], C.S[j])) in E:
                G[i, j] = G[j, i] = 1
        T8 = 24 * np.eye(C.n, dtype=np.int64) - 8 * G - C.K8
        _, _, dd = smith2(T8.tolist())
        n3 = sum(1 for x in dd if x and v2(x) == 3)
        r = rank2(n_mod2(G))
        if r == n3:
            ok += 1
        else:
            bad += 1
            print("  mismatch: rank_F2(N) %d, valuation-3 count %d" % (r, n3))
        if ok + bad >= lim:
            break
    print("rank_F2(N mod 2) == number of valuation-3 invariant factors: %d agree, %d disagree" % (ok, bad))


if __name__ == "__main__":
    main()
