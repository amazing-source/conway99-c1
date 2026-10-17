"""Checkpointed process pool for exact necessary fixed-Gram realizations.

Every original Gram orbit keeps its original index. Only INFEASIBLE is an
exclusion; a feasible relaxation or an interrupted search remains open.
"""

import argparse
from collections import Counter, deque
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from functools import lru_cache
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_signature_joint import solve
from root_component_signature_moments import gram_matrix
from root_component_resources import limit_research_process, atomic_json_write


@lru_cache(maxsize=None)
def load_tables(path):
    return json.loads(Path(path).read_text())


def run_one(task):
    index, gi, values, template, cover, options = task
    options = dict(options)
    table_path = options.pop("local_table_path", None)
    if table_path:
        options["local_tables"] = load_tables(table_path)
    result = solve(template, gram_matrix(cover, values), **options)
    # Necessary models may have many witnesses; retain compact diagnostics.
    result.pop("relaxation_edges", None)
    result.update(gram_index=gi, gram_anchor_values=values)
    return index, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--layer", type=int, choices=range(5), default=0)
    parser.add_argument("--eigen", action="store_true")
    parser.add_argument("--cpu-time", action="store_true", help="Budget actual process CPU time, excluding resource pauses.")
    parser.add_argument("--minc-lines", type=int,default=0,help="Enforce global c>=4 at this many fixed nonroot lines.")
    parser.add_argument("--six-prism-profiles",action="store_true")
    parser.add_argument("--line-profiles",type=int,default=0)
    parser.add_argument("--profile-triples",action="store_true")
    parser.add_argument("--triangle-cuts",action="store_true")
    parser.add_argument("--exact-triangles",action="store_true")
    parser.add_argument("--short-vectors",action="store_true")
    parser.add_argument("--linearization",type=int,choices=range(3),default=0)
    parser.add_argument("--normalize-component",action="store_true")
    parser.add_argument("--upper-projector",action="store_true")
    parser.add_argument("--rotated-boundary",action="store_true")
    parser.add_argument("--interleave",action="store_true",help="Alternate new cases between the selected templates.")
    parser.add_argument("--local-tables", type=Path)
    parser.add_argument("--retry-from", type=Path, help="Only submit completed non-exclusions from this earlier report.")
    parser.add_argument("--limit-new", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.jobs <= 6:
        parser.error("At most six jobs are allowed, all sharing the same four logical cores.")
    resources = limit_research_process(4)
    config = {"seconds": args.seconds, "layer": args.layer, "eigen": args.eigen}
    if args.cpu_time:
        config["cpu_time"] = True
    if args.minc_lines:
        config["minc_lines"] = args.minc_lines
    if args.six_prism_profiles:
        config["six_prism_profiles"] = True
    if args.line_profiles:
        config["line_profiles"] = args.line_profiles
    if args.profile_triples:
        config["profile_triples"] = True
    if args.triangle_cuts:
        config["triangle_cuts"] = True
    if args.exact_triangles:
        config["exact_triangles"] = True
    if args.short_vectors:
        config["short_vectors"] = True
    if args.linearization:
        config['linearization'] = args.linearization
    if args.normalize_component:
        config['normalize_component'] = True
    if args.upper_projector:
        config['upper_projector'] = True
    if args.rotated_boundary:
        config['rotated_boundary'] = True
    if args.interleave:
        config["interleave"] = True
    if args.local_tables:
        config["local_tables"] = str(args.local_tables)
    if args.retry_from:
        config["retry_from"] = str(args.retry_from)
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    covers = {r["template_index"]: r for r in json.loads((args.directory / "root_component_gram_orbits20.json").read_text())["records"]}
    excluded = {}
    for path in sorted(args.directory.glob("root_component_signature_*.json")):
        if path.resolve() == args.output.resolve():
            continue
        data = json.loads(path.read_text())
        for record in data.get("records", []):
            index = record.get("template_index")
            if index not in args.indices:
                continue
            for case in record.get("cases", []):
                gi = case["gram_index"]
                if case["status"] == "INFEASIBLE":
                    assert covers[index]["gram_anchor_values"][gi] == case["gram_anchor_values"]
                    excluded.setdefault((index, gi), {"status": "INFEASIBLE", "source": path.name,
                                         "gram_index": gi, "gram_anchor_values": case["gram_anchor_values"]})
    # Resuming this exact output retains completed non-exclusions as well.
    completed = {}
    if args.output.exists():
        old = json.loads(args.output.read_text())
        assert old["options"] == config
        for record in old["records"]:
            for case in record["cases"]:
                completed[record["template_index"], case["gram_index"]] = case
    for key, case in excluded.items():
        if completed.get(key, {}).get("status") != "INFEASIBLE":
            completed[key] = case
    options = {"seconds": args.seconds, "layer": args.layer, "workers": 1, "eigen": args.eigen,
               "mate_normalize": not args.normalize_component, "corners": True, "cpu_time": args.cpu_time,"minc_lines":args.minc_lines,
               "six_prism_profiles":args.six_prism_profiles,"line_profiles":args.line_profiles,
               "profile_triples":args.profile_triples,"triangle_cuts":args.triangle_cuts,
               "exact_triangles":args.exact_triangles,"short_vectors":args.short_vectors,"linearization":args.linearization,
               "normalize_component":args.normalize_component,"upper_projector":args.upper_projector,
               "rotated_boundary":args.rotated_boundary}
    if args.local_tables:
        options["local_table_path"] = str(args.local_tables.resolve())
    retry = None
    if args.retry_from:
        retry = {(r["template_index"], c["gram_index"])
                 for r in json.loads(args.retry_from.read_text())["records"]
                 for c in r.get("cases", []) if c["status"] != "INFEASIBLE"}
    tasks = []
    for index in args.indices:
        cover = covers[index]
        assert cover["exhaustive"] and cover["usable_as_gram_cover"]
        for gi, values in enumerate(cover["gram_anchor_values"]):
            if (index, gi) not in completed and (retry is None or (index, gi) in retry):
                tasks.append((index, gi, values, templates[index], cover, options))
    if args.interleave:
        groups={index:deque(t for t in tasks if t[0]==index) for index in args.indices}
        tasks=[]
        while any(groups.values()):
            for index in args.indices:
                if groups[index]:tasks.append(groups[index].popleft())
    if args.limit_new is not None:
        tasks = tasks[:args.limit_new]
    started = time.monotonic()

    def checkpoint():
        records = []
        for index in args.indices:
            cases = [c for (i, _), c in sorted(completed.items()) if i == index]
            complete = len(cases) == covers[index]["gram_count"]
            records.append({"template_index": index, "complete_source_gram_count": covers[index]["gram_count"],
                            "cases": cases, "counts": dict(Counter(c["status"] for c in cases)),
                            "all_source_grams_processed": complete,
                            "excluded": complete and all(c["status"] == "INFEASIBLE" for c in cases)})
        data = {"scope": __doc__, "options": config,
                "jobs": args.jobs, "execution": "sequential" if args.jobs==1 else "process_pool",
                "resources": resources, "elapsed_seconds": time.monotonic() - started, "records": records}
        atomic_json_write(args.output,data)

    checkpoint()
    print(json.dumps({"new_cases": len(tasks), "inherited_exclusions": len(excluded)}), flush=True)
    if args.jobs==1:
        # No Windows multiprocessing handles are needed for a single worker.
        # Running in this process also keeps CPU pause/resume ownership simple.
        for task in tasks:
            index,case=run_one(task)
            completed[index,case['gram_index']]=case
            print(json.dumps({'template':index,**case}),flush=True)
            checkpoint()
        print(json.dumps({'finished':True,'elapsed_seconds':time.monotonic()-started}),flush=True)
        return
    todo = iter(tasks)
    with ProcessPoolExecutor(max_workers=args.jobs, initializer=limit_research_process, initargs=(4,)) as pool:
        pending = {}
        for _ in range(args.jobs):
            task = next(todo, None)
            if task is not None:
                pending[pool.submit(run_one, task)] = task[:2]
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                pending.pop(future)
                index, case = future.result()
                completed[index, case["gram_index"]] = case
                print(json.dumps({"template": index, **case}), flush=True)
                checkpoint()
                task = next(todo, None)
                if task is not None:
                    pending[pool.submit(run_one, task)] = task[:2]
    print(json.dumps({"finished": True, "elapsed_seconds": time.monotonic()-started}), flush=True)


if __name__ == "__main__":
    main()
