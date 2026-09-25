r"""X12 -- positivity of the hidden far projector (IDEES.md, X12).

Line L, ball N(L) (3 parts X_i), far set F, M = A[N(L), F], G = G(L), X = J/3 - A_G - I (A_F M^T = M^T X).
Visible part col(M^T): A_F acts as X.  Hidden part ker M: A_F = r Pi_r + s Pi_s.  Hence, exactly,
    A_F = B0 - (r - s) Pi_s,     B0 = r I + M^T Y M,     Y = (M M^T)^+ (X - r I)      (Y depends on G(L) only).
Diagonal:  Pi_s[w,w] = (r + y(N_w)) / (r - s),   Pi_r[w,w] = 1 - z(N_w) - Pi_s[w,w],
with y(N) = 1_N^T Y 1_N, z(N) = 1_N^T (M M^T)^+ 1_N for the 6-set N_w of ball neighbours of w.
Necessary: 0 <= Pi_s[w,w] and 0 <= Pi_r[w,w].  For 99 (r=3, s=-4, rank Pi_s = 8) every non-partner pair of each part
is the trace N_w cap X_i of exactly one far vertex, so every such pair needs an admissible completion.

Part 1 (BvLS, real): check the identity A_F = B0 - (r-s) Pi_s with the true projector (numerically).
Part 2 (99, random admissible balls): for each part and each non-partner pair, count admissible completions.
"""
import sys, os, random, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'c1_recherche', 'code'))
import graphs
import line_ball as lb


def ball_data(A):
    n = len(A)
    for u in range(n):
        for v in np.nonzero(A[u])[0]:
            if v > u:
                w = np.nonzero(A[u] & A[v])[0]
                if len(w) == 1:
                    L = [u, int(v), int(w[0])]
                    X = [[int(z) for z in np.nonzero(A[p])[0] if z not in L] for p in L]
                    N = X[0] + X[1] + X[2]
                    F = [z for z in range(n) if z not in L and z not in N]
                    return L, X, N, F
    raise ValueError


def ball_operators(AG, part_sizes, r):
    n = len(AG)
    I = np.eye(n); J = np.ones((n, n))
    BJ = np.zeros((n, n)); o = 0
    for s_ in part_sizes:
        BJ[o:o + s_, o:o + s_] = 1; o += s_
    k2 = AG.shape[0] // 3 * 0  # unused
    return I, J, BJ


def part1_bvls():
    A = graphs.bvls(); r, s = 4, -5
    L, X, N, F = ball_data(A)
    AG = A[np.ix_(N, N)].astype(float); M = A[np.ix_(N, F)].astype(float); AF = A[np.ix_(F, F)].astype(float)
    n = len(N); I = np.eye(n); J = np.ones((n, n))
    Xop = J / 3 - AG - I
    MMt = M @ M.T
    assert np.allclose(Xop @ MMt, MMt @ Xop)
    P = np.linalg.pinv(MMt, rcond=1e-9)
    Y = P @ (Xop - r * I)
    B0 = r * np.eye(len(F)) + M.T @ Y @ M
    Pis = (B0 - AF) / (r - s)
    ev = np.linalg.eigvalsh(Pis)
    rank = int(np.sum(ev > 0.5))
    print(f'[BvLS] Pi_s from the formula: idempotent err {np.abs(Pis @ Pis - Pis).max():.2e}, rank {rank}, '
          f'|M Pi_s| {np.abs(M @ Pis).max():.2e}, eigenvalues in [{ev.min():.3f}, {ev.max():.3f}]')
    Pir = np.eye(len(F)) - M.T @ P @ M - Pis
    print(f'        diag Pi_s in [{np.diag(Pis).min():.4f}, {np.diag(Pis).max():.4f}], '
          f'diag Pi_r in [{np.diag(Pir).min():.4f}, {np.diag(Pir).max():.4f}]')


def part2_99(seed=5, trials=200):
    rng = random.Random(seed)
    r, s = 3, -4
    I = np.eye(36); J = np.ones((36, 36))
    BJ = np.zeros((36, 36))
    for p in range(3):
        BJ[12 * p:12 * (p + 1), 12 * p:12 * (p + 1)] = 1
    summary = Counter(); worst = []
    for t in range(trials):
        ta, tb = lb.random_matching(rng), lb.random_matching(rng)
        perm = lb.others[:]; rng.shuffle(perm); sigma = {b: perm[i] for i, b in enumerate(lb.others)}
        if not lb.local_ok(ta, tb, sigma):
            continue
        G = lb.cubic_graph(ta, tb, sigma).astype(float)
        if lb.ncomp(G.astype(np.int64)) != 1:
            continue
        MMt = 12 * I + 2 * J - G - G @ G - BJ
        Xop = J / 3 - G - I
        P = np.linalg.pinv(MMt, rcond=1e-9)
        Y = P @ (Xop - r * I)
        # non-partner pairs in each part (partner = G-edge inside the part)
        pairs = []
        for p in range(3):
            idx = list(range(12 * p, 12 * (p + 1)))
            pairs.append([(i, j) for i, j in itertools.combinations(idx, 2) if G[i, j] == 0])
        # vectors: y(N) = sum over parts of 1_Pi^T Y 1_Pj ; precompute blocks
        V = [np.zeros((len(pairs[p]), 36)) for p in range(3)]
        for p in range(3):
            for m_, (i, j) in enumerate(pairs[p]):
                V[p][m_, i] = V[p][m_, j] = 1
        # quadratic forms q(N) = sum_{p,q} V_p Y V_q^T, broadcast over all triples
        def triple_values(Q):
            D = [np.einsum('ij,jk,ik->i', V[p], Q, V[p]) for p in range(3)]      # diagonal blocks
            C01 = V[0] @ Q @ V[1].T; C02 = V[0] @ Q @ V[2].T; C12 = V[1] @ Q @ V[2].T
            return (D[0][:, None, None] + D[1][None, :, None] + D[2][None, None, :]
                    + 2 * C01[:, :, None] + 2 * C02[:, None, :] + 2 * C12[None, :, :])
        yv = triple_values(Y); zv = triple_values(P)
        pis = (r + yv) / (r - s); pir = 1 - zv - pis
        ok = (pis >= -1e-9) & (pir >= -1e-9)
        c0 = ok.any(axis=(1, 2)).sum(); c1 = ok.any(axis=(0, 2)).sum(); c2 = ok.any(axis=(0, 1)).sum()
        frac = ok.mean()
        summary[(int(c0) == 60 and int(c1) == 60 and int(c2) == 60)] += 1
        worst.append((min(c0, c1, c2), frac))
    print(f'[99] connected admissible balls tested: {sum(summary.values())}; all pairs completable: {dict(summary)}')
    if worst:
        mins = sorted(worst)[:5]
        print(f'     fewest completable pairs in a part (5 worst balls): {[w[0] for w in mins]}; '
              f'admissible triple fraction: min {min(w[1] for w in worst):.4f}, max {max(w[1] for w in worst):.4f}')


if __name__ == '__main__':
    part1_bvls()
    part2_99(int(sys.argv[1]) if len(sys.argv) > 1 else 5, int(sys.argv[2]) if len(sys.argv) > 2 else 200)
