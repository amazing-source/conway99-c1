"""Unbiased test of H46 at c = 1 (exploration, LAB 17/10/2026).
Our c = 1 data are bottlenecked (Laplacian gap of G_l: median 0.088, 93 % below 0.17), while uniformly random line types
passing the local axioms have median gap 0.31 (c1_connectivity_bias.py).  Here: random line type (mu_0, mu_1, sigma),
then a random completion of H = G_l u Y_x (x = letter 3, Y_x = its 10 far neighbours {3,s}) by CP-SAT with a random
objective, under NECESSARY local conditions only:
  - each far label {3,s} is adjacent to the letters 3 and s, to exactly 2 labels of L_0 and 2 of L_1 (its common
    neighbours with the points 0 and 1), and these two are not mu-paired;
  - x = 3 has all its 14 neighbours in v u N(l) u Y_x: its neighbourhood is a perfect matching (lambda = 1, exact);
  - caps for every pair of vertices of l u G_l u Y_x: common neighbours inside <= lambda / mu; EXACT for the pairs
    (x, w) and (p, w) with p a point of l (all neighbours of x and of p are inside).
Then lambda_2(A_H) (Conway needs exactly 3) and the Laplacian gap of G_l.  Same statistic on the data for comparison is
in EXPLORATION.md (2.911 .. 2.993).
usage: python c1_h46_random.py <number of line types> <seed> [seconds per solve]"""
import itertools
import random
import sys

import numpy as np
from ortools.sat.python import cp_model

N, seed = int(sys.argv[1]), int(sys.argv[2])
secs = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
X = list(range(2, 14))
MATE = lambda a: a ^ 1
XH = 3                                                   # hub letter (a point of m = {v,2,3})
OUT = [s for s in X if s not in (2, 3)]                  # outer letters: Y_x = {3,s}


def rand_type(rng):
    def rm():
        p = X[:]
        rng.shuffle(p)
        mm = {}
        for i in range(0, 12, 2):
            mm[p[i]], mm[p[i + 1]] = p[i + 1], p[i]
        return mm
    mu0, mu1 = rm(), rm()
    perm = X[:]
    rng.shuffle(perm)
    return mu0, mu1, dict(zip(X, perm))


def base_graph(mu0, mu1, sig):
    """vertices: points v,0,1 ; letters ; L_0 ; L_1 ; Y (10).  Returns names, fixed adjacency (np) for the first 39."""
    V = ["v", "p0", "p1"] + [("L", a) for a in X] + [(0, a) for a in X] + [(1, a) for a in X] + [("Y", s) for s in OUT]
    pos = {x: i for i, x in enumerate(V)}
    n = len(V)
    A = np.zeros((n, n), dtype=int)
    def e(a, b):
        A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    e("v", "p0"); e("v", "p1"); e("p0", "p1")
    for a in X:
        e("v", ("L", a)); e("p0", (0, a)); e("p1", (1, a))
        if a < MATE(a):
            e(("L", a), ("L", MATE(a)))
        e(("L", a), (0, a)); e(("L", a), (1, a))
        if a < mu0[a]:
            e((0, a), (0, mu0[a]))
        if a < mu1[a]:
            e((1, a), (1, mu1[a]))
        e((0, a), (1, sig[a]))
    for s in OUT:
        e(("Y", s), ("L", XH)); e(("Y", s), ("L", s))
    return V, pos, A


def axioms_ok(mu0, mu1, sig):
    V, pos, A = base_graph(mu0, mu1, sig)
    B = A[:39, :39]
    B2 = B @ B
    for i, j in itertools.combinations(range(39), 2):
        cap = 1 if B[i, j] else 2
        if B2[i, j] > cap:
            return False
    # connectivity of G_l (indices 3..38)
    G = B[3:, 3:]
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for w in np.nonzero(G[u])[0]:
            if w not in seen:
                seen.add(int(w)); st.append(int(w))
    return len(seen) == 36 and all(G.sum(1) == 3)


def complete(mu0, mu1, sig, rng):
    V, pos, A0 = base_graph(mu0, mu1, sig)
    n = len(V)
    m = cp_model.CpModel()
    var = {}
    Yv = [pos[("Y", s)] for s in OUT]
    L0 = [pos[(0, a)] for a in X]
    L1 = [pos[(1, a)] for a in X]
    for y in Yv:
        for u in L0 + L1:
            var[(y, u)] = var[(u, y)] = m.NewBoolVar("")
    for y, y2 in itertools.combinations(Yv, 2):
        var[(y, y2)] = var[(y2, y)] = m.NewBoolVar("")
    def adj(i, j):
        if i == j:
            return 0
        if (i, j) in var:
            return var[(i, j)]
        return int(A0[i, j])
    for y in Yv:
        m.Add(sum(var[(y, u)] for u in L0) == 2)
        m.Add(sum(var[(y, u)] for u in L1) == 2)
    def AND(p, q):
        if isinstance(p, int) or isinstance(q, int):
            if isinstance(p, int) and isinstance(q, int):
                return p * q
            return (q if p else 0) if isinstance(p, int) else (p if q else 0)
        z = m.NewBoolVar("")
        m.AddBoolOr([p.Not(), q.Not(), z]); m.AddImplication(z, p); m.AddImplication(z, q)
        return z
    xh = pos[("L", XH)]
    exact = {pos["v"], pos["p0"], pos["p1"], xh}
    for i, j in itertools.combinations(range(n), 2):
        terms = [AND(adj(i, t), adj(j, t)) for t in range(n) if t not in (i, j)]
        const = sum(t for t in terms if isinstance(t, int))
        terms = [t for t in terms if not isinstance(t, int)]
        e = adj(i, j)
        full = (i in exact) or (j in exact)
        if isinstance(e, int):
            tgt = 1 if e else 2
            if full:
                if terms:
                    m.Add(sum(terms) + const == tgt)
                elif const != tgt:
                    return None
            else:
                if terms:
                    m.Add(sum(terms) + const <= tgt)
                elif const > tgt:
                    return None
        else:
            if full:
                m.Add(sum(terms) + const == 2 - e)
            else:
                m.Add(sum(terms) + const <= 2 - e)
    m.Maximize(sum(rng.randint(-5, 5) * v for v in set(var.values())))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    sv.parameters.random_seed = rng.randint(0, 10 ** 6)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return "none" if st == cp_model.INFEASIBLE else "unknown"
    A = A0.copy()
    for (i, j), v in var.items():
        A[i, j] = sv.Value(v)
    return A


def main():
    rng = random.Random(seed)
    got, stat = [], {"infeasible completion": 0, "unknown": 0}
    tries = 0
    while len(got) < N and tries < 400 * N:
        tries += 1
        mu0, mu1, sig = rand_type(rng)
        if not axioms_ok(mu0, mu1, sig):
            continue
        A = complete(mu0, mu1, sig, rng)
        if isinstance(A, str) or A is None:
            stat["infeasible completion" if A == "none" else "unknown"] += 1
            continue
        H = A[3:, 3:]                                    # G_l (36) + Y (10)
        G = H[:36, :36]
        gap = np.sort(np.linalg.eigvalsh(3 * np.eye(36) - G))[1]
        ev = np.sort(np.linalg.eigvalsh(H))[::-1]
        got.append((ev[1], gap))
        print("type %d: lambda_2(A_H) = %.4f  (lambda_1 %.3f)  gap(G_l) = %.3f" % (len(got), ev[1], ev[0], gap), flush=True)
    if got:
        l2 = np.array([g[0] for g in got])
        print("random c = 1 types completed: %d ; lambda_2(A_H): min %.4f median %.4f max %.4f ; %s" % (
            len(got), l2.min(), np.median(l2), l2.max(), stat))


main()
