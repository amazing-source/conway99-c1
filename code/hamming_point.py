"""Special case 'Hamming point': a vertex x of srg(n, 2(t+1), 1, 2) with tau = mate at x (equivalently x lies in
all C(t+1,2) grids through it). Exact rooted model:
  vertices: x, labels (i,s) (class i in 0..t, sign s in 0/1), X-vertices = pairs of labels in distinct classes.
  fixed: x ~ labels, mates, label ~ X-vertex containing it, labelled X-X edges ab ~ a bbar.
  unknown: disjoint X-X edges.
Tightness of grids (lemma L5) forces: an X-vertex u with classes {i,j} has exactly one disjoint neighbour in
each grid G_{kl}, {k,l} disjoint from {i,j}, i.e. exactly one neighbour among the 4 X-vertices of class pair {k,l},
and no disjoint neighbour whose class pair meets {i,j}.
All SRG equations are then imposed exactly (lambda = 1, mu = 2 on every pair).
Validation: --plant bvls / srg9 checks that the real graph satisfies the CNF (as assumptions).
Usage: python hamming_point.py --t 6 [--conflicts N]   |   python hamming_point.py --t 10 --plant
"""
import argparse, itertools, time, json, sys
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153, Glucose4


FIXED_CONTRA = []


def model(t, use_tight=True, only_local=False):
    classes = list(range(t + 1))
    labels = [(i, s) for i in classes for s in (0, 1)]
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(labels, 2) if a[0] != b[0]]
    cls = lambda u: frozenset(l[0] for l in u)
    pool = IDPool()
    cnf = CNF()
    D = {}  # disjoint-edge variables

    def dvar(u, w):
        key = (u, w) if (min(u, key=str), max(u, key=str)) <= (min(w, key=str), max(w, key=str)) else (w, u)
        key = tuple(sorted([tuple(sorted(u)), tuple(sorted(w))]))
        if key not in D:
            D[key] = pool.id(('d',) + key)
        return D[key]
    # adjacency oracle over all vertices: returns ('const', 0/1) or ('var', id)
    V = ['x'] + labels + Xv

    def adj(u, v):
        if u == v:
            return ('const', 0)
        if u == 'x' or v == 'x':
            o = v if u == 'x' else u
            return ('const', 1 if isinstance(o, tuple) and len(o) == 2 and isinstance(o[0], int) else 0)
        ul = isinstance(u, tuple)  # label
        vl = isinstance(v, tuple)
        if ul and vl:
            return ('const', 1 if u[0] == v[0] else 0)
        if ul and not vl:
            return ('const', 1 if u in v else 0)
        if vl and not ul:
            return ('const', 1 if v in u else 0)
        # both X
        common = u & v
        if common:
            (a,) = common
            (b,) = u - common
            (c,) = v - common
            return ('const', 1 if (b[0] == c[0] and b[1] != c[1]) else 0)   # tau = mate
        cu, cv = cls(u), cls(v)
        if cu & cv:
            return ('const', 0) if use_tight else ('var', dvar(u, v))
        return ('var', dvar(u, v))
    # tightness: exactly one neighbour per disjoint class pair
    if use_tight:
        for u in Xv:
            free = [c for c in classes if c not in cls(u)]
            for k, l in itertools.combinations(free, 2):
                grp = [w for w in Xv if cls(w) == frozenset((k, l))]
                lits = [dvar(u, w) for w in grp]
                cnf.extend(CardEnc.equals(lits=lits, bound=1, vpool=pool, encoding=EncType.pairwise).clauses)
    # degree of X-vertices: 2(t+1) - 2 labels - 2 labelled = 2t - 2 disjoint neighbours
    for u in Xv:
        lits = [a[1] for w in Xv if w != u for a in [adj(u, w)] if a[0] == 'var']
        cnf.extend(CardEnc.equals(lits=lits, bound=2 * t - 2, vpool=pool, encoding=EncType.seqcounter).clauses)
    if only_local:
        return cnf, pool, D, Xv, labels
    # common-neighbour equations for all pairs involving at least one unknown
    nV = len(V)
    for i in range(nV):
        for j in range(i + 1, nV):
            u, v = V[i], V[j]
            a_uv = adj(u, v)
            const_cnt = 0
            lits = []
            for w in V:
                if w in (u, v):
                    continue
                a1, a2 = adj(u, w), adj(v, w)
                if a1 == ('const', 0) or a2 == ('const', 0):
                    continue
                if a1[0] == 'const' and a2[0] == 'const':
                    const_cnt += 1
                    continue
                if a1[0] == 'const':
                    lits.append(a2[1]); continue
                if a2[0] == 'const':
                    lits.append(a1[1]); continue
                c = pool.id(('c', i, j, str(w)))
                cnf.extend([[-c, a1[1]], [-c, a2[1]], [c, -a1[1], -a2[1]]])
                lits.append(c)
            if not lits and a_uv[0] == 'const':
                want = 1 if a_uv[1] else 2
                if const_cnt != want:
                    cnf.append([])  # contradiction in the fixed part
                    FIXED_CONTRA.append((str(u), str(v), const_cnt, want))
                continue
            if a_uv[0] == 'const':
                want = (1 if a_uv[1] else 2) - const_cnt
                if want < 0 or want > len(lits):
                    cnf.append([])
                    FIXED_CONTRA.append((str(u), str(v), const_cnt, want, len(lits)))
                    continue
                cnf.extend(CardEnc.equals(lits=lits, bound=want, vpool=pool, encoding=EncType.seqcounter).clauses)
            else:
                e = a_uv[1]
                for want, cond in ((1 - const_cnt, e), (2 - const_cnt, -e)):
                    if want < 0 or want > len(lits):
                        cnf.append([-cond])
                        continue
                    for cl in CardEnc.equals(lits=lits, bound=want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    return cnf, pool, D, Xv, labels


def plant(t, name):
    """Map a real grid-full graph's rooted structure at vertex 0 onto the model's labels; return assumptions."""
    import numpy as np
    sys.path.insert(0, '.')
    import graphs, rooted
    A = graphs.ALL[name]()
    R = rooted.Rooted(A, 0)
    assert R.is_mate_system()
    lab = {}
    for i, (a, ab) in enumerate(R.classes()):
        lab[a], lab[ab] = (i, 0), (i, 1)
    Xmap = {frozenset((lab[a], lab[b])): u for u, (a, b) in ((u, tuple(R.label[u])) for u in R.X)}
    return A, Xmap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=6)
    ap.add_argument('--plant', action='store_true')
    ap.add_argument('--conflicts', type=int, default=0)
    ap.add_argument('--notight', action='store_true')
    ap.add_argument('--only-local', action='store_true', help='relaxed positive control: degrees + tightness only')
    ap.add_argument('--sigma', action='store_true', help='impose invariance under sigma_x (flip every sign): C2 case')
    ap.add_argument('--breaksym', action='store_true', help='same symmetry breaking as hamming_phi.py --breaksym')
    a = ap.parse_args()
    t0 = time.time()
    cnf, pool, D, Xv, labels = model(a.t, use_tight=not a.notight, only_local=a.only_local)
    print('fixed-part contradictions:', len(FIXED_CONTRA), FIXED_CONTRA[:3], flush=True)
    if a.sigma:
        flip = lambda lab: tuple(sorted(((c, 1 - s) for (c, s) in lab)))
        nsig = 0
        for key, var in list(D.items()):
            k2 = tuple(sorted([flip(key[0]), flip(key[1])]))
            if k2 in D and D[k2] != var:
                cnf.append([-var, D[k2]]); cnf.append([var, -D[k2]]); nsig += 1
        print('sigma-invariance clauses pairs:', nsig, flush=True)
    if a.breaksym:
        def dv(u, w):
            key = tuple(sorted([tuple(sorted(u)), tuple(sorted(w))]))
            return D[key]
        X = lambda i, si, j, sj: frozenset(((i, si), (j, sj)))
        u0 = X(0, 0, 1, 0)
        Qv = lambda K: [X(K[0], p, K[1], q) for p in (0, 1) for q in (0, 1)]
        cnf.append([dv(u0, X(2, 0, 3, 0))])
        cnf.append([dv(u0, X(4, 0, 5, 0))])
        cnf.append([dv(u0, X(2, 0, 6, 0)), dv(u0, X(2, 1, 6, 0))])
        NF = {0: [(1, 2), (3, 4)], 1: [(0, 3), (2, 4)], 2: [(0, 4), (1, 3)], 3: [(0, 2), (1, 4)], 4: [(0, 1), (2, 3)]}
        for d, (e1, e2) in NF.items():
            K = (e1[0] + 2, e1[1] + 2); M = (e2[0] + 2, e2[1] + 2)
            for z in Qv(K):
                for w in Qv(M):
                    cnf.append([-dv(u0, z), -dv(u0, w), dv(z, w)])
        print('symmetry breaking added', flush=True)
    print(f't={a.t}: {len(Xv)} X-vertices, {len(D)} unknown disjoint edges, {pool.top} vars, {len(cnf.clauses)} clauses '
          f'(built in {time.time()-t0:.1f}s)', flush=True)
    assumptions = []
    if a.plant:
        name = {1: 'srg9', 10: 'bvls'}[a.t]
        A, Xmap = plant(a.t, name)
        for key, var in D.items():
            u, w = Xmap[frozenset(key[0])], Xmap[frozenset(key[1])]
            assumptions.append(var if A[u, w] else -var)
    S = Cadical153(bootstrap_with=cnf.clauses) if not a.conflicts else Glucose4(bootstrap_with=cnf.clauses)
    t1 = time.time()
    if a.conflicts:
        S.conf_budget(a.conflicts)
        ok = S.solve_limited(assumptions=assumptions)
    else:
        ok = S.solve(assumptions=assumptions)
    print('result:', {True: 'SAT', False: 'UNSAT', None: 'UNKNOWN (budget)'}[ok], f'({time.time()-t1:.1f}s)', flush=True)
    if ok and not a.plant:
        m = set(l for l in S.get_model() if l > 0)
        sol = [list(map(list, k)) for k, v in D.items() if v in m]
        json.dump(sol, open(f'../data/hamming_point_t{a.t}_solution.json', 'w'))
        print('solution saved')


if __name__ == '__main__':
    main()
