"""c = 1: is the odd saturation lambda_1 (ODD-PURE margin) driven by a bottleneck of the cubic graph G_l?
For each c = 1 side (l = (0,1), iota = (2 3)): lambda_1, lambda_2 of (C Phi^+ C^t, K) [cle3_spectrum.side], the algebraic
connectivity a(G_l) = second smallest Laplacian eigenvalue, the smallest positive eigenvalue of K = T_UU.
usage: python c1_bottleneck.py <distinct cache.jsonl> <cle3_sides.jsonl>"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c1_network import build
from cle3_spectrum import kval, side

want = {}
for x in open(sys.argv[2]):
    s = json.loads(x)
    if s["c"] == 1:
        want[s["src"]] = 1
rows = []
for line in open(sys.argv[1]):
    d = json.loads(line)
    if d["src"] not in want:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S, Gv, Y, AG, B, AY = build(L, E)
    el = np.linalg.eigvalsh(3 * np.eye(36) - AG)
    if np.sum(el < 1e-9) != 1:
        continue
    idx = {l: i for i, l in enumerate(S)}
    G = np.zeros((44, 44))
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            G[idx[a], idx[b]] = G[idx[b], idx[a]] = 1
    T = 3 * np.eye(44) - G - np.array([[kval(a, b) for b in S] for a in S])
    s = side(S, idx, T, 2, 3)
    U = [l for l in S if not (l & {2, 3})]
    K = T[np.ix_([idx[u] for u in U], [idx[u] for u in U])]
    ek = np.linalg.eigvalsh(K)
    kmin = float(ek[ek > 1e-9][0])
    rows.append((s["lam"][0], s["lam"][1] if len(s["lam"]) > 1 else 0, float(el[1]), kmin, d["src"]))
rows.sort(reverse=True)
print("c = 1 sides: %d" % len(rows))
print("lambda_1 | lambda_2 | a(G_l) | min pos eig K | src   (top 12 by lambda_1)")
for r in rows[:12]:
    print("%.6f | %.4f | %.4f | %.4f | %s" % r)
a = np.array([r[2] for r in rows]); l1 = np.array([r[0] for r in rows]); km = np.array([r[3] for r in rows])
print("corr(lambda_1, a(G_l)) = %.3f ; corr(lambda_1, kmin) = %.3f" % (np.corrcoef(l1, a)[0, 1], np.corrcoef(l1, km)[0, 1]))
for th in (0.99, 0.95, 0.9):
    sel = l1 >= th
    if sel.any():
        print("lambda_1 >= %.2f: %d sides, a(G_l) in [%.4f, %.4f], kmin in [%.4f, %.4f]" % (th, sel.sum(), a[sel].min(), a[sel].max(), km[sel].min(), km[sel].max()))
print("all: a(G_l) in [%.4f, %.4f]" % (a.min(), a.max()))
