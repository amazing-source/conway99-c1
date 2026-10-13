"""Lab session, 2026-10-13. Microscope for the statement "no alternating square" (l = 2 never occurs).
l = 2 at the edge x~a means: two lines through x and two lines through a (other than the line x a) such that each of
the four cross pairs of lines is joined by exactly 2 edges. Here the same pattern is counted for ANY two points x, y:
two lines through x, two lines through y, the four cross pairs disjoint and joined by exactly j edges, for j = 0..3,
split by x ~ y / x not adjacent to y. Also printed: the distribution of j over pairs of disjoint lines.
python square_pattern.py <edge file> ...     One process, about 300 MB, under a minute per graph."""
import sys, itertools, collections
import numpy as np
def run(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]; n = 1 + max(max(e) for e in E)
    A = np.zeros((n, n), dtype=np.int32)
    for a, b in E: A[a, b] = A[b, a] = 1
    lines = sorted({tuple(sorted((a, b, int(np.nonzero(A[a] & A[b])[0][0])))) for a, b in E}); nl = len(lines)
    N = np.zeros((nl, n), dtype=np.int32)
    for i, L in enumerate(lines): N[i, list(L)] = 1
    J = N @ A @ N.T; meet = (N @ N.T) > 0
    print("%s: %d lines; edges between two disjoint lines: %s" % (path.replace("\\", "/").split("/")[-1], nl, dict(sorted(collections.Counter(J[~meet].tolist()).items()))))
    thru = [np.nonzero(N[:, x])[0] for x in range(n)]
    for j in range(4):
        P = ((J == j) & ~meet).astype(np.int32); adj_cnt = 0; non_cnt = 0
        for x in range(n):
            for l1, l2 in itertools.combinations(thru[x], 2):
                S = P[l1] & P[l2]; c = S @ N; pairs = c * (c - 1) // 2
                adj_cnt += int(pairs[A[x] == 1].sum()); non_cnt += int(pairs[A[x] == 0].sum())
        print("   all four cross pairs joined by exactly %d edges: %d with x ~ y, %d with x not adjacent to y (each counted twice)" % (j, adj_cnt, non_cnt), flush=True)
for p in sys.argv[1:]: run(p)
