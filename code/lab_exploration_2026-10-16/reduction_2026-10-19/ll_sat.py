"""Line-local system as pure SAT (LAB 19/10/2026): same constraints as ll_test.py (L1, L2, L3, L4), CNF via pysat
cardinality encodings, solved by CaDiCaL 1.5.3 (pysat), one thread.  Second solver family for the hardness question
(CP-SAT gave UNKNOWN at 280 s x 12 workers for n = 12).
usage: python ll_sat.py planted <seed> <sec> [n] | random <seed> <sec> [L1|L12|L123] | blocks <seed> <k1,..> <sec> [tag]"""
import json
import random
import sys
import threading
import time

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from ll_test import (block_gt, components, gt_matrix, inv, k_matrix, pairs_of, random_gt, uses,  # noqa: E402
                     verify)


def build(n, s01, s12, s20, use, margins=None):
    pool = IDPool()
    cnf = CNF()
    P = pairs_of(n)
    m = len(P)
    if margins is None:
        G = gt_matrix(n, s01, s12, s20)
        K = k_matrix(n, G)
        K01, K02, K12 = K[0:n, n:2 * n], K[0:n, 2 * n:3 * n], K[n:2 * n, 2 * n:3 * n]
    else:
        K01, K02, K12 = margins
    X = [[pool.id(("X", f, e)) for e in range(m)] for f in range(m)]
    Y = [[pool.id(("Y", f, e)) for e in range(m)] for f in range(m)]

    def exactly(lits, k):
        if not lits:
            if k:
                cnf.append([])
            return
        enc = CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter)
        cnf.extend(enc.clauses)

    def atmost(lits, k):
        enc = CardEnc.atmost(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter)
        cnf.extend(enc.clauses)
    for f in range(m):
        exactly(X[f], 1)
        exactly(Y[f], 1)
    for e in range(m):
        exactly([X[f][e] for f in range(m)], 1)
        exactly([Y[f][e] for f in range(m)], 1)
    inc = [[e for e, pr in enumerate(P) if v in pr] for v in range(n)]
    a = [[pool.id(("a", f, v)) for v in range(n)] for f in range(m)]
    b = [[pool.id(("b", f, v)) for v in range(n)] for f in range(m)]
    for f in range(m):
        for v in range(n):
            for (W, M) in ((a, X), (b, Y)):
                cnf.append([-W[f][v]] + [M[f][e] for e in inc[v]])
                for e in inc[v]:
                    cnf.append([-M[f][e], W[f][v]])
    pin = [[f for f, pr in enumerate(P) if u in pr] for u in range(n)]
    z = {}
    for f in range(m):
        for v in range(n):
            for w in range(n):
                t = pool.id(("z", f, v, w))
                z[f, v, w] = t
                cnf.extend([[-t, a[f][v]], [-t, b[f][w]], [t, -a[f][v], -b[f][w]]])
    if "L1" in use:
        for u in range(n):
            for v in range(n):
                exactly([a[f][v] for f in pin[u]], int(K01[u][v]))
                exactly([b[f][v] for f in pin[u]], int(K02[u][v]))
        for v in range(n):
            for w in range(n):
                exactly([z[f, v, w] for f in range(m)], int(K12[v][w]))
    if "L2" in use:
        i01, i12, i20 = inv(s01), inv(s12), inv(s20)
        for f, (x, y) in enumerate(P):
            pset = {x, y}
            for u in range(n):
                cap = 2 - int(u in pset) - int((u ^ 1) in pset)
                lits = [a[f][s01[u]], b[f][i20[u]]]
                if cap < 0:
                    cnf.append([])
                elif cap < 2:
                    atmost(lits, cap)
            # x = (1,v): a[v^1] + [i01 v in p(f)] + b[s12 v] <= 2 - a[v]; vacuous unless i01[v] in p(f), where it
            # says at most one of a[v^1], b[s12 v], a[v] (a[v] + a[v^1] <= 1 always: names are non-partner pairs)
            for v in range(n):
                if i01[v] in pset:
                    atmost([a[f][v ^ 1], b[f][s12[v]], a[f][v]], 1)
            for w in range(n):                                   # x = (2,w), same shape
                if s20[w] in pset:
                    atmost([b[f][w ^ 1], a[f][i12[w]], b[f][w]], 1)
    if "L3" in use:
        for u in range(n):
            for v in range(n):
                for w in range(n):
                    atmost([z[f, v, w] for f in pin[u]], 1)
    if "L4" in use and s01 is not None:
        G = gt_matrix(n, s01, s12, s20)
        nc, comp = components(G)
        if nc > 1:
            sizes = {}
            for x in range(3 * n):
                sizes[comp[x]] = sizes.get(comp[x], 0) + 1
            for f, (x0, y0) in enumerate(P):
                for cc, sz in sizes.items():
                    fixed = int(comp[x0] == cc) + int(comp[y0] == cc)
                    lits = [a[f][v] for v in range(n) if comp[n + v] == cc] + \
                           [b[f][w] for w in range(n) if comp[2 * n + w] == cc]
                    exactly(lits, sz // 6 - fixed) if sz // 6 - fixed >= 0 else cnf.append([])
    return cnf, P, X, Y


SOLVER = __import__("os").environ.get("LL_SOLVER", "cadical195")


def _child(name, clauses, conn):
    s = Solver(name=name, bootstrap_with=clauses)
    r = s.solve()
    conn.send((r, s.get_model() if r else None))
    s.delete()


def run(cnf, P, X, Y, sec):
    """solve in a child process (hard wall-clock limit for solvers without interrupt support)"""
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    parent, child = ctx.Pipe(duplex=False)
    pr = ctx.Process(target=_child, args=(SOLVER, cnf.clauses, child), daemon=True)
    t0 = time.time()
    pr.start()
    r, model = None, None
    if parent.poll(sec):
        r, model = parent.recv()
    wall = round(time.time() - t0, 1)
    if pr.is_alive():
        pr.terminate()
    pr.join(5)
    names = None
    if r is True:
        mdl = set(l for l in model if l > 0)
        m = len(P)
        names = [(P[f], P[[e for e in range(m) if X[f][e] in mdl][0]], P[[e for e in range(m) if Y[f][e] in mdl][0]])
                 for f in range(m)]
    st = {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[r]
    return st, wall, names


def main():
    mode = sys.argv[1]
    rec = {"mode": mode, "argv": sys.argv[2:], "solver": SOLVER}
    if mode == "planted":
        seed, sec = int(sys.argv[2]), float(sys.argv[3])
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        rng = random.Random(seed)
        P = pairs_of(n)
        m = len(P)
        q, s = rng.sample(range(m), m), rng.sample(range(m), m)
        E = np.zeros((3 * n, m), dtype=np.int64)
        for f in range(m):
            for c, pr in enumerate((P[f], P[q[f]], P[s[f]])):
                for i in pr:
                    E[c * n + i, f] = 1
        K = E @ E.T
        cnf, P2, X, Y = build(n, None, None, None, {"L1"}, margins=(K[0:n, n:2 * n], K[0:n, 2 * n:], K[n:2 * n, 2 * n:]))
        st, wall, sol = run(cnf, P2, X, Y, sec)
        ok = None
        if sol:
            E2 = np.zeros_like(E)
            for f, nm in enumerate(sol):
                for c, pr in enumerate(nm):
                    for i in pr:
                        E2[c * n + i, f] = 1
            ok = bool(((E2 @ E2.T) == K).all())
        rec.update(n=n, vars=cnf.nv, clauses=len(cnf.clauses), status=st, wall=wall, recheck_margins_equal=ok)
    else:
        seed = int(sys.argv[2])
        rng = random.Random(seed)
        n = 12
        if mode == "random":
            sec, tag = float(sys.argv[3]), (sys.argv[4] if len(sys.argv) > 4 else "L123")
            s01, s12, s20, tries = random_gt(n, rng, 1)
        else:
            sizes, sec = [int(x) for x in sys.argv[3].split(",")], float(sys.argv[4])
            tag = sys.argv[5] if len(sys.argv) > 5 else "L1234"
            s01, s12, s20, tries = block_gt(n, rng, sizes)
        use = uses(tag)
        cnf, P, X, Y = build(n, s01, s12, s20, use)
        st, wall, sol = run(cnf, P, X, Y, sec)
        G = gt_matrix(n, s01, s12, s20)
        rec.update(n=n, c=components(G)[0], use=sorted(use), vars=cnf.nv, clauses=len(cnf.clauses), status=st,
                   wall=wall, recheck=verify(n, s01, s12, s20, sol, conway=True) if sol else None, gt=[s01, s12, s20])
    print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
