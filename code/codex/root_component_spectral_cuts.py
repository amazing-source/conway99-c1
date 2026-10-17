"""Exact integer spectral cuts from binary C1/component relaxation solutions.

Necessary PSD matrices are L=8T=24I-8Gamma-3B^tB-B^tMB+2J and
U=15(7Pi-T)=60I+15Gamma-4B^tB+B^tMB-2J. Numerical eigenvectors
only propose integer vectors; every added negative quadratic witness is
checked with integer arithmetic. No floating verdict excludes a template.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_projector import build
from root_component_propagation import LABELS, PAIRS
from root_component_obstruction_layers import pair_layer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--layer", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    cover = next(r for r in json.loads((args.directory / "root_component_gram_orbits20.json").read_text())["records"] if r["template_index"] == args.index)
    model, graph, info = build(templates[args.index], cover, args.layer, projector=False)
    common = np.array([[len(set(p)&set(q)) for q in LABELS] for p in LABELS], dtype=np.int64)
    mates = np.array([[sum((a^1) in q for a in p) for q in LABELS] for p in LABELS], dtype=np.int64)
    lower_base = 24*np.eye(84, dtype=np.int64)-3*common-mates+2
    upper_base = 60*np.eye(84, dtype=np.int64)-4*common+mates-2
    cuts, rounds, seen = [], [], set()
    started = time.monotonic()
    for iteration in range(args.rounds):
        assert not model.validate(), model.validate()
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = args.workers
        solver.parameters.max_time_in_seconds = args.seconds
        solver.parameters.cp_model_probing_level = 0
        solver.parameters.symmetry_level = 0
        status = solver.solve(model)
        result = {"iteration": iteration, "status": solver.status_name(status), "seconds": solver.wall_time,
                  "conflicts": solver.num_conflicts, "branches": solver.num_branches}
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            gamma = np.array([[solver.value(x) for x in row] for row in graph], dtype=np.int64)
            errors = Counter()
            gamma2 = gamma @ gamma
            for u,v in PAIRS:
                if gamma[u,v]+gamma2[u,v] != 2-common[u,v]:
                    errors[pair_layer(u,v)] += 1
            result["violated_C2_by_layer"] = dict(errors)
            new_cuts = 0
            minima = {}
            for name, base, coefficient in (("T_lower",lower_base,-8),("T_upper",upper_base,15)):
                matrix = base + coefficient*gamma
                eigenvalues, vectors = np.linalg.eigh(matrix)
                minima[name] = float(eigenvalues[0])
                for i in np.flatnonzero(eigenvalues < -1e-7)[:4]:
                    vector = vectors[:,i]
                    vector /= np.max(np.abs(vector))
                    for scale in (2,4,8,16,32,64):
                        v = np.rint(scale*vector).astype(np.int64)
                        value = int(v @ matrix @ v)
                        if value >= 0:
                            continue
                        vv = tuple(int(x) for x in v)
                        key = (name,vv)
                        if key in seen:
                            continue
                        seen.add(key)
                        constant = int(v @ base @ v)
                        model.add(constant+sum(2*coefficient*int(v[u])*int(v[w])*graph[u][w]
                                               for u,w in PAIRS if v[u] and v[w]) >= 0)
                        cuts.append({"kind":name,"vector":vv,"witness_value":value,"constant":constant,
                                     "adjacency_coefficient":coefficient,"iteration":iteration})
                        new_cuts += 1
                        break
            result.update(new_exact_cuts=new_cuts, numerical_minima=minima)
            if not errors:
                info["candidate_edges"] = [[u,v] for u,v in PAIRS if gamma[u,v]]
            if not new_cuts and errors:
                result["status"] = "NO_INTEGER_CUT_FOUND"
        rounds.append(result)
        output = {**info, "template_index":args.index,"status":result["status"],"rounds":rounds,"cuts":cuts,
                  "total_seconds":time.monotonic()-started,
                  "scope":"Whole template. Only exact integer PSD inequalities are added; solver UNKNOWN stays open."}
        args.output.write_text(json.dumps(output,separators=(",",":"))+"\n",encoding="utf-8")
        print(json.dumps({**result,"cumulative_cuts":len(cuts)}),flush=True)
        if result["status"] not in ("OPTIMAL","FEASIBLE") or "candidate_edges" in info:
            break


if __name__ == "__main__":
    main()
