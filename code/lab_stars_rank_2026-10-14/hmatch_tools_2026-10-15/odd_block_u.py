"""Where does U fail?  h-even / h-odd blocks of T and U (LAB 15/10/2026, mechanism A, question (i)).

Exact identities used (checked numerically below): K = D^T Q D with D the 14 x 84 letter-label incidence, and
Pi = I - D^T (D D^T)^-1 D, so for every label vector x on S with D x = 0:  T x = 3x - Gamma x  and  U x = 4x + Gamma x.
h-odd vectors x have D x = (al, -al, be, -be, 0, ..., 0), and the two star differences (kernel of T and U) span the
(al, be) directions, so on the odd side positivity is EXACTLY  spec(Gamma on V0-) in [-4, 3],  V0- = {x odd : D x = 0}
(dim 20), and Gamma on odd vectors only sees the average Gamma_0 = (Gamma + h Gamma h)/2.

For each structure: lambda_min of U on E+, on E- (the blocks A', C'), of U itself (all on the complement of the four
star vectors), lambda_min / lambda_max of Gamma on V0-, and the weights (l-side f_y, m-side e_y, C4) of the most negative
odd direction of U.
usage: python odd_block_u.py <json> [...]"""
import json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.')
sys.path.insert(0, '..')
from stars_rank import kval, LABELS

hm = {0: 1, 1: 0, 2: 3, 3: 2}
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}


def blocks(f):
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    K = np.array([[kval(a, b) for b in S] for a in S])
    T = 3 * np.eye(n) - G - K
    PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
    U = 7 * PiS - T
    D = D84[:, [pos[l] for l in S]]
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    # orbit representatives: the label containing 0 (l-side, C4) or 2 (m-side)
    reps = [i for i in range(n) if (0 in S[i]) or (2 in S[i] and not (S[i] & {0, 1}))]
    assert len(reps) == 22
    Ep = np.zeros((n, 22)); Em = np.zeros((n, 22))
    for k, r in enumerate(reps):
        Ep[r, k] = Ep[hp[r], k] = 1 / np.sqrt(2)
        Em[r, k] = 1 / np.sqrt(2); Em[hp[r], k] = -1 / np.sqrt(2)
    Z = np.array([[1.0 if y in s else 0.0 for s in S] for y in (0, 1, 2, 3)]).T     # star vectors (kernel of T, U)

    def perp_min(M, basis):
        # lambda_min of the form M on span(basis) minus the star vectors
        B = basis
        Zc = B.T @ Z                                         # star vectors expressed in the basis (they lie in E+ + E-)
        Q, _ = np.linalg.qr(Zc) if Zc.size else (np.zeros((B.shape[1], 0)), None)
        rkz = np.linalg.matrix_rank(Zc, 1e-9)
        Q = Q[:, :rkz]
        P = np.eye(B.shape[1]) - Q @ Q.T
        Mb = B.T @ M @ B
        w, V = np.linalg.eigh(P @ Mb @ P + 50 * (np.eye(B.shape[1]) - P))
        return w[0], B @ V[:, 0]
    Iall = np.eye(n)
    uA, _ = perp_min(U, Ep)
    uC, vC = perp_min(U, Em)
    uU, vU = perp_min(U, Iall)
    tT, _ = perp_min(T, Iall)
    # Gamma on V0- (odd, D x = 0)
    Dm = D @ Em
    _, s, Vt = np.linalg.svd(Dm)
    rk = int(np.sum(s > 1e-9))
    W = Em @ Vt[rk:].T                                       # orthonormal basis of V0- (20 vectors)
    gw = np.linalg.eigvalsh(W.T @ G @ W)
    # identity check: on V0-, U = 4 + Gamma, T = 3 - Gamma
    chk = max(np.abs(W.T @ U @ W - (4 * np.eye(W.shape[1]) + W.T @ G @ W)).max(),
              np.abs(W.T @ T @ W - (3 * np.eye(W.shape[1]) - W.T @ G @ W)).max())
    # weights of the most negative odd U-direction
    side = lambda i: "l" if (S[i] & {0, 1}) and not (S[i] & {2, 3}) else ("m" if (S[i] & {2, 3}) and not (S[i] & {0, 1}) else "c4")
    wts = Counter()
    for i in range(n):
        wts[side(i)] += vC[i] ** 2
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    return dict(nu=nu, psd=bool(d.get("psd")), uA=uA, uC=uC, uU=uU, tT=tT, gmin=gw[0], gmax=gw[-1], chk=chk,
                wl=wts["l"], wm=wts["m"], wc=wts["c4"])


if __name__ == "__main__":
    import glob, os
    files = []
    for a in sys.argv[1:]:
        files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
    sys.argv = [sys.argv[0]] + files
    rows = [blocks(f) for f in sys.argv[1:]]
    print("identity check (max deviation of U = 4 + Gamma, T = 3 - Gamma on V0-): %.2e" % max(r["chk"] for r in rows))
    tab = Counter()
    for r in rows:
        key = (r["nu"], "PSD" if r["psd"] else "-", "U fails on E-" if r["uC"] < -1e-9 else "E- ok",
               "U fails on E+" if r["uA"] < -1e-9 else "E+ ok", "U fails" if r["uU"] < -1e-9 else "U ok")
        tab[key] += 1
    for k, v in sorted(tab.items(), key=lambda kv: -kv[1]):
        print("  ", k, v)
    print("first rows: nu, lam_min U|E+, U|E-, U, T ; Gamma on V0-: min, max ; odd direction weights l / m / c4")
    for f, r in list(zip(sys.argv[1:], rows))[:12]:
        print("  %-28s %2d  %+.4f %+.4f %+.4f %+.4f   %+.4f %+.4f   %.2f %.2f %.2f" % (
            f.split('/')[-1][-28:], r["nu"], r["uA"], r["uC"], r["uU"], r["tT"], r["gmin"], r["gmax"], r["wl"], r["wm"], r["wc"]))
