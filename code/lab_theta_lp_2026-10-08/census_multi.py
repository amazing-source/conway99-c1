"""C1, lab session, 2026-10-08. Targeted census above order 10 for MANY targets at once: prism + F (disjoint, anticomplete)
for every admissible type F of the given orders; shared memoisation. Same recursion as census_target.py.
  python census_multi.py <census2 order-10 json> <orders of F, e.g. 5 or 5,6> <seconds> <out json>
Output: the closure (all types above order 10 met, with their embedding forms) and the new parameters. The positivity of
the closure types gives extra constraints on the order-10 parameters (through the new ones); lp_multi.py uses them."""
import sys, json, time
from fractions import Fraction as Fr
import census2 as C2
sys.setrecursionlimit(100000)
t0 = time.time(); D = json.load(open(sys.argv[1])); orders = [int(x) for x in sys.argv[2].split(",")]; budget = float(sys.argv[3])
V, K = D["v"], D["k"]; npar0 = len(D["params"]); base = {}
for n, lst in D["types"].items():
    for key, rows, aut, form in lst: base[(int(n), key)] = {int(p): Fr(v_) for p, v_ in form.items()}
base[(1, 0)] = {0: Fr(V)}; memo = {}; newparams = []; rowsof = {}
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
PRISM = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]; done = 0
try:
    for o in orders:
        for key, rowsF, aut, form in D["types"][str(o)]:
            n = 6 + o; rows = [0] * n
            for i, j in PRISM: rows[i] |= 1 << j; rows[j] |= 1 << i
            for i in range(o): rows[6 + i] = rowsF[i] << 6
            x_of(n, rows); done += 1
        print("prism + all %d types of order %d done: closure %d types, %d new parameters  [%.0f s]" % (len(D["types"][str(o)]), o, len(memo), len(newparams), time.time() - t0), flush=True)
except Timeout: print("TIME BUDGET EXCEEDED: %d targets done, closure %d types, %d new parameters (partial closure still gives valid constraints)" % (done, len(memo), len(newparams)), flush=True)
json.dump({"newparams": [[nn, kk] for nn, kk in newparams], "closure": [[nn, kk, {str(p): str(v_) for p, v_ in f.items()}] for (nn, kk), f in memo.items()]}, open(sys.argv[4], "w"))
print("written", sys.argv[4])
