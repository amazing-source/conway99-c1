"""Near blocks of the two projectors on N[T] (39 vertices) for random admissible G_T (LAB, NOTE_ORDRE2 §3.5):
P_-4,NN = (27I - 9A + J)/63 and P_3,NN = (4I + A)/7 - 2J/77 must be PSD, rank(P_-4,NN) = 36, and the kernel vectors
kappa_t = e_t + (5/18) 1_{C_t} - (1/18)(1_{C_t'} + 1_{C_t''}) (RD §1) must annihilate P_-4,NN.
usage: python o2_nearblocks.py <seed> ..."""
import os
import sys

import numpy as np

MERGE = r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19"
sys.path.insert(0, MERGE)
sys.path.insert(0, os.path.join(MERGE, "..", "reduction_2026-10-19"))
from star_csp import line_graph, n, N  # noqa: E402

for seed in map(int, sys.argv[1:]):
    gt, G, Om, K, leg = line_graph(seed, 0)
    A = np.zeros((39, 39))
    A[3:, 3:] = G
    for t in range(3):
        A[t, [u for u in range(3) if u != t]] = 1
        A[t, 3 + n * t: 3 + n * (t + 1)] = 1
        A[3 + n * t: 3 + n * (t + 1), t] = 1
    I, J = np.eye(39), np.ones((39, 39))
    Pm = (27 * I - 9 * A + J) / 63
    P3 = (4 * I + A) / 7 - 2 * J / 77
    em, e3 = np.linalg.eigvalsh(Pm), np.linalg.eigvalsh(P3)
    kap = []
    for t in range(3):
        k = np.zeros(39); k[t] = 1
        for s in range(3):
            k[3 + n * s: 3 + n * (s + 1)] = 5 / 18 if s == t else -1 / 18
        kap.append(np.abs(Pm @ k).max())
    print({"seed": seed, "min eig P-4,NN": float(em.min()), "rank P-4,NN": int((em > 1e-9).sum()),
           "min eig P3,NN": float(e3.min()), "rank P3,NN": int((e3 > 1e-9).sum()), "max |P kappa_t|": float(max(kap))})

# image conditions: the kernels of both near blocks must annihilate the near column of every far vertex
# (6 names, two non-partner names per class, none in T): P_-4[N, a] = (-9 e_W + 1)/63, P_3[N, a] = e_W/7 - 2/77.
import random
from ll_test import pairs_of  # noqa: E402
rng = random.Random(7)
for seed in map(int, sys.argv[1:]):
    gt, G, Om, K, leg = line_graph(seed, 0)
    A = np.zeros((39, 39)); A[3:, 3:] = G
    for t in range(3):
        A[t, [u for u in range(3) if u != t]] = 1
        A[t, 3 + n * t: 3 + n * (t + 1)] = 1
        A[3 + n * t: 3 + n * (t + 1), t] = 1
    I, J = np.eye(39), np.ones((39, 39))
    worst = 0.0
    for Pnn, col in (((27 * I - 9 * A + J) / 63, lambda e: (-9 * e + 1) / 63), ((4 * I + A) / 7 - 2 * J / 77, lambda e: e / 7 - 2 / 77)):
        w, V = np.linalg.eigh(Pnn)
        ker = V[:, w < 1e-9]
        for _ in range(200):
            e = np.zeros(39)
            for c in range(3):
                a, b = rng.choice(pairs_of(n))
                e[3 + n * c + a] = e[3 + n * c + b] = 1
            worst = max(worst, float(np.abs(ker.T @ col(e)).max()))
    print({"seed": seed, "max |kernel^T column| over 200 random far columns, both blocks": worst})
