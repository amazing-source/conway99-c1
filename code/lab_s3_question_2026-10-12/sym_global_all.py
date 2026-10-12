"""Lab session, 2026-10-12. Is a non-trivial parity skeleton class on BH invariant under some non-identity automorphism?

Aut(BH) = {x -> g x + v : g in G0, v in F_3^4}, G0 = the linear maps with q(g x) = +- q(x) (order 2880), order 233 280.
Conjugacy classes of Aut(BH): pairs (class of g in G0, orbit of the centraliser of g on the cosets of (1 - g)V).
For one representative sigma of every non-identity class: the complete skeleton problem (hybrid encoding of
full_hybrid.py) plus "state(sigma x, sigma y) = sigma(state(x, y)) for every pair" plus "some pair is split".
The states do not depend on the gauge, so this expresses exactly the invariance of the class.
UNSAT for sigma: no non-trivial skeleton class is invariant under sigma (nor under a conjugate, nor under a power
... of which sigma is a power: if tau^k = sigma then tau-invariant implies sigma-invariant).

python sym_global_all.py <tmp dir> <seconds per class> <first index> <last index> [list]
Memory: cadical on about 55 000 variables, 430 000 clauses."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid

tmp, tl, i0, i1 = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); only_list = len(sys.argv) > 5
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")

def mat_apply(M, v): return tuple(sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4))
def mat_mul(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))
E4 = [tuple(int(i == j) for j in range(4)) for i in range(4)]; ident = tuple(E4)
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
glist = sorted(group)
def inverse(g):
    h = g
    while mat_mul(h, g) != ident: h = mat_mul(h, g)
    return h
inv = {g: inverse(g) for g in glist}
left = set(group); reps = []
while left:
    g = min(left); cls = {mat_mul(mat_mul(h, g), inv[h]) for h in glist}; reps.append((g, len(cls))); left -= cls
sigmas = []                                   # (g, v, description)
total = 0
for g, size in reps:
    cent = [h for h in glist if mat_mul(h, g) == mat_mul(g, h)]
    image = {sub(u, mat_apply(g, u)) for u in V}
    coset = lambda v: min(add(v, w) for w in image)
    seen = set()
    for v in V:
        c = coset(v)
        if c in seen: continue
        orb = {coset(mat_apply(h, c)) for h in cent}; seen |= orb
        # class size in Aut(BH): |class of g| * (number of cosets in the orbit) * |image|
        csize = size * len(orb) * len(image); total += csize
        if g == ident and c == coset((0, 0, 0, 0)): continue
        fixed = sum(1 for x in V if add(mat_apply(g, x), c) == x)
        sigmas.append((g, c, csize, fixed))
assert total == 233280, total
def order(g, v):
    k = 1; x = lambda p: add(mat_apply(g, p), v); pts = list(V); cur = [x(p) for p in pts]
    while cur != pts: cur = [x(p) for p in cur]; k += 1
    return k
sigmas.sort(key=lambda s: (order(s[0], s[1]), -s[3], s[2]))
print("conjugacy classes of non-identity automorphisms of BH: %d (total size %d)" % (len(sigmas), sum(s[2] for s in sigmas)), flush=True)
if only_list:
    for idx, (g, v, cs, fx) in enumerate(sigmas): print("  %2d: order %2d, class size %6d, fixed vertices %2d" % (idx, order(g, v), cs, fx))
    sys.exit()
nv, base, ev, xs = full_hybrid.build([])
base.append([-vs[0] for vs in xs.values()])
for idx in range(i0, min(i1 + 1, len(sigmas))):
    g, v, cs, fx = sigmas[idx]
    sg = [I[add(mat_apply(g, V[i]), v)] for i in range(n)]
    assert all((sg[b] in nbs[sg[a]]) == (b in nbs[a]) for a in range(0, n, 5) for b in range(n))
    extra = []
    for (a, b), vs in xs.items():
        k2 = key(sg[a], sg[b]); c, c2 = CN[(a, b)], CN[k2]
        for s in range(11):
            side = {sg[z] for i, z in enumerate(c) if (MASKS[s] >> i) & 1}
            m = sum(1 << i for i, z in enumerate(c2) if z in side)
            if m & 1: m ^= 63
            extra.append([-vs[s], xs[k2][MASKS.index(m)]])
    path = os.path.join(tmp, "syma_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base: f.write(" ".join(map(str, c)) + " 0\n")
        for c in extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("class %2d (order %2d, size %6d, %2d fixed vertices): invariant non-trivial skeleton: %s (%.1f s)" % (idx, order(g, v), cs, fx, res, time.time() - t0), flush=True)
    if res == "SAT":
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        edges = sorted(ev); open(os.path.join(tmp, "skeleton_class%d.txt" % idx), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
    try: os.remove(path)
    except OSError: pass
