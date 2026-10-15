"""h-block structure of real six-star blocks of srg(243) (LAB 15/10/2026): for each pair of the three lines, h = mate
swap on that pair; T = [[A, B], [B^T, C]] in (h-even, h-odd); nullities of A, C, T, rank of B, and the dimensions of
the projections of ker T on the two parts.  usage: python hblocks243.py <block json> [...]"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_gen import Model
for f in sys.argv[1:]:
    d = json.load(open(f))
    M = Model(d["k"], d["r"], d["s"])
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    ii = [M.pos[l] for l in S]
    K = M.Kfull[np.ix_(ii, ii)]
    G = np.zeros((n, n))
    for i, j in d["edges"]: G[i, j] = G[j, i] = 1
    T = M.r * np.eye(n) - G - K
    w, V = np.linalg.eigh(T); N = V[:, np.abs(w) < 1e-8]
    stars = d["stars"]; lines = [(stars[2*t], stars[2*t+1]) for t in range(len(stars)//2)]
    out = []
    for (a, a2), (b, b2) in itertools.combinations(lines, 2):
        hm = {a: a2, a2: a, b: b2, b2: b}
        hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
        H = np.zeros((n, n))
        for i in range(n): H[hp[i], i] = 1
        Pp, Pm = (np.eye(n) + H) / 2, (np.eye(n) - H) / 2
        dp, dm = int(round(np.trace(Pp))), int(round(np.trace(Pm)))
        Qp = np.linalg.svd(Pp)[0][:, :dp]; Qm = np.linalg.svd(Pm)[0][:, :dm]
        A = Qp.T @ T @ Qp; C = Qm.T @ T @ Qm; B = Qp.T @ T @ Qm
        nz = lambda X: int(np.sum(np.abs(np.linalg.eigvalsh(X)) < 1e-8))
        out.append("pair %s%s: dim E+ %d, E- %d | nullity A %d, C %d | rank B %d | ker T on E+ %d, on E- %d"
                   % ((a, a2), (b, b2), dp, dm, nz(A), nz(C), int(np.linalg.matrix_rank(B, tol=1e-8)),
                      int(np.linalg.matrix_rank(Pp @ N, tol=1e-7)), int(np.linalg.matrix_rank(Pm @ N, tol=1e-7))))
    print("%s: nullity %d" % (f, N.shape[1])); print("   " + "\n   ".join(out))
