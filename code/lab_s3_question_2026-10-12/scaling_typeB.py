"""Lab session, 2026-10-12. Scaling measurement: local problem at P = 0, R0 = far[0] in a fixed type B state, type B
allowed only on a set Omega of k blocks: Omega_25 (see explore_typeB4.py) plus the next blocks in a fixed order (blocks
sharing two points with Oct(R0) first). cadical time against k, to extrapolate to k = 60 (the real problem).
python scaling_typeB.py <tmp dir> <seconds per call> <k> [<k> ...]"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2]); ks = [int(a) for a in sys.argv[3:]]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
m = L.MASKS[sB]; Cr = L.C[R0]; side = {z: (m >> i) & 1 for i, z in enumerate(Cr)}
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
meet = {r: len(set(L.C[r]) & set(Cr)) for r in L.far}
omega = [R0] + sorted(r for r in L.far if meet[r] == 3)
for a, b in itertools.combinations(Cr, 2):
    if side[a] != side[b] and L.partner[R0][a] != b:
        for r in L.far:
            if a in L.C[r] and b in L.C[r] and r not in omega: omega.append(r)
assert len(omega) == 25
rest = sorted((r for r in L.far if r not in omega), key=lambda r: (-meet[r], r))
order = omega + rest
for k in ks:
    om = set(order[:k])
    extra = [[-x[r][s]] for r in L.far if r not in om for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
    path = os.path.join(tmp, "scal_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("type B allowed on %d blocks: %s (%.1f s)" % (k, res, time.time() - t0), flush=True)
