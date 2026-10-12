"""Lab session, 2026-10-12. Which part of the line solution at P is contradictory at a neighbour Z?
Local problem at Z only (local_lib.py), with a chosen part of the states prescribed by the line solution at P = 0 in the
direction d: (a) the pairs {Z, Z'}, Z' in N(P) (blocks at Z); (b) only those of them that are split (they are of type B);
(c) the pairs {P, R}, R in N(Z) (inner pairs at Z); (d) everything (control: UNSAT as in local_glue.py neighbour).
python core_neighbour.py <tmp dir> <seconds>"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
def solve(pb, label):
    path = os.path.join(tmp, "core_%d.cnf" % os.getpid()); pb.write(path); t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("%s: %s (%.1f s)" % (label, res, time.time() - t0), flush=True)
    return res
P = 0; d = ISO[0]; Z = [z for z in sorted(nbs[P]) if Bf(V[z], d) != 0][0]
ls = line_solution(P, d)
blocksZ = {k: s for k, s in ls.items() if Z in k and P not in k}                 # pairs {Z, Z'} inside N(P)
innerZ = {k: s for k, s in ls.items() if P in k and (k[0] if k[1] == P else k[1]) in nbs[Z]}   # pairs {P, R}, R ~ Z
print("P = 0, direction %s, Z = %s; pairs {Z,Z'}: %d (split: %d, types %s); pairs {P,R} with R ~ Z: %d (split: %d)" % (
    d, V[Z], len(blocksZ), sum(1 for s in blocksZ.values() if s), sorted({state_type(k[0], k[1], s) for k, s in blocksZ.items() if s}),
    len(innerZ), sum(1 for s in innerZ.values() if s)))
for label, data in (("(a) all the pairs {Z,Z'}", blocksZ), ("(b) only the split pairs {Z,Z'}", {k: s for k, s in blocksZ.items() if s}),
                    ("(c) the pairs {P,R}, R ~ Z", innerZ), ("(c') only the split pairs {P,R}", {k: s for k, s in innerZ.items() if s}),
                    ("(d) (a) and (c)", {**blocksZ, **innerZ})):
    pb = Problem(); pb.add_local(Z)
    for (a, b), s in data.items(): pb.fix(a, b, s)
    solve(pb, label)
# smaller cores: subsets of the split pairs {Z, Z'}
import itertools
splitZ = sorted(k for k, s in blocksZ.items() if s)
for size in (1, 2, 3):
    res = {}
    for sub in itertools.combinations(splitZ, size):
        pb = Problem(); pb.add_local(Z)
        for k in sub: pb.fix(k[0], k[1], blocksZ[k])
        path = os.path.join(tmp, "core_%d.cnf" % os.getpid()); pb.write(path)
        try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=3).stdout
        except subprocess.TimeoutExpired: out = ""
        r = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "?"
        res[r] = res.get(r, 0) + 1
    print("subsets of %d split pairs {Z,Z'} prescribed (3 s each): %s" % (size, res), flush=True)
