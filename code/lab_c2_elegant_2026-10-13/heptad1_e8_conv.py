"""Lab session, 2026-10-13. Convolution of a 4-dimensional array [m, A, B, tt] with coordinate types (s, t, u):
the same routine as in heptad1_e8.py, in a module without side effects (heptad1_e8.py runs a search when imported)."""
import numpy as np
import heptad1 as H
from jacobi_tables import MMAX


def convolve(P, types, shadow):
    for s, t, u in types:
        Q = np.zeros_like(P)
        vals = [2 * k + 1 for k in range(-4, 4)] if shadow else [2 * k for k in range(-3, 4)]
        for w in vals:
            dm, da, db, dt = w * w, s * w, t * w, u * w
            if dm > MMAX:
                continue
            a0, a1 = max(0, -da), min(H.NA, H.NA - da)
            b0, b1 = max(0, -db), min(H.NA, H.NA - db)
            c0, c1 = max(0, -dt), min(H.NT, H.NT - dt)
            if a0 >= a1 or b0 >= b1 or c0 >= c1:
                continue
            Q[dm:, a0 + da:a1 + da, b0 + db:b1 + db, c0 + dt:c1 + dt] += P[:MMAX + 1 - dm, a0:a1, b0:b1, c0:c1]
        P = Q
    return P
