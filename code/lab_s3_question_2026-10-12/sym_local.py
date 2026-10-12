"""Lab session, 2026-10-12. Local problem at P = 0 (encoding of local_cnf2.py): search for local solutions that contain a
type B block and are INVARIANT under a given automorphism g of BH fixing P.

The stabiliser of P in Aut(BH) is the group of the linear maps g of F_3^4 with q(g x) = +- q(x) (order 2880). It is
generated here by closure from reflections and one anti-isometry; one representative of every conjugacy class of
non-identity elements is tried: the local problem with "some block is of type B" and "the states are g-invariant".
A SAT answer gives a local solution with a type B block (printed); UNSAT for g says that no such solution is g-invariant.

python sym_local.py <tmp dir> <seconds per call> [list]
  with "list": only print the conjugacy classes (order of the element, class size, cycle type on the 60 blocks).
  with "involutions": only the three classes of involutions without fixed point on N(P) (longer time limit)."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2]); only_list = len(sys.argv) > 3 and sys.argv[3] == "list"
only_inv = len(sys.argv) > 3 and sys.argv[3] == "involutions"     # only the three classes of involutions without fixed point on N(P)
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
V, I, q, Bf = L.V, L.I, L.q, L.Bf

def mat_apply(M, v): return tuple(sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4))
def mat_mul(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
def from_images(imgs): return tuple(tuple(imgs[j][i] for j in range(4)) for i in range(4))   # columns = images of the basis
gens = []
for w in V:
    if q(w) == 0: continue
    qi = q(w)                                                    # reflection x -> x - B(x,w)/q(w) w   (1/q = q in F_3)
    gens.append(from_images([tuple((E[j][i] - Bf(E[j], w) * qi * w[i]) % 3 for i in range(4)) for j in range(4)]))
# an anti-isometry: q(g x) = -q(x). q = x0^2 + x1^2 + x2 x3; take (x0, x1, x2, x3) -> (x0 + x1, x0 - x1, x2, -x3):
# (x0+x1)^2 + (x0-x1)^2 - x2 x3 = 2 x0^2 + 2 x1^2 - x2 x3 = -(x0^2 + x1^2 + x2 x3).
anti = ((1, 1, 0, 0), (1, 2, 0, 0), (0, 0, 1, 0), (0, 0, 0, 2))
assert all(q(mat_apply(anti, v)) == (-q(v)) % 3 for v in V)
gens.append(anti)
ident = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
group = {ident}; frontier = [ident]
while frontier:
    new = []
    for g in frontier:
        for h in gens:
            k = mat_mul(h, g)
            if k not in group: group.add(k); new.append(k)
    frontier = new
assert len(group) == 2880, len(group)
def perm(g): return [I[mat_apply(g, V[i])] for i in range(81)]
def order(g):
    k, h = 1, g
    while h != ident: h = mat_mul(h, g); k += 1
    return k
def inverse(g):
    h = g
    while mat_mul(h, g) != ident: h = mat_mul(h, g)
    return h
# conjugacy classes
left = set(group); left.discard(ident); classes = []
glist = sorted(group); inv = {g: inverse(g) for g in glist}
while left:
    g = min(left); cls = {mat_mul(mat_mul(h, g), inv[h]) for h in glist}
    classes.append((g, len(cls))); left -= cls
def cycle_type(p, pts):
    seen = set(); ct = {}
    for a in pts:
        if a in seen: continue
        n = 0; b = a
        while b not in seen: seen.add(b); b = p[b]; n += 1
        ct[n] = ct.get(n, 0) + 1
    return sorted(ct.items())
print("stabiliser of P: order %d, %d conjugacy classes of non-identity elements" % (len(group), len(classes)), flush=True)
nv, base, x, y = L.build([])
someB = [x[r][s] for r in L.far for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
for g, size in sorted(classes, key=lambda c: (order(c[0]), c[1])):
    p = perm(g); o = order(g); ct = cycle_type(p, L.far)
    if only_inv and not (o == 2 and cycle_type(p, L.NP) == [(2, 10)]): continue
    if only_list:
        print("order %d, class size %d, cycles on the blocks %s, on N(P) %s" % (o, size, ct, cycle_type(p, L.NP))); continue
    extra = [someB]
    for r in L.far:
        r2 = p[r]
        for s in range(11):
            side = {p[z] for i, z in enumerate(L.C[r]) if (L.MASKS[s] >> i) & 1}
            m = sum(1 << i for i, z in enumerate(L.C[r2]) if z in side)
            if m & 1: m ^= 63
            extra.append([-x[r][s], x[r2][L.MASKS.index(m)]])
    path = os.path.join(tmp, "sym_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    line = "element of order %d (class of %d, cycles on blocks %s): invariant solution with a type B block: %s (%.1f s)" % (o, size, ct, res, time.time() - t0)
    if res == "SAT":
        model = set(int(t) for l2 in out.split("\n") if l2.startswith("v ") for t in l2[2:].split() if int(t) > 0)
        st = {r: [s for s in range(11) if x[r][s] in model][0] for r in L.far}; types = {}
        for r in L.far:
            t = L.state_type(r, L.MASKS[st[r]]); types[t] = types.get(t, 0) + 1
        line += "  block types %s" % types
        with open(os.path.join(tmp, "sym_solution_order%d_class%d.txt" % (o, size)), "w") as f:
            f.write(repr({"g": g, "states": st}) + "\n")
    print(line, flush=True)
