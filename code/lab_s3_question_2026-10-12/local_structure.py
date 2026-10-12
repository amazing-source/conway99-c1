"""Lab session, 2026-10-12. Structure of the non-trivial solutions of the local problem (local_vertex.py): for each solution found
by cadical (blocking clauses), the set of split far vertices is compared with the sets far(l) = vertices with no neighbour
on l, for the ten lines l through P = 0, and with unions of such sets.
python local_structure.py <tmp dir> <max solutions> <seconds per call>"""
import sys, os, subprocess, itertools, collections, importlib.util
tmp, maxsol, tl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("lv", os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_vertex.py"))
lv = importlib.util.module_from_spec(spec); keep = sys.argv; sys.argv = ["x"]; spec.loader.exec_module(lv); sys.argv = keep
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
cl = lv.build("nontrivial"); nlab = 300; P = 0
lines0 = sorted({tuple(sorted((P, z, next(iter(lv.nbs[P] & lv.nbs[z]))))) for z in lv.NP}); assert len(lines0) == 10
farline = [frozenset(r for r in lv.far if not any(r in lv.nbs[x] for x in l)) for l in lines0]; assert all(len(f) == 24 for f in farline)
path = os.path.join(tmp, "loc2.cnf"); found = []
for it in range(maxsol):
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (lv.nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: print("call %d: no answer in %d s" % (it + 1, tl)); break
    if "s UNSATISFIABLE" in out: print("call %d: UNSATISFIABLE: the %d solutions found are all the non-trivial ones" % (it + 1, len(found))); break
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    lab = {k: (v in model) for k, v in lv.var.items()}
    split = frozenset(r for r in lv.far if any(lab[(z, r)] for z in lv.C[r][1:]))
    which = [i for i, f in enumerate(farline) if f == split]
    found.append((split, lab))
    print("solution %d: %d split far vertices; equal to far(l) for the line number %s; lines l with far(l) inside the split set: %s"
          % (len(found), len(split), which, [i for i, f in enumerate(farline) if f <= split]), flush=True)
    cl.append([(-v if (v in model) else v) for v in range(1, nlab + 1)])
if found:
    by = collections.Counter(s for s, _ in found)
    print("distinct split sets: %d; multiplicities %s" % (len(by), sorted(by.values())))
