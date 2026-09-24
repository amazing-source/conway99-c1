"""Minimal UNSAT cores for the rooted model (rooted_model.py), to turn quick SAT refutations into hand proofs.

Each constraint group gets a selector literal: 'deg:u' (X-vertex u has 10 disjoint neighbours), 'tight:G:z' (z has
exactly one neighbour in grid G), 'srg:u:v' (lambda/mu equation for the pair u, v).  Solve under all selectors,
take the core, then shrink it by deletion (each check is a short solve).  Prints the minimal core in readable form.
Usage: core_extract.py CASE [--notight]      CASE as in rooted_model.py (g19A, g19AA, g19AB, spec:...)
"""
import sys, itertools, time
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
from rooted_model import tau_case, LABELS, CL, mate


def build_sel(tau, tight=True):
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    V = ['x'] + LABELS + Xv
    pool = IDPool()
    groups = {}          # selector -> (name, clauses)
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
            return ('c', 1 if tau[a][b] == c else 0)
        return ('v', dvar(u, v))

    def add(name, clauses):
        s = pool.id(('sel', name))
        groups[s] = (name, [[-s] + cl for cl in clauses])

    for u in Xv:
        lits = [adj(u, w)[1] for w in Xv if w != u and adj(u, w)[0] == 'v']
        add(('deg', u), CardEnc.equals(lits, 10, vpool=pool, encoding=EncType.seqcounter).clauses)
    grids = [(i, j) for i, j in itertools.combinations(CL, 2)
             if all(tau[(i, s)][(j, r)] == (j, 1 - r) and tau[(j, r)][(i, s)] == (i, 1 - s) for s in (0, 1) for r in (0, 1))]
    if tight:
        for i, j in grids:
            G = ['x', (i, 0), (i, 1), (j, 0), (j, 1)] + [frozenset(((i, s), (j, r))) for s in (0, 1) for r in (0, 1)]
            for z in V:
                if z in G:
                    continue
                const, lits = 0, []
                for g in G:
                    a = adj(z, g)
                    if a[0] == 'c':
                        const += a[1]
                    else:
                        lits.append(a[1])
                want = 1 - const
                cl = [[]] if (want < 0 or want > len(lits)) else CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses
                add(('tight', (i, j), z), cl)
    for p in range(len(V)):
        for q in range(p + 1, len(V)):
            u, v = V[p], V[q]
            auv = adj(u, v)
            const, lits, ands = 0, [], []
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
                    ands.extend([[-c, a1[1]], [-c, a2[1]], [c, -a1[1], -a2[1]]])
                    lits.append(c)
            cls = list(ands)
            if auv[0] == 'c':
                want = (1 if auv[1] else 2) - const
                if want < 0 or want > len(lits) or (not lits and want != 0):
                    cls.append([])
                elif lits:
                    cls.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
            else:
                e = auv[1]
                for want, cond in ((1 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits):
                        cls.append([-cond]); continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cls.append([-cond] + cl)
            add(('srg', u, v), cls)
    return groups, pool


def fmt(v):
    if v == 'x':
        return 'x'
    if isinstance(v, tuple):
        return f'{v[0]}{"ab"[v[1]]}'
    a, b = sorted(v)
    return '{' + fmt(a) + ',' + fmt(b) + '}'


def main():
    case = sys.argv[1]
    tight = '--notight' not in sys.argv
    t0 = time.time()
    groups, pool = build_sel(tau_case(case), tight)
    sels = list(groups)
    solver = Cadical153()
    for s in sels:
        for cl in groups[s][1]:
            solver.add_clause(cl)
    r = solver.solve(assumptions=sels)
    print(f'{case}: {len(sels)} groups, solve -> {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)', flush=True)
    if r:
        return
    core = list(solver.get_core())
    print('initial core size', len(core), flush=True)
    # deletion-based minimisation
    i = 0
    while i < len(core):
        trial = core[:i] + core[i + 1:]
        if not solver.solve(assumptions=trial):
            core = list(solver.get_core()) if len(solver.get_core()) < len(trial) else trial
            core = [c for c in core]  # keep order
        else:
            i += 1
    print(f'minimal core ({len(core)} groups, {time.time()-t0:.1f}s):')
    for s in sorted(core, key=lambda s: str(groups[s][0])):
        name = groups[s][0]
        print('  ', name[0], ' '.join(fmt(p) if not isinstance(p, tuple) or len(p) != 2 or not isinstance(p[0], int) or p in LABELS else str(p) for p in name[1:]))


if __name__ == '__main__':
    main()
