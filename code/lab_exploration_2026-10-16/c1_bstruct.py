"""c = 1, statement b >= 1: range(F) contains a nonzero vector supported on Y_2 (= a linear relation satisfied by the
Y_2-parts of ALL profiles).  Is there a STRUCTURAL such vector?  For each c = 1 side and each hub x (other hub o):
R_o = range(F) n R^{Y_o} (dimension b), and the squared cosine between R_o and structured vectors on Y_o:
  line-antisymmetric d_n = e_{o s} - e_{o s'} (mates s, s'), line-symmetric u_n = e_{os} + e_{os'},
  M-matching differences e_{os} - e_{ot} for M_o edges inside Y_o, sigma-transversal patterns, and their spans.
usage: python c1_bstruct.py <distinct cache.jsonl> <cle3_sides.jsonl>"""
import json, sys, collections
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c1_network import build

want = {json.loads(x)["src"] for x in open(sys.argv[2]) if json.loads(x)["c"] == 1}
res = collections.defaultdict(list)
dims = collections.Counter()
for line in open(sys.argv[1]):
    d = json.loads(line)
    if d["src"] not in want:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S, Gv, Y, AG, B, AY = build(L, E)
    Lg = 3 * np.eye(36) - AG
    el, Vl = np.linalg.eigh(Lg)
    if np.sum(el < 1e-9) != 1:
        continue
    Lp = (Vl[:, el > 1e-9] / el[el > 1e-9]) @ Vl[:, el > 1e-9].T
    F = 3 * np.eye(20) - AY + np.ones((20, 20)) / 12 - B.T @ Lp @ B
    F = (F + F.T) / 2
    ef, Vf = np.linalg.eigh(F)
    Rg = Vf[:, ef > 1e-8]                     # orthonormal basis of range(F)
    for o in (2, 3):
        io = [i for i, y in enumerate(Y) if o in y]
        ix = [i for i in range(20) if i not in io]
        # R_o = vectors in range(F) vanishing on Y_x: kernel of the restriction of Rg to the ix rows
        Mx = Rg[ix, :]
        u, s, vt = np.linalg.svd(Mx)
        null = vt[np.sum(s > 1e-8):].T          # coefficients
        Ro = Rg @ null                            # vectors in range(F) supported on Y_o
        Ro = Ro[io, :]
        q, _ = np.linalg.qr(Ro) if Ro.shape[1] else (np.zeros((10, 0)), None)
        dims[Ro.shape[1]] += 1
        lab = lambda s: io.index(Y.index(frozenset((o, s)))) if frozenset((o, s)) in Y else None
        def cos2(vec):
            vec = vec / np.linalg.norm(vec)
            return float(np.linalg.norm(q.T @ vec) ** 2) if q.shape[1] else 0.0
        anti = []
        for s in (4, 6, 8, 10, 12):
            v = np.zeros(10); v[lab(s)] = 1; v[lab(s + 1)] = -1; anti.append(v)
            res["line-antisym single"].append(cos2(v))
        sym = []
        for s in (4, 6, 8, 10, 12):
            v = np.zeros(10); v[lab(s)] = 1; v[lab(s + 1)] = 1; sym.append(v)
        # M_o edges inside Y_o
        for i in range(10):
            for j in range(i + 1, 10):
                if AY[io[i], io[j]]:
                    v = np.zeros(10); v[i] = 1; v[j] = -1
                    res["M-edge difference"].append(cos2(v))
                    v2 = np.zeros(10); v2[i] = 1; v2[j] = 1
                    res["M-edge sum"].append(cos2(v2))
        # span-level: dimension of R_o n span(anti)
        A_ = np.array(anti).T
        Qa, _ = np.linalg.qr(A_)
        res["dim(R_o n line-antisym)"].append(int(np.sum(np.linalg.svd(q.T @ Qa, compute_uv=False) > 1 - 1e-8)) if q.shape[1] else 0)
        S_ = np.array(sym).T; Qs, _ = np.linalg.qr(S_)
        res["dim(R_o n line-sym)"].append(int(np.sum(np.linalg.svd(q.T @ Qs, compute_uv=False) > 1 - 1e-8)) if q.shape[1] else 0)
print("dim R_o (= b) distribution:", dict(sorted(dims.items())))
for k, v in res.items():
    v = np.array(v)
    if k.startswith("dim("):
        print("%-28s: distribution %s" % (k, dict(sorted(collections.Counter(v.tolist()).items()))))
    else:
        print("%-28s: cos^2 to R_o: min %.3f  median %.3f  max %.3f  (1 = inside R_o)  [fraction = 1: %.3f]" % (
            k, v.min(), np.median(v), v.max(), np.mean(v > 1 - 1e-6)))
