"""Lab session, 2026-10-13. Types of the thirds of a graph: for each third F found (classes under Aut, thirds_bfs.thirds),
the number of lines through a vertex of F that lie inside F (a third is a SUBSPACE when every vertex has 5 such lines,
i.e. no line meets F in exactly two points), and the dimensions of the eigenvectors supported in F.
python third_types.py <max classes> <edge files ...>      (environment PYLIB)"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import aut_tools as T, thirds_bfs as TB, support_dims as SD
for path in sys.argv[2:]:
    A = T.load(path); n = 243; adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    o, gens, base, sizes = T.aut_group(A); reps, complete = TB.thirds(A, gens, maxn=int(sys.argv[1]))
    out = collections.Counter()
    for F, sz in reps:
        Fs = set(F); inside = collections.Counter()
        for x in F:
            inside[sum(1 for y in adj[x] & Fs if next(iter(adj[x] & adj[y])) in Fs) // 2] += 1
        w4, w5 = SD.dims(A.astype(float), F)
        out[(tuple(sorted(inside.items())), w4, w5)] += 1
    print("%s: %d classes of thirds listed%s" % (os.path.basename(path), len(reps), "" if complete else " (list not complete)"))
    for (ins, w4, w5), c in sorted(out.items(), key=lambda t: -t[1]):
        print("    %2d classes: lines inside the third per vertex (value: vertices) %s; supported eigenvectors (4, -5) = (%d, %d)%s" % (c, dict(ins), w4, w5, "   <- SUBSPACE" if dict(ins) == {5: 81} else ""))
