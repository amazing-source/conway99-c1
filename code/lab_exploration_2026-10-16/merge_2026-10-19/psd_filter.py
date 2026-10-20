"""Strength of the REAL far-projector conditions on single far vertices and on pairs (LAB 20/10/2026).

Theorem 1 of ../representation_2026-10-19 (P): for every line T,
    7 Pi_T = 3I - R - [E^T (4I + G) - 2J] K^+ E,     K = E E^T = 12I - G - G^2 + 2J - J_cl (L1),
is 7 times the orthogonal projector of rank 7 + c onto the -4 eigenvectors of Gamma carried by the far set.  Hence,
whatever rank_7(A - 3I) is, every principal submatrix of 7 Pi_T has its eigenvalues in [0, 7]:
  (S1) single far vertex w:  0 <= 7Pi(w,w) = 3.2 - e_w^T (4I+G) K^+ e_w <= 7      (1^T K^+ e_w = 6/60);
  (S2) pair w, w' (R(w,w') = 0 or 1 to be chosen): 7Pi(w,w') = 0.2 - R(w,w') - e_w^T (4I+G) K^+ e_w', and both
       [[7Pi(w,w), 7Pi(w,w')], [., 7Pi(w',w')]] and 7I minus it are PSD.
This script: for a random G_T (c = 1 generic, or a block profile), all name triples passing L2 (and L4 for c >= 2):
fraction passing (S1); fraction of the rank-37 candidates (beta(w,w) = 4 mod 7) passing (S1); for random pairs of
(S1)-candidates of distinct p-pairs, the fraction for which R = 0, R = 1, or neither is allowed by (S2).
usage: python psd_filter.py <c1|blocks:k1,k2> <seed> [pairs]"""
import json
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from oblr_prep import make_gt, near_block, P7  # noqa: E402
from ll_test import k_matrix, pairs_of  # noqa: E402
from rank7_line import ginv_mod  # noqa: E402


def main():
    spec, seed = sys.argv[1], int(sys.argv[2])
    npairs = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    rng = random.Random(seed)
    n, N = 12, 36
    s01, s12, s20, G, nc, comp, d = make_gt(spec, rng, 0, n)
    K = k_matrix(n, G).astype(float)
    Kp = np.linalg.pinv(K)
    MQ = (4 * np.eye(N) + G) @ Kp                       # (4I + G) K^+, symmetric (G and K commute)
    assert np.allclose(MQ, MQ.T, atol=1e-9)
    MNN = near_block(n, G)
    X = ginv_mod(MNN, P7)
    X = (X @ MNN % P7 @ X.T) % P7
    P = pairs_of(n)
    nb = [set(int(y) for y in np.nonzero(G[x])[0]) for x in range(N)]
    compsize = {}
    for x in range(N):
        compsize[comp[x]] = compsize.get(comp[x], 0) + 1
    tot = s1 = cand37 = cand37_s1 = 0
    diag_vals = []
    keep = []                                            # (p-pair index, names, 7Pi diag) for (S1)-passing triples
    for pi, pp in enumerate(P):
        for qq in P:
            for ss in P:
                names = [pp[0], pp[1], n + qq[0], n + qq[1], 2 * n + ss[0], 2 * n + ss[1]]
                nm = set(names)
                if any(len(nb[x] & nm) > 1 for x in names):
                    continue
                cnt = {}
                for y in names:
                    for x in nb[y]:
                        if x not in nm:
                            cnt[x] = cnt.get(x, 0) + 1
                if any(v > 2 for v in cnt.values()):
                    continue
                if nc > 1:
                    per = {}
                    for x in names:
                        per[comp[x]] = per.get(comp[x], 0) + 1
                    if any(per.get(kk, 0) * 6 != compsize[kk] for kk in compsize):
                        continue
                tot += 1
                dq = 3.2 - float(MQ[np.ix_(names, names)].sum())
                diag_vals.append(dq)
                ok1 = -1e-9 <= dq <= 7 + 1e-9
                s1 += ok1
                e = np.zeros(3 + N, dtype=np.int64)
                e[[3 + x for x in names]] = 1
                is37 = int(e @ X @ e) % P7 == 4
                cand37 += is37
                cand37_s1 += is37 and ok1
                if ok1:
                    keep.append((pi, names, dq))
    dv = np.array(diag_vals)
    res = {"gt": spec, "seed": seed, "c": nc, "d": d, "L2_triples": tot, "S1_pass": s1, "S1_frac": round(s1 / tot, 4),
           "diag7Pi_min": round(float(dv.min()), 3), "diag7Pi_median": round(float(np.median(dv)), 3),
           "diag7Pi_max": round(float(dv.max()), 3), "rank37_cands": cand37, "rank37_and_S1": cand37_s1}
    # pairs
    allowed = {"none": 0, "R0_only": 0, "R1_only": 0, "both": 0}
    for _ in range(npairs):
        a, b = rng.sample(keep, 2)
        if a[0] == b[0]:
            continue
        off0 = 0.2 - float(MQ[np.ix_(a[1], b[1])].sum())
        ok = []
        for Rv in (0, 1):
            o = off0 - Rv
            M1 = np.array([[a[2], o], [o, b[2]]])
            ev = np.linalg.eigvalsh(M1)
            ok.append(ev[0] >= -1e-9 and ev[1] <= 7 + 1e-9)
        key = "both" if all(ok) else ("R0_only" if ok[0] else ("R1_only" if ok[1] else "none"))
        allowed[key] += 1
    s = sum(allowed.values())
    res["pairs"] = {k: round(v / s, 4) for k, v in allowed.items()}
    print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
