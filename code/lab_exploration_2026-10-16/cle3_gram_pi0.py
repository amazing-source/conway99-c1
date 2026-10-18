"""Integer Gram test of cle3_gram.py plus ONE extra necessary condition (LAB, 18/10/2026): R <= 28 Pi0 on the non-grid
rectangles, instead of only R <= 28 I.

Proof.  R = P^t T P over the 21 rectangles, with T <= 7 Pi (Pi = projection on ker B, proved in the audit, step 3), so
R <= 7 P^t Pi P = 28 Pi0, where Pi0 = I - C0^t C0 / 5 + J / 15 is the orthogonal projection on ker C0 (C0 = incidence
of K7, rank-14 projection, checked exactly).  A principal submatrix keeps the order, so R_NN <= 28 (Pi0)_NN on the set
N of non-grid rectangles, which is exactly the matrix of the model.  Since (Pi0)_NN <= I, this is at least as strong
as R <= 28 I.  Exact lazy cuts: 15 (28 Pi0_NN - R) = 420 I - 84 (C0^t C0)_NN + 28 J - 15 R must be PSD; an integer
witness v of a negative value gives the linear cut  15 v^t R v <= v^t (420 I - 84 C0^t C0 + 28 J) v.
Everything else is cle3_gram.solve, unchanged (same domains, C R = 0, cuts, trace, minors, PSD cuts).
usage: python cle3_gram_pi0.py <seconds per template> <output.json> <templates .jsonl or .json.gz catalogue>"""
import gzip
import json
import sys
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cle3_gram as GR                                   # noqa: E402
from three_star_ambient_upper import psd_or_witness      # noqa: E402


def solve(t, seconds):
    edges, nodes, links = GR.template_graph(t)
    m = len(edges)
    incidence = sp.zeros(len(nodes), m)
    for i, (a, b) in enumerate(links):
        incidence[a, i] = incidence[b, i] = 1
    kernel = sp.Matrix.hstack(*incidence.nullspace())
    anchors = list(kernel.T.rref()[1])
    model = cp_model.CpModel()
    R = [[None] * m for _ in range(m)]
    for i in range(m):
        R[i][i] = model.new_int_var_from_domain(cp_model.Domain.from_values([4, 6, 8]), "r%d_%d" % (i, i))
        for j in range(i):
            common = set(edges[i]) & set(edges[j])
            R[i][j] = R[j][i] = model.new_int_var(-8, 0 if common else 4, "r%d_%d" % (j, i))
            if common:
                root = next(iter(common))
                same = any(r == root and all((set(e) - {root}) <= set(part) for e in (edges[i], edges[j]))
                           for r, part in nodes)
                if not same:
                    model.add(R[i][j] == 0)
    for node in range(len(nodes)):
        inc = [i for i, ends in enumerate(links) if node in ends]
        for j in range(m):
            model.add(sum(R[i][j] for i in inc) == 0)
        if len(inc) >= 3:
            for size in range(1, len(inc)):
                for U in combinations(inc, size):
                    if inc[0] not in U:
                        continue
                    rest = [f for f in inc if f not in U]
                    model.add(sum(R[e][f] for e in U for f in rest) <= -2)
    model.add(sum(R[i][i] for i in range(m)) <= 28 * len(anchors))
    allowed = [(a, b, c) for a in (4, 6, 8) for b in (4, 6, 8) for c in range(-8, 5) if c * c <= a * b]
    for i, j in combinations(range(m), 2):
        model.add_allowed_assignments([R[i][i], R[j][j], R[i][j]], allowed)
    # 15 * 28 * (Pi0)_NN as an integer matrix
    pi0 = sp.Matrix(m, m, lambda i, j: 420 * (i == j) - 84 * len(set(edges[int(i)]) & set(edges[int(j)])) + 28)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    stats, t0 = Counter(), time.monotonic()
    while True:
        rem = seconds - (time.monotonic() - t0)
        if rem <= 0:
            return {"status": "UNKNOWN", "stats": dict(stats)}
        solver.parameters.max_time_in_seconds = rem
        st = solver.solve(model)
        if st == cp_model.INFEASIBLE:
            return {"status": "QUOTIENT_INFEASIBLE", "stats": dict(stats)}
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"status": "UNKNOWN", "stats": dict(stats)}
        cand = sp.Matrix([[solver.value(v) for v in row] for row in R])
        low = psd_or_witness(cand.extract(anchors, anchors))
        if not low["psd"]:
            vec = [0] * m
            for i, x in zip(anchors, low["integer_witness"]):
                vec[i] = x
            model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j]) >= 0)
            stats["psd_cut"] += 1
            continue
        up = psd_or_witness(pi0 - 15 * cand)
        if not up["psd"]:
            vec = up["integer_witness"]
            rhs = sum(vec[i] * vec[j] * int(pi0[i, j]) for i in range(m) for j in range(m))
            model.add(15 * sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j]) <= rhs)
            stats["pi0_cut"] += 1
            continue
        return {"status": "QUOTIENT_FEASIBLE", "R": cand.tolist(), "stats": dict(stats)}


if __name__ == "__main__":
    secs, out, src = float(sys.argv[1]), sys.argv[2], sys.argv[3]
    if src.endswith(".jsonl"):
        temps = [json.loads(l) for l in open(src)]
    else:
        data = json.load(gzip.open(src, "rt") if src.endswith(".gz") else open(src))
        temps = ([y["template"] for y in data["open"]] if "open" in data else
                 data["templates"] if "templates" in data else data["survivors"])
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    end = int(sys.argv[5]) if len(sys.argv) > 5 else len(temps)
    counts, recs, t0 = Counter(), [], time.time()
    for k in range(start, end):
        r = solve(temps[k], secs) if temps[k]["nongrid_edges"] else {"status": "QUOTIENT_FEASIBLE"}
        counts[r["status"]] += 1
        recs.append({"index": k, **{x: r[x] for x in r if x != "R"}})
    json.dump({"source": src, "range": [start, end], "counts": dict(counts), "records": recs}, open(out, "w"), default=int)
    print(json.dumps({"range": [start, end], "counts": dict(counts), "seconds": round(time.time() - t0, 1)}))
