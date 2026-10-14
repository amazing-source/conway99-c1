"""Candidate trade regions in the hemisystem graph srg(378,52,1,8) (14/10/2026).
Vertices = lines of the hemisystem H of FTWKB(5). For a GQ line m NOT in H let X_m = the H-lines meeting m (26 points
x 3 = 78). Facts checked here: |N(v) & X_m| for v in X_m and for v outside (expected constant: then 1_{X_m} is an
'intriguing set' and 1_{X_m} - 1_{X_m'} an eigenvector with small support). For F = X_m u X_m' (two non-H lines,
opposite or concurrent), the dimensions of the eigenvectors of each eigenvalue supported in F (exact ranks mod a large
prime; the eigenspace basis comes from the integral matrices A - r I, A - s I).
usage: python regions378.py <gq.json> <hemi.json> <edges> <number of pairs to test>"""
import json
import random
import sys

import numpy as np

PR = 1000003


def rank_mod(M):
    M = [list(map(int, r)) for r in M]
    if not M:
        return 0
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] % PR), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        iv = pow(M[r][c], PR - 2, PR)
        M[r] = [(x * iv) % PR for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % PR:
                f = M[i][c]
                M[i] = [(a - f * b) % PR for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def supported_dim(A, theta, F):
    """dim of {x : (A - theta I) x = 0, x = 0 outside F} = |F| - rank of (A - theta I)[:, F] (columns in F)"""
    n = len(A)
    M = (A - theta * np.eye(n, dtype=np.int64))[:, sorted(F)]
    return len(F) - rank_mod(M.tolist())


if __name__ == "__main__":
    G = json.load(open(sys.argv[1]))
    H = json.load(open(sys.argv[2]))
    E = [tuple(map(int, l.split())) for l in open(sys.argv[3]) if l.strip()]
    ntest = int(sys.argv[4])
    lines = [set(l) for l in G["lines"]]
    n = len(H)
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in E:
        A[a, b] = A[b, a] = 1
    Hs = set(H)
    nonH = [i for i in range(len(lines)) if i not in Hs]
    X = {m: {k for k, h in enumerate(H) if lines[h] & lines[m]} for m in nonH}
    sizes = {len(x) for x in X.values()}
    inside, outside = set(), set()
    for m in nonH[:40]:
        for v in range(n):
            c = int(A[v, sorted(X[m])].sum())
            (inside if v in X[m] else outside).add(c)
    print("non-H lines %d; |X_m| %s; |N(v) & X_m| inside %s, outside %s (40 lines tested)" % (len(nonH), sizes, inside, outside), flush=True)
    rng = random.Random(1)
    opp = [(m1, m2) for m1, m2 in ((rng.choice(nonH), rng.choice(nonH)) for _ in range(4000))
           if m1 != m2 and not (lines[m1] & lines[m2])][:ntest]
    con = [(m1, m2) for m1, m2 in ((rng.choice(nonH), rng.choice(nonH)) for _ in range(40000))
           if m1 != m2 and (lines[m1] & lines[m2])][:ntest]
    for kind, pairs in (("opposite", opp), ("concurrent", con)):
        for m1, m2 in pairs:
            F = X[m1] | X[m2]
            d4 = supported_dim(A, 4, F)
            d11 = supported_dim(A, -11, F)
            print("%s non-H lines: |F| = %d, supported eigenvectors: theta=4 -> %d, theta=-11 -> %d" % (kind, len(F), d4, d11), flush=True)
