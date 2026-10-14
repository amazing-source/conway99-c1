"""Where does the symmetry live in a srg(v,k,1,2)? (asymmetry campaign, 14/10/2026)
At a vertex x: FIRST-ORDER data F_x = x, its k/2 lines, the outer vertices with their two inner neighbours, and the
edges of the lines through the inner vertices (the matchings M_a). SECOND-ORDER data = the outer lines (lines with
no vertex in {x} u N(x)). The graph G1_x = G minus the edges of the outer lines encodes F_x.
Forced-symmetry principle: Aut(G)_x <= Aut(G1_x) (x is fixed: the only vertex of degree k whose k neighbours all have
degree k); if |Aut(G1_x)| > |Aut(G)_x| the outer lines are NOT determined by F_x (the extra elements send G to other
completions of F_x: at least |Aut(G1_x)| / |Aut(G)_x| of them).
usage: python firstorder.py file.edges [...]"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pairgroup243 as PG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T


def group_plain(Ms):
    n = len(Ms[0])
    init = sum((1 << (3 * i)) * M for i, M in enumerate(Ms)) + (1 << 20) * np.eye(n, dtype=np.int64)
    C = T.wl2([Ms[0]], [init])[0]
    base, order, gens = [], 1, []
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
        base.append(x)
    return order, gens


def first_order(A, x):
    n = len(A)
    adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    inner = adj[x] | {x}
    B = A.copy()
    for a in range(n):
        if a in inner:
            continue
        for b in adj[a]:
            if b > a and b not in inner:
                z = (adj[a] & adj[b]).pop()
                if z not in inner:          # edge of an outer line
                    B[a, b] = B[b, a] = 0
    return B


if __name__ == "__main__":
    for f in sys.argv[1:]:
        A = T.load(f)
        n = len(A)
        t = time.time()
        o, s, gens = PG.common_group([A])
        orbs = T.vertex_orbits(n, gens)
        out = []
        for O in orbs:
            x = O[0]
            stab = o // len(O)
            B = first_order(A, x)
            o1, _ = group_plain([B])
            out.append("orbit %d: |Aut_x| %d, |Aut(F_x)| %d%s" % (len(O), stab, o1, "" if o1 == stab else
                       "  (ratio %d: F_x has >= %d completions)" % (o1 // stab, o1 // stab)))
        print("%s: |Aut| %d; %s (%.0f s)" % (os.path.basename(f), o, "; ".join(out), time.time() - t), flush=True)
