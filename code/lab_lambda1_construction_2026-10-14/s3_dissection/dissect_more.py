"""Second look at the S3 graph: which lines carry the small orbits, the fixed triad and its perp, and the structure of
the 6x6 grids fixed by the involutions (which parallel class lies in the hemisystem).  usage: python dissect_more.py <dir> <report.json>"""
import itertools, json, os, sys
D = sys.argv[1]
gq = json.load(open(os.path.join(D, "ftwkb5_data", "gq.json"))); lines = [frozenset(l) for l in gq["lines"]]
H = json.load(open(os.path.join(D, "ftwkb5_data", "hemi_s1.hemi.json"))); Hs = set(H)
rep = json.load(open(sys.argv[2]))
P = rep["points_fixed_by_group"]
on = {p: [k for k, l in enumerate(lines) if p in l] for p in P}
def collinear(a, b): return any(a in l and b in l for l in lines)
print("fixed triad", P, "pairwise collinear:", [collinear(a, b) for a, b in itertools.combinations(P, 2)])
perp = [x for x in range(gq["npoints"]) if x not in P and all(collinear(x, p) for p in P)]
print("triad perp size:", len(perp), "| perp pairwise collinear:", sum(collinear(a, b) for a, b in itertools.combinations(perp, 2)))
pp = [x for x in range(gq["npoints"]) if x not in perp and all(collinear(x, q) for q in perp)]
print("perp of the perp (span of the triad):", len(pp), "contains the triad:", set(P) <= set(pp))
for p in P:
    print("point", p, ": of its 6 lines,", sum(1 for k in on[p] if k in Hs), "are in the hemisystem")
for o, hl in zip(rep["small_orbits"], rep["H_lines_of_small_orbits"]):
    pts = [sorted(set(lines[k]) & (set(P) | set(perp))) for k in hl]
    print("orbit of size", len(o), ": lines", hl, "| special points on them:", pts)
