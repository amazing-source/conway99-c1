"""Lab session, 2026-10-13. SUBSPACE THIRDS: thirds F in which every vertex has its 5 "inside" lines entirely in F (no
line meets F in exactly two points). For each graph: the subspace thirds among the first classes listed (CryptoMiniSat
with the extra condition "subspace" imposed directly, so that the list concerns only them), whether the induced graph
on F is isomorphic to the folded Hamming graph (block 0..80 of the fifth graph), and the dimensions of the eigenvectors
supported in F (an invariant of the boundary = F with its attachments).
python subspace_thirds.py <reference: fifth graph> <max classes> <edge files ...>      (environment PYLIB)"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import pycryptosat
import aut_tools as T, support_dims as SD, row_census as RC
n = 243
ref = T.load(sys.argv[1])[:81, :81].copy()
for path in sys.argv[3:]:
    A = T.load(path); adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    o, gens, base, sizes = T.aut_group(A)
    nv = [n]; cls = []
    def new(): nv[0] += 1; return nv[0]
    for v in range(n):
        lits = [w + 1 for w in sorted(adj[v])]; prev = None
        for l in lits:
            cur = [None] + [new() for _ in range(11)]
            for j in range(1, 12):
                pj = prev[j] if prev else None
                if pj is not None: cls.append([-pj, cur[j]])
                if j == 1: cls.append([-l, cur[j]])
                elif prev: cls.append([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cls.append(c + [l])
                if j > 1: cls.append(c + ([prev[j - 1]] if prev else []))
            prev = cur
        x = v + 1; cls += [[-x, prev[10]], [-x, -prev[11]], [x, prev[6]], [x, -prev[7]]]
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y})
    for (a, b, c) in lines:                                              # subspace: two points of a line in F force the third
        cls += [[-(a + 1), -(b + 1), c + 1], [-(a + 1), -(c + 1), b + 1], [-(b + 1), -(c + 1), a + 1]]
    s = pycryptosat.Solver(time_limit=120); s.add_clauses(cls); reps = []; complete = False
    while len(reps) < int(sys.argv[2]):
        sat, sol = s.solve()
        if sat is None: break
        if not sat: complete = True; break
        F = frozenset(v for v in range(n) if sol[v + 1]); orb = {F}; frontier = [F]
        while frontier and len(orb) < 20000:
            nxt = []
            for S_ in frontier:
                for g in gens:
                    S2 = frozenset(g[v] for v in S_)
                    if S2 not in orb: orb.add(S2); nxt.append(S2)
            frontier = nxt
        for S_ in orb: s.add_clause([-(v + 1) for v in S_])
        reps.append((sorted(F), len(orb)))
    print("%s (|Aut| = %d): %d classes of subspace thirds%s" % (os.path.basename(path), o, len(reps), " (complete list)" if complete else " (list NOT complete)"), flush=True)
    for F, sz in reps:
        B = A[np.ix_(F, F)].copy(); Cs = T.wl2([B, ref]); iso = T.find_iso(B, ref, (), Cs) is not None
        w4, w5 = SD.dims(A.astype(float), F)
        print("    class of %d thirds: induced graph is the folded Hamming graph: %s; supported eigenvectors (4, -5) = (%d, %d)" % (sz, iso, w4, w5), flush=True)
