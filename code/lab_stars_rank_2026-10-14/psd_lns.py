"""Large-neighbourhood search for an admissible star structure maximising lambda_perp(T_S) (14/10/2026).

State = admissible structure on S (stars_rank.build constraints). Move: pick r random labels, keep every pair not
touching them fixed (SAT assumptions), let cryptominisat (random polarity) re-complete the pairs touching them; score =
smallest eigenvalue of T_S off the star directions. Simulated annealing on the score. Saves the best structure.
usage: python psd_lns.py <stars> <moves> <r> <seed> <out prefix> [zero|psd|lowrankK] [T0] [decay]
lowrankK: score = -(sum of the K smallest |eigenvalues| of T_S), i.e. push the rank down to |S| - K (PSD ignored).
With "zero": the score is -|lambda_perp| (target: T_S >= 0 with an extra kernel vector, i.e. rank T_S <= 30 at three
stars); success = |lambda_perp| < 1e-9, then the rank is recomputed exactly.
"""
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval


def main():
    stars = [int(t) for t in sys.argv[1].split(",")]
    moves, r, seed, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    zero = len(sys.argv) > 6 and sys.argv[6] == "zero"
    lowrank = int(sys.argv[6][7:]) if len(sys.argv) > 6 and sys.argv[6].startswith("lowrank") else 0
    T0 = float(sys.argv[7]) if len(sys.argv) > 7 else 0.05
    decay = float(sys.argv[8]) if len(sys.argv) > 8 else 0.9995
    rng = random.Random(seed)
    S, idx, e, F = build(stars, rng)
    n = len(S)
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    import os
    sq = os.environ.get("FORCE_SQUARE")         # "grid" or "twisted": impose a closed square on the cross labels
    if sq:
        X4 = [idx[frozenset(p)] for p in [(0, 2), (0, 3), (1, 2), (1, 3)]]
        pairs4 = [(0, 1), (2, 3), (0, 2), (1, 3)] if sq == "grid" else [(0, 1), (2, 3), (0, 3), (1, 2)]
        for a_, b_ in pairs4:
            sol.add_clause([e[(X4[a_], X4[b_])]])
    def force_partition(centre, Mset):
        cs = set(centre)
        for i in range(n):
            for j in range(i + 1, n):
                li, lj = S[i], S[j]
                if not (li & cs) or not (lj & cs):
                    continue
                xi = [y for y in li if y not in cs]
                xj = [y for y in lj if y not in cs]
                if len(xi) != 1 or len(xj) != 1:
                    continue
                if (xi[0] in Mset) != (xj[0] in Mset):
                    sol.add_clause([-e[(i, j)]])
    part = os.environ.get("PARTITION")          # e.g. "4,5,6,7": letters of M; forces Q(v,l) to split along M
    if part:
        force_partition((0, 1), set(int(t) for t in part.split(",")))
    part_m = os.environ.get("PARTITION_M")      # same for the line m = {2,3}
    if part_m:
        force_partition((2, 3), set(int(t) for t in part_m.split(",")))
    Ks = np.array([[kval(a, b) for b in S] for a in S])
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]

    def score(model):
        G = np.zeros((n, n))
        for i, j in pairs:
            if model[e[(i, j)]]:
                G[i, j] = G[j, i] = 1
        ev, V = np.linalg.eigh(Pp @ (3 * np.eye(n) - G - Ks) @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        lam = float(ev[keep].min())
        if lowrank:
            full = np.sort(np.abs(np.linalg.eigvalsh(3 * np.eye(n) - G - Ks)))
            return -float(full[:lowrank].sum()), G
        return (-abs(lam) if zero else lam), G

    ok, model = sol.solve()
    cur, G = score(model)
    best, bestG = cur, G
    temp = T0
    t0 = time.time()
    for mv in range(moves):
        R = set(rng.sample(range(n), r))
        assum = []
        for i, j in pairs:
            if i in R or j in R:
                continue
            v = e[(i, j)]
            assum.append(v if model[v] else -v)
        ok2, m2 = sol.solve(assum)
        if not ok2:
            continue
        s2, G2 = score(m2)
        if s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
            model, cur = m2, s2
            if s2 > best:
                best, bestG = s2, G2
                json.dump({"stars": stars, "labels": [sorted(l) for l in S], "gamma": bestG.astype(int).tolist(),
                           "lambda_perp": best}, open(out + "_best.json", "w"))
                if (zero or lowrank) and best > -1e-9 or (not zero and not lowrank and best >= -1e-9):
                    print("move %d: target reached, score %.3e" % (mv, best), flush=True)
                    return
        temp = max(0.002, temp * decay)
        if mv % 200 == 0:
            print("move %d: current %.4f, best %.4f, temperature %.4f (%.0f s)" % (mv, cur, best, temp, time.time() - t0),
                  flush=True)
    print("end: best lambda_perp %.5f" % best, flush=True)


if __name__ == "__main__":
    main()
