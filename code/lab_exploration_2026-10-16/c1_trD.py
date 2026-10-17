"""Positive blocks: D <= 0, so nu = 14 <=> tr(D_OO) = 0 <=> Phi = sum_a z_a^T R z_a = 80/3.  Measure -tr(D_OO)."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, gl_connected
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
Bm = np.array([[1.0 if r in l else 0.0 for l in S] for r in range(14)])
Cp = np.array([[3.0 * (i == j) - (1.0 if j == (i ^ 1) else 0.0) - 1.0 / 3 for j in range(14)] for i in range(14)])
rows = []
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
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
        T = (24 * np.eye(44) - 8 * G - K8) / 8
        if np.linalg.eigvalsh(T)[0] < -1e-9:
            continue
        X = 3 * np.eye(44) - G
        ev = np.linalg.eigvalsh(X)
        if np.min(np.abs(ev)) < 1e-9:
            continue
        R = np.linalg.inv(X)
        D = Bm @ R @ Bm.T - Cp
        DO = D[4:, 4:]
        nu = 44 - rank_mod((24 * np.eye(44, dtype=np.int64) - 8 * G.astype(np.int64) - K8).tolist(), 1000000007)
        e = np.linalg.eigvalsh(DO)
        rows.append((nu, -np.trace(DO), e.max(), e[np.abs(e) > 1e-7].max() if np.any(np.abs(e) > 1e-7) else 0))
        done += 1
    if done >= int(sys.argv[2]):
        break
rows.sort()
tab = Counter((r[0]) for r in rows)
print("positive c=1 sides with 3 not in spec:", len(rows), dict(tab))
for nu in sorted(tab):
    sel = [r for r in rows if r[0] == nu]
    print("nu %d: -tr(D_OO) min %.4f median %.4f ; max eigenvalue of D_OO %.2e ; largest nonzero eigenvalue (closest to 0) %.4f" % (
        nu, min(r[1] for r in sel), np.median([r[1] for r in sel]), max(r[2] for r in sel), max(r[3] for r in sel)))
