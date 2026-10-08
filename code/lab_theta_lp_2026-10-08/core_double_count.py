"""C1, lab session, 2026-10-09. Codex's double count over ALL motifs S, written in the census (its message of about 22:40 UTC).
  python core_double_count.py <census2 order-10 json> <out json>
S = two disjoint triangles joined by exactly two edges; D(S) = its 8 vertices with two neighbours in S; e(D(S)) = number
of edges inside D(S). Then  T = sum over S of e(D(S))  = number of triples (S, d, d') with d ~ d' both in D(S), which is a
sum of counts of induced subgraphs of order 8:  T = sum over types X of order 8 of m(X) N(X), m(X) = number of ways to
read X as "a motif plus two adjacent vertices having exactly two neighbours each in it". N(X) is an exact affine form of
the 549 census parameters, so T is one too. Likewise N_2 = number of motifs (expected 4158 - 3 P, P = number of prisms).
Output: the forms, and the range of T, of the mean T / N_2 and of T - 4 N_2 over the census polytope (all induced counts
of orders 6 to 10 non-negative, with or without the two parameters 58, 59 that the 174 cores force to zero).
Floating LP for the ranges (diagnostic); the forms are exact."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import linprog
t0 = time.time(); C = json.load(open(sys.argv[1])); npar = len(C["params"])
def is_motif(rows, six):
    sub = {v: [w for w in six if rows[v] >> w & 1] for v in six}
    if sorted(len(x) for x in sub.values()) != [2, 2, 3, 3, 3, 3]: return False
    tri = [t for t in combinations(six, 3) if all(rows[a] >> b & 1 for a, b in combinations(t, 2))]
    if len(tri) != 2 or set(tri[0]) & set(tri[1]): return False
    return sum(1 for a in tri[0] for b in tri[1] if rows[a] >> b & 1) == 2
def addform(acc, form, mult):
    for p, v in form.items(): acc[p] = acc.get(p, Fr(0)) + Fr(v) * mult
T = {}; N2 = {}; used = 0
for key, rows, aut, form in C["types"]["6"]:
    if is_motif(rows, list(range(6))): addform(N2, form, Fr(1, aut))
for key, rows, aut, form in C["types"]["8"]:
    m = 0
    for six in combinations(range(8), 6):
        if not is_motif(rows, list(six)): continue
        d, e = [v for v in range(8) if v not in six]
        if rows[d] >> e & 1 and all(sum(1 for w in six if rows[x] >> w & 1) == 2 for x in (d, e)): m += 1
    if m: addform(T, form, Fr(m, aut)); used += 1
print("order-8 types contributing to T: %d; N_2 form: %s" % (used, {p: str(v) for p, v in sorted(N2.items(), key=lambda kv: int(kv[0])) if v}))
print("T form (%d terms): %s" % (len([1 for v in T.values() if v]), {p: str(v) for p, v in sorted(T.items(), key=lambda kv: int(kv[0])) if v}))
ri, ci, va, const = [], [], [], []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in C["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v)) for p, v in form.items()}; sc = max(abs(x) for x in f.values()); const.append(f.get(0, 0.0) / sc)
        for p, v in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(-v / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); b = np.array(const)
def vec(form):
    c = np.zeros(npar)
    for p, v in form.items():
        if int(p): c[int(p) - 1] = float(v)
    return c, float(form.get("0", 0))
cT, kT = vec(T); cN, kN = vec(N2); res = {"T_form": {p: str(v) for p, v in T.items() if v}, "N2_form": {p: str(v) for p, v in N2.items() if v}, "ranges": {}}
for tag, zero in (("census positivity only", []), ("with parameters 58, 59 = 0", [58, 59])):
    bounds = [(0, 0) if (i + 1) in zero else (0, None) for i in range(npar)]; out = {}
    for name, c, k in (("T", cT, kT), ("N_2", cN, kN), ("T - 4 N_2", cT - 4 * cN, kT - 4 * kN), ("T - N_2", cT - cN, kT - kN)):
        lo = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs-ipm"); hi = linprog(-c, A_ub=A, b_ub=b, bounds=bounds, method="highs-ipm")
        out[name] = [None if lo.status else round(lo.fun + k, 1), None if hi.status else round(-hi.fun + k, 1)]
    res["ranges"][tag] = out; print("%s: %s" % (tag, out), flush=True)
json.dump(res, open(sys.argv[2], "w"), indent=0); print("[%.0f s]" % (time.time() - t0))
