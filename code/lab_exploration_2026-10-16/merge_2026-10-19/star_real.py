"""Real (rank-independent) test of the complete star of a near vertex (LAB 20/10/2026).

Theorem 1 of ../representation_2026-10-19 (P): for every line T and every rank,
    7 Pi_T = 3I - R - [E^T (4I + G) - 2J] K^+ E
is 7 times the orthogonal projector onto the -4 eigenvectors of A carried by the far set; it has rank 7 + c (= 8 for c = 1).
Hence for any set S of far vertices, the block 7 Pi_T[S, S] = 3I - R_S - A_S (4I + G) K^+ A_S^T + 0.2 J is positive
semi-definite with eigenvalues in [0, 7] and rank <= 8.  For the star of x (10 far vertices), the all-ones vector of the
star is in the kernel automatically (it is the projection of E^T e_x), so "rank <= 8" is one real equation beyond it.
This script samples complete star configurations satisfying ONLY the rank-independent combinatorial conditions (L2,
bijections, margins K(x, .), L3, matching with caps 1 - |N_G(x) n W|, NF) and measures how often the real conditions
hold: PSD with eigenvalues <= 7, and rank <= 8 (second smallest eigenvalue 0).
usage: python star_real.py <seed> <x> <samples> [time limit s] [--s1]   (--s1: keep triples with 0 <= 7Pi(W,W) <= 7)"""
import ctypes
import itertools
import json
import os
import random
import sys
import time

import numpy as np

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from star_csp import line_graph, n, N  # noqa: E402
from ll_test import pairs_of  # noqa: E402


def main():
    seed, x, samples = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    limit = float(sys.argv[4]) if len(sys.argv) > 4 else 120.0
    S1 = "--s1" in sys.argv
    gt, G, Om, K, leg = line_graph(seed, -1)
    Kf = K.astype(float)
    Kp = np.linalg.pinv(Kf)
    Q = (4 * np.eye(N) + G) @ Kp
    assert np.allclose(Q, Q.T, atol=1e-9)
    nb = [set(int(z) for z in np.nonzero(G[v])[0]) for v in range(N)]
    xb = x ^ 1
    ys = [y for y in range(n) if y not in (x, xb)]
    P1 = [(n + a, n + b) for a, b in pairs_of(n)]
    P2 = [(2 * n + a, 2 * n + b) for a, b in pairs_of(n)]
    dom = {}
    for y in ys:
        c = []
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
                if any(v > 2 for v in cnt.values()):
                    continue
                if S1:
                    d = 3.2 - Q[np.ix_(W, W)].sum()
                    if d < -1e-9 or d > 7 + 1e-9:
                        continue
                c.append((W, qi, si))
        dom[y] = c
    e_check = np.zeros(N)
    e_check[list(dom[ys[0]][0][0])] = 1
    one_kp = float(np.ones(N) @ Kp @ e_check)
    rng = random.Random(1000 + seed)
    t0 = time.time()
    stats = {"configs": 0, "matchings": 0, "psd_ok": 0, "rank_le_8": 0, "kernel_ones_ok": 0, "min_lam2": None,
             "lam2_quantiles": None}
    lam2s = []
    lam_min = []

    def sample():
        """one random complete configuration of triples (no Green), or None"""
        chosen, usedq, useds, marg = {}, set(), set(), {}
        order = ys[:]
        rng.shuffle(order)

        def rec(i):
            if time.time() - t0 > limit:
                return False
            if i == len(order):
                return True
            y = order[i]
            cand = dom[y][:]
            rng.shuffle(cand)
            for (W, qi, si) in cand[:400]:
                if qi in usedq or si in useds:
                    continue
                if any(marg.get(u, 0) + 1 > K[x, u] for u in W[2:]):
                    continue
                if any(len(set(W) & set(W2)) > 2 for W2 in chosen.values()):
                    continue
                chosen[y] = W
                usedq.add(qi)
                useds.add(si)
                for u in W[2:]:
                    marg[u] = marg.get(u, 0) + 1
                if rec(i + 1):
                    return True
                del chosen[y]
                usedq.discard(qi)
                useds.discard(si)
                for u in W[2:]:
                    marg[u] -= 1
            return False

        return dict(chosen) if rec(0) else None

    while stats["configs"] < samples and time.time() - t0 < limit:
        conf = sample()
        if conf is None:
            break
        stats["configs"] += 1
        Ws = [conf[y] for y in ys]
        A = np.zeros((10, N))
        for i, W in enumerate(Ws):
            A[i, list(W)] = 1
        cap = [1 - len(nb[x] & set(W)) for W in Ws]
        free = [i for i in range(10) if cap[i] == 1]

        def allowed(i, j):
            Wi, Wj = set(Ws[i]), set(Ws[j])
            if Wi & Wj != {x}:
                return False
            for z in Wj - {x}:
                if len(nb[z] & Wi) > 1:
                    return False
            for z in Wi - {x}:
                if len(nb[z] & Wj) > 1:
                    return False
            return True

        def matchings(rest):
            if not rest:
                yield []
                return
            a = rest[0]
            for b in rest[1:]:
                if allowed(a, b):
                    for m in matchings([v for v in rest[1:] if v != b]):
                        yield [(a, b)] + m

        base = 3 * np.eye(10) - A @ Q @ A.T + 0.2 * np.ones((10, 10))
        for m in matchings(free):
            stats["matchings"] += 1
            R = np.zeros((10, 10))
            for a, b in m:
                R[a, b] = R[b, a] = 1
            Pm = base - R
            if np.abs(Pm @ np.ones(10)).max() < 1e-8:
                stats["kernel_ones_ok"] += 1
            ev = np.linalg.eigvalsh(Pm)
            lam_min.append(float(ev[0]))
            if ev[0] > -1e-8 and ev[-1] < 7 + 1e-8:
                stats["psd_ok"] += 1
                lam2s.append(float(ev[1]))
                if ev[1] < 1e-8:
                    stats["rank_le_8"] += 1
    if lam2s:
        a = np.array(lam2s)
        stats["min_lam2"] = round(float(a.min()), 6)
        stats["lam2_quantiles"] = [round(float(q), 4) for q in np.quantile(a, [0.01, 0.1, 0.5])]
    if lam_min:
        a = np.array(lam_min)
        stats["lam_min_quantiles"] = [round(float(q), 3) for q in np.quantile(a, [0.0, 0.1, 0.5, 0.9])]
    print(json.dumps({"seed": seed, "x": x, "tau_leg": leg, "one_Kp_e": round(one_kp, 6),
                      "dom_sizes": [len(dom[y]) for y in ys], **stats,
                      "seconds": round(time.time() - t0, 1)}), flush=True)


if __name__ == "__main__":
    main()
