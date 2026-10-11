"""Triangle far-graph switching (the original mechanism) applied to every triangle orbit of a graph.
Usage: python3 triswitch.py GRAPH(.npy|.edges) TAG [max_orbits]"""
import sys, time, collections, numpy as np
sys.path.insert(0, "../omega")
from switch243 import row_candidates, consistent_choices
from lib243 import *
path, tag = sys.argv[1], sys.argv[2]
maxo = int(sys.argv[3]) if len(sys.argv) > 3 else 99
G = np.load(path) if path.endswith(".npy") else load_edges(path)
o, orb, gens = aut(G)
tris = triangles(G); tidx = {t: i for i, t in enumerate(tris)}
# triangle orbits under the generators
parent = list(range(len(tris)))
def find(a):
    while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
    return a
for g in gens:
    for i, t in enumerate(tris):
        j = tidx[tuple(sorted(g[x] for x in t))]
        a, b = find(i), find(j)
        if a != b: parent[a] = b
orbs = collections.defaultdict(list)
for i in range(len(tris)): orbs[find(i)].append(i)
orbs = sorted(orbs.values(), key=len)
print(path, "|Aut| =", o, "triangle orbits:", [len(x) for x in orbs], flush=True)
known = {canon_g6(G): "self"}
for k, O in enumerate(orbs[:maxo]):
    T = tris[O[0]]; t0 = time.time()
    far, cands = row_candidates(G, T)
    dist = collections.Counter(len(c) for c in cands)
    sols = consistent_choices(far, cands, limit=64)
    out = []
    for sol in sols:
        B = G.copy()
        for i, wi in enumerate(far):
            S = cands[i][sol[i]]
            for j, wj in enumerate(far):
                B[wi, wj] = 1 if j in S else 0
        if is_srg(B):
            c = canon_g6(B)
            if c not in known:
                known[c] = f"{tag}_o{k}_{len(known)}"; np.save(known[c] + ".npy", B)
                ao = aut(B)[0]
                out.append((known[c], ao))
            else:
                out.append((known[c], None))
    print(f"orbit {k} (size {len(O)}) T={T}: cands/row {dict(dist)} consistent {len(sols)} srg-results {out} "
          f"[{time.time()-t0:.0f}s]", flush=True)
