"""Design skeleton of a grid-cover representation: for each pair of adjacent grids (G,H), how the 9 transversal lines
through G and H distribute over the third grids K (closure sizes).  Also the fixed-point counts of the triangle
holonomies sigma_GK^-1 sigma_HK sigma_GH."""
import sys, pickle, collections, os, numpy as np
from lib243 import *
from gridcover_anatomy import grid_partitions
for path in sys.argv[1:]:
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    parts = pickle.load(open(path + ".gridparts.pkl", "rb")) if os.path.exists(path + ".gridparts.pkl") else grid_partitions(G)
    tri = triangles(G); pat = collections.Counter(); per_part = []
    for part in parts:
        cell = {p: i for i, g in enumerate(part) for p in g}
        cnt = collections.Counter()
        for t in tri:
            cs = tuple(sorted(cell[p] for p in t))
            if len(set(cs)) == 3: cnt[cs] += 1
        pairs = collections.defaultdict(list)
        for (a, b, c), v in cnt.items():
            for (x, y) in ((a, b), (a, c), (b, c)): pairs[(x, y)].append(v)
        P = collections.Counter(tuple(sorted(v, reverse=True)) for v in pairs.values())
        per_part.append(dict(P)); pat.update(P)
    print(path, "pair patterns over all partitions:", dict(pat), flush=True)
