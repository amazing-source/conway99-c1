import time
from cover import *
A = load_edges("bvls243.edges"); B = load_edges("twin243_switched.edges")
fib = fibres_of(A, 0); ok, Qadj = is_cover(A, fib)
t = time.time()
# sanity: fix everything to BvLS -> feasible ; fix to twin -> feasible
for name, M in (("BvLS", A), ("twin", B)):
    fix = {}
    for P in range(81):
        for R in range(P + 1, 81):
            if Qadj[P, R]:
                fix[(P, R)] = M[np.ix_(fib[P], fib[R])]
    m, X, E = cover_model(A, fib, Qadj, fix_edges=fix)
    s = cp_model.CpSolver(); s.parameters.num_workers = 1
    r = s.Solve(m); print(name, "fixed model:", s.StatusName(r), f"{time.time()-t:.1f}s")
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        G2 = graph_from_X(s, X, fib); print("  equals input:", (G2 == M).all(), "srg", is_srg(G2))
