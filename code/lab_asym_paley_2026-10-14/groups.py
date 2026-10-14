"""Automorphism groups of every graph of a Spence list (exact, srglib). usage: python groups.py <spence file>"""
import sys
import time
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L

header, gs = L.read_spence(sys.argv[1])
print(header, "|", len(gs), "graphs")
for i, nb in enumerate(gs):
    t0 = time.time()
    p = L.srg_params(nb)
    order, chain, base = L.group_order(nb)
    orb = L.vertex_orbits(nb)
    print("#%2d params %s |Aut| = %d chain %s vertex orbits %s (%.1f s)"
          % (i + 1, p, order, chain, sorted(len(o) for o in orb), time.time() - t0), flush=True)
