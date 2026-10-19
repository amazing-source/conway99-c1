"""Mod-p rank identity of a line (LAB 19/10/2026).  M = A - rI for a srg(v,k,1,2) with p | r - s (p = 7, r = 3 for
Conway; p = 3, r = 4 for v = 243).  For a line T with near set N[T] = T u N(T) and far set F:
    rank_p(M) = rank_p(M[N[T],N[T]]) + rank_p(R_T),   R_T = M[F,F] - M[F,N] M[N,N]^- M[N,F]   (generalised Schur)
holds as soon as every vector of ker_p M[N,N] is also killed by M[F,N] (then M[N,N]^- may be any generalised inverse).
Here: checks the kernel condition and the identity on real graphs (positive control of the mod-p linear algebra), and
reports d(T) = dim ker_p of the Laplacian of G_T and the ranks.
usage: python rank7_line.py <edges> <p> <r> [lines]"""
import sys
import numpy as np


def rank_mod(M, p):
    M = M.copy() % p
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = np.nonzero(M[r:, c])[0]
        if len(piv) == 0:
            continue
        i = r + piv[0]
        M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % p
        r += 1
        if r == rows:
            break
    return r


def kernel_mod(M, p):
    """basis of the right kernel of M over F_p (columns)"""
    M = M.copy() % p
    rows, cols = M.shape
    piv_cols, r = [], 0
    for c in range(cols):
        piv = np.nonzero(M[r:, c])[0] if r < rows else []
        if len(piv) == 0:
            continue
        i = r + piv[0]
        M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % p
        piv_cols.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv_cols]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv_cols):
            v[c] = (-M[i, f]) % p
        basis.append(v)
    return np.array(basis).T if basis else np.zeros((cols, 0), dtype=np.int64)


def ginv_mod(S, p):
    """a generalised inverse X with S X S = S over F_p (via row reduction of [S | I])"""
    n = S.shape[0]
    aug = np.concatenate([S % p, np.eye(n, dtype=np.int64)], axis=1)
    piv_cols, r = [], 0
    for c in range(n):
        piv = np.nonzero(aug[r:, c])[0] if r < n else []
        if len(piv) == 0:
            continue
        i = r + piv[0]
        aug[[r, i]] = aug[[i, r]]
        aug[r] = (aug[r] * pow(int(aug[r, c]), p - 2, p)) % p
        nz = np.nonzero(aug[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            aug[nz] = (aug[nz] - np.outer(aug[nz, c], aug[r])) % p
        piv_cols.append(c)
        r += 1
    E = aug[:, n:]                                   # E S = reduced row echelon form R (rows 0..r-1)
    X = np.zeros((n, n), dtype=np.int64)
    for i, c in enumerate(piv_cols):                 # X = P E with P placing pivot rows at pivot columns
        X[c] = E[i]
    assert (((S @ X) % p) @ S % p == S % p).all(), "generalised inverse failed"
    return X


def main():
    edges = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
    p, r = int(sys.argv[2]), int(sys.argv[3])
    nlines = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    v = 1 + max(max(e) for e in edges)
    A = np.zeros((v, v), dtype=np.int64)
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    M = (A - r * np.eye(v, dtype=np.int64)) % p
    rk = rank_mod(M, p)
    adj = [set(np.nonzero(A[i])[0]) for i in range(v)]
    lines = sorted({tuple(sorted((a, b, c))) for a in range(v) for b in adj[a] for c in adj[a] & adj[b]})
    print("v = %d, rank_%d(A - %dI) = %d, lines %d" % (v, p, r, rk, len(lines)), flush=True)
    step = max(1, len(lines) // nlines)
    for T in lines[::step][:nlines]:
        Ts = set(T)
        near = sorted({u for t in T for u in adj[t]} - Ts)
        Nn = list(T) + near
        F = [u for u in range(v) if u not in Ts and u not in set(near)]
        MNN = M[np.ix_(Nn, Nn)]
        MFN = M[np.ix_(F, Nn)]
        ker = kernel_mod(MNN, p)
        cond = bool(((MFN @ ker) % p == 0).all()) if ker.shape[1] else True
        X = ginv_mod(MNN, p)
        RT = (M[np.ix_(F, F)] - MFN @ X % p @ MFN.T) % p
        rN, rR = rank_mod(MNN, p), rank_mod(RT, p)
        G = A[np.ix_(near, near)]
        Lap = (3 * np.eye(len(near), dtype=np.int64) - G) % p
        d = len(near) - rank_mod(Lap, p)
        print("line %s: d(T) = %d, rank near = %d, kernel dim %d, kernel killed by M[F,N]: %s, rank far residue = %d,"
              " identity %s" % (T, d, rN, ker.shape[1], cond, rR, "OK" if rN + rR == rk else "FAILS (%d + %d != %d)" % (rN, rR, rk)),
              flush=True)


if __name__ == "__main__":
    main()
