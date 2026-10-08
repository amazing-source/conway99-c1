"""C1, lab session, 2026-10-08. Is Codex's forced pattern already impossible on THREE shadows?
  python two_apex_triples.py <codex code/codex dir> <ball json | cyclic> <centre: 0 or 12> <out json>
Fact used (Codex's counting lemma, checked by hand, valid when no 4-cycle of G passes through the centre): every complete
star contains an apex w and another member n with d_w(n) >= 2, where d_w(n) is the number of points of n outside the layer
of the centre whose residual star sum K e_centre - w equals one.
Test: the star has TWO apexes w1 (through the first transversal neighbour of the centre) and w2 (through the second); both
are isolated in the star, so the three adjacencies inside {w1, w2, n} are known (none) and everything about the triple is
determined by the three supports. Count the triples (w1, w2, n) of pool candidates with distinct labels such that
  * Green value 3 (mod 7) between each two, overlaps <= 2, pointwise w1 + w2 + n <= K e_centre  (necessary conditions);
  * [real]  the 3 x 3 matrix Q (Q_ii = 37/12 - n_i^T H^+ n_i, Q_ij = 1/12 - n_i^T H^+ n_j, H^+ the REAL pseudo-inverse of
    3I - G) is positive semidefinite (all principal minors >= -1e-9; floating point, diagnostic);
split by max(d_w1(n), d_w2(n)) >= 2 or <= 1. If no triple with d >= 2 survived, the forced pattern would be excluded by a
three-shadow argument. One process, below 2 GB."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
import numpy as np
from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
t0 = time.time(); g0 = cyclic_ball() if sys.argv[2] == "cyclic" else json.load(open(sys.argv[2]))["adjacency"]; centre = int(sys.argv[3]); first = 12 if centre == 0 else 0
u, v = (centre, first) if centre // 12 != first // 12 else (centre, first); prepared = prepare(g0, u, v); g = np.asarray(prepared[0]); green = np.asarray(prepared[1]); K = np.asarray(prepared[2]); pool = prepared[4]
second = [int(q) for q in np.flatnonzero(g[centre]) if q // 12 not in (centre // 12, first // 12)][0]; layer = centre // 12; outer = np.array([p // 12 != layer for p in range(36)])
z = int(sum(1 for p in range(36) if outer[p] and (g @ g)[p, centre] == 2)); t = K[:, centre].copy()
labs = []; sup = []
for grp, cands in sorted(pool.items()):
    for s in cands: labs.append(grp); sup.append(s)
labs = np.array(labs); C = np.zeros((len(sup), 36), dtype=np.int64)
for r, s in enumerate(sup): C[r, list(s)] = 1
GR = (C @ green @ C.T) % 7; OV = C @ C.T; H = 3 * np.eye(36) - g; HP = np.linalg.pinv(H); E = C @ HP @ C.T; qd = 37 / 12 - np.diag(E); QO = 1 / 12 - E
okpair = (GR == 3) & (OV <= 2) & (labs[:, None] != labs[None, :]) & ((C[:, None, :] + C[None, :, :] <= t[None, None, :]).all(axis=2) if len(sup) <= 6000 else True)
A1 = np.flatnonzero(C[:, first] == 1); A2 = np.flatnonzero(C[:, second] == 1); N0 = np.flatnonzero((C[:, first] == 0) & (C[:, second] == 0)); tol = 1e-9
cnt = {"mod7_d_ge2": 0, "mod7_d_le1": 0, "real_d_ge2": 0, "real_d_le1": 0}; pairs = 0; pairs_real = 0; ex = []
for a in A1:
    ta = t - C[a]; da_all = (C[:, outer] * (ta[outer] == 1)[None, :]).sum(axis=1)
    for b in A2[okpair[a, A2]]:
        pairs += 1; tb = t - C[b]; m2 = qd[a] * qd[b] - QO[a, b] ** 2; pr = qd[a] >= -tol and qd[b] >= -tol and m2 >= -tol; pairs_real += int(pr)
        nn = N0[okpair[a, N0] & okpair[b, N0]]
        if not len(nn): continue
        nn = nn[((C[nn] + C[a] + C[b]) <= t).all(axis=1)]
        if not len(nn): continue
        d = np.maximum(da_all[nn], (C[nn][:, outer] * (tb[outer] == 1)[None, :]).sum(axis=1)); ge = d >= 2
        cnt["mod7_d_ge2"] += int(ge.sum()); cnt["mod7_d_le1"] += int((~ge).sum())
        if pr:
            det = (qd[a] * qd[b] * qd[nn] + 2 * QO[a, b] * QO[a, nn] * QO[b, nn] - qd[a] * QO[b, nn] ** 2 - qd[b] * QO[a, nn] ** 2 - qd[nn] * QO[a, b] ** 2)
            ok = (qd[nn] >= -tol) & (qd[a] * qd[nn] - QO[a, nn] ** 2 >= -tol) & (qd[b] * qd[nn] - QO[b, nn] ** 2 >= -tol) & (det >= -tol)
            cnt["real_d_ge2"] += int((ok & ge).sum()); cnt["real_d_le1"] += int((ok & ~ge).sum())
            if len(ex) < 3 and (ok & ge).any(): k_ = nn[np.flatnonzero(ok & ge)[0]]; ex.append({"w1": [int(x) for x in sup[a]], "w2": [int(x) for x in sup[b]], "n": [int(x) for x in sup[k_]], "d": int(d[np.flatnonzero(ok & ge)[0]])})
out = {"ball": sys.argv[2], "centre": centre, "first_transversal_neighbour": first, "second": second, "four_cycles_through_centre_z": z, "pool": len(sup), "apex1_candidates": len(A1), "apex2_candidates": len(A2),
       "apex_pairs_mod7": pairs, "apex_pairs_real_psd": pairs_real, "triples": cnt, "examples_real_d_ge2": ex, "seconds": round(time.time() - t0, 1)}
json.dump(out, open(sys.argv[4], "w"), indent=1)
print("centre %d (z = %d): pool %d, apex candidates %d / %d; apex pairs passing mod 7 %d, also real 2x2 %d; triples (w1, w2, n) passing mod 7: d>=2 %d, d<=1 %d; also real 3x3 PSD: d>=2 %d, d<=1 %d  [%.0f s]" % (
    centre, z, len(sup), len(A1), len(A2), pairs, pairs_real, cnt["mod7_d_ge2"], cnt["mod7_d_le1"], cnt["real_d_ge2"], cnt["real_d_le1"], time.time() - t0)); print("examples:", ex[:2])
