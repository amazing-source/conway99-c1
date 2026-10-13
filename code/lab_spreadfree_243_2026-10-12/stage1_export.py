"""Lab session, 2026-10-13. Export for stage1_search.c: the candidate rows of the freed vertices of the block when only
the first <kept> vertices of the block are kept, their pairwise targets, and the orbit representatives for the first
freed vertex (under the automorphisms of the input preserving the kept set and fixing that vertex).
Binary layout (little endian): 5 ints (freed vertices NV, free vertices NF, 64-bit words per row W, number of
representatives, 0); NV x (bit position, number of rows); NV x NV targets; the representatives (row indices of the
first vertex); NV indices of the rows of the input; then the rows, W words each.
python stage1_export.py <edge file> <kept> <out prefix> <row cap>      (environment PYLIB)"""
import sys, os, struct, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import numpy as np
import aut_tools as T, boundary_census as BC, regular_subgroups as RS
n = 243
path, kept, prefix, cap = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
A0 = T.load(path); adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]
H4 = list(itertools.product(range(3), repeat=4)); IDX4 = {g: i for i, g in enumerate(H4)}
def shift(v, t): return 81 * (v // 81) + IDX4[tuple((a + b) % 3 for a, b in zip(H4[v % 81], t))]
R0 = list(range(kept)); Rs = set(R0); F = list(range(kept, n)); NF = len(F); pos = {v: i for i, v in enumerate(F)}; B1 = list(range(kept, 81))
trans = [t for t in H4 if all(shift(v, t) in Rs for v in R0)]            # translations preserving the kept set
print("kept %d: %d translations preserve the kept set; %d freed vertices of the block" % (kept, len(trans), len(B1)), flush=True)
rows = {}; t0 = time.time(); done = set()
for b in B1:                                                            # one enumeration per orbit of these translations
    if b in done: continue
    r = BC.rows_of(adj, R0, Rs, F, b, cap)
    if r is None: raise SystemExit("more than %d rows at vertex %d" % (cap, b))
    for t in trans:
        b2 = shift(b, t)
        if b2 not in done: rows[b2] = [frozenset(shift(v, t) for v in N) for N in r]; done.add(b2)
    print("   vertex %d: %d rows (%.0f s)" % (b, len(r), time.time() - t0), flush=True)
o, gens, base, sizes = T.aut_group(A0); ident = tuple(range(n)); G = RS.generate([tuple(g) for g in gens], ident)
b0 = B1[0]; stab = [g for g in G if g[b0] == b0 and all(g[v] in Rs for v in R0)]
seen = set(); reps = []
for i, N in enumerate(rows[b0]):
    if N in seen: continue
    seen |= {frozenset(g[v] for v in N) for g in stab}; reps.append(i)
W = (NF + 63) // 64
with open(prefix + ".bin", "wb") as f:
    f.write(struct.pack("<5i", len(B1), NF, W, len(reps), 0))
    for b in B1: f.write(struct.pack("<2i", pos[b], len(rows[b])))
    for b in B1:
        for c in B1: f.write(struct.pack("<i", 2 - len(adj[b] & adj[c] & Rs) if b != c else 0))
    f.write(struct.pack("<%di" % len(reps), *reps))
    for b in B1: f.write(struct.pack("<i", rows[b].index(frozenset(adj[b] - Rs))))
    for b in B1:
        for N in rows[b]:
            m = sum(1 << pos[v] for v in N); f.write(struct.pack("<%dQ" % W, *[(m >> (64 * k)) & 0xFFFFFFFFFFFFFFFF for k in range(W)]))
print("written %s.bin: %d freed vertices, %d first-row representatives under %d automorphisms" % (prefix, len(B1), len(reps), len(stab)))
