"""Lab session, 2026-10-12. Tests on glued local problems (local_lib.py).
python local_glue.py <tmp dir> <seconds> <test>
  selfcheck : the local problem at 0 with the states of the line solution at 0 imposed must be SAT (all ten directions)
  neighbour : the line solution at P = 0 (direction d) imposed, plus the local problem at a neighbour Z of P not on the line
  typeb     : a type B pair {P, R}: local problems at P only / at P and R / at P, R and their six common neighbours"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
tmp, tl, test = sys.argv[1], int(sys.argv[2]), sys.argv[3]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
def solve(pb, label):
    path = os.path.join(tmp, "glue_%d.cnf" % os.getpid()); pb.write(path); t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("%s: %d variables, %d clauses: %s (%.1f s)" % (label, pb.nv, len(pb.cl), res, time.time() - t0), flush=True)
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    try: os.remove(path)
    except OSError: pass
    return res, model
P = 0
if test == "selfcheck":
    for d in ISO:
        pb = Problem(); pb.add_local(P)
        for (a, b), s in line_solution(P, d).items(): pb.fix(a, b, s)
        solve(pb, "line solution at 0, direction %s, in the local problem at 0" % (d,))
elif test == "neighbour":
    d = ISO[0]
    for Z in sorted(nbs[P]):
        if Bf(V[Z], d) == 0: continue
        pb = Problem(); pb.add_local(P); pb.add_local(Z)
        for (a, b), s in line_solution(P, d).items(): pb.fix(a, b, s)
        solve(pb, "line solution at 0 (direction %s) + local problem at the neighbour %s" % (d, V[Z]))
elif test == "typeb":
    R = [r for r in range(n) if r != P and r not in nbs[P]][0]
    sB = [s for s in range(1, 11) if state_type(P, R, s) == "B"]
    for label, verts in (("P", [P]), ("P, R", [P, R]), ("P, R and C(P,R)", [P, R] + CN[key(P, R)])):
        pb = Problem()
        for X in verts: pb.add_local(X)
        pb.fix(P, R, sB[0])
        solve(pb, "pair {0, %s} of type B (state %d), local problems at %s" % (V[R], sB[0], label))
