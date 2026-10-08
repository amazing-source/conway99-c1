"""C1, lab session, 2026-10-08. Minimal supports of the two-star pair-LP obstruction (asked by Codex, message of 19:45 UTC).
  python min_support_two_star.py <codex code/codex dir> <ball json> <out dir> <mode> <apex> [<apex> ...]
Rows used: Codex's domain normalisations, pair marginals and pointwise star sums only (no degree, ceiling or prism row).

mode "shadows": greedy deletion of whole SHADOWS (variables). When a set of shadows is removed, their domain and marginal
  rows disappear and each star sum over the remaining shadows of a side becomes  t(p) - m <= sum <= t(p)  (m = number of
  removed shadows of that side; a removed shadow covers a point at most once). Any sub-family of a true solution
  satisfies this sub-system, so its infeasibility still excludes the branch. Output: an LP-infeasible core of shadows
  that is minimal for single deletions, with an exact integer Farkas vector (Codex's verify_farkas) archived in full.
mode "rows": all 18 shadows kept; first a dual vector minimising the L1 norm of the star multipliers (sparse support), then
  greedy deletion of single pointwise star-sum ROWS within the time budget. Output: a set of star rows minimal for single deletions, exact Farkas vector archived in full.

mode "core": the star rows found by an archived "rows" run are kept and whole shadows are then deleted greedily.

Floating HiGHS decides the greedy steps (diagnostic); only the final integer Farkas check certifies. A "feasible" answer
during the greedy is numerical: the core is an upper bound on the true minimal core. One process, below 3 GB."""
import sys, json, time, math
sys.path.insert(0, sys.argv[1])
import numpy as np
from scipy.sparse import csr_matrix, vstack, hstack, diags, identity
from scipy.optimize import linprog
from joint_generic_stars import prepare
from joint_star_pair_lp import build, find_bounded_dual, verify_farkas
ball = json.load(open(sys.argv[2]))["adjacency"]; outdir = sys.argv[3]; mode = sys.argv[4]; prepared = prepare(ball, 0, 12); BUDGET = 125.0
def system(matrix, lower, upper, names, V, star_keep, side_of, ucols):
    """Sub-system on the shadows V with the star rows star_keep. Returns (A, lo, up, names) in Codex's row convention."""
    nv = matrix.shape[1]; rows = []; lo = []; up = []; nm = []; mask = np.zeros(nv)
    for i in V: mask[ucols[i]] = 1.0
    miss = [sum(1 for i in range(18) if side_of[i] == s and i not in V) for s in (0, 1)]
    eq = [r for r, n_ in enumerate(names) if (n_.startswith("domain") and int(n_.split(":")[1]) in V) or
          (n_.startswith("marginal") and int(n_.split(":")[1]) in V and int(n_.split(":")[2]) in V)]
    rows.append(matrix[eq]); lo += [int(lower[r]) for r in eq]; up += [int(upper[r]) for r in eq]; nm += [names[r] for r in eq]
    if star_keep:
        S = (matrix[star_keep] @ diags(mask)).astype(np.int64).tocsr()
        for k, r in enumerate(star_keep):
            s = int(names[r].split(":")[1]); t = int(upper[r])
            if miss[s] == 0: rows.append(S[k]); lo.append(t); up.append(t); nm.append(names[r])
            else:
                rows.append(S[k]); lo.append(-math.inf); up.append(t); nm.append(names[r] + ":le")
                rows.append(-S[k]); lo.append(-math.inf); up.append(-(t - miss[s])); nm.append(names[r] + ":ge")
    return vstack(rows).astype(np.int64).tocsr(), np.array(lo, dtype=float), np.array(up, dtype=float), nm
def infeasible(A, lo, up):
    e = np.flatnonzero(lo == up); u = np.flatnonzero(lo != up)
    o = linprog(np.zeros(A.shape[1]), A_eq=A[e], b_eq=up[e], A_ub=A[u] if len(u) else None, b_ub=up[u] if len(u) else None, bounds=[(0, 1)] * A.shape[1], method="highs-ipm")
    return o.status == 2
def l1_star_support(A, lo, up, nm, delta):
    """Dual vector (same normalisation as Codex's find_bounded_dual, value <= -delta) minimising the L1 norm of the star multipliers."""
    nr, nc = A.shape; st = [r for r, n_ in enumerate(nm) if n_.startswith("star_sum")]; ns = len(st)
    E = csr_matrix((np.ones(ns), (np.arange(ns), st)), shape=(ns, nr)); Z = csr_matrix((ns, nc)); I = identity(ns, format="csr")
    Aub = vstack([hstack([-A.T.tocsr(), -identity(nc, format="csr"), csr_matrix((nc, ns))]),
                  csr_matrix(np.concatenate([up, np.ones(nc), np.zeros(ns)]).reshape(1, -1)),
                  hstack([E, Z, -I]), hstack([-E, Z, -I])]).tocsr()
    bub = np.concatenate([np.zeros(nc), [-delta], np.zeros(2 * ns)])
    bnd = [((-1, 1) if lo[r] == up[r] else (0, 1)) for r in range(nr)] + [(0, None)] * (nc + ns)
    o = linprog(np.concatenate([np.zeros(nr + nc), np.ones(ns)]), A_ub=Aub, b_ub=bub, bounds=bnd, method="highs")
    if o.status != 0: return None
    return {nm[r] for k, r in enumerate(st) if abs(o.x[r]) > 1e-7}
for ap in [int(a) for a in sys.argv[5:]]:
    t0 = time.time(); matrix, lower, upper, names, info = build(prepared, 0, 12, ap); matrix = matrix.tocsr()
    ucols = {int(n_.split(":")[1]): matrix[r].indices.copy() for r, n_ in enumerate(names) if n_.startswith("domain")}
    star = [r for r, n_ in enumerate(names) if n_.startswith("star_sum")]; side_of = {}
    for r in star:
        s = int(names[r].split(":")[1]); cols = set(matrix[r].indices.tolist())
        for i, c in ucols.items():
            if cols & set(c.tolist()): side_of[i] = s
    assert len(side_of) == 18 and sorted(list(side_of.values()).count(s) for s in (0, 1)) == [9, 9]
    V = set(range(18)); keep = list(star); log = []
    assert infeasible(*system(matrix, lower, upper, names, V, keep, side_of, ucols)[:3]), "full system not infeasible"
    if mode == "core":                                                                  # star rows of the archived "rows" run, then shadows
        prev = json.load(open("%s/minsupport_rows_ball12_apex%d.json" % (outdir, ap)))["star_rows_kept"]; keep = [r for r in star if names[r] in set(prev)]
        assert infeasible(*system(matrix, lower, upper, names, V, keep, side_of, ucols)[:3])
    if mode in ("shadows", "core"):
        order = sorted(range(18), key=lambda i: (len(ucols[i]), i), reverse=True)        # try the shadows with the largest domains first
        for i in order:
            if time.time() - t0 > BUDGET: log.append("budget reached before trying %s" % [j for j in order if j >= 0 and j in V and order.index(j) >= order.index(i)]); break
            if infeasible(*system(matrix, lower, upper, names, V - {i}, keep, side_of, ucols)[:3]): V.discard(i); log.append("removed shadow %d (side %d)" % (i, side_of[i]))
    else:
        A, lo, up, nm = system(matrix, lower, upper, names, V, keep, side_of, ucols); cert, check, diag = find_bounded_dual(A, lo, up, nm, 60, False)
        sup = l1_star_support(A, lo, up, nm, 0.5 * abs(diag["objective"]))
        if sup is not None and infeasible(*system(matrix, lower, upper, names, V, [r for r in star if names[r] in sup], side_of, ucols)[:3]):
            keep = [r for r in star if names[r] in sup]; log.append("L1-sparse dual: %d star rows" % len(keep))
        for r in sorted(keep, key=lambda r_: (int(names[r_].split(":")[1]), int(names[r_].split(":")[2]))):
            if time.time() - t0 > BUDGET: log.append("budget reached"); break
            trial = [q for q in keep if q != r]
            if infeasible(*system(matrix, lower, upper, names, V, trial, side_of, ucols)[:3]): keep = trial
    A, lo, up, nm = system(matrix, lower, upper, names, V, keep, side_of, ucols)
    cert, check, diag = find_bounded_dual(A, lo, up, nm, 60, False)
    if cert is not None: check = verify_farkas(A, lo, up, nm, cert)
    rec = {"ball": sys.argv[2], "edge": [0, 12], "apex_index": ap, "common_apex_support": info["common_apex_support"], "mode": mode,
           "shadows_kept": sorted(V), "sides": {str(i): side_of[i] for i in sorted(V)}, "domain_sizes_kept": {str(i): int(len(ucols[i])) for i in sorted(V)},
           "star_rows_kept": [names[r] for r in keep], "greedy_log": log, "row_names": nm, "exact_check": check, "farkas_certificate": cert,
           "replay": "rebuild with system(...) of min_support_two_star.py on (shadows_kept, star_rows_kept), then verify_farkas", "seconds": round(time.time() - t0, 1)}
    json.dump(rec, open("%s/minsupport_%s_ball12_apex%d.json" % (outdir, mode, ap), "w"))
    print("apex %d, mode %s: shadows kept %d (side u %d, side v %d) %s; star rows kept %d; exact certificate %s  [%.0f s]  %s" % (
        ap, mode, len(V), sum(1 for i in V if side_of[i] == 0), sum(1 for i in V if side_of[i] == 1), sorted(V), len(keep),
        ("gap %d, %d rows" % (check["contradiction_gap"], check["nonzero_rows"])) if cert is not None else "NOT FOUND (%s)" % diag, time.time() - t0, "; ".join(l for l in log if "budget" in l)), flush=True)
