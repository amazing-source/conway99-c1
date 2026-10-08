"""C1, lab session, 2026-10-08. A (6,6) line at P = S = 0: does each component admit its system of far triples?
  python comp66_triples.py [seconds per component]
NEW FACT USED (Codex's notes 125, 126 par.3 bis; re-derived): let L be a line whose cubic graph G(L) = Gamma[N(L)] has a
component C with 6 points in each layer (18 points), girth >= 5. Every far vertex w (60 of them) meets C in exactly 3
points (equilibrium); call it its triple. For n, n' in C, the number of far common neighbours is
K[n,n'] = (1 if n ~ n' else 2) - |common neighbours of n, n' inside the ball L + N(L)|, and it must equal the number of
triples containing {n, n'}. A triple has at most 2 points per layer, no mates, at most one G-edge, and K >= 1 on its pairs.
Question: for each of the 288 labelled (6,6) components of girth >= 5, is there a multiset of triples (multiplicity
0..2) with exactly these pair multiplicities? UNSAT for a component excludes it from any (6,6) line at P = S = 0.
CP-SAT, one process, a few seconds per component, memory < 1 GB. Only C is used (no shadows, no second component)."""
import sys, itertools, time
import networkx as nx
from ortools.sat.python import cp_model
lim = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
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
def cyc(Gr):
    c = {5: 0, 6: 0}
    for cy in nx.simple_cycles(Gr, length_bound=6):
        if len(cy) in c: c[len(cy)] += 1
    return (c[5], c[6], nx.girth(Gr))
t0 = time.time(); res = {}
for idx, Gr in enumerate(comps):
    V = sorted(Gr.nodes()); layer = {v: v[0] for v in V}
    isgedge = lambda a, b: Gr.has_edge(a, b)
    def ball_nb(v): return set(Gr[v]) | {("pt", layer[v])}
    K = {}
    bad = False
    for a, b in itertools.combinations(V, 2):
        k = (1 if isgedge(a, b) else 2) - len(ball_nb(a) & ball_nb(b))
        if k < 0: bad = True
        K[a, b] = K[b, a] = k
    rows = {v: sum(K[v, w] for w in V if w != v) for v in V}
    triples = []
    for T in itertools.combinations(V, 3):
        if any(K[a, b] < 1 for a, b in itertools.combinations(T, 2)): continue
        if max(sum(1 for v in T if layer[v] == L) for L in "xub") > 2: continue
        if sum(1 for a, b in itertools.combinations(T, 2) if isgedge(a, b)) > 1: continue
        if any(sum(1 for t in T if isgedge(v, t)) > (1 if v in T else 2) for v in V): continue   # mu / lambda between w and every x of C (Codex, 09/10 msg)
        triples.append(T)
    m = cp_model.CpModel(); x = [m.NewIntVar(0, 1, "") for _ in triples]   # two far vertices with the same triple would share 3 neighbours (mu = 2)
    cover = {}
    for i, T in enumerate(triples):
        for a, b in itertools.combinations(T, 2): cover.setdefault(frozenset((a, b)), []).append(i)
    infeasible_now = False
    for a, b in itertools.combinations(V, 2):
        lst = cover.get(frozenset((a, b)), [])
        if not lst and K[a, b] > 0: infeasible_now = True
        m.Add(sum(x[i] for i in lst) == K[a, b]) if lst else None
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = lim; sol.parameters.num_workers = 4
    st = "INFEASIBLE(pair uncovered)" if infeasible_now else sol.StatusName(sol.Solve(m))
    key = cyc(Gr) + (min(rows.values()), max(rows.values()), len(triples), bad)
    res.setdefault(key, {}); res[key][st] = res[key].get(st, 0) + 1
    if idx % 48 == 47: print("  %d components done  [%.0f s]" % (idx + 1, time.time() - t0), flush=True)
print("(c5, c6, girth, min row sum K, max row sum K, admissible triples, K<0?) : statuses")
for k_, v in sorted(res.items()): print("  %s : %s" % (k_, v))
