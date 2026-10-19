"""Build and save flag blocks (LAB 19/10/2026): for sigma indices [start, start+count) of order k, flags of order m,
the coefficient matrices of M_sigma (affine in the census parameters), facially reduced to their joint range,
saved as blocks/k{k}_m{m}_s{idx}.npz (arrays: P0 = constant part, Pp = stacked parameter parts, params = indices).
usage: python flag_build.py <census json> <k> <m> <start> <count>"""
import json, sys, time
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from flag_sdp import Census, build_matrix, flags_of  # noqa: E402
path, k, m, start, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
t0 = time.time()
cen = Census(path)
d = json.load(open(path))
sig = [rws for key, rws, aut, form in d["types"][str(k)]]
cache = {}
for si in range(start, min(start + count, len(sig))):
    fl = flags_of(sig[si], k, m)
    mats = build_matrix(cen, fl, k, m, cache)
    nf = len(fl)
    M0 = mats.get(0, np.zeros((nf, nf)))
    ps = sorted(p for p in mats if p)
    stack = np.hstack([M0] + [mats[p] for p in ps])
    U, sv, _ = np.linalg.svd(stack, full_matrices=False)
    rk = int((sv > sv.max() * 1e-10).sum()) if sv.size and sv.max() > 0 else 0
    Q = U[:, :rk]
    P0 = Q.T @ M0 @ Q
    Pp = np.array([Q.T @ mats[p] @ Q for p in ps]) if ps else np.zeros((0, rk, rk))
    np.savez_compressed("blocks/k%d_m%d_s%d.npz" % (k, m, si), P0=P0, Pp=Pp, params=np.array(ps), flags=nf)
    print("sigma %d: %d flags, reduced %d, %d parameters  [%.0f s]" % (si, nf, rk, len(ps), time.time() - t0), flush=True)
