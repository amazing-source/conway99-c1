"""Lab session, 2026-10-12. Exploration: local problem at P = 0, R0 = far[0] in a fixed type B state {a, b, b'} | {a', c, c'};
type B allowed only at R0, at the blocks meeting Oct(R0) in three points, and at the blocks through a chosen set of pairs
of Oct(R0). Which pairs are needed for the solver to stop refuting at once?
python explore_typeB3.py <tmp dir> <seconds per call>"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
m = L.MASKS[sB]; Cr = L.C[R0]; side = {z: (m >> i) & 1 for i, z in enumerate(Cr)}
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
meet = {r: len(set(L.C[r]) & set(L.C[R0])) for r in L.far}
core = {r for r in L.far if meet[r] >= 3}
def run(omega):
    extra = [[-x[r][s]] for r in L.far if r not in omega for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
    path = os.path.join(tmp, "ex3_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    return ("UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"), time.time() - t0
def kind(a, b):
    return ("grid pair" if L.partner[R0][a] == b else "non-grid") + (", separated" if side[a] != side[b] else ", same side")
groups = {}
for a, b in itertools.combinations(Cr, 2):
    blocks = {r for r in L.far if a in L.C[r] and b in L.C[r]}
    groups.setdefault(kind(a, b), set()).update(blocks)
    res, t = run(core | blocks)
    print("pair %s %s (%s): type B also allowed at its blocks: %s (%.1f s)" % (L.V[a], L.V[b], kind(a, b), res, t), flush=True)
for k, blocks in groups.items():
    res, t = run(core | blocks)
    print("ALL pairs of kind [%s] (%d blocks): %s (%.1f s)" % (k, len(core | blocks), res, t), flush=True)
