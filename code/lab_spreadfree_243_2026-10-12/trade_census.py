"""Lab session, 2026-10-12. TRADES in a strongly regular graph srg(243,22,1,2): free a region and re-complete.

Classical switching does not exist for these parameters (mu = 2 is too small: counting argument in NOTE_SPREADFREE.md),
so "switching" is taken in the widest sense. Given a graph G = srg(243,22,1,2) and a set F of vertices, every adjacency
with an endpoint in F is forgotten; question: is there ANOTHER srg(243,22,1,2) G' on the same vertex set that agrees with
G on all pairs of vertices outside F?  UNSAT = the region F is rigid; SAT = a trade, G' is written out and analysed
(strongly regular? number of 3x3 grids through each vertex, regular spreads).

Encoding (cadical): one variable per pair {f, v} with f in F;
  degrees: each f has 22 neighbours; each v outside F keeps its number of neighbours in F;
  pairs outside F: (common neighbours outside F, fixed) + #(f adjacent to both) = 1 or 2;
  pairs {f, v} and {f, f'}: #(common neighbours) + [adjacent] = 2;
  G' differs from G on at least one pair.
Cardinalities by sequential counters.

python trade_census.py <edge file> <tmp dir> <seconds> <region> [seed] [inner]
  default mode "newattach": some vertex of F gets a set of outside neighbours that no vertex of F had (this excludes the
  isomorphic copies obtained by relabelling F); mode "inner": the outside attachments are kept, only the graph inside F
  may change.
  region:  ball:<v>            closed neighbourhood of v (23 vertices)
           ball2:<v>:<w>       union of the closed neighbourhoods of v and w
           line:<v>            the line through v and its first neighbour (3 vertices)
           grid:<v>            a 3x3 grid through v (9 vertices), if any
           fibres:<k>:<v>      k fibres of the first regular spread: the one of v and those of its first neighbours' fibres
           rand:<k>            k random vertices (seed)
           list:a,b,c,...      explicit list
Memory: cadical on up to a few million clauses, under 2 GB for regions of at most 30 vertices."""
import sys, os, subprocess, time, itertools, random, collections


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, adj


def is_srg(n, adj, k=22, lam=1, mu=2):
    if any(len(a) != k for a in adj): return False
    for x in range(n):
        for y in range(x + 1, n):
            if len(adj[x] & adj[y]) != (lam if y in adj[x] else mu): return False
    return True


def grids_profile(n, adj):
    line = {}
    for x in range(n):
        for y in adj[x]:
            if x < y: z = next(iter(adj[x] & adj[y])); line[(x, y)] = z; line[(y, x)] = z
    cnt = []
    for x in range(n):
        lines = sorted({tuple(sorted((y, line[(x, y)]))) for y in adj[x]}); c = 0
        for (a, a2), (b, b2) in itertools.combinations(lines, 2):
            sec = lambda u, w: next(v for v in adj[u] & adj[w] if v != x)
            cab, cab2, ca2b, ca2b2 = sec(a, b), sec(a, b2), sec(a2, b), sec(a2, b2)
            if cab2 in adj[cab] and ca2b in adj[cab] and ca2b2 in adj[cab2] and ca2b2 in adj[ca2b]: c += 1
        cnt.append(c)
    return sorted(collections.Counter(cnt).items())


def find_grid(adj, v):
    lines = sorted({tuple(sorted((y, next(iter(adj[v] & adj[y]))))) for y in adj[v]})
    for (a, a2), (b, b2) in itertools.combinations(lines, 2):
        sec = lambda u, w: next(t for t in adj[u] & adj[w] if t != v)
        c = [sec(a, b), sec(a, b2), sec(a2, b), sec(a2, b2)]
        if c[1] in adj[c[0]] and c[2] in adj[c[0]] and c[3] in adj[c[1]] and c[3] in adj[c[2]]: return [v, a, a2, b, b2] + c
    return None


def region(spec, n, adj, seed):
    kind, _, arg = spec.partition(":")
    if kind == "ball": v = int(arg); return sorted({v} | adj[v])
    if kind == "ball2": v, w = map(int, arg.split(":")); return sorted({v, w} | adj[v] | adj[w])
    if kind == "line": v = int(arg); y = min(adj[v]); return sorted({v, y, next(iter(adj[v] & adj[y]))})
    if kind == "grid": g = find_grid(adj, int(arg)); assert g, "no grid through this vertex"; return sorted(g)
    if kind == "rand": random.seed(seed); return sorted(random.sample(range(n), int(arg)))
    if kind == "list": return sorted(int(t) for t in arg.split(","))
    if kind == "fibres":
        k, v = map(int, arg.split(":"))
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "s3_question_2026-10-12"))
        import verify_drg
        sp = verify_drg.spreads(n, adj)[0]; fib = {x: t for t in sp for x in t}
        out = [fib[v]]; q = [fib[v]]
        while len(out) < k:
            t = q.pop(0)
            for x in t:
                for y in sorted(adj[x]):
                    if fib[y] not in out and len(out) < k: out.append(fib[y]); q.append(fib[y])
        return sorted(x for t in out for x in t)
    raise SystemExit("unknown region")


def build(n, adj, F, mode="newattach"):
    Fs = set(F); R = [v for v in range(n) if v not in Fs]
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    X = {}
    def x(f, v):
        key = (f, v) if (v not in Fs or f < v) else (v, f)
        if key not in X: X[key] = new()
        return X[key]
    for f in F:
        for v in range(n):
            if v != f: x(f, v)
    def exactly(lits, k):
        """exactly k of lits (sequential counter up to k+1)"""
        m = len(lits)
        if k < 0 or k > m: cl.append([]); return
        prev = None
        for i, l in enumerate(lits):
            cur = [None] + [new() for _ in range(k + 1)]             # cur[j]: at least j among the first i+1
            for j in range(1, k + 2):
                pj = prev[j] if prev else None; pj1 = (prev[j - 1] if j > 1 else "T") if prev else ("T" if j == 1 else None)
                if pj is not None: cl.append([-pj, cur[j]])
                if pj1 == "T": cl.append([-l, cur[j]])
                elif pj1 is not None: cl.append([-l, -pj1, cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cl.append(c + [l])
                if pj1 != "T": cl.append(c + ([pj1] if pj1 is not None else []))
            prev = cur
        if k >= 1: cl.append([prev[k]])
        cl.append([-prev[k + 1]])
    def AND(a, b):
        t = new(); cl.extend([[-t, a], [-t, b], [t, -a, -b]]); return t
    # degrees
    for f in F: exactly([x(f, v) for v in range(n) if v != f], 22)
    for v in R: exactly([x(f, v) for f in F], len(adj[v] & Fs))
    # pairs outside F
    for i, u in enumerate(R):
        for w in R[i + 1:]:
            tgt = len(adj[u] & adj[w] & Fs)                          # what F must contribute (as in G)
            if tgt == 0:
                for f in F: cl.append([-x(f, u), -x(f, w)])
            else: exactly([AND(x(f, u), x(f, w)) for f in F], tgt)
    # pairs {f, v}, v outside F: common neighbours + [adjacent] = 2
    for f in F:
        for v in R:
            lits = [x(f, w) for w in adj[v] if w not in Fs] + [AND(x(f, g), x(g, v)) for g in F if g != f] + [x(f, v)]
            exactly(lits, 2)
    # pairs inside F
    for f, g in itertools.combinations(F, 2):
        lits = [AND(x(f, w), x(g, w)) for w in range(n) if w not in (f, g)] + [x(f, g)]
        exactly(lits, 2)
    # different from G. Relabelling the vertices of F gives isomorphic copies of G that agree with G outside F; they are
    # excluded: mode "newattach" asks for a vertex of F whose set of neighbours outside F is none of the old ones;
    # mode "inner" keeps all the attachments to the outside and asks for a different graph inside F.
    if mode == "newattach":
        es = []
        for g in F:
            e = new(); es.append(e)
            for f in F: cl.append([-e] + [(-x(g, v)) if v in adj[f] else x(g, v) for v in R])
        cl.append(es)
    else:
        for f in F:
            for v in R: cl.append([x(f, v)] if v in adj[f] else [-x(f, v)])
        cl.append([(-X[k]) if (k[1] in adj[k[0]]) else X[k] for k in X if k[1] in Fs])
    return nv[0], cl, X


if __name__ == "__main__":
    path, tmp, tl, spec = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    seed = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5].isdigit() else 1
    mode = "inner" if "inner" in sys.argv[5:] else "newattach"
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    n, adj = load(path); F = region(spec, n, adj, seed)
    t0 = time.time(); nv, cl, X = build(n, adj, F, mode)
    cnf = os.path.join(tmp, "trade_%d.cnf" % os.getpid())
    with open(cnf, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    name = os.path.basename(path)
    print("%s, region %s (%d vertices), mode %s: %d free pairs, %d variables, %d clauses (built in %.0f s)" % (name, spec, len(F), mode, len(X), nv, len(cl), time.time() - t0), flush=True)
    t1 = time.time()
    try: out = subprocess.run([CAD, "-q", cnf], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT (rigid region: no other completion)" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("  result: %s (%.1f s)" % (res, time.time() - t1), flush=True)
    if res == "SAT":
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        adj2 = [set(a) for a in adj]
        for (f, v), var in X.items():
            if var in model: adj2[f].add(v); adj2[v].add(f)
            else: adj2[f].discard(v); adj2[v].discard(f)
        changed = sum(1 for (f, v) in X if (v in adj[f]) != (v in adj2[f]))
        ok = is_srg(n, adj2)
        print("  TRADE: %d pairs changed; the new graph is srg(243,22,1,2): %s" % (changed, ok), flush=True)
        if ok:
            print("  grids through a vertex, old graph: %s" % grids_profile(n, adj))
            print("  grids through a vertex, new graph: %s" % grids_profile(n, adj2))
            outp = os.path.join(tmp, "trade_%s_%s.edges" % (name.split(".")[0], spec.replace(":", "_").replace(",", "-")[:60]))
            with open(outp, "w", newline="\n") as f:
                for a in range(n):
                    for b in sorted(adj2[a]):
                        if a < b: f.write("%d %d\n" % (a, b))
            print("  new graph written to %s" % outp)
    try: os.remove(cnf)
    except OSError: pass
