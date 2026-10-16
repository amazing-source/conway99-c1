"""Read a cadical model of the five-star CNF (five_split_par.py), rebuild the 52-label structure, check it with an
independent direct checker (C1 exact for the stars, C1' for the other letters, C2 caps), and report T, U on the
four-star block (stars 0..3) and on all 52 labels (LAB 16/10/2026).
usage: python five_model.py <model file> <out json>"""
import itertools
import json
import random
import sys

import numpy as np

from stars_rank import build, kval, LABELS

MATE = lambda i: i ^ 1


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


S, idx, e, F = build([0, 1, 2, 3, 4], random.Random(1))
vals = set()
for line in open(sys.argv[1]):
    if line.startswith("v "):
        vals.update(int(t) for t in line.split()[1:] if t != "0")
n = len(S)
G = np.zeros((n, n), dtype=np.int64)
for i, j in itertools.combinations(range(n), 2):
    if e[(i, j)] in vals:
        G[i, j] = G[j, i] = 1
stars = [0, 1, 2, 3, 4]
bad = []
for i, l in enumerate(S):
    for y in range(14):
        cnt = sum(G[i, j] for j, t in enumerate(S) if y in t and j != i)
        c = count_needed(l, y)
        if (y in stars and cnt != c) or (y not in stars and cnt > c):
            bad.append(("C1", sorted(l), y, int(cnt), c))
for i, j in itertools.combinations(range(n), 2):
    com = int(sum(G[i, t] * G[j, t] for t in range(n)))
    if com + len(S[i] & S[j]) + G[i, j] > 2:
        bad.append(("C2", sorted(S[i]), sorted(S[j]), com))
print("independent check: %s" % ("OK" if not bad else "VIOLATIONS %d, e.g. %s" % (len(bad), bad[:3])), flush=True)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: k for k, l in enumerate(LABELS)}


def tu(sub):
    K = np.array([[kval(a, b) for b in sub] for a in sub])
    ii = [S.index(l) for l in sub]
    T = 3 * np.eye(len(sub)) - G[np.ix_(ii, ii)] - K
    PiS = Pi[np.ix_([pos[l] for l in sub], [pos[l] for l in sub])]
    ev = np.linalg.eigvalsh(T)
    eu = np.linalg.eigvalsh(7 * PiS - T)
    return float(ev[0]), float(eu[0]), int(np.sum(np.abs(ev) < 1e-8))


S4 = [l for l in S if l & {0, 1, 2, 3}]
print("four-star block: lambda_min T %.4f, lambda_min U %.4f, nullity %d" % tu(S4), flush=True)
print("52-label block:  lambda_min T %.4f, lambda_min U %.4f, nullity %d (Conway needs >= 22)" % tu(S), flush=True)
json.dump({"labels": [sorted(l) for l in S], "edges": [[i, j] for i, j in itertools.combinations(range(n), 2) if G[i, j]],
           "check": "OK" if not bad else bad[:20]}, open(sys.argv[2], "w"))
