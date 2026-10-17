"""Lab session, 2026-10-12. EXPLORATION BY 81-VERTEX TRADES, no symmetry imposed.

A graph srg(243,22,1,2) labelled so that the blocks B0 = 0..80, B1 = 81..161, B2 = 162..242 are the three orbits of the
original tri-Cayley structure. For a graph G and a block B: keep everything except the adjacency INSIDE B (so the 162
other vertices and all their adjacencies, including those to B, are fixed) and list the strongly regular completions
(cadical, each solution blocked). Every completion is checked (A^2 = 20I - A + 2J), given an invariant key (lines
parallel to a line, grids per vertex) and compared by a direct isomorphism test with the known graphs having the same
key. New graphs are written to the output directory, their automorphism group is computed, and they are put in the
queue: breadth-first exploration of the classes reachable by such trades.

python trade_bfs.py <out dir> <seconds per solver call> <max solutions per (graph, block)> <total seconds> <start edge files ...> [-- reference edge files ...]
Memory: about 3 million clauses per call, under 1 GB."""
import sys, os, subprocess, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
n = 243


def invariant(A):
    adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    third = {(x, y): next(iter(adj[x] & adj[y])) for x in range(n) for y in adj[x]}
    par = collections.Counter(); grids = collections.Counter()
    for x in range(n):
        lines = sorted({tuple(sorted((y, third[(x, y)]))) for y in adj[x]}); g = 0
        for (a, a2), (b, b2) in itertools.combinations(lines, 2):
            sec = lambda u, w: next(v for v in adj[u] & adj[w] if v != x)
            c = [sec(a, b), sec(a, b2), sec(a2, b), sec(a2, b2)]
            if c[1] in adj[c[0]] and c[2] in adj[c[0]] and c[3] in adj[c[1]] and c[3] in adj[c[2]]: g += 1
        grids[g] += 1
        for (y, z) in lines:
            if x < y:                                                   # each line once, from its smallest point
                cnt = 0
                for w in adj[x]:
                    if w in (y, z): continue
                    w1 = [t for t in adj[w] & adj[y] if t != x][0]; w2 = [t for t in adj[w1] & adj[z] if t != y][0]
                    if w2 in adj[w]: cnt += 1
                par[cnt] += 1
    return tuple(sorted(par.items())), tuple(sorted(grids.items()))


def completions(A0, block, tmp, tl, maxsol):
    """yields (A, status) for the completions of the adjacency inside the block; last item (None, status)"""
    F = list(range(81 * block, 81 * block + 81)); Fs = set(F); R = [v for v in range(n) if v not in Fs]
    adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]; nbF = {v: sorted(adj[v] & Fs) for v in range(n)}; nbR = {v: adj[v] - Fs for v in range(n)}
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    X = {}
    for i, a in enumerate(F):
        for b in F[i + 1:]: X[(a, b)] = new()
    x = lambda a, b: X[(a, b)] if a < b else X[(b, a)]
    cache = {}
    def AND(a, b):
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            t = new(); cache[k] = t; cl.extend([[-t, a], [-t, b], [t, -a, -b]])
        return cache[k]
    def exactly(lits, k):
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
    for r in R:
        for f in F: exactly([x(g, f) for g in nbF[r] if g != f], (1 if f in adj[r] else 2) - len(nbR[r] & nbR[f]))
    for f in F: exactly([x(f, g) for g in F if g != f], 22 - len(nbR[f]))
    for i, f in enumerate(F):
        for g in F[i + 1:]:
            tgt = 2 - len(nbR[f] & nbR[g])
            if tgt == 0:
                cl.append([-x(f, g)])
                for h in F:
                    if h != f and h != g: cl.append([-x(f, h), -x(g, h)])
            else: exactly([AND(x(f, h), x(g, h)) for h in F if h != f and h != g] + [x(f, g)], tgt)
    free = sorted(X.values()); block_cl = []; cnf = os.path.join(tmp, "bfs_%d.cnf" % os.getpid())
    for it in range(maxsol):
        with open(cnf, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv[0], len(cl) + len(block_cl)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
            for c in block_cl: f.write(" ".join(map(str, c)) + " 0\n")
        try: out = subprocess.run([CAD, "-q", cnf], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
        if res != "SAT":
            yield None, "complete" if res == "UNSAT" else "NO DECISION"; return
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if 0 < int(t) <= len(free))
        A = A0.copy()
        for (a, b), v in X.items(): A[a, b] = A[b, a] = 1 if v in model else 0
        block_cl.append([(-v if v in model else v) for v in free])
        yield A, "solution"
    yield None, "limit of %d solutions" % maxsol


if __name__ == "__main__":
    outdir, tl, maxsol, total = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    args = sys.argv[5:]; cut = args.index("--") if "--" in args else len(args)
    t00 = time.time(); known = []                                          # (name, A, key, |Aut|)
    def register(name, A, queue):
        key = invariant(A); o, gens, base, sizes = T.aut_group(A)
        known.append((name, A, key, o));
        if queue is not None: queue.append(len(known) - 1)
        return key, o, [len(q) for q in T.vertex_orbits(n, gens)]
    queue = collections.deque()
    for p in args[cut + 1:]: register(os.path.basename(p), T.load(p), None)
    for p in args[:cut]:
        A = T.load(p)
        if not any(T.find_iso(A, B) is not None for (_, B, _, _) in known): register(os.path.basename(p), A, queue)
        else: queue.append(next(i for i, (_, B, _, _) in enumerate(known) if T.find_iso(A, B) is not None))
    print("start: %d graphs known, %d in the queue" % (len(known), len(queue)), flush=True)
    while queue and time.time() - t00 < total:
        gi = queue.popleft(); name, A0 = known[gi][0], known[gi][1]
        for block in range(3):
            if time.time() - t00 > total: break
            t1 = time.time(); tally = collections.Counter(); status = "?"
            for A, st in completions(A0, block, outdir, tl, maxsol):
                if A is None: status = st; break
                if not bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all()): tally["NOT STRONGLY REGULAR"] += 1; continue
                key = invariant(A)
                hit = next((nm for (nm, B, k, _) in known if k == key and T.find_iso(A, B) is not None), None)
                if hit is None:
                    nm = "g%03d.edges" % len(known)
                    with open(os.path.join(outdir, nm), "w", newline="\n") as f:
                        for a in range(n):
                            for b in range(a + 1, n):
                                if A[a, b]: f.write("%d %d\n" % (a, b))
                    key, o, orbs = register(nm, A, queue); hit = nm
                    even = all(c % 2 == 0 for c, _ in key[0]); flat = dict(key[0]).get(20, 0)
                    print("   NEW %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s, flat lines %d, all parallel counts even: %s" % (nm, o, orbs, key[0], key[1], flat, even), flush=True)
                tally[hit] += 1
            print("%s, block %d: %s (%.0f s): %s" % (name, block, status, time.time() - t1, dict(tally)), flush=True)
    print("end after %.0f s: %d graphs known, %d still in the queue" % (time.time() - t00, len(known), len(queue)), flush=True)
    print("orders of the automorphism groups: %s" % sorted(collections.Counter(o for (_, _, _, o) in known).items()), flush=True)
