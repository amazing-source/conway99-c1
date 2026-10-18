"""Orbits of a complete Gram cover under the automorphisms of its root template (LAB, 18/10/2026).
An automorphism is a permutation p of the 7 root lines mapping the non-grid edges onto themselves and, for every root r,
the block partition at r onto the block partition at p(r).  It maps every realization of the template to a realization
(relabel the lines; letters follow), hence a Gram R to p(R): R and p(R) are excluded together, and one representative
per orbit suffices.  usage: python aut_orbits.py <catalogue> <index> <cover.json.gz> [out.json]"""
import gzip, json, sys
from itertools import permutations
cat, idx, cover = sys.argv[1], int(sys.argv[2]), sys.argv[3]
recs = json.loads(gzip.decompress(open(cat, "rb").read()))["open"]
t = recs[idx]["template"]
E = [tuple(e) for e in t["nongrid_edges"]]
Es = set(E)
parts = []
for r in range(7):
    ps = {frozenset(p) for p in t["nontrivial_component_groups"][r]}
    parts.append(ps)
aut = []
for p in permutations(range(7)):
    if {tuple(sorted((p[a], p[b]))) for a, b in E} != Es:
        continue
    if all({frozenset(p[j] for j in P) for P in parts[r]} == parts[p[r]] for r in range(7)):
        aut.append(p)
cv = json.load(gzip.open(cover, "rt"))
edges = [tuple(e) for e in cv["edges"]]
assert sorted(edges) == sorted(E)
pos = {e: i for i, e in enumerate(edges)}
perm_idx = [[pos[tuple(sorted((p[a], p[b])))] for (a, b) in edges] for p in aut]
seen = {}
reps = []
for gi, R in enumerate(cv["grams"]):
    key = min(tuple(R[q[i]][q[j]] for i in range(len(edges)) for j in range(len(edges))) for q in perm_idx)
    # R permuted: entry (i, j) of p(R) is R[q^-1 ...]; using all q in the group, the min over the orbit is canonical
    if key not in seen:
        seen[key] = gi
        reps.append(gi)
print(json.dumps({"index": idx, "aut_order": len(aut), "grams": len(cv["grams"]), "orbits": len(reps)}))
if len(sys.argv) > 4:
    json.dump({"index": idx, "aut": aut, "representatives": reps}, open(sys.argv[4], "w"))
