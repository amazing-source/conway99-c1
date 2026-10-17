"""Parity of the negative directions under iota = (2 3) and under iota_l = (0 1) (exploration, LAB 17/10/2026).
For several solutions of the SV1 model and for the best constrained walk structures: share of the odd part of the
3 most negative directions of T_S (complement of the stars) under the formal swaps of the two points of m and of l.
usage: python c1_sv1_parity.py <cuts.json> <seconds per solve> <solves> [structure.json ...]"""
import json
import random
import sys

import numpy as np
from ortools.sat.python import cp_model

argv = list(sys.argv)
import c1_sv1_cuts as C  # noqa: E402


def swap_perm(a, b):
    sw = {a: b, b: a}
    return np.array([C.IDX[frozenset(sw.get(y, y) for y in l)] for l in C.S])


PM = swap_perm(2, 3)
PL = swap_perm(0, 1)


def report(G, tag):
    T = (24 * np.eye(C.n) - 8 * G - C.K8) / 8.0
    ev, V = C.perp_eigs(T)
    out = []
    for k in np.argsort(ev)[:3]:
        v = V[:, k]
        odd_m = float(np.sum(((v - v[PM]) / 2) ** 2))
        odd_l = float(np.sum(((v - v[PL]) / 2) ** 2))
        out.append("lambda %.3f odd(m) %.2f odd(l) %.2f" % (ev[k], odd_m, odd_l))
    print(tag + ": " + " | ".join(out), flush=True)


cuts = json.load(open(argv[1]))
for k in ("P", "PV", "R", "B2"):
    cuts.setdefault(k, [])
for s in range(int(argv[3])):
    m, e, tau = C.build_model(cuts, random.Random(100 + s))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 2
    sv.parameters.max_time_in_seconds = float(argv[2])
    sv.parameters.random_seed = 100 + s
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        continue
    G = np.zeros((C.n, C.n), dtype=np.int64)
    for k, (i, j) in enumerate(C.PAIRS):
        if sv.Value(e[k]):
            G[i, j] = G[j, i] = 1
    report(G, "model solution %d" % s)
for fn in argv[4:]:
    d = json.load(open(fn))
    lab = [frozenset(x) for x in d["labels"]]
    G = np.zeros((C.n, C.n), dtype=np.int64)
    for i, j in d["edges"]:
        a, b = C.IDX[lab[i]], C.IDX[lab[j]]
        G[a, b] = G[b, a] = 1
    report(G, fn.split("/")[-1])
