"""Does any admissible star structure make T_S positive semidefinite?  Cutting planes, 14/10/2026.

T_S = 3I - Gamma_S - K_S (stars_rank.py). For any vector c on S, c^T T_S c >= 0 is LINEAR in the edge variables of
Gamma_S:  sum_{i<j} 2 c_i c_j x_ij <= 3|c|^2 - c^T K_S c.  So: MILP over admissible structures ((C1) exact star counts,
(C2) caps linearised with continuous products p_ijt >= x_it + x_jt - 1, sum_t p_ijt <= 2 - |l_i n l_j| - x_ij), solve,
take the eigenvectors of the negative eigenvalues of T_S at the solution, add their cuts, repeat. Ends with either a PSD
admissible structure (saved) or an infeasible MILP (then no admissible structure on S has T_S >= 0: to be certified
exactly before any claim). The cuts are valid for every c, so numerical error in c only weakens nothing; a tolerance
of 1e-7 is added to the right-hand side.
usage: python psd_cuts.py <stars> <max iterations> <seconds per MILP> <out prefix>
"""
import itertools
import json
import sys
import time

import numpy as np
from scipy.optimize import LinearConstraint, Bounds, milp
from scipy.sparse import lil_matrix, csr_matrix, vstack

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from stars_rank import LABELS, kval, count_needed


def main():
    stars = [int(t) for t in sys.argv[1].split(",")]
    iters, secs, out = int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    S = [l for l in LABELS if any(y in l for y in stars)]
    n = len(S)
    pairs = list(itertools.combinations(range(n), 2))
    pid = {p: k for k, p in enumerate(pairs)}
    def X(i, j):
        return pid[(i, j) if i < j else (j, i)]
    nx = len(pairs)
    thirds = {p: [t for t in range(n) if t not in p] for p in pairs}
    poff = {}
    nv = nx
    for p in pairs:
        poff[p] = nv
        nv += len(thirds[p])
    Ks = np.array([[kval(a, b) for b in S] for a in S])
    rows, lo, hi = [], [], []
    A = lil_matrix((0, nv))
    blocks = []
    # (C1)
    C1 = lil_matrix((n * len(stars), nv))
    r = 0
    for i, l in enumerate(S):
        for y in stars:
            for t in range(n):
                if t != i and y in S[t]:
                    C1[r, X(i, t)] = 1
            lo.append(count_needed(l, y)); hi.append(count_needed(l, y)); r += 1
    blocks.append(C1.tocsr())
    # (C2) products and caps
    nprod = nv - nx
    P = lil_matrix((nprod, nv))
    r = 0
    for p in pairs:
        i, j = p
        for k, t in enumerate(thirds[p]):
            P[r, poff[p] + k] = 1
            P[r, X(i, t)] = -1
            P[r, X(j, t)] = -1
            lo.append(-1); hi.append(np.inf); r += 1
    blocks.append(P.tocsr())
    Cap = lil_matrix((nx, nv))
    for r, p in enumerate(pairs):
        i, j = p
        for k in range(len(thirds[p])):
            Cap[r, poff[p] + k] = 1
        Cap[r, X(i, j)] = 1
        lo.append(-np.inf); hi.append(2 - len(S[i] & S[j]))
    blocks.append(Cap.tocsr())
    base = vstack(blocks).tocsr()
    base_lo, base_hi = np.array(lo, float), np.array(hi, float)
    integrality = np.concatenate([np.ones(nx), np.zeros(nv - nx)])
    bounds = Bounds(np.zeros(nv), np.ones(nv))
    cuts, cut_hi = [], []
    rng = np.random.default_rng(0)
    t0 = time.time()
    for it in range(iters):
        cons = [LinearConstraint(base, base_lo, base_hi)]
        if cuts:
            cons.append(LinearConstraint(csr_matrix(np.array(cuts)), -np.inf, np.array(cut_hi)))
        obj = np.concatenate([rng.normal(size=nx) * 0.01, np.zeros(nv - nx)])
        res = milp(obj, constraints=cons, integrality=integrality, bounds=bounds,
                   options={"time_limit": secs, "disp": False})
        if res.x is None:
            print("iteration %d: MILP %s (status %d) after %d cuts, %.0f s" % (it, res.message, res.status, len(cuts),
                                                                                time.time() - t0), flush=True)
            json.dump({"stars": stars, "cuts": len(cuts), "status": int(res.status), "message": res.message},
                      open(out + "_end.json", "w"))
            return
        x = np.round(res.x[:nx]).astype(int)
        G = np.zeros((n, n))
        for (i, j), k in pid.items():
            G[i, j] = G[j, i] = x[k]
        T = 3 * np.eye(n) - G - Ks
        ev, V = np.linalg.eigh(T)
        neg = [k for k in range(n) if ev[k] < -1e-7]
        print("iteration %d: lambda_min %.5f, %d negative, lambda_max %.4f, cuts %d (%.0f s)"
              % (it, ev[0], len(neg), ev[-1], len(cuts), time.time() - t0), flush=True)
        if not neg and ev[-1] <= 7 + 1e-9:
            json.dump({"stars": stars, "labels": [sorted(l) for l in S], "edges": [list(p) for p, k in pid.items() if x[k]],
                       "eigenvalues": ev.tolist()}, open(out + "_psd.json", "w"))
            print("PSD admissible structure found and saved", flush=True)
            return
        for k in neg[:6]:
            c = V[:, k]
            row = np.zeros(nv)
            for (i, j), q in pid.items():
                row[q] = 2 * c[i] * c[j]
            cuts.append(row)
            cut_hi.append(3 * c @ c - c @ Ks @ c + 1e-7)
    print("no decision after %d iterations" % iters, flush=True)


if __name__ == "__main__":
    main()
