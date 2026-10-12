"""Lab session, 2026-10-12. A structured family of signings of BH tested for parity skeletons.

A line-even signing is the same as a choice, on every line L, of a marked point or of no mark (the two edges at the
marked point are negative). FAMILY F1: for each of the ten isotropic directions omega, either no line of that direction
is marked, or all 27 lines of direction omega are marked at their point in one affine hyperplane H_omega not parallel
to omega (81 choices). 82^10 signings; the stabiliser of a generic member is trivial.
Complete skeleton problem (encoding of full_hybrid.py: edges + states of the pairs) restricted to this family, with
"some pair is split". SAT would give a non-trivial parity skeleton.
python family_hyperplanes.py <tmp dir> <seconds>"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
# no gauge fixing here: the family is not closed under switching, so build the plain constraints
nv, cl, ev, xs = full_hybrid.build([])
P = 0; farP = [r for r in range(n) if r != P and r not in nbs[P]]
gauge = {ev[key(P, z)] for z in nbs[P]} | {ev[key(r, CN[key(P, r)][0])] for r in farP}
cl = [c for c in cl if not (len(c) == 1 and -c[0] in gauge)]          # remove the 80 gauge unit clauses
nvv = [nv]
def new(): nvv[0] += 1; return nvv[0]
ups = []
for u in V:
    if any(u) and neg(u) not in ups: ups.append(u)
assert len(ups) == 40
for s in ISO:
    opts = [(u, c) for u in ups if Bf(s, u) != 0 for c in range(3)]; assert len(opts) == 81
    hv = [new() for _ in range(len(opts) + 1)]                        # last one = no mark
    cl.append(list(hv))
    for a, b in itertools.combinations(hv, 2): cl.append([-a, -b])
    for w in V:
        w2 = add(w, s); e = ev[key(I[w], I[w2])]
        if I[w] > I[w2] and False: pass
        # the edge {w, w + s} is negative iff the marked point of its line is w or w + s
        negopts = [hv[k] for k, (u, c) in enumerate(opts) if Bf(w, u) == c or Bf(w2, u) == c]
        cl.append([-e] + negopts)
        for h in negopts: cl.append([-h, e])
        # each edge is visited once: w ranges over V and the edge {w, w+s} is determined by w
cl.append([-vs[0] for vs in xs.values()])
path = os.path.join(tmp, "famh_%d.cnf" % os.getpid())
with open(path, "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (nvv[0], len(cl)))
    for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
t0 = time.time()
try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
except subprocess.TimeoutExpired: out = ""
res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
print("family F1 (one affine hyperplane or nothing per direction), some pair split: %s (%.1f s; %d variables, %d clauses)" % (res, time.time() - t0, nvv[0], len(cl)), flush=True)
if res == "SAT":
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    types = {}
    for k, vs in xs.items():
        st = [i for i in range(11) if vs[i] in model][0]; t = state_type(k[0], k[1], st); types[t] = types.get(t, 0) + 1
    print("  pair types: %s" % types)
    edges = sorted(ev); open(os.path.join(tmp, "skeleton_family_F1.txt"), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
try: os.remove(path)
except OSError: pass
