"""Lab session, 2026-10-12. Local problem at P = 0 (encoding of local_cnf2.py) with a prescribed pattern of odd squares
through P inside ONE grid through P.
Grid g = <z, z'> (two isotropic directions): its four squares through P are (P, s z, s z + s' z', s' z'), s, s' = +-1;
such a square is odd iff the block v = s z + s' z' separates its grid pair {s z, s' z'}.
A grid of BH has 16 possible curvatures: flat, 9 of "rectangle" type (four odd squares, those through one special point c)
and 6 of "six" type (six odd squares; a special transversal). Seen from one of its points P, the set of odd squares
through P is: empty (flat grid); all four (P = c); two with the same s or the same s' (P collinear with c); one (other
points of a rectangle grid); two "diagonal" ones, s s' constant (P on the special transversal of a six grid); three (the
six other points of a six grid).
python grid_patterns.py <tmp dir> <seconds per call> [index of z' among the neighbours, default 2]"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2]); k = int(sys.argv[3]) if len(sys.argv) > 3 else 2
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
neg = lambda a: tuple((-c) % 3 for c in a)
z = L.V[L.NP[0]]; zp = L.V[L.NP[k]]; assert zp not in (z, neg(z))
nv, base, x, y = L.build([])
corner = {}
for s in (1, 2):
    for sp in (1, 2):
        a = L.I[tuple((s * c) % 3 for c in z)]; b = L.I[tuple((sp * c) % 3 for c in zp)]
        p = (a, b) if (a, b) in y else (b, a)
        assert L.pblocks[p][0] == L.I[L.add(L.V[a], L.V[b])]
        corner[(s, sp)] = y[p][0]
def run(odd):
    extra = [[corner[c]] if c in odd else [-corner[c]] for c in corner]
    path = os.path.join(tmp, "gp_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: return "NO DECISION", time.time() - t0
    return ("UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"), time.time() - t0
print("grid <%s, %s> through P = 0" % (z, zp))
allc = sorted(corner)
for size in (4, 3, 2, 1):
    for odd in itertools.combinations(allc, size):
        if size == 2:
            kind = "two, same s" if odd[0][0] == odd[1][0] else "two, same s'" if odd[0][1] == odd[1][1] else "two, diagonal"
        else: kind = {4: "four (P = special point of a rectangle grid)", 3: "three (six grid, P off the special transversal)", 1: "one (rectangle grid, generic point)"}[size]
        res, t = run(set(odd))
        print("odd squares at the corners %s  [%s]: %s (%.1f s)" % (list(odd), kind, res, t), flush=True)
