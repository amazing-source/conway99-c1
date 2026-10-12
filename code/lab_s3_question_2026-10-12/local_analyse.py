"""Lab session, 2026-10-12. Enumerate solutions of the local problem of local_vertex.py with cadical (blocking clauses on the
300 label variables) and describe them: number of split far vertices, types (number of odd grid squares 1 or 3).
python local_analyse.py <tmp dir> <max solutions>"""
import sys, os, subprocess, itertools, collections
sys.argv_keep = sys.argv; tmp, maxsol = sys.argv[1], int(sys.argv[2])
import importlib.util
spec = importlib.util.spec_from_file_location("lv", os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_vertex.py"))
lv = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(lv); sys.argv = sys.argv_keep
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
cl = lv.build("nontrivial"); nlab = 300
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
def grid_pairs(r):                                  # the three pairs {Z, Z'} of C(P,R) with Z + Z' = R (P = 0)
    out = []; cs = lv.C[r]
    for a, b in itertools.combinations(cs, 2):
        if lv.add(lv.V[a], lv.V[b]) == lv.V[r]: out.append((a, b))
    assert len(out) == 3; return out
hist = collections.Counter(); sols = 0; path = os.path.join(tmp, "loc.cnf")
while sols < maxsol:
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (lv.nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    out = subprocess.run([CAD, "-q", path], capture_output=True, text=True).stdout
    if "s SATISFIABLE" not in out: print("no further solution: %s" % out.split("\n")[0]); break
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    sols += 1; lab = {k: (v in model) for k, v in lv.var.items()}
    split = [r for r in lv.far if any(lab[(z, r)] for z in lv.C[r][1:])]
    types = collections.Counter()
    for r in split:
        l = {z: lab.get((z, r), False) for z in lv.C[r]}
        types[sum(1 for a, b in grid_pairs(r) if l[a] != l[b])] += 1
    key = (len(split), tuple(sorted(types.items()))); hist[key] += 1
    if sols <= 5: print("solution %d: split far vertices %d of 60; odd grid squares per split vertex %s" % (sols, len(split), dict(types)))
    cl.append([(-v if (v in model) else v) for v in range(1, nlab + 1)])
print("solutions enumerated: %d; by (number of split vertices, types): %s" % (sols, sorted(hist.items())))
