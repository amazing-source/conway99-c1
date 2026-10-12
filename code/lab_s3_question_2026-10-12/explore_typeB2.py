"""Lab session, 2026-10-12. Exploration: local problem at P = 0, the block R0 = far[0] in a fixed type B state, type B
allowed only for the blocks of a set Omega (the others are flat or of type A).
python explore_typeB2.py <tmp dir> <seconds per call> <mode>
  mode single : Omega = {R0}
  mode share  : Omega = blocks meeting Oct(R0) in at least k points, k = 3, 2, 1, 0 in turn
  mode count  : for information, the number of blocks meeting Oct(R0) in 0, 1, 2, 3 points"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl, mode = sys.argv[1], float(sys.argv[2]), sys.argv[3]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
meet = {r: len(set(L.C[r]) & set(L.C[R0])) for r in L.far}
def run(omega, label):
    extra = [[-x[r][s]] for r in L.far if r not in omega for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
    path = os.path.join(tmp, "ex2_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("%s (|Omega| = %d): %s (%.1f s)" % (label, len(omega), res, time.time() - t0), flush=True)
    return out
if mode == "count":
    import collections; print(sorted(collections.Counter(meet.values()).items()))
elif mode == "single": run({R0}, "type B allowed only at R0")
elif mode.startswith("k="):
    k = int(mode[2:]); run({r for r in L.far if meet[r] >= k}, "type B allowed at the blocks meeting Oct(R0) in >= %d points" % k)
else:
    for k in (4, 3, 2, 1, 0):
        run({r for r in L.far if meet[r] >= k}, "type B allowed at the blocks meeting Oct(R0) in >= %d points" % k)
