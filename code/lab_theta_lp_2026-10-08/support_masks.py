"""C1, lab session, 2026-10-09. One-vertex boundary test for an arbitrary induced support H of an srg(99,14,1,2)
(general form of ribbon_masks.py; same filters as Codex's note 222, exact arithmetic).

H is given by its adjacency. Necessary conditions on H itself: an edge has at most one common neighbour, a non-edge at
most two, and the two projector blocks Q- = 27I - 9A + J, Q+ = 44I + 11A - 2J are positive semidefinite.
A mask b (neighbours in H of an outside vertex z) is kept when
  - for u in b: at most one neighbour of u lies in b, and then the edge has no triangle inside H (z is its third point);
  - for u not in b: at most two neighbours of u lie in b;
  - no pair of b is saturated: adjacent pairs of b need 1 - (A^2)_uv = 1, non-adjacent pairs need 2 - (A^2)_uv >= 1;
  - the bordered blocks [[Q-, 1 - 9b], [., 28]] and [[Q+, 11b - 2], [., 42]] are positive semidefinite (exact).
Multiplicities x_b >= 0:  sum = 99 - |H|;  every point u has 14 - deg(u) outside neighbours;  every pair u < v has
exactly 1 - (A^2)_uv (adjacent) or 2 - (A^2)_uv (non-adjacent) common outside neighbours. Decided exactly over Q.

Used as a module: verdict(n, edges) -> dict.  As a script:  python support_masks.py window5
  runs the five-centre open window of a transport geodesic with every single extra edge and every single identification
  of two roles (up to the symmetries: exchange of the two strands, reversal).  One process, below 1 GB."""
import sys, itertools, collections, time
from fractions import Fraction as Fr
import numpy as np


def _simplex():
    src = open(__file__.replace("support_masks.py", "lap_harm/harm4_exact.py")).read()
    code = src[src.index("def simplex(cols, c, g):"):src.index("import time")]
    ns = {"Fr": Fr}; exec(code, ns); return ns["simplex"]


simplex = _simplex()


def border_tester(Q):
    """exact test of positive semidefiniteness of [[Q, c], [c^T, d]] for a PSD integer matrix Q; None if Q is not PSD"""
    N = len(Q); w = np.linalg.eigvalsh(np.array(Q, dtype=float))
    if w.min() < -1e-7: return None, 0
    M = [[Fr(x) for x in r] for r in Q]; I = []
    for i in range(N):                                   # greedy maximal invertible principal submatrix (exact elimination)
        J = I + [i]; T = [[M[p][q] for q in J] for p in J]; ok = True
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
    # exact confirmation that Q itself is PSD: Q = Q[:, I] B^-1 Q[I, :] and B positive definite (leading minors > 0 by construction order)
    def test(c, d):
        wv = [sum(Binv[a][b] * c[I[b]] for b in range(k)) for a in range(k)]
        if any(sum(M[u][I[a]] * wv[a] for a in range(k)) != c[u] for u in range(N)): return False
        return sum(c[I[a]] * wv[a] for a in range(k)) <= d
    return test, k


def verdict(n, edges, want_certificate=False):
    A = [[0] * n for _ in range(n)]
    for x, y in edges: A[x][y] = A[y][x] = 1
    adj = [set(j for j in range(n) if A[i][j]) for i in range(n)]
    A2 = [[len(adj[i] & adj[j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if A2[i][j] > (1 if A[i][j] else 2): return {"status": "LOCAL", "why": "pair %d %d has %d common neighbours" % (i, j, A2[i][j])}
    if any(len(adj[i]) > 14 for i in range(n)): return {"status": "LOCAL", "why": "degree"}
    Qm = [[(27 if i == j else 0) - 9 * A[i][j] + 1 for j in range(n)] for i in range(n)]
    Qp = [[(44 if i == j else 0) + 11 * A[i][j] - 2 for j in range(n)] for i in range(n)]
    tm, rkm = border_tester(Qm); tp, rkp = border_tester(Qp)
    if tm is None or tp is None: return {"status": "NOT PSD", "why": "Q- " + ("ok" if tm else "negative") + ", Q+ " + ("ok" if tp else "negative")}
    dem = {(u, v): (1 if A[u][v] else 2) - A2[u][v] for u in range(n) for v in range(u + 1, n)}
    masks = []
    # float pre-test of the two bordered blocks; the exact rational test is run only when the float test is not clear-cut
    Pm = np.linalg.pinv(np.array(Qm, dtype=float)); Pp = np.linalg.pinv(np.array(Qp, dtype=float)); Qmf = np.array(Qm, dtype=float); Qpf = np.array(Qp, dtype=float)
    def border_ok(b):
        cm = 1.0 - 9.0 * np.array(b, dtype=float); cp = 11.0 * np.array(b, dtype=float) - 2.0
        wm = Pm @ cm; wp = Pp @ cp
        rm = np.abs(Qmf @ wm - cm).max(); rp = np.abs(Qpf @ wp - cp).max(); vm = cm @ wm; vp = cp @ wp
        if rm > 1e-6 or rp > 1e-6 or vm > 28 + 1e-6 or vp > 42 + 1e-6: 
            if (rm > 1e-3 or vm > 28 + 1e-3) or (rp > 1e-3 or vp > 42 + 1e-3): return False      # clearly violated
        elif vm < 28 - 1e-6 and vp < 42 - 1e-6 and rkm == n and rkp == n: return True            # clearly satisfied, non-singular blocks
        return tm([Fr(1 - 9 * x) for x in b], Fr(28)) and tp([Fr(11 * x - 2) for x in b], Fr(42))
    def rec(start, cur, curset):
        ok = True
        for u in range(n):
            c = len(adj[u] & curset)
            if (u in curset and c > 1) or (u not in curset and c > 2): ok = False; break
        if ok:
            b = [1 if h in curset else 0 for h in range(n)]
            if border_ok(b): masks.append(tuple(cur))
        for h in range(start, n):
            if all(dem[(min(g, h), max(g, h))] > 0 for g in cur) and len(adj[h] & curset) <= 1:
                rec(h + 1, cur + [h], curset | {h})
    rec(0, [], set())
    rows = [[1] * len(masks)]; rhs = [99 - n]; lab = ["total"]
    for h in range(n): rows.append([1 if h in s else 0 for s in masks]); rhs.append(14 - len(adj[h])); lab.append("point %d" % h)
    for (p, q), d in dem.items(): rows.append([1 if (p in s and q in s) else 0 for s in masks]); rhs.append(d); lab.append("pair %d %d" % (p, q))
    R = len(rows); res = {"masks": len(masks), "rank_minus": rkm, "rank_plus": rkp}
    # float LP first (HiGHS); the exact simplex is run only to certify an infeasibility
    from scipy.optimize import linprog
    if not masks and not want_certificate: res["status"] = "INFEASIBLE (no mask at all)"; return res
    if masks:
        fl = linprog(np.zeros(len(masks)), A_eq=np.array(rows, dtype=float), b_eq=np.array(rhs, dtype=float), bounds=[(0, None)] * len(masks), method="highs")
        if fl.status == 0: res["status"] = "feasible (float LP)"; return res
        if not want_certificate: res["status"] = "INFEASIBLE (float LP, status %d)" % fl.status; return res
    cols = [[Fr(rows[r][j]) for r in range(R)] for j in range(len(masks))] + [[Fr(int(r == q)) for r in range(R)] for q in range(R)]
    out = simplex(cols, [Fr(0)] * len(masks) + [Fr(-1)] * R, [Fr(x) for x in rhs])
    assert out[0] == "optimal"
    if out[1] < 0:
        y = out[3]
        assert all(sum(y[r] * rows[r][j] for r in range(R)) >= 0 for j in range(len(masks))) and sum(y[r] * rhs[r] for r in range(R)) < 0
        res["status"] = "INFEASIBLE"
        if want_certificate: res["certificate"] = {"rows": lab, "rhs": rhs, "y": [str(v) for v in y], "masks": [list(s) for s in masks]}
    else:
        res["status"] = "feasible"
    return res


def window(w):
    """roles of an open ribbon with w centres: names and forced edges"""
    names = ["a%d" % i for i in range(1, w + 2)] + ["b%d" % i for i in range(1, w + 2)] + ["c%d" % i for i in range(1, w + 1)]
    ix = {s: i for i, s in enumerate(names)}; E = []
    for i in range(1, w + 1):
        for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, "a%d" % (i + 1)), ("a%d" % i, "a%d" % (i + 1)), ("c%d" % i, "b%d" % i), ("c%d" % i, "b%d" % (i + 1)), ("b%d" % i, "b%d" % (i + 1))):
            E.append((ix[x], ix[y]))
    return names, ix, E


if __name__ == "__main__" and sys.argv[1] == "window5":
    w = 5; names, ix, E0 = window(w); n = len(names); t0 = time.time()
    def sym(s, swap, rev):
        t, i = s[0], int(s[1:])
        if swap and t in "ab": t = "b" if t == "a" else "a"
        if rev: i = (w + 2 - i) if t in "ab" else (w + 1 - i)
        return "%s%d" % (t, i)
    def canon(x, y):
        return min(tuple(sorted((sym(x, s_, r_), sym(y, s_, r_)))) for s_ in (0, 1) for r_ in (0, 1))
    base = set(tuple(sorted(e_)) for e_ in E0)
    print("clean window:", verdict(n, E0)["status"], flush=True)
    PART = sys.argv[2] if len(sys.argv) > 2 else "all"
    seen = set(); tally = collections.Counter()
    print("--- one extra edge", flush=True)
    for x, y in (itertools.combinations(names, 2) if PART in ("all", "edges") else []):
        if tuple(sorted((ix[x], ix[y]))) in base: continue
        k_ = canon(x, y)
        if k_ in seen: continue
        seen.add(k_); r = verdict(n, E0 + [(ix[x], ix[y])]); tally[("edge", r["status"])] += 1
        if r["status"] not in ("NOT PSD", "LOCAL"): print("   %s - %s : %s (masks %d, ranks %d %d)  [%.0f s]" % (x, y, r["status"], r["masks"], r["rank_minus"], r["rank_plus"], time.time() - t0), flush=True)
    seen = set()
    print("--- one identification of two roles", flush=True)
    for x, y in (itertools.combinations(names, 2) if PART in ("all", "ident") else []):
        if tuple(sorted((ix[x], ix[y]))) in base: continue
        k_ = canon(x, y)
        if k_ in seen: continue
        seen.add(k_)
        keep = [s for s in names if s != y]; jx = {s: i for i, s in enumerate(keep)}; jx[y] = jx[x]
        E = set()
        for p, q in E0:
            u, v = jx[names[p]], jx[names[q]]
            if u == v: E = None; break
            E.add((min(u, v), max(u, v)))
        if E is None: tally[("ident", "LOCAL")] += 1; continue
        r = verdict(len(keep), sorted(E)); tally[("ident", r["status"])] += 1
        if r["status"] not in ("NOT PSD", "LOCAL"): print("   %s = %s : %s (masks %d, ranks %d %d)  [%.0f s]" % (x, y, r["status"], r["masks"], r["rank_minus"], r["rank_plus"], time.time() - t0), flush=True)
    print("summary (kind, verdict) -> number of classes:", dict(sorted(tally.items())))
