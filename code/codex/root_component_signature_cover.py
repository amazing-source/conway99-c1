"""Exact individual-vertex Schur domains, conditional on a complete Gram cover."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_rectangle_domains import signature_domains, rectangle_realizations


def enrich(template, record):
    assert record["exhaustive"] and record["usable_as_gram_cover"]
    started = time.monotonic()
    edges = [tuple(e) for e in template["nongrid_edges"]]
    lift = sp.Matrix([[sp.Rational(*x) for x in row] for row in record["lift_matrix"]])
    d = lift.cols
    retained, tables, rejected, orbit_sizes = [], {}, [], []
    for old_index, values in enumerate(record["gram_anchor_values"]):
        small = sp.zeros(d)
        for (i, j), value in zip(record["anchor_pairs"], values):
            small[i, j] = small[j, i] = value
        matrix = lift * small * lift.T
        assert all(x.q == 1 for x in matrix)
        raw = [[int(x) for x in row] for row in matrix.tolist()]
        domains = signature_domains(edges, raw)
        bad = [item["rectangle"] for item in domains if item["four_sum"] is None]
        if bad:
            rejected.append({"source_gram_index": old_index, "reason": "NO_FOUR_SUM", "rectangle": bad[0]})
            continue
        corners = rectangle_realizations(edges, raw, domains, root_prism_budget=51)
        if not corners["feasible"]:
            rejected.append({"source_gram_index": old_index, "reason": "NO_CORNER_REALIZATION", "failure": corners})
            continue
        new_index = len(retained)
        retained.append(values)
        if "gram_orbit_sizes" in record:
            orbit_sizes.append(record["gram_orbit_sizes"][old_index])
        for item in domains:
            key = tuple(item["rectangle"])
            rows = tables.setdefault(key, [])
            rows.extend([new_index] + [h[i] for i in record["anchors"]] for h in item["signatures"])
    result = dict(record)
    result.update(gram_anchor_values=retained, gram_count=len(retained),
                  requires_separate_corner_realization=True, signature_domain_seconds=time.monotonic() - started,
                  source_gram_orbit_count=record["gram_count"], rejected_grams=rejected,
                  row_signature_tables=[{"rectangle": list(e), "rows": rows} for e, rows in sorted(tables.items())])
    if "gram_orbit_sizes" in record:
        result["gram_orbit_sizes"] = orbit_sizes
        result["orbit_size_histogram"] = dict(Counter(orbit_sizes))
        result["covered_input_gram_count_after_filter"] = sum(orbit_sizes)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", type=Path)
    parser.add_argument("grams", type=Path)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads(args.templates.read_text(encoding="utf-8"))["survivors"]
    original = {r["template_index"]: r for r in json.loads(args.grams.read_text(encoding="utf-8"))["records"]}
    records = []
    for index in args.indices:
        record = enrich(templates[index], original[index])
        records.append(record)
        args.output.write_text(json.dumps({"scope": "Complete Gram cover with exact vertex Schur domains and separate corner feasibility.",
                                          "source": str(args.grams), "records": records}, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({"template_index": index, "source_grams": record["source_gram_orbit_count"],
                          "remaining_grams": record["gram_count"], "seconds": record["signature_domain_seconds"],
                          "signature_table_rows": sum(len(t["rows"]) for t in record["row_signature_tables"])}), flush=True)


if __name__ == "__main__":
    main()
