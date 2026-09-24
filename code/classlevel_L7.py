"""Class-level system behind L7 (Hamming point + sigma_x automorphism => all phi isometries).
For each unordered pair {P, R} of disjoint class pairs (105), a perfect matching between P and R (2 choices, m=0: sorted
order p0-r0, p1-r1 ; m=1: crossed). Fact C forces, for every class i and j < k (both != i):
   #{R subset [7]-{i,j,k}, |R| = 2 : partner of i in M({i,j},R) == partner of i in M({i,k},R)}  in {2, 4, 6}.
Question: is this purely combinatorial system satisfiable?  (If not: human-checkable proof skeleton for L7.)
"""
import itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
C7 = range(7)
PAIRS = list(itertools.combinations(C7, 2))
pool = IDPool(); cnf = []
key = lambda P, R: (P, R) if P < R else (R, P)
m = lambda P, R: pool.id(('m',) + key(P, R))
def partner_is(i, P, R, r):
    """literal meaning: in M(P,R), class i (in P) is matched to r (in R)."""
    A, B = key(P, R)
    if P == A:
        idx_i, idx_r = P.index(i), R.index(r)
    else:
        idx_i, idx_r = P.index(i), R.index(r)
        # matching variable refers to (A,B)=(R,P): straight pairs A[k]-B[k]
    # straight (m=0) pairs A[k]-B[k]; i at position idx_i in P, r at idx_r in R -> straight iff idx_i == idx_r
    v = m(P, R)
    return -v if idx_i == idx_r else v
nparity = 0
for i in C7:
    others = [c for c in C7 if c != i]
    for j, k in itertools.combinations(others, 2):
        S = [c for c in C7 if c not in (i, j, k)]
        eqs = []
        for R in itertools.combinations(S, 2):
            P1, P2 = tuple(sorted((i, j))), tuple(sorted((i, k)))
            e = pool.id(('eq', i, j, k, R))
            # e <-> exists r in R: partner1 = r and partner2 = r ; partner in R is determined by one bit each
            r0, r1 = R
            a0, b0 = partner_is(i, P1, R, r0), partner_is(i, P2, R, r0)   # i -> r0 in each
            # equal iff (a0 and b0) or (not a0 and not b0)
            cnf += [[-e, -a0, b0], [-e, a0, -b0], [e, a0, b0], [e, -a0, -b0]]
            eqs.append(e)
        # count in {2,4,6}: parity even (xor chain) and at least 2
        par = eqs[0]
        for q in eqs[1:]:
            p = pool.id(('x', i, j, k, q)); cnf += [[-p, par, q], [-p, -par, -q], [p, -par, q], [p, par, -q]]; par = p
        cnf.append([-par])
        cnf += CardEnc.atleast(eqs, 2, vpool=pool, encoding=EncType.seqcounter).clauses
        nparity += 1
S = Cadical153(bootstrap_with=cnf)
print('class-level system:', nparity, 'conditions, 105 matching variables ->', 'SAT' if S.solve() else 'UNSAT')
