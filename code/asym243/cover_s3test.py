"""General (non-affine) 3-covers of BH: is an S3-type non-adjacent fibre pair possible at all?"""
import sys, time, collections
from cover import *
A = load_edges("bvls243.edges")
fib = fibres_of(A, 0); ok, Qadj = is_cover(A, fib)
m, X, E = cover_model(A, fib, Qadj)
def odd(P, R):
    a, b = fib[P], fib[R]
    terms = []
    for j, k in ((0, 2), (1, 0), (2, 1)):
        y = m.NewBoolVar(""); m.AddImplication(y, X[(a[0], b[j])]); m.AddImplication(y, X[(a[1], b[k])])
        m.AddBoolOr([X[(a[0], b[j])].Not(), X[(a[1], b[k])].Not(), y]); terms.append(y)
    o = m.NewBoolVar(""); m.AddMaxEquality(o, terms); return o
mode = sys.argv[1]
P0 = 0
nonadj = [R for R in range(81) if R != 0 and not Qadj[0, R]]
R0 = nonadj[int(sys.argv[2]) if len(sys.argv) > 2 else 0]
if mode == "pair":
    CN = [Z for Z in range(81) if Qadj[P0, Z] and Qadj[Z, R0]]
    pp = []
    for Z in CN:
        o1, o2 = odd(P0, Z), odd(Z, R0)
        b = m.NewBoolVar(""); m.AddBoolXOr([o1, o2, b.Not()]); pp.append(b)
    m.Add(sum(pp) == 3)
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
t = time.time(); r = s.Solve(m)
print(mode, (P0, R0), s.StatusName(r), f"{time.time()-t:.0f}s", flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    G = graph_from_X(s, X, fib); np.save("cover_s3_found.npy", G)
    print("srg", is_srg(G), "aut", aut(G)[0], "parity coboundary", is_coboundary(parity_cocycle(G, fib, Qadj), 81))
