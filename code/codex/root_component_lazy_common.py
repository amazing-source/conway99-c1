"""Separate exact common-neighbour upper bounds as small forbidden subgraphs.

Under C1 every Gamma row has degree 12. For each u, the sum over v!=u of
Gamma_uv+(Gamma^2)_uv is 144, exactly the sum of 2-|label_u intersect label_v|.
Consequently satisfying every upper bound implies all C2 equalities.
Each cut forbids t+1 currently present contributions to a bound t<=2;
it is a clause with at most six positive edge variables negated.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_signature_joint import build
from root_component_signature_moments import gram_matrix
from root_component_propagation import LABELS, PAIRS
from conway_global_cover import reconstruct_and_check


def solve(template, matrix, seconds, per_solve, cut_limit, eigen=False, checkpoint=None):
    started = time.monotonic()
    model, graph, info = build(template, matrix, 0, eigen=eigen, mate_normalize=True, four_corners=True)
    assert not model.validate(), model.validate()
    edge_index = {e: i for i, e in enumerate(PAIRS)}
    cuts = set()
    iterations = []
    info.update(status="RUNNING", iterations=iterations, cuts=[])
    while time.monotonic() - started < seconds:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.cp_model_probing_level = 0
        solver.parameters.symmetry_level = 0
        solver.parameters.linearization_level = 0
        solver.parameters.max_time_in_seconds = min(per_solve, seconds - (time.monotonic()-started))
        status = solver.solve(model)
        event = {"iteration": len(iterations), "status": solver.status_name(status),
                 "seconds": solver.wall_time, "branches": solver.num_branches, "conflicts": solver.num_conflicts}
        iterations.append(event)
        if status == cp_model.INFEASIBLE:
            info["status"] = "INFEASIBLE"
            break
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            info["status"] = solver.status_name(status)
            break
        gamma = [[solver.value(x) for x in row] for row in graph]
        assert all(sum(row) == 12 for row in gamma)
        violations, candidates = Counter(), []
        for u, v in PAIRS:
            target = 2 - len(set(LABELS[u]) & set(LABELS[v]))
            terms = [(edge_index[u, v],)] if gamma[u][v] else []
            terms += [(edge_index[tuple(sorted((u,w)))], edge_index[tuple(sorted((v,w)))])
                      for w in range(84) if gamma[u][w] and gamma[v][w]]
            if len(terms) <= target:
                continue
            violations[target] += 1
            for selected in combinations(terms, target + 1):
                clause = tuple(sorted({k for contribution in selected for k in contribution}))
                if clause not in cuts:
                    candidates.append(clause)
        if not violations:
            info.update(status="SAT_FULL", adjacency99=reconstruct_and_check(14, LABELS, gamma),
                        exact_all_pair_check=True)
            break
        candidates = sorted(set(candidates), key=lambda c: (len(c), c))
        assert candidates, "A previous forbidden subgraph was violated."
        selected = candidates[:cut_limit]
        for clause in selected:
            literals = []
            for k in clause:
                u, v = PAIRS[k]
                edge = graph[u][v]
                if isinstance(edge, int):
                    assert edge == 1
                else:
                    literals.append(edge.Not())
            model.add_bool_or(literals)
            cuts.add(clause)
        event.update(upper_violations=dict(violations), added_cuts=len(selected), total_cuts=len(cuts))
        info["cuts"] = [list(c) for c in sorted(cuts)]
        info["total_seconds"] = time.monotonic() - started
        print(json.dumps(event), flush=True)
        if checkpoint:
            checkpoint(info)
    if info["status"] == "RUNNING":
        info["status"] = "UNKNOWN"
    info.update(total_seconds=time.monotonic()-started, cuts=[list(c) for c in sorted(cuts)],
                common_bound_argument="Degree 12 makes all C2 upper bounds sufficient; every learned clause is necessary.")
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--gram-index", type=int, required=True)
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--per-solve", type=float, default=30)
    parser.add_argument("--cut-limit", type=int, default=2000)
    parser.add_argument("--eigen", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    covers = {r["template_index"]: r for r in json.loads((args.directory / "root_component_gram_orbits20.json").read_text())["records"]}
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    cover = covers[args.index]
    assert cover["exhaustive"] and cover["usable_as_gram_cover"]
    values = cover["gram_anchor_values"][args.gram_index]
    def checkpoint(result):
        case = dict(result, gram_index=args.gram_index, gram_anchor_values=values)
        record = {"template_index": args.index, "complete_source_gram_count": cover["gram_count"],
                  "cases": [case], "excluded": False, "all_source_grams_processed": False}
        temporary = args.output.with_suffix(".json.tmp")
        temporary.write_text(json.dumps({"scope": __doc__, "records": [record]}, separators=(",", ":"))+"\n", encoding="utf-8")
        temporary.replace(args.output)
    result = solve(templates[args.index], gram_matrix(cover, values), args.seconds, args.per_solve,
                   args.cut_limit, args.eigen, checkpoint)
    checkpoint(result)
    print(json.dumps({k:v for k,v in result.items() if k not in ("cuts", "iterations", "adjacency99")}), flush=True)


if __name__ == "__main__":
    main()
