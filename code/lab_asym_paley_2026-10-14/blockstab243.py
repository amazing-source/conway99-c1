"""Stabiliser of a block in Aut(G) (= stabiliser of the completion G in the boundary group), 14/10/2026."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firstorder as FO
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12")
for name, f, b in (("fifth", "new243_tricayley_Z3x4_grids25.edges", 2), ("fifth", "new243_tricayley_Z3x4_grids25.edges", 0),
                   ("sixth", "new243_trade_aut108.edges", 0), ("sixth", "new243_trade_aut108.edges", 1)):
    A = T.load(os.path.join(D, f))
    M = np.zeros_like(A)
    blk = np.arange(81 * b, 81 * b + 81)
    M[np.ix_(blk, blk)] = 1
    np.fill_diagonal(M, 0)
    o, g = FO.group_plain([A, M])
    print("%s, block %d: |Stab_Aut(G)(block)| = %d" % (name, b, o), flush=True)
