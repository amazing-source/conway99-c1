"""General-position model at a vertex (LAB, 20/10/2026, NOTE_BORNE_RANG section 4).

Coordinates: the 84 non-neighbours of a vertex v, labelled by pairs {p, q} of points of N(v) on two different lines
of the 7 lines through v.  Z = {z : sum_{w containing p} z_w = 0 for every point p} (dimension 70, non-degenerate for
the dot product mod 7).  In a srg(99,14,1,2) with rank_7(A - 3I) = r, D_v = (codewords of D vanishing on N[v]) is a
totally isotropic subspace of Z of dimension r - 15, and for the line T_i = {v, a_i, b_i}:
    C(T_i) = D_v cap F^(F_i),  F_i = pairs avoiding line i (60),  dim C(T_i) = r - 38 + d(T_i)   (P, note section 2).
This script draws RANDOM totally isotropic subspaces D' of Z of dimension k = r - 15 and prints the same numbers:
dim(D' cap F^(F_i)), rank of D' on S_i (24), dim(D' cap F^(F_i cap F_j)), and the dimension of the space of linear
relations sum_i c_i = 0 with c_i in D' cap F^(F_i).  If they coincide with the values forced in a srg, the
dimension pattern of the lines through a vertex carries no obstruction at that rank.

usage: python vertex_general_position.py <seed> <trials>
"""
import itertools
import random
import sys

import numpy as np

P = 7


def rref_basis(M):
    """row-reduced basis (rows) of the row space of M mod P"""
    M = (np.array(M, dtype=np.int64) % P).copy()
    if M.size == 0:
        return M.reshape(0, M.shape[1] if M.ndim == 2 else 0)
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        if r == rows:
            break
        piv = np.nonzero(M[r:, c])[0]
        if len(piv) == 0:
            continue
        i = r + piv[0]
        M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), P - 2, P)) % P
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % P
        r += 1
    return M[:r]


def rank(M):
    return len(rref_basis(M)) if np.size(M) else 0


def nullspace(M):
    """basis (rows) of {x : M x = 0} mod P"""
    M = np.array(M, dtype=np.int64) % P
    rows, cols = M.shape
    R = rref_basis(M)
    pivots = []
    for row in R:
        pivots.append(int(np.nonzero(row)[0][0]))
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        x = np.zeros(cols, dtype=np.int64)
        x[f] = 1
        for row, pc in zip(R, pivots):
            x[pc] = (-row[f]) % P
        basis.append(x)
    return np.array(basis, dtype=np.int64).reshape(len(basis), cols)


def setup():
    points = [(i, e) for i in range(7) for e in range(2)]          # point e of line i
    pairs = [(a, b) for a, b in itertools.combinations(range(14), 2) if points[a][0] != points[b][0]]
    assert len(pairs) == 84
    inc = np.zeros((14, 84), dtype=np.int64)
    for w, (a, b) in enumerate(pairs):
        inc[a, w] = inc[b, w] = 1
    line_of = lambda a: points[a][0]
    S = [[w for w, (a, b) in enumerate(pairs) if line_of(a) == i or line_of(b) == i] for i in range(7)]
    F = [[w for w in range(84) if w not in set(S[i])] for i in range(7)]
    return pairs, inc, S, F


def random_isotropic(Zb, k, rng):
    """random totally isotropic k-dim subspace of span(Zb) (rows), dot product mod P"""
    W = np.zeros((0, Zb.shape[1]), dtype=np.int64)
    while len(W) < k:
        # vectors of span(Zb) orthogonal to W: y = c Zb with (c Zb) W^T = 0
        if len(W):
            C = nullspace((Zb @ W.T % P).T)          # c with c (Zb W^T) = 0
            Y = C @ Zb % P
        else:
            Y = Zb.copy()
        for _ in range(200):
            c1 = np.array([rng.randrange(P) for _ in range(len(Y))], dtype=np.int64)
            c2 = np.array([rng.randrange(P) for _ in range(len(Y))], dtype=np.int64)
            y1, y2 = c1 @ Y % P, c2 @ Y % P
            a, b, c = int(y2 @ y2 % P), int(2 * (y1 @ y2) % P), int(y1 @ y1 % P)   # a t^2 + b t + c
            sols = [t for t in range(P) if (a * t * t + b * t + c) % P == 0]
            if not sols:
                continue
            y = (y1 + rng.choice(sols) * y2) % P
            if not y.any() or rank(np.vstack([W, y])) == len(W):
                continue
            W = np.vstack([W, y])
            break
        else:
            raise RuntimeError("no isotropic extension found")
    assert not (W @ W.T % P).any()
    return W


def sub_on(W, cols_zero):
    """basis of {x in rowspace(W) : x vanishes on cols_zero}"""
    if len(W) == 0:
        return W
    C = nullspace(W[:, cols_zero].T) if len(cols_zero) else np.eye(len(W), dtype=np.int64)
    if len(C) == 0:
        return np.zeros((0, W.shape[1]), dtype=np.int64)
    return rref_basis(C @ W % P)


def main():
    seed, trials = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    pairs, inc, S, F = setup()
    Zb = nullspace(inc)
    assert len(Zb) == 70
    gram = Zb @ Zb.T % P
    print("dim Z = %d, rank of the dot product on Z = %d" % (len(Zb), rank(gram)))
    for r in (37, 39, 41, 43):
        k = r - 15
        for t in range(trials):
            W = random_isotropic(Zb, k, rng)
            dimsC = []
            Cs = []
            for i in range(7):
                Ci = sub_on(W, S[i])
                Cs.append(Ci)
                dimsC.append(len(Ci))
            rkS = [rank(W[:, S[i]]) for i in range(7)]
            inter = []
            for i, j in itertools.combinations(range(7), 2):
                inter.append(len(sub_on(W, sorted(set(S[i]) | set(S[j])))))
            tot = sum(dimsC)
            span = rank(np.vstack([c for c in Cs if len(c)])) if tot else 0
            print("r=%d k=%d trial %d: dim C_i = %s (srg value %d), rank on S_i = %s, max dim C_i cap C_j = %d,"
                  " dim sum C_i = %d, relations = %d (forced lower bound %d)"
                  % (r, k, t, dimsC, r - 37, rkS, max(inter), span, tot - span, max(0, 7 * (r - 37) - k)),
                  flush=True)


if __name__ == "__main__":
    main()
