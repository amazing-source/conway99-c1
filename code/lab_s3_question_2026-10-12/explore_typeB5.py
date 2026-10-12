"""Lab session, 2026-10-12. Local problem at P = 0 with TWO blocks of type B prescribed: R0 = far[0] in a fixed type B
state, and a second block R' in a type B state; for each (R', state): one cadical call with a short limit.
Blocks R' are listed by the number of points they share with Oct(R0).
python explore_typeB5.py <tmp dir> <seconds per call> <first index> <last index>   (indices in the list of 59 x 6 cases)"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl, i0, i1 = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
meet = {r: len(set(L.C[r]) & set(L.C[R0])) for r in L.far}
cases = [(r, s) for r in sorted((r for r in L.far if r != R0), key=lambda r: (meet[r], r)) for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
res = {}
for idx in range(i0, min(i1 + 1, len(cases))):
    r, s = cases[idx]
    path = os.path.join(tmp, "ex5_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + 1))
        for c in base + [[x[r][s]]]: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    v = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "?"
    res.setdefault((meet[r], v), 0); res[(meet[r], v)] += 1
    if v == "SAT": print("SAT at case %d: block %s state %d" % (idx, L.V[r], s), flush=True)
print("cases %d..%d; counts by (points shared with Oct(R0), verdict): %s" % (i0, i1, sorted(res.items())), flush=True)
