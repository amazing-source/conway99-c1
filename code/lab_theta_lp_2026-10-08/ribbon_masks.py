"""C1, lab session, 2026-10-09. Boundary of a clean closed transport ribbon of length m, with the full one-vertex filters
of Codex's note 222 (not only the balancing of ribbon6_boundary.py).

H = L(D), D the circular ladder (cylinder) or the Moebius ladder on 2m vertices: 3m points, 4-regular, induced.
A mask b in {0,1}^H (neighbours in H of an outside vertex) is kept when
  1. b is a coclique of H and every point u outside b has at most 2 neighbours in b;
  2. no pair of b is saturated (2 - A_uv - (A^2)_uv = 0);
  3. the two projector blocks on H + the vertex are positive semidefinite, EXACTLY (rational Schur complements):
        [ Q-   1-9b ]      [ Q+    11b-2 ]        Q- = 27I - 9A + J,  Q+ = 44I + 11A - 2J
        [ .     28  ],     [ .      42   ],
     for a singular Q the transversal vector must lie in the image of Q.
Then the multiplicities x_b >= 0 must satisfy: sum = 99 - 3m; every point has 10 outside neighbours; every non-adjacent
pair u, v has 2 - (A^2)_uv common outside neighbours. Rational feasibility is decided exactly (Farkas certificate).

  python ribbon_masks.py <m> <cylinder|moebius>   or   <number of centres w> open        One process, below 1 GB, seconds to a minute."""
import sys, itertools, collections, json
from fractions import Fraction as Fr
m = int(sys.argv[1]); MO = sys.argv[2] == "moebius"; OPEN = sys.argv[2] == "open"
if OPEN:
    w = m; n = 3 * w + 2
    ia = lambda i: i - 1; ib = lambda i: (w + 1) + i - 1; ic = lambda i: 2 * (w + 1) + i - 1
    A = [[0] * n for _ in range(n)]
    def e(x, y): A[x][y] = A[y][x] = 1
    for i in range(1, w + 1):
        e(ic(i), ia(i)); e(ic(i), ia(i + 1)); e(ia(i), ia(i + 1)); e(ic(i), ib(i)); e(ic(i), ib(i + 1)); e(ib(i), ib(i + 1))
else:
    n = 3 * m
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
A2 = [[len(adj[i] & adj[j]) for j in range(n)] for i in range(n)]
assert all(A2[i][j] == 1 for i in range(n) for j in adj[i]), "an edge of H in two triangles or none: not a ribbon of the family"
assert all(A2[i][j] <= 2 for i in range(n) for j in range(n) if i != j and j not in adj[i])


def solve_psd_border(Q):
    """returns a function test(c, d): is [[Q, c], [c^T, d]] PSD, for a PSD rational matrix Q (exact)."""
    N = len(Q); M = [[Fr(x) for x in r] for r in Q]
    # greedy choice of a maximal invertible principal submatrix by exact LDL^T pivoting
    I = []; L = {}                                    # we keep the inverse of Q[I, I] by bordering
    inv = []
    for i in range(N):
        J = I + [i]; B = [[M[p][q] for q in J] for p in J]
        # determinant test through Gaussian elimination
        T = [r[:] for r in B]; ok = True
        for c in range(len(J)):
            p = next((r for r in range(c, len(J)) if T[r][c] != 0), None)
            if p is None: ok = False; break
            T[c], T[p] = T[p], T[c]
            for r in range(c + 1, len(J)):
                if T[r][c] != 0:
                    f = T[r][c] / T[c][c]; T[r] = [x - f * y for x, y in zip(T[r], T[c])]
        if ok: I = J
    k = len(I); B = [[M[p][q] for q in I] + [Fr(int(a == b)) for b in range(k)] for a, p in enumerate(I)]
    for c in range(k):
        p = next(r for r in range(c, k) if B[r][c] != 0); B[c], B[p] = B[p], B[c]
        pv = B[c][c]; B[c] = [x / pv for x in B[c]]
        for r in range(k):
            if r != c and B[r][c] != 0:
                f = B[r][c]; B[r] = [x - f * y for x, y in zip(B[r], B[c])]
    Binv = [r[k:] for r in B]

    def test(c, d):
        w = [sum(Binv[a][b] * c[I[b]] for b in range(k)) for a in range(k)]
        if any(sum(M[u][I[a]] * w[a] for a in range(k)) != c[u] for u in range(N)): return False      # c not in the image
        return sum(c[I[a]] * w[a] for a in range(k)) <= d
    return test, k


Qm = [[(27 if i == j else 0) - 9 * A[i][j] + 1 for j in range(n)] for i in range(n)]
Qp = [[(44 if i == j else 0) + 11 * A[i][j] - 2 for j in range(n)] for i in range(n)]
tm, rkm = solve_psd_border(Qm); tp, rkp = solve_psd_border(Qp)
print("%s %d, %s: %d points; rank of Q- %d, rank of Q+ %d" % ("w =" if OPEN else "m =", m, sys.argv[2], n, rkm, rkp))
delta = {(u, v): 2 - A[u][v] - A2[u][v] for u in range(n) for v in range(u + 1, n)}
masks = []; stats = collections.Counter()
def rec(start, cur):
    b = [1 if h in cur else 0 for h in range(n)]
    if all(len(adj[u] & set(cur)) <= 2 for u in range(n) if u not in cur):
        stats["local"] += 1
        if tm([Fr(1 - 9 * x) for x in b], Fr(28)) and tp([Fr(11 * x - 2) for x in b], Fr(42)): masks.append(tuple(cur))
    for h in range(start, n):
        if all(h not in adj[g] and delta[(min(g, h), max(g, h))] > 0 for g in cur): rec(h + 1, cur + [h])
rec(0, [])
print("   masks passing the local filters: %d; passing the two exact spectral filters: %d, by size %s"
      % (stats["local"], len(masks), dict(sorted(collections.Counter(len(s) for s in masks).items()))))
pairs = [(p, q) for p in range(n) for q in range(p + 1, n) if q not in adj[p]]
rows = [[1] * len(masks)]; rhs = [99 - n]; lab = ["total"]
for h in range(n): rows.append([1 if h in s else 0 for s in masks]); rhs.append(14 - len(adj[h])); lab.append("point %d" % h)
for (p, q) in pairs: rows.append([1 if (p in s and q in s) else 0 for s in masks]); rhs.append(delta[(p, q)]); lab.append("pair %d %d" % (p, q))
sys.path.insert(0, "lap_harm")
src = open("lap_harm/harm4_exact.py").read(); code = src[src.index("def simplex(cols, c, g):"):src.index("import time")]
ns = {"Fr": Fr}; exec(code, ns); simplex = ns["simplex"]
R = len(rows); cols = [[Fr(rows[r][j]) for r in range(R)] for j in range(len(masks))] + [[Fr(int(r == q)) for r in range(R)] for q in range(R)]
out = simplex(cols, [Fr(0)] * len(masks) + [Fr(-1)] * R, [Fr(x) for x in rhs])
assert out[0] == "optimal"
if out[1] < 0:
    y = out[3]
    assert all(sum(y[r] * rows[r][j] for r in range(R)) >= 0 for j in range(len(masks))) and sum(y[r] * rhs[r] for r in range(R)) < 0
    print("   EXACT: the multiplicity system is INFEASIBLE (Farkas vector checked, y . rhs = %s, support %d rows)" % (sum(y[r] * rhs[r] for r in range(R)), sum(1 for v in y if v)))
    json.dump({"m": m, "closure": sys.argv[2], "masks": [list(s) for s in masks], "rows": lab, "rhs": rhs, "y": [str(v) for v in y]}, open("ribbon_masks_%d_%s_certificate.json" % (m, sys.argv[2]), "w"))
else:
    lam = out[2]; use = collections.Counter()
    for s, c in zip(masks, lam[:len(masks)]):
        if c: use[len(s)] += c
    print("   EXACT: the multiplicity system is feasible over the rationals; one solution uses masks by size:", {k: str(v) for k, v in sorted(use.items())})
