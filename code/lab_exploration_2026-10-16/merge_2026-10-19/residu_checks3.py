"""T6 for NOTE_RESIDU_GLOBAL.md: 3-side Schur identity (LAB 20/10/2026).
Schur complement of Y3 = 4I + A_59 - (2/11)J w.r.t. the ball block N[T] equals H3 = 4I + R - (2/35)J - E^T (4I+G)^-1 E
for ARBITRARY far-far values R, i.e.  (2/11)J + B3^T Y3^+ B3 = (2/35)J + E^T (4I+G)^-1 E  with B3 = E_ext - (2/11)J.
Also: Y3 >= 0 of rank 36 and the range condition.  usage: python residu_checks3.py <out.json>"""
import json, os, random, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
sys.path.insert(0, HERE)
from ll_test import gt_matrix, random_gt  # noqa: E402
from residu_checks import near_block, random_names  # noqa: E402
n, N = 12, 36
rng = random.Random(3)
out = {"lines": 0, "Y3_psd_rank36": 0, "range_ok": 0, "maxerr": 0.0}
for _ in range(20):
    s01, s12, s20, _t = random_gt(n, rng, 1)
    G = gt_matrix(n, s01, s12, s20)
    A = near_block(G).astype(float)
    Y3 = 4 * np.eye(3 + N) + A - (2 / 11) * np.ones((3 + N, 3 + N))
    ev = np.linalg.eigvalsh(Y3)
    out["lines"] += 1
    out["Y3_psd_rank36"] += int(ev.min() > -1e-9 and int((ev > 1e-9).sum()) == 36)
    Yp = np.linalg.pinv(Y3, rcond=1e-10)
    Es = np.array([random_names(rng) for _ in range(12)]).T.astype(float)
    Eext = np.vstack([np.zeros((3, Es.shape[1])), Es])
    B3 = Eext - (2 / 11) * np.ones(Eext.shape)
    out["range_ok"] += int(np.abs((np.eye(3 + N) - Y3 @ Yp) @ B3).max() < 1e-8)
    J = np.ones((Es.shape[1], Es.shape[1]))
    lhs = (2 / 11) * J + B3.T @ Yp @ B3
    rhs = (2 / 35) * J + Es.T @ np.linalg.inv(4 * np.eye(N) + G) @ Es
    out["maxerr"] = max(out["maxerr"], float(np.abs(lhs - rhs).max()))
json.dump(out, open(sys.argv[1], "w"))
print(json.dumps(out))
