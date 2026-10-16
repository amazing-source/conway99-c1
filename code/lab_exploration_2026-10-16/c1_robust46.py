"""c = 1: which 46-vertex sets N(l) u X (X = 10 of the 20 labels of Y = Y_2 u Y_3) give the most ROBUST certificate
lambda_2(A_H) < 3 (Conway forces lambda_2 = 3 exactly on every 46-vertex induced subgraph)?
Structured choices tested on all c = 1 sides; exhaustive search over all C(20,10) choices on a few sides.
usage: python c1_robust46.py <distinct cache.jsonl> <cle3_sides.jsonl> <n exhaustive>"""
import itertools, json, sys, time
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c1_network import build

want = {json.loads(x)["src"] for x in open(sys.argv[2]) if json.loads(x)["c"] == 1}
nex = int(sys.argv[3])
sides = []
for line in open(sys.argv[1]):
    d = json.loads(line)
    if d["src"] not in want:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S, Gv, Y, AG, B, AY = build(L, E)
    if np.sum(np.linalg.eigvalsh(3 * np.eye(36) - AG) < 1e-9) != 1:
        continue
    A = np.block([[AG, B], [B.T, AY]])
    sides.append((d["src"], A, Y))
print("c = 1 sides:", len(sides))
outer = list(range(4, 14))
def choice(Y, name):
    lab = lambda r, s: Y.index(frozenset((r, s)))
    if name == "Y3":
        return [lab(3, s) for s in outer]
    if name == "transversal even/odd":       # {2,s} for even s, {3,s} for odd s
        return [lab(2, s) if s % 2 == 0 else lab(3, s) for s in outer]
    if name == "two lines full + {2,3}x line3 even":
        return [lab(r, s) for r in (2, 3) for s in (4, 5, 6, 7)] + [lab(2, 8), lab(3, 8)]
    if name == "mates split":                 # {2,s},{3,s'} for each outer line (s even, s' odd)
        return [lab(2, s) for s in outer if s % 2 == 0] + [lab(3, s) for s in outer if s % 2 == 1]
def gap(A, X):
    kk = list(range(36)) + [36 + i for i in X]
    ev = np.sort(np.linalg.eigvalsh(A[np.ix_(kk, kk)]))[::-1]
    return 3 - ev[1]
names = ["Y3", "transversal even/odd", "two lines full + {2,3}x line3 even", "mates split"]
for nm in names:
    g = [gap(A, choice(Y, nm)) for _, A, Y in sides]
    print("%-38s: min gap 3 - lambda_2 = %+.4f  (negative = lambda_2 > 3 ; 0 = eigenvalue 3)  max %+.4f" % (nm, min(g), max(g)))
# exhaustive on the sides where Y3 is tightest
order = sorted(range(len(sides)), key=lambda i: gap(sides[i][1], choice(sides[i][2], "Y3")))
t0 = time.time()
for i in order[:nex]:
    src, A, Y = sides[i]
    best, bestX = -9, None
    for X in itertools.combinations(range(20), 10):
        g = gap(A, X)
        if g > best:
            best, bestX = g, X
    names_ = ["".join(map(str, sorted(Y[j]))) for j in bestX]
    print("exhaustive %s: best gap %.4f with X = %s  (Y3 gap %.4f)  [%.0f s]" % (src.split("\\")[-1], best, names_, gap(A, choice(Y, "Y3")), time.time() - t0))
