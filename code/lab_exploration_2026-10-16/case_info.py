"""LEMMA 3-SPEC helper: nu <= 14 + 2 K0 - m3 (m3 = mult_3 Gamma_S, K0 = dim E_3(Gamma_S) cap ker B)."""
import sys
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod
P = 1000000007
Bm = [[1 if r in l else 0 for l in S] for r in range(14)]
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)


def info(EE):
    G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
    X = [[(3 if i == j else 0) - G[i][j] for j in range(44)] for i in range(44)]
    m3 = 44 - rank_mod(X, P)
    k0 = 44 - rank_mod(X + Bm, P)
    T8 = 24 * np.eye(44, dtype=np.int64) - 8 * np.array(G, dtype=np.int64) - K8
    nu = 44 - rank_mod(T8.tolist(), P)
    psd = bool(np.linalg.eigvalsh(T8 / 8.0)[0] > -1e-9)
    return nu, m3, k0, 14 + 2 * k0 - m3, psd
