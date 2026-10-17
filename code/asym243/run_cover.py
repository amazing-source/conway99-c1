"""Enumerate S3-covers of BH (gauge fixed on a BFS spanning tree to agree with BvLS); analyse each on the fly."""
import sys, time, pickle, collections
from cover import *
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 30
A = load_edges("bvls243.edges"); B = load_edges("twin243_switched.edges")
fib = fibres_of(A, 0); ok, Qadj = is_cover(A, fib)
# BFS spanning tree of Q
tree = []; seen = {0}; dq = collections.deque([0])
while dq:
    u = dq.popleft()
    for v in np.nonzero(Qadj[u])[0]:
        if v not in seen: seen.add(v); dq.append(v); tree.append((min(u, v), max(u, v)))
fix = {e: A[np.ix_(fib[e[0]], fib[e[1]])] for e in tree}
m, X, E = cover_model(A, fib, Qadj, fix_edges=fix)
known = {canon_g6(A): "BvLS", canon_g6(B): "twin"}
t0 = time.time(); found = []
while len(found) < limit:
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 3600
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("status", s.StatusName(r), f"{time.time()-t0:.0f}s"); break
    G = graph_from_X(s, X, fib)
    c = canon_g6(G); name = known.get(c)
    eps = parity_cocycle(G, fib, Qadj); cob = is_coboundary(eps, 81)
    o, orb, gens = aut(G)
    if name is None:
        name = f"new{len(known)-1}"; known[c] = name
    print(f"[{time.time()-t0:.0f}s] sol {len(found)+1}: srg={is_srg(G)} iso={name} |Aut|={o} "
          f"orbits={sorted(len(x) for x in orb)[:8]}{'...' if len(orb)>8 else ''} parity_coboundary={cob}", flush=True)
    found.append(G)
    np.save(f"cover_s{seed}_{len(found)}.npy", G)
    sel = [X[(p, q)] for (p, q) in X if p < q and G[p, q]]
    m.AddBoolOr([v.Not() for v in sel])
