"""Lab session, 2026-10-13. Stage 2 of the staged census: each family found by stage1_search.c (new rows for the freed
vertices of the block) gives 81 vertices with complete neighbourhoods; their internal consistency is checked, then every
strongly regular completion on the 162 remaining vertices is listed (boundary_census.completions), checked
(A^2 = 20I - A + 2J), identified (invariants, isomorphism) and, if new, written out with its automorphism group.
Families are read from the file as they are (lines "i_0 ... i_26 NEW"); families already treated are skipped, so the
script can be run again while stage 1 is still writing.

python stage2_complete.py <out dir> <edge file> <kept> <file.bin> <families file> <first family> <last family> [references ...]
environment PYLIB.      Memory: small."""
import sys, os, struct, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import aut_tools as T, trade_bfs as B, boundary_census as BC
n = 243

if __name__ == "__main__":
    outdir, path, kept, binf, famf, f0, f1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
    A0 = T.load(path); known = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[8:]]; keys = {nm: B.invariant(A) for nm, A in known}
    data = open(binf, "rb").read(); off = 0
    NV, NF, W, NREP, _ = struct.unpack_from("<5i", data, off); off += 20
    pbit = []; cnt = []
    for v in range(NV): a, b = struct.unpack_from("<2i", data, off); off += 8; pbit.append(a); cnt.append(b)
    off += 4 * NV * NV + 4 * NREP
    orig = list(struct.unpack_from("<%di" % NV, data, off)); off += 4 * NV
    start = []
    for v in range(NV): start.append(off); off += 8 * W * cnt[v]
    def row(v, i):
        words = struct.unpack_from("<%dQ" % W, data, start[v] + 8 * W * i); m = 0
        for k, w in enumerate(words): m |= w << (64 * k)
        return m
    F = list(range(kept, n)); assert NF == len(F) and NV == 81 - kept and all(pbit[v] == v for v in range(NV))
    fams = [list(map(int, l.split()[:NV])) for l in open(famf) if l.strip().endswith("NEW")]
    print("%d new families in the file; treating %d..%d" % (len(fams), f0, min(f1, len(fams) - 1)), flush=True)
    tally = collections.Counter(); R1 = list(range(81)); seen_blocks = {}
    for fi, fam in enumerate(fams):
        if fi < f0 or fi > f1: continue
        t1 = time.time(); A1 = A0.copy()
        for v in range(NV):
            M = row(v, fam[v]); b = F[v]
            for q in range(NF): A1[b, F[q]] = (M >> q) & 1; A1[F[q], b] = (M >> q) & 1
        blk = A1[:81, :]; cn = blk @ blk.T
        good = all(blk[a].sum() == 22 for a in range(81)) and all(cn[a, b] == (1 if A1[a, b] else 2) for a in range(81) for b in range(a + 1, 81))
        changed = sum(1 for v in range(NV) if fam[v] != orig[v]); inner = int(A1[:81, :81].sum()) // 2
        if not good:
            tally["rejected: the 81 rows are inconsistent"] += 1; print("family %d (%d rows changed): rejected, the 81 complete rows are inconsistent" % (fi, changed), flush=True); continue
        deg_in = sorted(collections.Counter(int(x) for x in A1[:81, :81].sum(1)).items())
        sols, status, info = BC.completions(A1, R1, 900)
        res = collections.Counter()
        for A in sols:
            assert bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all())
            key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
            if hit is None:
                hit = "staged%d_%d.edges" % (kept, len(known))
                with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                    for a in range(n):
                        for b in range(a + 1, n):
                            if A[a, b]: f.write("%d %d\n" % (a, b))
                known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(x) for x in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
            res[hit] += 1; tally[hit] += 1
        print("family %d (%d of the %d rows changed; degrees inside the first 81 vertices %s): %s, %d completions (%.0f s): %s" % (fi, changed, NV, deg_in, status, len(sols), time.time() - t1, dict(res)), flush=True)
    print("end: %s" % dict(tally), flush=True)
