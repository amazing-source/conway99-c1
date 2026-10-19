"""SAT model of 'a line in six grids' (C1 NOTE 17.46), LAB 19/10/2026.  Equivalent to: an srg(99,14,1,2) has a line
Theta lying in six 3x3 grids G_k = Theta + X_k.  Re-derived facts (NOTE_ENONCE_RENFORCE_2026-10-19.md section 4):
  * the 60 vertices b far from Theta have one neighbour v_k(b) in each prism X_k; name x(b) = (x_0..x_5), x_k in 0..5,
    x_k = 2 * column + row (column i: the line of G_k through t_i; row: which of the two rows of X_k besides Theta);
  * (N1) each column is used exactly twice in a name (mu(b, t_i) = 2);
  * (N2) for k != j: #{b : x_k = v, x_j = v'} = 1 if col v = col v', 2 otherwise (blocks of prism vertices meet in
    lambda/mu - [same column]);  hence every block has 10 names;
  * (N3) two names agree in at most 2 coordinates (common neighbours);
  stage B (--graph): the graph on the far vertices,
  * (G1) for each b, k: exactly one neighbour of b has the same x_k  (lambda(b, v_k(b)) = 1; the M_k partner);
  * (G2) for each b, k and value v != x_k(b): the number of neighbours of b with x_k = v is 1 if v is adjacent to
    x_k(b) in the prism (same column or same row), 2 otherwise  (lambda / mu between b and the prism vertex);
  * (G3) for b != b': agreements(b, b') + common far neighbours = 1 if adjacent, 2 if not;  degree 8.
Conversely (N1)-(N3) + (G1)-(G3) give the strongly regular graph, so UNSAT of stage A or B excludes a line in six
grids.  Symmetry breaking: names are distinct (N3), so they can be sorted; the first two coordinates are then fixed by
(N2) up to relabelling names (group of 10 per x_0 value, sorted x_1 pattern 1,1,2,2,2,2 per value).  The remaining
coordinate/value symmetries are not used.
usage: python sixgrid_sat.py <out.json> <cpu seconds> [--graph] [--no-n3] [--dump=FILE.cnf]"""
import json
import sys
import threading
import time
from itertools import combinations

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

OUT, CPU = sys.argv[1], float(sys.argv[2])
GRAPH = '--graph' in sys.argv
NO_N3 = '--no-n3' in sys.argv          # control: drop (N3)
DUMP = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--dump=')), None)
NB, NK, NV = 60, 6, 6
col = lambda v: v // 2
row = lambda v: v % 2
pool = IDPool()
cl = []


def eq(lits, k):
    cl.extend(CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)


def atmost(lits, k):
    cl.extend(CardEnc.atmost(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)


X = {(b, k, v): pool.id(('X', b, k, v)) for b in range(NB) for k in range(NK) for v in range(NV)}
for b in range(NB):
    for k in range(NK):
        eq([X[(b, k, v)] for v in range(NV)], 1)
    for i in range(3):
        eq([X[(b, k, v)] for k in range(NK) for v in range(NV) if col(v) == i], 2)
# symmetry breaking: coordinate 0 sorted, coordinate 1 fixed sorted pattern inside each block of coordinate 0
fixed = {}
b = 0
for v0 in range(NV):
    pat = []
    for v1 in range(NV):
        pat += [v1] * (1 if col(v1) == col(v0) else 2)
    assert len(pat) == 10
    for v1 in pat:
        fixed[b] = (v0, v1); b += 1
for b, (v0, v1) in fixed.items():
    cl.append([X[(b, 0, v0)]]); cl.append([X[(b, 1, v1)]])
# (N2) pair intersections, with AND variables
Z = {}
for k, j in combinations(range(NK), 2):
    for v in range(NV):
        for w in range(NV):
            lits = []
            for b in range(NB):
                z = pool.id(('Z', b, k, v, j, w))
                cl.extend([[-z, X[(b, k, v)]], [-z, X[(b, j, w)]], [z, -X[(b, k, v)], -X[(b, j, w)]]])
                lits.append(z)
            eq(lits, 1 if col(v) == col(w) else 2)
# (N3) agreements
A = {}
for b, c in combinations(range(NB), 2):
    for k in range(NK):
        a = pool.id(('A', b, c, k))
        A[(b, c, k)] = a
        ors = []
        for v in range(NV):
            y = pool.id(('Y', b, c, k, v))
            cl.extend([[-y, X[(b, k, v)]], [-y, X[(c, k, v)]], [y, -X[(b, k, v)], -X[(c, k, v)]]])
            cl.append([a, -y]); ors.append(y)
        cl.append([-a] + ors)
    if not NO_N3:
        atmost([A[(b, c, k)] for k in range(NK)], 2)
if GRAPH:
    E = {}
    for b, c in combinations(range(NB), 2):
        E[(b, c)] = E[(c, b)] = pool.id(('E', b, c))
    for b in range(NB):
        eq([E[(b, c)] for c in range(NB) if c != b], 8)
        for k in range(NK):
            # (G1) exactly one neighbour with the same x_k
            lits = []
            for c in range(NB):
                if c == b:
                    continue
                key = (min(b, c), max(b, c), k)
                t = pool.id(('G1', b, c, k))
                cl.extend([[-t, E[(b, c)]], [-t, A[key]], [t, -E[(b, c)], -A[key]]])
                lits.append(t)
            eq(lits, 1)
            # (G2) neighbours of b in the block (k, v), v != x_k(b), as a function of the prism adjacency
            for u in range(NV):          # u = x_k(b)
                for v in range(NV):
                    if v == u:
                        continue
                    need = 1 if (col(u) == col(v) or row(u) == row(v)) else 2
                    lits = []
                    for c in range(NB):
                        if c == b:
                            continue
                        t = pool.id(('G2', b, c, k, v))
                        cl.extend([[-t, E[(b, c)]], [-t, X[(c, k, v)]], [t, -E[(b, c)], -X[(c, k, v)]]])
                        lits.append(t)
                    # conditional cardinality: if X[b,k,u] then sum(lits) == need
                    sel = X[(b, k, u)]
                    enc = CardEnc.equals(lits=lits, bound=need, vpool=pool, encoding=EncType.seqcounter)
                    for clause in enc.clauses:
                        cl.append(clause + [-sel])
    # (G3) common neighbours
    for b, c in combinations(range(NB), 2):
        common = []
        for d in range(NB):
            if d in (b, c):
                continue
            t = pool.id(('C', b, c, d))
            cl.extend([[-t, E[(b, d)]], [-t, E[(c, d)]], [t, -E[(b, d)], -E[(c, d)]]])
            common.append(t)
        ag = [A[(b, c, k)] for k in range(NK)]
        # adjacent: ag + common == 1 ; non-adjacent: == 2
        for clause in CardEnc.equals(lits=ag + common, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses:
            cl.append(clause + [-E[(b, c)]])
        for clause in CardEnc.equals(lits=ag + common, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses:
            cl.append(clause + [E[(b, c)]])
nvars = pool.top
if DUMP:
    with open(DUMP, 'w') as f:
        f.write('p cnf %d %d\n' % (nvars, len(cl)))
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('dumped', DUMP, nvars, len(cl)); sys.exit(0)
t0 = time.process_time()
res = {'graph': GRAPH, 'variables': nvars, 'clauses': len(cl)}
with Cadical153(bootstrap_with=cl) as S:
    timer = threading.Timer(CPU, S.interrupt); timer.start()
    r = S.solve_limited(expect_interrupt=True)
    timer.cancel()
    res['status'] = {True: 'SAT', False: 'UNSAT', None: 'UNKNOWN'}[r]
    res['cpu'] = round(time.process_time() - t0, 1)
    if r:
        m = set(l for l in S.get_model() if l > 0)
        names = [[next(v for v in range(NV) if X[(b, k, v)] in m) for k in range(NK)] for b in range(NB)]
        res['names'] = names
        if GRAPH:
            res['edges'] = [[b, c] for b, c in combinations(range(NB), 2) if E[(b, c)] in m]
json.dump(res, open(OUT, 'w'))
print(json.dumps({k: v for k, v in res.items() if k not in ('names', 'edges')}))
