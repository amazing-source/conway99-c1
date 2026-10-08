"""C1, lab session, 2026-10-08. A (6,6) line at P = S = 0: JOINT far-vertex system of its two components.
  python comp66_joint.py <i> <j> [mode lp|sat] [seconds]      (i, j = orbit representatives 0..14 of x30c's 15 types)
NEW FACT USED: the 60 far vertices w of a (6,6) line L each meet C_1 and C_2 in a triple (equilibrium), with
 - layers: the shadow T_1 + T_2 has exactly 2 points in each layer;
 - pair multiplicities: inside C_k, K as in comp66_triples.py; across (n in C_1, n' in C_2): K = 1 if same layer, else 2
   (only p can be a common neighbour in the ball; mu = 2);
 - two far vertices share at most 2 shadow points (mu = 2): every 3-set of N(L) lies in at most one shadow;
 - the shadow's G-edges form a matching (no edge inside T_1 meets... automatically: at most one per triple).
Variables z[T_1, T_2] (0/1) over layer-compatible pairs; x_k[T] = sum of z. LP relaxation (HiGHS) or CP-SAT.
UNSAT/infeasible for a pair of types excludes that pair at P = S = 0. One process; memory below 2 GB."""
import sys, itertools, time
import numpy as np, networkx as nx
labels = list(range(6)); mate = {i: i ^ 1 for i in labels}
def matchings(ls):
    if not ls: yield {}; return
    a = ls[0]
    for b in ls[1:]:
        if b == mate[a]: continue
        rest = [c for c in ls if c not in (a, b)]
        for m in matchings(rest):
            d = dict(m); d[a] = b; d[b] = a; yield d
M = list(matchings(labels)); good = []
for tu in M:
    for tb in M:
        for perm in itertools.permutations(labels):
            s = dict(zip(labels, perm))
            if all(s[v] not in (v, mate[v], tu[v], tb[v]) for v in labels) and all(tb[s[w]] != s[tu[w]] for w in labels): good.append((tu, tb, s))
G48 = []
for p in itertools.permutations(range(3)):
    for flips in itertools.product((0, 1), repeat=3):
        g = {}
        for c in range(3):
            for e in (0, 1): g[2 * c + e] = 2 * p[c] + (e ^ flips[c])
        G48.append(g)
def key(cfg): return tuple(tuple(f[i] for i in labels) for f in cfg)
def act(g, cfg):
    gi = {v: k for k, v in g.items()}; return tuple({i: g[f[gi[i]]] for i in labels} for f in cfg)
seen = set(); reps = []
for cfg in good:
    k = key(cfg)
    if k in seen: continue
    seen |= {key(act(g, cfg)) for g in G48}; reps.append(cfg)
def comp_graph(cfg, tag):
    tu, tb, s = cfg; Gr = nx.Graph()
    for v in labels:
        Gr.add_edge(('x', tag, v), ('x', tag, mate[v])); Gr.add_edge(('u', tag, v), ('u', tag, tu[v])); Gr.add_edge(('b', tag, v), ('b', tag, tb[v]))
        Gr.add_edge(('x', tag, v), ('u', tag, v)); Gr.add_edge(('x', tag, v), ('b', tag, v)); Gr.add_edge(('u', tag, v), ('b', tag, s[v]))
    return Gr
def comp_data(Gr):
    V = sorted(Gr.nodes()); K = {}
    nb = {v: set(Gr[v]) | {("pt", v[0])} for v in V}
    for a, b in itertools.combinations(V, 2):
        K[a, b] = K[b, a] = (1 if Gr.has_edge(a, b) else 2) - len(nb[a] & nb[b])
    T = [t for t in itertools.combinations(V, 3) if all(K[a, b] >= 1 for a, b in itertools.combinations(t, 2))
         and max(sum(1 for v in t if v[0] == L) for L in "xub") <= 2 and sum(1 for a, b in itertools.combinations(t, 2) if Gr.has_edge(a, b)) <= 1
         and all(sum(1 for x in t if Gr.has_edge(v, x)) <= (1 if v in t else 2) for v in V)]   # mu / lambda between w and every x of C
    return V, K, T
if __name__ == "__main__":
    i, j = int(sys.argv[1]), int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "lp"; lim = float(sys.argv[4]) if len(sys.argv) > 4 else 200
    t0 = time.time(); G1 = comp_graph(reps[i], 1); G2 = comp_graph(reps[j], 2)
    V1, K1, T1 = comp_data(G1); V2, K2, T2 = comp_data(G2)
    lay = lambda t: tuple(sum(1 for v in t if v[0] == L) for L in "xub")
    by2 = {}
    for b, t in enumerate(T2): by2.setdefault(lay(t), []).append(b)
    pairs = [(a, b) for a, t in enumerate(T1) for b in by2.get(tuple(2 - c for c in lay(t)), [])]
    print("types %d, %d: %d + %d admissible triples, %d layer-compatible pairs  [%.0f s]" % (i, j, len(T1), len(T2), len(pairs), time.time() - t0), flush=True)
    # constraint rows
    rows = []; rhs = []; sense = []
    idx1 = {}; idx2 = {}
    for q, (a, b) in enumerate(pairs): idx1.setdefault(a, []).append(q); idx2.setdefault(b, []).append(q)
    def addrow(qs, val, s): rows.append(qs); rhs.append(val); sense.append(s)
    for (V, K, T, idx) in ((V1, K1, T1, idx1), (V2, K2, T2, idx2)):
        cov = {}
        for a, t in enumerate(T):
            for u, v in itertools.combinations(t, 2): cov.setdefault(frozenset((u, v)), []).extend(idx.get(a, []))
        for u, v in itertools.combinations(V, 2): addrow(cov.get(frozenset((u, v)), []), K[u, v], "=")
        for a in range(len(T)): addrow(idx.get(a, []), 1, "<")                                  # each triple at most once
    cross = {}
    for q, (a, b) in enumerate(pairs):
        for n in T1[a]:
            for n2 in T2[b]: cross.setdefault((n, n2), []).append(q)
    for n in V1:
        for n2 in V2: addrow(cross.get((n, n2), []), 1 if n[0] == n2[0] else 2, "=")
    three = {}
    for q, (a, b) in enumerate(pairs):
        for (A, B) in ((T1[a], T2[b]), (T2[b], T1[a])):
            for u, v in itertools.combinations(A, 2):
                for w in B: three.setdefault((frozenset((u, v)), w), []).append(q)
    for qs in three.values(): addrow(qs, 1, "<")                                                # 3-sets in at most one shadow
    print("rows: %d  [%.0f s]" % (len(rows), time.time() - t0), flush=True)
    if mode == "lp":
        from scipy.optimize import linprog
        from scipy.sparse import csr_matrix
        eq = [k for k in range(len(rows)) if sense[k] == "="]; ub = [k for k in range(len(rows)) if sense[k] == "<"]
        def mat(ks):
            r_ = []; c_ = []
            for t, k in enumerate(ks):
                for q in rows[k]: r_.append(t); c_.append(q)
            return csr_matrix((np.ones(len(r_)), (r_, c_)), shape=(len(ks), len(pairs)))
        res = linprog(np.zeros(len(pairs)), A_eq=mat(eq), b_eq=[rhs[k] for k in eq], A_ub=mat(ub), b_ub=[rhs[k] for k in ub], bounds=(0, 1), method="highs")
        print("LP relaxation: status %d (%s)  [%.0f s]" % (res.status, res.message[:50], time.time() - t0))
    else:
        from ortools.sat.python import cp_model
        m = cp_model.CpModel(); z = [m.NewBoolVar("") for _ in pairs]
        for k in range(len(rows)):
            e = sum(z[q] for q in rows[k])
            if sense[k] == "=": m.Add(e == rhs[k])
            else: m.Add(e <= rhs[k])
        sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = lim; sol.parameters.num_workers = 4; sol.parameters.max_memory_in_mb = 2000
        st = sol.Solve(m); print("CP-SAT: %s  [%.0f s]" % (sol.StatusName(st), time.time() - t0))
