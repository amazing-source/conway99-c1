"""C1, lab session, 2026-10-09. Is the parity formula  c(Q) = c_va + c_aw + c_wb + c_bv (mod 2)  forced LOCALLY?
Smallest case: valency 6 (three lines through every vertex). A quadrangle Q = (v, a, w, b) and its four walls form
16 vertices: Q, the four ears a', p, q, b' (third points of the sides) and one free mate pair in each wall.
Every abstract configuration of the four cross matchings is enumerated (up to the symmetries of the labelling), its
parity is computed, and a SAT instance asks for a partial geometry around it:
  - all 16 core vertices have degree exactly 6;
  - every pair containing a core vertex: adjacent -> exactly one common neighbour, non-adjacent -> 0 or 2;
  - every other pair: adjacent -> at most one common neighbour, non-adjacent -> at most two; degree at most 6.
UNSAT = the configuration cannot occur in any graph of the family (a local exclusion); SAT = locally consistent at
this radius (nothing more). Solver: cadical (the copy shipped in the Codex repository), one process, time limit.

  python local_quad_sat.py <cadical.exe> <number of extra vertices> <time limit per instance s> [max instances]"""
import sys, os, itertools, subprocess, tempfile, time, collections
CADICAL = sys.argv[1]; EXTRA = int(sys.argv[2]); TLIM = int(sys.argv[3]); MAXI = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
FREE = int(sys.argv[5]) if len(sys.argv) > 5 else 1            # free mate pairs per wall: valency = 4 + 2 * FREE
MODE = sys.argv[6] if len(sys.argv) > 6 else "full"            # full | corepairs (axioms only for pairs of core vertices)
import random
random.seed(int(sys.argv[7]) if len(sys.argv) > 7 else 1)
Qv = ["v", "a", "w", "b"]
def fr(c): return [c + str(i) + s_ for i in range(FREE) for s_ in ("", "'")]
WALL = {"v": ["a", "a'", "b", "b'"] + fr("x"), "a": ["v", "a'", "w", "p"] + fr("y"),
        "w": ["a", "p", "b", "q"] + fr("z"), "b": ["w", "q", "v", "b'"] + fr("u")}
MATE = {}
for u_, pts in WALL.items():
    for i in range(0, len(pts), 2): MATE[(u_, pts[i])] = pts[i + 1]; MATE[(u_, pts[i + 1])] = pts[i]
EDGES = [("v", "a"), ("a", "w"), ("w", "b"), ("b", "v")]
FORCED = {("v", "a"): ("b", "w"), ("a", "w"): ("v", "b"), ("w", "b"): ("a", "v"), ("b", "v"): ("w", "a")}


def domain(e):
    s, t = e; third = MATE[(s, t)]
    return [x for x in WALL[s] if x not in (t, third)], [y for y in WALL[t] if y not in (s, third)]


def all_configs():
    opts = []
    for e in EDGES:
        src, dst = domain(e); f0, f1 = FORCED[e]; rs = [x for x in src if x != f0]; rd = [y for y in dst if y != f1]; o = []
        for perm in itertools.permutations(rd):
            d = {f0: f1}; d.update(zip(rs, perm)); o.append(d)
        opts.append(o)
    for combo in itertools.product(*opts):
        P = dict(zip(EDGES, combo))
        # the same pair of vertices may be seen from two pairs of consecutive walls: the answers must agree
        adj = {}
        ok = True
        for e in EDGES:
            src, dst = domain(e)
            for x in src:
                for y in dst:
                    val = (P[e][x] == y); key = frozenset((x, y))
                    if len(key) == 1: ok = False
                    if adj.setdefault(key, val) != val: ok = False
        if ok: yield P


def parity(P):
    def two_layer(e):
        s, t = e; d = P[e]; inv = {y: x for x, y in d.items()}; seen = set(); c = 0
        for x in d:
            if x in seen: continue
            c += 1; z = x
            while z not in seen:
                seen.add(z); z1 = MATE[(s, z)]; seen.add(z1); y = d[z1]; y1 = MATE[(t, y)]; z = inv[y1]
        return c

    def phi(e, x):
        s, t = e
        return x if x in (s, t, MATE[(s, t)]) else P[e][x]
    dom = [x for x in WALL["v"] if x not in ("a", "b")]; hol = {}
    for x in dom:
        y = x
        for e in EDGES: y = phi(e, y)
        hol[x] = y
    assert set(hol.values()) == set(dom)
    seen = set(); cq = 0
    for x in dom:
        if x in seen: continue
        cq += 1; z = x
        while z not in seen: seen.add(z); z = hol[z]
    cs = [two_layer(e) for e in EDGES]
    return (cq + sum(cs)) % 2, cq, tuple(cs)


CORE = Qv + ["a'", "p", "q", "b'"] + fr("x") + fr("y") + fr("z") + fr("u")
IDX = {c: i for i, c in enumerate(CORE)}


def core_adjacency(P):
    """dict frozenset -> True / False for the pairs of core vertices that are determined; the others are free"""
    A = {}
    def put(x, y, val):
        k = frozenset((x, y)); assert A.setdefault(k, val) == val, (x, y)
    for s in Qv:
        for t in CORE:
            if t != s: put(s, t, t in WALL[s])
    for s in Qv:
        for x, y in itertools.combinations(WALL[s], 2): put(x, y, MATE[(s, x)] == y)
    for e in EDGES:
        src, dst = domain(e)
        for x in src:
            for y in dst: put(x, y, P[e][x] == y)
    return A


def canon(P):
    """canonical form under the swaps of the four free pairs (the dihedral symmetries of Q are not used)"""
    best = None
    for bits in itertools.product((0, 1), repeat=4):
        ren = {c: c for c in CORE}
        for bit, (m, n) in zip(bits, (("x0", "x0'"), ("y0", "y0'"), ("z0", "z0'"), ("u0", "u0'"))):
            if bit: ren[m], ren[n] = n, m
        key = tuple(tuple(sorted((ren[x], ren[y]) for x, y in P[e].items())) for e in EDGES)
        if best is None or key < best: best = key
    return best


def cnf_for(P, N):
    A = core_adjacency(P); nv = [0]; clauses = []
    def new():
        nv[0] += 1; return nv[0]
    E = {}
    for i in range(N):
        for j in range(i + 1, N): E[(i, j)] = new()
    e = lambda i, j: E[(min(i, j), max(i, j))]
    for k, val in A.items():
        x, y = tuple(k); clauses.append([e(IDX[x], IDX[y]) if val else -e(IDX[x], IDX[y])])
    nc = len(CORE)

    def counter(lits, top):
        """returns s[1..top] with s[j] <-> at least j of the literals are true"""
        prev = [None] * (top + 1)
        for t, x in enumerate(lits):
            cur = [None] * (top + 1)
            for j in range(1, min(top, t + 1) + 1):
                v = new(); cur[j] = v
                a = prev[j]                     # at least j among the first t
                b = prev[j - 1] if j > 1 else True   # at least j-1 among the first t
                # v <-> a or (b and x)
                if b is True:
                    if a is None: clauses.extend([[-v, x], [v, -x]])
                    else: clauses.extend([[-v, a, x], [v, -a], [v, -x]])
                elif b is None:                 # j - 1 > t : impossible
                    if a is None: clauses.append([-v])
                    else: clauses.extend([[-v, a], [v, -a]])
                else:
                    if a is None: clauses.extend([[-v, b], [-v, x], [v, -b, -x]])
                    else: clauses.extend([[-v, a, b], [-v, a, x], [v, -a], [v, -b, -x]])
            prev = cur
        return prev
    C = {}
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(N):
                if k != i and k != j:
                    v = new(); C[(i, j, k)] = v; clauses.extend([[-v, e(i, k)], [-v, e(j, k)], [v, -e(i, k), -e(j, k)]])
    for i in range(N):
        for j in range(i + 1, N):
            s = counter([C[(i, j, k)] for k in range(N) if k != i and k != j], 3); eij = e(i, j)
            if (i < nc and MODE == "full") or (j < nc and MODE == "corepairs"):   # exact axioms
                clauses.extend([[-eij, s[1]], [-eij, -s[2]], [eij, -s[3]], [eij, -s[1], s[2]]])
            else:
                clauses.extend([[-eij, -s[2]], [eij, -s[3]]])
    for i in range(N):
        s = counter([e(i, j) for j in range(N) if j != i], VAL + 1)
        clauses.append([-s[VAL + 1]])
        if i < nc: clauses.append([s[VAL]])
    for i in range(nc, N - 1):                  # mild symmetry breaking on the extra vertices: used in order
        # vertex i+1 has a neighbour only if vertex i has one
        s1 = [e(i, j) for j in range(N) if j != i]; s2 = [e(i + 1, j) for j in range(N) if j != i + 1]
        for l in s2: clauses.append([-l] + s1)
    return nv[0], clauses


def solve(P, N):
    nvar, clauses = cnf_for(P, N)
    fd, path = tempfile.mkstemp(suffix=".cnf"); os.close(fd)
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (nvar, len(clauses)))
        for c in clauses: f.write(" ".join(map(str, c)) + " 0\n")
    try:
        r = subprocess.run([CADICAL, "-q", path], capture_output=True, text=True, timeout=TLIM)
        out = r.stdout
    except subprocess.TimeoutExpired:
        out = ""
    os.remove(path)
    return "SAT" if "s SATISFIABLE" in out else "UNSAT" if "s UNSATISFIABLE" in out else "UNKNOWN"


VAL = 4 + 2 * FREE


def random_config():
    while True:
        P = {}
        for e in EDGES:
            src, dst = domain(e); f0, f1 = FORCED[e]; rs = [x for x in src if x != f0]; rd = [y for y in dst if y != f1]
            random.shuffle(rd); d = {f0: f1}; d.update(zip(rs, rd)); P[e] = d
        adj = {}; ok = True
        for e in EDGES:
            src, dst = domain(e)
            for x in src:
                for y in dst:
                    if adj.setdefault(frozenset((x, y)), P[e][x] == y) != (P[e][x] == y): ok = False
        if ok: return P


seen = {}
if FREE == 1:
    for P in all_configs():
        k = canon(P)
        if k not in seen: seen[k] = P
else:
    want = {0: MAXI // 2, 1: MAXI - MAXI // 2}
    while sum(want.values()) > 0:
        P = random_config(); pr = parity(P)[0]
        if want[pr] > 0: want[pr] -= 1; seen[len(seen)] = P
print("valency %d, mode %s: abstract four-wall configurations taken: %d" % (VAL, MODE, len(seen)))
par = collections.Counter(parity(P)[0] for P in seen.values()); print("parity of c(Q) + sum of c_e over them:", dict(par))
N = len(CORE) + EXTRA; res = collections.Counter(); t0 = time.time(); done = 0
for k, P in sorted(seen.items(), key=lambda kv: -parity(kv[1])[0]):   # odd ones first
    if done >= MAXI: break
    pr, cq, cs = parity(P); ans = solve(P, N); res[(pr, ans)] += 1; done += 1
    pris = int(P[("v", "a")]["b'"] == "p") + int(P[("a", "w")]["a'"] == "q")
    print("parity %d  c(Q) %d  c_e %s  prism extensions %d : %s   [%.0f s]" % (pr, cq, cs, pris, ans, time.time() - t0), flush=True)
print("summary (parity, answer) -> count:", dict(sorted(res.items())))
