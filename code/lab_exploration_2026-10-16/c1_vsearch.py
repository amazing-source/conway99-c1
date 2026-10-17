"""Which canonical subspace V of R^Y keeps F (20x20 Schur of T_S onto the far labels Y of l) farthest from singular?
Conway: dim ker F >= 12, so ker F meets every subspace V with dim(V) + 12 > 20 + dim(V cap trivial):
  for V avoiding the trivial kernel vectors (1_Y, 1_Y2 - 1_Y3), dim(ker F cap V) >= dim V - 8.
Canonical pieces (invariant under the 2<->3 swap iota, the 5 mate flips mu_j and the S5 of the lines 2..6):
  per rectangle Q_1j = {2,2j},{2,2j+1},{3,2j},{3,2j+1}: characters (iota, mu) in {++,+-,-+,--}; over the 5 rectangles each
  character gives a 5-dim space = trivial (1) + standard (4).  8 pieces.  We test every sum of pieces of dim >= 9,
  report min over data of lambda_min(F|V on V minus trivial) and the max over data of dim(ker F cap V).
usage: python c1_vsearch.py <distinct_cache.jsonl> <max sides>"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, gl_connected

def F_of(EE):
    n = 44
    G = np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        if frozenset((S[i], S[j])) in EE:
            G[i, j] = G[j, i] = 1
    K8 = np.array([[k8(a, b) for b in S] for a in S], float)
    T = (24 * np.eye(n) - 8 * G - K8) / 8
    if np.linalg.eigvalsh(T)[0] < -1e-9:
        return None
    ix = [S.index(l) for l in XL]
    iy = [S.index(l) for l in Y]
    Txx, Txy, Tyy = T[np.ix_(ix, ix)], T[np.ix_(ix, iy)], T[np.ix_(iy, iy)]
    return Tyy - Txy.T @ np.linalg.pinv(Txx, rcond=1e-10) @ Txy

# basis of Y-coordinates
Ylist = list(Y)
pos = {l: i for i, l in enumerate(Ylist)}
pieces = {}
chars = {"++": (1, 1), "+-": (1, -1), "-+": (-1, 1), "--": (-1, -1)}
for cname, (ei, em) in chars.items():
    vecs = []
    for j in range(2, 7):
        v = np.zeros(20)
        for a, sa in ((2, 1), (3, ei)):
            for s, sm in ((2 * j, 1), (2 * j + 1, em)):
                v[pos[frozenset((a, s))]] = sa * sm
        vecs.append(v / 2.0)
    Vc = np.array(vecs).T                      # 20 x 5, orthonormal columns
    triv = Vc @ (np.ones(5) / np.sqrt(5))
    U, s_, Wt = np.linalg.svd(np.eye(5) - np.outer(np.ones(5), np.ones(5)) / 5)
    std = Vc @ U[:, :4]
    pieces[cname + "T"] = triv.reshape(20, 1)
    pieces[cname + "S"] = std
T1 = np.zeros(20); T2 = np.zeros(20)
for l in Ylist:
    T1[pos[l]] = 1
    T2[pos[l]] = 1 if 2 in l else -1
trivial = np.array([T1, T2]).T

def main():
    mx = int(sys.argv[2])
    Fs = []
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        for side in (0, 1):
            L, EE = relabel(S0, E0, side)
            conn, degok = gl_connected(EE)
            if not (conn and degok):
                continue
            F = F_of(EE)
            if F is not None:
                Fs.append(F)
        if len(Fs) >= mx:
            break
    names = sorted(pieces)
    res = []
    for r in range(1, len(names) + 1):
        for combo in itertools.combinations(names, r):
            B = np.hstack([pieces[c] for c in combo])
            d = B.shape[1]
            # remove trivial directions contained in V
            Q, _ = np.linalg.qr(B)
            Pt = Q @ Q.T
            tin = [t for t in (T1, T2) if np.linalg.norm(Pt @ t - t) < 1e-9]
            if tin:
                Tm = np.array(tin).T
                Tq, _ = np.linalg.qr(Tm)
                Q2 = Q - Tq @ (Tq.T @ Q)
                u, sv, _ = np.linalg.svd(Q2, full_matrices=False)
                Q = u[:, sv > 1e-9]
            de = Q.shape[1]
            if de < 9:
                continue
            need = de - 8
            worst, maxk = 1e9, 0
            for F in Fs:
                ev = np.linalg.eigvalsh(Q.T @ F @ Q)
                worst = min(worst, ev[0])
                maxk = max(maxk, int(np.sum(np.abs(ev) < 1e-7)))
            res.append((worst, combo, de, need, maxk))
    res.sort(key=lambda t: -t[0])
    print("positive c=1 sides:", len(Fs))
    print("best canonical subspaces (dim without trivial, Conway needs ker cap V >= dim-8):")
    for worst, combo, de, need, maxk in res[:12]:
        print("   lam_min(F|V) >= %.4f   dim %2d  Conway needs ker dim >= %d   data max ker dim %d   V = %s" % (worst, de, need, maxk, "+".join(combo)))
    odd = [t for t in res if set(t[1]) == {"-+T", "-+S", "--T", "--S"}]
    print("ODD sector for comparison:", ["%.5f dim %d" % (t[0], t[2]) for t in odd])

main()
