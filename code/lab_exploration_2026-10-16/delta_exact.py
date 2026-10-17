"""Exact rational delta_a = 8/3 - z_a^T (3I - Gamma_S)^{-1} z_a on a few positive c=1 sides; denominators vs det."""
import itertools, json, sys
from fractions import Fraction
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, relabel, gl_connected
from c1_3adic import solve_frac
from c1_mod3n import bareiss_det
IDX = {l: i for i, l in enumerate(S)}
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=float)
done = 0
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    for side in (0, 1):
        L, EE = relabel(S0, E0, side)
        conn, degok = gl_connected(EE)
        if not (conn and degok):
            continue
        G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
        Gn = np.array(G, float)
        if np.linalg.eigvalsh(3 * np.eye(44) - Gn - K8 / 8)[0] < -1e-9:
            continue
        X = [[(3 if i == j else 0) - G[i][j] for j in range(44)] for i in range(44)]
        det = bareiss_det(X)
        if det == 0:
            continue
        Z = [[1 if (frozenset((r, a)) == S[i]) else 0 for a in range(4, 14) for r in range(4)] for i in range(44)]
        cols = [[1 if a in S[i] else 0 for a in range(4, 14)] for i in range(44)]
        Y = solve_frac(X, cols)
        out = []
        for k, a in enumerate(range(4, 14)):
            za = [cols[i][k] for i in range(44)]
            v = sum(za[i] * Y[i][k] for i in range(44))
            out.append(Fraction(8, 3) - v)
        print("det(3I-Gamma_S) =", det, "factor-ish:", [abs(det) % p == 0 for p in (2, 3, 5, 7, 11, 13)])
        print("   delta_a:", [str(x) for x in out[:4]], "...")
        print("   delta_a * det:", [x * det for x in out[:4]])
        done += 1
    if done >= int(sys.argv[2]):
        break
