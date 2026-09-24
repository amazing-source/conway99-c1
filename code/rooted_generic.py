"""Generic exact rooted model of srg(n, 2(t+1), 1, 2) at a vertex x, for ANY t, with a prescribed transition
system tau (read from a real graph, from a spec, or tau = mate). Same equations as rooted_model.py (t = 6).
Purposes:
  * SAT-level POSITIVE CONTROL: with tau read from BvLS (t = 10) the CNF must be SAT (lab PC: ~20 M clauses);
    with --plant the real disjoint edges are given as assumptions (must be SAT instantly).
  * DIMACS export (--dimacs FILE) for DRAT certification of the UNSAT results (lab PC: cadical + drat-trim).
Usage:
  python rooted_generic.py --graph srg9 [--plant] [--dimacs f.cnf]
  python rooted_generic.py --graph bvls --root 0 --dimacs bvls_rooted.cnf        (lab PC)
  python rooted_generic.py --t 6 --case hamming --dimacs hamming.cnf              (for DRAT on the lab PC)
"""
import argparse, itertools, time, sys
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType


def build(t, tau, want_tight=False):
    CL = range(t + 1)
    LABELS = [(c, s) for c in CL for s in (0, 1)]
    mate = lambda l: (l[0], 1 - l[1])
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    V = ['x'] + LABELS + Xv
    pool, cnf, D = IDPool(), CNF(), {}

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
            (a,) = com
            (b,) = u - com
            (c,) = v - com
            return ('c', 1 if tau[a][b] == c else 0)
        return ('v', dvar(u, v))
    for u in Xv:
        lits = [adj(u, w)[1] for w in Xv if w != u and adj(u, w)[0] == 'v']
        if lits:
            cnf.extend(CardEnc.equals(lits, 2 * t - 2, vpool=pool, encoding=EncType.seqcounter).clauses)
        elif 2 * t - 2 != 0:
            cnf.append([])
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
                        cnf.append([-cond]); continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    return cnf, pool, D, LABELS, Xv


def tau_from_graph(name, root):
    import graphs, rooted
    A = graphs.ALL[name]()
    R = rooted.Rooted(A, root)
    lab = {}
    for i, (a, ab) in enumerate(R.classes()):
        lab[a], lab[ab] = (i, 0), (i, 1)
    tau = {lab[a]: {lab[b]: lab[c] for b, c in R.tau[a].items()} for a in R.L}
    t = len(R.L) // 2 - 1
    real = {}
    for u in R.X:
        a, b = tuple(R.label[u])
        real[frozenset((lab[a], lab[b]))] = u
    return t, tau, A, real


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--graph', default=None)
    ap.add_argument('--root', type=int, default=0)
    ap.add_argument('--t', type=int, default=6)
    ap.add_argument('--case', default=None, help='rooted_model.py case (t = 6 only)')
    ap.add_argument('--plant', action='store_true')
    ap.add_argument('--dimacs', default=None)
    ap.add_argument('--solve', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    if a.graph:
        t, tau, A, real = tau_from_graph(a.graph, a.root)
    else:
        import rooted_model as rm
        t, tau = 6, rm.tau_case(a.case)
    cnf, pool, D, LABELS, Xv = build(t, tau)
    print(f't = {t}: {len(D)} unknowns, {pool.top} vars, {len(cnf.clauses)} clauses ({time.time()-t0:.0f}s)', flush=True)
    if a.dimacs:
        cnf.to_file(a.dimacs)
        print('written', a.dimacs, flush=True)
    if a.solve or a.plant:
        from pysat.solvers import Cadical153
        assum = []
        if a.plant:
            for key, var in D.items():
                u, w = real[frozenset(key[0])], real[frozenset(key[1])]
                assum.append(var if A[u, w] else -var)
        S = Cadical153(bootstrap_with=cnf.clauses)
        t1 = time.time()
        ok = S.solve(assumptions=assum)
        print('result:', 'SAT' if ok else 'UNSAT', f'({time.time()-t1:.1f}s)', 'with planted solution' if a.plant else '')


if __name__ == '__main__':
    main()
