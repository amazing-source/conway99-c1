"""Falsification attempt for H46-c1 with UNBIASED starts (exploration, LAB 17/10/2026).
W = N[l] u Y_x (49 vertices: line l = {v,0,1}, its 36 neighbours, the 10 far neighbours of the letter x = 3).
Conway needs: lambda_2(A_W) <= 3 (interlacing) AND nullity(A_W - 3I) >= 49 - 45 = 4 (2 universal vectors + 2 more,
i.e. an eigenvector of H = W - l vanishing on l).  For c(l) = 1 our biased data never reach nullity 4.
Here: random generic line type (local axioms, c = 1), random completion (c1_h46_random.py), descent by attachment
swaps to lambda_2(A_W) <= 3, then a random walk inside {lambda_2 <= 3} with the same swap moves (all local caps kept),
computing the exact nullity of A_W - 3I (rank modulo two primes near 2^31) at every visited structure.
Output: per line type the gap of G_l, the number of positive structures visited, the nullity histogram; any structure
with nullity >= 4 is saved (it would be a c = 1 local configuration passing H46).
usage: python c1_h46_boundary.py <line types> <seed> <walk steps per type>"""
import itertools
import json
import random
import sys
from collections import Counter

import numpy as np

saved_argv = list(sys.argv)
N, seed, steps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
sys.argv = [sys.argv[0], "0", "0", "15"]
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
import c1_h46_random as R  # noqa: E402
from c1_h46_descent import caps_ok  # noqa: E402
sys.argv = saved_argv
PRIMES = (2147483647, 2147483629)


def rank_mod(M, p):
    M = (M % p).astype(np.int64)
    n, m = M.shape
    r = 0
    for c in range(m):
        piv = None
        for i in range(r, n):
            if M[i, c] % p:
                piv = i
                break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        for i in range(n):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
    return r


def nullity3(A):
    M = A.astype(np.int64) - 3 * np.eye(len(A), dtype=np.int64)
    return len(A) - max(rank_mod(M, p) for p in PRIMES)


def lam2(A):
    return np.sort(np.linalg.eigvalsh(A.astype(float)))[-2]


def swaps(A, Yi, L0, L1, rng):
    y, y2 = rng.sample(Yi, 2)
    Lr = L0 if rng.random() < 0.5 else L1
    au = [u for u in Lr if A[y, u] and not A[y2, u]]
    bu = [u for u in Lr if A[y2, u] and not A[y, u]]
    if not au or not bu:
        return None
    u, u2 = rng.choice(au), rng.choice(bu)
    B = A.copy()
    B[y, u] = B[u, y] = 0; B[y2, u2] = B[u2, y2] = 0
    B[y, u2] = B[u2, y] = 1; B[y2, u] = B[u, y2] = 1
    return B


def main():
    rng = random.Random(seed)
    done = 0
    while done < N:
        mu0, mu1, sig = R.rand_type(rng)
        if not R.axioms_ok(mu0, mu1, sig):
            continue
        A = R.complete(mu0, mu1, sig, rng)
        if isinstance(A, str) or A is None:
            continue
        A = A.astype(int)
        V, pos, _ = R.base_graph(mu0, mu1, sig)
        exact_idx = [pos["v"], pos["p0"], pos["p1"], pos[("L", R.XH)]]
        Yi = [pos[("Y", t)] for t in R.OUT]
        L0 = [pos[(0, a)] for a in R.X]
        L1 = [pos[(1, a)] for a in R.X]
        G = A[3:39, 3:39]
        gap = np.sort(np.linalg.eigvalsh(3 * np.eye(36) - G))[1]
        cur = lam2(A)
        # descent to positivity
        for _ in range(4000):
            if cur <= 3 + 1e-9:
                break
            B = swaps(A, Yi, L0, L1, rng)
            if B is None:
                continue
            val = lam2(B)
            if val < cur and caps_ok(B, exact_idx):
                A, cur = B, val
        if cur > 3 + 1e-9:
            done += 1
            print("type %d: gap %.3f  positivity not reached (lambda_2 %.4f)" % (done, gap, cur), flush=True)
            continue
        hist = Counter()
        visited = 0
        best_l2 = cur
        for _ in range(steps):
            B = swaps(A, Yi, L0, L1, rng)
            if B is None:
                continue
            val = lam2(B)
            if val > 3 + 1e-9 or not caps_ok(B, exact_idx):
                continue
            A, cur = B, val
            visited += 1
            nu = nullity3(A)
            hist[nu] += 1
            best_l2 = max(best_l2, cur)
            if nu >= 4:
                fn = "c1_h46_boundary_hit_seed%d_type%d.json" % (seed, done + 1)
                json.dump({"adjacency": A.tolist(), "names": [str(x) for x in V]}, open(fn, "w"))
                print("   HIT nullity %d saved %s" % (nu, fn), flush=True)
        done += 1
        print("type %d: gap %.3f  positive structures visited %d  nullity histogram %s  max lambda_2 seen %.4f" % (
            done, gap, visited, dict(sorted(hist.items())), best_l2), flush=True)


main()
