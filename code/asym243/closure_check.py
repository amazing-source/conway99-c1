"""Closure sets of quotient triangles in grid-cover representations: for a quotient triangle (G,H,K), the points of G
lying on a transversal line through H and K.  Conjecture: empty, a line of the grid G, or all of G."""
import sys, pickle, itertools, collections, numpy as np
from lib243 import *
from gridcover_anatomy import grid_partitions
for path in sys.argv[1:]:
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    import os
    parts = pickle.load(open(path + ".gridparts.pkl", "rb")) if os.path.exists(path + ".gridparts.pkl") else grid_partitions(G)
    tri = triangles(G)
    stats = collections.Counter()
    for part in parts:
        cell = {p: i for i, g in enumerate(part) for p in g}
        inside = {i: [t for t in tri if all(cell[p] == i for p in t)] for i in range(len(part))}
        lines_in = {i: {frozenset(t) for t in inside[i]} for i in inside}
        over = collections.defaultdict(list)
        for t in tri:
            cs = frozenset(cell[p] for p in t)
            if len(cs) == 3: over[cs].append(t)
        for cs, ls in over.items():
            for Gi in cs:
                pts = frozenset(p for t in ls for p in t if cell[p] == Gi)
                if len(pts) == 9: stats["all 9"] += 1
                elif len(pts) == 3 and pts in lines_in[Gi]: stats["a grid line"] += 1
                elif len(pts) == 3 and not any(G[a, b] for a in pts for b in pts): stats["a diagonal (3 independent pts)"] += 1
                else: stats[f"other ({len(pts)} pts)"] += 1
    print(path, "partitions:", len(parts), dict(stats), flush=True)
