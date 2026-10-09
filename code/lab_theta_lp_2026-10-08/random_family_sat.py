"""C1, lab session, 2026-10-09. Adversarial test of the exact parity law on members of the family that are NOT built by
hand: random graphs with every edge in exactly one triangle and every non-adjacent pair with 0 or 2 common neighbours,
regular of valency k on n vertices, found by a SAT solver with random decisions (cadical, the copy of the Codex
repository). For every graph found: components, a crude symmetry indicator (number of distinct vertex invariants), and
the test of two_layer_test.py: is  f + c_e (+1)  a coboundary, f = sign cochain of PHI', c_e = two-layer cycles.
A graph for which neither is a coboundary REFUTES the law.

  python random_family_sat.py <cadical.exe> <n> <k> <first seed> <number of seeds> <time limit per call s> [forced random edges]
One process, memory below 1 GB."""
import sys, os, subprocess, tempfile, random, collections, itertools, time, json
CADICAL = sys.argv[1]; n = int(sys.argv[2]); k = int(sys.argv[3]); SEED0 = int(sys.argv[4]); NSEED = int(sys.argv[5]); TLIM = int(sys.argv[6])
FORCE = int(sys.argv[7]) if len(sys.argv) > 7 else 0
OUT = sys.argv[8] if len(sys.argv) > 8 else None


def cnf(rng):
    nv = [0]; clauses = []
    def new():
        nv[0] += 1; return nv[0]
    E = {}
    for i in range(n):
        for j in range(i + 1, n): E[(i, j)] = new()
    e = lambda i, j: E[(min(i, j), max(i, j))]

    def counter(lits, top):
        prev = [None] * (top + 1)
        for t, x in enumerate(lits):
            cur = [None] * (top + 1)
            for j in range(1, min(top, t + 1) + 1):
                v = new(); cur[j] = v; a = prev[j]; b = prev[j - 1] if j > 1 else True
                if b is True:
                    if a is None: clauses.extend([[-v, x], [v, -x]])
                    else: clauses.extend([[-v, a, x], [v, -a], [v, -x]])
                elif b is None:
                    if a is None: clauses.append([-v])
                    else: clauses.extend([[-v, a], [v, -a]])
                else:
                    if a is None: clauses.extend([[-v, b], [-v, x], [v, -b, -x]])
                    else: clauses.extend([[-v, a, b], [-v, a, x], [v, -a], [v, -b, -x]])
            prev = cur
        return prev
    C = {}
    for i in range(n):
        for j in range(i + 1, n):
            for l in range(n):
                if l != i and l != j:
                    v = new(); C[(i, j, l)] = v; clauses.extend([[-v, e(i, l)], [-v, e(j, l)], [v, -e(i, l), -e(j, l)]])
    for i in range(n):
        for j in range(i + 1, n):
            s = counter([C[(i, j, l)] for l in range(n) if l != i and l != j], 3); eij = e(i, j)
            clauses.extend([[-eij, s[1]], [-eij, -s[2]], [eij, -s[3]], [eij, -s[1], s[2]]])
    for i in range(n):
        s = counter([e(i, j) for j in range(n) if j != i], k + 1)
        clauses.append([-s[k + 1]]); clauses.append([s[k]])
    # symmetry breaking: the neighbourhood of vertex 0 and its mates
    for j in range(1, n): clauses.append([e(0, j)] if j <= k else [-e(0, j)])
    for j in range(1, k + 1, 2): clauses.append([e(j, j + 1)])
    # vertex 1: its other neighbours are k+1 .. 2k-2 (first far vertices), a valid labelling of any solution
    for j in range(k + 1, n): clauses.append([e(1, j)] if j <= 2 * k - 2 else [-e(1, j)])
    # random forced non-edges / edges among the remaining pairs (kept only if satisfiable)
    free = [(i, j) for i in range(2, n) for j in range(i + 1, n) if not (i <= k and j <= k)]
    forced = []
    for (i, j) in rng.sample(free, min(FORCE, len(free))): forced.append(-e(i, j))
    return nv[0], clauses, E, forced


def solve(seed):
    rng = random.Random(seed); nvar, clauses, E, forced = cnf(rng)
    fd, path = tempfile.mkstemp(suffix=".cnf"); os.close(fd)
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nvar, len(clauses) + len(forced)))
        for c in clauses: f.write(" ".join(map(str, c)) + " 0\n")
        for u in forced: f.write("%d 0\n" % u)
    try:
        r = subprocess.run([CADICAL, "-q", "--seed=%d" % seed, "--shuffle=true", "--shufflerandom=true", "--randec=true", "--randecstable=true",
                            "--phase=%s" % ("true" if seed % 2 else "false"), path], capture_output=True, text=True, timeout=TLIM)
        out = r.stdout
    except subprocess.TimeoutExpired:
        out = ""
    os.remove(path)
    if "s UNSATISFIABLE" in out: return "UNSAT"
    if "s SATISFIABLE" not in out: return "UNKNOWN"
    val = set()
    for line in out.split("\n"):
        if line.startswith("v "): val.update(int(t) for t in line.split()[1:] if int(t) > 0)
    return [(i, j) for (i, j), v in E.items() if v in val]


def study(Eg):
    adj = [set() for _ in range(n)]
    for a, b in Eg: adj[a].add(b); adj[b].add(a)
    assert all(len(s) == k for s in adj)
    for a in range(n):
        for b in range(a + 1, n):
            cn = len(adj[a] & adj[b]); assert cn == 1 if b in adj[a] else cn in (0, 2)
    comp = [-1] * n; nc = 0
    for s0 in range(n):
        if comp[s0] < 0:
            st = [s0]; comp[s0] = nc
            while st:
                x = st.pop()
                for y in adj[x]:
                    if comp[y] < 0: comp[y] = nc; st.append(y)
            nc += 1
    third = {}
    for a, b in Eg:
        t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
    pi = lambda v, w, x: next(iter((adj[x] & adj[w]) - {v}))

    def sgn(d, o1, o2):
        pos = {y: i for i, y in enumerate(o2)}; p = [pos[d[x]] for x in o1]; seen = [False] * len(p); s = 0
        for i in range(len(p)):
            if not seen[i]:
                j = i; ln = 0
                while not seen[j]: seen[j] = True; j = p[j]; ln += 1
                s ^= (ln - 1) & 1
        return s
    order = [[v] + sorted(adj[v]) for v in range(n)]; f = {}; c = {}; shape = {}
    for a, b in Eg:
        t = third[(a, b)]; d = {a: a, b: b, t: t}
        for x in adj[a]:
            if x != b and x != t: d[x] = pi(a, b, x)
        f[(a, b)] = f[(b, a)] = sgn(d, order[a], order[b])
        X = [x for x in adj[a] if x != b and x != t]; seen = set(); cyc = []
        for x in X:
            if x in seen: continue
            u = x; ln = 0
            while u not in seen:
                seen.add(u); u1 = third[(a, u)]; seen.add(u1); y = pi(a, b, u1); y1 = third[(b, y)]; u = pi(b, a, y1); ln += 1
            cyc.append(ln)
        c[(a, b)] = c[(b, a)] = len(cyc); shape[(a, b)] = shape[(b, a)] = tuple(sorted(cyc))
    res = []
    for const in (0, 1):
        g = {e_: (f[e_] + c[e_] + const) % 2 for e_ in f}; pot = [None] * n; ok = True
        for s0 in range(n):
            if pot[s0] is not None: continue
            pot[s0] = 0; st = [s0]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if pot[y] is None: pot[y] = pot[x] ^ g[(x, y)]; st.append(y)
        res.append(all((pot[a] ^ pot[b]) == g[(a, b)] for a, b in Eg))
    # per component: is the plain sign class f itself a coboundary (+ constant)? and invariants of the vertices
    inv = collections.Counter(tuple(sorted(shape[(v, w)] for w in adj[v])) for v in range(n))
    diam2 = all(b in adj[a] or adj[a] & adj[b] for a in range(n) for b in range(a + 1, n))
    return nc, res, len(inv), collections.Counter(shape[e_] for e_ in Eg), diam2


found = collections.Counter(); t0 = time.time(); graphs = []
for seed in range(SEED0, SEED0 + NSEED):
    r = solve(seed)
    if isinstance(r, str):
        print("seed %d: %s  [%.0f s]" % (seed, r, time.time() - t0), flush=True); found[r] += 1; continue
    nc, res, ninv, shapes, diam2 = study(r); graphs.append(sorted(r))
    verdict = "LAW HOLDS (kappa = %d)" % (0 if res[0] else 1) if (res[0] or res[1]) else "*** LAW REFUTED ***"
    if res[0] and res[1]: verdict = "both (bipartite-like class)"
    print("seed %d: graph found, components %d, diameter two %s, distinct vertex invariants %d, edge shapes %s -> %s  [%.0f s]"
          % (seed, nc, diam2, ninv, dict(sorted(shapes.items())), verdict, time.time() - t0), flush=True)
    found[verdict] += 1
print("summary n = %d, k = %d:" % (n, k), dict(found))
if OUT: json.dump(graphs, open(OUT, "w"))
