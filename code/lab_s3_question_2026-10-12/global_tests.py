"""Lab session, 2026-10-12. Complete parity skeleton problem on BH (hybrid encoding of full_hybrid.py) under global
assumptions.
python global_tests.py <tmp dir> <seconds> <test>
  allsplit   : every non-adjacent pair is split (a signing of BH with A^2 = A + 20 I, eigenvalues 5 and -4)
  trivialP   : the vertex P = 0 is trivial (its 60 pairs are flat) and some pair is split
  trivialline: the three vertices of a line through P are trivial and some pair is split
  nosplitnear: P is trivial, all pairs through the neighbours of P are flat too, and some pair is split
  noflatP    : the 60 pairs through P are all split
  flatpair   : the pair {P, far[0]} is flat and some pair is split
  lineF3     : the three pairs of the non-isotropic line T = {P, P + v, P - v} (v = far[0]) are flat, some pair is split
  lineF1     : the pair {P, P + v} is flat, the two other pairs of T are split"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid
tmp, tl, test = sys.argv[1], float(sys.argv[2]), sys.argv[3]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv, cl, ev, xs = full_hybrid.build([])
P = 0; some_split = [-vs[0] for vs in xs.values()]
through = lambda X: [k for k in xs if X in k]
if test == "allsplit":
    for vs in xs.values(): cl.append([-vs[0]])
elif test == "trivialP":
    for k in through(P): cl.append([xs[k][0]])
    cl.append(some_split)
elif test == "trivialline":
    z = sorted(nbs[P])[0]; w = next(iter(nbs[P] & nbs[z]))
    for X in (P, z, w):
        for k in through(X): cl.append([xs[k][0]])
    cl.append(some_split)
elif test == "nosplitnear":
    for X in [P] + sorted(nbs[P]):
        for k in through(X): cl.append([xs[k][0]])
    cl.append(some_split)
elif test == "noflatP":
    for k in through(P): cl.append([-xs[k][0]])
elif test in ("flatpair", "lineF3", "lineF1"):
    R = [r for r in range(n) if r != P and r not in nbs[P]][0]; R2 = I[tuple((-c) % 3 for c in V[R])]
    assert R2 not in nbs[P] and R2 not in nbs[R]
    cl.append([xs[key(P, R)][0]])
    if test == "flatpair": cl.append(some_split)
    elif test == "lineF3": cl += [[xs[key(P, R2)][0]], [xs[key(R, R2)][0]], some_split]
    else: cl += [[-xs[key(P, R2)][0]], [-xs[key(R, R2)][0]]]
path = os.path.join(tmp, "gt2_%d.cnf" % os.getpid())
with open(path, "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (nv, len(cl)))
    for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
t0 = time.time()
try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
except subprocess.TimeoutExpired: out = ""
res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
print("%s: %s (%.1f s)" % (test, res, time.time() - t0), flush=True)
if res == "SAT":
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    types = {}
    for k, vs in xs.items():
        s = [i for i in range(11) if vs[i] in model][0]; t = state_type(k[0], k[1], s); types[t] = types.get(t, 0) + 1
    print("  pair types: %s" % types)
    edges = sorted(ev); open(os.path.join(tmp, "skeleton_%s.txt" % test), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
try: os.remove(path)
except OSError: pass
