"""C1, lab session, 2026-10-08. Direction and locality of the radial two-star obstruction.
  python radial_ball_range.py <codex code/codex dir> <ball json> <out json> <apex> [<apex> ...]
New fact tested: on the pair-marginal polytope (Codex's domain rows + pair marginals, propagated domains), the number
  m_s = sum over the 9 non-apex shadows of side s of |shadow  ∩  B_2(centre_s)|      (B_2 = G-ball of radius 2)
is prescribed by the exact star sums (target t_s = sum of the star-sum targets over B_2). For each side this prints the
range [min m_s, max m_s] on three polytopes: all pairs; pairs inside the same star only; no pair at all (domains only).
Then min and max of m_0 + m_1 with all pairs. A target outside a range = infeasibility with ONE aggregated row.
Floating HiGHS (diagnostic only; the exact certificates are in radial_two_star_exact.py). One process, < 3 GB."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import linprog
from joint_generic_stars import prepare
from joint_star_pair_lp import build
ball = json.load(open(sys.argv[2]))["adjacency"]; g = np.array(ball); out = {}
def dist(src):
    d = {src: 0}; q = [src]
    for x in q:
        for y in range(36):
            if g[x][y] and y not in d: d[y] = d[x] + 1; q.append(y)
    return d
D = [dist(0), dist(12)]; prepared = prepare(ball, 0, 12)
for ap in [int(a) for a in sys.argv[4:]]:
    t0 = time.time(); matrix, lower, upper, names, info = build(prepared, 0, 12, ap); matrix = matrix.tocsr(); nv = matrix.shape[1]
    side_of = {}                                                      # variable -> side, read off the star-sum rows
    obj = [np.zeros(nv), np.zeros(nv)]; tgt = [0, 0]; nun = info["unary_variables"]
    for r, nm in enumerate(names):
        f = nm.split(":")
        if f[0] == "star_sum" and D[int(f[1])][int(f[2])] <= 2:
            obj[int(f[1])] += np.asarray(matrix[r].todense()).ravel(); tgt[int(f[1])] += int(upper[r])
    dom = [r for r, nm in enumerate(names) if nm.startswith("domain")]; var_side = {}
    for s in (0, 1):
        for r in dom:
            cols = matrix[r].indices
            if obj[s][cols].any(): var_side[int(names[r].split(":")[1])] = s
    def rng(rows, c):
        A = matrix[rows]; b = np.array([upper[r] for r in rows], dtype=float); res = []
        for sg in (1, -1):
            o = linprog(sg * c, A_eq=A, b_eq=b, bounds=[(0, 1)] * nv, method="highs-ipm")
            res.append(None if o.status != 0 else round(sg * o.fun, 3))
        return res
    allp = [r for r, nm in enumerate(names) if nm.startswith(("domain", "marginal"))]
    same = [r for r, nm in enumerate(names) if nm.startswith("domain") or (nm.startswith("marginal") and var_side.get(int(nm.split(":")[1])) == var_side.get(int(nm.split(":")[2])))]
    rec = {"targets": tgt, "sides_of_variables": var_side}
    for s in (0, 1):
        rec["side%d" % s] = {"all_pairs": rng(allp, obj[s]), "same_star_pairs": rng(same, obj[s]), "domains_only": rng(dom, obj[s])}
    rec["sum_all_pairs"] = rng(allp, obj[0] + obj[1]); out[ap] = rec
    print("apex %d: targets (u, v) = %s | side u: all pairs %s, same-star pairs %s, domains only %s | side v: all %s, same-star %s, domains %s | m_u + m_v (all pairs) in %s, target %d  [%.0f s]" % (
        ap, tgt, rec["side0"]["all_pairs"], rec["side0"]["same_star_pairs"], rec["side0"]["domains_only"], rec["side1"]["all_pairs"], rec["side1"]["same_star_pairs"], rec["side1"]["domains_only"], rec["sum_all_pairs"], sum(tgt), time.time() - t0), flush=True)
json.dump(out, open(sys.argv[3], "w"), indent=1)
