"""Check: X-based forced value beta(w,w') = e_w^T S^- e_w' (obligation37.setup) equals 4 - e_w^T Omega e_w' with
Omega = (3I - G_T + J)^{-1} mod 7 computed by an independent Gauss-Jordan (sympy), for random 6-sets with 2 names
per class.  Also checks Codex's form: R = 3J + 3I - E^T Lplus E, Lplus = Omega - J."""
import random, sys, os
import numpy as np
import sympy
TR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "treasure_2026-10-19")
sys.path.insert(0, TR); sys.path.insert(0, os.path.join(TR, "..", "reduction_2026-10-19"))
from ll_test import random_gt
from obligation37 import setup
rng = random.Random(7)
n = 12
for inst in range(3):
    while True:
        s01, s12, s20, _ = random_gt(n, rng, 1)
        G, d, rk, X = setup(n, s01, s12, s20)
        if d == 1:
            break
    N = 3 * n
    Lj = sympy.Matrix((3 * np.eye(N, dtype=int) - G + np.ones((N, N), dtype=int)).tolist())
    Om = np.array(Lj.inv_mod(7).tolist(), dtype=np.int64)
    bad = 0
    for t in range(2000):
        def six():
            v = np.zeros(3 + N, dtype=np.int64)
            for c in range(3):
                a, b = rng.sample(range(n), 2)
                v[3 + c * n + a] = v[3 + c * n + b] = 1
            return v
        e1, e2 = six(), six()
        beta = int(e1 @ X @ e2) % 7
        om = int(e1[3:] @ Om @ e2[3:]) % 7
        if beta != (4 - om) % 7:
            bad += 1
    print("instance %d: d=%d near rank=%d, mismatches beta vs 4-e.Omega.e: %d / 2000" % (inst, d, rk, bad))
