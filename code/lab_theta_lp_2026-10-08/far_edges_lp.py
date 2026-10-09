"""C1, lab session, 2026-10-09. The far set of a cubic 8-support seen by the census of order 10.
  python far_edges_lp.py <census2 order-10 json> <out json> [pcap]
Fact used (Codex, bridge message of 00:40 UTC; equality case of Cauchy-Schwarz in sum d_U d_V = 128): two ANTICOMPLETE
induced cubic 8-sets U, V always have the same projection, so the pairs of cubic supports with the same projection are
exactly the anticomplete pairs, and V is then a component of the graph induced on Z(U) = outside vertices with no
neighbour in U (NOTE 17.75). A twin of U therefore puts 12 edges inside Z(U), and
      number of ordered pairs (U, twin of U)  <=  N(U + K_2) / 12,
where U + K_2 (disjoint union, no edge between) is an induced type of order 10, whose count is an exact affine form of
the census parameters. Likewise N(U + K_1) = sum over U of |Z(U)| <= 23 N(U).
This script writes these forms for the three admissible cubic types of order 8 and gives, on the census polytope with
P <= pcap (default 0), the range of N(U + K_2), of N(U + K_2) - 12 N(U) and of N(U + K_1) - 23 N(U).
Floating LP (diagnostic); the forms are exact. One process, below 2 GB."""
import sys, json, os, time, importlib.util
from fractions import Fraction as Fr
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import linprog
spec = importlib.util.spec_from_file_location("census2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2.py")); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
t0 = time.time(); C = json.load(open(sys.argv[1])); npar = len(C["params"]); pcap = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
tmap = {n: {t[0]: t for t in C["types"][str(n)]} for n in range(6, 11)}
def decode(code, n):
    rows = [0] * n; k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (code >> k) & 1: rows[i] |= 1 << j; rows[j] |= 1 << i
            k += 1
    return rows
def copies(n, rows):
    key = c2.canon(n, rows)[0]
    if key not in tmap[n]: return None
    t = tmap[n][key]; aut = t[2] if t[2] is not None else c2.aut_order(n, t[1]); return {p: Fr(v) / aut for p, v in t[3].items()}
def polytope():
    ri, ci, va, const = [], [], [], []; r = 0; seen = set()
    for n in ("6", "7", "8", "9", "10"):
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
def comb(*terms):
    out = {}
    for w, f in terms:
        for p, v in f.items(): out[p] = out.get(p, Fr(0)) + w * v
    return out
A, b = polytope(); bounds = [(0, pcap)] + [(0, None)] * (npar - 1); out = {}
def rng(f):
    c, k = vec(f); lo = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs-ipm"); hi = linprog(-c, A_ub=A, b_ub=b, bounds=bounds, method="highs-ipm")
    return (None if lo.status else lo.fun + k, None if hi.status else -hi.fun + k, None if hi.status else hi.x)
for code in (2022000, 5683824, 5691760):
    rows = decode(code, 8); f8 = copies(8, rows); f9 = copies(9, rows + [0]); f10e = copies(10, rows + [1 << 9, 1 << 8]); f10n = copies(10, rows + [0, 0])
    if f9 is None or f10e is None: print("type %d: U + K_1 or U + K_2 not among the census types" % code); continue
    out[str(code)] = {k_: {p: str(v) for p, v in f.items() if v} for k_, f in (("N8", f8), ("N9_plus_K1", f9), ("N10_plus_K2", f10e), ("N10_plus_2K1", f10n or {}))}
    r8 = rng(f8); rZ = rng(comb((1, f9), (-23, f8))); rE = rng(f10e); rD = rng(comb((1, f10e), (-12, f8))); c8, k8 = vec(f8); cE, kE = vec(f10e); c9, k9 = vec(f9)
    print("type %d: N(U) in [%.0f, %.0f]; N(U + K_1) - 23 N(U) in [%.0f, %.0f]; N(U + K_2) in [%.0f, %.0f]; N(U + K_2) - 12 N(U) in [%.0f, %.0f]   [%.0f s]" % (
        code, r8[0], r8[1], rZ[0], rZ[1], rE[0], rE[1], rD[0], rD[1], time.time() - t0), flush=True)
    x = r8[2]; n8 = c8 @ x + k8
    print("     at the point where N(U) is largest (%.0f): mean |Z(U)| = %.2f, mean number of edges inside Z(U) = %.2f" % (n8, (c9 @ x + k9) / n8, (cE @ x + kE) / n8), flush=True)
    x = rE[2]; n8 = c8 @ x + k8
    print("     at the point where N(U + K_2) is largest: N(U) = %.0f, mean number of edges inside Z(U) = %s" % (n8, "%.2f" % ((cE @ x + kE) / n8) if n8 > 1 else "-"), flush=True)
json.dump(out, open(sys.argv[2], "w"))
