"""Checkpoint a cheap exact short-lattice-vector filter over remaining Grams."""

import argparse
from collections import Counter
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process
from root_component_short_vectors import short_directions, filter_domains, admissible, evaluations
from root_component_signature_moments import gram_matrix
from root_rectangle_domains import signature_domains, corner_graphs, RECTANGLE_LABELS
from ortools.sat.python import cp_model
import sympy as sp


def controls():
    examples = [([[2]], (1, 0)), ([[2, -1], [-1, 2]], (3, 0)),
                ([[2, -1, 1], [-1, 2, 1], [1, 1, 2]], (3, 0)),
                ([[2, -1, 0, 0], [-1, 2, -1, -1], [0, -1, 2, 0], [0, -1, 0, 2]], (12, 12))]
    for gram, expected in examples:
        data = short_directions(gram)
        actual = tuple(sum(d["norm"] == n for d in data["directions"]) for n in (2, 4))
        assert actual == expected, (actual, expected)
    redundant = short_directions(examples[2][0])
    assert admissible((1, 0, 1), redundant)
    assert not admissible((1, 1, 2), redundant)
    paths = corner_graphs(3)
    assert len(paths) == 4
    for adjacency, _, signature in paths:
        positive = [i for i, h in enumerate(signature) if h == 1]
        assert len(positive) == 2 and set(RECTANGLE_LABELS[positive[0]]) & set(RECTANGLE_LABELS[positive[1]])
    return {"exact_lattice_enumeration_controls": len(examples), "redundant_generator_control": True,
            "three_edge_rectangle_patterns": len(paths), "all_violate_short_matching": True}


def scan_case(edges, matrix, seconds, direct_only=False):
    started = time.process_time()
    diagonal_two = [list(edges[i]) for i in range(matrix.rows) if matrix[i, i] == 2]
    if diagonal_two:
        return {'status': 'INFEASIBLE', 'reason': 'three_edge_rectangle_forces_norm14_with_shared_positive_label',
                'rectangles': diagonal_two, 'total_cpu_seconds': time.process_time()-started}
    if direct_only:
        return {'status': 'UNKNOWN', 'reason': 'no_three_edge_rectangle'}
    data = short_directions(matrix)
    domains = {tuple(x["rectangle"]): x for x in signature_domains(edges, matrix.tolist())}
    info = filter_domains(domains, data)
    bad = [r for r, d in domains.items() if not d["signatures"]]
    if bad:
        return {"status": "INFEASIBLE", "reason": "empty_short_vector_domain", "rectangles": bad,
                "short_vector_filter": info, "directions": data}
    # First moments enforce four rows per rectangle; second moments enforce H^t H=7R.
    model = cp_model.CpModel()
    terms = []
    matching_terms = {}
    anchors = data["anchors"]
    for ri, item in enumerate(domains.values()):
        hs = [tuple(h[i] for i in anchors) for h in item["signatures"]]
        counts = [model.new_int_var(0, 4, f"n_{ri}_{i}") for i in range(len(hs))]
        model.add(sum(counts) == 4)
        for ai, a in enumerate(anchors):
            model.add(sum(v * h[ai] for v, h in zip(counts, hs)) == item["target"][a])
        terms.extend(zip(counts, hs))
        for h, count in zip(item['signatures'], counts):
            for root_id, value in enumerate(evaluations(h, data, roots_only=True)):
                if value:
                    for root in item['rectangle']:
                        matching_terms.setdefault((root_id, value, root), []).append(count)
    for root_id in range(sum(d['norm'] == 2 for d in data['directions'])):
        for value in (-1, 1):
            for root in range(7):
                model.add(sum(matching_terms.get((root_id, value, root), [])) == 2)
    for i, j in combinations_with_replacement(range(len(anchors)), 2):
        model.add(sum(v * h[i] * h[j] for v, h in terms) == 7 * int(matrix[anchors[i], anchors[j]]))
    assert not model.validate(), model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = max(60, 100 * seconds)
    search_start = time.process_time()
    done = threading.Event()
    def interrupt():
        while not done.wait(.02):
            if time.process_time() - search_start >= seconds:
                solver.stop_search()
                return
    timer = threading.Thread(target=interrupt, daemon=True)
    timer.start()
    try:
        status = solver.solve(model)
    finally:
        done.set()
        timer.join()
    return {"status": solver.status_name(status), "short_vector_filter": info,
            "solver_cpu_seconds": time.process_time() - search_start,
            "total_cpu_seconds": time.process_time() - started,
            "reason": "necessary_integral_signature_moments"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--grams", type=Path, required=True)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--seconds", type=float, default=1)
    parser.add_argument("--direct-only", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    resources = limit_research_process(4)
    checks = controls()
    covers = {r["template_index"]: r for r in json.loads(args.grams.read_text())["records"]}
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    records = []
    output = {"scope": "Necessary short integral eigenvector bounds and exact moments; feasible is not a graph.",
              "direct_only": args.direct_only,
              "source": str(args.grams), "resources": resources, "controls": checks, "records": records}
    if args.output.exists():
        old = json.loads(args.output.read_text())
        assert old["source"] == str(args.grams)
        assert old.get('direct_only', False) == args.direct_only
        records.extend(old["records"])
    def checkpoint():
        temp = args.output.with_suffix(".json.tmp")
        temp.write_text(json.dumps(output, separators=(",", ":")) + "\n", encoding="utf-8")
        temp.replace(args.output)
    for index in args.indices:
        cover = covers[index]
        record = next((r for r in records if r["template_index"] == index), None)
        if record is None:
            record = {"template_index": index,
                      "complete_source_gram_count": cover.get("source_gram_count", cover["gram_count"]), "cases": []}
            records.append(record)
        completed = {c["gram_index"] for c in record["cases"]}
        edges = [tuple(e) for e in templates[index]["nongrid_edges"]]
        ids = cover.get("source_gram_indices", list(range(cover["gram_count"])))
        for gi, values in zip(ids, cover["gram_anchor_values"]):
            if gi in completed:
                continue
            result = scan_case(edges, gram_matrix(cover, values), args.seconds, args.direct_only)
            result.update(gram_index=gi, gram_anchor_values=values)
            record["cases"].append(result)
            record["counts"] = dict(Counter(c["status"] for c in record["cases"]))
            record["all_filtered_grams_processed"] = len(record["cases"]) == len(ids)
            checkpoint()
            print(json.dumps({"template": index, "gram": gi, "done": len(record["cases"]),
                              "counts": record["counts"], **result}), flush=True)


if __name__ == "__main__":
    main()
