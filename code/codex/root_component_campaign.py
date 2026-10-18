"""Run the complete component cover, checkpointing each exact global model.

INFEASIBLE is a CP-SAT verdict, not a portable proof. UNKNOWN is always kept
open. Previously completed runs are retained unless --retry-unknown is used.
The modular rank option is deliberately not used for this baseline campaign.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_root_order import arbitrary_root_rejection


TERMINAL = {"INFEASIBLE", "OPTIMAL", "FEASIBLE", "PROPAGATION_CONTRADICTION"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--retry-unknown", action="store_true")
    parser.add_argument("--refresh-only", action="store_true")
    parser.add_argument("--gram-cover", type=Path)
    parser.add_argument("--committed-only",action="store_true",help="Ignore untracked signature and projector reports in the exclusion ledger.")
    args = parser.parse_args()
    directory = args.directory.resolve()
    cover_path = directory / "root_component_cover79.json"
    templates_path = directory / "root_component_templates.json"
    grams_path = directory / "root_component_gram_budget51.json"
    cover = json.loads(cover_path.read_text(encoding="utf-8"))
    grams = json.loads(grams_path.read_text(encoding="utf-8"))["records"]
    expected = {r["template_index"] for r in grams if r["status"] == "QUOTIENT_FEASIBLE"}
    assert {r["template_index"] for r in cover["templates"]} == expected
    assert cover["template_count"] == len(expected)
    provenance = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (templates_path, grams_path, Path(__file__).with_name("root_component_global.py"))
    }
    exclusions = {}
    tracked=None
    if args.committed_only:
        repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
        tracked={(repo/name).resolve() for name in subprocess.check_output(['git','ls-files'],text=True).splitlines()}
    for name in ("root_component_linear_obstructions.json", "root_component_rectangle_probe.json",
                 "root_component_rectangle_obstructions.json", "root_component_letter_obstructions.json",
                 "root_component_gram_layer1_obstructions.json"):
        path = directory / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["root_prism_budget"] == 51 and 0 <= data["layer"] <= 4
        provenance[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for result in data["records"]:
            if result["status"] == "INFEASIBLE":
                exclusions.setdefault(result["template_index"], {
                    "exclusion_method": "CP_SAT_RELAXATION", "exclusion_source": name,
                    "exclusion_layer": data["layer"]})
    dual_path = directory / "root_component_prism_dual.json"
    if dual_path.exists():
        provenance[dual_path.name] = hashlib.sha256(dual_path.read_bytes()).hexdigest()
        for result in json.loads(dual_path.read_text(encoding="utf-8"))["records"]:
            if result.get("excludes_budget51"):
                exclusions[result["template_index"]] = {
                    "exclusion_method": "RATIONAL_LINEAR_CERTIFICATE", "exclusion_source": dual_path.name,
                    "exclusion_layer": 0, "integer_prism_lower_bound": result["integer_prism_lower_bound"]}
    complete_grams_path = directory / "root_component_gram_orbits20.json"
    if complete_grams_path.exists():
        complete_grams = {r["template_index"]: r for r in json.loads(complete_grams_path.read_text(encoding="utf-8"))["records"]}
        gram_exclusions = {}
        for path in sorted(directory.glob("root_component_signature_*.json")):
            if tracked is not None and path.resolve() not in tracked:continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if arbitrary_root_rejection(data):continue
            used = False
            for record in data.get("records", []):
                if "cases" not in record:
                    continue
                index = record["template_index"]
                complete = complete_grams[index]
                assert complete["exhaustive"] and complete["usable_as_gram_cover"]
                assert record["complete_source_gram_count"] == complete["gram_count"]
                for case in record["cases"]:
                    if case["status"] == "INFEASIBLE":
                        gi = case["gram_index"]
                        assert case["gram_anchor_values"] == complete["gram_anchor_values"][gi]
                        gram_exclusions.setdefault(index, {}).setdefault(gi, path.name)
                        used = True
            if used:
                provenance[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for index, cases in gram_exclusions.items():
            if len(cases) == complete_grams[index]["gram_count"]:
                assert set(cases) == set(range(complete_grams[index]["gram_count"]))
                exclusions[index] = {"exclusion_method": "COMPLETE_GRAM_SIGNATURE_COVER",
                                     "exclusion_source": sorted(set(cases.values())),
                                     "excluded_gram_orbits": len(cases)}
    for path in sorted(directory.glob("root_component_projector_*.json")):
        if tracked is not None and path.resolve() not in tracked:continue
        result = json.loads(path.read_text(encoding="utf-8"))
        if arbitrary_root_rejection(result):continue
        if result.get("status") == "INFEASIBLE":
            assert result["complete_gram_cover"]["exhaustive"]
            assert not result["complete_gram_cover"]["fixed_single_gram"]
            exclusions[result["template_index"]] = {"exclusion_method": "VARIABLE_GRAM_PROJECTOR",
                                                     "exclusion_source": path.name}
            provenance[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    started = time.monotonic()
    runs = []
    if args.gram_cover:
        args.gram_cover = args.gram_cover.resolve()
        provenance[args.gram_cover.name] = hashlib.sha256(args.gram_cover.read_bytes()).hexdigest()

    def result_path(index):
        suffix = "_gramcover" if args.gram_cover else ""
        return directory / f"root_component_global_{index}_budget51{suffix}.json"

    def refresh():
        results = []
        for item in cover["templates"]:
            path = directory / f"root_component_global_{item['template_index']}_budget51_gramcover.json"
            if not path.exists():
                path = directory / f"root_component_global_{item['template_index']}_budget51.json"
            result = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            if arbitrary_root_rejection(result):result={}
            status = result.get("status", "NOT_RUN")
            item["global_solver_status"] = status
            if result:
                assert result["template_index"] == item["template_index"]
                assert result["root_prism_budget"] == 51
                assert not result["fixed_gram_witness"] and not result["fixed_local_seed"]
                assert result.get("modular_rank_constraint") is None
                item["global_solver_result"] = path.name
                item["global_solver_seconds"] = result.get("solver_seconds")
            exclusion = exclusions.get(item["template_index"])
            if exclusion:
                item.update(exclusion, exclusion_status="EXCLUDED")
            elif status == "INFEASIBLE":
                item.update(exclusion_status="EXCLUDED", exclusion_method="CP_SAT_FULL",
                            exclusion_source=path.name)
            else:
                item["exclusion_status"] = "OPEN"
            results.append({"template_index": item["template_index"], "status": status})
        counts = dict(sorted(Counter(r["status"] for r in results).items()))
        cover["global_solver_counts"] = counts
        cover["exclusion_counts"] = dict(Counter(r["exclusion_status"] for r in cover["templates"]))
        cover["open_template_indices"] = [r["template_index"] for r in cover["templates"] if r["exclusion_status"] == "OPEN"]
        cover_path.write_text(json.dumps(cover, indent=2) + "\n", encoding="utf-8")
        report = {
            "scope": cover["scope"], "does_not_cover": cover["does_not_cover"],
            "input_sha256": provenance, "seconds_per_model": args.seconds,
            "portable_unsat_proof": False,
            "global_conway_exclusion": False,
            "solver_counts": counts, "runs_in_this_invocation": runs,
            "exclusion_counts": cover["exclusion_counts"],
            "open_template_indices": cover["open_template_indices"],
            "invocation_elapsed_seconds": time.monotonic() - started,
            "results": results,
        }
        (directory / "root_component_campaign.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return counts

    refresh()
    if args.refresh_only:
        print(json.dumps({"exclusion_counts": cover["exclusion_counts"],
                          "open_template_indices": cover["open_template_indices"]}), flush=True)
        return
    ordered = sorted(cover["templates"], key=lambda r: (
        r["unfixed_binary_edges_after_propagation"], r["template_index"]))
    for item in ordered:
        status = item["global_solver_status"]
        first_gram_cover_run = args.gram_cover is not None and not result_path(item["template_index"]).exists()
        if item["exclusion_status"] == "EXCLUDED" or status in TERMINAL or (status == "UNKNOWN" and not args.retry_unknown and not first_gram_cover_run):
            continue
        if args.limit and len(runs) >= args.limit:
            break
        index = item["template_index"]
        print(json.dumps({"starting": index, "remaining_edges": item["unfixed_binary_edges_after_propagation"]}), flush=True)
        command = [sys.executable, "-I", "-u", "-X", "utf8",
                   str(Path(__file__).with_name("root_component_global.py")),
                   str(templates_path), str(grams_path), "--template-index", str(index),
                   "--seconds", str(args.seconds), "--output", str(result_path(index))]
        if args.gram_cover:
            command += ["--gram-cover", str(args.gram_cover)]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        if completed.returncode:
            print(completed.stdout, flush=True)
            print(completed.stderr, file=sys.stderr, flush=True)
            raise RuntimeError(f"Template {index} exited with {completed.returncode}")
        result = json.loads(result_path(index).read_text(encoding="utf-8"))
        assert result["status"] in TERMINAL | {"UNKNOWN"}, result
        runs.append({k: result.get(k) for k in (
            "template_index", "status", "solver_seconds", "total_seconds", "branches", "conflicts")})
        print(json.dumps({"finished": runs[-1], "counts": refresh()}), flush=True)
        if result["status"] in {"OPTIMAL", "FEASIBLE"}:
            print("Full candidate found and reconstructed; stopping for inspection.", flush=True)
            break
    print(json.dumps({"final_counts": refresh(), "runs": len(runs)}), flush=True)


if __name__ == "__main__":
    main()
