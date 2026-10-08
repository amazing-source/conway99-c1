"""C1, lab session, 2026-10-09. Coupling the rank-free catalogue of cores with the census (exact linear equations).
  python core_type_equations.py <twisted_core_check.json> <codex_unresolved_174_bits.json> <census2 order-10 json> <out json>
Unknowns added to the 549 census parameters: lambda_c >= 0, c = 1..174 = number of motifs S of the graph whose 14-vertex
core has type c (Codex's notes 221, 222: every motif has one of these 174 types).
For an abstract graph X of order 6 + j (j = 0..4) let m(X) = number of 6-subsets S0 of X inducing a motif such that every
other vertex of X has exactly two neighbours in S0, and for a core c let cnt_c(X) = number of j-subsets D' of its eight
doubles with S + D' isomorphic to X. Counting the pairs (motif S, j of its doubles inducing X with S) in two ways:
        m(X) N(X)  =  sum over c of lambda_c cnt_c(X),          N(X) = number of induced copies of X,
and N(X) is an exact affine form of the census parameters. j = 0 gives sum lambda_c = N_2. A type X with m(X) > 0 that
occurs in no surviving core gets N(X) = 0.
Self-check: for j = 1 the right-hand side is cnt(X) N_2 for every core, so m(X) N(X) - cnt(X) N_2 must vanish as a form.
Output: the list of equations (census form, lambda coefficients). Exact rational arithmetic; no solver."""
import sys, json, os, time, importlib.util
from fractions import Fraction as Fr
from itertools import combinations
spec = importlib.util.spec_from_file_location("census2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2.py")); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
t0 = time.time(); D = json.load(open(sys.argv[1])); keep = set(json.load(open(sys.argv[2]))); C = json.load(open(sys.argv[3]))
SUP = {6: (0, 3), 7: (1, 4), 8: (2, 3), 9: (2, 4), 10: (0, 5), 11: (1, 5), 12: (2, 5), 13: (2, 5)}
BASE = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4)] + [(d, s) for d, sp in SUP.items() for s in sp]
def key_of(vertices, edges):
    pos = {v: i for i, v in enumerate(vertices)}; rows = [0] * len(vertices)
    for u, v in edges:
        if u in pos and v in pos: rows[pos[u]] |= 1 << pos[v]; rows[pos[v]] |= 1 << pos[u]
    return c2.canon(len(vertices), rows)[0]
def motif_mask(rows, n, mask):
    six = [v for v in range(n) if mask >> v & 1]; deg = sorted(bin(rows[v] & mask).count("1") for v in six)
    if deg != [2, 2, 3, 3, 3, 3]: return False
    tri = [t for t in combinations(six, 3) if rows[t[0]] >> t[1] & 1 and rows[t[0]] >> t[2] & 1 and rows[t[1]] >> t[2] & 1]
    if len(tri) != 2 or set(tri[0]) & set(tri[1]): return False
    return sum(1 for a in tri[0] for b in tri[1] if rows[a] >> b & 1) == 2
def m_of(rows, n):
    m = 0; full = (1 << n) - 1
    for six in combinations(range(n), 6):
        mask = sum(1 << v for v in six)
        if all(bin(rows[v] & mask).count("1") == 2 for v in range(n) if not mask >> v & 1) and motif_mask(rows, n, mask): m += 1
    return m
surv = [c for c in D["cores"] if c["bits"] in keep]; assert len(surv) == 174
cnt = {j: {} for j in range(5)}                                           # j -> key -> {core index: count}
for ci, c in enumerate(surv):
    edges = BASE + [tuple(e) for e in c["edges_among_doubles"]]
    for j in range(5):
        for sub in combinations(range(6, 14), j):
            k = key_of(list(range(6)) + list(sub), edges); cnt[j].setdefault(k, {}); cnt[j][k][ci] = cnt[j][k].get(ci, 0) + 1
rows_out = []; stats = {}
N2 = None
for j in range(5):
    n = 6 + j; nz = 0; absent = 0
    for key, rows, aut, form in C["types"][str(n)]:
        if min(bin(r).count("1") for r in rows) < 2: continue                    # every vertex of "S + doubles" has degree >= 2
        m = m_of(rows, n)
        if not m: continue
        if aut is None: aut = c2.aut_order(n, rows)
        f = {p: Fr(v) * m / aut for p, v in form.items()}; lam = cnt[j].get(key, {})
        if j == 0: N2 = {p: v / m for p, v in f.items()}
        if j == 1:                                                              # self-check: cnt is the same for every core
            vals = set(lam.get(ci, 0) for ci in range(174)); assert len(vals) == 1, "j = 1 count depends on the core"
            v0 = vals.pop(); diff = {p: f.get(p, 0) - v0 * N2.get(p, 0) for p in set(f) | set(N2)}; assert all(v == 0 for v in diff.values()), ("self-check failed", key, diff)
        rows_out.append({"order": n, "key": key, "m": m, "p": {p: str(v) for p, v in f.items() if v}, "lam": {str(ci): v for ci, v in lam.items()}}); nz += 1; absent += (not lam)
    miss = set(cnt[j]) - {r["key"] for r in rows_out if r["order"] == n}; assert not miss, ("core pattern not found among the census types", j, len(miss))
    stats[n] = (nz, absent); print("order %d: %d types of the form 'motif + %d doubles', of which %d occur in no surviving core   [%.0f s]" % (n, nz, j, absent, time.time() - t0), flush=True)
json.dump({"nlam": 174, "rows": rows_out, "what": "m(X) N(X) = sum_c lambda_c cnt_c(X); 'p' = census form of the left side (key 0 = constant), 'lam' = cnt_c(X)"}, open(sys.argv[4], "w"))
print("equations written: %d (self-check for one double passed); N_2 form %s" % (len(rows_out), {p: str(v) for p, v in N2.items()}))
