"""Generalised star model for srg(v,k,1,2) (LAB 15/10/2026; calibration of the (H-MATCH) evidence on srg(243,22,1,2)).

Rooted at x: letters 0..k-1 (mates i, i^1), labels = non-mate pairs of letters (common neighbour of the two letters
other than x).  T = r I - Gamma - K, K = B^T Q B with Q the letter block of (r I - W)^-1, W = windmill on x + letters
(Schur complement of r I - A on the labels; r = the positive non-principal eigenvalue: 3 for (99,14,1,2), 4 for
(243,22,1,2)), U = (r - s) Pi - T with Pi = I - D^T (D D^T)^-1 D on the labels.  Admissible structures on the labels
meeting a set of star letters: (C1) exact counts towards the stars, (C1') caps towards the other letters, (C2) caps
(same rules as stars_rank.build, which this reproduces for k = 14, r = 3).
"""
import itertools

import numpy as np

from stars_rank import CNF


class Model:
    def __init__(self, k, r, s):
        self.k, self.r, self.s = k, r, s
        self.mate = lambda i: i ^ 1
        self.labels = [frozenset((u, w)) for u, w in itertools.combinations(range(k), 2) if w != (u ^ 1)]
        L = len(self.labels)
        W = np.zeros((k + 1, k + 1))
        for y in range(k):
            W[0, 1 + y] = W[1 + y, 0] = 1
            W[1 + y, 1 + (y ^ 1)] = 1
        Q = np.linalg.inv(r * np.eye(k + 1) - W)[1:, 1:]
        B = np.zeros((k, L))
        for j, l in enumerate(self.labels):
            for y in l:
                B[y, j] = 1
        self.Kfull = B.T @ Q @ B
        self.Pifull = np.eye(L) - B.T @ np.linalg.inv(B @ B.T) @ B
        self.pos = {l: i for i, l in enumerate(self.labels)}

    def count_needed(self, l, y):
        return 1 if (y in l or (y ^ 1) in l) else 2

    def build(self, stars, rng):
        S = [l for l in self.labels if any(y in l for y in stars)]
        idx = {l: i for i, l in enumerate(S)}
        F = CNF()
        pairs = list(itertools.combinations(range(len(S)), 2))
        rng.shuffle(pairs)
        e = {}
        for i, j in pairs:
            e[(i, j)] = e[(j, i)] = F.var()
        for l in S:
            i = idx[l]
            for y in range(self.k):
                lits = [e[(i, idx[t])] for t in S if y in t and t != l]
                if not lits:
                    continue
                c = self.count_needed(l, y)
                if y in stars:
                    # exactly c (c is 1 or 2): at most c by pairwise/triple exclusion, at least c by covering clauses
                    for sub in itertools.combinations(lits, c + 1):
                        F.add([-x for x in sub])
                    if c == 1:
                        F.add(list(lits))
                    else:
                        for x in lits:
                            F.add([z for z in lits if z != x])
                else:
                    for sub in itertools.combinations(lits, c + 1):
                        F.add([-x for x in sub])
        for i, j in itertools.combinations(range(len(S)), 2):
            sh = len(S[i] & S[j])
            prev = {}
            for t in range(len(S)):
                if t in (i, j):
                    continue
                p = F.var()
                F.add([-e[(i, t)], -e[(j, t)], p])
                cur = {}
                for m in (1, 2, 3):
                    rr = F.var()
                    if m == 1:
                        F.add([-p, rr])
                    elif m - 1 in prev:
                        F.add([-p, -prev[m - 1], rr])
                    if m in prev:
                        F.add([-prev[m], rr])
                    cur[m] = rr
                prev = cur
            eij = e[(i, j)]
            if sh == 1:
                F.add([-eij, -prev[1]])
                F.add([eij, -prev[2]])
            else:
                F.add([-eij, -prev[2]])
                F.add([eij, -prev[3]])
        return S, idx, e, F

    def matrices(self, S):
        ii = [self.pos[l] for l in S]
        return self.Kfull[np.ix_(ii, ii)], self.Pifull[np.ix_(ii, ii)]
