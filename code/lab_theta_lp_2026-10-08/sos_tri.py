"""C1, lab session, 2026-10-08. First Cauchy-Schwarz ("sum of squares") cut on the census polytope: the variance of the
number n3(T) of prisms on a triangle T is >= 0. Floating point HiGHS, exploration.

  python sos_tri.py <census2 order-10 json>

sum_T n3(T) = 2 P and sum_T n3(T)^2 = 2 P + 2 N_TT, where N_TT = number of unordered pairs of distinct prisms sharing a
triangle (their union has exactly 9 vertices: two triangles matched to the same triangle cannot meet). N_TT is a linear
form in the order-9 type counts: N_TT = sum_H m(H) N_H, m(H) = number of (T, {T', T''}) in H with T, T', T'' covering H
and (T, T'), (T, T'') induced prisms. Cauchy-Schwarz over the 231 triangles: 2 P + 2 N_TT >= 4 P^2 / 231, a convex
constraint, entered as tangent cuts 2 N_TT + 2 P - (8 P0 / 231) P + 4 P0^2 / 231 >= 0 at successive optima P0.
Prints the maximum of P before and after, and the range of N_TT."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set()
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
cTT = np.zeros(npar); kTT = 0.0; used = 0
for key, rows, aut, form in D["types"]["9"]:
    tris = [t for t in combinations(range(9), 3) if rows[t[0]] >> t[1] & 1 and rows[t[0]] >> t[2] & 1 and rows[t[1]] >> t[2] & 1]
    if len(tris) < 3: continue
    def prism(T, U):                                                     # disjoint triangles joined by a perfect matching
        if set(T) & set(U): return False
        um = sum(1 << u for u in U); d = [bin(rows[t] & um).count("1") for t in T]
        tm = sum(1 << t for t in T); e = [bin(rows[u] & tm).count("1") for u in U]
        return d == [1, 1, 1] and e == [1, 1, 1]
    m = 0
    for T in tris:
        part = [U for U in tris if prism(T, U)]
        m += sum(1 for U, W in combinations(part, 2) if not set(U) & set(W))
    if not m: continue
    used += 1
    for p, v_ in form.items():
        val = float(Fr(v_)) * m / aut
        if int(p): cTT[int(p) - 1] += val
        else: kTT += val
print("N_TT: %d order-9 types contribute; constant term %.6g, %d parameters  [%.0f s]" % (used, kTT, int((cTT != 0).sum()), time.time() - t0), flush=True)
eP = np.zeros(npar); eP[0] = 1.0; cuts = []; cutb = []
def solve(c, sign):
    Aub, bub = -A, const
    if cuts: Aub = vstack([-A, csr_matrix(-np.array(cuts))]); bub = np.append(const, np.array(cutb))
    res = linprog(sign * c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * npar, method="highs-ipm")
    return (sign * res.fun, res.x) if res.status == 0 else (None, None)
v, x = solve(cTT, 1); print("without cuts: min N_TT = %.6g" % (v + kTT)); v, x = solve(cTT, -1); print("without cuts: max N_TT = %.6g (P = %.5g)" % (v + kTT, x[0]))
for it in range(12):
    v, x = solve(eP, -1); P0 = x[0]; ntt = cTT @ x + kTT; need = 2 * P0 * P0 / 231 - P0
    print("iteration %d: max P = %.6g, N_TT there = %.6g, Cauchy-Schwarz needs N_TT >= %.6g  [%.0f s]" % (it, P0, ntt, need, time.time() - t0), flush=True)
    if ntt >= need - 1e-6 * max(1.0, need): break
    # cut: 2 cTT.x + 2 kTT + 2 P - (8 P0/231) P + 4 P0^2/231 >= 0   <=>   -(2 cTT + (2 - 8 P0/231) eP).x <= 2 kTT + 4 P0^2/231
    cuts.append(2 * cTT + (2 - 8 * P0 / 231) * eP); cutb.append(2 * kTT + 4 * P0 * P0 / 231)
