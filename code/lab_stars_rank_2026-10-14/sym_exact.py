"""Exact search for rank-30 three-star structures with c(l) = 1 under the swap symmetry a <-> a' (14/10/2026).

By P5 the only letter symmetries compatible with c(l) = 1 swap the mates 0 <-> 1 (a <-> a') and fix 2, 3.  Under such an
involution h, T_S splits into an even block (orbit sums) and an odd block (orbit differences); the star relations are
1_L0 + 1_L1, 1_L2 (even) and 1_L0 - 1_L1 (odd).  A fourth relation makes one block drop rank by one more: an exact
integer determinant of a ~16 x 16 matrix vanishes, a coincidence much more reachable than for the full 31 x 31.
The search walks through h-invariant admissible structures (large-neighbourhood moves on pair orbits, cryptominisat),
computes c(l) exactly and the exact ranks of both blocks, and records every structure with an extra relation.
Modes: rand (plain walk), det (minimise log10 of the smaller reduced block determinant), psd (maximise the smallest
eigenvalue of T and U off the stars).
zero: maximise min(-|lambda_min T even|, lambda_min T odd, U even, U odd) (stars removed): PSD with an
extra relation in the even sector.
usage: python sym_exact.py <cycles> <moves> <seed> <out prefix> [rand|det|psd|zero]
"""
import itertools
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank


def bareiss_det(M):
    A = [list(row) for row in M]
    n = len(A)
    if n == 0:
        return 1
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            p = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if p is None:
                return 0
            A[k], A[p] = A[p], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def reduced_det(B, k):
    """Delete k coordinates so that the rest is nonsingular when B has nullity exactly k; return its determinant."""
    m = len(B)
    r = m - k
    keep = list(range(m))
    for t in range(m - 1, -1, -1):
        if len(keep) == r:
            break
        trial = [i for i in keep if i != t]
        if exact_rank([[B[i][j] for j in trial] for i in trial]) == r:
            keep = trial
    return bareiss_det([[B[i][j] for j in keep] for i in keep])


def main():
    cyc, moves, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else "rand"
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14)), "h must preserve mates"
    assert h[0] == 1 and h[1] == 0 and h[2] == 2 and h[3] == 3, "h must swap 0,1 and fix 2,3"
    rng = random.Random(seed)
    stars = [0, 1, 2]
    S, idx, e, F = build(stars, rng)
    n = len(S)
    hl = {i: idx[frozenset(h[y] for y in S[i])] for i in range(n)}
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    reps, seen = [], set()
    for i, j in itertools.combinations(range(n), 2):
        orb, a, b = [], i, j
        while True:
            p = (min(a, b), max(a, b))
            if p in orb:
                break
            orb.append(p)
            a, b = hl[a], hl[b]
        key = min(orb)
        if key in seen:
            continue
        seen.add(key)
        reps.append(key)
        for p in orb:
            if p != key:
                sol.add_clause([-e[key], e[p]])
                sol.add_clause([e[key], -e[p]])
    orbits, done = [], set()
    for i in range(n):
        if i in done:
            continue
        o = sorted({i, hl[i]})
        done |= set(o)
        orbits.append(o)
    even, odd = [], []
    for o in orbits:
        v = np.zeros(n, dtype=np.int64)
        v[o] = 1
        even.append(v)
        if len(o) == 2:
            w = np.zeros(n, dtype=np.int64)
            w[o[0]], w[o[1]] = 1, -1
            odd.append(w)
    Ev, Od = np.array(even), np.array(odd)
    Ks = np.array([[kval(a, b) for b in S] for a in S])
    K8 = np.rint(8 * Ks).astype(np.int64)
    X = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    D = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for y in l:
            D[y, j] = 1
    Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
    pos = {l: i for i, l in enumerate(LABELS)}
    ix = [pos[l] for l in S]
    PiS = Pi[np.ix_(ix, ix)]
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T

    Pmat = np.zeros((n, n))
    for i in range(n):
        Pmat[hl[i], i] = 1

    def sector_basis(sign):
        Ps = (np.eye(n) + sign * Pmat) / 2
        Q = Pp @ Ps @ Pp
        ev, V = np.linalg.eigh((Q + Q.T) / 2)
        return V[:, ev > 0.5]

    Be, Bo = sector_basis(1), sector_basis(-1)

    def sector_mins(T):
        U = 7 * PiS - T
        return (float(np.linalg.eigvalsh(Be.T @ T @ Be)[0]), float(np.linalg.eigvalsh(Bo.T @ T @ Bo)[0]),
                float(np.linalg.eigvalsh(Be.T @ U @ Be)[0]), float(np.linalg.eigvalsh(Bo.T @ U @ Bo)[0]))

    def perp_min(M):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min())

    def analyse(model):
        G = np.zeros((n, n), dtype=np.int64)
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        BE = (Ev @ M8 @ Ev.T).tolist()
        BO = (Od @ M8 @ Od.T).tolist()
        nE, nO = len(BE) - exact_rank(BE), len(BO) - exact_rank(BO)
        c = 23 - exact_rank([[int(M8[i][j]) for j in X] for i in X])
        return G, M8, BE, BO, nE, nO, c

    ok, model = sol.solve()
    if not ok:
        print("no invariant admissible structure", flush=True)
        return
    t0 = time.time()
    stats = {"c1": 0, "c>1": 0, "psd": 0, "psd_rel": 0, "rel_lt": []}
    found, cur, temp = [], None, 0.5
    sizes = []
    for mv in range(moves):
        Rl = set(rng.sample(range(n), 4))
        assum = []
        for key in reps:
            i, j = key
            if i in Rl or j in Rl or hl[i] in Rl or hl[j] in Rl:
                continue
            v = e[key]
            assum.append(v if model[v] else -v)
        ok2, m2 = sol.solve(assum)
        if not ok2:
            continue
        G, M8, BE, BO, nE, nO, c = analyse(m2)
        stats["c1" if c == 1 else "c>1"] += 1
        T = M8 / 8.0
        sTU = None
        if mode == "zero" and c == 1:
            te, to, ue, uo = sector_mins(T)
            sZ = min(-abs(te), to, ue, uo)
            sTU = min(te, to, ue, uo)
            if sTU > -1e-9:
                stats["psd"] += 1
        if mode == "psd" and c == 1:
            sTU = min(perp_min(T), perp_min(7 * PiS - T))
            if sTU > -1e-9:
                stats["psd"] += 1
        if c == 1 and (nE > 2 or nO > 1):
            if sTU is not None and sTU > -1e-9:
                stats["psd_rel"] += 1
            lt, lu = perp_min(T), perp_min(7 * PiS - T)
            found.append({"move": mv, "null_even": nE, "null_odd": nO, "lambda_T": lt, "lambda_U": lu,
                          "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]})
            json.dump({"labels": [sorted(l) for l in S], "h": cyc, "found": found}, open(out + "_found.json", "w"))
            print("move %d: c=1 and EXTRA RELATION (null even %d, odd %d), lambda_T %.4f, lambda_U %.4f"
                  % (mv, nE, nO, lt, lu), flush=True)
        if mode in ("det", "rand") and c == 1 and nE == 2 and nO == 1 and (mode == "det" or mv % 20 == 0):
            dE, dO = reduced_det(BE, 2), reduced_det(BO, 1)
            sizes.append((math.log10(abs(dE)), math.log10(abs(dO))))
        if mode == "rand":
            model = m2
        else:
            if c != 1:
                s2 = -99.0
            elif mode == "det":
                s2 = -min(sizes[-1]) if (nE == 2 and nO == 1) else 0.0
            elif mode == "zero":
                s2 = sZ
            else:
                s2 = sTU
            if cur is None or s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
                model, cur = m2, s2
            temp = max(0.01, temp * 0.999)
        if mv % 200 == 0:
            msg = ""
            if sizes:
                se = sorted(s[0] for s in sizes)
                so = sorted(s[1] for s in sizes)
                msg = "; log10|reduced det| even median %.1f min %.1f, odd median %.1f min %.1f" % (
                    se[len(se) // 2], se[0], so[len(so) // 2], so[0])
            print("move %d: c=1 %d, c>1 %d, extra relations with c=1: %d (PSD visits %d, PSD with relation %d), "
                  "score %s%s (%.0f s)" % (mv, stats["c1"], stats["c>1"], len(found), stats["psd"], stats["psd_rel"],
                                           "%.3f" % cur if cur is not None else "-", msg, time.time() - t0), flush=True)
    print("end: c=1 %d, c>1 %d, extra relations with c=1: %d, PSD visits %d, PSD with relation %d"
          % (stats["c1"], stats["c>1"], len(found), stats["psd"], stats["psd_rel"]), flush=True)


if __name__ == "__main__":
    main()
