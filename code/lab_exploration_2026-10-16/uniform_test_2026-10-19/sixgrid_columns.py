"""Column part of the six-grid design (C1 NOTE 17.46), exhaustive (LAB 19/10/2026).
A line Theta in six grids G_k = Theta + X_k (k = 0..5): every vertex b far from Theta has exactly one neighbour v_k(b)
in each prism X_k, lying in column c_k(b) in {0,1,2} (the line of G_k through the point t_c of Theta).  Exact facts
(re-derived 19/10, see NOTE_ENONCE_RENFORCE_2026-10-19.md section 4):
  (C0) every far vertex uses each column exactly twice (mu(b, t_i) = 2), so c(b) is a labelled syntheme of the six
       grids (three duads, each labelled by a column): 90 possibilities;
  (C1) for every pair {k, j} and column i: exactly 4 far vertices have c_k = c_j = i (two prism vertices of the same
       column in different prisms have exactly 1 common far neighbour, 4 sign pairs);
  (C2) for every pair {k, j} and columns i != i': exactly 8 far vertices have (c_k, c_j) = (i, i') (2 common far
       neighbours, 4 sign pairs).
This enumerates all multisets of 60 labelled synthemes satisfying (C1), (C2), up to S_6 (grids) x S_3 (columns).
usage: python sixgrid_columns.py <out.json> [max_solutions]"""
import json
import sys
from itertools import combinations, permutations

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

OUT = sys.argv[1]
MAXSOL = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 7


def synthemes():
    pts = list(range(6))
    res = []

    def rec(rest, acc):
        if not rest:
            res.append(tuple(acc)); return
        a = rest[0]
        for b in rest[1:]:
            rec([x for x in rest if x not in (a, b)], acc + [(a, b)])
    rec(pts, [])
    return res


SYN = synthemes()
assert len(SYN) == 15
LS = []                                    # labelled synthemes as column vectors c[0..5]
for s in SYN:
    for lab in permutations(range(3)):
        c = [None] * 6
        for d, col in zip(s, lab):
            c[d[0]] = col; c[d[1]] = col
        LS.append(tuple(c))
assert len(set(LS)) == 90
pool = IDPool()
y = {(s, m): pool.id(('y', s, m)) for s in range(90) for m in range(1, 5)}
cl = []
for s in range(90):
    for m in range(1, 4):
        cl.append([-y[(s, m + 1)], y[(s, m)]])


def card_eq(lits, k):
    enc = CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter)
    cl.extend(enc.clauses)


for k, j in combinations(range(6), 2):
    for i in range(3):
        for i2 in range(3):
            lits = [y[(s, m)] for s in range(90) if LS[s][k] == i and LS[s][j] == i2 for m in range(1, 5)]
            card_eq(lits, 4 if i == i2 else 8)
# group S_6 x S_3 acting on labelled synthemes
G = []
for pg in permutations(range(6)):
    for pc in permutations(range(3)):
        img = []
        for s in range(90):
            c = LS[s]
            nc = [None] * 6
            for k in range(6):
                nc[pg[k]] = pc[c[k]]
            img.append(LS.index(tuple(nc)))
        G.append(img)


def canon(x):
    best = None
    for g in G:
        v = [0] * 90
        for s in range(90):
            v[g[s]] = x[s]
        t = tuple(v)
        if best is None or t > best:
            best = t
    return best


classes, nsol = {}, 0
with Cadical153(bootstrap_with=cl) as S:
    while S.solve() and nsol < MAXSOL:
        model = set(l for l in S.get_model() if l > 0)
        x = [sum(1 for m in range(1, 5) if y[(s, m)] in model) for s in range(90)]
        nsol += 1
        c = canon(x)
        classes.setdefault(c, 0)
        classes[c] += 1
        # block every image of this solution (whole orbit) to enumerate classes only
        for g in G:
            v = [0] * 90
            for s in range(90):
                v[g[s]] = x[s]
            block = []
            for s in range(90):
                for m in range(1, 5):
                    block.append(-y[(s, m)] if v[s] >= m else y[(s, m)])
            S.add_clause(block)
        print('solution', nsol, 'classes', len(classes), 'multiplicities', sorted(set(x)), flush=True)
out = {'classes': [{'x': list(c), 'labelled_synthemes': [list(LS[s]) for s in range(90) for _ in range(c[s])]}
                   for c in classes], 'n_classes': len(classes), 'complete': nsol < MAXSOL}
json.dump(out, open(OUT, 'w'))
print('done: %d classes up to S6 x S3, complete = %s' % (len(classes), out['complete']))
