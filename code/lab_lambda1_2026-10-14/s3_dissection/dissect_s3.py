"""Dissect the automorphism group of the S3 hemisystem graph srg(378,52,1,8) (FTWKB(5), seed 1).
Steps: exact Aut of the graph (pipeline of srg_group3.py), lift each automorphism to the GQ (points = triangles of the
graph, since every GQ point lies on exactly 3 hemisystem lines that pairwise meet there), check that the lift maps
every GQ line (hemisystem or not) onto a GQ line, then list what each group element fixes.
usage: python dissect_s3.py <lambda1_construction dir> <out.json>"""
import itertools
import json
import os
import sys
import time

import numpy as np

D = sys.argv[1]
sys.path.insert(0, D)
sys.path.insert(0, os.path.join(D, "..", "spreadfree_243_2026-10-12"))
import pq_invariants as PQ  # noqa: E402
import srg_group2 as S  # noqa: E402
import aut_tools as T  # noqa: E402

gq = json.load(open(os.path.join(D, "ftwkb5_data", "gq.json")))
lines = [frozenset(l) for l in gq["lines"]]
npts = gq["npoints"]
H = json.load(open(os.path.join(D, "ftwkb5_data", "hemi_s1.hemi.json")))
Hset = set(H)
A = PQ.load(os.path.join(D, "ftwkb5_data", "hemi_s1.edges"))
n = len(A)
assert n == 378 and len(H) == 378

# vertex i <-> line H[i] ? check against concurrency
conc = np.zeros((n, n), dtype=np.int64)
for i, j in itertools.combinations(range(n), 2):
    if lines[H[i]] & lines[H[j]]:
        conc[i, j] = conc[j, i] = 1
print("vertex i = line H[i]:", bool(np.array_equal(conc, A)), flush=True)

t = time.time()
C, _, _, _, _ = PQ.pair_colours(A)
order, sizes, gens = S.aut_group(A, C)
print("|Aut| =", order, "basic orbits", sizes, "gens", len(gens), "(%.0f s)" % (time.time() - t), flush=True)

# close the group (small) by BFS over generators
def compose(f, g):  # f after g
    return tuple(f[g[i]] for i in range(n))
ident = tuple(range(n))
G = {ident}
frontier = [ident]
while frontier:
    new = []
    for x in frontier:
        for g in gens:
            y = compose(tuple(g), x)
            if y not in G:
                G.add(y)
                new.append(y)
    frontier = new
G = sorted(G)
print("group elements:", len(G), flush=True)
for g in G:
    assert all(A[g[i], g[j]] == A[i, j] for i in range(n) for j in range(i + 1, n) if A[i, j]), "not an automorphism"

# points of the GQ as triangles of the graph: point p <-> the 3 hemisystem lines through it
pt_tri = {}
for p in range(npts):
    tri = tuple(sorted(i for i in range(n) if p in lines[H[i]]))
    assert len(tri) == 3, (p, tri)
    pt_tri[p] = tri
tri_pt = {v: k for k, v in pt_tri.items()}
assert len(tri_pt) == npts

def lift_points(g):
    return [tri_pt[tuple(sorted(g[i] for i in pt_tri[p]))] for p in range(npts)]

line_index = {l: k for k, l in enumerate(lines)}
def elem_order(g):
    k, x = 1, g
    while x != ident:
        x = compose(g, x)
        k += 1
    return k

report = []
for g in G:
    pm = lift_points(g)
    lm = []
    for l in lines:
        img = frozenset(pm[p] for p in l)
        assert img in line_index, "lift does not map a GQ line to a GQ line"
        lm.append(line_index[img])
    fixed_pts = [p for p in range(npts) if pm[p] == p]
    fixed_lines = [k for k in range(len(lines)) if lm[k] == k]
    fixed_H = [k for k in fixed_lines if k in Hset]
    # incidence structure of the fixed set: points on fixed lines, lines through fixed points
    fl_pts = {k: sum(1 for p in lines[k] if pm[p] == p) for k in fixed_lines}
    report.append({"order": elem_order(g), "fixed_vertices": sum(1 for i in range(n) if g[i] == i),
                   "fixed_points": len(fixed_pts), "fixed_lines": len(fixed_lines), "fixed_H_lines": len(fixed_H),
                   "fixed_nonH_lines": len(fixed_lines) - len(fixed_H),
                   "fixed_points_per_fixed_line": sorted(fl_pts.values()),
                   "fixed_lines_per_fixed_point": sorted(sum(1 for k in fixed_lines if p in lines[k]) for p in fixed_pts)})
for r in report:
    print(r, flush=True)

# vertex orbits and what the small orbits are
orbs = T.vertex_orbits(n, [list(g) for g in G])
small = [sorted(o) for o in orbs if len(o) < 6]
print("vertex orbit sizes:", sorted(len(o) for o in orbs))
# common fixed point / line of the whole group
allfix_pts = [p for p in range(npts) if all(lift_points(g)[p] == p for g in G)]
print("points fixed by the whole group:", len(allfix_pts))
json.dump({"order": order, "report": report, "small_orbits": small, "H_lines_of_small_orbits": [[H[i] for i in o] for o in small],
           "points_fixed_by_group": allfix_pts}, open(sys.argv[2], "w"), indent=1)
