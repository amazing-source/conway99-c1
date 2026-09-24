"""Can a vertex x have ALL its transitions tau_a of class type (2,2,2) (tau_a swaps the 6 other classes in three
pairs; 15 pairings x 8 sign patterns = 120 choices per label)?  By L20 (notes/97), k = 6 forces this at every vertex,
so UNSAT here gives k >= 8.  Rooted exact model at x: tau variables (one-hot over the 120 choices per label),
unknown disjoint X-X edges, all SRG equations (lambda = 1, mu = 2 on every pair).
Usage: type222.py [seconds]
"""
import sys, itertools, time
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

CL = range(7)
LABELS = [(c, s) for c in CL for s in (0, 1)]
mate = lambda l: (l[0], 1 - l[1])


def pairings(cls):
    if not cls:
        yield []; return
    f = cls[0]
    for i in range(1, len(cls)):
        for rest in pairings(cls[1:i] + cls[i + 1:]):
            yield [(f, cls[i])] + rest


def choices(a):
    """all (2,2,2) matchings of the 12 labels outside class a[0], as dicts label -> partner"""
    others = [c for c in CL if c != a[0]]
    out = []
    for pr in pairings(others):
        for signs in itertools.product((0, 1), repeat=3):
            m = {}
            for (j, k), f in zip(pr, signs):
                for s in (0, 1):
                    b, c = (j, s), (k, s ^ f)
                    m[b], m[c] = c, b
            out.append(m)
    assert len(out) == 120 and all(len(m) == 12 for m in out)
    return out


def main():
    secs = float(sys.argv[1]) if len(sys.argv) > 1 else 600
    t0 = time.time()
    pool = IDPool(); cnf = CNF()
    CH = {a: choices(a) for a in LABELS}
    sel = {a: [pool.id(('ch', a, i)) for i in range(120)] for a in LABELS}
    for a in LABELS:
        cnf.extend(CardEnc.equals(sel[a], 1, vpool=pool, encoding=EncType.seqcounter).clauses)
    # t[a,b,c] <-> OR of choices pairing b with c
    T = {}
    for a in LABELS:
        others = [b for b in LABELS if b[0] != a[0]]
        for b, c in itertools.combinations(others, 2):
            t = pool.id(('t', a, b, c)); T[(a, b, c)] = T[(a, c, b)] = t
            src = [sel[a][i] for i, m in enumerate(CH[a]) if m[b] == c]
            if not src:
                cnf.append([-t]); continue
            cnf.append([-t] + src)
            for s_ in src:
                cnf.append([t, -s_])
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    V = ['x'] + LABELS + Xv
    D = {}

    def dvar(u, w):
        key = tuple(sorted([tuple(sorted(u)), tuple(sorted(w))]))
        if key not in D:
            D[key] = pool.id(('d',) + key)
        return D[key]

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
            (a,) = com; (b,) = u - com; (c,) = v - com
            return ('v', T[(a, b, c)])
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
    for p in range(len(V)):
        for q in range(p + 1, len(V)):
            u, v = V[p], V[q]
            auv = adj(u, v); const, lits = 0, []
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
                    cnf.extend([[-c, a1[1]], [-c, a2[1]], [c, -a1[1], -a2[1]]]); lits.append(c)
            if auv[0] == 'c':
                want = (1 if auv[1] else 2) - const
                if want < 0 or want > len(lits) or (not lits and want != 0):
                    cnf.append([])
                elif lits:
                    cnf.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
            else:
                e = auv[1]
                for want, cond in ((1 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits):
                        cnf.append([-cond]); continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    # symmetry breaking (valid): relabel signs so that tau_(0,0) uses sign-preserving swaps, and classes so that
    # tau_(0,0) pairs classes {1,2},{3,4},{5,6}.  (Class relabelling and sign flips within classes 1..6 are
    # automorphisms of the rooted structure at x.)
    base = [i for i, m in enumerate(CH[(0, 0)]) if all(m[(j, s)] == (j + 1 if j % 2 else j - 1, s) for j in range(1, 7) for s in (0, 1))]
    cnf.append([sel[(0, 0)][i] for i in base])
    print(f'model: {pool.top} vars, {len(cnf.clauses)} clauses ({time.time()-t0:.1f}s); base choices {len(base)}', flush=True)
    with Cadical153(bootstrap_with=cnf.clauses) as s:
        import threading
        timer = threading.Timer(secs, lambda: s.interrupt()); timer.start()
        r = s.solve_limited(expect_interrupt=True)
        timer.cancel()
        print('result:', {True: 'SAT', False: 'UNSAT', None: 'UNKNOWN (time limit)'}[r], f'({time.time()-t0:.1f}s)', flush=True)


if __name__ == '__main__':
    main()
