"""Stage 2' of the c <= 3 root cover (LAB, 18/10/2026): integer Gram + corner realizations + root prism budget.

At a root of minimal prism load (tau(v) = sum over its 7 lines of t(l) <= 51, which exists in every Conway graph because
P <= 852, Codex's certificate), a template survives only if some integer Gram R passes cle3_gram's system AND every
root rectangle has a corner realization (Codex's root_rectangle_domains: four integral signatures h in im R with
h^T R^+ h <= 5/2, summing to the column of R, binary corner graph with the right degrees, conditional 4x4 Gram PSD),
with the sum of the per-rectangle minimal prism edges <= 51.  A Gram without realization is cut (no-good on its anchor
values) and the search continues.  Codex's functions are copied here WITHOUT their rank <= 4 assert: the signature
bound h in im R, h^T R^+ h <= 5/2 holds in any rank (T P R^+ P^T T <= T and T_ww = 5/2); only the enumeration grows
like 5^rank.
usage: python cle3_corner.py <json with open templates> <seconds per template> <output> [start end]"""
import json
import sys
import time
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-asymmetry-audit\code\codex")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_ambient_upper import psd_or_witness  # noqa: E402
import cle3_gram as GR  # noqa: E402

EDGES = tuple(combinations(range(7), 2))
RECTANGLE_LABELS = ((0, 2), (0, 3), (1, 2), (1, 3))
BUDGET = 51


def corner_graphs(edge_count):                      # Codex, verbatim
    pairs = [(i, j) for i, j in combinations_with_replacement(range(4), 2) if i != j]
    result = []
    for mask in range(1 << 6):
        if bin(mask).count("1") != edge_count:
            continue
        adjacency = [[0] * 4 for _ in range(4)]
        for k, (i, j) in enumerate(pairs):
            adjacency[i][j] = adjacency[j][i] = int(bool(mask & (1 << k)))
        if any(sum(adjacency[i][j] for j in range(4) if a in RECTANGLE_LABELS[j]) > 1
               for i in range(4) for a in range(4)):
            continue
        t4 = [[10 if i == j else -4 * adjacency[i][j] - int(bool(set(RECTANGLE_LABELS[i]) & set(RECTANGLE_LABELS[j])))
               for j in range(4)] for i in range(4)]
        result.append((adjacency, t4, [2 - sum(row) for row in adjacency]))
    return result


def bounds(rectangle, coordinate):                  # Codex, verbatim
    if rectangle == coordinate:
        return 0, 2
    return (-2, 0) if set(rectangle).intersection(coordinate) else (-3, 1)


def signature_domains(edges, raw):                  # Codex, without the rank <= 4 assert
    matrix = sp.Matrix(raw)
    m = len(edges)
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    denominator = int(small.det())
    assert denominator > 0
    inverse_scaled = (small.inv(method="DM") * denominator).applyfunc(int)
    lift = matrix[:, anchors] * inverse_scaled
    inverse_scaled = [[int(x) for x in row] for row in inverse_scaled.tolist()]
    lift = [[int(x) for x in row] for row in lift.tolist()]
    results = []
    for rectangle in EDGES:
        intervals = [bounds(rectangle, edge) for edge in edges]
        domains = []
        for coordinates in product(*(range(intervals[i][0], intervals[i][1] + 1) for i in anchors)):
            norm = sum(coordinates[i] * inverse_scaled[i][j] * coordinates[j]
                       for i in range(len(anchors)) for j in range(len(anchors)))
            if 2 * norm > 5 * denominator:
                continue
            numerator = [sum(a * b for a, b in zip(row, coordinates)) for row in lift]
            if any(x % denominator for x in numerator):
                continue
            h = tuple(x // denominator for x in numerator)
            if all(lo <= x <= hi for x, (lo, hi) in zip(h, intervals)):
                domains.append(h)
        target = tuple(int(matrix[i, edges.index(rectangle)]) for i in range(m)) if rectangle in edges else (0,) * m
        results.append({"rectangle": rectangle, "signatures": domains, "target": target})
    return results


def rectangle_realizations(edges, raw, budget=BUDGET):     # Codex's logic, with the prism budget
    domains = signature_domains(edges, raw)
    matrix = sp.Matrix(raw)
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    denominator = int(small.det())
    adjugate = (small.inv(method="DM") * denominator).applyfunc(int)
    minimum_total = 0
    for item in domains:
        rectangle = tuple(item["rectangle"])
        signatures = [tuple(v) for v in item["signatures"]]
        coordinate = edges.index(rectangle) if rectangle in edges else None
        energy = int(matrix[coordinate, coordinate]) if coordinate is not None else 0
        patterns = corner_graphs(4 - energy // 2)

        def prism_count(pattern):
            adjacency = pattern[0]
            return sum(adjacency[i][j] for i in range(4) for j in range(i + 1, 4)
                       if set(RECTANGLE_LABELS[i]) & set(RECTANGLE_LABELS[j]))
        patterns.sort(key=prism_count)
        vectors = [sp.Matrix([h[i] for i in anchors]) for h in signatures]
        gram = [[int((a.T * adjugate * b)[0]) for b in vectors] for a in vectors]
        target = tuple(item["target"])
        found = None
        for adjacency, t4, degrees in patterns:
            choices = [[i for i, h in enumerate(signatures) if coordinate is None or h[coordinate] == value]
                       for value in degrees]
            pair_sums = {}
            for i, j in product(choices[2], choices[3]):
                pair_sums.setdefault(tuple(a + b for a, b in zip(signatures[i], signatures[j])), []).append((i, j))
            for i, j in product(choices[0], choices[1]):
                needed = tuple(t - a - b for t, a, b in zip(target, signatures[i], signatures[j]))
                for k, l in pair_sums.get(needed, []):
                    idx = (i, j, k, l)
                    residual = sp.Matrix(4, 4, lambda a, b: denominator * t4[int(a)][int(b)] - 4 * gram[idx[int(a)]][idx[int(b)]])
                    if psd_or_witness(residual)["psd"]:
                        found = prism_count((adjacency, t4, degrees))
                        break
                if found is not None:
                    break
            if found is not None:
                break
        if found is None:
            return {"feasible": False, "failed_rectangle": rectangle}
        minimum_total += found
        if minimum_total > budget:
            return {"feasible": False, "failed_rectangle": "root_prism_budget", "partial_sum": minimum_total}
    return {"feasible": True, "minimum_root_prism_sum": minimum_total}


def solve(t, seconds):
    """cle3_gram's model, then a lazy loop: PSD cuts, then corner realizations with no-good cuts on failure."""
    edges, nodes, links = GR.template_graph(t)
    m = len(edges)
    incidence = sp.zeros(len(nodes), m)
    for i, (a, b) in enumerate(links):
        incidence[a, i] = incidence[b, i] = 1
    kernel = sp.Matrix.hstack(*incidence.nullspace())
    anchors = list(kernel.T.rref()[1])
    model, R = GR.build_model(edges, nodes, links, anchors) if hasattr(GR, "build_model") else (None, None)
    if model is None:
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
                        if inc[0] in U:
                            rest = [f for f in inc if f not in U]
                            model.add(sum(R[e][f] for e in U for f in rest) <= -2)
        model.add(sum(R[i][i] for i in range(m)) <= 28 * len(anchors))
        model.add(4 * (21 - m) <= BUDGET)                    # grids at the root cost 4 prisms each
        allowed = [(a, b, c) for a in (4, 6, 8) for b in (4, 6, 8) for c in range(-8, 5) if c * c <= a * b]
        for i, j in combinations(range(m), 2):
            model.add_allowed_assignments([R[i][i], R[j][j], R[i][j]], allowed)
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
            return {"status": "INFEASIBLE", "stats": dict(stats)}
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"status": "UNKNOWN", "stats": dict(stats)}
        cand = sp.Matrix([[solver.value(v) for v in row] for row in R])
        low = psd_or_witness(cand.extract(anchors, anchors))
        up = psd_or_witness(28 * sp.eye(m) - cand) if low["psd"] else None
        if low["psd"] and up["psd"]:
            real = rectangle_realizations(list(edges), cand.tolist())
            if real["feasible"]:
                return {"status": "CORNERS_FEASIBLE", "R": cand.tolist(), "R_rank": len(cand.rref()[1]),
                        "minimum_root_prism_sum": real["minimum_root_prism_sum"], "stats": dict(stats)}
            stats["no_good_" + ("budget" if real["failed_rectangle"] == "root_prism_budget" else "corners")] += 1
            pairs = [(i, j) for i in anchors for j in anchors if i <= j]
            model.add_forbidden_assignments([R[i][j] for i, j in pairs], [[int(cand[i, j]) for i, j in pairs]])
            continue
        if not low["psd"]:
            vec = [0] * m
            for i, x in zip(anchors, low["integer_witness"]):
                vec[i] = x
            model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j]) >= 0)
            stats["psd_cut"] += 1
        else:
            vec = up["integer_witness"]
            model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j])
                      <= 28 * sum(x * x for x in vec))
            stats["upper_cut"] += 1


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    temps = data["templates"]
    secs = float(sys.argv[2])
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    end = int(sys.argv[5]) if len(sys.argv) > 5 else len(temps)
    counts, recs, t0 = Counter(), [], time.time()
    for k in range(start, end):
        r = solve(temps[k], secs)
        counts[r["status"]] += 1
        recs.append({"index": k, "kernel_dimension": temps[k]["kernel_dimension"], **r})
    json.dump({"source": sys.argv[1], "range": [start, end], "counts": dict(counts), "records": recs},
              open(sys.argv[3], "w"), default=int)
    print(json.dumps({"range": [start, end], "counts": dict(counts), "seconds": round(time.time() - t0, 1)}))
