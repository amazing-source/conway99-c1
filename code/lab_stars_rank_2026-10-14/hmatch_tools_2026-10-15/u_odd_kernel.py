"""The odd -4 directions of the averaged structure (LAB 15/10/2026, mechanism A, question (i)).

On V0- = {x h-odd, D x = 0} one has U = 4 + Gamma_0 (odd_block_u.py), so the odd block of U is singular exactly when
Gamma_0 has the eigenvalue -4 on V0-.  If w is such a vector and U >= 0, then U w = 0, hence Gamma w = -4 w, hence
Delta w = 0 (Delta = Gamma - h Gamma h maps odd vectors to even ones, Gamma = Gamma_0 + Delta / 2).
For each structure: multiplicity of -4 for Gamma_0 on V0-, a basis of that eigenspace in odd orbit coordinates
(a_y on f_y = 1_0y - 1_1y, b_y on e_y = 1_2y - 1_3y, c1 on 1_02 - 1_13, c2 on 1_03 - 1_12), whether Gamma w = -4 w on
all of S (as a 44-vector), and |Delta w|.
usage: python u_odd_kernel.py <json> [verbose]"""
import json, sys
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, '.')
sys.path.insert(0, '..')
from stars_rank import LABELS

hm = {0: 1, 1: 0, 2: 3, 3: 2}
OUT = list(range(4, 14))


def analyse(f, verbose=True):
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    Ph = np.zeros((n, n))
    for i in range(n):
        Ph[hp[i], i] = 1
    G0 = (G + Ph @ G @ Ph) / 2
    Dl = G - Ph @ G @ Ph
    # odd basis in orbit coordinates
    cols, names = [], []
    for y in OUT:
        v = np.zeros(n); v[idx[frozenset((0, y))]] = 1; v[idx[frozenset((1, y))]] = -1; cols.append(v); names.append("f%d" % y)
    for y in OUT:
        v = np.zeros(n); v[idx[frozenset((2, y))]] = 1; v[idx[frozenset((3, y))]] = -1; cols.append(v); names.append("e%d" % y)
    v = np.zeros(n); v[idx[frozenset((0, 2))]] = 1; v[idx[frozenset((1, 3))]] = -1; cols.append(v); names.append("c1")
    v = np.zeros(n); v[idx[frozenset((0, 3))]] = 1; v[idx[frozenset((1, 2))]] = -1; cols.append(v); names.append("c2")
    E = np.array(cols).T                                      # 44 x 22, odd orbit vectors (norm^2 2)
    Dm = np.zeros((4, n))
    for i, s in enumerate(S):
        for a in (0, 1, 2, 3):
            if a in s:
                Dm[a, i] = 1
    # V0- in orbit coordinates: kernel of Dm E (the outer letters see nothing on odd vectors)
    _, s_, Vt = np.linalg.svd(Dm @ E)
    rk = int(np.sum(s_ > 1e-9))
    C = Vt[rk:].T                                             # 22 x 20 coefficient basis
    W = E @ C
    Q, _ = np.linalg.qr(W)
    w_, V = np.linalg.eigh(Q.T @ G0 @ Q)
    mult = int(np.sum(np.abs(w_ + 4) < 1e-8))
    res = dict(mult=mult, lmin=w_[0], ok_full=[], dnorm=[], coeffs=[])
    if mult:
        Wk = Q @ V[:, np.abs(w_ + 4) < 1e-8]                  # 44 x mult
        # orbit coordinates of the eigenspace basis
        coef, *_ = np.linalg.lstsq(E, Wk, rcond=None)
        for k in range(mult):
            wv = Wk[:, k]
            res["ok_full"].append(float(np.abs(G0 @ wv + 4 * wv).max()))
            res["dnorm"].append(float(np.linalg.norm(Dl @ wv)))
            c = coef[:, k] / np.abs(coef[:, k]).max()
            res["coeffs"].append(c)
        if verbose:
            print("%s: lambda_min(Gamma_0 on V0-) = %.6f, multiplicity of -4 = %d" % (f, w_[0], mult))
            # a nicer basis: reduced row echelon of the coefficient vectors
            M = coef.T
            M = M / np.abs(M).max()
            for k in range(mult):
                c = res["coeffs"][k]
                terms = ["%+.3f %s" % (c[j], names[j]) for j in range(22) if abs(c[j]) > 1e-6]
                print("   w%d: |Gamma_0 w + 4 w|_inf = %.1e, |Delta w| = %.4f" % (k, res["ok_full"][k], res["dnorm"][k]))
                print("       " + " ".join(terms))
    elif verbose:
        print("%s: lambda_min(Gamma_0 on V0-) = %.6f, no -4 eigenvalue" % (f, w_[0]))
    return res


if __name__ == "__main__":
    analyse(sys.argv[1])
