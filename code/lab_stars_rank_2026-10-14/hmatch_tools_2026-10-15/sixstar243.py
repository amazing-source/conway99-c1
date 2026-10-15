"""Six-star blocks of REAL srg(243,22,1,2) graphs (LAB 15/10/2026, calibration of the (H-MATCH) evidence).
For a vertex x and three lines l, m, n at x: Sigma = N[x] u (the labels meeting the six letters), and the nullity of
T_S = multiplicity of the eigenvalue 4 of A_Sigma (Haynsworth, as catalogue G1 for Conway), forced >= |S| - 88.
Also the h-relation of the star matchings for each of the three pairs.
usage: python sixstar243.py <edges> [vertices] [triples per vertex]"""
import itertools
import random
import sys

import numpy as np

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in E)
A = np.zeros((nv, nv))
adj = [set() for _ in range(nv)]
for i, j in E:
    A[i, j] = A[j, i] = 1
    adj[i].add(j)
    adj[j].add(i)
nvert = int(sys.argv[2]) if len(sys.argv) > 2 else 3
ntrip = int(sys.argv[3]) if len(sys.argv) > 3 else 3
rng = random.Random(1)
for x in range(nvert):
    Nx = sorted(adj[x])
    mate = {a: [y for y in adj[a] if y in adj[x]][0] for a in Nx}
    lines = sorted({tuple(sorted((a, mate[a]))) for a in Nx})
    for tri in rng.sample(list(itertools.combinations(lines, 3)), ntrip):
        letters = [a for ln in tri for a in ln]
        labs = set()
        for a in letters:
            for y in Nx:
                if y in (a, mate[a]):
                    continue
                w = [z for z in adj[a] & adj[y] if z != x][0]
                labs.add(w)
        Sig = [x] + Nx + sorted(labs)
        ev = np.linalg.eigvalsh(A[np.ix_(Sig, Sig)])
        m4 = int(np.sum(np.abs(ev - 4) < 1e-7))
        m5 = int(np.sum(np.abs(ev + 5) < 1e-7))
        print("vertex %d lines %s: |S| = %d labels, forced nullity >= %d, mult(4) = %d, mult(-5) = %d, lambda_2 = %.4f, "
              "lambda_min = %.4f" % (x, tri, len(labs), len(labs) - 88, m4, m5, sorted(ev)[-2], ev[0]), flush=True)
