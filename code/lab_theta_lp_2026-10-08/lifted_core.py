"""C1, lab session, 2026-10-08. Is the near/far block (saturation) needed, or do the CONDITIONED star sums suffice?
  python lifted_core.py <codex code/codex dir (commit 96e7f23)> <ball json | cyclic> <out json> <mode> <apex> [<apex> ...]
Question (after Codex's note 214): in the modes where the two-star core LP is exactly feasible (green, overlap, capacity),
add the level-1 conditioned star sums, i.e. each exact star-sum equation multiplied by the indicator "shadow i takes
candidate c" and linearised with the pair marginals:
    for every shadow i, candidate c, side s, point p:
        sum_{j in side s, j != i} sum_d n_j(d, p) y_ij(c, d)  =  ( t_s(p) - [i in s] n_i(c, p) ) x_i(c).
These are valid for every integer solution and use only the near/near block N N^T = K (star sums); no saturation, no K
filter, no degree row. Pair tables and propagation are Codex's `filtered_system(mode)` / `propagate`, rebuilt per mode.
If the LP becomes infeasible, Codex's find_bounded_dual / verify_farkas give an exact integer Farkas vector, archived in
full. A feasible outcome here is a floating diagnostic only.
Positive control of the row construction: with the environment variable PLANT=<seed>, one candidate per shadow is drawn,
the targets are redefined as the sums of the drawn candidates and the drawn pairs are declared compatible; the LP must then
be feasible (the planted integer point satisfies every row). One process, below 3 GB."""
import sys, json, time, os
sys.path.insert(0, sys.argv[1])
from itertools import combinations
import numpy as np
import highspy
from scipy.sparse import coo_matrix
from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay
from joint_star_pair_lp import find_bounded_dual, verify_farkas
from two_star_core_ablation import filtered_system
g0 = cyclic_ball() if sys.argv[2] == "cyclic" else json.load(open(sys.argv[2]))["adjacency"]; mode = sys.argv[4]; prepared = prepare(g0, 0, 12); out = {}
for ap in [int(a) for a in sys.argv[5:]]:
    t0 = time.time(); system = filtered_system(prepared, 0, 12, ap, mode)
    if os.environ.get("PLANT"):                                           # POSITIVE CONTROL of the row construction: plant an integer solution
        common, labels, arrays, sides, targets, compat = system; rng = np.random.default_rng(int(os.environ["PLANT"])); pick = [int(rng.integers(len(a))) for a in arrays]
        targets = [sum(arrays[i][pick[i]] for i in sides[s_]) for s_ in (0, 1)]
        for i, j in combinations(range(18), 2): compat[i, j][pick[i], pick[j]] = True; compat[j, i][pick[j], pick[i]] = True
        system = (common, labels, arrays, sides, targets, compat)
    result = propagate(system); alive = replay(system, result)
    if result["contradiction"] is not None: print("apex %d, mode %s: dead by propagation" % (ap, mode)); continue
    common, labels, arrays, sides, targets, compat = system; kept = [sorted(a) for a in alive]; arr = [a[k] for a, k in zip(arrays, kept)]
    side_of = {i: s for s in (0, 1) for i in sides[s]}; x = []; count = 0
    for a in arr: x.append(np.arange(count, count + len(a))); count += len(a)
    nun = count; pairs = {}
    for i, j in combinations(range(18), 2):
        left, right = np.nonzero(compat[i, j][np.ix_(kept[i], kept[j])]); pairs[i, j] = (left, right, np.arange(count, count + len(left))); count += len(left)
    rr, cc, vv, rhs, names = [], [], [], [], []
    def row(cols, vals, target, name):
        r = len(rhs)
        for c_, v_ in zip(cols, vals):
            if v_: rr.append(r); cc.append(int(c_)); vv.append(int(v_))
        rhs.append(int(target)); names.append(name)
    for i in range(18): row(x[i], [1] * len(x[i]), 1, "domain:%d" % i)
    for (i, j), (left, right, cols) in pairs.items():
        for var, ch in ((i, left), (j, right)):
            order = np.argsort(ch, kind="stable"); bounds = np.searchsorted(ch[order], np.arange(len(x[var]) + 1))
            for c in range(len(x[var])):
                sel = cols[order[bounds[c]:bounds[c + 1]]]; row(list(sel) + [x[var][c]], [1] * len(sel) + [-1], 0, "marginal:%d:%d:%d:%d" % (i, j, var, c))
    for s in (0, 1):
        for p in range(36): row(np.concatenate([x[i] for i in sides[s]]), np.concatenate([arr[i][:, p] for i in sides[s]]), targets[s][p], "star_sum:%d:%d" % (s, p))
    nbase = len(rhs)
    for i in range(18):                                                   # conditioned star sums
        for s in (0, 1):
            acc = {}                                                       # (c, p) -> (cols, vals)
            for j in sides[s]:
                if j == i: continue
                left, right, cols = pairs[min(i, j), max(i, j)]; own, oth = (left, right) if i < j else (right, left)
                nz_r, nz_p = np.nonzero(arr[j][oth])                       # pair index r, point p with n_j(d_r, p) = 1
                for r_, p_ in zip(nz_r.tolist(), nz_p.tolist()): acc.setdefault((int(own[r_]), p_), []).append(int(cols[r_]))
            for c in range(len(x[i])):
                for p in range(36):
                    coef = int(targets[s][p]) - (int(arr[i][c, p]) if side_of[i] == s else 0); cl = acc.get((c, p), [])
                    if not cl and coef == 0: continue
                    row(cl + [x[i][c]], [1] * len(cl) + [-coef], 0, "lifted:%d:%d:%d:%d" % (i, c, s, p))
    A = coo_matrix((vv, (rr, cc)), shape=(len(rhs), count), dtype=np.int64).tocsr(); b = np.array(rhs, dtype=float)
    lp = highspy.HighsLp(); lp.num_row_, lp.num_col_ = A.shape; lp.col_cost_ = np.zeros(count); lp.col_lower_ = np.zeros(count); lp.col_upper_ = np.ones(count)
    lp.row_lower_, lp.row_upper_ = b, b; lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise; lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = A.indptr, A.indices, A.data
    h = highspy.Highs()
    for k_, v_ in (("output_flag", False), ("solver", "ipm"), ("run_crossover", "off"), ("threads", 1), ("time_limit", 90.0)): h.setOptionValue(k_, v_)
    h.passModel(lp); h.run(); status = str(h.getModelStatus()); rec = {"mode": mode, "apex_index": ap, "common_apex_support": list(common), "unary": nun, "pairs": count - nun,
        "base_rows": nbase, "lifted_rows": len(rhs) - nbase, "primal_status": status, "domain_sizes": [len(a) for a in arr]}
    if "Infeasible" in status:
        cert, check, diag = find_bounded_dual(A, b, b, names, 90, False)
        if cert is not None:
            check = verify_farkas(A, b, b, names, cert); fam = {}
            for e in cert: fam[e["name"].split(":")[0]] = fam.get(e["name"].split(":")[0], 0) + 1
            rec.update({"exact_check": check, "certificate_families": fam, "farkas_certificate": cert, "row_names_count": len(names)})
        rec["dual_diagnostic"] = diag
    out[ap] = rec
    print("apex %d, mode %s + conditioned star sums: %d unary, %d pair variables, %d + %d rows: %s%s  [%.0f s]" % (ap, mode, nun, count - nun, nbase, len(rhs) - nbase, status,
          ("; EXACT Farkas, gap %d, families %s" % (rec["exact_check"]["contradiction_gap"], rec["certificate_families"])) if "exact_check" in rec else "", time.time() - t0), flush=True)
json.dump(out, open(sys.argv[3], "w"))
