"""C1, lab session, 2026-10-08. TARGETED census above order 10, by the same triangular recursion as census2.py, top-down
with memoisation, on top of the full order-10 census.

  python census_target.py <census2 order-10 json> <target> [seconds] [out json]
  targets: prism+house (order 11), prism+prism (order 12), prism+edge (order 8, control), prism+triangle (order 9, control)

x_H (embeddings) for the target H = disjoint anticomplete union of the two named graphs:
    x_H = c(S) x_G - sum over admissible strict supersets S' of S of x_(G + S'),   G = H - u, u of degree <= 2, S = N(u).
Types of order > 10 with minimum degree >= 3 become new parameters. The closure (all types met) is reported; the
counts of all closure types are >= 0, which gives the constraints used afterwards.
Why: tau = number of unordered pairs of disjoint anticomplete prisms = N(prism + prism); 12 tau <= N(prism + house).
Stops cleanly when the time budget is exceeded (the closure is then incomplete and nothing is concluded)."""
import sys, json, time
from fractions import Fraction as Fr
import census2 as C2
sys.setrecursionlimit(100000)
t0 = time.time(); D = json.load(open(sys.argv[1])); target = sys.argv[2]; budget = float(sys.argv[3]) if len(sys.argv) > 3 else 240.0
V, K = D["v"], D["k"]; npar0 = len(D["params"])
base = {}                                                                # (order, key) -> form {param: Fraction}
for n, lst in D["types"].items():
    for key, rows, aut, form in lst: base[(int(n), key)] = {int(p): Fr(v_) for p, v_ in form.items()}
base[(1, 0)] = {0: Fr(V)}
memo = {}; newparams = []; rowsof = {}
class Timeout(Exception): pass


def x_of(n, rows):
    key, perm = C2.canon(n, rows)
    if n <= 10: return base[(n, key)]
    if (n, key) in memo: return memo[(n, key)]
    if time.time() - t0 > budget: raise Timeout()
    rows = C2.relabel(n, rows, perm); rowsof[(n, key)] = rows
    deg = [bin(r).count("1") for r in rows]; u = min(range(n), key=lambda i: deg[i])
    if deg[u] >= 3:
        newparams.append((n, key)); memo[(n, key)] = {npar0 + len(newparams): Fr(C2.aut_order(n, rows))}; return memo[(n, key)]
    keep = [i for i in range(n) if i != u]; pos = {i: p for p, i in enumerate(keep)}; m = n - 1; g = [0] * m
    for i in keep:
        r = rows[i] & ~(1 << u); acc = 0
        while r:
            low = r & -r; r ^= low; acc |= 1 << pos[low.bit_length() - 1]
        g[pos[i]] = acc
    S = 0
    for i in keep:
        if rows[u] >> i & 1: S |= 1 << pos[i]
    mem = [i for i in range(m) if S >> i & 1]
    if len(mem) == 0: c = V - m
    elif len(mem) == 1: c = K - bin(g[mem[0]]).count("1")
    else: c = (1 if g[mem[0]] >> mem[1] & 1 else 2) - bin(g[mem[0]] & g[mem[1]]).count("1")
    acc = {p: c * val for p, val in x_of(m, g).items()}
    for S2 in C2.admissible_sets(m, g, S):
        if S2 == S: continue
        for p, val in x_of(n, C2.extend(m, g, S2)).items(): acc[p] = acc.get(p, 0) - val
    acc = {p: val for p, val in acc.items() if val}; memo[(n, key)] = acc; return acc


PRISM = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]
PARTS = {"house": (5, [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4), (4, 0)]), "prism": (6, PRISM), "edge": (2, [(0, 1)]), "triangle": (3, [(0, 1), (0, 2), (1, 2)])}
a, b = target.split("+"); (na, ea), (nb, eb) = PARTS[a], PARTS[b]; n = na + nb; rows = [0] * n
for i, j in ea: rows[i] |= 1 << j; rows[j] |= 1 << i
for i, j in eb: rows[na + i] |= 1 << (na + j); rows[na + j] |= 1 << (na + i)
try:
    form = x_of(n, rows); aut = C2.aut_order(n, rows)
    print("target %s (order %d): closure %d types above order 10, %d new parameters, |Aut| = %d  [%.0f s]" % (target, n, len(memo), len(newparams), aut, time.time() - t0))
    print("N(target) = x / |Aut|: constant term %s; %d parameters of order <= 10 and %d new ones involved" % (form.get(0, 0) / aut, len([p for p in form if 0 < p <= npar0]), len([p for p in form if p > npar0])))
    if len(sys.argv) > 4:
        json.dump({"target": target, "aut": aut, "form": {str(p): str(v_) for p, v_ in form.items()}, "newparams": [[nn, kk, list(rowsof[(nn, kk)])] for nn, kk in newparams],
                   "closure": [[nn, kk, {str(p): str(v_) for p, v_ in f.items()}] for (nn, kk), f in memo.items()]}, open(sys.argv[4], "w"))
        print("written", sys.argv[4])
except Timeout:
    print("TIME BUDGET EXCEEDED after %.0f s: %d types met so far, %d new parameters; nothing concluded" % (time.time() - t0, len(memo), len(newparams)))
