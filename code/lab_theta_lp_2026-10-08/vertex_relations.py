"""C1, lab session, 2026-10-08. Relations mod 7 among the grids through ONE vertex, for every grid graph Xi on its 7 lines.
  python vertex_relations.py <codex-grid-hub-profiles.json>
NEW FACT USED: for y supported on the closed neighbourhood of v, (A + 4I) y is determined by y alone in ANY
srg(99,14,1,2): at z = c(a,b) in Gamma_2(v) it is y_a + y_b, at a on the line l it is 4 y_a + y_v + y_(mate of a), at v it
is 4 y_v + sum over the neighbours. So "(A + 4I) y = sum a_G 1_G + k 1 (mod 7) over the grids G through v" is a
linear system depending only on Xi: y is constant on each line minus v (value y_l), and
   (E1) y_l + y_l' = k                         for every pair of lines NOT spanning a grid,
        a_G = y_l + y_l' - k                    for every grid G = <l, l'>,
   (E2) 5 y_l + y_v = sum_{l' ~ l} (y_l + y_l' - k) + k      for every line l,
   (E3) 4 y_v + 2 sum_l y_l = sum_G a_G + k.
Solution space minus the trivial solution ((A+4I) y = const) = TRUE relations among the classes of the grids at v,
valid in every graph. A line in six grids contributes the pencil relation (y = 1 on the line). EXCESS = (dimension of
the non-trivial solutions with some a_G != 0, modulo those with all a_G = 0) - (number of lines in six grids).
Then the dimension count of profile_lp3.py is redone with  rho <= 18 + c' + x6 + sum_v excess(v)  (all vertex relations
assumed independent: favourable to the adversary), c' = relations NOT of this one-vertex type."""
import sys, json
from itertools import combinations
import networkx as nx, numpy as np
from scipy.optimize import linprog
def rank7(M):
    M = [[x % 7 for x in r] for r in M]; rk = 0; nc = len(M[0]) if M else 0
    for c in range(nc):
        p = next((i for i in range(rk, len(M)) if M[i][c]), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; inv = pow(M[rk][c], 5, 7); M[rk] = [(x * inv) % 7 for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % 7 for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def relations(G):
    # unknowns: y_v (0), y_l (1..7), k (8)
    rows = []; E = list(G.edges()); nonE = [e for e in combinations(range(7), 2) if not G.has_edge(*e)]
    for l, lp in nonE:
        r = [0] * 9; r[1 + l] = 1; r[1 + lp] = 1; r[8] = -1; rows.append(r)
    for l in range(7):
        d = G.degree(l); r = [0] * 9; r[1 + l] += 5 - d; r[0] += 1
        for lp in G[l]: r[1 + lp] -= 1
        r[8] += d - 1; rows.append(r)
    r = [0] * 9; r[0] = 4
    for l in range(7): r[1 + l] = 2 - G.degree(l)
    r[8] = len(E) - 1; rows.append(r)
    sol = 9 - rank7(rows)                                                      # all solutions (y, k)
    # those with every a_G = 0: add y_l + y_l' = k on the edges too
    rows0 = rows + [[(1 if j in (1 + l, 1 + lp) else 0) - (1 if j == 8 else 0) for j in range(9)] for l, lp in E]
    triv = 9 - rank7(rows0)
    return sol - triv
D = json.load(open(sys.argv[1])); prof = D["refined_profiles"]; degvecs = set(tuple(sorted(d)) for d in D["degree_vectors"])
exc = {}; stats = {}
for G in nx.graph_atlas_g():
    if G.number_of_nodes() != 7: continue
    deg = sorted(d for _, d in G.degree())
    if tuple(deg) not in degvecs: continue
    non = [e for e in combinations(range(7), 2) if not G.has_edge(*e)]
    if non and not any(not (set(a) & set(b)) for a, b in combinations(non, 2)): continue      # D1
    e = G.number_of_edges(); c = sum(d * (d - 1) // 2 for d in deg); h2 = sum(d >= 2 for d in deg); u6 = sum(d == 6 for d in deg)
    rel = relations(G); x = rel - u6; key = (e, c, h2, u6); exc[key] = max(exc.get(key, -9), x); stats[(rel, u6)] = stats.get((rel, u6), 0) + 1
print("graphs by (number of true one-vertex relations, number of lines in six grids): %s" % dict(sorted(stats.items())))
missing = [tuple(p) for p in prof if tuple(p) not in exc]; print("profiles of Codex without a graph in my list: %d" % len(missing))
pos = sorted((k_, v) for k_, v in exc.items() if v > 0); print("profiles (e, cherries, h2, u6) with a positive excess: %d of %d; examples %s" % (len(pos), len(exc), pos[:12]))
def solve(s, c, objective, withexc):
    cols = []
    for (e, ch, h2, u6) in prof:
        ins = 1 if e >= 14 else 0
        if ins and s == 0: continue
        x_ = max(exc.get((e, ch, h2, u6), 0), 0) if withexc else 0
        for d in range(0, min(s - ins, 14 if ins else 2 * h2) + 1): cols.append((e, ch, u6, ins, d, x_))
    n = len(cols); Ee = np.array([q[0] for q in cols], float); C = np.array([q[1] for q in cols], float); U = np.array([q[2] for q in cols], float); I = np.array([q[3] for q in cols], float); Dn = np.array([q[4] for q in cols], float); X = np.array([q[5] for q in cols], float)
    z = lambda *v: np.concatenate([np.zeros(n), v])
    A_eq = [np.concatenate([I, [0, 0]]), np.concatenate([1 - I, [0, 0]]), np.concatenate([Ee, [-9, 0]]), np.concatenate([Dn, [0, 0]]), np.concatenate([Dn * Dn + I * Dn, [0, 0]])]
    b_eq = [s, 99 - s, 0, 14 * s, 12 * s + 2 * s * s]
    A_ub = [np.concatenate([I * Dn, [0, 0]]), z(6, -1), z(5, 1), np.concatenate([-(2.0 * (U == 1) + 1.0 * (U == 2) - 3.0 * (U == 3)), [0, 0]]), np.concatenate([-U / 3 - X, [1, 0]])]
    b_ub = [3 * s + s * s / 9, 0, 1386, 0, 18 + c]
    r = linprog(np.concatenate([-C / 3, [0, 0]]), A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=[(0, None)] * n + [(0, 126), (0, 852)], method="highs")
    return None if r.status != 0 else (-r.fun, r.x[n], float((r.x[:n] * X).sum()))
print("  c' | max tau_g, vertex relations ignored | max tau_g with them (rho, number of vertex relations used) | 27 828 tau_g")
for c in (0, 4, 8, 10):
    a = max((solve(s, c, "tau_g", False) for s in range(0, 74)), key=lambda o: -1 if o is None else o[0]); b = max((solve(s, c, "tau_g", True) for s in range(0, 74)), key=lambda o: -1 if o is None else o[0])
    print("  %2d | %8.1f | %8.1f (rho %.1f, %.1f) | %.2fM %s" % (c, a[0], b[0], b[1], b[2], 27828 * b[0] / 1e6, "below 17.1M" if 27828 * b[0] < 17.1e6 else "ABOVE 17.1M"), flush=True)
