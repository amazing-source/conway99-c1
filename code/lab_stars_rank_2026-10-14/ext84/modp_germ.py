"""Local mod-p test of a four-star germ (LAB 16/10).

Global facts (Conway, vertex v, 84 labels): 8T = 24I - 8G - 3B'B - B'PB + 2J and 15U = 60I + 15G - 4B'B + B'PB - 2J are
integral, T U = 0, hence (8T)(15U) = 0 over Z.  For p = 3, 5 the matrix 15U mod p = Gp := (-4B'B + B'PB - 2J) mod p does
not depend on the graph G.  So 8T Gp = 0 (mod p).  If g in F_p^S has zero extension g~ = Gp h (h in F_p^84) supported
on S, then (8T g~)_S = 8T_SS g = 0 (mod p).  (MODp): 8T_SS g = 0 (mod p) for every g in Z_p(S) = {g : g~ in col(Gp)}.
Necessary for every four-star block of a Conway graph, of any rank."""
import sys, json, itertools
import numpy as np

LET = 14
LABELS84 = [(a, b) for a in range(LET) for b in range(a + 1, LET) if b != (a ^ 1)]

def geometry(labels):
    n = len(labels)
    B = np.zeros((LET, n), dtype=np.int64)
    for j, (a, b) in enumerate(labels):
        B[a, j] = B[b, j] = 1
    P = np.zeros((LET, LET), dtype=np.int64)
    for r in range(LET):
        P[r, r ^ 1] = 1
    return B, P

def rref_mod(M, p):
    """row-reduce a copy of M over F_p; returns (R, pivots)."""
    A = np.array(M, dtype=np.int64) % p
    rows, cols = A.shape
    piv = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        k = r + nz[0]
        A[[r, k]] = A[[k, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        for i in range(rows):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        piv.append(c)
        r += 1
    return A[:r], piv

def nullspace_mod(M, p):
    R, piv = rref_mod(M, p)
    cols = M.shape[1]
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-R[i, f]) % p
        basis.append(v)
    return np.array(basis, dtype=np.int64).reshape(len(basis), cols)

def rank_mod(M, p):
    return len(rref_mod(M, p)[1])

def Gp84(p):
    B, P = geometry(LABELS84)
    J = np.ones((84, 84), dtype=np.int64)
    return (-4 * B.T @ B + B.T @ P @ B - 2 * J) % p

def Zp(S_idx, p):
    """basis of Z_p(S): vectors G h (mod p) vanishing outside S, restricted to S."""
    G = Gp84(p)
    O = [i for i in range(84) if i not in S_idx]
    H = nullspace_mod(G[O, :], p)            # h with (G h)_O = 0
    if len(H) == 0:
        return np.zeros((0, len(S_idx)), dtype=np.int64)
    V = (H @ G.T) % p                         # rows = (G h)^T
    V = V[:, S_idx]
    R, piv = rref_mod(V, p)
    return R

def t8(labels, edges):
    n = len(labels)
    B, P = geometry(labels)
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in edges:
        G[i, j] = G[j, i] = 1
    J = np.ones((n, n), dtype=np.int64)
    return 24 * np.eye(n, dtype=np.int64) - 8 * G - 3 * B.T @ B - B.T @ P @ B + 2 * J, G

if __name__ == "__main__":
    for p in (3, 5):
        G = Gp84(p)
        print("p=%d: rank_p(15U mod p) on 84 labels = %d" % (p, rank_mod(G, p)))
    files = sys.argv[1:]
    for f in files:
        d = json.load(open(f))
        labels = [tuple(sorted(l)) for l in d["labels"]]
        S_idx = [LABELS84.index(l) for l in labels]
        M8, G = t8(labels, d["edges"])
        out = []
        for p in (3, 5):
            Z = Zp(S_idx, p)
            viol = (M8 @ Z.T) % p
            nviol = int(np.count_nonzero(np.any(viol, axis=0)))
            out.append("p=%d: dim Z_p(S)=%d, rank_p(8T_SS)=%d, violated basis vectors %d" % (p, len(Z), rank_mod(M8, p), nviol))
        print(f.split("/")[-1], " | ".join(out))
