"""Lab session, 2026-10-12. Local problem at P = 0, R0 = far[0] in a fixed type B state; type B allowed only at the blocks
of Omega = R0 + the blocks through at least one of the eight non-grid pairs of Oct(R0) separated by R0 (25 blocks with
the blocks meeting Oct(R0) in three points). Longer time limit; if SAT the solution is printed (block types, which blocks
are of type B).
python explore_typeB4.py <tmp dir> <seconds>"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
m = L.MASKS[sB]; Cr = L.C[R0]; side = {z: (m >> i) & 1 for i, z in enumerate(Cr)}
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
omega = {r for r in L.far if len(set(L.C[r]) & set(Cr)) >= 3}
for a, b in itertools.combinations(Cr, 2):
    if side[a] != side[b] and L.partner[R0][a] != b: omega |= {r for r in L.far if a in L.C[r] and b in L.C[r]}
extra = [[-x[r][s]] for r in L.far if r not in omega for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
path = os.path.join(tmp, "ex4_%d.cnf" % os.getpid())
with open(path, "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
    for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
t0 = time.time()
try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
except subprocess.TimeoutExpired: out = ""
res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
print("type B allowed at %d blocks (R0, its 3-point neighbours, the blocks through its separated non-grid pairs): %s (%.1f s)" % (len(omega), res, time.time() - t0))
if res == "SAT":
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    st = {r: [s for s in range(11) if x[r][s] in model][0] for r in L.far}
    types = {r: L.state_type(r, L.MASKS[st[r]]) for r in L.far}
    print("block types:", {t: sum(1 for r in L.far if types[r] == t) for t in ("flat", "A", "B")})
    print("type B blocks:", [L.V[r] for r in L.far if types[r] == "B"])
    print("states:", [st[r] for r in L.far])
