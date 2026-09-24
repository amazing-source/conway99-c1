"""Rooted model of srg(99,14,1,2) at x with tau PARTIALLY FREE (SAT variables), to exclude whole families of
local configurations at once.
Family 'confined(K)': twists only inside a set K of classes: for a label a in a class of K, tau_a restricted to the
labels of the other classes of K is a free perfect matching of those labels; everything else is mate.
(This is consistent: tau_a must map labels of classes outside K to their mates, so it maps the labels of K minus [a]
among themselves.) At least one twist is required (tau != mate).
Variables: t[a,{b,c}] (tau_a pairs b and c, b, c in K - [a], distinct classes allowed incl. mates); disjoint X-X edges.
Adjacency oracle: labelled X-X edge {a,b}~{a,c} is a constant (mate) or a t-variable.
All SRG equations (lambda = 1, mu = 2 on every pair) are imposed exactly. Grid tightness is not imposed (implied).
Usage: python rooted_family.py K   e.g.  python rooted_family.py 012   |  0123
"""
import sys, itertools, time
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

CL = range(7)
LABELS = [(c, s) for c in CL for s in (0, 1)]
mate = lambda l: (l[0], 1 - l[1])


def build(K, sources=None):
    K = set(K)
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    V = ['x'] + LABELS + Xv
    pool = IDPool()
    cnf = CNF()
    T = {}

    def tvar(a, b, c):
        key = (a, tuple(sorted((b, c))))
        if key not in T:
            T[key] = pool.id(('t',) + key)
        return T[key]
    free = {}  # a -> list of labels whose partner is free
    for a in LABELS:
        dom = None
        if sources is not None:
            if a in sources:
                dom = [b for b in LABELS if b[0] != a[0]]
        elif a[0] in K:
            dom = [b for b in LABELS if b[0] in K and b[0] != a[0]]
        if dom is not None:
            free[a] = dom
            for b in dom:
                lits = [tvar(a, b, c) for c in dom if c != b]
                cnf.extend(CardEnc.equals(lits, 1, vpool=pool, encoding=EncType.pairwise).clauses)
    # at least one twist
    tw = [tvar(a, b, c) for a in free for b, c in itertools.combinations(free[a], 2) if c != mate(b)]
    cnf.append(tw)
    # no 3-cycles in the trail system is implied by lambda; not added.

    def dvar(u, w):
        key = tuple(sorted([tuple(sorted(u)), tuple(sorted(w))]))
        return pool.id(('d',) + key)

    def adj(u, v):
        if u == v:
            return ('c', 0)
        if u == 'x' or v == 'x':
            o = v if u == 'x' else u
            return ('c', 1 if isinstance(o, tuple) else 0)
        ul, vl = isinstance(u, tuple), isinstance(v, tuple)
        if ul and vl:
            return ('c', 1 if mate(u) == v else 0)
        if ul:
            return ('c', 1 if u in v else 0)
        if vl:
            return ('c', 1 if v in u else 0)
        com = u & v
        if com:
            (a,) = com
            (b,) = u - com
            (c,) = v - com
            if a in free and b in free[a] and c in free[a]:
                return ('v', tvar(a, b, c))
            return ('c', 1 if mate(b) == c else 0)
        return ('v', dvar(u, v))
    for u in Xv:
        lits, const = [], 0
        for w in Xv:
            if w == u:
                continue
            a_ = adj(u, w)
            if a_[0] == 'v':
                lits.append(a_[1])
            else:
                const += a_[1]
        cnf.extend(CardEnc.equals(lits, 12 - const, vpool=pool, encoding=EncType.seqcounter).clauses)
    nV = len(V)
    for p in range(nV):
        for q in range(p + 1, nV):
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
                want = (1 if auv[1] else 2) - const
                if want < 0 or want > len(lits):
                    cnf.append([])
                elif lits:
                    cnf.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
                elif want != 0:
                    cnf.append([])
            else:
                e = auv[1]
                for want, cond in ((1 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits):
                        cnf.append([-cond])
                        continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    return cnf, pool, T


def main():
    t0 = time.time()
    if sys.argv[1] == 'sources':
        src = [(int(p[0]), int(p[1])) for p in sys.argv[2].split(',')]
        cnf, pool, T = build([], sources=src)
        K = f'sources {src}'
    else:
        K = [int(ch) for ch in sys.argv[1]]
        cnf, pool, T = build(K)
    print(f'family {K}: {len(T)} tau-variables, {pool.top} vars, {len(cnf.clauses)} clauses ({time.time()-t0:.1f}s)', flush=True)
    S = Cadical153(bootstrap_with=cnf.clauses)
    t1 = time.time()
    ok = S.solve()
    print('result:', 'SAT' if ok else 'UNSAT', f'({time.time()-t1:.1f}s)', flush=True)
    if ok:
        m = set(l for l in S.get_model() if l > 0)
        print('twists:', [k for k, v in T.items() if v in m and k[1][1] != mate(k[1][0])])


if __name__ == '__main__':
    main()
