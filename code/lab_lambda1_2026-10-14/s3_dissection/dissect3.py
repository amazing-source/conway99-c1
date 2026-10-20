"""Fixed structures of each element of the S3 (lifted to FTWKB(5)), relative to the pair a=849, c=3275 and its perp.
Recomputes the group from the graph (as dissect_s3.py). usage: python dissect3.py <dir>"""
import itertools, json, os, sys
import numpy as np
D = sys.argv[1]
sys.path.insert(0, D); sys.path.insert(0, os.path.join(D, "..", "spreadfree_243_2026-10-12"))
import pq_invariants as PQ, srg_group2 as S
gq = json.load(open(os.path.join(D, "ftwkb5_data", "gq.json"))); lines = [frozenset(l) for l in gq["lines"]]; npts = gq["npoints"]
H = json.load(open(os.path.join(D, "ftwkb5_data", "hemi_s1.hemi.json"))); Hs = set(H)
A = PQ.load(os.path.join(D, "ftwkb5_data", "hemi_s1.edges")); n = len(A)
C, *_ = PQ.pair_colours(A); order, sizes, gens = S.aut_group(A, C)
comp = lambda f, g: tuple(f[g[i]] for i in range(n)); I = tuple(range(n)); G = {I}; fr = [I]
while fr:
    new = []
    for x in fr:
        for g in gens:
            y = comp(tuple(g), x)
            if y not in G: G.add(y); new.append(y)
    fr = new
on_pt = [[] for _ in range(npts)]
for k, l in enumerate(lines):
    for p in l: on_pt[p].append(k)
tri = {p: tuple(sorted(H.index(k) for k in on_pt[p] if k in Hs)) for p in range(npts)}
inv_tri = {v: k for k, v in tri.items()}
def lift(g): return [inv_tri[tuple(sorted(g[i] for i in tri[p]))] for p in range(npts)]
def coll(a, b): return bool(set(on_pt[a]) & set(on_pt[b]))
a, b, c = 849, 3170, 3275
perp_ac = [x for x in range(npts) if x not in (a, c) and coll(x, a) and coll(x, c)]
print("perp{a,c}:", perp_ac, "(b in it:", b in perp_ac, ")")
lk = {l: k for k, l in enumerate(lines)}
for g in sorted(G):
    if g == I: continue
    pm = lift(g); o = 1; x = g
    while x != I: x = comp(g, x); o += 1
    fp = [p for p in range(npts) if pm[p] == p]
    fl = [k for k, l in enumerate(lines) if lk[frozenset(pm[p] for p in l)] == k]
    inperp = [p for p in fp if p in perp_ac]
    print("order %d: %d fixed points; a,b,c fixed: %s; fixed points in perp{a,c}: %d/6; fixed lines in H: %d/%d"
          % (o, len(fp), [p in fp for p in (a, b, c)], len(inperp), sum(k in Hs for k in fl), len(fl)))
    if o == 3:
        rest = [p for p in fp if p not in (a, c) and p not in perp_ac]
        print("   other fixed points:", rest, "| collinear with a:", [coll(p, a) for p in rest], "with c:", [coll(p, c) for p in rest])
        six = [p for p in fp if sum(1 for k in fl if p in lines[k]) == 6]
        print("   fixed points with all 6 lines fixed:", six)
    if o == 2:
        rows = [k for k in fl]
        print("   grid lines in H:", sorted(k for k in fl if k in Hs), " not in H:", sorted(k for k in fl if k not in Hs))
        # parallel classes of the 6x6 grid: two grid lines are in the same class iff disjoint
        cls = []
        for k in fl:
            for cl in cls:
                if not (lines[k] & lines[cl[0]]): cl.append(k); break
            else: cls.append([k])
        print("   parallel classes:", [[(k, k in Hs) for k in cl] for cl in cls])
