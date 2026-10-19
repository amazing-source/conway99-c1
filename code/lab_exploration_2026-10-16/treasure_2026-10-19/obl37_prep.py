"""Preparation for the C++ engine obl37.cpp (LAB 19/10/2026): for a random generic line (seed), the candidate far
triples per p-pair (lambda/mu filter L2 and the rank-37 diagonal condition e^T X e = 4 mod 7), and for every pair of
p-pairs the compatibility bitsets (forced adjacency e_i^T X e_j in {0,1} mod 7, distinct q- and s-pairs, at most one
shadow per transversal 3-set) and the adjacency bitsets (forced value 1).  Binary output read by obl37.cpp.
usage: python obl37_prep.py <seed> <instance> <out.bin>"""
import random
import struct
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),
                                              "..", "reduction_2026-10-19"))
from ll_test import k_matrix, random_gt  # noqa: E402
from obligation37 import candidates, setup  # noqa: E402

seed, inst, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed)
n = 12
k = -1
while True:
    s01, s12, s20, tries = random_gt(n, rng, 1)
    G, d, rk, X = setup(n, s01, s12, s20)
    if d != 1:
        continue
    k += 1
    if k == inst:
        break
P, cand = candidates(n, s01, s12, s20, G, X)
K = k_matrix(n, G)
m = len(P)
N3 = 3 + 3 * n
sizes = [len(cand[p]) for p in range(m)]
Y, Ev, Q, S, NM = [], [], [], [], []
for p in range(m):
    c = cand[p]
    Y.append(np.array([t[4] for t in c], dtype=np.int64))              # X e_t (len 39)
    e = np.zeros((len(c), N3), dtype=np.int64)
    for i, t in enumerate(c):
        e[i, [3 + x for x in t[3]]] = 1
    Ev.append(e)
    Q.append(np.array([P.index(t[1]) for t in c]))
    S.append(np.array([P.index(t[2]) for t in c]))
    NM.append([t[3] for t in c])
W = max(sizes)
SHARE = np.array([[bool(set(a) & set(b)) for b in P] for a in P])
words = (W + 63) // 64
with open(out, "wb") as f:
    f.write(struct.pack("<iiii", n, m, W, words))
    f.write(struct.pack("<%di" % m, *sizes))
    for p in range(m):                                                  # names of each candidate (6 ints)
        for t in NM[p]:
            f.write(struct.pack("<6i", *t))
    f.write(struct.pack("<%di" % (3 * n * n), *[int(x) for x in np.concatenate(
        [K[0:n, n:2 * n].ravel(), K[0:n, 2 * n:3 * n].ravel(), K[n:2 * n, 2 * n:3 * n].ravel()])]))
    for p in range(m):
        for p2 in range(m):
            if p2 == p:
                continue
            B = (Y[p] @ Ev[p2].T) % 7                                   # forced adjacency values
            ok = (B <= 1) & (Q[p][:, None] != Q[p2][None, :]) & (S[p][:, None] != S[p2][None, :])
            # L3: no two far vertices sharing a letter in each of the three classes
            if set(P[p]) & set(P[p2]):
                ok &= ~(SHARE[Q[p][:, None], Q[p2][None, :]] & SHARE[S[p][:, None], S[p2][None, :]])
            adj = ok & (B == 1)
            for M in (ok, adj):
                bits = np.zeros((sizes[p], words * 64), dtype=np.uint8)
                bits[:, :sizes[p2]] = M
                packed = np.packbits(bits, axis=1, bitorder="little").view("<u8")
                f.write(packed.tobytes())
print("prepared: seed %d instance %d, candidates per p-pair %d..%d (W = %d)" % (seed, inst, min(sizes), max(sizes), W))
