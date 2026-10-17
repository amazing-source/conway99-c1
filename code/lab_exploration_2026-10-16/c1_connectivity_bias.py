"""Bias check (exploration, LAB 17/10/2026): algebraic connectivity of G_l (Laplacian gap of the cubic graph on the 36
neighbours of l) for (i) the c = 1 sides of our data, (ii) uniformly random line types (mu_0, mu_1, sigma) passing the
local axioms (c1_linetypes_sample.py).  Literature: random cubic graphs are connected/Hamiltonian a.a.s. (Robinson-
Wormald) and near-Ramanujan (Friedman: lambda_2(A) <= 2 sqrt 2 + eps, i.e. Laplacian gap >= 3 - 2.83 = 0.17).
usage: python c1_connectivity_bias.py <distinct cache.jsonl> <random samples> <seed>"""
import json
import random
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from gg_test import orient, line_graph, components  # noqa: E402
# functions copied from c1_linetypes_sample.py (that file runs its sampling at import)
import itertools  # noqa: E402
MATE = lambda i: i ^ 1
LET = list(range(2, 14))
def rand_matching(rng):
    p = LET[:]; rng.shuffle(p)
    m = {}
    for i in range(0, 12, 2):
        m[p[i]], m[p[i + 1]] = p[i + 1], p[i]
    return m
def build(mu0, mu1, sig):
    labs = [frozenset((0, a)) for a in LET] + [frozenset((1, a)) for a in LET]
    idx = {l: i for i, l in enumerate(labs)}
    G = np.zeros((24, 24), dtype=int)
    for a in LET:
        G[idx[frozenset((0, a))], idx[frozenset((0, mu0[a]))]] = 1
        G[idx[frozenset((1, a))], idx[frozenset((1, mu1[a]))]] = 1
        i, j = idx[frozenset((0, a))], idx[frozenset((1, sig[a]))]
        G[i, j] = G[j, i] = 1
    return labs, idx, G
def axioms(labs, G):
    # letter counts
    for i, u in enumerate(labs):
        for y in range(14):
            cnt = sum(G[i, j] for j, w in enumerate(labs) if y in w and j != i)
            c = 1 if (y in u or MATE(y) in u) else 2
            if y in (0, 1):
                if cnt != c: return False
            elif cnt > c: return False
    # pair caps
    G2 = G @ G
    for i, j in itertools.combinations(range(24), 2):
        if G2[i, j] + len(labs[i] & labs[j]) + G[i, j] > 2: return False
    return True
def connected(mu0, mu1, sig):
    adj = {a: {MATE(a), mu0[a], mu1[a], sig[a]} | {b for b in LET if sig[b] == a} for a in LET}
    seen, st = {2}, [2]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == 12

class LT:
    LET = LET
    rand_matching = staticmethod(rand_matching)
    build = staticmethod(build)
    axioms = staticmethod(axioms)
    connected = staticmethod(connected)


def gap(A):
    L = 3 * np.eye(len(A)) - np.array(A, dtype=float)
    ev = np.sort(np.linalg.eigvalsh(L))
    return ev[1]


def from_type(mu0, mu1, sig):
    X = list(range(2, 14))
    V = [("L", a) for a in X] + [(0, a) for a in X] + [(1, a) for a in X]
    pos = {x: i for i, x in enumerate(V)}
    A = np.zeros((36, 36))
    for a in X:
        A[pos[("L", a)], pos[("L", a ^ 1)]] = 1
        for r in (0, 1):
            A[pos[("L", a)], pos[(r, a)]] = A[pos[(r, a)], pos[("L", a)]] = 1
        A[pos[(0, a)], pos[(0, mu0[a])]] = 1
        A[pos[(1, a)], pos[(1, mu1[a])]] = 1
        A[pos[(0, a)], pos[(1, sig[a])]] = A[pos[(1, sig[a])], pos[(0, a)]] = 1
    return A


def main():
    cache, ns, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    data = []
    for line in open(cache):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        for side in (0, 1):
            L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
            V, pos, A = line_graph(L, E)
            if any(sum(r) != 3 for r in A) or components(A) != 1:
                continue
            data.append(gap(A))
    rng = random.Random(seed)
    rnd = []
    tries = 0
    while len(rnd) < ns and tries < 50 * ns:
        tries += 1
        mu0, mu1 = LT.rand_matching(rng), LT.rand_matching(rng)
        perm = LT.LET[:]
        rng.shuffle(perm)
        sig = dict(zip(LT.LET, perm))
        labs, idx, G = LT.build(mu0, mu1, sig)
        if not LT.axioms(labs, G) or not LT.connected(mu0, mu1, sig):
            continue
        rnd.append(gap(from_type(mu0, mu1, sig)))
    q = lambda xs, p: float(np.quantile(xs, p))
    for name, xs in (("data c = 1 sides", data), ("random line types (axioms, c = 1)", rnd)):
        xs = np.array(xs)
        print("%-36s n = %5d  gap: min %.3f  q10 %.3f  median %.3f  q90 %.3f  max %.3f  share < 0.17: %.3f" % (
            name, len(xs), xs.min(), q(xs, .1), q(xs, .5), q(xs, .9), xs.max(), float(np.mean(xs < 0.17))))


main()
