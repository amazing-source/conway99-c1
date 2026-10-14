"""Star condition of route Omega (Codex note 157, section 2.5), 14/10/2026.

Conway graph rooted at v: letters 0..13 (mates i, i^1), labels = the 84 non-mate pairs of letters (far vertices).
T = 3I - Gamma - K is the Schur complement of 3I - A on the labels (K_ll' = -1/4 + 3/8 |l n l'| + 1/8 m(l, l'),
m = number of mate relations between the letters of l and l'; re-derived here from P^-1, P = 3I - windmill, and checked
numerically below). T^2 = 7T and rank T = 30, so for every set S of labels: 0 <= T_S <= 7I and rank T_S <= 30.
For S a union of stars L_y (labels containing y) the star vectors 1_{L_y} lie in ker T_S automatically.

Admissible structure on S = graph Gamma_S with
  (C1) |N(l) n L_y| = 1 if y or mate(y) is a letter of l, else 2      (lambda / mu between the label l and the letter y)
  (C2) shared letters + common neighbours inside S <= 1 if l ~ l', <= 2 if not      (lambda / mu caps)
Random admissible structures from cryptominisat (random polarity, random seed, random variable order); spectrum of T_S.
usage: python stars_rank.py <stars, e.g. 0,1,2> <samples> <seed> [out.npz]
"""
import itertools
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

MATE = lambda i: i ^ 1
LETTERS = list(range(14))
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(LETTERS, 2) if w != MATE(u)]
assert len(LABELS) == 84


def kval(l1, l2):
    inter = len(l1 & l2)
    m = sum(1 for y in l1 for z in l2 if z == MATE(y))
    return -0.25 + 0.375 * inter + 0.125 * m


def check_K():
    """K = B^T Q B with Q the letter block of P^-1, P = 3I - windmill on {v} + letters."""
    W = np.zeros((15, 15))
    for y in LETTERS:
        W[0, 1 + y] = W[1 + y, 0] = 1
        W[1 + y, 1 + MATE(y)] = 1
    Pinv = np.linalg.inv(3 * np.eye(15) - W)
    Q = Pinv[1:, 1:]
    B = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for y in l:
            B[y, j] = 1
    Kn = B.T @ Q @ B
    Kc = np.array([[kval(a, b) for b in LABELS] for a in LABELS])
    assert np.allclose(Kn, Kc), "closed form of K"
    assert np.allclose(np.linalg.solve(3 * np.eye(15) - W, np.ones(15)), [-2] + [-0.5] * 14)


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


class CNF:
    def __init__(self):
        self.n = 0
        self.clauses = []

    def var(self):
        self.n += 1
        return self.n

    def add(self, c):
        self.clauses.append(c)


def build(stars, rng):
    S = [l for l in LABELS if any(y in l for y in stars)]
    idx = {l: i for i, l in enumerate(S)}
    F = CNF()
    pairs = list(itertools.combinations(range(len(S)), 2))
    rng.shuffle(pairs)
    e = {}
    for i, j in pairs:
        e[(i, j)] = e[(j, i)] = F.var()
    # (C1) exact counts towards every star in S
    for l in S:
        i = idx[l]
        for y in stars:
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            c = count_needed(l, y)
            for sub in itertools.combinations(lits, c + 1):         # at most c
                F.add([-x for x in sub])
            if c == 1:                                              # at least c
                F.add(list(lits))
            else:
                for x in lits:
                    F.add([z for z in lits if z != x])
    # (C2) caps on common neighbours inside S (sequential counter, upper direction only)
    for i, j in itertools.combinations(range(len(S)), 2):
        s = len(S[i] & S[j])
        prods = []
        for t in range(len(S)):
            if t in (i, j):
                continue
            p = F.var()
            F.add([-e[(i, t)], -e[(j, t)], p])
            prods.append(p)
        R = {}
        prev = {}
        for p in prods:
            cur = {}
            for m in (1, 2, 3):
                r = F.var()
                if m == 1:
                    F.add([-p, r])
                else:
                    if m - 1 in prev:
                        F.add([-p, -prev[m - 1], r])
                if m in prev:
                    F.add([-prev[m], r])
                cur[m] = r
            prev = cur
        R = prev
        eij = e[(i, j)]
        if s == 1:
            F.add([-eij, -R[1]])
            F.add([eij, -R[2]])
        else:
            F.add([-eij, -R[2]])
            F.add([eij, -R[3]])
    return S, idx, e, F


def spectrum(S, adj):
    n = len(S)
    T = np.array([[(3.0 if a == b else 0.0) - adj[a][b] - kval(S[a], S[b]) for b in range(n)] for a in range(n)])
    return T, np.linalg.eigvalsh(T)


def main():
    stars = [int(t) for t in sys.argv[1].split(",")]
    samples, seed = int(sys.argv[2]), int(sys.argv[3])
    out = sys.argv[4] if len(sys.argv) > 4 else None
    check_K()
    rng = random.Random(seed)
    S0 = [l for l in LABELS if any(y in l for y in stars)]
    nstar = len(stars)
    print("stars %s: |S| = %d labels, forced kernel %d, rank bound 30 -> extra relations needed: %d"
          % (stars, len(S0), nstar, max(0, len(S0) - nstar - 30)), flush=True)
    rows = []
    t0 = time.time()
    for k in range(samples):
        S, idx, e, F = build(stars, rng)
        sol = Solver(options={"polar": "rnd", "seed": str(rng.randrange(1, 10 ** 9))})
        for c in F.clauses:
            sol.add_clause(c)
        ok, model = sol.solve()
        if not ok:
            print("UNSAT (no admissible structure at all)", flush=True)
            return
        n = len(S)
        adj = [[0] * n for _ in range(n)]
        for (i, j), v in e.items():
            if i < j and model[v]:
                adj[i][j] = adj[j][i] = 1
        T, ev = spectrum(S, adj)
        for y in stars:                                   # sanity: star vectors in the kernel
            vec = np.array([1.0 if y in l else 0.0 for l in S])
            assert np.allclose(T @ vec, 0), "star relation fails"
        rank = int((np.abs(ev) > 1e-8).sum())
        free = ev[nstar:nstar + 12] if nstar else ev[:12]
        rows.append((ev[0], ev[nstar], ev[-1], rank) + tuple(ev[:nstar + 12]))
        if k < 5 or k % 20 == 0:
            print("  sample %d: lambda_min %.4f, first free eigenvalue %.4f, lambda_max %.4f, rank %d (%.0f s)"
                  % (k, ev[0], ev[nstar], ev[-1], rank, time.time() - t0), flush=True)
    a = np.array(rows)
    print("samples %d | PSD (lambda_min >= -1e-9): %d | lambda_max <= 7: %d | rank <= 30: %d"
          % (len(a), int((a[:, 0] >= -1e-9).sum()), int((a[:, 2] <= 7 + 1e-9).sum()), int((a[:, 3] <= 30).sum())))
    print("lambda_min range [%.4f, %.4f]; first free eigenvalue range [%.4f, %.4f]; lambda_max range [%.4f, %.4f]"
          % (a[:, 0].min(), a[:, 0].max(), a[:, 1].min(), a[:, 1].max(), a[:, 2].min(), a[:, 2].max()))
    from collections import Counter
    print("rank histogram:", dict(sorted(Counter(a[:, 3].astype(int)).items())))
    if out:
        np.savez(out, rows=a)


if __name__ == "__main__":
    main()
