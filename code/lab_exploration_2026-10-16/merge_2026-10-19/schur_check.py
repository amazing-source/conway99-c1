"""Check over F_7: symmetric M = [[A, B], [B^T, D]], Z = ker A, W = B^T Z (dim w), Q = D - B^T X B (X symmetric
g-inverse of A) restricted to W^perp.  Claim: rank M = rank A + 2 w + rank(Q | W^perp).  Random tests."""
import random, sys, os
import numpy as np
TR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "treasure_2026-10-19")
sys.path.insert(0, TR)
from rank7_line import rank_mod, kernel_mod, ginv_mod
p = 7
rng = np.random.default_rng(3)
bad = 0
for trial in range(300):
    na, nf = int(rng.integers(4, 9)), int(rng.integers(3, 8))
    ra = int(rng.integers(1, na))
    U = rng.integers(0, p, (na, ra)); S = rng.integers(0, p, (ra, ra)); S = (S + S.T) % p
    A = (U @ S @ U.T) % p
    B = rng.integers(0, p, (na, nf))
    if trial % 3 == 0:                      # make some kernel directions balanced
        Z = kernel_mod(A, p)
        if Z.shape[1] >= 1:
            z = Z[:, 0]
            # project B's columns so that z^T B = 0 for this z (if possible)
            j = int(np.nonzero(z)[0][0]); inv = pow(int(z[j]), p - 2, p)
            for c in range(nf):
                s = int(z @ B[:, c]) % p
                B[j, c] = (B[j, c] - s * inv) % p
    D = rng.integers(0, p, (nf, nf)); D = (D + D.T) % p
    M = np.block([[A, B], [B.T, D]]) % p
    X = ginv_mod(A, p); X = (X @ A % p @ X.T) % p
    Z = kernel_mod(A, p)
    W = (B.T @ Z) % p if Z.shape[1] else np.zeros((nf, 0), dtype=np.int64)
    w = rank_mod(W, p) if W.shape[1] else 0
    Q = (D - B.T @ X % p @ B) % p
    # basis of W^perp
    P = kernel_mod(W.T % p, p) if W.shape[1] else np.eye(nf, dtype=np.int64)
    rq = rank_mod((P.T @ Q % p @ P) % p, p) if P.shape[1] else 0
    lhs, rhs = rank_mod(M, p), rank_mod(A, p) + 2 * w + rq
    if lhs != rhs:
        bad += 1
print("rank formula mismatches:", bad, "/ 300")
