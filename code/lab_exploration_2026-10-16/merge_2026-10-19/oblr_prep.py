"""Preparation for oblr.cpp: the 7-adic line obligation with a far residue of rank rho (LAB 19/10/2026).

Identity (Codex, September notes 124-127; re-derived and checked in ../treasure_2026-10-19): for a line T whose near
block M[N,N] (N = T u N(T), M = A - 3I mod 7) has every kernel vector killed by M[F,N],
    rank_7(A - 3I) = rank_7 M[N,N] + rank_7 Res_T,   Res_T = (R - 3I) - E^T S^- E   (60 x 60, far vertices).
rank_7 M[N,N] = 38 - d, d = dim ker_7 (3I - G_T); the kernel condition holds for d = 1 (line eigenvectors) and, by the
equitable lemma L4, for the component vectors of a disconnected G_T with d = c.  With r = rank_7(A - 3I):
    rho := rank_7 Res_T = r - 38 + d.     (c = 1 generic: rho = r - 37 in {0, 2, 4, 6}; c = 2, d = 2: rho = r - 36.)
Encoding: Res_T = U D U^T with D = diag(1, .., 1, delta) (rho x rho, delta = 1 or 3; any non-degenerate symmetric form
over F_7 is congruent to one of these).  A far vertex is (name triple, u in F_7^rho) with
    diagonal:   u^T D u = -3 - beta(w, w)              (R(w,w) = 0),     beta(a, b) = e_a^T S^- e_b,
    pairs:      R(w, w') = beta(w, w') + u_w^T D u_w'  must be 0 or 1.
Candidate filters: L2 (lambda/mu between a near vertex and w), L4 for c >= 2 (exactly |K|/6 names in every component K),
orthogonality of e_w to ker M[N,N] (asserted).  Pair filters and the exact counts are applied in oblr.cpp.

usage: python oblr_prep.py <gt> <seed> <inst> <rho> <delta> <out.bin>
  gt = c1 (random connected G_T with d = 1), c1t (connected, d = 2: a 7-torsion line; only far vertices orthogonal
       to the near kernel are kept, i.e. the balanced case, the only one possible at rank 37 since
       rank_7(A - 3I) = 38 - d + 2 r(T) + rho), or blocks:k1,k2,.. (components of 6 k_i vertices, d = c required)
"""
import itertools
import json
import os
import random
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "treasure_2026-10-19"))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
from ll_test import block_gt, components, gt_matrix, k_matrix, pairs_of, random_gt  # noqa: E402
from rank7_line import ginv_mod, kernel_mod, rank_mod  # noqa: E402

P7 = 7


def near_block(n, G):
    N = 3 * n
    A = np.zeros((3 + N, 3 + N), dtype=np.int64)
    for a in range(3):
        for b in range(3):
            if a != b:
                A[a, b] = 1
    for c in range(3):
        for i in range(n):
            A[c, 3 + c * n + i] = A[3 + c * n + i, c] = 1
    A[3:, 3:] = G
    return (A - 3 * np.eye(3 + N, dtype=np.int64)) % P7


def make_gt(spec, rng, inst, n=12):
    """the inst-th G_T of the requested kind with d = c (generic) from the seeded stream"""
    k = -1
    while True:
        if spec in ("c1", "c1t"):
            s01, s12, s20, _ = random_gt(n, rng, 1)
        else:
            sizes = [int(x) for x in spec.split(":")[1].split(",")]
            s01, s12, s20, _ = block_gt(n, rng, sizes)
        G = gt_matrix(n, s01, s12, s20)
        nc, comp = components(G)
        Lap = (3 * np.eye(3 * n, dtype=np.int64) - G) % P7
        d = 3 * n - rank_mod(Lap, P7)
        torsion = spec == "c1t" or spec.startswith("blockst")
        if d != (nc + 1 if torsion else nc):
            continue
        k += 1
        if k == inst:
            return s01, s12, s20, G, nc, comp, d


def level_sets(rho, delta):
    """for each value t in F_7: the list of u in F_7^rho with u^T D u = t"""
    D = [1] * (rho - 1) + [delta] if rho > 0 else []
    sets = {t: [] for t in range(P7)}
    for u in itertools.product(range(P7), repeat=rho):
        t = sum(D[i] * u[i] * u[i] for i in range(rho)) % P7
        sets[t].append(u)
    return D, sets


def orbit_reps(rho, D):
    """canonical representative (lexicographic minimum) of every u under O(D) (rho <= 2: brute force)"""
    pts = list(itertools.product(range(P7), repeat=rho))
    if rho == 0:
        return {(): ()}
    Dm = np.diag(D)
    group = []
    for flat in itertools.product(range(P7), repeat=rho * rho):
        g = np.array(flat, dtype=np.int64).reshape(rho, rho)
        if ((g.T @ Dm @ g) % P7 == Dm % P7).all():
            group.append(g)
    rep = {}
    for u in pts:
        uu = np.array(u, dtype=np.int64)
        orb = [tuple(int(x) for x in (g @ uu) % P7) for g in group]
        rep[u] = min(orb)
    return rep, len(group)


def main():
    spec, seed, inst, rho, delta, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), \
        int(sys.argv[5]), sys.argv[6]
    rng = random.Random(seed)
    n = 12
    N = 3 * n
    s01, s12, s20, G, nc, comp, d = make_gt(spec, rng, inst, n)
    MNN = near_block(n, G)
    rk = rank_mod(MNN, P7)
    assert rk == 38 - d, (rk, d)
    X = ginv_mod(MNN, P7)
    X = (X @ MNN % P7 @ X.T) % P7                         # symmetric reflexive g-inverse (needed when unbalanced)
    assert ((MNN @ X % P7) @ MNN % P7 == MNN).all() and (X == X.T).all()
    ker = kernel_mod(MNN, P7)
    torsion = spec == "c1t" or spec.startswith("blockst")
    unbal = rho < 0
    kappa = None
    if unbal:
        # unbalanced 7-torsion (r(T) = 1, residual zero on b^perp): R - 3I = E^T X E + b c^T + c b^T, b_w = e_w . kappa,
        # encoded as u = (b + c, b - c) with D = diag(4, 3) (4 s s' + 3 t t' = b c' + c b' mod 7); no symmetry used
        assert torsion
        rho = 2
        D, lsets = [4, 3], None
        rep, gorder = None, 1
    else:
        D, lsets = level_sets(rho, delta)
        if rho > 0:
            rep, gorder = orbit_reps(rho, D)
        else:
            rep, gorder = {(): ()}, 1
    P = pairs_of(n)
    nb = [set(int(y) for y in np.nonzero(G[x])[0]) for x in range(N)]
    compsize = {}
    for x in range(N):
        compsize[comp[x]] = compsize.get(comp[x], 0) + 1
    triples, cands = [], []          # per p-pair: list of triples (names, qi, si, Y) and candidates (ti, u)
    stats = []
    for pi, pp in enumerate(P):
        tl, cl = [], []
        for qi, qq in enumerate(P):
            for si, ss in enumerate(P):
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
                if nc > 1:                                       # L4: |K|/6 names in every component K
                    per = {}
                    for x in names:
                        per[comp[x]] = per.get(comp[x], 0) + 1
                    if any(per.get(kk, 0) * 6 != compsize[kk] for kk in compsize):
                        continue
                e = np.zeros(3 + N, dtype=np.int64)
                e[[3 + x for x in names]] = 1
                ek = (e @ ker) % P7
                if unbal:
                    # e . ker must lie on ONE line F_7 g (one unbalanced direction; the line eigenvectors and, by L4,
                    # the component vectors are orthogonal to every far vector); then b_w = lambda with e . ker = lambda g
                    if (ek != 0).any() and kappa is None:
                        j0 = int(np.nonzero(ek)[0][0])
                        kappa = (ek * pow(int(ek[j0]), P7 - 2, P7)) % P7          # g, normalised at its first entry
                elif ker.shape[1] and not (ek == 0).all():
                    if torsion:                                  # balanced 7-torsion: orthogonal far vertices only
                        continue
                    raise AssertionError("far vector not orthogonal to the near kernel")
                Xe = (X @ e) % P7
                bww = int(e @ Xe) % P7
                t = (-3 - bww) % P7
                if unbal:
                    if kappa is None or not ek.any():
                        bw = 0
                    else:
                        j0 = int(np.nonzero(kappa)[0][0])
                        bw = int(ek[j0])
                        assert ((bw * kappa - ek) % P7 == 0).all(), "two unbalanced directions"
                    if bw:
                        cs = [(t * pow(2 * bw, P7 - 2, P7)) % P7]
                    else:
                        cs = list(range(P7)) if t == 0 else []
                    us = [((bw + c) % P7, (bw - c) % P7) for c in cs]
                else:
                    us = lsets[t]
                if not us:
                    continue
                ti = len(tl)
                tl.append((names, qi, si, Xe[3:].copy()))
                for u in us:
                    cl.append((ti, u))
        triples.append(tl)
        cands.append(cl)
        stats.append((len(tl), len(cl)))
    K = k_matrix(n, G)
    with open(out, "wb") as f:
        f.write(struct.pack("<iiiii", n, len(P), rho, delta, gorder))
        f.write(struct.pack("<%di" % (N * 3), *[y for x in range(N) for y in sorted(nb[x])]))
        f.write(struct.pack("<%di" % (N * N), *[int(v) for v in K.ravel()]))
        for p in range(len(P)):
            f.write(struct.pack("<ii", len(triples[p]), len(cands[p])))
            for (names, qi, si, Y) in triples[p]:
                f.write(struct.pack("<6i", *names))
                f.write(struct.pack("<ii", qi, si))
                f.write(struct.pack("<%dB" % N, *[int(v) for v in Y]))
            for (ti, u) in cands[p]:
                if unbal:
                    canon = 1
                else:
                    r = rep[u] if rho > 0 else ()
                    canon = 1 if (rho == 0 or tuple(u) == tuple(r)) else 0
                f.write(struct.pack("<ii", ti, canon))
                if rho > 0:
                    f.write(struct.pack("<%di" % rho, *u))
        f.write(struct.pack("<%di" % max(rho, 1), *(D if rho > 0 else [0])))
    tri = [s[0] for s in stats]
    cn = [s[1] for s in stats]
    print(json.dumps({"gt": spec, "seed": seed, "inst": inst, "c": nc, "d": d, "near_rank": rk, "rho": rho,
                      "delta": delta, "O(D)": gorder, "triples_min": min(tri), "triples_max": max(tri),
                      "cands_min": min(cn), "cands_med": sorted(cn)[len(cn) // 2], "cands_max": max(cn),
                      "s01": s01, "s12": s12, "s20": s20}))


if __name__ == "__main__":
    main()
