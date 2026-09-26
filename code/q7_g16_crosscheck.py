"""Independent re-implementation of the unary q:7 filters of q7_g16_test.py, at the 12-label level (closed form):
  after eliminating the 7 block coordinates of the ball (1/(-4) = 5 mod 7), the star Schur complement is Q_c + 2J and a far
  column x_f = (b_f, s_f) reduces to s~_f = s_f + 2 delta_f, delta_f = sum over the labels (d, eps) of f of eps (e_{d+} - e_{d-});
  so Z_ff = 5 |b_f|^2 + 3 + s~_f^T G s~_f = 13 + s~^T G s~ (G a generalized inverse of Q_c + 2J), and balance = s~_f . phi = 0
  for phi in ker(Q_c + 2J).
Compares, class by class, the per-orbit numbers of surviving options with q7_g16_test.unary_filter; then checks invariance of
the counts (as multisets) under random relabelings g in Aut(X, pi)."""
import itertools, json, random, sys
import numpy as np
from q7_g16_test import (classes_t_ge, unary_filter, K2, FAR, L, PI, P7, G, conj, kernel_mod, rank_mod, inv_mod)


def ginv_any(M):
    """generalized inverse of a symmetric matrix mod 7: brute-force a nonsingular principal submatrix of maximal size."""
    n = len(M)
    r = rank_mod(M.tolist())
    for T in itertools.combinations(range(n), r):
        sub = M[np.ix_(T, T)]
        if rank_mod(sub.tolist()) == r:
            Gi = np.zeros((n, n), dtype=np.int64)
            Gi[np.ix_(T, T)] = inv_mod(sub.tolist())
            assert np.array_equal((M @ Gi @ M) % P7, M % P7)
            return Gi
    raise RuntimeError


def counts_closed_form(tau, eta, t2=True):
    Q = np.zeros((12, 12), dtype=np.int64)
    for l in L:
        Q[l, tau[l]] += 1
        Q[l, eta[l]] -= 1
        Q[l, PI[l]] -= 2
        Q[l, l] -= 1
    M = (Q + 2) % P7                      # Q + 2J
    Gi = ginv_any(M)
    ker = kernel_mod(M.tolist())
    k2 = K2(tau, eta)
    nonmu = [e for e in itertools.combinations(L, 2) if tau[e[0]] != e[1]]
    counts = []
    for (z, sz) in FAR:
        delta = np.zeros(12, dtype=np.int64)
        for a in z:
            d = a // 2
            eps = 1 if a % 2 == 0 else -1
            delta[2 * d] += eps
            delta[2 * d + 1] -= eps
        ok1 = [e for e in nonmu if all(k2[a, b] > 0 for a in z for b in e)]
        ok2 = [e for e in nonmu if all(k2[a, b] > 0 for a in sz for b in e)]
        c = 0
        for e in ok1:
            for e2 in ok2:
                if e == e2:
                    continue
                s = np.zeros(12, dtype=np.int64)
                for l in e:
                    s[l] += 1
                for l in e2:
                    s[l] -= 1
                st = (s + 2 * delta) % P7
                if np.any((ker @ st) % P7):
                    continue
                if t2 and (13 + int(st @ ((Gi @ st) % P7))) % P7 != 0:
                    continue
                c += 1
        counts.append(c)
    return counts


if __name__ == '__main__':
    random.seed(7)
    cls = classes_t_ge(2)
    mism = 0
    for (tau, eta, t, osz) in cls:
        a = counts_closed_form(tau, eta, t2=(t == 2))
        _, res, _ = unary_filter(tau, eta, regime_t2=(t == 2))
        b = [len(r[0]) for r in res]
        if a != b:
            mism += 1
            print('MISMATCH', t, tau, eta, a, b)
    print('classes compared:', len(cls), 'mismatches:', mism, flush=True)
    # invariance under relabeling (as multisets of per-orbit counts), on 20 random (class, g)
    bad = 0
    for _ in range(20):
        tau, eta, t, osz = random.choice(cls)
        g = random.choice(G)
        tau2, eta2 = conj(tau, g), conj(eta, g)
        c1 = sorted(len(r[0]) for r in unary_filter(tau, eta, regime_t2=(t == 2))[1])
        c2 = sorted(len(r[0]) for r in unary_filter(tau2, eta2, regime_t2=(t == 2))[1])
        if c1 != c2:
            bad += 1
            print('NOT INVARIANT', tau, eta, g)
    print('relabeling invariance failures:', bad, 'of 20')
