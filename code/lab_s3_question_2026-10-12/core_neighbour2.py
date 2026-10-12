"""Lab session, 2026-10-12. The contradiction at a neighbour Z of a line-type vertex P: which inner pairs of Z carry it?
The eight split pairs {Z, Z'} (Z' in N(P)) of the line solution at P are prescribed (all of type B, with P on the
separated grid pair); the local problem at Z is restricted to a subset of its inner pairs.
python core_neighbour2.py <tmp dir> <seconds>"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
def solve(pb):
    path = os.path.join(tmp, "core2_%d.cnf" % os.getpid()); pb.write(path); t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    return ("UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"), time.time() - t0
P = 0; d = ISO[0]; Z = [z for z in sorted(nbs[P]) if Bf(V[z], d) != 0][0]
ls = line_solution(P, d)
splitZ = {k: s for k, s in ls.items() if Z in k and P not in k and s}
others = lambda k: k[0] if k[1] == Z else k[1]
pts = set()
for k in splitZ: pts |= set(CN[k])
print("Z = %s; the eight blocks at Z: %s; their points: %d of the 20 neighbours of Z" % (V[Z], [V[others(k)] for k in sorted(splitZ)], len(pts)))
tests = [("pairs through P only", lambda a, b: P in (a, b)),
         ("pairs inside the points of the eight blocks", lambda a, b: a in pts and b in pts),
         ("pairs not through P", lambda a, b: P not in (a, b)),
         ("pairs inside one of the eight blocks", lambda a, b: any(a in CN[k] and b in CN[k] for k in splitZ)),
         ("pairs through P or inside one of the eight blocks", lambda a, b: P in (a, b) or any(a in CN[k] and b in CN[k] for k in splitZ))]
for label, flt in tests:
    pb = Problem(); pb.add_local(Z, flt)
    for (a, b), s in splitZ.items(): pb.fix(a, b, s)
    res, t = solve(pb); print("%s: %s (%.1f s)" % (label, res, t), flush=True)
# deletion: a minimal subset of the eight blocks that is still refuted quickly (full local problem at Z)
keep = sorted(splitZ)
for k in sorted(splitZ):
    trial = [c for c in keep if c != k]
    pb = Problem(); pb.add_local(Z)
    for c in trial: pb.fix(c[0], c[1], splitZ[c])
    res, t = solve(pb)
    if res == "UNSAT": keep = trial
    print("  without the block %s: %s (%.1f s); kept %d" % (V[others(k)], res, t, len(keep)), flush=True)
print("a subset still refuted: %s" % [V[others(k)] for k in keep])
