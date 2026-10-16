"""c = 1: look for a STRUCTURAL 9-dim subspace V of R^Y with F|_V > 0 robustly (certificate of rank F >= 9).
Pattern types per outer line n = {s, s'} (s even, s' = s+1), on its 4 labels (2s, 2s', 3s, 3s'):
  P++ = (1,1,1,1), Phub = (1,1,-1,-1) (hub-odd), Pmate = (1,-1,1,-1) (mate-odd), Pboth = (1,-1,-1,1).
Each type spans a 5-dim space (one vector per outer line).  We report, over all c = 1 sides, the smallest eigenvalue of F
restricted to unions of types (and to their zero-sum versions), and how the top-9 eigenspace of F projects on each type.
usage: python c1_structV.py <distinct cache.jsonl> <cle3_sides.jsonl>"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c1_network import build

want = {json.loads(x)["src"] for x in open(sys.argv[2]) if json.loads(x)["c"] == 1}
Fs = []
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
    Fs.append(((F + F.T) / 2, Y))
pat = {"P++": (1, 1, 1, 1), "Phub": (1, 1, -1, -1), "Pmate": (1, -1, 1, -1), "Pboth": (1, -1, -1, 1)}
def basis(Y, types):
    cols = []
    for t in types:
        a, b, c, d_ = pat[t]
        for s in (4, 6, 8, 10, 12):
            v = np.zeros(20)
            for (r, x), w in zip(((2, s), (2, s + 1), (3, s), (3, s + 1)), (a, b, c, d_)):
                v[Y.index(frozenset((r, x)))] = w
            cols.append(v / 2)
    return np.array(cols).T
print("c = 1 sides:", len(Fs))
# projection of the top-9 eigenspace on each type
proj = {t: [] for t in pat}
for F, Y in Fs:
    ev, V = np.linalg.eigh(F)
    V9 = V[:, -9:]
    for t in pat:
        Bt = basis(Y, [t])
        proj[t].append(np.linalg.norm(Bt.T @ V9) ** 2)
print("mean squared projection of the top-9 eigenspace of F on each 5-dim type (sum = 9):")
for t in pat:
    print("   %-6s %.3f (min %.3f, max %.3f)" % (t, np.mean(proj[t]), min(proj[t]), max(proj[t])))
# smallest eigenvalue of F on unions of types
for k in (1, 2, 3):
    for types in itertools.combinations(pat, k):
        mins = []
        for F, Y in Fs:
            Bt = basis(Y, types)
            Q, _ = np.linalg.qr(Bt)
            mins.append(np.linalg.eigvalsh(Q.T @ F @ Q)[0])
        print("lambda_min(F | %s) (dim %d): min over sides %.4f, median %.4f" % ("+".join(types), 5 * k, min(mins), np.median(mins)))
