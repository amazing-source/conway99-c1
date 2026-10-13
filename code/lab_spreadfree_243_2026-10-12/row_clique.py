"""Lab session, 2026-10-13. COMPLETE CENSUS OF THE COMPLETIONS OF A KEPT THIRD, without SAT solver on the big system.

Input: the fifth graph in tri-Cayley form (vertex 81 i + index of g, the 81 translations of Z_3^4 are automorphisms).
The block R = 0..80 is kept with all its adjacencies; the adjacency inside F = 81..242 is unknown, NO symmetry imposed.
Fact used: every condition of strong regularity that involves the unknown part is either
  (a) a condition on ONE row: the neighbourhood N(f) inside F of a vertex f against the 81 vertices of R (and the degree), or
  (b) a condition on TWO rows: g in N(f) iff f in N(g), and |N(f) & N(g)| = 2 - #(common neighbours in R) - [f ~ g].
Step 1: the complete list of the rows allowed by (a) for the vertex 81 and for the vertex 162 (CryptoMiniSat, 161
variables); by translation this gives the candidate rows of every vertex of F. Step 2: a completion is exactly a choice
of one candidate row per vertex, pairwise compatible for (b): depth-first search with forward checking. The row of the
vertex 81 runs over one representative of each orbit under the automorphisms of the input preserving R and fixing 81.
Every completion found is rebuilt, checked (A^2 = 20I - A + 2J), keyed by invariants and compared by isomorphism with
the known graphs; new graphs are written out with their automorphism group.
The search is exhaustive: when it ends, the list of completions is complete (up to the automorphisms used).

python row_clique.py <out dir> <edge file> <first case> <last case> <max seconds> [references ...]
environment PYLIB = directory of pycryptosat.        Memory: small (about 150 000 rows of 162 bits)."""
import sys, os, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import aut_tools as T, trade_bfs as B, regular_subgroups as RS, row_census as RC
n = 243; NF = 162

if __name__ == "__main__":
    outdir, path, c0, c1, tmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    A0 = T.load(path); known = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[6:]]; keys = {nm: B.invariant(A) for nm, A in known}
    R = list(range(81)); Rs = set(R); F = list(range(81, n)); adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]
    H4 = list(itertools.product(range(3), repeat=4)); IDX4 = {g: i for i, g in enumerate(H4)}
    def shift(v, t): return 81 * (v // 81) + IDX4[tuple((a + b) % 3 for a, b in zip(H4[v % 81], t))]
    for t in H4[1:5]: assert all(A0[shift(a, t), shift(b, t)] == A0[a, b] for a in range(0, n, 5) for b in range(n)), "translations are not automorphisms"
    t0 = time.time(); base_rows = {81: RC.candidate_rows(adj, R, F, 81), 162: RC.candidate_rows(adj, R, F, 162)}
    mask = lambda S: sum(1 << (v - 81) for v in S)
    cand = [None] * NF
    for b0 in (81, 162):
        for t in H4:
            f = shift(b0, t); cand[f - 81] = [mask(shift(v, t) for v in N) for N in base_rows[b0]]
    Tm = [[2 - len(adj[F[p]] & adj[F[q]] & Rs) for q in range(NF)] for p in range(NF)]
    o, gens, base, sizes = T.aut_group(A0); ident = tuple(range(n)); G = RS.generate([tuple(g) for g in gens], ident)
    stab = [g for g in G if g[81] == 81 and all(g[v] in Rs for v in R)]
    seen = set(); reps = []
    for N in sorted(base_rows[81], key=sorted):
        if N in seen: continue
        orb = {frozenset(g[v] for v in N) for g in stab}; seen |= orb; reps.append((mask(N), len(orb)))
    print("candidate rows: %d for a vertex of block 1, %d for a vertex of block 2 (%.0f s); %d cases for the row of the vertex 81" % (len(base_rows[81]), len(base_rows[162]), time.time() - t0, len(reps)), flush=True)

    def propagate(lists, fixed, p, N):
        """fix the row N at p: filter the lists of the other vertices; cascades on singletons. Returns False on a wipe-out."""
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

    def search(lists, fixed, sols, stats, deadline):
        if time.time() > deadline: stats["timeout"] = 1; return
        if len(fixed) == NF: sols.append(dict(fixed)); return
        stats["nodes"] += 1
        q = min((len(lists[v]), v) for v in range(NF) if v not in fixed)[1]
        for M in lists[q]:
            l2 = list(lists); f2 = dict(fixed)
            if propagate(l2, f2, q, M): search(l2, f2, sols, stats, deadline)
            if stats.get("timeout"): return

    total = collections.Counter(); t00 = time.time(); undecided = []
    for ci, (N, sz) in enumerate(reps):
        if ci < c0 or ci > c1: continue
        if time.time() - t00 > tmax: print("time budget reached before case %d" % ci, flush=True); undecided.append(ci); continue
        t1 = time.time(); lists = list(cand); fixed = {}; sols = []; stats = collections.Counter()
        if propagate(lists, fixed, 0, N): search(lists, fixed, sols, stats, t1 + 900)
        tally = collections.Counter()
        for sol in sols:
            A = A0.copy()
            for p, M in sol.items():
                for q in range(NF): A[81 + p, 81 + q] = (M >> q) & 1
            assert (A == A.T).all() and bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all()), "a compatible family of rows is not strongly regular"
            key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
            if hit is None:
                hit = "clique_%03d_%d.edges" % (ci, len(known))
                with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                    for a in range(n):
                        for b in range(a + 1, n):
                            if A[a, b]: f.write("%d %d\n" % (a, b))
                known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(x) for x in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
            tally[hit] += 1; total[hit] += 1
        if stats.get("timeout"): undecided.append(ci)
        print("case %d/%d (orbit of %d rows): %s, %d completions, %d search nodes (%.1f s): %s" % (ci, len(reps) - 1, sz, "NOT FINISHED (15 min)" if stats.get("timeout") else "complete", len(sols), stats["nodes"], time.time() - t1, dict(tally)), flush=True)
    print("end after %.0f s: cases %d..%d; unfinished cases %s; completions by graph: %s" % (time.time() - t00, c0, min(c1, len(reps) - 1), undecided, dict(total)), flush=True)
