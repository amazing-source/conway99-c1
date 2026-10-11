"""General Z_3-covers of BH (voltage delta added to the BvLS voltage), table-constraint model.
delta: Z_3-valued on oriented edges, zero sum on every line-triangle, gauge-fixed to 0 on a BFS spanning tree.
srg condition: for every non-adjacent fibre pair the 6 path values base_i + delta(PZ_i) + delta(Z_iR) are
equidistributed in Z_3.   Usage: python3 zcover.py SEED LIMIT TAG [uniform]"""
import sys, time, collections, itertools, numpy as np
from ortools.sat.python import cp_model
from cover import *
from lib243 import *
seed, limit, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
uniform = len(sys.argv) > 4 and sys.argv[4] == "uniform"
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0]) for P in range(n)]
from lines_model import PTS, IDX, add, HS
hd = HS[0]
# fibre coordinates: point base + t*h_d has coordinate t
fcoord = {}
for i, f in enumerate(fib):
    base = PTS[f[0]]
    for t in range(3): fcoord[IDX[add(base, hd, t)]] = (i, t)
fpts = [[IDX[add(PTS[f[0]], hd, t)] for t in range(3)] for f in fib]
def bvls_volt(P, R):
    """BvLS matching P->R is t -> t + c."""
    p0 = fpts[P][0]; q = [x for x in fpts[R] if A[p0, x]][0]
    return fcoord[q][1]
m = cp_model.CpModel()
D = {}
for P in range(n):
    for R in nb[P]:
        if P < R:
            D[(P, R)] = m.NewIntVar(0, 2, "")
def dv(P, R):
    return (D[(P, R)], 1) if P < R else (D[(R, P)], -1)
# gauge
tree = []; seen = {0}; dq = collections.deque([0])
while dq:
    u = dq.popleft()
    for v in sorted(nb[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: m.Add(D[(min(u, v), max(u, v))] == 0)
# triangles: oriented sum zero
def sum_table(signs, const, target_set):
    """allowed assignments for vars with given signs such that (const + sum s_i x_i) mod 3 in target_set"""
    out = []
    for xs in itertools.product(range(3), repeat=len(signs)):
        if (const + sum(s * x for s, x in zip(signs, xs))) % 3 in target_set: out.append(list(xs))
    return out
for P in range(n):
    for R in nb[P]:
        if R <= P: continue
        for S in nb[P] & nb[R]:
            if S <= R: continue
            vs = [dv(P, R), dv(R, S), dv(S, P)]
            m.AddAllowedAssignments([v for v, _ in vs], sum_table([s for _, s in vs], 0, {0}))
# Latin condition
eq90 = [list(t) for t in itertools.product(range(3), repeat=6) if sorted(t) == [0, 0, 1, 1, 2, 2]]
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        vals = []
        for Z in sorted(nb[P] & nb[R]):
            base = (bvls_volt(P, Z) + bvls_volt(Z, R)) % 3
            (x1, s1), (x2, s2) = dv(P, Z), dv(Z, R)
            v = m.NewIntVar(0, 2, "")
            tab = [[a, b, (base + s1 * a + s2 * b) % 3] for a in range(3) for b in range(3)]
            m.AddAllowedAssignments([x1, x2, v], tab); vals.append(v)
        m.AddAllowedAssignments(vals, eq90)
if uniform:   # voltage change constant along each Q-line (affine re-ruling)
    for P in range(n):
        for R in nb[P]:
            for S in nb[P] & nb[R]:
                (x1, s1), (x2, s2) = dv(P, R), dv(R, S)
                m.AddAllowedAssignments([x1, x2], [[a, b] for a in range(3) for b in range(3) if (s1 * a - s2 * b) % 3 == 0])
def graph_of(sol):
    G = np.zeros((243, 243), dtype=np.int64)
    for f in fpts:
        for a, b in itertools.combinations(f, 2): G[a, b] = G[b, a] = 1
    for (P, R), var in D.items():
        c = (bvls_volt(P, R) + sol[(P, R)]) % 3
        for t in range(3):
            a = fpts[P][t]; b = fpts[R][(t + c) % 3]; G[a, b] = G[b, a] = 1
    return G
known = {canon_g6(A): "BvLS", canon_g6(load_edges("twin243_switched.edges")): "twin"}
try:
    import pickle; known.update(pickle.load(open("zclasses.pkl", "rb")))
except Exception:
    pass
t0 = time.time(); k = 0
while k < limit:
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 3600
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("status", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True); break
    sol = {e: s.Value(v) for e, v in D.items()}
    G = graph_of(sol); k += 1
    c = canon_g6(G); name = known.get(c); fresh = name is None
    if fresh:
        name = f"Z{len(known) - 1}"; known[c] = name; np.save(f"{tag}_{name}.npy", G)
        pickle.dump(known, open("zclasses.pkl", "wb"))
    o, orb, gens = aut(G)
    print(f"[{time.time()-t0:.0f}s] sol {k}: srg={is_srg(G)} class={name}{' NEW' if fresh else ''} |Aut|={o} "
          f"#orbits={len(orb)} nonzero-delta={sum(1 for v in sol.values() if v)}", flush=True)
    m.AddBoolOr([D[e] != sol[e] for e in D] if False else [])
    # block this exact assignment
    bl = []
    for e, v in D.items():
        b = m.NewBoolVar(""); m.Add(v != sol[e]).OnlyEnforceIf(b); m.Add(v == sol[e]).OnlyEnforceIf(b.Not()); bl.append(b)
    m.AddBoolOr(bl)
