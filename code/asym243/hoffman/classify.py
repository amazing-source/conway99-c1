"""Rebuild the completions written by assemble.py, check srg(243,22,1,2) in integers, compare with the reference
graph (nauty canonical form) and compute |Aut|.
  python3 classify.py GRAPH COCLIQUE.npy BLOCKS COMPLETIONS"""
import sys, numpy as np, collections
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges, is_srg, canon_g6, aut
path, cpath, bpath, spath = sys.argv[1:5]
G = np.load(path) if path.endswith(".npy") else load_edges(path)
F = [int(x) for x in np.load(bpath + ".F.npy")]
ref = canon_g6(G)
classes = collections.Counter(); first = {}
for line in open(spath):
    if not line.strip(): continue
    H = G.copy()
    for a in F:
        for b in F: H[a, b] = 0
    for wi, row in enumerate(line.rstrip("\n").split(";")):
        for u in row.split():
            H[F[wi], F[int(u)]] = 1
    assert (H == H.T).all() and is_srg(H), "not an srg"
    c = canon_g6(H); classes[c] += 1
    if c not in first: first[c] = H
for c, k in classes.items():
    order = aut(first[c])[0]
    print(("REFERENCE" if c == ref else "NEW CLASS"), "copies:", k, "|Aut| =", order)
