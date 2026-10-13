"""Lab session, 2026-10-12. CENSUS of the strongly regular graphs (243,22,1,2) with a semiregular group of
automorphisms H = Z_3^4 (three orbits of 81 vertices): "tri-Cayley graphs" over Z_3^4.

Model: vertices (i, g), i in {0,1,2}, g in H; (i, g) ~ (j, h) iff h - g in D_ij, with D_ji = -D_ij, D_ii = -D_ii,
0 not in D_ii. The translations of H are automorphisms. Strong regularity: for all i, j, d with (i,0) != (j,d),
    sum_k #{g in D_ik : d - g in D_kj} = 1 if d in D_ij, 2 otherwise.
The matrix (|D_ij|) is the quotient matrix of an equitable partition: eigenvalues 22 and two of {4, -5}, |D_ii| even;
only two cases: TYPE I  |D_ii| = 10, |D_ij| = 6;   TYPE II  |D_ii| = 4, |D_ij| = 9.
Normal forms (proofs in NOTE_SPREADFREE.md):
  type I : D_00 is a cap of 5 projective points with no point on two secants = a frame; D_00 = +-{e1,e2,e3,e4,e1+e2+e3+e4};
           0 in D_01, 0 in D_02 (translations of the orbits 1 and 2);
  type II: D_00 = +-{e1,e2}; D_01 is a transversal of <e1,e2>, and 0, e3, e4 in D_01; 0 in D_02.
Enumeration: cadical; every solution is rebuilt as a graph, checked (strongly regular), identified by the number of 3x3
grids through each vertex and the number of flat lines, and then ALL its images in normal form (permutations of the
orbits, linear maps, translations) are blocked. The loop ends with UNSAT = the census is complete for that type.

python tricayley_census.py <tmp dir> <type: 1 or 2> <seconds per solver call> [max classes]
Memory: under 1 GB (instance below one million clauses)."""
import sys, os, subprocess, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trade_census, line_holonomy

H = list(itertools.product(range(3), repeat=4)); IDX = {g: i for i, g in enumerate(H)}; ZERO = (0, 0, 0, 0)
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b)); neg = lambda a: tuple((-x) % 3 for x in a)
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
REPS = [g for g in H if g != ZERO and g < neg(g)]
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]


def encode(typ):
    dsize, osize = (10, 6) if typ == 1 else (4, 9)
    D00 = set()
    for g in (E + [(1, 1, 1, 1)] if typ == 1 else E[:2]): D00 |= {g, neg(g)}
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    U = [dict() for _ in range(3)]
    for i in range(3):
        for g in REPS: v = new(); U[i][g] = v; U[i][neg(g)] = v
    V = {p: {g: new() for g in H} for p in [(0, 1), (0, 2), (1, 2)]}
    fixed = {}
    for g in REPS: fixed[U[0][g]] = (g in D00)
    fixed[V[(0, 1)][ZERO]] = True; fixed[V[(0, 2)][ZERO]] = True
    if typ == 2: fixed[V[(0, 1)][E[2]]] = True; fixed[V[(0, 1)][E[3]]] = True
    def m(i, k, g):
        if i == k: return None if g == ZERO else U[i][g]
        return V[(i, k)][g] if i < k else V[(k, i)][neg(g)]
    cache = {}
    def AND(a, b):
        """literal for a & b, or None if it is false, or "T" if true (a, b positive variables or None)"""
        if a is None or b is None: return None
        fa, fb = fixed.get(a), fixed.get(b)
        if fa is False or fb is False: return None
        if fa is True and fb is True: return "T"
        if fa is True: return b
        if fb is True: return a
        if a == b: return a
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            t = new(); cl.extend([[-t, a], [-t, b], [t, -a, -b]]); cache[k] = t
        return cache[k]
    def exactly(lits, k):
        """exactly k of lits; entries None (false) are dropped, "T" (true) lower k"""
        k -= sum(1 for l in lits if l == "T"); lits = [l for l in lits if l is not None and l != "T"]
        l2 = []
        for l in lits:
            f = fixed.get(l)
            if f is True: k -= 1
            elif f is None: l2.append(l)
        lits = l2
        if k < 0 or k > len(lits): cl.append([]); return
        if not lits: return
        prev = None
        for l in lits:
            cur = [None] + [new() for _ in range(k + 1)]
            for j in range(1, k + 2):
                pj = prev[j] if prev else None
                if pj is not None: cl.append([-pj, cur[j]])
                if j == 1: cl.append([-l, cur[j]])
                elif prev: cl.append([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cl.append(c + [l])
                if j > 1: cl.append(c + ([prev[j - 1]] if prev else []))
            prev = cur
        if k >= 1: cl.append([prev[k]])
        cl.append([-prev[k + 1]])
    for v, b in fixed.items(): cl.append([v] if b else [-v])
    for i in range(3): exactly([U[i][g] for g in REPS], dsize // 2)
    for p in V: exactly(list(V[p].values()), osize)
    if typ == 2:
        # redundant but propagating (proved in the note): D_01 and D_02 are transversals of U_0 = <e1, e2>
        for p in [(0, 1), (0, 2)]:
            for c in itertools.product(range(3), repeat=2):
                exactly([V[p][g] for g in H if g[2:] == c], 1)
    for i in range(3):
        for j in range(i, 3):
            for d in (REPS if i == j else H):
                lits = [AND(m(i, k, g), m(k, j, sub(d, g))) for k in range(3) for g in H]
                lits.append(m(i, j, d))
                exactly(lits, 2)
    return nv[0], cl, U, V


def graph_of(D):
    """D[(i,j)] for all ordered i, j -> adjacency lists on 243 vertices"""
    adj = [set() for _ in range(243)]
    for i in range(3):
        for j in range(3):
            for g in H:
                for d in D[(i, j)]: adj[81 * i + IDX[g]].add(81 * j + IDX[add(g, d)])
    return adj


def identify(adj):
    grids = tuple(trade_census.grids_profile(243, adj))
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(243) for y in adj[x] if x < y})
    flat = sum(1 for (p, u, us) in lines if all(c == 1 for c in line_holonomy.cycle_type(line_holonomy.holonomy(adj, p, u, us))))
    known = {((55, 243),): "BvLS", ((13, 180), (19, 60), (55, 3)): "twin", ((23, 243),): "Gamma3", ((31, 243),): "Gamma4",
             ((25, 243),): "fifth (Gamma5)", ((17, 243),): "sixth or seventh", ((19, 243),): "eighth"}
    return known.get(grids, "NEW ?"), grids, flat


def images(D, typ):
    """all normal-form images of the solution D (dict over ordered pairs (i,j) of frozensets)"""
    std = set()
    for g in (E + [(1, 1, 1, 1)] if typ == 1 else E[:2]): std |= {g, neg(g)}
    out = set()
    def inverse_table(B):
        """B = images of e1..e4; returns the dict x -> coordinates of x in the basis B, or None if B is not a basis"""
        tab = {}
        for c in H: tab[tuple((c[0] * B[0][t] + c[1] * B[1][t] + c[2] * B[2][t] + c[3] * B[3][t]) % 3 for t in range(4))] = c
        return tab if len(tab) == 81 else None
    for perm in itertools.permutations(range(3)):
        Dp = {(i, j): D[(perm[i], perm[j])] for i in range(3) for j in range(3)}
        d00 = sorted(Dp[(0, 0)])
        if typ == 1:                                                         # the linear maps do not depend on a
            maps = []
            for b in itertools.permutations(d00, 4):
                A = inverse_table(b)
                if A is not None and {A[x] for x in Dp[(0, 0)]} == std: maps.append(A)
            assert len(maps) == 240, len(maps)
        for a in sorted(Dp[(0, 1)]):
            T01 = {sub(x, a) for x in Dp[(0, 1)]}
            if typ == 2:
                maps = []
                for b in itertools.permutations(d00, 2):
                    for tl in itertools.permutations(sorted(T01 - {ZERO}), 2):
                        A = inverse_table(list(b) + list(tl))
                        if A is not None and {A[x] for x in Dp[(0, 0)]} == std: maps.append(A)
            for A in maps:
                n01 = frozenset(A[x] for x in T01)
                n11 = frozenset(A[x] for x in Dp[(1, 1)]); n22 = frozenset(A[x] for x in Dp[(2, 2)])
                for bb in Dp[(0, 2)]:
                    n02 = frozenset(A[sub(x, bb)] for x in Dp[(0, 2)])
                    n12 = frozenset(A[sub(add(x, a), bb)] for x in Dp[(1, 2)])
                    out.add((n11, n22, n01, n02, n12))
    return out


if __name__ == "__main__":
    tmp, typ, tl = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]); maxc = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    t0 = time.time(); nv, cl, U, V = encode(typ)
    print("tri-Cayley over Z_3^4, type %s: %d variables, %d clauses (built in %.0f s)" % ("I" if typ == 1 else "II", nv, len(cl), time.time() - t0), flush=True)
    block = []; found = []
    path = os.path.join(tmp, "tricay_%d_%d.cnf" % (typ, os.getpid()))
    while len(found) < maxc:
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv, len(cl) + len(block)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
            for c in block: f.write(" ".join(map(str, c)) + " 0\n")
        t1 = time.time()
        try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
        if res != "SAT":
            print("solver call %d: %s (%.1f s) with %d blocking clauses" % (len(found) + 1, res, time.time() - t1, len(block)), flush=True)
            break
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        D = {}
        for i in range(3): D[(i, i)] = frozenset(g for g in H if g != ZERO and U[i][g] in model)
        for (i, j) in V:
            D[(i, j)] = frozenset(g for g in H if V[(i, j)][g] in model); D[(j, i)] = frozenset(neg(g) for g in D[(i, j)])
        adj = graph_of(D); ok = trade_census.is_srg(243, adj)
        name, grids, flat = identify(adj) if ok else ("NOT SRG", None, None)
        imgs = images(D, typ)
        me = (D[(1, 1)], D[(2, 2)], D[(0, 1)], D[(0, 2)], D[(1, 2)]); assert me in imgs, "the solution is not among its own images"
        for (n11, n22, n01, n02, n12) in imgs:
            c = [-U[1][g] for g in n11 if g in REPS] + [-U[2][g] for g in n22 if g in REPS]
            c += [-V[(0, 1)][g] for g in n01] + [-V[(0, 2)][g] for g in n02] + [-V[(1, 2)][g] for g in n12]
            block.append(c)
        found.append((name, grids, flat, len(imgs)))
        print("class %d (%.1f s): strongly regular %s; %s; grids through a vertex %s; flat lines %s; %d normal-form images blocked" % (len(found), time.time() - t1, ok, name, grids, flat, len(imgs)), flush=True)
        if ok and name == "NEW ?":
            outp = os.path.join(tmp, "tricayley_new_type%d_%d.edges" % (typ, len(found)))
            with open(outp, "w", newline="\n") as f:
                for a in range(243):
                    for b in sorted(adj[a]):
                        if a < b: f.write("%d %d\n" % (a, b))
            print("   written to %s" % outp, flush=True)
    print("summary type %s: %s" % ("I" if typ == 1 else "II", collections.Counter(n for n, _, _, _ in found).most_common()), flush=True)
    try: os.remove(path)
    except OSError: pass
