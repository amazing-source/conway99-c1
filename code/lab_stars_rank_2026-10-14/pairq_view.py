"""Partial-star quotient of a four-star structure (14/10/2026).
For the outer letters x (4..13), d_x = indicator of the labels of S containing x. On these vectors the form of T is
M_D = D T D^T = 6 I + 2 (J - Mt) - E, with E[x][y] = number of ordered pairs (a, b) in {0,1,2,3}^2 with ax ~ by.
So T >= 0 forces E <= 4 on mate-symmetric vectors orthogonal to 1 and E <= 8 on mate-antisymmetric vectors.
Prints the spectrum of M_D and of E on both subspaces.  usage: python pairq_view.py <json> ..."""
import json
import sys
import numpy as np
from stars_rank import kval

for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    G = np.zeros((n, n))
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    outer = list(range(4, 14))
    Dm = np.array([[1.0 if x in l else 0.0 for l in S] for x in outer])
    MD = Dm @ T @ Dm.T
    E = Dm @ G @ Dm.T
    Mt = np.array([[1.0 if y == (x ^ 1) else 0.0 for y in outer] for x in outer])
    check = np.allclose(MD, 6 * np.eye(10) + 2 * (np.ones((10, 10)) - Mt) - E)
    sym = np.array([[1.0 if (x ^ 1) == outer[k] or x == outer[k] else 0.0 for k in range(10)] for x in outer[::2]]) / np.sqrt(2)
    anti = np.array([[(1.0 if x == outer[k] else (-1.0 if (x ^ 1) == outer[k] else 0.0)) for k in range(10)] for x in outer[::2]]) / np.sqrt(2)
    one = np.ones(5) / np.sqrt(5)
    Ps = sym.T @ (np.eye(5) - np.outer(one, one))     # mate-symmetric, orthogonal to 1
    U1, s1, _ = np.linalg.svd(Ps, full_matrices=False)
    Bs = U1[:, s1 > 1e-9]
    Ba = anti.T
    print("%s: identity M_D = 6I + 2(J - Mt) - E holds: %s; lambda_min(M_D) = %.4f" % (f, check, np.linalg.eigvalsh(MD)[0]))
    print("   E on mate-symmetric (perp 1): max %.3f (must be <= 4);  E on mate-antisymmetric: max %.3f (must be <= 8)"
          % (np.linalg.eigvalsh(Bs.T @ E @ Bs)[-1], np.linalg.eigvalsh(Ba.T @ E @ Ba)[-1]))
