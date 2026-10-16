"""Per-germ statistics of the column stage: binary range solutions, wrong T Schur norms (with the exact residues),
negative U residuals, admissible columns.  usage: python colstats.py <glob> [...]"""
import sys, json, glob
from itertools import combinations
from fractions import Fraction
from collections import Counter
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_completion_columns import prepare, inverse_on_range, linear_column_model, column_geometry
from ortools.sat.python import cp_model
OUTSIDE = [p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1)]
files = sorted(set(sum((glob.glob(p) for p in sys.argv[1:]), [])))
for f in files:
    rec = json.loads(Path(f).read_text(encoding='utf-8'))
    try:
        gamma, t8, u15, kt, ku = prepare(rec)
    except Exception:
        continue
    if kt.shape[1] != 14:
        continue
    ti, tn, td = inverse_on_range(t8)
    tot = Counter(); resid = Counter()
    for lab in OUTSIDE:
        model, var, fail = linear_column_model(lab, gamma, kt, ku)
        if fail:
            tot['congruence_fail'] += 1
            continue
        k8, _ = column_geometry(lab)
        class CB(cp_model.CpSolverSolutionCallback):
            def on_solution_callback(self):
                d = np.array([self.Value(x) for x in var], dtype=np.int64)
                b = (-8 * d - k8)[ti].astype(object)
                nt = Fraction(int(b @ tn @ b), int(td))
                tot['range_solutions'] += 1
                resid[str(nt - 20)] += 1
        s = cp_model.CpSolver(); s.parameters.num_search_workers = 1; s.parameters.enumerate_all_solutions = True
        s.parameters.max_time_in_seconds = 5
        st = s.Solve(model, CB())
        tot['labels_with_range_solutions' if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else 'labels_linear_infeasible'] += 1
    print(Path(f).name, dict(tot), 'residues 8T-norm - 20:', dict(resid.most_common(8)))
