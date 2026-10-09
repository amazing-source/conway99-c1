"""C1, lab session, 2026-10-09. Is the quadrangle law  c(Q) = c_va + c_az + c_zb + c_bv (mod 2)  a LOCAL consequence of
the axioms?  A quadrangle Q = (v, a, z, b) with its four closed walls is the core (4k - 8 vertices, valency k). The SAT
solver is free to choose every cross matching and every other edge; it must give degree k to the core vertices, exactly
one common neighbour to adjacent pairs and 0 or 2 to non-adjacent pairs, for every pair containing a core vertex
(mode full) or for pairs of core vertices only (mode corepairs); the other pairs only get the upper bounds. For every
model found the parity of  c(Q) + sum of c_e  is computed from the model. An ODD model shows that the law does not
follow from the axioms at this radius. Random decisions give different models for different seeds.

  python quad_free_sat.py <cadical.exe> <valency k> <extra vertices> <first seed> <number of seeds> <time limit s> [full|corepairs]
One process, below 2 GB."""
import sys, os, subprocess, tempfile, itertools, collections, time, random
CADICAL = sys.argv[1]; K = int(sys.argv[2]); EXTRA = int(sys.argv[3]); SEED0 = int(sys.argv[4]); NSEED = int(sys.argv[5]); TLIM = int(sys.argv[6])
MODE = sys.argv[7] if len(sys.argv) > 7 else "full"
H = (K - 4) // 2                                            # free mate pairs per wall
Q = ["v", "a", "z", "b"]; NEXT = {"v": "a", "a": "z", "z": "b", "b": "v"}; PREV = {y: x for x, y in NEXT.items()}
T = {p: "t" + p + NEXT[p] for p in Q}                        # third point of the side p - next(p)
R = {p: ["%s%d%s" % (p, i, s) for i in range(H) for s in ("", "'")] for p in Q}
CORE = Q + [T[p] for p in Q] + [x for p in Q for x in R[p]]
IDX = {c: i for i, c in enumerate(CORE)}; nc = len(CORE); N = nc + EXTRA
WALL = {p: [NEXT[p], T[p], PREV[p], T[PREV[p]]] + R[p] for p in Q}       # N(p), mates consecutive


def build(seed):
    nv = [0]; clauses = []
    def new():
        nv[0] += 1; return nv[0]
    E = {}
    for i in range(N):
        for j in range(i + 1, N): E[(i, j)] = new()
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
    # fixed part: the neighbourhoods of the four vertices of Q and the mates inside every wall
    fixed = {}
    def put(x, y, val):
        k_ = frozenset((x, y)); assert fixed.setdefault(k_, val) == val, (x, y)
    for p in Q:
        for c in CORE + ["x%d" % i for i in range(EXTRA)]:
            if c != p: put(p, c, c in WALL[p])
        w = WALL[p]
        for i, x in enumerate(w):
            for j in range(i + 1, len(w)): put(x, w[j], j == i + 1 and i % 2 == 0)
    name = CORE + ["x%d" % i for i in range(EXTRA)]; idx = {c: i for i, c in enumerate(name)}
    for k_, val in fixed.items():
        x, y = tuple(k_); clauses.append([e(idx[x], idx[y]) if val else -e(idx[x], idx[y])])
    C = {}
    for i in range(N):
        for j in range(i + 1, N):
            for l in range(N):
                if l != i and l != j:
                    v = new(); C[(i, j, l)] = v; clauses.extend([[-v, e(i, l)], [-v, e(j, l)], [v, -e(i, l), -e(j, l)]])
    for i in range(N):
        for j in range(i + 1, N):
            s = counter([C[(i, j, l)] for l in range(N) if l != i and l != j], 3); eij = e(i, j)
            if (i < nc and MODE == "full") or (j < nc and MODE == "corepairs"):
                clauses.extend([[-eij, s[1]], [-eij, -s[2]], [eij, -s[3]], [eij, -s[1], s[2]]])
            else:
                clauses.extend([[-eij, -s[2]], [eij, -s[3]]])
    for i in range(N):
        s = counter([e(i, j) for j in range(N) if j != i], K + 1)
        clauses.append([-s[K + 1]])
        if i < nc: clauses.append([s[K]])
    return nv[0], clauses, E, name


def solve(seed):
    nvar, clauses, E, name = build(seed)
    fd, path = tempfile.mkstemp(suffix=".cnf"); os.close(fd)
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nvar, len(clauses)))
        for c in clauses: f.write(" ".join(map(str, c)) + " 0\n")
    try:
        r = subprocess.run([CADICAL, "-q", "--seed=%d" % seed, "--shuffle=true", "--shufflerandom=true", "--randec=true", "--randecstable=true",
                            "--phase=%s" % ("true" if seed % 2 else "false")] + [path], capture_output=True, text=True, timeout=TLIM)
        out = r.stdout
    except subprocess.TimeoutExpired:
        out = ""
    os.remove(path)
    if "s UNSATISFIABLE" in out: return "UNSAT", None
    if "s SATISFIABLE" not in out: return "UNKNOWN", None
    val = set()
    for line in out.split("\n"):
        if line.startswith("v "): val.update(int(t) for t in line.split()[1:] if int(t) > 0)
    adj = {c: set() for c in name}
    for (i, j), v in E.items():
        if v in val: adj[name[i]].add(name[j]); adj[name[j]].add(name[i])
    return "SAT", adj


def analyse(adj):
    third = lambda x, y: next(iter(adj[x] & adj[y]))
    pi = lambda p, q, x: next(iter((adj[x] & adj[q]) - {p}))

    def phi(p, q):
        t = third(p, q); d = {p: p, q: q, t: t}
        for x in adj[p]:
            if x != q and x != t:
                cn = (adj[x] & adj[q]) - {p}; assert len(cn) == 1, (p, q, x, cn); d[x] = next(iter(cn))
        return d

    def two_layer(p, q):
        t = third(p, q); X = [x for x in adj[p] if x != q and x != t]; seen = set(); cyc = []
        for x in X:
            if x in seen: continue
            u = x; ln = 0
            while u not in seen:
                seen.add(u); u1 = third(p, u); seen.add(u1); y = pi(p, q, u1); y1 = third(q, y); u = pi(q, p, y1); ln += 1
            cyc.append(ln)
        return tuple(sorted(cyc))
    d1, d2, d3, d4 = phi("v", "a"), phi("a", "z"), phi("z", "b"), phi("b", "v")
    dom = ["v"] + sorted(adj["v"]); hol = {x: d4[d3[d2[d1[x]]]] for x in dom}
    seen = set(); cyc = 0
    for s in dom:
        if s in seen: continue
        cyc += 1; u = s
        while u not in seen: seen.add(u); u = hol[u]
    omega = (len(dom) - cyc) % 2
    shapes = [two_layer("v", "a"), two_layer("a", "z"), two_layer("z", "b"), two_layer("b", "v")]
    return (omega + sum(len(s) for s in shapes)) % 2, omega, shapes


res = collections.Counter(); t0 = time.time()
print("valency %d, core %d vertices, %d extra, mode %s" % (K, nc, EXTRA, MODE), flush=True)
for seed in range(SEED0, SEED0 + NSEED):
    st, adj = solve(seed)
    if st != "SAT":
        print("seed %d: %s  [%.0f s]" % (seed, st, time.time() - t0), flush=True); res[st] += 1; continue
    par, omega, shapes = analyse(adj)
    print("seed %d: model, holonomy sign %d, side types %s -> parity of (f + c)(Q) = %d %s  [%.0f s]"
          % (seed, omega, shapes, par, "" if par == 0 else "*** ODD ***", time.time() - t0), flush=True)
    res["even" if par == 0 else "ODD"] += 1
print("summary:", dict(res))
