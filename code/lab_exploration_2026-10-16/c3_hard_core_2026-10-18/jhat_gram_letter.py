"""Per-Gram filter with letters (LAB, 18/10/2026).  Measurement tool: LP feasibility (GLOP), no certificate yet.

For a template and one Gram R of its complete cover (R on the m non-grid rectangles):
  rows: the DFS catalogue rows (jhat_catalogue.py) whose vector h (on the non-grid rectangles) satisfies the Schur
        condition of a vertex (h in im R, h^T R^+ h <= 5/2; exact rationals) -- AUDIT item on [[T_ww, h^T], [h, R]] >= 0;
  base design at fixed R (multiplicities n_{F,s} >= 0): four rows per class; sum_{u in F} h_u(G) = R_FG for every class
        F and non-grid G (grid classes: = 0); sum_w h_w(i) h_w(j) = 7 R_ij;
  letters: per (class, row, root a off the class) the delta^a vectors (jhat_letter_lp.py), linked to n, and the
        identities N1, N3, N3s, N4 of jhat_letter_lp.py (checked on srg(243,22,1,2), letter_identities_control).
Status: INFEASIBLE_BASE (the fixed-R design alone has no fractional solution), INFEASIBLE_LETTERS (only with letters),
FEASIBLE.  usage: python jhat_gram_letter.py <catalogue> <index> <cover.json(.gz)> <gram indices i,j,...>"""
import gzip
import json
import sys
import time
from fractions import Fraction
from itertools import combinations

import sympy as sp
from ortools.linear_solver import pywraplp

from jhat_catalogue import catalogue
from jhat_rows import RECT, records

RI = {q: i for i, q in enumerate(RECT)}
from itertools import product


def rq(a, j):
    return RECT.index((a, j) if a < j else (j, a))


def delta_vectors(z, a):
    """All delta^a for a z-row of a label off line a (same as jhat_letter_lp.delta_vectors)."""
    js = [j for j in range(7) if j != a]
    zs = [z[rq(a, j)] for j in js]
    assert sum(zs) == 4
    return [dict(zip(js, d)) for d in product(*[range(-v, v + 1, 2) for v in zs]) if sum(d) == 0]


def base(q, f):
    return 2 if f == q else (0 if set(f) & set(q) else 1)


def schur_ok(h, R, Rp, proj):
    v = sp.Matrix(h)
    if proj * v != v:                     # h in im R
        return False
    return (v.T * Rp * v)[0, 0] <= Fraction(5, 2)


def run(t, cat, edges, Rraw, letters=True, seconds=120):
    m = len(edges)
    R = sp.Matrix(Rraw)
    Rp = R.pinv()
    proj = R * Rp
    eidx = {tuple(e): i for i, e in enumerate(edges)}
    cols = []                              # (class index, z-row, h on edges)
    for qi, item in enumerate(cat["row_types"]):
        q = RECT[qi]
        for z in item["states"]:
            h = [base(q, RECT[f]) - z[f] for f in range(21)]
            he = [h[RI[tuple(e)]] for e in edges]
            if schur_ok(he, R, Rp, proj):
                cols.append((qi, z, he))
    per_class = [sum(1 for c in cols if c[0] == qi) for qi in range(21)]
    if min(per_class) == 0:
        return "INFEASIBLE_BASE", {"empty_class": RECT[per_class.index(0)], "rows": len(cols)}
    lp = pywraplp.Solver.CreateSolver("GLOP")
    lp.SetTimeLimit(int(seconds * 1000))
    x = [lp.NumVar(0, 4, "n%d" % i) for i in range(len(cols))]
    for qi in range(21):
        lp.Add(sum(x[i] for i, c in enumerate(cols) if c[0] == qi) == 4)
    for qi in range(21):
        F = RECT[qi]
        for gi, G in enumerate(edges):
            target = int(R[eidx[F], gi]) if F in eidx else 0
            lp.Add(sum(x[i] * c[2][gi] for i, c in enumerate(cols) if c[0] == qi) == target)
    for i_, j_ in combinations(range(m), 2):
        lp.Add(sum(x[i] * c[2][i_] * c[2][j_] for i, c in enumerate(cols)) == 7 * int(R[i_, j_]))
    for i_ in range(m):
        lp.Add(sum(x[i] * c[2][i_] ** 2 for i, c in enumerate(cols)) == 7 * int(R[i_, i_]))
    st = lp.Solve()
    if st == pywraplp.Solver.INFEASIBLE:
        return "INFEASIBLE_BASE", {"rows": len(cols)}
    if not letters:
        return ("FEASIBLE" if st in (0, 1) else "UNKNOWN_%d" % st), {"rows": len(cols)}
    # letters
    comps = {}
    for a in range(7):
        parts = [tuple(p) for p in t["nontrivial_component_groups"][a]]
        used = {j for p in parts for j in p}
        parts += [(j,) for j in range(7) if j != a and j not in used]
        comps[a] = parts
    ext = []
    for ci, (qi, z, he) in enumerate(cols):
        q = RECT[qi]
        ys = {}
        for a in range(7):
            if a in q:
                continue
            ds = delta_vectors(z, a)
            ys[a] = [lp.NumVar(0, 4, "m%d_%d_%d" % (ci, a, k)) for k in range(len(ds))]
            lp.Add(sum(ys[a]) == x[ci])
            for k, d in enumerate(ds):
                ext.append((ci, a, d, ys[a][k]))
    for a in range(7):
        ea = [(ci, d, y) for (ci, aa, d, y) in ext if aa == a]
        for P in comps[a]:
            p = len(P)
            dK = [(ci, sum(d[j] for j in P), d, y) for ci, d, y in ea]
            for G in RECT:
                if a in G:
                    continue
                gi = RI[G]
                lp.Add(sum(y * (dk * cols[ci][1][gi] + (dk if cols[ci][0] == gi else 0)) for ci, dk, d, y in dK) == 0)
            for j in range(7):
                if j == a:
                    continue
                lp.Add(sum(y * dk * cols[ci][1][rq(a, j)] for ci, dk, d, y in dK) == 0)
                lp.Add(sum(y * dk * d[j] for ci, dk, d, y in dK) == (8 * (6 - p) if j in P else -8 * p))
                lp.Add(sum(y * dk for ci, dk, d, y in dK if j in RECT[cols[ci][0]]) == 0)
    st2 = lp.Solve()
    if st2 == pywraplp.Solver.INFEASIBLE:
        return "INFEASIBLE_LETTERS", {"rows": len(cols), "ext": len(ext)}
    return ("FEASIBLE" if st2 in (0, 1) else "UNKNOWN_%d" % st2), {"rows": len(cols), "ext": len(ext)}


if __name__ == "__main__":
    path, idx, cover = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    which = [int(v) for v in sys.argv[4].split(",")]
    t = next(r for i, r in enumerate(records(path)) if i == idx)
    cat = catalogue(t)
    cv = json.load(gzip.open(cover, "rt") if cover.endswith(".gz") else open(cover))
    edges = [tuple(e) for e in cv["edges"]]
    assert sorted(edges) == sorted(tuple(e) for e in t["nongrid_edges"])
    for gi in which:
        t0 = time.time()
        st, info = run(t, cat, edges, cv["grams"][gi])
        print(json.dumps({"gram": gi, "status": st, **{k: (list(v) if isinstance(v, tuple) else v) for k, v in info.items()},
                          "seconds": round(time.time() - t0, 1)}), flush=True)
