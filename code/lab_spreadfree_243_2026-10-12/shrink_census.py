"""Lab session, 2026-10-13. LEAVING THE FAMILY: completions when the kept set is SMALLER than the common third.

The census of section 6h keeps the whole third (81 vertices) and finds seven graphs. Here only a part R of the third is
kept (with all its adjacencies); the other vertices of the third ("watch" vertices) are free like the 162 outside ones.
Same exact method (boundary_census: candidate rows per vertex, then pairwise compatible families), no symmetry imposed.
The search first assigns the rows of the watch vertices; the branch where they all keep their rows of the input is the
known census (third intact) and is skipped; every other completion is a strongly regular graph in which this copy of the
third is destroyed. Each one is checked, identified (invariants, isomorphism) and its automorphism group computed if new.

python shrink_census.py <out dir> <edge file> <number of kept vertices of the block 0..80> <max seconds> [references ...]
environment PYLIB.      Memory: a few hundred thousand rows of 180 bits, under 1 GB."""
import sys, os, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import aut_tools as T, trade_bfs as B, boundary_census as BC
n = 243

if __name__ == "__main__":
    outdir, path, kept, tmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    A0 = T.load(path); known = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[5:]]; keys = {nm: B.invariant(A) for nm, A in known}
    R = list(range(kept)); Rs = set(R); F = [v for v in range(n) if v not in Rs]; NF = len(F); pos = {v: i for i, v in enumerate(F)}
    watch = [pos[v] for v in range(kept, 81)]
    adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]; t0 = time.time(); cand = []; orig = []
    for f in F:
        rows = BC.rows_of(adj, R, Rs, F, f, 8000)
        if rows is None: raise SystemExit("more than 8000 candidate rows at vertex %d: kept set too small for this method" % f)
        cand.append([sum(1 << pos[g] for g in N) for N in rows]); orig.append(sum(1 << pos[g] for g in adj[f] - Rs))
        assert orig[-1] in cand[-1]
    print("kept %d vertices of the third, %d free; candidate rows: %d in all, watch vertices %s, others up to %d (%.0f s)" % (kept, NF, sum(map(len, cand)), sorted(set(len(cand[w]) for w in watch)), max(len(c) for c in cand), time.time() - t0), flush=True)
    Tm = [[2 - len(adj[F[p]] & adj[F[q]] & Rs) for q in range(NF)] for p in range(NF)]
    deadline = time.time() + tmax; stats = collections.Counter(); sols = []
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
        if time.time() > deadline: stats["stop"] = 1; return
        wfree = [w for w in watch if w not in fixed]
        if not wfree and all(fixed[w] == orig[w] for w in watch): stats["intact branches skipped"] += 1; return
        if len(fixed) == NF: sols.append(dict(fixed)); return
        stats["nodes"] += 1
        q = min((len(lists[v]), v) for v in wfree)[1] if wfree else min((len(lists[v]), v) for v in range(NF) if v not in fixed)[1]
        for M in lists[q]:
            l2 = list(lists); f2 = dict(fixed)
            if propagate(l2, f2, q, M): search(l2, f2)
            if stats["stop"]: return
    search(list(cand), {})
    tally = collections.Counter()
    for sol in sols:
        A = A0.copy()
        for p, M in sol.items():
            for q in range(NF): A[F[p], F[q]] = (M >> q) & 1
        assert (A == A.T).all() and bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all())
        key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
        if hit is None:
            hit = "shrink%d_%d.edges" % (kept, len(known))
            with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                for a in range(n):
                    for b in range(a + 1, n):
                        if A[a, b]: f.write("%d %d\n" % (a, b))
            known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
            print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(x) for x in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
        tally[hit] += 1
    print("search %s: %d completions with the third destroyed, %d search nodes, %d intact branches skipped (%.0f s): %s" % ("NOT FINISHED" if stats["stop"] else "complete", len(sols), stats["nodes"], stats["intact branches skipped"], time.time() - t0, dict(tally)), flush=True)
