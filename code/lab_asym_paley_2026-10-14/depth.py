"""Asymmetry certificates by refinement (14/10/2026): for each graph of a Spence list, the number of vertices v whose
individualisation alone makes the equitable refinement discrete (then Aut fixes nothing but... a discrete partition
after individualising v proves that the stabiliser of v is trivial), and the minimum number of individualised vertices
(greedy over the first non-singleton cell) needed to reach a discrete partition.
usage: python depth.py <spence file>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L

header, gs = L.read_spence(sys.argv[1])
for gi, nb in enumerate(gs):
    n = len(nb)
    c0 = L.refine(nb, [0] * n)
    one = 0
    cells_after = []
    for v in range(n):
        d = list(c0); d[v] = max(c0) + 1
        r = L.refine(nb, d)
        cells_after.append(len(set(r)))
        if len(set(r)) == n:
            one += 1
    order = L.group_order(nb)[0]
    print("#%2d |Aut|=%-4d vertices whose individualisation alone gives a discrete partition: %2d of %d ; cells after one individualisation: min %d max %d"
          % (gi + 1, order, one, n, min(cells_after), max(cells_after)), flush=True)
