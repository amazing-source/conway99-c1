"""C1, lab session, 2026-10-08. EXACT certificates for the radial two-star LP (see radial_two_star_lp.py).
  python radial_two_star_exact.py <codex code/codex dir> <ball json> <out json> <apex> [<apex> ...]
Rows kept: Codex's domain normalisations and pair marginals; the 72 star-sum equations replaced by their sums over the
classes {p : G-distance(p, centre of its side) = d}; NO degree row, no ceiling, no prism row.
With the environment variable RADIAL_BALL=t the classes are only "distance <= t" and "distance > t" (one effective row per side).
With RADIAL_BALL=pt nothing is aggregated: the 72 pointwise star sums, still without any degree row (control).
The certificate is searched and verified with Codex's own find_bounded_dual / verify_farkas (integer Farkas check with
the box 0 <= x <= 1) applied to this reduced integer matrix."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
import numpy as np
from scipy.sparse import csr_matrix, vstack
from joint_generic_stars import prepare
from joint_star_pair_lp import build, find_bounded_dual, verify_farkas
import os
ball = json.load(open(sys.argv[2]))["adjacency"]; g = np.array(ball); out = {}
THR = os.environ.get("RADIAL_BALL")                      # e.g. RADIAL_BALL=2: only two classes per side, distance <= 2 and distance >= 3
cls = (lambda d: d) if THR in (None, "pt") else (lambda d: 0 if d <= int(THR) else 1)
def dist(src):
    d = {src: 0}; q = [src]
    for x in q:
        for y in range(36):
            if g[x][y] and y not in d: d[y] = d[x] + 1; q.append(y)
    return d
D = [dist(0), dist(12)]; prepared = prepare(ball, 0, 12)
for ap in [int(a) for a in sys.argv[4:]]:
    t0 = time.time(); matrix, lower, upper, names, info = build(prepared, 0, 12, ap)
    keep = [r for r, nm in enumerate(names) if nm.startswith(("domain", "marginal"))]; groups = {}
    for r, nm in enumerate(names):
        f = nm.split(":")
        if f[0] == "star_sum": groups.setdefault((int(f[1]), int(f[2]) if THR == "pt" else cls(D[int(f[1])][int(f[2])])), []).append(r)
    rows = [matrix[keep]]; lo = [lower[r] for r in keep]; up = [upper[r] for r in keep]; nm2 = [names[r] for r in keep]
    for key, rs in sorted(groups.items()):
        rows.append(csr_matrix(matrix[rs].sum(axis=0), dtype=np.int64)); val = int(sum(int(upper[r]) for r in rs)); lo.append(val); up.append(val); nm2.append("radial_star:%d:%d" % key)
    A = vstack(rows).astype(np.int64).tocsr()
    cert, check, diag = find_bounded_dual(A, np.array(lo, dtype=float), np.array(up, dtype=float), nm2, 60, False)
    if cert is None: print("apex %d: no exact certificate found (%s)" % (ap, diag)); continue
    check = verify_farkas(A, np.array(lo, dtype=float), np.array(up, dtype=float), nm2, cert)
    rad = {e["name"]: e["multiplier"] for e in cert if e["name"].startswith("radial_star")}
    fam = {}
    for e in cert: fam[e["name"].split(":")[0]] = fam.get(e["name"].split(":")[0], 0) + 1
    out[ap] = {"exact_check": check, "families": fam, "radial_multipliers": rad, "radial_class_sizes": {"%d:%d" % k: len(v) for k, v in sorted(groups.items())}}
    print("apex %d: EXACT Farkas certificate, gap %d, rows by family %s; radial multipliers %s  [%.0f s]" % (ap, check["contradiction_gap"], fam, rad, time.time() - t0), flush=True)
json.dump(out, open(sys.argv[3], "w"), indent=1)
