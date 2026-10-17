"""Can positivity (lambda_2(A_H) <= 3, forced in Conway) be reached at c = 1 with a WELL-CONNECTED G_l?
(exploration, LAB 17/10/2026).  Start: random line type + random completion of H = G_l u Y_x (c1_h46_random.py).
Moves: swaps of one attachment (in L_0 or in L_1) between two far labels {3,s}, {3,t} (the numbers of far labels
attached to each label of L_0 u L_1 are EXACT, so single changes are impossible), keeping every local cap of c1_h46_random.py (checked exactly on the 49-vertex adjacency), minimising
lambda_2(A_H).  Reports the best lambda_2 reached and the Laplacian gap of G_l (unchanged by the moves).
Our c = 1 data (bottlenecked, gap median 0.088) all have lambda_2(A_H) in [2.911, 2.993]; random completions of
generic line types (gap ~0.3) have lambda_2 in [3.18, 3.56].
usage: python c1_h46_descent.py <number of line types> <seed> <sweeps>"""
import itertools
import random
import sys

import numpy as np

sys.argv_saved = list(sys.argv)
N, seed, sweeps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
sys.argv = [sys.argv[0], "0", "0", "15"]
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
import c1_h46_random as R  # noqa: E402  (its main() runs with N = 0: nothing)
sys.argv = sys.argv_saved

X = R.X
OUT = R.OUT


def caps_ok(A, exact_idx):
    A2 = A @ A
    n = len(A)
    iu = np.triu_indices(n, 1)
    cap = np.where(A[iu] == 1, 1, 2)
    c = A2[iu]
    if np.any(c > cap):
        return False
    for i in exact_idx:
        row = A2[i].copy()
        tgt = np.where(A[i] == 1, 1, 2)
        tgt[i] = row[i]
        if np.any(row != tgt):
            return False
    return True


def lam2(A):
    H = A[3:, 3:].astype(float)
    return np.sort(np.linalg.eigvalsh(H))[-2]


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
        G = A[3:39, 3:39]
        gap = np.sort(np.linalg.eigvalsh(3 * np.eye(36) - G))[1]
        cur = lam2(A)
        start = cur
        L0 = [pos[(0, a)] for a in X]
        L1 = [pos[(1, a)] for a in X]
        Yi = [pos[("Y", t)] for t in OUT]
        for sw in range(sweeps):
            improved = False
            # swap moves: y gives an attachment u (in L_r) to y2 which gives back u2 (keeps every exact count)
            for y, y2 in itertools.combinations(Yi, 2):
                for Lr in (L0, L1):
                    au = [u for u in Lr if A[y, u] and not A[y2, u]]
                    bu = [u for u in Lr if A[y2, u] and not A[y, u]]
                    for u in au:
                        for u2 in bu:
                            B = A.copy()
                            B[y, u] = B[u, y] = 0; B[y2, u2] = B[u2, y2] = 0
                            B[y, u2] = B[u2, y] = 1; B[y2, u] = B[u, y2] = 1
                            val = lam2(B)
                            if val < cur - 1e-12 and caps_ok(B, exact_idx):
                                A, cur = B, val
                                improved = True
            if not improved:
                break
        done += 1
        print("type %d: gap(G_l) %.3f  lambda_2(A_H): start %.4f -> best %.4f  (%s)" % (
            done, gap, start, cur, "<= 3" if cur <= 3 + 1e-9 else "> 3"), flush=True)


main()
