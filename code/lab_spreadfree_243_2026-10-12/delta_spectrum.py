"""Lab session, 2026-10-12. Differences Delta = A' - A between the stored graphs (same labelling): support F, rank and
spectrum of Delta, dimensions of the spaces of eigenvectors (4 and -5) supported in F, rank of A[R, F].
python -I delta_spectrum.py <directory srg243 with bvls243.edges, twin243_switched.edges, family/...>"""
import sys, itertools, collections
import numpy as np
def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 243; A = np.zeros((n, n))
    for a, b in E: A[a, b] = A[b, a] = 1
    return A
names = ["bvls243.edges", "twin243_switched.edges", "family/gamma3_aut864.edges", "family/gamma4_aut3888.edges"]
G = [load(sys.argv[1] + "/" + p) for p in names]
def eigsupp(A, F, ev):
    """dimension of the space of ev-eigenvectors of A supported in F"""
    n = len(A); R = [v for v in range(n) if v not in set(F)]
    w, U = np.linalg.eigh(A); B = U[:, np.abs(w - ev) < 1e-6]            # basis of the eigenspace
    s = np.linalg.svd(B[R, :], compute_uv=False)
    return B.shape[1] - int((s > 1e-8).sum())
for i, j in [(0, 1), (0, 3), (0, 2), (1, 3)]:
    A, A2 = G[i], G[j]; Dl = A2 - A
    F = [v for v in range(243) if np.abs(Dl[v]).any()]; R = [v for v in range(243) if v not in set(F)]
    w = np.linalg.eigvalsh(Dl); nz = w[np.abs(w) > 1e-7]
    spec = collections.Counter(np.round(nz, 4))
    print(names[i], "->", names[j], ": |F| =", len(F), " rank(Delta) =", len(nz), " spectrum of Delta:", sorted(spec.items()))
    print("    eigenvectors supported in F: eigenvalue 4:", eigsupp(A, F, 4), " eigenvalue -5:", eigsupp(A, F, -5), "; rank of A[R,F]:", np.linalg.matrix_rank(A[np.ix_(R, F)]) if R else 0)
    if R:
        fib = sorted({v // 3 for v in R}); print("    untouched: %d vertices in %d fibres; induced degrees in R: %s" % (len(R), len(fib), sorted(collections.Counter(int(A[v][R].sum()) for v in R).items())))
        # is R = N[L] for a fibre L ?
        for L0 in fib:
            L = [3 * L0, 3 * L0 + 1, 3 * L0 + 2]; NL = set(L) | {int(y) for x in L for y in np.nonzero(A[x])[0]}
            if NL == set(R): print("    R = closed neighbourhood of the fibre", L)
    dch = collections.Counter(int((Dl[v] > 0).sum()) for v in F); print("    changed pairs per vertex (added): ", sorted(dch.items()))
