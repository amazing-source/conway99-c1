"""Codex's Gram-free count design at any kernel dimension (LAB, 18/10/2026).

Same steps as Codex's root_component_z_pipeline.run (afa3706e), with two changes only:
  * the row catalogue comes from jhat_catalogue.py (DFS on the block graph; identical to Codex's row_catalogue where
    both run, and not limited to free dimension <= 6);
  * Codex's verifier re-enumerates 5^d points to prove the catalogue complete, which is out of reach for d >= 9; here the
    integer Farkas certificate is re-checked by recomputing the combined vector and constant with Python integers from
    the catalogue (the same arithmetic as root_component_z_design_verify.verify), and completeness rests on the DFS.
Codex's linear_system, find_certificate and solve_design are imported unchanged.
Statuses: EXCLUDED_BY_INTEGER_CERTIFICATE (checked), DESIGN_CP_INFEASIBLE (CP-SAT verdict), AGGREGATE_DESIGN_FEASIBLE,
UNKNOWN, EMPTY_ROW_CATALOGUE.
usage: python jhat_zpipeline.py <codex dir> <catalogue> <first> <last> [--only i,j] [--design-seconds S]"""
import json
import sys
import time
from itertools import combinations

codex = sys.argv[1]
sys.path.insert(0, codex)
from root_component_z_design_certificate import linear_system, find_certificate   # noqa: E402  (Codex, unchanged)
from root_component_z_design import solve_design                                    # noqa: E402  (Codex, unchanged)

from jhat_catalogue import catalogue as dfs_catalogue                               # noqa: E402
from jhat_rows import records                                                        # noqa: E402

RECT = list(combinations(range(7), 2))


def recheck(template, cat, cert):
    """Integer re-check of a Farkas certificate (arithmetic of Codex's verify, without the 5^d completeness step)."""
    columns = [(qi, si, z) for qi, item in enumerate(cat["row_types"]) for si, z in enumerate(item["states"])]
    assert cert["column_order"] == [{"rectangle": list(RECT[q]), "state_index": s} for q, s, z in columns]
    nongrid = {tuple(q) for q in template["nongrid_edges"]}
    vector, constant = [0] * len(columns), 0
    for is_bound, terms in ((False, cert["equation_multipliers"]), (True, cert["upper_bound_multipliers"])):
        for term in terms:
            kind, idx, w = term["kind"], term["indices"], term["multiplier"]
            assert type(w) is int and (not is_bound or w >= 0)
            if kind == "four_rows":
                i, = idx
                co, tg = [int(q == i) for q, s, z in columns], 4
            elif kind == "block_symmetry":
                i, j = idx
                co, tg = [int(q == i) * z[j] - int(q == j) * z[i] for q, s, z in columns], 0
            elif kind == "neighbor_moment":
                i, j = idx
                co = [z[i] * z[j] + int(q == i) * z[j] for q, s, z in columns]
                tg = 64 if i == j else 24 if set(RECT[i]) & set(RECT[j]) else 32
            elif kind == "no_three_edge_rectangle":
                i, = idx
                assert RECT[i] in nongrid
                co, tg = [z[i] if q == i else 0 for q, s, z in columns], 4
            elif kind == "degree_histogram":
                i, = idx
                assert RECT[i] in nongrid
                co, tg = [(2 * int(z[i] == 2) - int(z[i] == 1)) if q == i else 0 for q, s, z in columns], 0
            else:
                raise ValueError(kind)
            assert term["upper" if is_bound else "target"] == tg
            vector = [a + w * b for a, b in zip(vector, co)]
            constant += w * tg
    assert vector == cert["nonnegative_variable_coefficients"]
    assert constant == cert["constant_upper_bound"] < 0 and min(vector, default=0) >= 0
    return constant


def run(template, design_seconds=5.0):
    t0 = time.process_time()
    cat = dfs_catalogue(template)
    out = {"dim": template.get("kernel_dimension"),
           "row_state_count": sum(len(r["states"]) for r in cat["row_types"])}
    if any(not r["states"] for r in cat["row_types"]):
        out["status"] = "EMPTY_ROW_CATALOGUE"
        return out
    columns, equations, bounds = linear_system(template, cat, degree_histograms=True)
    cert = find_certificate(columns, equations, bounds)
    if cert["status"] == "EXCLUDED_BY_INTEGER_CERTIFICATE":
        cert["column_order"] = [{"rectangle": list(RECT[q]), "state_index": s} for q, s, z in columns]
        out["constant_upper_bound"] = recheck(template, cat, cert)
        out["status"] = "EXCLUDED_BY_INTEGER_CERTIFICATE"
        out["certificate_terms"] = len(cert["equation_multipliers"]) + len(cert["upper_bound_multipliers"])
    elif design_seconds > 0:
        d = solve_design(template, cat, seconds=design_seconds, exclude_three_edges=True)
        out["design_status"] = d["status"]
        out["status"] = ("DESIGN_CP_INFEASIBLE" if d["status"] == "INFEASIBLE" else
                         "AGGREGATE_DESIGN_FEASIBLE" if d["status"] in ("FEASIBLE", "OPTIMAL") else "UNKNOWN")
    else:
        out["status"] = "NO_CERTIFICATE_FOUND"
    out["cpu_seconds"] = round(time.process_time() - t0, 2)
    return out


if __name__ == "__main__":
    path, first, last = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    only = None
    if "--only" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    ds = float(sys.argv[sys.argv.index("--design-seconds") + 1]) if "--design-seconds" in sys.argv else 5.0
    for idx, t in enumerate(records(path)):
        if idx < first or (only is not None and idx not in only):
            continue
        if idx >= last:
            break
        r = run(t, ds)
        r["index"] = idx
        print(json.dumps(r), flush=True)
