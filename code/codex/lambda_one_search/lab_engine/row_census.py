"""Lab session, 2026-10-13. CENSUS OF THE COMPLETIONS OF A KEPT THIRD, by cases on the neighbourhood of one vertex.

Input: a graph srg(243,22,1,2) whose first 81 vertices R are kept with all their adjacencies (inside R and from R to
the 162 other vertices F). Unknown: the adjacency inside F, no symmetry imposed (encoding of free_trade.py).
Step 1: all candidate neighbourhoods inside F of the vertex f0 = 81 allowed by R alone (linear conditions with the 81
vertices of R, degree, two F-vertices with two common neighbours in R are not both neighbours of f0): a short complete
list (930 for the fifth graph). Step 2: orbits of this list under the automorphisms of the input that preserve R and
fix f0 (they map completions to completions). Step 3: for one candidate per orbit, the neighbourhood of f0 is fixed
and cadical lists ALL completions (each blocked), until UNSAT. Every completion is checked (A^2 = 20I - A + 2J), keyed
by invariants, compared by isomorphism with the known graphs; new graphs are written out with their automorphism group.
If every case ends with UNSAT, the union of the lists is the complete list of the completions of this third, up to
the automorphisms used.

python row_census.py <out dir> <edge file> <seconds per solver call> <first case> <last case> [references ...]
environment PYLIB = directory of pycryptosat.      Memory: cadical about 4.5 GB (28 million clauses), one process."""
import sys, os, subprocess, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import pycryptosat
import aut_tools as T, trade_bfs as B, regular_subgroups as RS
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
n = 243


def counter(cl, new, lits, k):
    if k < 0 or k > len(lits): cl([]); return
    if not lits: return
    prev = None
    for l in lits:
        cur = [None] + [new() for _ in range(k + 1)]
        for j in range(1, k + 2):
            pj = prev[j] if prev else None
            if pj is not None: cl([-pj, cur[j]])
            if j == 1: cl([-l, cur[j]])
            elif prev: cl([-l, -prev[j - 1], cur[j]])
            c = [-cur[j]] + ([pj] if pj is not None else [])
            cl(c + [l])
            if j > 1: cl(c + ([prev[j - 1]] if prev else []))
        prev = cur
    if k >= 1: cl([prev[k]])
    cl([-prev[k + 1]])


def candidate_rows(adj, R, F, f0):
    Rs = set(R); var = {g: i + 1 for i, g in enumerate(v for v in F if v != f0)}; nv = [len(var)]; cls = []
    def new(): nv[0] += 1; return nv[0]
    for r in R: counter(cls.append, new, [var[g] for g in sorted(adj[r] - Rs) if g != f0], (1 if f0 in adj[r] else 2) - len(adj[r] & adj[f0] & Rs))
    counter(cls.append, new, list(var.values()), 22 - len(adj[f0] & Rs))
    for g, h in itertools.combinations(sorted(var), 2):
        if len(adj[g] & adj[h] & Rs) == 2: cls.append([-var[g], -var[h]])
    s = pycryptosat.Solver(); s.add_clauses(cls); rows = []
    while True:
        sat, sol = s.solve()
        if not sat: return rows
        N = frozenset(g for g in var if sol[var[g]]); rows.append(N); s.add_clause([-var[g] for g in N])


if __name__ == "__main__":
    outdir, path, tl, c0, c1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    A0 = T.load(path); known = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[6:]]; keys = {nm: B.invariant(A) for nm, A in known}
    R = list(range(81)); Rs = set(R); F = list(range(81, n)); f0 = 81; adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]
    o, gens, base, sizes = T.aut_group(A0); ident = tuple(range(n)); G = RS.generate([tuple(g) for g in gens], ident)
    stab = [g for g in G if g[f0] == f0 and all(g[v] in Rs for v in R)]
    rows = candidate_rows(adj, R, F, f0); seen = set(); reps = []
    for N in sorted(rows, key=sorted):
        if N in seen: continue
        orb = {frozenset(g[v] for v in N) for g in stab}; seen |= orb; reps.append((N, len(orb)))
    old = frozenset(adj[f0] - Rs)
    print("%d candidate neighbourhoods of the vertex %d, %d orbits under the %d automorphisms preserving R and fixing it; orbit sizes %s" % (len(rows), f0, len(reps), len(stab), sorted(collections.Counter(sz for _, sz in reps).items())), flush=True)
    # base CNF, streamed once
    t0 = time.time(); nv = [0]; nc = [0]; cnf = os.path.join(outdir, "rowcensus_%d.cnf" % os.getpid()); out = open(cnf, "w+", newline="\n"); HEAD = "p cnf %12d %12d\n"; out.write(HEAD % (0, 0))
    def new(): nv[0] += 1; return nv[0]
    def emit(c): out.write(" ".join(map(str, c)) + " 0\n"); nc[0] += 1
    X = {}
    for i, a in enumerate(F):
        for b in F[i + 1:]: X[(a, b)] = new()
    x = lambda a, b: X[(a, b)] if a < b else X[(b, a)]
    cache = {}
    def AND(a, b):
        k = (a, b) if a < b else (b, a); t = cache.get(k)
        if t is None:
            t = new(); cache[k] = t; emit([-t, a]); emit([-t, b]); emit([t, -a, -b])
        return t
    nbF = {v: sorted(adj[v] - Rs) for v in range(n)}; nbR = {v: adj[v] & Rs for v in range(n)}
    for r in R:
        for f in F: counter(emit, new, [x(g, f) for g in nbF[r] if g != f], (1 if f in adj[r] else 2) - len(nbR[r] & nbR[f]))
    for f in F: counter(emit, new, [x(f, g) for g in F if g != f], 22 - len(nbR[f]))
    for i, f in enumerate(F):
        for g in F[i + 1:]:
            tgt = 2 - len(nbR[f] & nbR[g])
            if tgt == 0:
                emit([-x(f, g)])
                for h in F:
                    if h != f and h != g: emit([-x(f, h), -x(g, h)])
            else: counter(emit, new, [AND(x(f, h), x(g, h)) for h in F if h != f and h != g] + [x(f, g)], tgt)
    out.flush(); base_pos = out.tell(); base_nc = nc[0]; free = sorted(X.values())
    print("base CNF: %d variables, %d clauses (%.0f s)" % (nv[0], nc[0], time.time() - t0), flush=True)
    summary = collections.Counter(); undecided = []
    for ci, (N, sz) in enumerate(reps):
        if ci < c0 or ci > c1: continue
        out.seek(base_pos); out.truncate(); nc[0] = base_nc
        for g in F:
            if g != f0: emit([x(f0, g)] if g in N else [-x(f0, g)])
        tally = collections.Counter(); status = "?"; t1 = time.time()
        while True:
            out.flush(); out.seek(0); out.write(HEAD % (nv[0], nc[0])); out.flush(); out.seek(0, 2)
            try: res_out = subprocess.run([CAD, "-q", cnf], capture_output=True, text=True, timeout=tl).stdout
            except subprocess.TimeoutExpired: res_out = ""
            res = "UNSAT" if "s UNSATISFIABLE" in res_out else "SAT" if "s SATISFIABLE" in res_out else "NO DECISION"
            if res != "SAT": status = "complete" if res == "UNSAT" else "NO DECISION"; break
            model = set(int(t) for line in res_out.split("\n") if line.startswith("v ") for t in line[2:].split() if 0 < int(t) <= len(free))
            A = A0.copy()
            for (a, b), v in X.items(): A[a, b] = A[b, a] = 1 if v in model else 0
            emit([(-v if v in model else v) for v in free])
            if not bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all()): tally["NOT STRONGLY REGULAR"] += 1; continue
            key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
            if hit is None:
                hit = "row_%03d_%d.edges" % (ci, len(known))
                with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                    for a in range(n):
                        for b in range(a + 1, n):
                            if A[a, b]: f.write("%d %d\n" % (a, b))
                known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(q) for q in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
            tally[hit] += 1
        if status != "complete": undecided.append(ci)
        for k, v in tally.items(): summary[k] += v
        print("case %d/%d (orbit of %d rows; %d of the 16 neighbours as in the input): %s, %d completions (%.0f s): %s" % (ci, len(reps) - 1, sz, len(N & old), status, sum(tally.values()), time.time() - t1, dict(tally)), flush=True)
    out.close()
    print("end: cases %d..%d; undecided cases: %s; completions by graph: %s" % (c0, min(c1, len(reps) - 1), undecided, dict(summary)), flush=True)
    try: os.remove(cnf)
    except OSError: pass
