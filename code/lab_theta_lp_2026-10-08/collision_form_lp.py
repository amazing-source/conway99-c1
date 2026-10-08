"""C1, lab session, 2026-10-08. A linear collision bound of Codex written in my census, and maximised on the polytope.
  python collision_form_lp.py <census2 order-10 json> <codex bound json> <out json: the form in my parameters> [pcap]
Codex's file lists types by its own code: the adjacency of 9 vertices read row by row above the diagonal, first pair in
the least significant bit (checked: this decoding gives 39 graphs of minimum degree 3, all present in my order-9 census).
The form sum(coefficient * number of induced copies) becomes an affine form of the 549 census parameters. It is then
maximised (floating LP) with P <= pcap (default 0), first with the induced counts of orders 6 to 9 only, then with order
10 as well; the largest contributions at the optimum are printed. One process, below 2 GB."""
import sys, json, os, time, importlib.util
from fractions import Fraction as Fr
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import linprog
spec = importlib.util.spec_from_file_location("census2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2.py")); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
t0 = time.time(); C = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2])); npar = len(C["params"]); pcap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
def decode(code, n):
    rows = [0] * n; k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (code >> k) & 1: rows[i] |= 1 << j; rows[j] |= 1 << i
            k += 1
    return rows
tmap = {n: {t[0]: t for t in C["types"][str(n)]} for n in range(6, 11)}; form = {}; terms = []
for c in B["coefficients"]:
    n = 9; rows = decode(c["code"], n); key = c2.canon(n, rows)[0]; t = tmap[n][key]; aut = t[2] if t[2] is not None else c2.aut_order(n, t[1]); w = Fr(c["integer_coefficient"])
    f = {p: Fr(v) / aut for p, v in t[3].items()}; terms.append((c["code"], c["edges"], c["integer_coefficient"], f))
    for p, v in f.items(): form[p] = form.get(p, Fr(0)) + w * v
json.dump({"what": B.get("linear_bound"), "form": {p: str(v) for p, v in form.items() if v}}, open(sys.argv[3], "w"))
def polytope(orders):
    ri, ci, va, const = [], [], [], []; r = 0; seen = set()
    for n in orders:
        for key, rows, aut, fo in C["types"][n]:
            sig = tuple(sorted(fo.items()))
            if sig in seen or not fo: continue
            seen.add(sig); f = {int(p): float(Fr(v)) for p, v in fo.items()}; sc = max(abs(x) for x in f.values()); const.append(f.get(0, 0.0) / sc)
            for p, v in f.items():
                if p: ri.append(r); ci.append(p - 1); va.append(-v / sc)
            r += 1
    return csr_matrix((va, (ri, ci)), shape=(r, npar)), np.array(const)
def vec(f):
    c = np.zeros(npar)
    for p, v in f.items():
        if int(p): c[int(p) - 1] = float(v)
    return c, float(f.get("0", 0))
cF, kF = vec(form); bounds = [(0, pcap)] + [(0, None)] * (npar - 1)
for tag, orders in (("orders 6 to 9", ("6", "7", "8", "9")), ("orders 6 to 10", ("6", "7", "8", "9", "10"))):
    A, b = polytope(orders); o = linprog(-cF, A_ub=A, b_ub=b, bounds=bounds, method="highs-ipm")
    if o.status: print(tag, "LP status", o.status); continue
    x = o.x; val = cF @ x + kF; contrib = sorted(((float(w) * (vec(f)[0] @ x + vec(f)[1]), code, e, w) for code, e, w, f in terms), reverse=True)
    print("%s, P <= %g: maximum of the bound %.4g million   [%.0f s]" % (tag, pcap, val / 1e6, time.time() - t0), flush=True)
    print("   largest terms (millions, code, edges, coefficient): %s" % [(round(v / 1e6, 2), code, e, w) for v, code, e, w in contrib[:6]])
