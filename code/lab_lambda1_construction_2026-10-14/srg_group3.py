"""Exact |Aut| of a lambda = 1 strongly regular graph with the prism invariants of pq_invariants.py as initial pair
colours (isomorphism invariants), then 2-dim WL + individualisation-refinement + orbit-stabiliser chain
(srg_group2.aut_group); every automorphism is checked edge by edge. (14/10/2026)
usage: python srg_group3.py file.edges [...]"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pq_invariants as PQ
import srg_group2 as S
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T

for p in sys.argv[1:]:
    A = PQ.load(p)
    t = time.time()
    C, lines, p3, p2, vstat = PQ.pair_colours(A)
    o, sizes, gens = S.aut_group(A, C)
    orbs = T.vertex_orbits(len(A), gens)
    print("%s: |Aut| = %d (basic orbits %s); vertex orbits %s (%.0f s)"
          % (os.path.basename(p), o, sizes, sorted(len(x) for x in orbs), time.time() - t), flush=True)
