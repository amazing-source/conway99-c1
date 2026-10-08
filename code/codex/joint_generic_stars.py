"""Joint integer/mod-7 model for two generic stars (note209).

Default input is the already-excluded cyclic (2,4,1) calibration ball.
By default only ONE common-apex branch is tested. A partial run is never
reported as an exclusion of the ball. --max-apex 0 requests all branches.
The script accepts --ball JSON with a 36x36 `adjacency` matrix.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

import numpy as np
import ortools
from ortools.sat.python import cp_model

from generic_star_apex_audit import cyclic_ball, inverse7
from grid_kernel_rank_obstruction import rank_pivots


def prepare(g, u, v):
    g = np.asarray(g, dtype=np.int64)
    assert g.shape == (36, 36) and np.array_equal(g, g.T)
    assert np.all((g == 0) | (g == 1)) and not np.any(np.diag(g))
    assert all(np.all(g[:, 12*t:12*t+12].sum(axis=1) == 1) for t in range(3))
    assert not np.any(np.diag(g@g@g))
    assert g[u, v] == 1 and u//12 != v//12
    h = 3*np.eye(36, dtype=np.int64)-g
    assert rank_pivots(h.tolist())[0] == 35
    green = (np.array(inverse7((h+1).tolist()), dtype=np.int64)-1) % 7
    d = np.array([[int(i//12 == j//12) for j in range(36)] for i in range(36)])
    k = 12*np.eye(36, dtype=np.int64)-g+2-g@g-d
    c4 = int((g@g@g)[u, v]-5)
    assert 0 <= c4 <= 2
    pairs = [[p for p in combinations(range(12*t, 12*t+12), 2) if not g[p[0], p[1]]]
             for t in range(3)]
    neighbours = [set(np.flatnonzero(row).tolist()) for row in g]

    def pool(center):
        layer = center//12
        others = [t for t in range(3) if t != layer]
        result = {}
        for pair in pairs[layer]:
            if center not in pair:
                continue
            group = next(i for i in pair if i != center)
            candidates = []
            for p in pairs[others[0]]:
                for q in pairs[others[1]]:
                    support = tuple(sorted(pair+p+q))
                    ss = set(support)
                    if any(len(neighbours[i] & ss) > 2-int(i in ss) for i in range(36)):
                        continue
                    if any(k[i, j] <= 0 for i, j in combinations(support, 2)):
                        continue
                    if sum(int(green[i, j]) for i in support for j in support) % 7 != 6:
                        continue
                    candidates.append(support)
            result[group] = candidates
        assert len(result) == 10
        return result

    pu, pv = pool(u), pool(v)
    common_u = {s for domain in pu.values() for s in domain if v in s}
    common_v = {s for domain in pv.values() for s in domain if u in s}
    assert common_u == common_v
    return g, green, k, c4, pu, pv, sorted(common_u)


def branch_model(g, green, k, c4, u, v, pu, pv, common):
    w = np.array([int(i in common) for i in range(36)], dtype=np.int64)
    assert (g@w)[u] == (g@w)[v] == 1
    common_groups = [next(i for i in common if i//12 == x//12 and i != x) for x in (u, v)]
    labels, domains = [], []
    for side, (pool, other, omitted) in enumerate(zip((pu, pv), (v, u), common_groups)):
        for group, candidates in sorted(pool.items()):
            if group == omitted:
                continue
            domain = [s for s in candidates if other not in s
                      and sum(int(green[i, j]) for i in common for j in s) % 7 == 3
                      and len(set(common) & set(s)) <= 2]
            labels.append((side, group))
            domains.append(domain)
    assert len(domains) == 18
    if any(not domain for domain in domains):
        return None, labels, domains, None
    model = cp_model.CpModel()
    choices = [model.NewIntVar(0, len(domain)-1, f"choice_{i}") for i, domain in enumerate(domains)]
    arrays = [np.array([[int(p in s) for p in range(36)] for s in domain], dtype=np.int64)
              for domain in domains]

    def element(choice, values, name):
        values = [int(x) for x in values]
        if min(values) == max(values):
            return values[0]
        result = model.NewIntVar(min(values), max(values), name)
        model.AddElement(choice, values, result)
        return result

    def both(a, b, name):
        if isinstance(a, int):
            return b if a else 0
        if isinstance(b, int):
            return a if b else 0
        result = model.NewBoolVar(name)
        model.Add(result <= a)
        model.Add(result <= b)
        model.Add(result >= a+b-1)
        return result

    incidence = [[element(choices[i], arr[:, p], f"inc_{i}_{p}") for p in range(36)]
                 for i, arr in enumerate(arrays)]
    adjacency, overlaps = {}, {}
    for i, j in combinations(range(18), 2):
        products = (arrays[i]@green@arrays[j].T) % 7
        overlap = arrays[i]@arrays[j].T
        binary = 3-products
        good = ((binary == 0) | (binary == 1)) & (overlap <= 2-binary)
        left, right = np.nonzero(good)
        tuples = [(int(a), int(b), int(binary[a, b]), int(overlap[a, b])) for a, b in zip(left, right)]
        if not tuples:
            return None, labels, domains, None
        edge = model.NewBoolVar(f"edge_{i}_{j}")
        ov = model.NewIntVar(0, 2, f"overlap_{i}_{j}")
        adjacency[i, j] = edge
        overlaps[i, j] = ov
        model.AddAllowedAssignments([choices[i], choices[j], edge, ov], tuples)

    def edge(i, j):
        return adjacency[min(i, j), max(i, j)]

    side_indices = [[i for i, label in enumerate(labels) if label[0] == side] for side in (0, 1)]
    for side, center in enumerate((u, v)):
        indices = side_indices[side]
        for i in indices:
            cap = element(choices[i], 1-arrays[i]@g[center], f"cap_{i}")
            model.Add(sum(edge(i, j) for j in indices if j != i) == cap)
            model.Add(sum(edge(i, j) for j in side_indices[1-side]) <= 1)
        for p in range(36):
            terms = [incidence[i][p] for i in indices]
            model.Add(sum(terms)+int(w[p]) == int(k[p, center]))
    model.Add(sum(edge(i, j) for i in side_indices[0] for j in side_indices[1]) == 7+c4)

    # A 4-cycle alternating the two internal matchings and the cross
    # matching would yield a prism on the edge uv, forbidden by P=0.
    for a, b in combinations(side_indices[0], 2):
        for c, d in combinations(side_indices[1], 2):
            model.Add(edge(a, b)+edge(c, d)+edge(a, c)+edge(b, d) <= 3)
            model.Add(edge(a, b)+edge(c, d)+edge(a, d)+edge(b, c) <= 3)

    # Every pair of near points has at most its prescribed total number
    # of common far neighbours, even in this partial system.
    for p, q in combinations(range(36), 2):
        terms = [element(choices[i], arr[:, p]*arr[:, q], f"pair_{i}_{p}_{q}")
                 for i, arr in enumerate(arrays)]
        model.Add(sum(terms)+int(w[p]*w[q]) <= int(k[p, q]))

    # Count all common neighbours already present in this partial graph.
    # Far/far: near-shadow overlap plus paths through selected far points.
    for i, j in combinations(range(18), 2):
        terms = [both(edge(i, z), edge(j, z), f"ff_common_{i}_{j}_{z}")
                 for z in range(18) if z not in (i, j)]
        model.Add(overlaps[i, j]+sum(terms) <= 2-edge(i, j))
    # Near/far: fixed neighbours in G plus selected far neighbours.
    for i, arr in enumerate(arrays):
        for p in range(36):
            gn = element(choices[i], arr@g[p], f"gn_{i}_{p}")
            terms = [both(incidence[z][p], edge(i, z), f"nf_common_{i}_{p}_{z}")
                     for z in range(18) if z != i]
            model.Add(gn+sum(terms) <= 2-incidence[i][p])
    return model, labels, domains, choices


def verify_witness(g, green, k, c4, u, v, common, labels, supports):
    vectors = np.array([[int(p in s) for p in range(36)] for s in supports+[common]], dtype=np.int64)
    assert len(set(supports+[common])) == 19
    gram = (vectors@green@vectors.T) % 7
    a = (3*np.eye(19, dtype=np.int64)+3-gram) % 7
    assert np.all((a == 0) | (a == 1)) and not np.any(np.diag(a))
    assert not np.any(a[18])
    overlap = vectors@vectors.T
    assert all(overlap[i, j] <= 2-a[i, j] for i, j in combinations(range(19), 2))
    known_common = overlap+a@a
    assert all(known_common[i, j] <= 2-a[i, j] for i, j in combinations(range(19), 2))
    assert np.all(g@vectors.T+vectors.T@a <= 2-vectors.T)
    assert np.all(vectors.T@vectors <= k)
    side_indices = [[i for i, label in enumerate(labels) if label[0] == side] for side in (0, 1)]
    for side, center in enumerate((u, v)):
        indices = side_indices[side]
        assert np.array_equal(vectors[indices].sum(axis=0)+vectors[18], k[:, center])
        for i in indices:
            assert a[i, indices].sum() == 1-g[center]@vectors[i]
            assert a[i, side_indices[1-side]].sum() <= 1
    assert a[np.ix_(side_indices[0], side_indices[1])].sum() == 7+c4
    for a0, b in combinations(side_indices[0], 2):
        for c, d in combinations(side_indices[1], 2):
            assert a[a0, b]+a[c, d]+a[a0, c]+a[b, d] <= 3
            assert a[a0, b]+a[c, d]+a[a0, d]+a[b, c] <= 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--u", type=int, default=0)
    parser.add_argument("--v", type=int, default=12)
    parser.add_argument("--apex-start", type=int, default=0)
    parser.add_argument("--max-apex", type=int, default=1)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    assert args.seconds > 0 and args.apex_start >= 0 and args.max_apex >= 0
    start = time.monotonic()
    g0 = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"] if args.ball else cyclic_ball()
    g, green, k, c4, pu, pv, common_pool = prepare(g0, args.u, args.v)
    report = {"input": str(args.ball) if args.ball else "cyclic(2,4,1)",
              "centers": [args.u, args.v], "c4_at_edge": c4,
              "ortools_version": ortools.__version__, "numpy_version": np.__version__,
              "unary_pool_sizes": [[len(domain) for _, domain in sorted(pool.items())] for pool in (pu, pv)],
              "common_apex_candidates": len(common_pool), "branches": [],
              "scope": "joint local necessary model; not a full SRG completion"}
    print(json.dumps({"prepared": True, "common_apex_candidates": len(common_pool),
                      "seconds": round(time.monotonic()-start, 3)}), flush=True)
    end = len(common_pool) if args.max_apex == 0 else min(len(common_pool), args.apex_start+args.max_apex)
    for index in range(args.apex_start, end):
        if time.monotonic()-start >= args.seconds:
            break
        common = common_pool[index]
        model, labels, domains, choices = branch_model(g, green, k, c4, args.u, args.v, pu, pv, common)
        record = {"apex_index": index, "common_apex_support": common,
                  "domain_sizes": [len(d) for d in domains]}
        if model is None:
            record["status"] = "INFEASIBLE_EMPTY_DOMAIN_OR_PAIR"
        else:
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            solver.parameters.random_seed = 0
            solver.parameters.max_time_in_seconds = max(0.01, args.seconds-(time.monotonic()-start))
            status = solver.Solve(model)
            record["status"] = solver.StatusName(status)
            record["solver_seconds"] = solver.WallTime()
            record["solver_branches"] = solver.NumBranches()
            if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                supports = [domain[solver.Value(choice)] for domain, choice in zip(domains, choices)]
                verify_witness(g, green, k, c4, args.u, args.v, common, labels, supports)
                record["supports"] = supports
        report["branches"].append(record)
        print(json.dumps(record), flush=True)
        if record["status"] in ("OPTIMAL", "FEASIBLE", "UNKNOWN", "MODEL_INVALID"):
            break
    statuses = [r["status"] for r in report["branches"]]
    if any(s in ("OPTIMAL", "FEASIBLE") for s in statuses):
        report["conclusion"] = "LOCAL_WITNESS_FOUND"
    elif args.apex_start == 0 and len(statuses) == len(common_pool) and all(s.startswith("INFEASIBLE") for s in statuses):
        report["conclusion"] = "ALL_COMMON_APEX_BRANCHES_EXCLUDED"
    else:
        report["conclusion"] = "PARTIAL_RUN_NO_GLOBAL_EXCLUSION"
    report["elapsed_seconds"] = time.monotonic()-start
    args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"conclusion": report["conclusion"], "elapsed_seconds": report["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
