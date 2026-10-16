"""(i) drop_bal == b7 - b3 on every record; (ii) for every block with b-4 >= 1: the +-1 parity products
h_sigma({r,s}) = sigma(r) sigma(s) on the 40 outer labels (0 on corners), sigma(mate a) = -sigma(a), 64 choices up to sign,
that satisfy Gamma_S h = -4 h, and the dimension of their span compared with b-4."""
import itertools, json, sys, collections
import numpy as np
recs = {json.loads(x)["src"]: json.loads(x) for x in open(sys.argv[1])}
bad = [s for s, r in recs.items() if r["dbal"] != r["b7"] - r["b3"]]
print("records %d, drop_bal != b7 - b3 on %d" % (len(recs), len(bad)))
agg = collections.Counter()
for line in open(sys.argv[2]):
    d = json.loads(line)
    r = recs.get(d["src"])
    if r is None or r["bm4"] == 0:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S = [l for l in L if l & {0, 1, 2, 3}]
    G = np.array([[1 if i != j and frozenset((a, b)) in E else 0 for j, b in enumerate(S)] for i, a in enumerate(S)])
    good = []
    for bits in itertools.product((1, -1), repeat=6):   # sigma(0), sigma(2), sigma(4), ..., sigma(12); sigma(odd) = -sigma(even)
        sig = {}
        for k, b in enumerate(bits):
            sig[2 * k + (0 if k < 2 else 0)] = b
        sig = {}
        evens = [0, 2, 4, 6, 8, 10, 12]
        vals = (1,) + bits                                   # sigma(0) = 1 fixes the global sign
        for e, b in zip(evens, vals):
            sig[e], sig[e + 1] = b, -b
        h = np.array([0 if l in ({0, 2}, {0, 3}, {1, 2}, {1, 3}) else sig[min(l)] * sig[max(l)] for l in map(set, S)])
        if np.array_equal(G @ h, -4 * h):
            good.append(h)
    rk = np.linalg.matrix_rank(np.array(good)) if good else 0
    agg[(r["grid"], r["bm4"], len(good), int(rk))] += 1
print("(grid, b-4, number of parity products that are -4 eigenvectors, rank of their span): count")
for k, v in sorted(agg.items()):
    print("  ", k, v)
