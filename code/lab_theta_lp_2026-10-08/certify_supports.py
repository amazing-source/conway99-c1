"""C1, lab session, 2026-10-09. Exact certificates for the infeasible cases of the surveys of support_masks.py.
For a support H: masks as in support_masks.verdict (exact spectral filters), then
  1. float phase-1 LP (HiGHS) gives a dual vector y; the rows with |y| > 1e-9 form a sub-system of the equalities;
  2. the exact rational simplex is run on that sub-system only; a negative optimum with its dual vector, checked
     exactly against EVERY mask column, proves that the full system has no non-negative rational solution.
  python certify_supports.py window5 | closed6        One process, below 1 GB; a few minutes."""
import sys, time, json, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
import support_masks as S


def system(n, edges):
    """the mask columns and the equalities of support_masks.verdict, rebuilt here (same filters)"""
    A = [[0] * n for _ in range(n)]
    for x, y in edges: A[x][y] = A[y][x] = 1
    adj = [set(j for j in range(n) if A[i][j]) for i in range(n)]
    A2 = [[len(adj[i] & adj[j]) for j in range(n)] for i in range(n)]
    Qm = [[(27 if i == j else 0) - 9 * A[i][j] + 1 for j in range(n)] for i in range(n)]
    Qp = [[(44 if i == j else 0) + 11 * A[i][j] - 2 for j in range(n)] for i in range(n)]
    tm, rkm = S.border_tester(Qm); tp, rkp = S.border_tester(Qp); assert tm and tp
    dem = {(u, v): (1 if A[u][v] else 2) - A2[u][v] for u in range(n) for v in range(u + 1, n)}
    masks = []
    def rec(start, cur, curset):
        ok = all((len(adj[u] & curset) <= 1) if u in curset else (len(adj[u] & curset) <= 2) for u in range(n))
        if ok:
            b = [1 if h in curset else 0 for h in range(n)]
            if tm([Fr(1 - 9 * x) for x in b], Fr(28)) and tp([Fr(11 * x - 2) for x in b], Fr(42)): masks.append(tuple(cur))
        for h in range(start, n):
            if all(dem[(min(g, h), max(g, h))] > 0 for g in cur) and len(adj[h] & curset) <= 1: rec(h + 1, cur + [h], curset | {h})
    rec(0, [], set())
    rows = [[1] * len(masks)]; rhs = [99 - n]; lab = ["total"]
    for h in range(n): rows.append([1 if h in s else 0 for s in masks]); rhs.append(14 - len(adj[h])); lab.append("point %d" % h)
    for (p, q), d in dem.items(): rows.append([1 if (p in s and q in s) else 0 for s in masks]); rhs.append(d); lab.append("pair %d %d" % (p, q))
    return masks, rows, rhs, lab


def certify(n, edges):
    masks, rows, rhs, lab = system(n, edges); R = len(rows); M = len(masks)
    if M == 0: return "INFEASIBLE exactly (no admissible mask, total = %d required)" % rhs[0], None
    Aeq = np.hstack([np.array(rows, dtype=float), np.eye(R)]); c = np.concatenate([np.zeros(M), np.ones(R)])
    fl = linprog(c, A_eq=Aeq, b_eq=np.array(rhs, dtype=float), bounds=[(0, None)] * (M + R), method="highs")
    assert fl.status == 0
    if fl.fun < 1e-7: return "feasible (float phase 1)", None
    y = fl.eqlin.marginals; keep = [r for r in range(R) if abs(y[r]) > 1e-9]
    cols = [[Fr(rows[r][j]) for r in keep] for j in range(M)] + [[Fr(int(a == b)) for a in range(len(keep))] for b in range(len(keep))]
    out = S.simplex(cols, [Fr(0)] * M + [Fr(-1)] * len(keep), [Fr(rhs[r]) for r in keep])
    assert out[0] == "optimal"
    if out[1] >= 0: return "sub-system feasible exactly (%d rows): no certificate from this reduction" % len(keep), None
    yy = out[3]
    assert all(sum(yy[a] * rows[r][j] for a, r in enumerate(keep)) >= 0 for j in range(M)) and sum(yy[a] * rhs[r] for a, r in enumerate(keep)) < 0
    cert = {"rows": [lab[r] for r in keep], "rhs": [rhs[r] for r in keep], "y": [str(v) for v in yy], "masks": [list(s) for s in masks], "edges": [list(e) for e in edges], "n": n}
    return "INFEASIBLE exactly (Farkas vector on %d rows checked against %d masks)" % (len(keep), M), cert


if __name__ == "__main__":
    what = sys.argv[1]; t0 = time.time(); out = {}
    if what == "window5":
        names, ix, E0 = S.window(5); n = len(names)
        for x, y in (("a2", "a5"), ("a2", "b5"), ("a2", "c4"), ("a2", "c5"), ("c1", "c4"), ("c2", "c4")):
            st, cert = certify(n, E0 + [(ix[x], ix[y])]); out["%s-%s" % (x, y)] = {"status": st, "certificate": cert}
            print("window5 + edge %s-%s : %s  [%.0f s]" % (x, y, st, time.time() - t0), flush=True)
        keep = [s for s in names if s != "c4"]; jx = {s: i for i, s in enumerate(keep)}; jx["c4"] = jx["c1"]
        E = sorted({tuple(sorted((jx[names[p]], jx[names[q]]))) for p, q in E0})
        st, cert = certify(len(keep), E); out["c1=c4"] = {"status": st, "certificate": cert}
        print("window5 + identification c1 = c4 : %s  [%.0f s]" % (st, time.time() - t0), flush=True)
    else:
        for MO in (False, True):
            m = 6; names = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; ix = {s: i for i, s in enumerate(names)}; E0 = []
            for i in range(m):
                if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
                else: an, bn = "b0", "a0"
                for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E0.append((ix[x], ix[y]))
            tag = "moebius" if MO else "cylinder"
            for x, y in ((("a0", "a3"), ("c0", "c3")) if MO else (("a0", "a3"), ("a0", "b3"), ("c0", "c3"))):
                st, cert = certify(len(names), E0 + [(ix[x], ix[y])]); out["%s %s-%s" % (tag, x, y)] = {"status": st, "certificate": cert}
                print("closed6 %s + edge %s-%s : %s  [%.0f s]" % (tag, x, y, st, time.time() - t0), flush=True)
            for x, y in ((("c0", "c3"),) if MO else (("a0", "b3"), ("c0", "c3"))):
                keep = [s for s in names if s != y]; jx = {s: i for i, s in enumerate(keep)}; jx[y] = jx[x]
                E = sorted({tuple(sorted((jx[names[p]], jx[names[q]]))) for p, q in E0})
                st, cert = certify(len(keep), E); out["%s %s=%s" % (tag, x, y)] = {"status": st, "certificate": cert}
                print("closed6 %s + identification %s = %s : %s  [%.0f s]" % (tag, x, y, st, time.time() - t0), flush=True)
    json.dump(out, open("certificates_%s.json" % what, "w"))
