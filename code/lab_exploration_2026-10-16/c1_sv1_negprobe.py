"""Shape of the negative directions met by the SV1 cutting-plane loop (exploration, LAB 17/10/2026).
Solves the current model once, then for the solution prints, for the 3 most negative directions of T_S and U_S (on the
complement of the stars): eigenvalue, participation ratio (1/sum v^4), weight on L01 / m-only / cross labels, and the
labels carrying 80 % of the weight.
usage: python c1_sv1_negprobe.py <cuts.json> <seconds> <seed>"""
import json
import random
import sys

import numpy as np
from ortools.sat.python import cp_model

sys.argv_saved = list(sys.argv)
import c1_sv1_cuts as C  # noqa: E402

cuts = json.load(open(sys.argv_saved[1]))
for k in ("P", "PV", "R", "B2"):
    cuts.setdefault(k, [])
rng = random.Random(int(sys.argv_saved[3]))
m, e, tau = C.build_model(cuts, rng)
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = 2
sv.parameters.max_time_in_seconds = float(sys.argv_saved[2])
st = sv.Solve(m)
print("status", sv.StatusName(st), "tau", sv.Value(tau) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
G = np.zeros((C.n, C.n), dtype=np.int64)
for k, (i, j) in enumerate(C.PAIRS):
    if sv.Value(e[k]):
        G[i, j] = G[j, i] = 1
T = (24 * np.eye(C.n) - 8 * G - C.K8) / 8.0
for name, M in (("T", T), ("U", 7 * C.PiS - T)):
    ev, V = C.perp_eigs(M)
    for k in np.argsort(ev)[:3]:
        v = V[:, k]
        w = v ** 2
        pr = 1.0 / float(np.sum(w ** 2))
        order = np.argsort(-w)
        acc, top = 0.0, []
        for i in order:
            top.append(sorted(C.S[i]))
            acc += w[i]
            if acc > 0.8:
                break
        parts = {"L01": float(sum(w[i] for i in range(C.n) if C.S[i] & {0, 1} and not C.S[i] & {2, 3})),
                 "m": float(sum(w[i] for i in range(C.n) if C.S[i] & {2, 3} and not C.S[i] & {0, 1})),
                 "cross": float(sum(w[i] for i in range(C.n) if C.S[i] & {0, 1} and C.S[i] & {2, 3}))}
        print("%s: lambda %.3f, participation %.1f labels, weights %s, 80%% on %d labels: %s" % (
            name, ev[k], pr, {a: round(b, 2) for a, b in parts.items()}, len(top), top[:12]))
