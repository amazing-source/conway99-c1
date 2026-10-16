"""For every PSD block: which of the letter involutions tau01 = (0 1), tau23 = (2 3), tau = (0 1)(2 3), and the swaps
(0 2)(1 3), (0 3)(1 2) are automorphisms of the label graph Gamma_S; and for blocks with b-4 >= 1, whether the balanced
-4 eigenspace lies in D = {h : h_1s = -h_0s, h_3s = -h_2s, corners 0}."""
import json, sys, collections
import numpy as np
recs = {json.loads(x)["src"]: json.loads(x) for x in open(sys.argv[1])}
PERMS = {"(01)": {0: 1, 1: 0}, "(23)": {2: 3, 3: 2}, "(01)(23)": {0: 1, 1: 0, 2: 3, 3: 2},
         "(02)(13)": {0: 2, 2: 0, 1: 3, 3: 1}, "(03)(12)": {0: 3, 3: 0, 1: 2, 2: 1}}
agg = collections.Counter()
agg4 = collections.Counter()
for line in open(sys.argv[2]):
    d = json.loads(line)
    r = recs.get(d["src"])
    if r is None:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S = [l for l in L if l & {0, 1, 2, 3}]
    idx = {l: i for i, l in enumerate(S)}
    autos = []
    for name, p in PERMS.items():
        f = lambda l: frozenset(p.get(a, a) for a in l)
        if all((frozenset((f(a), f(b))) in E) == (frozenset((a, b)) in E) for i, a in enumerate(S) for b in S[i + 1:]):
            autos.append(name)
    agg[("G" if r["grid"] else "NG", r["bm4"] > 0, tuple(autos))] += 1
    if r["bm4"] > 0:
        n = 44
        G = np.array([[1 if i != j and frozenset((a, b)) in E else 0 for j, b in enumerate(S)] for i, a in enumerate(S)], dtype=float)
        B = np.array([[1 if q in l else 0 for l in S] for q in range(14)], dtype=float)
        M = np.vstack([G + 4 * np.eye(n), B])
        u, s, vt = np.linalg.svd(M)
        K = vt[np.sum(s > 1e-9):]          # orthonormal basis of the balanced -4 eigenspace
        # projector onto D
        P = np.zeros((n, n))
        for l in S:
            if len(l & {0, 1}) and not len(l & {2, 3}):
                s_ = min(l - {0, 1}) if l - {0, 1} else None
            # build D basis instead
        Dv = []
        for s_ in range(4, 14):
            for (a, b) in ((0, 1), (2, 3)):
                v = np.zeros(n); v[idx[frozenset((a, s_))]] = 1; v[idx[frozenset((b, s_))]] = -1; Dv.append(v / np.sqrt(2))
        Dm = np.array(Dv)
        res = K - (K @ Dm.T) @ Dm
        inD = bool(np.max(np.abs(res)) < 1e-8)
        agg4[(r["bm4"], inD, tuple(autos))] += 1
print("(grid?, b-4>0, automorphisms among the 5 letter involutions): count")
for k, v in sorted(agg.items()):
    print("  ", k, v)
print("blocks with b-4 >= 1: (b-4, -4 eigenspace inside D?, automorphisms): count")
for k, v in sorted(agg4.items()):
    print("  ", k, v)
