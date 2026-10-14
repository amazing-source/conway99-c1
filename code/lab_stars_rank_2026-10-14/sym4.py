"""Four-star structures (lines l = {v,0,1}, m = {v,2,3}) under an involution h, towards H4' (14/10/2026).

H4' (open): no admissible four-star structure with c(l) = c(m) = 1 is PSD (T and U) with rank <= 30. If H4' holds,
every vertex of a Conway graph has at most one non-special line, hence (B). In a Conway graph the 44 x 44 matrix T_S4
has nullity >= 14 (interlacing), i.e. 10 mixed relations beyond the four stars when both lines are non-special.
This script walks through h-invariant admissible structures (h must not fix 0,1,2 while moving letters, by P5) and
records, for c(l) = c(m) = 1, the exact nullity of T_S4 (sector by sector), and positivity.
Modes: rand (plain walk), psd (maximise the smallest eigenvalue of T and U off the stars), null (maximise the number
of exactly vanishing sector eigenvalues found so far, then positivity).
usage: python sym4.py <cycles> <moves> <seed> <out prefix> [rand|psd]
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


def main():
    cyc, moves, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else "rand"
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14)), "h must preserve mates"
    assert set(h[i] for i in range(4)) == {0, 1, 2, 3}, "h must preserve the four stars"
    rng = random.Random(seed)
    stars = [0, 1, 2, 3]
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
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    Xl = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    Xm = [i for i in range(n) if 2 in S[i] or 3 in S[i]]
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

    def perp_min(M):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min())

    ok, model = sol.solve()
    if not ok:
        print("no invariant admissible structure", flush=True)
        return
    t0 = time.time()
    hist = {}
    best_null, best_rec = -1, None
    cur, temp = None, 0.5
    npsd = 0
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
        G = np.zeros((n, n), dtype=np.int64)
        for (i, j), v in e.items():
            if i < j and m2[v]:
                G[i, j] = G[j, i] = 1
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        cl = 23 - exact_rank([[int(M8[i][j]) for j in Xl] for i in Xl])
        cm = 23 - exact_rank([[int(M8[i][j]) for j in Xm] for i in Xm])
        T = M8 / 8.0
        s = min(perp_min(T), perp_min(7 * PiS - T))
        if s > -1e-9:
            npsd += 1
        if cl == 1 and cm == 1:
            BE, BO = (Ev @ M8 @ Ev.T).tolist(), (Od @ M8 @ Od.T).tolist()
            nul = (len(BE) - exact_rank(BE)) + (len(BO) - exact_rank(BO))
            hist[nul] = hist.get(nul, 0) + 1
            if nul > best_null or (nul == best_null and s > best_rec["score"]):
                best_null = nul
                best_rec = {"move": mv, "nullity": nul, "score": s,
                            "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]}
                json.dump({"labels": [sorted(l) for l in S], "h": cyc, "best": best_rec}, open(out + "_best.json", "w"))
            if nul >= 14 and s > -1e-9:
                print("move %d: c(l)=c(m)=1, NULLITY %d AND T, U >= 0: H4' REFUTED" % (mv, nul), flush=True)
                json.dump({"labels": [sorted(l) for l in S], "h": cyc, "refutation": best_rec},
                          open(out + "_refute.json", "w"))
                return
        if mode == "rand":
            model = m2
        else:
            s2 = s if (cl == 1 and cm == 1) else s - 1.0
            if cur is None or s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
                model, cur = m2, s2
            temp = max(0.01, temp * 0.999)
        if mv % 200 == 0:
            print("move %d: nullity histogram (c(l)=c(m)=1) %s, PSD visits %d, best nullity %d, score %s (%.0f s)"
                  % (mv, dict(sorted(hist.items())), npsd, best_null, "%.3f" % cur if cur is not None else "-",
                     time.time() - t0), flush=True)
    print("end: nullity histogram %s, PSD visits %d" % (dict(sorted(hist.items())), npsd), flush=True)


if __name__ == "__main__":
    main()
