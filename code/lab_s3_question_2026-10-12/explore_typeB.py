"""Lab session, 2026-10-12. Exploration: the local problem at P = 0 with the block R0 = far[0] in one fixed type B state.
For each of the 15 pairs inside Oct(R0), and each status (flat / split of type A / split of type B), one cadical call
with a short time limit: which statuses are refuted at once?
python explore_typeB.py <tmp dir> <seconds per call>"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
m = L.MASKS[sB]; Cr = L.C[R0]; side = {z: (m >> i) & 1 for i, z in enumerate(Cr)}
print("block R0 = %s, type B state: side 0 = %s, side 1 = %s" % (L.V[R0], [L.V[z] for z in Cr if side[z] == 0], [L.V[z] for z in Cr if side[z] == 1]))
print("grid pairs of R0: %s" % sorted({tuple(sorted((L.V[z], L.V[L.partner[R0][z]]))) for z in Cr}))
nv, base, x, y = L.build([])
base = base + [[x[R0][sB]]]
def run(extra):
    path = os.path.join(tmp, "expl_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: return "?"
    return "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "?"
for a, b in itertools.combinations(Cr, 2):
    p = (a, b) if (a, b) in y else (b, a); g, v, w, v2, w2 = y[p]
    kind = ("grid pair" if L.partner[R0][a] == b else "non-grid") + (", separated by R0" if side[a] != side[b] else ", same side")
    res = {}
    res["flat"] = run([[-t] for t in y[p]])
    res["A"] = run([[g], [v, w], [-v, -w], [v2, w2], [-v2, -w2]])
    res["B"] = run([list(y[p])] + [[-g, -u1, -u2] for u1 in (v, w) for u2 in (v2, w2)])
    print("pair %s %s (%s): flat %s, type A %s, type B %s" % (L.V[a], L.V[b], kind, res["flat"], res["A"], res["B"]), flush=True)
