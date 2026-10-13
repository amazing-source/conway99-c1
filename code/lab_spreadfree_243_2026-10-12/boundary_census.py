"""Lab session, 2026-10-13. BOUNDARY CENSUS: all strongly regular completions of a kept set, by compatible rows.

General form of row_clique.py (no translation structure needed). Given a graph srg(243,22,1,2) and a set R of kept
vertices (all adjacencies inside R and from R to the rest F are kept), list ALL graphs srg(243,22,1,2) that agree with
it on these pairs. Every unknown condition is on one row (the neighbourhood inside F of a vertex of F, against R) or on
two rows (symmetry and number of common neighbours), so:
  1. for each vertex f of F, the complete list of its candidate rows (CryptoMiniSat on |F| - 1 variables); the census is
     abandoned if a vertex has more than ROWCAP candidates;
  2. a completion = one candidate row per vertex, pairwise compatible: depth-first search with forward checking,
     exhaustive (a time limit can interrupt it; the output says so).
Functions: completions(A0, R, seconds, maxsol) -> (list of adjacency matrices, status, info).
Driver: python boundary_census.py <out dir> <seconds per boundary> <mode> <graph> [references ...]
   mode thirds:<k>  : R = each of the first k thirds found in the graph (classes under Aut), F = the 162 other vertices
   mode line:<k>    : R = a line and its 60 neighbours, for k lines taken in different classes of "number of parallels"
   mode list:a-b,.. : R = the given vertices
environment PYLIB = directory of pycryptosat; SKIP = class sizes of thirds to skip (comma separated).      Memory: small."""
import sys, os, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import pycryptosat
import aut_tools as T, trade_bfs as B, row_census as RC
n = 243; ROWCAP = 6000


def rows_of(adj, R, Rs, F, f0, cap):
    var = {g: i + 1 for i, g in enumerate(v for v in F if v != f0)}; nv = [len(var)]; cls = []
    def new(): nv[0] += 1; return nv[0]
    for r in R:
        lits = [var[g] for g in sorted(adj[r] - Rs) if g != f0]
        if lits or True: RC.counter(cls.append, new, lits, (1 if f0 in adj[r] else 2) - len(adj[r] & adj[f0] & Rs))
    RC.counter(cls.append, new, list(var.values()), 22 - len(adj[f0] & Rs))
    for g, h in itertools.combinations(sorted(var), 2):
        if len(adj[g] & adj[h] & Rs) == 2: cls.append([-var[g], -var[h]])
    s = pycryptosat.Solver(); s.add_clauses(cls); rows = []
    while len(rows) <= cap:
        sat, sol = s.solve()
        if not sat: return rows
        N = [g for g in var if sol[var[g]]]; rows.append(N); s.add_clause([-var[g] for g in N])
    return None


def completions(A0, R, seconds, maxsol=5000):
    Rs = set(R); F = [v for v in range(n) if v not in Rs]; NF = len(F); pos = {v: i for i, v in enumerate(F)}
    adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]; t0 = time.time(); cand = []
    for f in F:
        rows = rows_of(adj, R, Rs, F, f, ROWCAP)
        if rows is None: return [], "too many candidate rows (more than %d at vertex %d)" % (ROWCAP, f), {}
        cand.append([sum(1 << pos[g] for g in N) for N in rows])
        if not rows: return [], "complete", {"rows": 0}
    info = {"rows": sum(len(c) for c in cand), "rows_max": max(len(c) for c in cand), "rows_seconds": time.time() - t0}
    Tm = [[2 - len(adj[F[p]] & adj[F[q]] & Rs) for q in range(NF)] for p in range(NF)]
    deadline = time.time() + seconds; sols = []; stats = collections.Counter()
    def propagate(lists, fixed, p, N):
        queue = [(p, N)]
        while queue:
            p, N = queue.pop(); fixed[p] = N; lists[p] = [N]
            for q in range(NF):
                if q == p: continue
                a = (N >> q) & 1; need = Tm[p][q] - a
                if q in fixed:
                    M = fixed[q]
                    if ((M >> p) & 1) != a or (N & M).bit_count() != need: return False
                    continue
                L = [M for M in lists[q] if ((M >> p) & 1) == a and (N & M).bit_count() == need]
                if not L: return False
                if len(L) < len(lists[q]):
                    lists[q] = L
                    if len(L) == 1 and all(qq != q for qq, _ in queue): queue.append((q, L[0]))
        return True
    def search(lists, fixed):
        if stats["stop"]: return
        if time.time() > deadline or len(sols) >= maxsol: stats["stop"] = 1; return
        if len(fixed) == NF: sols.append(dict(fixed)); return
        stats["nodes"] += 1
        q = min((len(lists[v]), v) for v in range(NF) if v not in fixed)[1]
        for M in lists[q]:
            l2 = list(lists); f2 = dict(fixed)
            if propagate(l2, f2, q, M): search(l2, f2)
            if stats["stop"]: return
    # singletons first (vertices with one candidate), then the search
    lists = list(cand); fixed = {}; ok = True
    for p in range(NF):
        if len(lists[p]) == 1 and p not in fixed:
            if not propagate(lists, fixed, p, lists[p][0]): ok = False; break
    if ok: search(lists, fixed)
    out = []
    for sol in sols:
        A = A0.copy()
        for p, M in sol.items():
            for q in range(NF): A[F[p], F[q]] = (M >> q) & 1
        out.append(A)
    info["nodes"] = stats["nodes"]; info["search_seconds"] = time.time() - t0 - info["rows_seconds"]
    return out, ("NOT FINISHED (limit)" if stats["stop"] else "complete"), info


if __name__ == "__main__":
    outdir, seconds, mode, path = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
    A0 = T.load(path); known = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[5:]]; keys = {nm: B.invariant(A) for nm, A in known}
    adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]; jobs = []
    if mode.startswith("thirds:"):
        import thirds_bfs as TB
        o, gens, base, sizes = T.aut_group(A0); reps, complete = TB.thirds(A0, gens, maxn=int(mode[7:]))
        skip = [int(t) for t in os.environ.get("SKIP", "").split(",") if t]            # class sizes already treated elsewhere
        jobs = [("third of class size %d" % sz, Fset) for Fset, sz in reps if sz not in skip]
    elif mode.startswith("line:"):
        lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y}); byf = {}
        for L in lines:
            p, u, us = L; cnt = 0
            for w in adj[p]:
                if w in L: continue
                w1 = [t for t in adj[w] & adj[u] if t != p][0]; w2 = [t for t in adj[w1] & adj[us] if t != u][0]
                if w2 in adj[w]: cnt += 1
            byf.setdefault(cnt, L)
        for cnt, L in sorted(byf.items())[:int(mode[5:])]:
            jobs.append(("line %s with %d parallel lines and its 60 neighbours" % (L, cnt), sorted(set(L) | set().union(*[adj[x] for x in L]))))
    else:
        jobs = [("given set", [v for part in mode[5:].split(",") for v in range(int(part.split("-")[0]), int(part.split("-")[1]) + 1)])]
    print("%s: %d boundaries to treat" % (os.path.basename(path), len(jobs)), flush=True)
    for label, R in jobs:
        t1 = time.time(); sols, status, info = completions(A0, R, seconds); tally = collections.Counter()
        for A in sols:
            assert bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all())
            key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
            if hit is None:
                hit = "bc_%s_%d.edges" % (os.path.basename(path).split(".")[0][-10:], len(known))
                with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                    for a in range(n):
                        for b in range(a + 1, n):
                            if A[a, b]: f.write("%d %d\n" % (a, b))
                known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(x) for x in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
            tally[hit] += 1
        print("kept: %s (%d vertices): %s; %d completions; rows %s (largest list %s), search nodes %s (%.0f s): %s" % (label, len(R), status, len(sols), info.get("rows"), info.get("rows_max"), info.get("nodes"), time.time() - t1, dict(tally)), flush=True)
