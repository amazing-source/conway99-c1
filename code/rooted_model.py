"""General exact rooted model of srg(99,14,1,2) at a vertex x with a PRESCRIBED transition system tau at x.
Labels (c, s): class c in 0..6, sign s in {0,1}; mate(c,s) = (c,1-s). X-vertices = pairs of labels in distinct classes.
Fixed: x ~ labels, mates, label ~ X-vertex containing it, labelled X-X edges given by tau:
   {a,b} ~ {a,c}  iff  tau[a][b] == c.
Unknown: disjoint X-X edges. All SRG equations imposed (lambda = 1, mu = 2 on every pair), plus grid tightness
(lemma L5) for every grid through x that exists under tau (redundant but helps).
Cases:
  --case hamming      tau = mate everywhere (same as hamming_point.py)
  --case g19A         tau_(0,0): classes 1,2 swapped sign-preserving (1s <-> 2s), rest mate         (g(x) = 19)
  --case g19AA        tau_(0,0) and tau_(0,1): both sign-preserving swap                             (g(x) = 19)
  --case g19AB        tau_(0,0) sign-preserving, tau_(0,1) sign-reversing swap                       (g(x) = 19)
"""
import argparse, itertools, time, sys
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

CL = range(7)
LABELS = [(c, s) for c in CL for s in (0, 1)]
mate = lambda l: (l[0], 1 - l[1])


def tau_case(case):
    tau = {a: {b: mate(b) for b in LABELS if b[0] != a[0]} for a in LABELS}

    def swap(a, preserve):
        for s in (0, 1):
            b, c = (1, s), (2, s if preserve else 1 - s)
            tau[a][b], tau[a][c] = c, b
    if case == 'g19A':
        swap((0, 0), True)
    elif case == 'g19AA':
        swap((0, 0), True); swap((0, 1), True)
    elif case == 'g19AB':
        swap((0, 0), True); swap((0, 1), False)
    elif case.startswith('spec:'):
        # spec:LABEL/J/K/P;...  e.g. spec:00/5/6/1;21/5/6/1  (label (0,0) swaps classes 5,6, sign-preserving=1)
        for item in case[5:].split(';'):
            lab, j, k, p = item.split('/')
            a = (int(lab[0]), int(lab[1])); j, k, p = int(j), int(k), int(p)
            for s_ in (0, 1):
                b, c = (j, s_), (k, s_ if p else 1 - s_)
                tau[a][b], tau[a][c] = c, b
    elif case != 'hamming':
        raise ValueError(case)
    for a in LABELS:
        for b, c in tau[a].items():
            assert tau[a][c] == b and c != b and c[0] != a[0]
    return tau


def build(tau, tight=True, srg=True):
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    V = ['x'] + LABELS + Xv
    pool = IDPool()
    cnf = CNF()
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
            (a,) = com
            (b,) = u - com
            (c,) = v - com
            return ('c', 1 if tau[a][b] == c else 0)
        return ('v', dvar(u, v))
    TAU = tau
    # degrees of X-vertices: 14 - 2 labels - 2 labelled = 10 disjoint
    for u in Xv:
        lits = [adj(u, w)[1] for w in Xv if w != u and adj(u, w)[0] == 'v']
        cnf.extend(CardEnc.equals(lits, 10, vpool=pool, encoding=EncType.seqcounter).clauses)
    # grids through x that exist under tau: classes {i,j} with tau mate between them in both directions
    grids = []
    for i, j in itertools.combinations(CL, 2):
        ok = all(tau[(i, s)][(j, r)] == (j, 1 - r) and tau[(j, r)][(i, s)] == (i, 1 - s) for s in (0, 1) for r in (0, 1))
        if ok:
            grids.append((i, j))
    for i, j in (grids if tight else []):
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
            if want < 0 or want > len(lits):
                cnf.append([])
            else:
                cnf.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
    # all SRG equations
    nV = len(V) if srg else 0
    bad = 0
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
                    cnf.append([]); bad += 1
                elif lits:
                    cnf.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
                elif want != 0:
                    cnf.append([]); bad += 1
            else:
                e = auv[1]
                for want, cond in ((1 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits):
                        cnf.append([-cond])
                        continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    return cnf, pool, D, grids, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--case', default='g19A')
    ap.add_argument('--notight', action='store_true')
    ap.add_argument('--nosrg', action='store_true', help='relaxed positive control: degrees + tightness only')
    a = ap.parse_args()
    tau = tau_case(a.case)
    t0 = time.time()
    cnf, pool, D, grids, bad = build(tau, tight=not a.notight, srg=not a.nosrg)
    print(f'case {a.case}: grids through x = {len(grids)}, fixed-part contradictions = {bad}, '
          f'{len(D)} unknowns, {pool.top} vars, {len(cnf.clauses)} clauses ({time.time()-t0:.1f}s)', flush=True)
    S = Cadical153(bootstrap_with=cnf.clauses)
    t1 = time.time()
    ok = S.solve()
    print('result:', 'SAT' if ok else 'UNSAT', f'({time.time()-t1:.1f}s)', flush=True)


if __name__ == '__main__':
    main()
