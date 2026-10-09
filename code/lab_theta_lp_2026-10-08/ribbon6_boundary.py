"""C1, lab session, 2026-10-09. Can a CLEAN transport ribbon of length m exist in an srg(99,14,1,2)?  Boundary test.

The ribbon: points a_i, b_i, c_i (i mod m), lines {c_i, a_i, a_(i+1)} and {c_i, b_i, b_(i+1)}, closed as a cylinder or as
a Moebius band; H = the induced 4-regular graph on the 3m points (no other edge, no identification).
Facts used (all from A^2 + A = 12 I + 2 J and the spectrum 14, 3, -4):
  (1) an outside vertex z meets H in a coclique S (its mask): two adjacent points of H have their third point in H;
  (2) every point of H has exactly 10 outside neighbours;
  (3) two non-adjacent points p, q of H have exactly 2 - (number of common neighbours in H) common outside neighbours;
  (4) if 3 is an eigenvalue of A_H on a vector y of sum zero (equality case of positivity: m = 3 and m = 6), then y
      extended by zero is a 3-eigenvector of A, so every mask S is balanced: sum of y over S = 0;
  (5) there are 99 - 3m outside vertices.
Unknowns: the multiplicity x_S >= 0 of every admissible mask. The system (2), (3), (5) is linear. It is solved over the
rationals (exact simplex, Farkas certificate when infeasible) and, when the rational system is feasible, over the
integers by scipy's MILP (HiGHS) as an indication only.

  python ribbon6_boundary.py <m> <cylinder|moebius>          One process, seconds, below 500 MB."""
import sys, itertools, collections
from fractions import Fraction as Fr
import numpy as np
m = int(sys.argv[1]); MO = sys.argv[2] == "moebius"; n = 3 * m
idx = lambda t, i: {"a": 0, "b": 1, "c": 2}[t] * m + i % m
A = [[0] * n for _ in range(n)]
def e(x, y): A[x][y] = A[y][x] = 1
for i in range(m):
    if i < m - 1 or not MO: an, bn = idx("a", i + 1), idx("b", i + 1)
    else: an, bn = idx("b", 0), idx("a", 0)
    e(idx("c", i), idx("a", i)); e(idx("c", i), an); e(idx("a", i), an)
    e(idx("c", i), idx("b", i)); e(idx("c", i), bn); e(idx("b", i), bn)
assert all(sum(r) == 4 for r in A)
adj = [set(j for j in range(n) if A[i][j]) for i in range(n)]


def nullspace(M):
    """rational nullspace of an integer matrix (list of rows)"""
    M = [[Fr(x) for x in r] for r in M]; rows, cols = len(M), len(M[0]); piv = []; r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [x / pv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    out = []
    for c in range(cols):
        if c in piv: continue
        v = [Fr(0)] * cols; v[c] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][c]
        out.append(v)
    return out


# 3-eigenvectors of A_H of sum zero
K3 = nullspace([[A[i][j] - (3 if i == j else 0) for j in range(n)] for i in range(n)] + [[1] * n])
print("m = %d, %s: %d points; dimension of the sum-zero 3-eigenspace of A_H: %d" % (m, "Moebius" if MO else "cylinder", n, len(K3)))
# admissible masks: balanced cocliques
masks = []
def rec(start, cur):
    if cur and all(sum(y[h] for h in cur) == 0 for y in K3): masks.append(tuple(cur))
    for h in range(start, n):
        if all(h not in adj[g] for g in cur): rec(h + 1, cur + [h])
rec(0, [])
by = collections.Counter(len(s) for s in masks)
print("   balanced cocliques by size (the empty mask is counted apart):", dict(sorted(by.items())))
pairs = [(p, q) for p in range(n) for q in range(p + 1, n) if q not in adj[p]]
dem = {(p, q): 2 - len(adj[p] & adj[q]) for p, q in pairs}
assert all(d >= 0 for d in dem.values())
# rows: one per point (= 10), one per non-adjacent pair (= demand), one for the total number of non-empty masks (<= 99 - n)
rows = []; rhs = []
for h in range(n): rows.append([1 if h in s else 0 for s in masks]); rhs.append(10)
for (p, q) in pairs: rows.append([1 if (p in s and q in s) else 0 for s in masks]); rhs.append(dem[(p, q)])
tot = [1] * len(masks)
print("   %d masks, %d equalities, at most %d non-empty masks" % (len(masks), len(rows), 99 - n))
if not masks or any(r_ > 0 and not any(row) for row, r_ in zip(rows, rhs)):
    bad = [i for i, (row, r_) in enumerate(zip(rows, rhs)) if r_ > 0 and not any(row)]
    lab = lambda i: "point %d" % i if i < n else "pair %s" % (pairs[i - n],)
    print("   INFEASIBLE at sight: %d demands have no admissible mask, e.g. %s (demand %d)" % (len(bad), lab(bad[0]), rhs[bad[0]]))
    sys.exit()
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
Aeq = np.array(rows, dtype=float); beq = np.array(rhs, dtype=float)
res = linprog(np.ones(len(masks)), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(masks), method="highs")
print("   rational relaxation (float): status %d, %s" % (res.status, "minimum number of non-empty masks %.4f" % res.fun if res.status == 0 else res.message))
if res.status == 0:
    res2 = milp(np.ones(len(masks)), constraints=[LinearConstraint(Aeq, beq, beq)], integrality=np.ones(len(masks)), bounds=Bounds(0, np.inf))
    print("   integer problem (HiGHS, indication): status %d, %s" % (res2.status, "minimum number of non-empty masks %.1f (allowed %d)" % (res2.fun, 99 - n) if res2.status == 0 else res2.message))
    if res2.status == 0:
        x = np.round(res2.x).astype(int); use = collections.Counter()
        for s, c in zip(masks, x):
            if c: use[len(s)] += c
        print("   one integer solution uses masks by size:", dict(sorted(use.items())), "-> empty masks:", 99 - n - int(x.sum()))
else:
    # exact Farkas certificate: maximise -(sum of artificial slacks); a negative optimum with its dual vector y proves that
    # the equalities have no non-negative rational solution:  y . column(S) >= 0 for every mask S  and  y . rhs < 0
    sys.path.insert(0, "lap_harm")
    import importlib.util, json
    src = open("lap_harm/harm4_exact.py").read(); code = src[src.index("def simplex(cols, c, g):"):src.index("import time")]
    ns = {"Fr": Fr}; exec(code, ns); simplex = ns["simplex"]
    R = len(rows); cols = [[Fr(rows[r][j]) for r in range(R)] for j in range(len(masks))] + [[Fr(int(r == q)) for r in range(R)] for q in range(R)]
    cost = [Fr(0)] * len(masks) + [Fr(-1)] * R
    out = simplex(cols, cost, [Fr(x) for x in rhs])
    assert out[0] == "optimal" and out[1] < 0, out[0]
    y = out[3]
    assert all(sum(y[r] * rows[r][j] for r in range(R)) >= 0 for j in range(len(masks))) and sum(y[r] * rhs[r] for r in range(R)) < 0
    lab = lambda i: "point %d" % i if i < n else "pair %s" % (pairs[i - n],)
    supp = [(lab(r), str(y[r])) for r in range(R) if y[r] != 0]
    print("   EXACT: infeasible. Farkas vector y checked: y . column >= 0 for all %d masks, y . rhs = %s < 0; support %d rows" % (len(masks), sum(y[r] * rhs[r] for r in range(R)), len(supp)))
    json.dump({"m": m, "closure": sys.argv[2], "masks": [list(s) for s in masks], "rows": [lab(r) for r in range(R)], "rhs": rhs, "y": [str(v) for v in y]}, open("ribbon%d_%s_certificate.json" % (m, sys.argv[2]), "w"))
