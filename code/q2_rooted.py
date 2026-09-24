"""Control of the whole rooted-SAT methodology on the q = 2 analogue: srg(56,10,0,2) (Gewirtz, unique, twisted:
no 3-cube closure at any vertex) and srg(16,5,0,2) (Clebsch, cube quotient: all closures).
Rooted model at x: labels = N(x) (k of them, no mates since lambda = 0), X = pairs of labels (mu = 2),
fixed: x ~ labels, label ~ X-vertices containing it; X-X edges only between DISJOINT pairs (sharing a label would
create a triangle with lambda = 0); unknown: those edges. All SRG equations exact.
  --closure : impose one 3-cube closure at x (a common neighbour of {0,1},{0,2},{1,2})  -> Gewirtz: must be UNSAT
  (no option) : must be SAT (Gewirtz / Clebsch exist), and the solution must be isomorphic to the real graph.
Usage: python q2_rooted.py k [--closure]      (k = 10 Gewirtz, k = 5 Clebsch)
"""
import sys, itertools, time
import numpy as np
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153


def build(k, closure=False):
    L = list(range(k))
    Xv = [frozenset(p) for p in itertools.combinations(L, 2)]
    V = ['x'] + L + Xv
    pool, cnf, D = IDPool(), CNF(), {}

    def dvar(u, w):
        key = tuple(sorted([tuple(sorted(u)), tuple(sorted(w))]))
        if key not in D:
            D[key] = pool.id(key)
        return D[key]

    def adj(u, v):
        if u == v:
            return ('c', 0)
        if u == 'x' or v == 'x':
            o = v if u == 'x' else u
            return ('c', 1 if isinstance(o, int) else 0)
        ul, vl = isinstance(u, int), isinstance(v, int)
        if ul and vl:
            return ('c', 0)
        if ul:
            return ('c', 1 if u in v else 0)
        if vl:
            return ('c', 1 if v in u else 0)
        if u & v:
            return ('c', 0)
        return ('v', dvar(u, v))
    n = len(V)
    for p in range(n):
        for q in range(p + 1, n):
            u, v = V[p], V[q]
            auv = adj(u, v)
            const, lits = 0, []
            for w in V:
                if w in (u, v):
                    continue
                a1, a2 = adj(u, w), adj(v, w)
                if a1 == ('c', 0) or a2 == ('c', 0):
                    continue
                if a1[0] == 'c' and a2[0] == 'c':
                    const += 1
                elif a1[0] == 'c':
                    lits.append(a2[1])
                elif a2[0] == 'c':
                    lits.append(a1[1])
                else:
                    c = pool.id(('and', p, q, str(w)))
                    cnf.extend([[-c, a1[1]], [-c, a2[1]], [c, -a1[1], -a2[1]]])
                    lits.append(c)
            if auv[0] == 'c':
                want = (0 if auv[1] else 2) - const
                if want < 0 or want > len(lits):
                    cnf.append([])
                elif lits:
                    cnf.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
                elif want != 0:
                    cnf.append([])
            else:
                e = auv[1]
                for want, cond in ((0 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits):
                        cnf.append([-cond]); continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    # degree of X-vertices: k - 2 disjoint neighbours
    for u in Xv:
        lits = [adj(u, w)[1] for w in Xv if adj(u, w)[0] == 'v']
        cnf.extend(CardEnc.equals(lits, k - 2, vpool=pool, encoding=EncType.seqcounter).clauses)
    if closure:
        a, b, c = frozenset((0, 1)), frozenset((0, 2)), frozenset((1, 2))
        cands = [w for w in Xv if not (w & {0, 1, 2})]
        ors = []
        for w in cands:
            z = pool.id(('clos', w))
            cnf.extend([[-z, dvar(w, a)], [-z, dvar(w, b)], [-z, dvar(w, c)]])
            ors.append(z)
        cnf.append(ors)
    return cnf, pool, D, V, Xv


def main():
    k = int(sys.argv[1])
    closure = '--closure' in sys.argv
    t0 = time.time()
    cnf, pool, D, V, Xv = build(k, closure)
    S = Cadical153(bootstrap_with=cnf.clauses)
    ok = S.solve()
    print(f'k = {k} closure = {closure}: {len(D)} unknowns, {len(cnf.clauses)} clauses -> {"SAT" if ok else "UNSAT"} ({time.time()-t0:.1f}s)')
    if ok:
        import networkx as nx, graphs
        m = set(l for l in S.get_model() if l > 0)
        ix = {v: i for i, v in enumerate(V)}
        A = np.zeros((len(V), len(V)), dtype=int)
        for i, u in enumerate(V):
            for j, v in enumerate(V):
                if i < j:
                    if u == 'x':
                        e = isinstance(v, int)
                    elif isinstance(u, int) and isinstance(v, int):
                        e = False
                    elif isinstance(u, int):
                        e = u in v
                    elif u & v:
                        e = False
                    else:
                        key = tuple(sorted([tuple(sorted(u)), tuple(sorted(v))]))
                        e = D[key] in m
                    A[i, j] = A[j, i] = int(e)
        print('   solution srg params:', graphs.srg_params(A))
        real = graphs.gewirtz() if k == 10 else graphs.clebsch()
        print('   isomorphic to the real graph:', nx.is_isomorphic(nx.from_numpy_array(A), nx.from_numpy_array(real)))


if __name__ == '__main__':
    main()
