"""Lab session, 2026-10-12. Can a grid of BH be curved in a parity skeleton?

A grid g = x + <a, a'> (a, a' isotropic, independent) is a 3x3 rook graph; with its six lines even, the parities of its
nine squares form one of 16 curvatures: flat; "rectangle" (the four squares through one special point are odd; 9 cases);
"six" (six odd squares: all the squares except three, 6 cases). A square of g is odd iff the state of either of its
diagonals separates the two other corners.
Test: the curvature of g is prescribed, and the local problems at the nine points of g are imposed together (pair states
shared, local_lib.py). UNSAT means: no parity skeleton has this curvature on g (necessary conditions only are used).

python grid_types.py <tmp dir> <seconds per call> <rect | six | both> [vertices: all | k]   (k = only the first k points)"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
tmp, tl, what = sys.argv[1], float(sys.argv[2]), sys.argv[3]
kpts = sys.argv[4] if len(sys.argv) > 4 else "all"
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
a, ap = ISO[0], ISO[1]; assert Bf(a, ap) != 0
pt = lambda i, j: I[tuple((i * a[k] + j * ap[k]) % 3 for k in range(4))]
grid = [pt(i, j) for i in range(3) for j in range(3)]
def odd_rect(i1, i2, j1, j2): return 0 in (i1, i2) and 0 in (j1, j2)                 # special point (0, 0)
def odd_six(i1, i2, j1, j2): return (3 - i1 - i2) != (3 - j1 - j2)                    # unused row index != unused column index
def run(label, oddfun, verts):
    pb = Problem()
    for X in verts: pb.add_local(X)
    nodd = 0
    for i1, i2 in itertools.combinations(range(3), 2):
        for j1, j2 in itertools.combinations(range(3), 2):
            odd = oddfun(i1, i2, j1, j2); nodd += odd
            for (x, y, z, w) in ((pt(i1, j1), pt(i2, j2), pt(i2, j1), pt(i1, j2)), (pt(i2, j1), pt(i1, j2), pt(i1, j1), pt(i2, j2))):
                xs = pb.pair(x, y); sep = pb.sepstates(x, y, z, w)
                if odd: pb.cl.append([xs[s] for s in sep])
                else:
                    for s in sep: pb.cl.append([-xs[s]])
    path = os.path.join(tmp, "gt_%d.cnf" % os.getpid()); pb.write(path); t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("%s (%d odd squares), local problems at %d points of the grid: %d variables, %d clauses: %s (%.1f s)" % (label, nodd, len(verts), pb.nv, len(pb.cl), res, time.time() - t0), flush=True)
verts = grid if kpts == "all" else grid[:int(kpts)]
if what in ("rect", "both"): run("rectangle type, special point P", odd_rect, verts)
if what in ("six", "both"): run("six type", odd_six, verts)
