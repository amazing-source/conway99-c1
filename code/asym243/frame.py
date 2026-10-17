"""Eigenspace-surgery view of a switch A -> A' supported on F x F.
For srg(243,22,1,2): A = 9 P_4 - 5 I + J/9, so A' - A = 9 (P'_4 - P_4).
The admissible free-region rotations live in X(F) = E_4(F) + E_{-5}(F), the eigenvectors supported on F."""
import numpy as np, sys
from lib243 import *


def supported_eigvecs(A, F, theta):
    """orthonormal basis of {x in ker(A - theta I) : supp x subset F}."""
    n = len(A); R = [i for i in range(n) if i not in set(F)]
    w, V = np.linalg.eigh(A.astype(float))
    E = V[:, np.abs(w - theta) < 1e-6]                 # n x m basis of eigenspace
    # want E c with (E c)_R = 0
    ER = E[R, :]
    if len(R) == 0:
        return E
    u, s, vt = np.linalg.svd(ER)
    rank = int((s > 1e-8).sum())
    null = vt[rank:].T
    X = E @ null
    if X.shape[1]:
        q, _ = np.linalg.qr(X)
        return q
    return X


def proj4(A):
    w, V = np.linalg.eigh(A.astype(float))
    E = V[:, np.abs(w - 4) < 1e-6]
    return E @ E.T


if __name__ == "__main__":
    A = load_edges("bvls243.edges"); B = load_edges("twin243_switched.edges")
    D = B - A
    F = sorted(set(np.nonzero(D)[0]))
    print("changed vertices", len(F), "changed edges +", int((D == 1).sum()) // 2, "-", int((D == -1).sum()) // 2)
    P, Pp = proj4(A), proj4(B)
    print("max |D - 9(P'_4-P_4)| =", np.abs(D - 9 * (Pp - P)).max())
    for th in (4, -5):
        X = supported_eigvecs(A, F, th)
        print(f"BvLS: dim E_{th}(F) =", X.shape[1])
        X = supported_eigvecs(B, F, th)
        print(f"twin: dim E_{th}(F) =", X.shape[1])
    DF = D[np.ix_(F, F)].astype(float)
    ev = np.round(np.linalg.eigvalsh(DF), 6)
    vals, cnt = np.unique(ev, return_counts=True)
    print("spectrum of D on F:", dict(zip(vals.tolist(), cnt.tolist())))
    # principal angles between W0 = E_4(F) of A and W1 = E_4(F) of B
    W0 = supported_eigvecs(A, F, 4); W1 = supported_eigvecs(B, F, 4)
    s = np.linalg.svd(W0.T @ W1, compute_uv=False)
    print("cosines of principal angles W0,W1:", np.unique(np.round(s, 6), return_counts=True))
