"""Lab session, 2026-10-13. Machine check, on real graphs srg(v,k,1,2), of the line (triangle) identities sent to Codex
for the case v = 99. General form, eigenvalues r > 0 > s, c = (k - r)/v, N = points x lines:
  (1) (r - s) * 1_L^t E_s 1_M = 3r - 6 + 9c if L = M;  r - 4 + 9c if L, M meet;  9c - j if they are disjoint with j edges;
  (2) G = (r - s) N^t E_s N satisfies G^2 = (r - s)(k/2 + s) G and has rank mult(s);
  (3) for every integer vector z: sum over the lines of ((r - s) z^t E_s 1_L)^2 = (r - s)^2 (k/2 + s) z^t E_s z.
At 99 (k = 14, r = 3, s = -4, c = 1/9) these read: entries 4, 0, 1 - j; G^2 = 21 G, rank 44; factor 147.
The check is done in exact integer arithmetic after clearing denominators (multiply by v).
python -I check_line_gram.py <edge file> [<edge file> ...]"""
import sys, random
import numpy as np
for path in sys.argv[1:]:
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]; v = 1 + max(max(e) for e in E)
    A = np.zeros((v, v), dtype=np.int64)
    for a, b in E: A[a, b] = A[b, a] = 1
    k = int(A[0].sum()); adj = [set(np.nonzero(A[x])[0].tolist()) for x in range(v)]
    # r, s from x^2 + x - (k - 2) = 0 (lambda = 1, mu = 2)
    disc = 1 + 4 * (k - 2); rt = int(round(disc ** 0.5)); assert rt * rt == disc; r, s = (-1 + rt) // 2, (-1 - rt) // 2
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(v) for y in adj[x] if x < y}); nl = len(lines)
    N = np.zeros((v, nl), dtype=np.int64)
    for i, L in enumerate(lines): N[list(L), i] = 1
    assert (N @ N.T == (k // 2) * np.eye(v, dtype=np.int64) + A).all()
    # v * (r - s) * E_s = v r I - v A + (k - r) J    (integer matrix)
    Ev = v * r * np.eye(v, dtype=np.int64) - v * A + (k - r) * np.ones((v, v), dtype=np.int64)
    G = N.T @ Ev @ N                                              # = v * (r - s) * N^t E_s N
    inter = N.T @ N; edges = N.T @ A @ N; ok1 = True
    for i in range(0, nl, 7):
        for j in range(nl):
            if i == j: want = v * (3 * r - 6) + 9 * (k - r)
            elif inter[i, j] == 1: want = v * (r - 4) + 9 * (k - r)
            else: want = 9 * (k - r) - v * int(edges[i, j])
            if G[i, j] != want: ok1 = False
    ok2 = bool((G @ G == v * (r - s) * (k // 2 + s) * G).all()); rank = np.linalg.matrix_rank(G.astype(float))
    rnd = random.Random(1); z = np.array([rnd.randint(-2, 2) for _ in range(v)], dtype=np.int64)
    lhs = int(((z @ Ev @ N) ** 2).sum()); rhs = v * (r - s) * (k // 2 + s) * int(z @ Ev @ z)
    # a maximal coclique found greedily, same identity with z = its indicator
    C = []
    for x in rnd.sample(range(v), v):
        if not (adj[x] & set(C)): C.append(x)
    zc = np.zeros(v, dtype=np.int64); zc[C] = 1
    lhs2 = int(((zc @ Ev @ N) ** 2).sum()); rhs2 = v * (r - s) * (k // 2 + s) * int(zc @ Ev @ zc)
    mult_s = round(np.sum(np.abs(np.linalg.eigvalsh(A.astype(float)) - s) < 1e-6))
    print("%s: v=%d k=%d r=%d s=%d, %d lines; (1) entries %s; (2) G^2 = (r-s)(k/2+s) G: %s, rank %d (multiplicity of s: %d); (3) random z: %s; coclique of %d: %s" % (path.split("/")[-1], v, k, r, s, nl, ok1, ok2, rank, mult_s, lhs == rhs, len(C), lhs2 == rhs2))
