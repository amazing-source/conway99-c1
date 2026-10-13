"""Lab session, 2026-10-13. STAGED CENSUS: going below the rung where the direct row method stops.

With only 54 vertices of the common third kept, the 162 outside vertices have more than 20 000 candidate rows each, but
the 27 freed vertices of the third have 8830. So the search is staged:
  stage 1: all families of rows for the 27 freed vertices of the block, pairwise compatible (rows are complete
           neighbourhoods inside the 189 free vertices), other than the family of the input; the row of the first
           freed vertex runs over one representative per orbit of the automorphisms of the input preserving the kept
           set and that vertex; the 27 translations preserving the kept set give the lists of the other freed vertices;
  stage 2: each family makes 81 vertices with complete, known neighbourhoods (the 54 kept + the 27 re-chosen);
           their internal consistency is checked, then boundary_census.completions lists every strongly regular
           completion on the 162 remaining vertices.
No symmetry is imposed on the result. Every graph obtained is checked, identified and its automorphism group computed.

python staged_census.py <out dir> <edge file> <max seconds for stage 1> <max families sent to stage 2> [references ...]
environment PYLIB.      Memory: about 240 000 rows of 189 bits."""
import sys, os, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import aut_tools as T, trade_bfs as B, boundary_census as BC, regular_subgroups as RS
n = 243

if __name__ == "__main__":
    outdir, path, tmax, maxfam = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
    A0 = T.load(path); known = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[5:]]; keys = {nm: B.invariant(A) for nm, A in known}
    H4 = list(itertools.product(range(3), repeat=4)); IDX4 = {g: i for i, g in enumerate(H4)}
    def shift(v, t): return 81 * (v // 81) + IDX4[tuple((a + b) % 3 for a, b in zip(H4[v % 81], t))]
    R0 = list(range(54)); Rs = set(R0); F = list(range(54, n)); NF = len(F); pos = {v: i for i, v in enumerate(F)}
    B1 = list(range(54, 81)); adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]
    t0 = time.time(); rows54 = BC.rows_of(adj, R0, Rs, F, 54, 30000); assert rows54 is not None
    mask = lambda S: sum(1 << pos[v] for v in S)
    cand = {}
    for t in H4:
        if t[0] != 0: continue                                          # the 27 translations preserving the kept set
        cand[pos[shift(54, t)]] = [mask(shift(v, t) for v in N) for N in rows54]
    orig = {pos[b]: mask(adj[b] - Rs) for b in B1}; assert all(orig[p] in cand[p] for p in cand) and len(cand) == 27
    Tm = {(p, q): 2 - len(adj[F[p]] & adj[F[q]] & Rs) for p in cand for q in cand if p != q}
    o, gens, base, sizes = T.aut_group(A0); ident = tuple(range(n)); G = RS.generate([tuple(g) for g in gens], ident)
    stab = [g for g in G if g[54] == 54 and all(g[v] in Rs for v in R0)]
    seen = set(); reps = []
    for N in sorted(rows54, key=sorted):
        fz = frozenset(N)
        if fz in seen: continue
        orb = {frozenset(g[v] for v in N) for g in stab}; seen |= orb; reps.append(mask(N))
    p0 = pos[54]; plist = sorted(cand)
    print("kept 54 vertices; %d candidate rows per freed vertex of the block (%.0f s); %d orbits for the first one under %d automorphisms" % (len(rows54), time.time() - t0, len(reps), len(stab)), flush=True)

    def propagate(lists, fixed, p, N):
        queue = [(p, N)]
        while queue:
            p, N = queue.pop(); fixed[p] = N; lists[p] = [N]
            for q in plist:
                if q == p: continue
                a = (N >> q) & 1; need = Tm[(p, q)] - a
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
    fams = []; stats = collections.Counter(); deadline = time.time() + tmax
    def search(lists, fixed):
        if stats["stop"]: return
        if time.time() > deadline: stats["stop"] = 1; return
        if len(fixed) == 27: fams.append(dict(fixed)); return
        stats["nodes"] += 1
        q = min((len(lists[v]), v) for v in plist if v not in fixed)[1]
        for M in lists[q]:
            l2 = dict(lists); f2 = dict(fixed)
            if propagate(l2, f2, q, M): search(l2, f2)
            if stats["stop"]: return
    t1 = time.time()
    for ri, N in enumerate(reps):
        if stats["stop"]: break
        lists = dict(cand); fixed = {}
        if propagate(lists, fixed, p0, N): search(lists, fixed)
        if ri % 200 == 0: print("   stage 1: %d / %d first rows done, %d families so far, %d nodes (%.0f s)" % (ri + 1, len(reps), len(fams), stats["nodes"], time.time() - t1), flush=True)
    new_fams = [f for f in fams if any(f[p] != orig[p] for p in f)]
    print("stage 1 %s: %d compatible families for the 27 freed vertices, of which %d differ from the input (%.0f s)" % ("NOT FINISHED" if stats["stop"] else "complete", len(fams), len(new_fams), time.time() - t1), flush=True)
    tally = collections.Counter(); R1 = list(range(81))
    for fi, fam in enumerate(new_fams[:maxfam]):
        A1 = A0.copy()
        for p, M in fam.items():
            b = F[p]
            for q in range(NF): A1[b, F[q]] = (M >> q) & 1; A1[F[q], b] = (M >> q) & 1
        blk = A1[:81, :]; cn = blk @ blk.T; good = all(cn[a, b] == (1 if A1[a, b] else 2) for a in range(81) for b in range(a + 1, 81)) and all(blk[a].sum() == 22 for a in range(81))
        changed = sum(1 for p in fam if fam[p] != orig[p])
        if not good: tally["family rejected (the 81 complete rows are inconsistent)"] += 1; continue
        sols, status, info = BC.completions(A1, R1, 600)
        print("   family %d (%d of the 27 rows changed): stage 2 %s, %d completions" % (fi, changed, status, len(sols)), flush=True)
        for A in sols:
            assert bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all())
            key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
            if hit is None:
                hit = "staged_%d.edges" % len(known)
                with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                    for a in range(n):
                        for b in range(a + 1, n):
                            if A[a, b]: f.write("%d %d\n" % (a, b))
                known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(x) for x in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
            tally[hit] += 1
    print("end: %s" % dict(tally), flush=True)
