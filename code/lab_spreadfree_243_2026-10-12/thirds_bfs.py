"""Lab session, 2026-10-12. CENSUS BY SWITCHING on the strongly regular graphs (243,22,1,2): exploration of the
classes connected by "third trades".

A THIRD of a graph is a set F of 81 vertices such that every vertex of F has 10 neighbours in F and every other vertex
has 6 (equivalently 1_F - 1/3 is an eigenvector for the eigenvalue 4). A THIRD TRADE keeps the whole graph except the
adjacency inside F and replaces it by another strongly regular completion (no symmetry imposed; complete list by
cadical, trade_bfs.completions).
For each graph of the queue: (1) automorphism group (aut_tools); (2) ALL its thirds (CryptoMiniSat, 243 variables, each
solution blocked together with its images under Aut, at most ORBCAP images; at most 40 classes per graph and 25 s
per solver call, the log says when the list is not complete); (3) for one third in each class, all the
completions; (4) every completion is checked (A^2 = 20I - A + 2J), keyed by invariants and compared by isomorphism
with the graphs already known; new graphs are written to the output directory and queued.

python thirds_bfs.py <out dir> <seconds per solver call> <max completions per third> <total seconds> <start edge files ...> [-- references ...]
environment PYLIB = directory of pycryptosat.       Memory: under 1 GB."""
import sys, os, itertools, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import pycryptosat
import aut_tools as T, trade_bfs as B
n = 243; ORBCAP = 30000


def thirds(A, gens, maxn=40, tlim=25):
    """representatives of the thirds of the graph up to Aut (orbit images blocked), with the orbit sizes"""
    adj = [np.nonzero(A[v])[0].tolist() for v in range(n)]
    nv = [n]; cl = []
    def new(): nv[0] += 1; return nv[0]
    for v in range(n):
        lits = [w + 1 for w in adj[v]]; prev = None                      # ge[j] : at least j of the neighbours, j = 1..11
        for l in lits:
            cur = [None] + [new() for _ in range(11)]
            for j in range(1, 12):
                pj = prev[j] if prev else None
                if pj is not None: cl.append([-pj, cur[j]])
                if j == 1: cl.append([-l, cur[j]])
                elif prev: cl.append([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cl.append(c + [l])
                if j > 1: cl.append(c + ([prev[j - 1]] if prev else []))
            prev = cur
        x = v + 1
        cl += [[-x, prev[10]], [-x, -prev[11]], [x, prev[6]], [x, -prev[7]]]
    s = pycryptosat.Solver(time_limit=tlim); s.add_clauses(cl); reps = []
    while len(reps) < maxn:
        sat, sol = s.solve()
        if sat is None: return reps, False                               # time limit of the solver: list not complete
        if not sat: return reps, True
        F = frozenset(v for v in range(n) if sol[v + 1]); orb = {F}; frontier = [F]
        while frontier and len(orb) < ORBCAP:
            nxt = []
            for S in frontier:
                for g in gens:
                    S2 = frozenset(g[v] for v in S)
                    if S2 not in orb: orb.add(S2); nxt.append(S2)
            frontier = nxt
        for S in orb: s.add_clause([-(v + 1) for v in S])
        reps.append((sorted(F), len(orb)))
    return reps, False


if __name__ == "__main__":
    outdir, tl, maxsol, total = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    args = sys.argv[5:]; cut = args.index("--") if "--" in args else len(args)
    t00 = time.time(); known = []; queue = collections.deque(); edges = collections.Counter()
    def register(name, A, q):
        key = B.invariant(A); o, gens, base, sizes = T.aut_group(A); known.append([name, A, key, o, gens])
        if q: queue.append(len(known) - 1)
        return key, o, [len(x) for x in T.vertex_orbits(n, gens)] if gens else [1] * n
    def lookup(A, key): return next((i for i, kn in enumerate(known) if kn[2] == key and T.find_iso(A, kn[1]) is not None), None)
    for p in args[:cut]: register(os.path.basename(p), T.load(p), True)
    for p in args[cut + 1:]: register(os.path.basename(p), T.load(p), False)
    print("start: %d graphs known, %d in the queue" % (len(known), len(queue)), flush=True)
    while queue and time.time() - t00 < total:
        gi = queue.popleft(); name, A0, _, o, gens = known[gi]
        t1 = time.time(); reps, complete = thirds(A0, gens)
        print("%s (|Aut| = %d): %d classes of thirds%s, class sizes %s (%.0f s)" % (name, o, len(reps), "" if complete else " (LIST NOT COMPLETE)", sorted(sz for _, sz in reps), time.time() - t1), flush=True)
        for F, sz in reps:
            if time.time() - t00 > total: break
            perm = F + [v for v in range(n) if v not in set(F)]; Ap = A0[np.ix_(perm, perm)]; tally = collections.Counter(); status = "?"; t1 = time.time()
            for A, st in B.completions(Ap, 0, outdir, tl, maxsol):
                if A is None: status = st; break
                if not bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all()): tally["NOT STRONGLY REGULAR"] += 1; continue
                key = B.invariant(A); hit = lookup(A, key)
                if hit is None:
                    nm = "t%03d.edges" % len(known)
                    with open(os.path.join(outdir, nm), "w", newline="\n") as f:
                        for a in range(n):
                            for b in range(a + 1, n):
                                if A[a, b]: f.write("%d %d\n" % (a, b))
                    key, o2, orbs = register(nm, A, True); hit = len(known) - 1
                    print("   NEW %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (nm, o2, orbs if len(orbs) < 30 else "%d orbits" % len(orbs), key[0], key[1]), flush=True)
                tally[known[hit][0]] += 1
                if hit != gi: edges[(min(gi, hit), max(gi, hit))] += 1
            print("   third of class size %d: %s (%.0f s): %s" % (sz, status, time.time() - t1, dict(tally)), flush=True)
    print("end after %.0f s: %d graphs known, %d still in the queue" % (time.time() - t00, len(known), len(queue)), flush=True)
    print("orders of the automorphism groups: %s" % sorted(collections.Counter(k[3] for k in known).items()), flush=True)
    print("trade links: %s" % sorted((known[a][0], known[b][0]) for (a, b) in edges), flush=True)
