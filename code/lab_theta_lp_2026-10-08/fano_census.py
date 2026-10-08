"""C1, lab session, 2026-10-08. A cap on the Fano vectors from the census: a_7 <= (2/21) N(F10).

  python fano_census.py <census2 order-10 json>

A Fano configuration (P, Q) is the incidence graph of the biplane 2-(7,4,2): 7 + 7 vertices, 4-regular bipartite, induced.
Removing two blocks and the two points common to them leaves an induced bipartite graph F10 on 5 + 5 vertices with 16
edges and minimum degree 3 (degrees 3,3,3,3,4 on each side): a special 10-support. Each Fano configuration contains 21
induced copies of F10 (one per pair of blocks). Two different Fano configurations cannot share a copy: the two Fano
vectors, oriented alike on the copy, would share a positive vertex and three of its negative neighbours, against the
seed-packing lemma. Hence (number of Fano configurations) = a_7 / 2 <= N(F10) / 21.
This script finds F10 among the parameters of the order-10 census and maximises N(F10) over the order-10 polytope
(floating point HiGHS: exploration; an exact certificate is needed before use). It also lists the other induced
sub-configurations of the Fano configuration that are special supports of order <= 10, with their multiplicity."""
import sys, json, time, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import census2 as C2
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
adj14 = [0] * 14                                                         # points 0..6, blocks 7..13; point i ~ block j iff i not on line j
for j, L in enumerate(LINES):
    for i in range(7):
        if i not in L: adj14[i] |= 1 << (7 + j); adj14[7 + j] |= 1 << i
assert all(bin(x).count("1") == 4 for x in adj14)
pc = lambda x: bin(x).count("1")
def induced(S):
    S = list(S); pos = {v: p for p, v in enumerate(S)}; rows = [0] * len(S)
    for v in S:
        for u in S:
            if adj14[v] >> u & 1: rows[pos[v]] |= 1 << pos[u]
    return rows
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); pid = {(n, key): i for i, (n, key, rows) in enumerate(D["params"])}
found = {}
for size in (6, 7, 8, 9, 10):
    for S in itertools.combinations(range(14), size):
        rows = induced(S)
        if min(pc(x) for x in rows) < 3: continue
        key, _ = C2.canon(size, rows); found.setdefault((size, key), 0); found[(size, key)] += 1
print("special sub-supports of the Fano configuration (order, parameter index, edges, copies per configuration):")
for (size, key), cnt in sorted(found.items()):
    rows = D["params"][pid[(size, key)]][2]; print("   order %d, parameter %d, %d edges: %d copies" % (size, pid[(size, key)], sum(pc(x) for x in rows) // 2, cnt))
ri = []; ci = []; va = []; const = []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values())
        const.append(f.get(0, 0.0) / sc)
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)
for (size, key), cnt in sorted(found.items()):
    c = np.zeros(npar); c[pid[(size, key)]] = 1.0
    res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    mx = -res.fun; print("   order %d, parameter %d: maximum of its number of copies %.8g  =>  a_7 <= 2 * max / %d = %.6g  [%.0f s]" % (size, pid[(size, key)], mx, cnt, 2 * mx / cnt, time.time() - t0), flush=True)
