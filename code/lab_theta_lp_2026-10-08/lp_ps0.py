"""C1, lab session, 2026-10-08. Is P = S = 0 compatible with the order-10 census polytope?
  python lp_ps0.py <census2 order-10 json>
NEW FACT USED: S (Codex's notes 125, 126; L18) = number of type-(ii) 4-cycles of the cubic graphs G(L), i.e. of copies of
the 7-vertex configuration Z2: two lines {p,q,r}, {p,n0,n1} through p, and n2 ~ q, n1, n3; n3 ~ r, n0, n2 (11 edges;
induced: n2 has one neighbour on {p,q,r}, and n2 ~ n0 would put the edge n0n1 in two triangles). The residual case of
note 126 par.3 ter ("(6,6) everywhere") lives at P = S = 0. Here: minimum of the number of induced Z2 over the order-10
census polytope with P = 0 (floating HiGHS; exploration). If it is positive, P = S = 0 is impossible."""
import sys, json
from fractions import Fraction as Fr
import numpy as np, networkx as nx
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
D = json.load(open(sys.argv[1])); npar = len(D["params"])
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
def graph(n, rows): return nx.Graph([(i, j) for i in range(n) for j in range(i + 1, n) if rows[i] >> j & 1])
hits = [(key, rows, aut, form) for key, rows, aut, form in D["types"]["7"] if nx.is_isomorphic(graph(7, rows), Z2)]
print("order-7 census types isomorphic to Z2: %d" % len(hits))
key, rows, aut, form = hits[0]; aut_ = aut if aut else None
c = np.zeros(npar); k0 = 0.0
for p, v_ in form.items():
    if int(p): c[int(p) - 1] = float(Fr(v_))
    else: k0 = float(Fr(v_))
print("form: constant %s, %d parameters, |Aut| %s" % (form.get("0", 0), len(form) - ("0" in form), aut))
for label, bnd in (("P free", (0, None)), ("P = 0", (0, 0))):
    bounds = [(0, None)] * npar; bounds[0] = bnd
    for sgn in (1, -1):
        res = linprog(sgn * c, A_ub=-A, b_ub=const, bounds=bounds, method="highs-ipm")
        val = sgn * res.fun + k0 if res.status == 0 else None
        print("%s: %s of the Z2 form = %s  (status %d)" % (label, "minimum" if sgn == 1 else "maximum", "%.6g" % val if val is not None else res.message[:60], res.status), flush=True)
