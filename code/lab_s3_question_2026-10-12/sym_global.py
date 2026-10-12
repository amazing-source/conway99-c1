"""Lab session, 2026-10-12. Complete parity skeleton problem on BH (hybrid encoding of full_hybrid.py) with the extra
requirement that the skeleton CLASS is invariant under a given involution sigma of BH fixing P = 0: the states of the
pairs (which do not depend on the gauge) satisfy state(sigma x, sigma y) = sigma(state(x, y)); and "some pair is split".
SAT would give a non-trivial parity skeleton; UNSAT says that no non-trivial skeleton class is sigma-invariant.
The three involutions tried are representatives of the three conjugacy classes of involutions of the stabiliser of P
without fixed point on N(P) (the classes left undecided by sym_local.py): they fix 0, 2 or 8 far vertices.

python sym_global.py <tmp dir> <seconds> <0 | 2 | 8>      (number of far vertices fixed by the involution)
Memory: cadical on about 55 000 variables and 430 000 clauses, well under 1 GB."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid

tmp, tl, nfix = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")

def mat_apply(M, v): return tuple(sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4))
def mat_mul(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))
E4 = [tuple(int(i == j) for j in range(4)) for i in range(4)]
ident = tuple(E4)
gens = []
for w in V:
    if q(w) == 0: continue
    gens.append(tuple(tuple((E4[j][i] - Bf(E4[j], w) * q(w) * w[i]) % 3 for j in range(4)) for i in range(4)))
gens.append(((1, 1, 0, 0), (1, 2, 0, 0), (0, 0, 1, 0), (0, 0, 0, 2)))
group = {ident}; frontier = [ident]
while frontier:
    new = []
    for g in frontier:
        for h in gens:
            k = mat_mul(h, g)
            if k not in group: group.add(k); new.append(k)
    frontier = new
assert len(group) == 2880
P = 0; NP = sorted(nbs[P]); far = [r for r in range(n) if r != P and r not in nbs[P]]
sigma = None
for g in sorted(group):
    if g == ident or mat_mul(g, g) != ident: continue
    p = [I[mat_apply(g, V[i])] for i in range(n)]
    assert all((p[b] in nbs[p[a]]) == (b in nbs[a]) for a in range(0, n, 7) for b in range(n))
    if all(p[z] != z for z in NP) and sum(1 for r in far if p[r] == r) == nfix: sigma = p; break
assert sigma is not None
print("involution with %d fixed far vertices, %d fixed vertices in all" % (nfix, sum(1 for i in range(n) if sigma[i] == i)), flush=True)
nv, cl, ev, xs = full_hybrid.build([])
for (a, b), vs in xs.items():
    a2, b2 = sigma[a], sigma[b]; k2 = key(a2, b2); c, c2 = CN[(a, b)], CN[k2]
    for s in range(11):
        side = {sigma[z] for i, z in enumerate(c) if (MASKS[s] >> i) & 1}
        m = sum(1 << i for i, z in enumerate(c2) if z in side)
        if m & 1: m ^= 63
        cl.append([-vs[s], xs[k2][MASKS.index(m)]])
cl.append([-vs[0] for vs in xs.values()])                    # some pair is split
path = os.path.join(tmp, "symg_%d.cnf" % os.getpid())
with open(path, "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (nv, len(cl)))
    for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
t0 = time.time()
try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
except subprocess.TimeoutExpired: out = ""
res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
print("non-trivial skeleton invariant under this involution: %s (%.1f s; %d variables, %d clauses)" % (res, time.time() - t0, nv, len(cl)), flush=True)
if res == "SAT":
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    types = {}
    for k, vs in xs.items():
        s = [i for i in range(11) if vs[i] in model][0]; t = state_type(k[0], k[1], s); types[t] = types.get(t, 0) + 1
    print("  pair types: %s" % types)
    edges = sorted(ev); open(os.path.join(tmp, "skeleton_sym%d.txt" % nfix), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
try: os.remove(path)
except OSError: pass
