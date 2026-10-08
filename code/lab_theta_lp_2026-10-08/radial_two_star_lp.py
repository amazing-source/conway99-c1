"""C1, lab session, 2026-10-08. Do the two-star branches die with RADIAL star sums only?
  python radial_two_star_lp.py <codex code/codex dir> <ball json> <mode> <apex> [<apex> ...]
NEW FACT USED: in the exact potential certificates of four branches of random ball 12 (Codex's two_star_potentials.py)
the star-sum multipliers beta are positive near the centre and negative far from it, and the degree multipliers are
nearly constant on each side. Test: keep Codex's pair-marginal LP (domains, marginals) but replace
  - the 72 star-sum equations by their sums over the classes {p : G-distance(p, centre of the side) = d}  (mode "radial"),
    or by their sums over (layer of p, distance) classes                                              (mode "layer"),
    (controls: "nostar" drops the star rows, "nodeg" drops the degree rows, "total" keeps one star row per side),
  - the 36 degree equations by 4 sums (side x internal/transversal),
and drop every other row. If this weaker LP is still infeasible, the branch has a certificate whose star potential
depends only on the distance to the centre. Floating HiGHS (a diagnostic, not a certificate)."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
import numpy as np
from scipy.sparse import csr_matrix, vstack
from scipy.optimize import linprog
from joint_generic_stars import prepare
from joint_star_pair_lp import build
ball = json.load(open(sys.argv[2]))["adjacency"]; mode = sys.argv[3]; g = np.array(ball)
def dist(src):
    d = {src: 0}; q = [src]
    for x in q:
        for y in range(36):
            if g[x][y] and y not in d: d[y] = d[x] + 1; q.append(y)
    return d
D = [dist(0), dist(12)]; prepared = prepare(ball, 0, 12)
for ap in [int(a) for a in sys.argv[4:]]:
    t0 = time.time()
    try: matrix, lower, upper, names, info = build(prepared, 0, 12, ap)
    except AssertionError as e: print("apex %d: %s" % (ap, e)); continue
    keep = [r for r, nm in enumerate(names) if nm.startswith(("domain", "marginal"))]
    groups = {}
    for r, nm in enumerate(names):
        f = nm.split(":")
        if f[0] == "star_sum":
            if "nostar" in mode: continue
            side, p = int(f[1]), int(f[2]); key = ("s", side, D[side][p]) if "radial" in mode else ("s", side, p // 12, D[side][p]) if "layer" in mode else ("s", side) if "total" in mode else ("s", side, p)
            groups.setdefault(key, []).append(r)
        elif f[0] == "degree":
            if "nodeg" in mode: continue
            i, other = int(f[1]), int(f[2]); side = 0 if i < 9 else 1
            groups.setdefault(("d", side, other), []).append(r)
    rows = [matrix[keep]]; rhs = [upper[keep]]
    agg = []
    for key, rs in sorted(groups.items()):
        rows.append(csr_matrix(matrix[rs].sum(axis=0))); agg.append(float(sum(upper[r] for r in rs)))
    A = vstack(rows).astype(float); b = np.concatenate([upper[keep].astype(float), np.array(agg)])
    res = linprog(np.zeros(A.shape[1]), A_eq=A, b_eq=b, bounds=(0, 1), method="highs-ipm")
    nstar = sum(1 for k in groups if k[0] == "s")
    print("apex %d, mode %s: %d star rows (instead of 72), 4 degree rows, %d x %d: %s  [%.0f s]" % (
        ap, mode, nstar, A.shape[0], A.shape[1], "INFEASIBLE (a certificate of this shape exists, numerically)" if res.status == 2 else "feasible: this shape is not enough" if res.status == 0 else res.message[:60], time.time() - t0), flush=True)
