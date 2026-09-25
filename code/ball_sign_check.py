"""notes/102, L23: sign of the 39-point line ball.  Q = A - 3I + 3J restricted to the ball L + N(L) (mod 7).
Predictions (hand proof): rank Q_ball = 37 - d(L); if d(L) = 1, Legendre(disc of its nondegenerate part) =
(tau(G(L)) | 7), tau = number of spanning trees of the cubic graph G(L); the two-star block S24 of M_x has the same
rank - 14 = 23 - d and the same Legendre symbol.  At k = 22 the extremal block must be split for M_x (Legendre -1)."""
import sys, random
import numpy as np
import line_ball as lb
from beta_form_check import rank_leg

p = 7


def det_mod(M, q=p):
    M = [[x % q for x in row] for row in M]; n = len(M); d = 1
    for c in range(n):
        r = next((i for i in range(c, n) if M[i][c]), None)
        if r is None:
            return 0
        if r != c:
            M[c], M[r] = M[r], M[c]; d = -d
        d = d * M[c][c] % q; iv = pow(M[c][c], -1, q)
        for i in range(c + 1, n):
            f = M[i][c] * iv % q
            if f:
                M[i] = [(a - f * b) % q for a, b in zip(M[i], M[c])]
    return d % q


def leg(x):
    x %= p
    return 0 if x == 0 else (1 if pow(x, (p - 1) // 2, p) == 1 else -1)


rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
bad_rank = bad_sign = bad24 = n1 = 0; seen = {}
for _ in range(trials):
    ta, tb = lb.random_matching(rng), lb.random_matching(rng)
    perm = lb.others[:]; rng.shuffle(perm); sigma = {b: perm[i] for i, b in enumerate(lb.others)}
    G = lb.cubic_graph(ta, tb, sigma)
    d = 36 - lb.rank_mod(G - 3 * np.eye(36, dtype=np.int64))
    Aball = lb.full_ball(ta, tb, sigma) + 3 * np.eye(39, dtype=np.int64)
    Q = (Aball - 3 * np.eye(39, dtype=np.int64) + 3) % p
    rq, lq = rank_leg(Q.tolist(), p)
    r24, l24 = rank_leg(lb.two_star_block(ta, tb, sigma).tolist(), p)
    bad_rank += (rq != 37 - d) or (r24 != 23 - d)
    ok = lb.local_ok(ta, tb, sigma)
    if d == 1:
        n1 += 1
        Lap = 3 * np.eye(36, dtype=np.int64) - G
        t = leg(det_mod(Lap[1:, 1:].tolist()))
        bad_sign += (lq != t); bad24 += (l24 != t)
        seen[(t, ok)] = seen.get((t, ok), 0) + 1
print(f'trials {trials}: rank failures {bad_rank}; d=1 cases {n1}: sign(Q_ball) != (tau|7): {bad_sign}, '
      f'sign(S24) != (tau|7): {bad24};  (tau|7, admissible) counts: {seen}')
