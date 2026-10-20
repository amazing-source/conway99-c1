"""Input of star39.cpp for ANY line type (LAB 20/10/2026): the complete star of a near vertex x, with the general
7-adic formalism of oblr_prep.py instead of Omega = (3I - G + J)^-1 (which needs d = 1).

Formalism (oblr_prep.py docstring): X = symmetric reflexive g-inverse of the near block M[N,N] mod 7 (rank 38 - d),
beta(a, b) = e_a^T X e_b, residue of rank rho = r - 38 + d with form D = diag(1, .., 1, delta):
    diagonal  u^T D u = -3 - beta(w, w),      pairs  R(w, w') = beta(w, w') + u_w^T D u_w'  in {0, 1}.
star39.cpp computes R = 4 - sum_k Y_a[names_b[k]] + u^T D u'; with Y_a = 3 - X e_a (mod 7) this sum is 18 - beta = 4 - beta,
so R = beta + u^T D u' exactly.  rho <= 2 (rho = 1: u = (u0, 0), D = (delta, 0)).
Real far projector (P, LAB 20/10): H = (3I - R)(I - E^T K^+ E) = 3I - R - E^T Z E + J/9 with Z = (3I - G + J)^+ (on the
complement of the component-difference kernel, to which every e_w is orthogonal by L4), H^2 = 7H, rank H = 7 + c.
So PSD of H and 7I - H holds for every c; the star rank test (rank <= 8) is meaningful only for c = 1 (for c >= 2,
rank <= 7 + c is automatic on 10 vectors with the all-ones relation): run star39.exe with STAR_NORANK=1 when c >= 2.
Unbalanced 7-torsion (--unbal, oblr_prep.py): r(T) = 1 and residual zero on b^perp, R - 3I = E^T X E + b c^T + c b^T with
b_w = e_w . kappa, encoded as u = (b + c, b - c), D = diag(4, 3); needs r = 40 - d; no symmetry reduction.
If the star candidates' e.ker span several directions, the unbalanced case is split over the lines F_7 g of that
span (every far vertex of a graph with r(T) = 1 has e.ker on one such line): --kappa k picks the k-th.
usage: python star_prep_gen.py <spec> <seed> <inst> <x> <r> <delta> <out.bin> [--unbal [--kappa k]]
   spec = lg[:tau] (star_csp.line_graph(seed, tau), tau in -1, 1, 0 = any; the G_T of star39_prep.py),
          c1, c1t, blocks:k1,k2,.., blockst:k1,k2,.. (oblr_prep.make_gt: inst-th G_T of that kind from Random(seed)),
          c1tt (connected with d = 3);  r = global 7-rank."""
import json
import os
import random
import struct
import sys

import numpy as np

HERE = "C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16/merge_2026-10-19"
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "treasure_2026-10-19"))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
from oblr_prep import level_sets, make_gt, near_block, orbit_reps  # noqa: E402
from ll_test import components, k_matrix, pairs_of  # noqa: E402
from rank7_line import ginv_mod, kernel_mod, rank_mod  # noqa: E402

P = 7
NOUNARY_OFF = False
n, N = 12, 36


def get_gt(spec, seed, inst):
    if spec == "c1tt":                                   # connected, d = 3 (double 7-torsion, about 0.35 % of lines)
        from ll_test import gt_matrix, random_gt
        rng, k = random.Random(seed), -1
        while True:
            s01, s12, s20, _ = random_gt(n, rng, 1)
            G = gt_matrix(n, s01, s12, s20)
            d = N - rank_mod((3 * np.eye(N, dtype=np.int64) - G) % P, P)
            if d == 3:
                k += 1
                if k == inst:
                    nc, comp = components(G)
                    return s01, s12, s20, G, nc, comp, d
    if spec.startswith("lg"):
        from star_csp import line_graph
        need = int(spec.split(":")[1]) if ":" in spec else -1
        (s01, s12, s20), G, _, _, _ = line_graph(seed, need)
        nc, comp = components(G)
        Lap = (3 * np.eye(N, dtype=np.int64) - G) % P
        return s01, s12, s20, G, nc, comp, N - rank_mod(Lap, P)
    return make_gt(spec, random.Random(seed), inst, n)


def span_basis(vecs):
    """row-reduced basis (mod 7) of the span of the given vectors"""
    basis = []
    for v in vecs:
        w = np.array(v, dtype=np.int64) % P
        for bvec, piv in basis:
            if w[piv]:
                w = (w - w[piv] * bvec) % P
        if w.any():
            piv = int(np.nonzero(w)[0][0])
            w = (w * pow(int(w[piv]), P - 2, P)) % P
            basis = [((bb - bb[piv] * w) % P, pp) for bb, pp in basis] + [(w, piv)]
    return [bb for bb, _ in basis]


def directions(basis):
    """all lines F_7 g of the span, g normalised at its first nonzero entry"""
    m = len(basis)
    out = []
    for coef in np.ndindex(*([P] * m)):
        c = np.array(coef, dtype=np.int64)
        if not c.any() or c[np.nonzero(c)[0][0]] != 1:
            continue
        g = sum(int(c[i]) * basis[i] for i in range(m)) % P
        g = (g * pow(int(g[np.nonzero(g)[0][0]]), P - 2, P)) % P
        out.append(g)
    return out


def witt_reps(rho, D):
    """canonical representative of every u under O(D) by Witt's theorem: O(D) is transitive on the nonzero vectors
    with a given value of u^T D u (non-degenerate form, odd characteristic), so rep(u) = least such vector"""
    import itertools
    best = {}
    for u in itertools.product(range(P), repeat=rho):
        if any(u):
            t = sum(D[i] * u[i] * u[i] for i in range(rho)) % P
            if t not in best or u < best[t]:
                best[t] = u
    rep = {}
    for u in itertools.product(range(P), repeat=rho):
        rep[u] = best[sum(D[i] * u[i] * u[i] for i in range(rho)) % P] if any(u) else u
    return rep


def main():
    spec, seed, inst, x, r, delta, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), \
        int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    unbal = "--unbal" in sys.argv
    fmt3 = "--fmt3" in sys.argv                          # three-component format of star3.cpp (needed for rho = 3)
    kidx = int(sys.argv[sys.argv.index("--kappa") + 1]) if "--kappa" in sys.argv else None
    n_kappa = None
    s01, s12, s20, G, nc, comp, d = get_gt(spec, seed, inst)
    torsion = spec in ("c1t", "c1tt") or spec.startswith("blockst")
    rho = r - 38 + d                                     # = number of components of u in both encodings
    rres = None
    if unbal:
        rres = rho - 2                                   # residue left after the b c^T + c b^T part (r(T) = 1)
        if not torsion or rres < 0:
            raise SystemExit("unbalanced encoding needs a torsion spec and r >= 40 - d")
    if not 0 <= rho <= (3 if fmt3 else 2):
        raise SystemExit("rho = %d not supported%s" % (rho, "" if fmt3 else " (rho = 3 needs --fmt3)"))
    MNN = near_block(n, G)
    rk = rank_mod(MNN, P)
    assert rk == 38 - d, (rk, d)
    X = ginv_mod(MNN, P)
    X = (X @ MNN % P @ X.T) % P
    assert ((MNN @ X % P) @ MNN % P == MNN).all() and (X == X.T).all()
    ker = kernel_mod(MNN, P)
    if unbal:
        # u = (b + c, b - c, v) with D = diag(4, 3) + D_res: 4 s s' + 3 t t' = b c' + c b', v in F_7^rres; no symmetry
        Dres, lres = level_sets(rres, delta)
        D, lsets, rep, gorder = [4, 3] + Dres, None, None, 1
    else:
        D, lsets = level_sets(rho, delta)
        if rho == 3:
            rep, gorder = witt_reps(rho, D), None
        else:
            rep, gorder = orbit_reps(rho, D) if rho > 0 else ({(): ()}, 1)
    kappa = None
    K = k_matrix(n, G)
    nb = [set(int(z) for z in np.nonzero(G[v])[0]) for v in range(N)]
    compsize = {}
    for v in range(N):
        compsize[comp[v]] = compsize.get(comp[v], 0) + 1
    xb = x ^ 1
    b1 = [z for z in nb[x] if n <= z < 2 * n][0]
    b2 = [z for z in nb[x] if z >= 2 * n][0]
    if b2 in nb[b1]:
        raise SystemExit("x lies in a transversal triangle of G: choose another x")
    Lr = 3 * np.eye(N) - G + 1.0
    w, V = np.linalg.eigh(Lr)
    kv = V[:, np.abs(w) < 1e-8]                       # component differences (dimension c - 1)
    assert kv.shape[1] == nc - 1, (kv.shape, nc)
    Z = np.linalg.inv(Lr + kv @ kv.T)                 # = Lr^+ + P_ker; e_w^T Z e_w' = e_w^T Lr^+ e_w' (e_w orthogonal)
    ys = [y for y in range(n) if y not in (x, xb)]
    P1 = [(n + a, n + b) for a, b in pairs_of(n)]
    P2 = [(2 * n + a, 2 * n + b) for a, b in pairs_of(n)]
    nd = 3 if fmt3 else 2
    Dq = (D + [0] * 3)[:nd]

    def comb_ok(W):
        Ws = set(W)
        if any(len(nb[v] & Ws) > 1 for v in W):
            return False
        cnt = {}
        for v in W:
            for z in nb[v]:
                if z not in Ws:
                    cnt[z] = cnt.get(z, 0) + 1
        if any(c > 2 for c in cnt.values()):
            return False
        if nc > 1:
            per = {}
            for v in W:
                per[comp[v]] = per.get(comp[v], 0) + 1
            if any(per.get(kk, 0) * 6 != compsize[kk] for kk in compsize):
                return False
        return True

    if unbal:
        # the unbalanced direction g (every far vertex has e.ker in F_7 g) is unknown: if the star candidates span
        # more than one direction, the case is split over the lines of that span (--kappa k)
        seen = set()
        for y in ys:
            for q in P1:
                if K[x, q[0]] == 0 or K[x, q[1]] == 0:
                    continue
                for s_ in P2:
                    if K[x, s_[0]] == 0 or K[x, s_[1]] == 0:
                        continue
                    W = (x, y) + q + s_
                    if not comb_ok(W):
                        continue
                    e = np.zeros(3 + N, dtype=np.int64)
                    e[[3 + v for v in W]] = 1
                    ek = (e @ ker) % P
                    if ek.any():
                        seen.add(tuple(int(v) for v in ek))
        basis = span_basis(sorted(seen))
        if len(basis) >= 2:
            lines = directions(basis)
            n_kappa = len(lines)
            if kidx is None:
                raise SystemExit("unbalanced: %d possible directions, pass --kappa 0..%d" % (n_kappa, n_kappa - 1))
            kappa = lines[kidx]
        elif len(basis) == 1:
            kappa = basis[0]
    stats = []
    with open(out, "wb") as f:
        f.write(struct.pack("<6i", rho, delta, x, b1, b2, len(ys)))
        f.write(struct.pack("<%di" % (N * 3), *[z for v in range(N) for z in sorted(nb[v])]))
        f.write(struct.pack("<%di" % N, *[int(K[x, v]) for v in range(N)]))
        f.write(struct.pack("<%di" % nd, *Dq))
        for y in ys:
            tris, cands = [], []
            for qi, q in enumerate(P1):
                if K[x, q[0]] == 0 or K[x, q[1]] == 0:
                    continue
                for si, s in enumerate(P2):
                    if K[x, s[0]] == 0 or K[x, s[1]] == 0:
                        continue
                    W = (x, y) + q + s
                    Ws = set(W)
                    if any(len(nb[v] & Ws) > 1 for v in W):
                        continue
                    cnt = {}
                    for v in W:
                        for z in nb[v]:
                            if z not in Ws:
                                cnt[z] = cnt.get(z, 0) + 1
                    if any(c > 2 for c in cnt.values()):
                        continue
                    if nc > 1:                                       # L4
                        per = {}
                        for v in W:
                            per[comp[v]] = per.get(comp[v], 0) + 1
                        if any(per.get(kk, 0) * 6 != compsize[kk] for kk in compsize):
                            continue
                    e = np.zeros(3 + N, dtype=np.int64)
                    e[[3 + v for v in W]] = 1
                    ek = (e @ ker) % P
                    bw = 0
                    if unbal:
                        if ek.any():
                            bw = int(ek[int(np.nonzero(kappa)[0][0])])
                            if ((bw * kappa - ek) % P).any():
                                continue                             # e.ker off the chosen direction F_7 g
                    elif ker.shape[1] and ek.any():
                        if torsion:
                            continue                                 # balanced 7-torsion only
                        raise AssertionError("far vector not orthogonal to the near kernel")
                    er = np.zeros(N)
                    er[list(W)] = 1
                    zq = Z @ er
                    dd = 3.0 + 1.0 / 9.0 - float(er @ zq)
                    if NOUNARY_OFF and (dd < -1e-9 or dd > 7 + 1e-9):
                        continue
                    Xe = (X @ e) % P
                    t = (-3 - int(e @ Xe)) % P
                    if unbal:
                        us = []                                      # 2 b c + v^T D_res v = t
                        for qv, vs in lres.items():
                            for v in vs:
                                if bw:
                                    cs = [((t - qv) * pow(2 * bw, P - 2, P)) % P]
                                else:
                                    cs = list(range(P)) if (t - qv) % P == 0 else []
                                us += [((bw + c) % P, (bw - c) % P) + tuple(v) for c in cs]
                    else:
                        us = lsets[t] if rho > 0 else ([()] if t == 0 else [])
                    if not us:
                        continue
                    Y = (3 - Xe[3:]) % P
                    ti = len(tris)
                    cap = 1 - len(nb[x] & Ws)
                    nbc = [len(nb[z] & Ws) for z in range(N)]
                    tris.append((W, qi, si, cap, int(b1 in Ws), int(b2 in Ws), Y, zq, dd, nbc))
                    for u in us:
                        canon = 1 if (unbal or rho == 0 or tuple(u) == tuple(rep[tuple(u)])) else 0
                        cands.append((ti, canon, u))
            f.write(struct.pack("<3i", y, len(tris), len(cands)))
            for (W, qi, si, cap, h1, h2, Y, zq, dd, nbc) in tris:
                f.write(struct.pack("<6i", *W))
                f.write(struct.pack("<5i", qi, si, cap, h1, h2))
                f.write(struct.pack("<%dB" % N, *[int(v) for v in Y]))
                f.write(struct.pack("<%dB" % N, *nbc))
                f.write(struct.pack("<%dd" % N, *[float(v) for v in zq]))
                f.write(struct.pack("<d", dd))
            for (ti, canon, u) in cands:
                uu = list(u) + [0] * (nd - len(u))
                f.write(struct.pack("<%di" % (2 + nd), ti, canon, *uu))
            stats.append((len(tris), len(cands)))
    print(json.dumps({"spec": spec, "seed": seed, "inst": inst, "x": x, "b1": b1, "b2": b2, "c": nc, "d": d, "r": r,
                      "rho": rho, "delta": delta, "O(D)": gorder, "triples": [s[0] for s in stats],
                      "candidates": [s[1] for s in stats], "rank_test_meaningful": nc == 1, "unbal": unbal,
                      "kappa_found": kappa is not None, "n_kappa": n_kappa, "kappa_index": kidx}))


if __name__ == "__main__":
    main()
