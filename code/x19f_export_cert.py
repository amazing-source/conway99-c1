r"""X19f -- export one block-level (P2) infeasibility certificate for independent verification.
Configuration: the first locally admissible maximal-torsion (tau, sigma) of seed 1 (X19 'random 1').
Writes data/x19_cert_s1_c1.json:
  tau, sigma (labels "c.s"; sigma pairs (v, w) mean {c.0, v} ~ {c.1, w}),
  rows: list of {name, rhs}; y: exact rationals (strings), one per row;
  claim: for EVERY pair z and EVERY label-realisable class-level type t of z,
         col(z,t) . y  <=  max(0, col(z,t) . y)  and  b . y - sum_z max_t max(0, col(z,t).y) > 0,
  i.e. no point x in [0,1]^n (in fact none with sum_t x[z,t] = 1) satisfies A x = b.
Row names: conv|z ; bal|R|R' ; lab|u|R ; P2|R|R'  (blocks as 'cd', pairs as 'c.s-d.t')."""
import sys, json, random, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import hstack, identity
sys.path.insert(0, 'scripts')
import x19_block_lp_generic as X
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible

fmt = lambda l: f'{l[0]}.{l[1]}'
bn = lambda R: ''.join(str(c) for c in sorted(R))
pn = lambda y: '-'.join(fmt(l) for l in sorted(y))

rng = random.Random(1)
while True:
    tau = {u: random_tau(u, rng) for u in LAB}
    sigma = {c: random_sigma(c, rng) for c in range(7)}
    if all(admissible(build([frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2)
                             for s in (0, 1) for t in (0, 1)], tau, sigma))
           for tri in itertools.combinations(range(7), 3)):
        break
built, msg = X.build_lp(tau, sigma, True)
A, b, nv, T = built
m = A.shape[0]
names = [f'conv|{pn(z)}' for z in X.PAIRS]
names += [f'bal|{bn(R)}|{bn(Rp)}' for R, Rp in itertools.combinations(X.BLOCKS, 2)]
names += [f'lab|{fmt(u)}|{bn(R)}' for u in LAB for R in X.BLOCKS if u[0] not in R]
names += [f'P2|{bn(R)}|{bn(Rp)}' for R, Rp in itertools.combinations_with_replacement(X.BLOCKS, 2)]
assert len(names) == m, (len(names), m)
I = identity(m, format='csr')
res = linprog(np.concatenate([np.zeros(nv), np.ones(2 * m)]), A_eq=hstack([A, I, -I]).tocsr(), b_eq=b,
              bounds=[(0, 1)] * nv + [(0, None)] * (2 * m), method='highs')
y = res.eqlin.marginals
yq = [Fr(v).limit_denominator(10 ** 6) for v in y]
# exact check (same as x19b)
Acoo = A.tocoo()
col = [Fr(0)] * nv
for i, j, v in zip(Acoo.row, Acoo.col, Acoo.data):
    if yq[i]:
        col[j] += yq[i] * int(round(v))
val = sum(yq[i] * int(round(b[i])) for i in range(m)) - sum(x for x in col if x > 0)
print('phase-1 value', res.fun, ' exact Farkas value', float(val), val > 0)
out = dict(
    note=__doc__,
    tau={fmt(u): [[fmt(v), fmt(w)] for v, w in tau[u].items() if v < w] for u in LAB},
    sigma={str(c): [[fmt(v), fmt(w)] for v, w in sigma[c].items()] for c in range(7)},
    rows=[dict(name=names[i], rhs=int(round(b[i]))) for i in range(m)],
    y=[str(q) for q in yq],
    farkas_value=str(val),
    types_per_pair={pn(z): [{bn(R): mm for R, mm in t.items()} for t in T[z]] for z in X.PAIRS})
json.dump(out, open('data/x19_cert_s1_c1.json', 'w'))
print('written data/x19_cert_s1_c1.json')
