"""Lab session, 2026-10-12. The linear code C = { ([p split])_p } = L(Z^1) in F_2^2430 (L_p = sum of eps over the bundle of p).
1. dimension of C (rank of L on the line-even edge functions); is L injective on H^1 (dimension 460)?
2. heuristic search (annealing on the line-even functions) for a codeword of large weight: the complement of its support
   would be the set of flat pairs, so 2430 - (maximal weight) is the minimal number of flat pairs allowed by parity alone.
   (A search gives only a lower bound on the maximal weight, i.e. an UPPER bound on that minimum.)
python parity_code.py <seconds> <seed>"""
import sys, time, random, itertools
import numpy as np
from local_lib import *
secs, seed = float(sys.argv[1]), int(sys.argv[2]); random.seed(seed)
edges = [(i, j) for i in range(n) for j in sorted(nbs[i]) if i < j]; eidx = {e: k for k, e in enumerate(edges)}
pairs = sorted(CN); pidx = {p: k for k, p in enumerate(pairs)}
lines = sorted({tuple(sorted((i, j, next(iter(nbs[i] & nbs[j]))))) for (i, j) in edges})
# generators of Z^1: for each line, two of its edges (three "V-shapes" per line)
gens = []
for t in lines:
    es = [eidx[key(t[0], t[1])], eidx[key(t[1], t[2])], eidx[key(t[0], t[2])]]
    gens += [(es[0], es[1]), (es[1], es[2]), (es[0], es[2])]
bund = [[] for _ in edges]                                    # edge -> pairs whose bundle contains it
for p, c in CN.items():
    for z in c:
        bund[eidx[key(p[0], z)]].append(pidx[p]); bund[eidx[key(z, p[1])]].append(pidx[p])
# rank of L on Z^1 (python ints as bit vectors over the pairs)
vec = lambda e: sum(1 << k for k in bund[e])
basis = {}; rank = 0
for (e1, e2) in gens:
    v = vec(e1) ^ vec(e2)
    while v:
        b = v.bit_length() - 1
        if b in basis: v ^= basis[b]
        else: basis[b] = v; rank += 1; break
print("dimension of C = L(Z^1): %d  (H^1 has dimension 460: L is %s on H^1)" % (rank, "injective" if rank == 460 else "NOT injective"))
# annealing
gen_pairs = [np.array(sorted(set(bund[e1]) ^ set(bund[e2])), dtype=np.int64) for (e1, e2) in gens]
sp = np.zeros(len(pairs), dtype=np.int8); w = 0; best = 0
t0 = time.time(); T0, T1 = 3.0, 0.3; it = 0
while time.time() - t0 < secs:
    frac = (time.time() - t0) / secs if it % 256 == 0 else frac if it else 0.0
    T = T0 * (T1 / T0) ** frac
    g = random.randrange(len(gens)); idx = gen_pairs[g]
    d = len(idx) - 2 * int(sp[idx].sum())
    if d >= 0 or random.random() < np.exp(d / T):
        sp[idx] ^= 1; w += d
        if w > best: best = w
    it += 1
print("annealing %d moves: best weight found %d of 2430, i.e. only %d flat pairs needed by parity (upper bound on the minimum)" % (it, best, 2430 - best))
