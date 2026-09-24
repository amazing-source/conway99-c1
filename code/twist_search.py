"""Attack on F2 (q = 3 rigidity): search for a finite graph that is locally (t+1)K2 (lambda = 1),
has mu in {0, 2} for non-adjacent pairs, and is TWISTED at vertex 0 (some tau_a(b) != mate(b)).

Symmetry breaking: vertex 0, N(0) = 1..2(t+1) with mates (1,2),(3,4),...; X-vertices = the next C(2t+2,2)-(t+1)
vertices with fixed labels (their neighbours in N(0)); vertices beyond the ball are at distance >= 3 from 0.
The twist is imposed as the edge X(1,3) ~ X(1,5) (tau_1(3) = 5 instead of mate(3) = 4); w.l.o.g. by the
hyperoctahedral symmetry of the rooted ball.
Also usable with --untwisted (impose tau = mate at 0) as a positive control: H(t+1,3) must be found for
n = 3^(t+1) when t is small.

Usage: python twist_search.py --t 2 --nmin 19 --nmax 60 [--untwisted] [--timeout 600]
"""
import argparse, itertools, sys, time, json
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153, Glucose4


def build(t, n, twisted=True):
    k = 2 * (t + 1)
    pool = IDPool()
    E = lambda u, v: pool.id(('e', min(u, v), max(u, v)))
    cnf = CNF()
    L = list(range(1, k + 1))
    mate = {}
    for i in range(0, k, 2):
        mate[L[i]] = L[i + 1]
        mate[L[i + 1]] = L[i]
    pairs = [(a, b) for a, b in itertools.combinations(L, 2) if mate[a] != b]
    Xv = {p: k + 1 + i for i, p in enumerate(pairs)}
    ball = 1 + k + len(pairs)
    assert n >= ball
    unit = lambda lit: cnf.append([lit])
    # fixed part of the ball
    for u in range(n):
        for v in range(u + 1, n):
            if u == 0:
                unit(E(0, v) if v in L else -E(0, v))
            elif u in L and v in L:
                unit(E(u, v) if mate[u] == v else -E(u, v))
            elif u in L and v >= k + 1:
                if v < ball:
                    lab = pairs[v - k - 1]
                    unit(E(u, v) if u in lab else -E(u, v))
                else:
                    unit(-E(u, v))                      # beyond the ball: distance >= 3 from 0
    # twist / untwisted at 0 on the labelled X-X edges
    def X(a, b):
        return Xv[(min(a, b), max(a, b))]
    if twisted:
        unit(E(X(1, 3), X(1, 5)))
    else:
        for a in L:
            for b in L:
                if b not in (a, mate[a]):
                    unit(E(X(a, b), X(a, mate[b])))
    # degrees
    for u in range(n):
        lits = [E(u, v) for v in range(n) if v != u]
        cnf.extend(CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)
    # common neighbours
    for u, v in itertools.combinations(range(n), 2):
        cs = []
        for w in range(n):
            if w in (u, v):
                continue
            c = pool.id(('c', u, v, w))
            cnf.append([-c, E(u, w)])
            cnf.append([-c, E(v, w)])
            cnf.append([c, -E(u, w), -E(v, w)])
            cs.append(c)
        e = E(u, v)
        # at most 2 common neighbours always
        cnf.extend(CardEnc.atmost(lits=cs, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
        # adjacent -> at least 1 and at most 1
        amo = CardEnc.atmost(lits=cs, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses
        for cl in amo:
            cnf.append([-e] + cl)
        cnf.append([-e] + cs)
        # non-adjacent -> not exactly one: each present c forces another one
        for i, c in enumerate(cs):
            cnf.append([e, -c] + cs[:i] + cs[i + 1:])
    return cnf, pool, E


def decode(model, pool, n, E):
    s = set(l for l in model if l > 0)
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if E(u, v) in s:
                A[u][v] = A[v][u] = 1
    return A


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=2)
    ap.add_argument('--nmin', type=int, default=19)
    ap.add_argument('--nmax', type=int, default=60)
    ap.add_argument('--untwisted', action='store_true')
    ap.add_argument('--conflicts', type=int, default=2000000)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    for n in range(a.nmin, a.nmax + 1):
        t0 = time.time()
        cnf, pool, E = build(a.t, n, twisted=not a.untwisted)
        with Glucose4(bootstrap_with=cnf.clauses) as S:
            S.conf_budget(a.conflicts)
            ok = S.solve_limited()
            dt = time.time() - t0
            verdict = {True: 'SAT', False: 'UNSAT', None: 'UNKNOWN(budget)'}[ok]
            print(f't={a.t} n={n} twisted={not a.untwisted} vars={pool.top} clauses={len(cnf.clauses)} -> {verdict} ({dt:.1f}s)', flush=True)
            if ok:
                A = decode(S.get_model(), pool, n, E)
                if a.out:
                    json.dump(A, open(a.out, 'w'))
                break


if __name__ == '__main__':
    main()
