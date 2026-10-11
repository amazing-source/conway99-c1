"""Uniform Z_3-covers of BH steered by curvature: impose the number of flat BH-grids (an isomorphism invariant via
grids(Gamma) = 270 + 3*flat).  Usage: python3 ucover_flat.py MODE K SEED TAG   (MODE in eq, le, ge)"""
import sys, time, pickle, itertools, numpy as np
from ortools.sat.python import cp_model
import ucover as U
from lib243 import *
mode, K, seed, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
m, e = U.model()
# grids of BH: cosets of <w_i, w_j> for unordered pairs of directions
dirs = sorted({U.rep[s] for s in U.S})
flats = []
for wi, wj in itertools.combinations(dirs, 2):
    cosets = set()
    for P in U.V4:
        key = min(U.addv(U.addv(P, tuple((a * x) % 3 for x in wi)), tuple((b * x) % 3 for x in wj))
                  for a in range(3) for b in range(3))
        cosets.add(key)
    for P0 in cosets:
        # 4 elementary squares at P0 + a wi + b wj, a,b in {0,1}; curl = E(P,wi)+E(P+wi,wj)-E(P,wj)-E(P+wj,wi)
        f = m.NewBoolVar(""); curls = []
        for a in range(2):
            for b in range(2):
                P = U.addv(U.addv(P0, tuple((a * x) % 3 for x in wi)), tuple((b * x) % 3 for x in wj))
                terms = [(U.LI[U.qline(P, wi)], 1), (U.LI[U.qline(U.addv(P, wi), wj)], 1),
                         (U.LI[U.qline(P, wj)], -1), (U.LI[U.qline(U.addv(P, wj), wi)], -1)]
                # sign of E: wi, wj are representatives (sign +1)
                z = m.NewBoolVar("")
                expr = sum(sg * e[l] for l, sg in terms)
                qv = m.NewIntVar(-4, 4, "")
                m.Add(expr == 3 * qv).OnlyEnforceIf(z)
                r = m.NewIntVar(1, 2, ""); qv2 = m.NewIntVar(-4, 4, "")
                m.Add(expr == 3 * qv2 + r).OnlyEnforceIf(z.Not())
                curls.append(z)
        m.AddBoolAnd(curls).OnlyEnforceIf(f)
        m.AddBoolOr([c.Not() for c in curls]).OnlyEnforceIf(f.Not())
        flats.append(f)
print("grids:", len(flats), flush=True)
tot = sum(flats)
if mode == "eq": m.Add(tot == K)
elif mode == "le": m.Add(tot <= K)
else: m.Add(tot >= K)
s = cp_model.CpSolver(); s.parameters.num_workers = 3; s.parameters.random_seed = seed
s.parameters.max_time_in_seconds = 1500
t0 = time.time(); r = s.Solve(m)
print(mode, K, s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    ev = [s.Value(x) for x in e]; G = U.graph_of(ev)
    nflat = sum(s.Value(f) for f in flats)
    o, orb, gens = aut(G); _, ng = grids_per_vertex(G)
    np.save(f"{tag}_{mode}{K}.npy", G)
    print(f"srg={is_srg(G)} flat={nflat} grids={ng} (270+3*flat={270+3*nflat}) |Aut|={o} orbits={sorted(len(x) for x in orb)[:10]}", flush=True)
