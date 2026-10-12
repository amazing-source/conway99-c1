"""Lab session, 2026-10-12. Parity skeleton of an S3-cover of the Brouwer-Haemers graph BH = srg(81,20,1,6), in the
"line gauge". Question (note 175 of branch claude/v7-simultaneous, OPEN there): is there a srg(243,22,1,2) with a
regular spread whose gains cannot be gauged into A3? A necessary condition is a non-trivial PARITY SKELETON:
    eps : edges of BH -> F_2,  even on every line (the 270 triangles),  and for every non-adjacent pair (P, R) the six
    path parities eps(PZ) + eps(ZR) (Z a common neighbour) have weight 0, 3 or 6;
    non-trivial = not a coboundary (two vertex switchings give the same class).
Equivalently (A_eps + I)^2 = 0 modulo 3 for the signed adjacency matrix A_eps.

BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3 (elliptic quadric, 20 non-zero isotropic vectors).
Line gauge at the line l = {P0, P1, P2} = {0, e, 2e}, e = (0,0,1,0). Layers L_i = N(P_i) minus l (18 vertices each),
far = the 24 vertices with no neighbour on l. By switching, all edges of l and all edges P_i - L_i are positive (hence
the 27 tangent lines are positive), and every far vertex has a positive edge to its first layer neighbour: this fixes
the switching class representative completely (80 conditions). Then (hand, NOTE of the lab):
  * a vertex u of L_i has 0 or 3 negative edges to L_j (pair (P_j, u): the path through P_i is even);
  * a non-trivial class has a split pair, and (Aut(BH) is transitive on non-adjacent pairs, and for a split pair
    (P, R) one may take P = P1, R in L_0) one may assume that the vertex u0 = first vertex of L_0 has exactly three
    negative edges to L_1: the ten choices of these three edges are the "cubes" 0..9.

Output: a CNF (DIMACS) for cube c, or "all" for the disjunction-free instance "u0 has three negative edges to L_1".
XORs are written with auxiliary variables (plain CNF) or, with option xor, as native "x" lines for CryptoMiniSat.

python parity_line.py <cube 0..9 | all | free> <out.cnf> [xor]
  free = no assumption at all (the trivial class is then a solution: positive control, must be SAT with eps = 0
         unless "nontrivial" clauses are added; used for the controls).
python parity_line.py check <model file with the 810 edge values as 0/1 in the order of the generator>
Standard library only, a few seconds."""
import sys, itertools

V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}; n = 81
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
S = [v for v in V if any(v) and q(v) == 0]; assert len(S) == 20
nb = [sorted(I[add(V[i], s)] for s in S) for i in range(n)]; nbs = [set(a) for a in nb]
for i in range(n):
    for j in range(i + 1, n): assert len(nbs[i] & nbs[j]) == (1 if j in nbs[i] else 6)
edges = [(i, j) for i in range(n) for j in nb[i] if i < j]; eid = {e: k for k, e in enumerate(edges)}; assert len(edges) == 810
E = lambda a, b: eid[(a, b) if a < b else (b, a)]
lines = sorted({tuple(sorted((i, j, next(iter(nbs[i] & nbs[j]))))) for (i, j) in edges}); assert len(lines) == 270
pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if j not in nbs[i]]; assert len(pairs) == 2430
e = (0, 0, 1, 0); assert q(e) == 0
P = [I[(0, 0, 0, 0)], I[e], I[add(e, e)]]
L = [sorted(nbs[P[i]] - set(P)) for i in range(3)]
far = sorted(set(range(n)) - set(P) - set(L[0]) - set(L[1]) - set(L[2])); assert len(far) == 24
lay = {}
for i in range(3):
    for u in L[i]: lay[u] = i
# gauge: fixed positive edges
fixed = set()
for a in range(3):
    for b in range(a + 1, 3): fixed.add(E(P[a], P[b]))
for i in range(3):
    for u in L[i]: fixed.add(E(P[i], u))
for t in lines:
    if sum(1 for x in t if x in P) == 1:                    # tangent line: its third edge is positive by balance
        a, b = [x for x in t if x not in P]; fixed.add(E(a, b))
for w in far:
    fixed.add(E(w, min(x for x in nb[w] if x in lay)))
u0 = L[0][0]; D1 = sorted(x for x in nb[u0] if lay.get(x) == 1); assert len(D1) == 5
cubes = list(itertools.combinations(range(5), 3))


def build(mode, xor):
    nv = [810]; cl = []; xl = []
    def new(): nv[0] += 1; return nv[0]
    lit = {}                                               # edge -> None (constant 0) or variable
    for k in range(810): lit[k] = None if k in fixed else k + 1
    def xor_clauses(vs, rhs):                              # sum of the variables vs = rhs (mod 2)
        vs = [v for v in vs if v is not None]
        if not vs:
            if rhs: cl.append([])
            return
        if xor: xl.append((vs, rhs)); return
        while len(vs) > 3:                                 # chain
            t = new(); a, b = vs[0], vs[1]
            for sa in (0, 1):
                for sb in (0, 1):
                    cl.append([(-a if sa else a), (-b if sb else b), (-t if (sa ^ sb) == 0 else t)] if False else [a * (1 if not sa else -1), b * (1 if not sb else -1), t * (-1 if (sa ^ sb) else 1)])
            vs = [t] + vs[2:]
        m = len(vs)
        for bits in itertools.product((0, 1), repeat=m):
            if sum(bits) % 2 != rhs: cl.append([vs[i] * (-1 if bits[i] else 1) for i in range(m)])
    for t in lines: xor_clauses([lit[E(t[0], t[1])], lit[E(t[1], t[2])], lit[E(t[0], t[2])]], 0)
    for (a, b) in pairs:
        ws = []
        for z in sorted(nbs[a] & nbs[b]):
            x, y = lit[E(a, z)], lit[E(z, b)]
            if x is None and y is None: ws.append(0)
            elif x is None: ws.append(y)
            elif y is None: ws.append(x)
            else:
                t = new(); xor_clauses([x, y, t], 0); ws.append(t)
        const = sum(1 for w in ws if w == 0 and False)
        vs = [w for w in ws if w != 0]; k0 = len(ws) - len(vs)      # k0 path parities are the constant 0
        m = len(vs)
        for bits in itertools.product((0, 1), repeat=m):
            if sum(bits) not in (0, 3, 6): cl.append([vs[i] * (-1 if bits[i] else 1) for i in range(m)])
    if mode != "free":
        ev = [lit[E(u0, x)] for x in D1]; assert all(v is not None for v in ev)
        if mode == "all":
            for bits in itertools.product((0, 1), repeat=5):
                if sum(bits) != 3: cl.append([ev[i] * (-1 if bits[i] else 1) for i in range(5)])
        else:
            c = cubes[int(mode)]
            for i in range(5): cl.append([ev[i] if i in c else -ev[i]])
    return nv[0], cl, xl


def check(path):
    vals = [int(ch) for ch in open(path).read().split()[0]]; assert len(vals) == 810
    for t in lines: assert (vals[E(t[0], t[1])] + vals[E(t[1], t[2])] + vals[E(t[0], t[2])]) % 2 == 0, "line"
    split = 0
    for (a, b) in pairs:
        w = sum((vals[E(a, z)] + vals[E(z, b)]) % 2 for z in nbs[a] & nbs[b]); assert w in (0, 3, 6), "pair"
        split += w == 3
    print("valid parity skeleton; split pairs: %d of 2430; negative edges: %d" % (split, sum(vals)))


if __name__ == "__main__":
    if sys.argv[1] == "check": check(sys.argv[2]); sys.exit()
    mode = sys.argv[1]; xor = len(sys.argv) > 3
    nv, cl, xl = build(mode, xor)
    with open(sys.argv[2], "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(cl) + len(xl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
        for vs, rhs in xl: f.write("x" + " ".join(str(v if (i or rhs) else -v) for i, v in enumerate(vs)) + " 0\n")
    print("mode %s: %d variables, %d clauses, %d xors; fixed edges %d; layers %s; u0 = %d, its neighbours in L_1: %s"
          % (mode, nv, len(cl), len(xl), len(fixed), [len(x) for x in L], u0, D1))
