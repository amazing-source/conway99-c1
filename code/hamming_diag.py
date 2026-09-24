"""Hamming point, isometric case (sigma_x in Aut): reduction of fact C (notes/40) to the diagonal shifts.

Every isometry phi_{PP''} of the 4-cycles Q_P -> Q_P'' commutes with the antipodal map, hence induces a shift
delta(P, P'') in F_2 on the two diagonals {00,11}, {01,10}.  Fact C (mu between grids sharing a class) implies:
for every class i and pair {j,k} of other classes, exactly 3 of the 6 pairs P'' in [7] - {i,j,k} have
delta(ij, P'') != delta(ik, P'')  (the six images of a point of Q_ij in Q_ik are: same i-sign once each,
opposite i-sign twice each, i.e. 3 in each diagonal).
Question: is this reduced system (105 bits) already contradictory?  Also: the same for one class i only.
Usage: hamming_diag.py [all|one]
"""
import itertools, sys
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

pairs = [frozenset(p) for p in itertools.combinations(range(7), 2)]
pool = IDPool()
def d(P, Q):
    return pool.id(('d', min(tuple(sorted(P)), tuple(sorted(Q))), max(tuple(sorted(P)), tuple(sorted(Q)))))

def build(classes):
    cnf = CNF()
    for i in classes:
        others = [c for c in range(7) if c != i]
        for j, k in itertools.combinations(others, 2):
            P, Pp = frozenset((i, j)), frozenset((i, k))
            rest = [c for c in range(7) if c not in (i, j, k)]
            zs = []
            for m, n in itertools.combinations(rest, 2):
                Q = frozenset((m, n))
                a, b = d(P, Q), d(Pp, Q)
                z = pool.id(('z', i, j, k, m, n))
                # z <-> a xor b
                cnf.extend([[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]])
                zs.append(z)
            card = CardEnc.equals(lits=zs, bound=3, vpool=pool, encoding=EncType.seqcounter)
            cnf.extend(card.clauses)
    return cnf

mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
cnf = build(range(7) if mode == 'all' else [0])
with Cadical153(bootstrap_with=cnf.clauses) as s:
    r = s.solve()
    print(mode, 'vars', pool.top, 'clauses', len(cnf.clauses), '->', 'SAT' if r else 'UNSAT')
    if r:
        model = set(l for l in s.get_model() if l > 0)
        vals = {}
        for P in pairs:
            for Q in pairs:
                if not (P & Q) and tuple(sorted(P)) < tuple(sorted(Q)):
                    vals[(tuple(sorted(P)), tuple(sorted(Q)))] = int(d(P, Q) in model)
        print('ones:', sum(vals.values()), 'of', len(vals))
