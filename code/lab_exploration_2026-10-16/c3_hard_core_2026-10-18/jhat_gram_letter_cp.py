"""Integer version of jhat_gram_letter.py (LAB, 18/10/2026): the same fixed-R design, with integer multiplicities, and
optionally the letter columns (integer).  CP-SAT verdicts (measurement).  Bounds are constants (no domain reads).
usage: python jhat_gram_letter_cp.py <catalogue> <index> <cover> <gram indices> <seconds> [--no-letters]"""
import gzip
import json
import sys
import time
from itertools import combinations

import sympy as sp
from ortools.sat.python import cp_model

from jhat_catalogue import catalogue
from jhat_gram_letter import RECT, RI, base, schur_ok, rq, delta_vectors
from jhat_rows import records


def run(t, cat, edges, Rraw, letters, seconds):
    m = len(edges)
    R = sp.Matrix(Rraw)
    Rp = R.pinv()
    proj = R * Rp
    eidx = {tuple(e): i for i, e in enumerate(edges)}
    cols = []
    for qi, item in enumerate(cat["row_types"]):
        q = RECT[qi]
        for z in item["states"]:
            h = [base(q, RECT[f]) - z[f] for f in range(21)]
            he = [h[RI[tuple(e)]] for e in edges]
            if schur_ok(he, R, Rp, proj):
                cols.append((qi, z, he))
    if min(sum(1 for c in cols if c[0] == qi) for qi in range(21)) == 0:
        return "INFEASIBLE_EMPTY_CLASS", 0.0
    md = cp_model.CpModel()
    x = [md.NewIntVar(0, 4, "n%d" % i) for i in range(len(cols))]
    for qi in range(21):
        md.Add(sum(x[i] for i, c in enumerate(cols) if c[0] == qi) == 4)
        F = RECT[qi]
        own = [i for i, c in enumerate(cols) if c[0] == qi]
        for gi in range(m):
            target = int(R[eidx[F], gi]) if F in eidx else 0
            md.Add(sum(x[i] * cols[i][2][gi] for i in own) == target)
    for i_ in range(m):
        for j_ in range(i_, m):
            md.Add(sum(x[i] * c[2][i_] * c[2][j_] for i, c in enumerate(cols)) == 7 * int(R[i_, j_]))
    if letters:
        comps = {}
        for a in range(7):
            parts = [tuple(p) for p in t["nontrivial_component_groups"][a]]
            used = {j for p in parts for j in p}
            parts += [(j,) for j in range(7) if j != a and j not in used]
            comps[a] = parts
        ext = []
        for ci, (qi, z, he) in enumerate(cols):
            for a in range(7):
                if a in RECT[qi]:
                    continue
                ds = delta_vectors(z, a)
                ys = [md.NewIntVar(0, 4, "m%d_%d_%d" % (ci, a, k)) for k in range(len(ds))]
                md.Add(sum(ys) == x[ci])
                ext += [(ci, a, d, y) for d, y in zip(ds, ys)]
        for a in range(7):
            ea = [(ci, d, y) for (ci, aa, d, y) in ext if aa == a]
            for P in comps[a]:
                p = len(P)
                dK = [(ci, sum(d[j] for j in P), d, y) for ci, d, y in ea]
                for G in RECT:
                    if a in G:
                        continue
                    gi = RI[G]
                    terms = [(y, dk * cols[ci][1][gi] + (dk if cols[ci][0] == gi else 0)) for ci, dk, d, y in dK]
                    md.Add(sum(c * y for y, c in terms if c) == 0)
                for j in range(7):
                    if j == a:
                        continue
                    md.Add(sum(dk * cols[ci][1][rq(a, j)] * y for ci, dk, d, y in dK if dk * cols[ci][1][rq(a, j)]) == 0)
                    md.Add(sum(dk * d[j] * y for ci, dk, d, y in dK if dk * d[j]) == (8 * (6 - p) if j in P else -8 * p))
                    md.Add(sum(dk * y for ci, dk, d, y in dK if dk and j in RECT[cols[ci][0]]) == 0)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1
    r = s.Solve(md)
    return {cp_model.INFEASIBLE: "INFEASIBLE", cp_model.OPTIMAL: "FEASIBLE", cp_model.FEASIBLE: "FEASIBLE"}.get(r, "UNKNOWN"), s.WallTime()


if __name__ == "__main__":
    path, idx, cover = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    which = [int(v) for v in sys.argv[4].split(",")]
    seconds = float(sys.argv[5])
    letters = "--no-letters" not in sys.argv
    t = next(r for i, r in enumerate(records(path)) if i == idx)
    cat = catalogue(t)
    cv = json.load(gzip.open(cover, "rt") if cover.endswith(".gz") else open(cover))
    edges = [tuple(e) for e in cv["edges"]]
    for gi in which:
        st, wall = run(t, cat, edges, cv["grams"][gi], letters, seconds)
        print(json.dumps({"gram": gi, "letters": letters, "status": st, "wall": round(wall, 1)}), flush=True)
