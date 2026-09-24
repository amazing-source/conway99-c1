"""F1 x F13: the induced subgraph on l U Gamma_1(l) (39 vertices) around a line l = {x, a, abar}.
Data (up to relabelling): M1 = tau_a (pulled back to P0 = N(x) - l), M2 = tau_abar (pulled back along the
x -> abar shadow), pi = line holonomy rho_l. M0 = mate matching (0,1),(2,3),...
Checks: local validity (lambda <= 1, mu <= 2 inside the 39 vertices), interlacing lambda_2 <= 3 and
lambda_min >= -4, and zero-sum eigenvectors for 3 / -4 (which must extend by zero to Gamma).
"""
import itertools, random, sys
import numpy as np

M0 = {i: i ^ 1 for i in range(12)}


def build(M1, M2, pi):
    # vertices: 0 = x, 1 = a, 2 = abar, 3..14 = p_i, 15..26 = q_i, 27..38 = r_i
    P = lambda i: 3 + i
    Q = lambda i: 15 + i
    R = lambda i: 27 + i
    A = np.zeros((39, 39), dtype=np.int64)

    def e(u, v):
        A[u, v] = A[v, u] = 1
    e(0, 1); e(0, 2); e(1, 2)
    for i in range(12):
        e(0, P(i)); e(1, Q(i)); e(2, R(i))
        e(P(i), Q(i)); e(P(i), R(i)); e(Q(i), R(pi[i]))
        if M0[i] > i:
            e(P(i), P(M0[i]))
        if M1[i] > i:
            e(Q(i), Q(M1[i]))
        if M2[i] > i:
            e(R(i), R(M2[i]))
    return A


def locally_valid(A):
    A2 = A @ A
    n = len(A)
    off = ~np.eye(n, dtype=bool)
    if (A2[(A == 1) & off] > 1).any():
        return False
    if (A2[(A == 0) & off] > 2).any():
        return False
    # also: degree-2 in l points ok; no K4 automatically
    return True


def random_matching(rng):
    idx = list(range(12))
    rng.shuffle(idx)
    M = {}
    for k in range(0, 12, 2):
        M[idx[k]], M[idx[k + 1]] = idx[k + 1], idx[k]
    return M


def zero_sum_mult(A, theta):
    K = np.vstack([A - theta * np.eye(len(A)), np.ones((1, len(A)))])
    return len(A) - np.linalg.matrix_rank(K, tol=1e-8)


def cycle_type(p):
    seen, ct = set(), []
    for i in p:
        if i in seen:
            continue
        L, j = 0, i
        while j not in seen:
            seen.add(j); j = p[j]; L += 1
        ct.append(L)
    return tuple(sorted(ct, reverse=True))


def main(samples=20000, seed=1):
    rng = random.Random(seed)
    # grid-full reference
    A = build(M0, M0, {i: i for i in range(12)})
    ev = np.linalg.eigvalsh(A.astype(float))
    print('grid-full reference: valid', locally_valid(A), 'lambda_2 = %.4f lambda_min = %.4f' % (ev[-2], ev[0]),
          'zero-sum mult(3) =', zero_sum_mult(A, 3), 'mult(-4) =', zero_sum_mult(A, -4))
    stats = {}
    viol = 0
    nvalid = 0
    for s in range(samples):
        M1, M2 = random_matching(rng), random_matching(rng)
        perm = list(range(12)); rng.shuffle(perm)
        pi = dict(enumerate(perm))
        A = build(M1, M2, pi)
        if not locally_valid(A):
            continue
        nvalid += 1
        ev = np.linalg.eigvalsh(A.astype(float))
        bad = ev[-2] > 3 + 1e-9 or ev[0] < -4 - 1e-9
        viol += bad
        key = cycle_type(pi)
        st = stats.setdefault(key, [0, 0])
        st[0] += 1; st[1] += bad
    print(f'random samples: {samples}, locally valid: {nvalid}, interlacing violations: {viol}')
    for k, (c, b) in sorted(stats.items(), key=lambda kv: -kv[1][0])[:15]:
        print('  holonomy type', k, 'count', c, 'violations', b)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20000)
