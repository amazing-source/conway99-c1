"""Lab session, 2026-10-12. Scan for TRADEABLE THIRDS given by the automorphism group: for each graph, every union F of
orbits of Aut with 81 vertices such that each vertex of F has 10 neighbours in F and each other vertex 6 (the type of
the blocks of a tri-Cayley graph of type I). For each such F: all completions of the adjacency inside F, nothing else
changed, no symmetry imposed (trade_bfs.completions after relabelling); completions are compared with the references and
new graphs are written out.
python third_scan.py <out dir> <seconds per call> <max solutions> <graphs to scan ...> -- <other references ...>"""
import sys, os, itertools, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T, trade_bfs as B
n = 243
if __name__ == "__main__":
    outdir, tl, maxsol = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); args = sys.argv[4:]; cut = args.index("--")
    known = [(os.path.basename(p), T.load(p)) for p in args[:cut] + args[cut + 1:]]
    keys = {nm: B.invariant(A) for nm, A in known}
    for p in args[:cut]:
        A0 = T.load(p); o, gens, base, sizes = T.aut_group(A0); orbs = T.vertex_orbits(n, gens)
        cands = []
        for k in range(1, len(orbs) + 1):
            for comb in itertools.combinations(range(len(orbs)), k):
                if sum(len(orbs[i]) for i in comb) == 81:
                    F = sorted(v for i in comb for v in orbs[i]); ind = np.zeros(n, dtype=np.int64); ind[F] = 1; d = A0 @ ind
                    if all(d[v] == (10 if ind[v] else 6) for v in range(n)): cands.append((comb, F))
        print("%s: |Aut| = %d, orbits %s, %d unions of orbits are thirds of type (10 inside, 6 from outside)" % (os.path.basename(p), o, [len(q) for q in orbs], len(cands)), flush=True)
        for comb, F in cands:
            perm = F + [v for v in range(n) if v not in set(F)]; Ap = A0[np.ix_(perm, perm)]
            tally = collections.Counter(); status = "?"; t1 = time.time()
            for A, st in B.completions(Ap, 0, outdir, tl, maxsol):
                if A is None: status = st; break
                assert (A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all()
                key = B.invariant(A); hit = next((nm for nm, R in known if keys[nm] == key and T.find_iso(A, R) is not None), None)
                if hit is None:
                    hit = "scan_%s_%d.edges" % (os.path.basename(p).split(".")[0][-12:], len(known))
                    with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                        for a in range(n):
                            for b in range(a + 1, n):
                                if A[a, b]: f.write("%d %d\n" % (a, b))
                    known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                    print("   NEW %s: |Aut| = %d, orbits %s, parallels %s, grids %s" % (hit, o2, [len(q) for q in T.vertex_orbits(n, g2)], key[0], key[1]), flush=True)
                tally[hit] += 1
            print("   orbits %s (sizes %s): %s (%.0f s): %s" % (comb, [len(orbs[i]) for i in comb], status, time.time() - t1, dict(tally)), flush=True)
