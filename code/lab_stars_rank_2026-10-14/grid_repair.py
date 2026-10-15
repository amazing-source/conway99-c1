"""Grid repair (15/10/2026, LAB): take a saved four-star structure, impose the straight grid on (l, m) (closed square
ab ~ ab', a'b ~ a'b', ab ~ a'b, ab' ~ a'b' on C4), keep every pair that does not touch a free set F of labels (C4 plus
r random labels, r growing until the SAT model is satisfiable), and report min(lambda_T, lambda_U) of the repaired
structure; the best of many repairs is saved as a warm start for sym4g.py (INIT=..., FORCE_GRID_L=2).
usage: python grid_repair.py <json> <tries> <seed> <out json> [rmin rmax]"""
import json
import random
import sys

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS


def main():
    src, tries, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    S, idx, e, F = build([0, 1, 2, 3], rng)
    n = len(S)
    d = json.load(open(src))
    assert [sorted(l) for l in S] == d["labels"]
    E0 = {tuple(x) for x in d["edges"]}
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    c4 = [idx[frozenset(p)] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
    for (p, q) in ((c4[0], c4[1]), (c4[2], c4[3]), (c4[0], c4[2]), (c4[1], c4[3])):
        sol.add_clause([e[(p, q)]])
    K = np.array([[kval(a, b) for b in S] for a in S])
    D = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for y in l:
            D[y, j] = 1
    Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
    pos = {l: i for i, l in enumerate(LABELS)}
    PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T

    def perp_min(M):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min())

    best = None
    for t in range(tries):
        r = rng.randint(int(sys.argv[5]) if len(sys.argv) > 5 else 2, int(sys.argv[6]) if len(sys.argv) > 6 else 12)
        free = set(c4) | set(rng.sample(range(n), r))
        assum = []
        for i in range(n):
            for j in range(i + 1, n):
                if i in free or j in free:
                    continue
                v = e[(i, j)]
                assum.append(v if (i, j) in E0 else -v)
        ok, model = sol.solve(assum)
        if not ok:
            continue
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - K
        lt, lu = perp_min(T), perp_min(7 * PiS - T)
        sc = min(lt, lu)
        if best is None or sc > best[0]:
            best = (sc, lt, lu, r, [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]])
            print("try %d (free %d): lambda_T %.4f lambda_U %.4f" % (t, len(free), lt, lu), flush=True)
            json.dump({"labels": d["labels"], "edges": best[4], "lambda_T": lt, "lambda_U": lu, "source": src},
                      open(out, "w"))
    if best is None:
        print("no repair found")
        return
    json.dump({"labels": d["labels"], "edges": best[4], "lambda_T": best[1], "lambda_U": best[2],
               "source": src}, open(out, "w"))
    print("best repaired structure: min(lambda) %.4f saved to %s" % (best[0], out))


if __name__ == "__main__":
    main()
