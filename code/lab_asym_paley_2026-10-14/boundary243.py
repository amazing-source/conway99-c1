"""Boundary groups of the block trades at 243 (asymmetry campaign, 14/10/2026).
H = G with the pairs inside one block (vertices 81 b .. 81 b + 80) erased and the block marked; Aut(H) acts on the
completions of the block (my exhaustive lists of 13/10: Gamma5, block 2 -> 6 completions; sixth graph, block 0 -> 6
completions). Orbit-stabiliser: every completion keeps a subgroup of Aut(H) of index <= number of completions.
Also: the group common to the fifth..eighth graphs (same labelling)."""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pairgroup243 as PG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12")
f5 = os.path.join(D, "new243_tricayley_Z3x4_grids25.edges")
f6 = os.path.join(D, "new243_trade_aut108.edges")
f7 = os.path.join(D, "new243_trade_aut162.edges")
f8 = os.path.join(D, "new243_trade_aut108_b.edges")
A5, A6, A7, A8 = (T.load(f) for f in (f5, f6, f7, f8))

t = time.time()
o, s, g = PG.common_group([A5, A6, A7, A8])
print("group common to the fifth, sixth, seventh, eighth graphs: order %d, vertex orbits %s (%.0f s)"
      % (o, sorted(len(x) for x in T.vertex_orbits(243, g)), time.time() - t), flush=True)


def boundary(A, b):
    H = A.copy()
    blk = np.arange(81 * b, 81 * b + 81)
    H[np.ix_(blk, blk)] = 0
    M = np.zeros_like(A)                      # mark the block: a second layer joining the block to itself
    M[np.ix_(blk, blk)] = 1
    np.fill_diagonal(M, 0)
    return H, M


def group_of_layers(Ms):
    # geometric initial colours assume lambda = 1, mu = 2; for a boundary use plain 2-WL from the layers
    n = len(Ms[0])
    init = sum((1 << (3 * i)) * M for i, M in enumerate(Ms)) + (1 << 20) * np.eye(n, dtype=np.int64)
    C = T.wl2([Ms[0]], [init])[0]
    base, order, sizes, gens = [], 1, [], []
    while True:
        col = np.diag(C).copy()
        for bb in base:
            col = PG.joint(col, C[bb], col, C[bb])[0]
        col = PG.refine_pair(Ms, col, col.copy())[0]
        cnt = np.bincount(col)
        if len(cnt) == n:
            break
        big = np.nonzero(cnt > 1)[0]
        c = big[np.argmax(cnt[big])]
        cell = [int(v) for v in np.nonzero(col == c)[0]]
        x = cell[0]
        level, orb = [], {x}
        for y in cell:
            if y in orb:
                continue
            f = PG.find_aut(Ms, C, [(bb, bb) for bb in base] + [(x, y)])
            if f is not None:
                level.append(f)
                gens.append(f)
                orb.add(y)
                changed = True
                while changed:
                    changed = False
                    for h in level:
                        for v in list(orb):
                            if h[v] not in orb:
                                orb.add(h[v])
                                changed = True
        order *= len(orb)
        sizes.append(len(orb))
        base.append(x)
    return order, sizes, gens


for name, A, b, ncomp in (("fifth (Gamma5)", A5, 2, 6), ("sixth", A6, 0, 6), ("sixth", A6, 1, 1), ("fifth (Gamma5)", A5, 0, 6)):
    t = time.time()
    H, M = boundary(A, b)
    o, s, g = group_of_layers([H, M])
    print("%s, block %d erased: |Aut(boundary)| = %d (basic orbits %s, %.0f s); completions listed on 13/10: %d; "
          "each completion keeps a subgroup of order >= %s" % (name, b, o, s, time.time() - t, ncomp,
                                                             o // ncomp if o % ncomp == 0 else "%d/%d" % (o, ncomp)),
          flush=True)
