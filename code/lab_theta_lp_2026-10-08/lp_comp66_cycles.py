"""C1, lab session, 2026-10-08. The residual case "(6,6) everywhere" (Codex's note 126 par.3 ter) against the census.
  python lp_comp66_cycles.py <census2 order-10 json>
NEW FACTS USED: (a) G(L) = Gamma[N(L)] (each vertex of N(L) has its mate and one neighbour in each other layer), so
F_k := sum over the 231 lines of the number of k-cycles of G(L) is a census form: sum over the induced types H of order
3 + k of N_H times the number of (triangle T of H, Hamiltonian k-cycle on the other k vertices, each of them adjacent
to exactly one vertex of T). (b) In "(6,6) everywhere" at P = S = 0 every G(L) is the disjoint union of two of the 15
types of 18-vertex components of girth >= 5 (Codex's x30c_comp66_girth5_orbits.py, re-run here), so F_5 and F_6 lie in
231 * [min, max] of c_k(C_1) + c_k(C_2). Test: range of F_5, F_6 over the order-10 census polytope with P = 0 and no Z2
(S = 0). Floating HiGHS; exploration. Disjoint ranges would exclude "(6,6) everywhere"."""
import sys, json, itertools
from fractions import Fraction as Fr
import numpy as np, networkx as nx
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
# ---- (b) the 15 types of (6,6) components with girth >= 5 (same construction as x30c)
labels = list(range(6)); mate = {i: i ^ 1 for i in labels}
def matchings(ls):
    if not ls: yield {}; return
    a = ls[0]
    for b in ls[1:]:
        if b == mate[a]: continue
        rest = [c for c in ls if c not in (a, b)]
        for m in matchings(rest):
            d = dict(m); d[a] = b; d[b] = a; yield d
M = list(matchings(labels)); comps = []
for tu in M:
    for tb in M:
        for perm in itertools.permutations(labels):
            s = dict(zip(labels, perm))
            if all(s[v] not in (v, mate[v], tu[v], tb[v]) for v in labels) and all(tb[s[w]] != s[tu[w]] for w in labels):
                Gr = nx.Graph()
                for v in labels:
                    Gr.add_edge(('x', v), ('x', mate[v])); Gr.add_edge(('u', v), ('u', tu[v])); Gr.add_edge(('b', v), ('b', tb[v]))
                    Gr.add_edge(('x', v), ('u', v)); Gr.add_edge(('x', v), ('b', v)); Gr.add_edge(('u', v), ('b', s[v]))
                comps.append(Gr)
def cyc_counts(Gr):
    cnt = {5: 0, 6: 0}
    for c in nx.simple_cycles(Gr, length_bound=6):
        if len(c) in cnt: cnt[len(c)] += 1
    return cnt
vals = sorted({(cyc_counts(Gr)[5], cyc_counts(Gr)[6], nx.girth(Gr)) for Gr in comps})
print("labelled components: %d; distinct (c5, c6, girth): %s" % (len(comps), vals))
c5s = sorted({a + b for (a, _, _) in vals for (b, _, _) in vals}); c6s = sorted({a + b for (_, a, _) in vals for (_, b, _) in vals})
print("per (6,6) line: c5 in [%d, %d], c6 in [%d, %d]; times 231: F5 in [%d, %d], F6 in [%d, %d]" % (
    c5s[0], c5s[-1], c6s[0], c6s[-1], 231 * c5s[0], 231 * c5s[-1], 231 * c6s[0], 231 * c6s[-1]), flush=True)
# ---- (a) census forms of F5, F6
D = json.load(open(sys.argv[1])); npar = len(D["params"])
def graph(n, rows): return [[(rows[i] >> j) & 1 for j in range(n)] for i in range(n)]
def ham_cycles(adj, vs):
    vs = list(vs); k = len(vs); first = vs[0]; cnt = 0
    for perm in itertools.permutations(vs[1:]):
        if perm[0] > perm[-1]: continue
        seq = (first,) + perm
        if all(adj[seq[i]][seq[(i + 1) % k]] for i in range(k)): cnt += 1
    return cnt
forms = {}
for k in (5, 6):
    n = 3 + k; acc = np.zeros(npar); k0 = 0.0; used = 0
    for key, rows, aut, form in D["types"][str(n)]:
        adj = graph(n, rows); tot = 0
        for T in itertools.combinations(range(n), 3):
            a, b, c = T
            if not (adj[a][b] and adj[a][c] and adj[b][c]): continue
            rest = [v for v in range(n) if v not in T]
            if any(sum(adj[v][t] for t in T) != 1 for v in rest): continue
            tot += ham_cycles(adj, rest)
        if not tot: continue
        used += 1
        au = aut if aut else 1
        for p, v_ in form.items():
            val = float(Fr(v_)) * tot / au
            if int(p): acc[int(p) - 1] += val
            else: k0 += val
    forms[k] = (acc, k0); print("F%d: %d census types of order %d contribute; constant %.6g" % (k, used, n, k0), flush=True)
# ---- LP: P = 0, Z2 = 0
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
Z2 = nx.Graph([("p", "q"), ("p", "r"), ("q", "r"), ("p", "n0"), ("p", "n1"), ("n0", "n1"), ("q", "n2"), ("n1", "n2"), ("r", "n3"), ("n0", "n3"), ("n2", "n3")])
def nxg(n, rows): return nx.Graph([(i, j) for i in range(n) for j in range(i + 1, n) if rows[i] >> j & 1])
z2 = [form for key, rows, aut, form in D["types"]["7"] if nx.is_isomorphic(nxg(7, rows), Z2)][0]
bounds = [(0, None)] * npar; bounds[0] = (0, 0)
for p in z2:
    if int(p): bounds[int(p) - 1] = (0, 0)
for k in (5, 6):
    acc, k0 = forms[k]
    for sgn in (1, -1):
        res = linprog(sgn * acc, A_ub=-A, b_ub=const, bounds=bounds, method="highs-ipm")
        print("P = S = 0: %s F%d = %s" % ("min" if sgn == 1 else "max", k, "%.6g" % (sgn * res.fun + k0) if res.status == 0 else res.message[:60]), flush=True)

# joint test: per component 2 c5 + c6 is 16 or 18 (see the table above), so 2 F5 + F6 must lie in [231 * 32, 231 * 36]
acc = 2 * forms[5][0] + forms[6][0]; k0 = 2 * forms[5][1] + forms[6][1]
for sgn in (1, -1):
    res = linprog(sgn * acc, A_ub=-A, b_ub=const, bounds=bounds, method="highs-ipm")
    print("P = S = 0: %s of 2 F5 + F6 = %s  (needed for (6,6) everywhere: [%d, %d])" % ("min" if sgn == 1 else "max", "%.6g" % (sgn * res.fun + k0), 231 * 32, 231 * 36), flush=True)
