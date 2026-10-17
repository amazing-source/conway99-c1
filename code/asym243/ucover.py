"""Uniform (affine) Z_3-covers of BH: one value e(l) in Z_3 per line l of BH (270 lines); the matching along
P -> P+s (s = eps*w_m) is t -> t + a(s) + eps*e(l).  srg <=> for every non-adjacent pair the 6 path values are
equidistributed.  Small table model; sampling with random seeds / random hints.
Usage: python3 ucover.py SEED0 SEED1 TAG"""
import sys, time, pickle, itertools, collections, numpy as np
from ortools.sat.python import cp_model
from heis import Sbar, aval, addv
from lines_model import PTS, IDX, HS, add, line
from lib243 import *
V4 = list(itertools.product(range(3), repeat=4)); I4 = {v: i for i, v in enumerate(V4)}
S = Sbar; Sset = set(S)
neg = lambda s: tuple((-x) % 3 for x in s)
rep = {s: (s if s == min(s, neg(s)) else neg(s)) for s in S}
sign = {s: (1 if s == rep[s] else -1) for s in S}
# Q-lines: coset of <w> ; key (w_rep, coset representative)
def qline(P, s):
    w = rep[s]
    return (w, min(I4[addv(P, tuple((t * x) % 3 for x in w))] for t in range(3)))
lines = sorted({qline(P, s) for P in V4 for s in S}); LI = {l: i for i, l in enumerate(lines)}
assert len(lines) == 270
pairs = []
for P in V4:
    for d in V4:
        if d == (0,) * 4 or d in Sset: continue
        R = addv(P, d)
        if I4[P] < I4[R]:
            paths = []
            for s1 in S:
                s2 = tuple((a - b) % 3 for a, b in zip(d, s1))
                if s2 in Sset:
                    Z = addv(P, s1)
                    paths.append(((aval[s1] + aval[s2]) % 3, (LI[qline(P, s1)], sign[s1]), (LI[qline(Z, s2)], sign[s2])))
            assert len(paths) == 6
            pairs.append(paths)
eq90 = [list(t) for t in itertools.product(range(3), repeat=6) if sorted(t) == [0, 0, 1, 1, 2, 2]]
def model():
    m = cp_model.CpModel(); e = [m.NewIntVar(0, 2, "") for _ in lines]
    for paths in pairs:
        vals = []
        for base, (l1, s1), (l2, s2) in paths:
            v = m.NewIntVar(0, 2, "")
            m.AddAllowedAssignments([e[l1], e[l2], v], [[a, b, (base + s1 * a + s2 * b) % 3] for a in range(3) for b in range(3)])
            vals.append(v)
        m.AddAllowedAssignments(vals, eq90)
    return m, e
# lift: vertex (P, t) <-> point of F_3^5 via basis (w1..w4 lifted, h0)
from heis import Bm
def graph_of(ev):
    def vid(P, t):
        c = np.array(list(P) + [t]); return IDX[tuple((Bm @ c) % 3)]
    G = np.zeros((243, 243), dtype=np.int64)
    for P in V4:
        for t in range(3):
            x = vid(P, t)
            for u in (1, 2):
                G[x, vid(P, (t + u) % 3)] = 1
            for s in S:
                c = (aval[s] + sign[s] * ev[LI[qline(P, s)]]) % 3
                G[x, vid(addv(P, s), (t + c) % 3)] = 1
    return G
if __name__ == "__main__":
    s0, s1, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    try: known = pickle.load(open("uclasses.pkl", "rb"))
    except Exception: known = {}
    # sanity: e = 0 gives BvLS
    G0 = graph_of([0] * 270); print("e=0 srg:", is_srg(G0), flush=True)
    for seed in range(s0, s1):
        rng = np.random.default_rng(seed)
        m2, e2 = model()
        for i in range(270):
            m2.AddHint(e2[i], int(rng.integers(0, 3)))
        sv = cp_model.CpSolver(); sv.parameters.num_workers = 2; sv.parameters.random_seed = seed
        sv.parameters.max_time_in_seconds = 600
        t0 = time.time(); r = sv.Solve(m2)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"seed {seed}: {sv.StatusName(r)}", flush=True); continue
        ev = [sv.Value(e2[i]) for i in range(270)]
        G = graph_of(ev); c = canon_g6(G)
        if c not in known:
            o = aut(G)[0]; name = f"U{len(known)}"; known[c] = (name, o, ev)
            np.save(f"{tag}_{name}.npy", G); pickle.dump(known, open("uclasses.pkl", "wb")); new = " NEW"
        else: new = ""
        name, o, _ = known[c]
        print(f"seed {seed}: srg={is_srg(G)} class={name}{new} |Aut|={o} nonzero e={sum(1 for x in ev if x)} [{time.time()-t0:.1f}s]", flush=True)
