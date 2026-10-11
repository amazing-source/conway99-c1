"""Affine line systems (fixed h_d spread) forced to be NON-abelian covers: at a chosen non-adjacent fibre pair (P0,R0)
of the quotient, exactly 3 of the 6 two-paths must carry odd (reflection) matchings.  This excludes every Z_3-cover
(BvLS, the twin, ...), so any solution is a new graph whose cover has monodromy S_3 (no deck transformation)."""
import sys, time, numpy as np
from ortools.sat.python import cp_model
from linesat import build
from lines_model import *
from lib243 import *
from cover import is_cover, parity_cocycle, is_coboundary
d = int(sys.argv[1]); seed = int(sys.argv[2]); limit = int(sys.argv[3]); tag = sys.argv[4]
pair_idx = int(sys.argv[5]) if len(sys.argv) > 5 else 0
hd = HS[d]
fixed = lines_of_direction(hd)
cands = []
for mm in range(11):
    if mm == d: continue
    for e in (0, 1, 2):
        cands += lines_of_direction(add(HS[mm], hd, e))
m, x, cands = build(fixed, cands)
fib = [list(f) for f in fixed]
where = {p: i for i, f in enumerate(fib) for p in f}
A0 = load_edges("bvls243.edges")
ok, Qadj = is_cover(A0, fib)
# fibre point ordering: p_i = base + i*h_d
def fib_order(F):
    base = PTS[F[0]]
    return [IDX[add(base, hd, i)] for i in range(3)]
def edge_odd(P, Z):
    """bool var: matching between fibres P and Z is a reflection."""
    pts = fib_order(fib[P])
    # find m and the lines from each p_i toward Z
    ys = []
    for pi in pts[:2]:
        row = []
        for mm in range(11):
            if mm == d: continue
            for e in (0, 1, 2):
                v = add(HS[mm], hd, e)
                L = line(PTS[pi], v)
                if any(where[q] == Z for q in L if q != pi):
                    row.append(x[L])
        assert len(row) == 3, len(row)
        ys.append(row)
    bs = []
    for e in range(3):
        b = m.NewBoolVar(""); m.AddBoolXOr([ys[0][e], ys[1][e], b.Not()]); bs.append(b)
    o = m.NewBoolVar("")
    m.AddMaxEquality(o, bs)
    return o
nonadj = [(0, R) for R in range(81) if R != 0 and not Qadj[0, R]]
P0, R0 = nonadj[pair_idx]
CN = [Z for Z in range(81) if Qadj[P0, Z] and Qadj[Z, R0]]
assert len(CN) == 6
pp = []
for Z in CN:
    o1, o2 = edge_odd(P0, Z), edge_odd(Z, R0)
    b = m.NewBoolVar(""); m.AddBoolXOr([o1, o2, b.Not()]); pp.append(b)
m.Add(sum(pp) == 3)
print("forced S3-type at fibre pair", (P0, R0), flush=True)
t0 = time.time(); n = 0; known = {}
while n < limit:
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 20000
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("status", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True); break
    sel = [c for c in cands if s.Value(x[c])]
    G = graph_from_lines(list(fixed) + sel); n += 1
    np.save(f"{tag}_{n}.npy", G)
    c = canon_g6(G); name = known.get(c)
    if name is None:
        name = f"S3new{len(known)}"; known[c] = name
    okc, Qa = is_cover(G, fib)
    cob = is_coboundary(parity_cocycle(G, fib, Qa), 81) if okc else None
    o, orb, gens = aut(G)
    gv, ng = grids_per_vertex(G)
    print(f"[{time.time()-t0:.0f}s] sol {n}: srg={is_srg(G)} class={name} |Aut|={o} #orbits={len(orb)} "
          f"cover={okc} parity_coboundary={cob} grids={ng}", flush=True)
    m.AddBoolOr([x[c_].Not() for c_ in sel])
