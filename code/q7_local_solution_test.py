"""q:7 tests on a LOCAL solution (mu, tau, Phi) of C2's compact free-star problem at a block c (notes/129, notes/131).
Labels 0..11: block i//2 (blocks 0..5 of X_c), sign + if i even, sigma(i) = i^1.  C2's letters: mu = mates in star(c+)
(my tau_c), tau: e_c+b ~ -(e_c+tau b) (my eta_c).  Far roots = 2-subsets of labels in different blocks (60).
Input JSON: {"mu": [12], "tau": [12], "Phi": {"a,b": [p, q], ...}} (a < b).
Output: checks of (i)-(iii); t_c = dim ker Q_c, chi(det Q_c); mod-7 far matrix Z (T_FF = Z + R_c, rank R_c = g - 18);
real residues |r_f|^2 = 3 - (Z_R)_ff; for g = 18: test T_FF == Z entries in {0,+-1}, zero diagonal;
for g = 20 with det square: backtracking search of K (k_f in F7^2, r = I2) with k_f.k_f = -Z_ff, Z_ff' + k_f.k_f' in {0,+-1},
sum k_f k_f^T = 0, X K = 0."""
import sys, json, itertools
import numpy as np
from fractions import Fraction

P7 = 7
SQ = {1, 2, 4}


def sgn(i):
    return 1 if i % 2 == 0 else -1


def load(path):
    d = json.load(open(path))
    mu, tau = d['mu'], d['tau']
    Phi = {}
    for k, v in d['Phi'].items():
        a, b = map(int, k.split(','))
        Phi[frozenset((a, b))] = frozenset(v)
    return mu, tau, Phi


def check_rsf(mu, tau, Phi):
    s = lambda x: x ^ 1
    far = [frozenset((a, b)) for a in range(12) for b in range(a + 1, 12) if a // 2 != b // 2]
    assert len(far) == 60 and set(Phi) == set(far)
    nonmu = {frozenset((a, b)) for a in range(12) for b in range(a + 1, 12) if mu[a] != b}
    ok_i = sorted(map(sorted, Phi.values())) == sorted(map(sorted, nonmu))
    bad_ii = 0
    for a in range(12):
        for b in range(12):
            cnt = sum(1 for z in far if a in z and b in Phi[z])
            tgt = (1 - (tau[a] == s(a))) if a == b else 2 - (b == s(a)) - (b == mu[a]) - (b == tau[s(a)])
            bad_ii += cnt != tgt
    bad_iii = 0
    for b in range(12):
        for dd in range(12):
            cnt = sum(1 for z in far if b in Phi[z] and dd in Phi[frozenset(s(x) for x in z)])
            tgt = 2 - (dd == s(b)) - (dd == tau[mu[b]]) - (dd == mu[tau[b]]) - (dd == tau[b])
            bad_iii += cnt != tgt
    return ok_i, bad_ii, bad_iii, far


def rank_mod(M, p=P7):
    M = [list(map(int, r)) for r in M]
    n, m = len(M), len(M[0])
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c] % p, p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


def solve_mod(A, B, p=P7):
    """solve A Y = B mod p (A square, possibly singular but B in its range); returns one solution."""
    n = len(A)
    M = [list(map(int, A[i])) + list(map(int, B[i])) for i in range(n)]
    m = len(A[0])
    piv_cols = []
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c] % p, p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv_cols.append(c)
        r += 1
    for i in range(r, n):
        assert all(x % p == 0 for x in M[i][m:]), 'B not in range'
    Y = [[0] * len(B[0]) for _ in range(m)]
    for i, c in enumerate(piv_cols):
        Y[c] = M[i][m:]
    return np.array(Y) % p


def det_mod(M, p=P7):
    M = [list(map(int, r)) for r in M]
    n = len(M)
    d = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] % p), None)
        if piv is None:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d = d * M[c][c] % p
        inv = pow(M[c][c] % p, p - 2, p)
        for i in range(c + 1, n):
            if M[i][c] % p:
                f = M[i][c] * inv % p
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[c])]
    return d % p


def analyse(mu, tau, Phi, far, kmax_nodes=2_000_000):
    s = lambda x: x ^ 1
    # far orbits with representatives (rep = root containing the smaller label with + sign if possible)
    orbs = []
    seen = set()
    for z in far:
        if z in seen:
            continue
        sz = frozenset(s(x) for x in z)
        seen |= {z, sz}
        rep = z if min(z) % 2 == 0 else sz
        orbs.append(rep)
    assert len(orbs) == 30
    # block coordinates: 0 = c, 1..6 = blocks of X
    Bnear = np.zeros((7, 12), int)
    for b in range(12):
        Bnear[0, b] = 1
        Bnear[1 + b // 2, b] = sgn(b)
    Bfar = np.zeros((7, 30), int)
    for j, z in enumerate(orbs):
        for x in z:
            Bfar[1 + x // 2, j] = sgn(x)
    Tnear = np.array([[int(mu[b] == bb) - int(tau[b] == bb) for bb in range(12)] for b in range(12)])
    S = np.zeros((12, 30), int)          # shadows: T_{o_b, f}
    for j, z in enumerate(orbs):
        sz = frozenset(s(x) for x in z)
        for b in range(12):
            S[b, j] = int(b in Phi[z]) - int(b in Phi[sz])
    # odd ball: blocks (7) + near orbits (12)
    Sball = np.block([[-np.eye(7, dtype=int), Bnear], [Bnear.T, Tnear]])
    Nball = (Sball - 3 * np.eye(19, dtype=int)) % P7
    Xf = np.vstack([Bfar, S])            # 19 x 30 (off-diagonal part of S between ball and far)
    rk = rank_mod(Nball)
    Qc = (np.array([[int(mu[b] == bb) - int(tau[b] == bb) - 2 * int(bb == s(b)) - int(b == bb) for bb in range(12)]
                    for b in range(12)]))
    tc = 12 - rank_mod(Qc % P7)
    dq = det_mod(Qc % P7)
    chi = 0 if dq == 0 else (1 if dq in SQ else -1)
    print('ball rank mod 7 =', rk, ' t_c =', tc, ' det Q_c mod 7 =', dq, ' chi =', chi)
    # possible g: 18 + t - 2 r0 + rho
    if tc == 0:
        Y = solve_mod(Nball, Xf % P7)
        Z = (3 * np.eye(30, dtype=int) + Xf.T @ Y) % P7
        # (sign convention: T_FF - 3I - X^T P^+ X = R_c  =>  T_FF = R_c + 3I + X^T P^+ X)
        diag = [int(Z[j, j]) for j in range(30)]
        print('Z_ff mod 7 (should be 0 for all f at g = 18):', diag)
        off_ok = sum(1 for i in range(30) for j in range(i + 1, 30) if Z[i, j] % 7 in (0, 1, 6))
        print('g=18 test: zero diagonal', all(d == 0 for d in diag), '; off-diagonal entries in {0,+-1}:', off_ok, '/ 435')
    # real residues
    BG = np.block([[4 * np.eye(7), -Bnear.astype(float)], [-Bnear.T.astype(float), 3 * np.eye(12) - Tnear]])
    Xr = -Xf.astype(float)
    ZR = Xr.T @ np.linalg.pinv(BG) @ Xr
    r2 = 3 - np.diag(ZR)
    print('real residues |r_f|^2: min %.4f  max %.4f  sum %.4f (must be >= 0, sum 28)' % (r2.min(), r2.max(), r2.sum()))
    print('   values:', sorted(np.round(r2, 4)))
    if tc == 0 and chi == 1:
        # g- = 20 forced; search K with r = I2
        search_K(Z, Xf % P7, kmax_nodes)
    return


def search_K(Z, X, kmax):
    vecs = {n: [] for n in range(7)}
    for x in range(7):
        for y in range(7):
            vecs[(x * x + y * y) % 7].append((x, y))
    need = [(-int(Z[f, f])) % 7 for f in range(30)]
    order = sorted(range(30), key=lambda f: len(vecs[need[f]]))
    print('K search: norm targets', need, ' zero-forced k_f:', sum(1 for n in need if n == 0))
    K = [None] * 30
    nodes = [0]
    sols = [0]

    def consistent(f):
        kf = K[f]
        for g in range(30):
            if g == f or K[g] is None:
                continue
            dot = (kf[0] * K[g][0] + kf[1] * K[g][1]) % 7
            if (int(Z[f, g]) + dot) % 7 not in (0, 1, 6):
                return False
        return True

    def final_ok():
        A = np.array(K)
        if np.any((A.T @ A) % 7):
            return False
        if np.any((X @ A) % 7):
            return False
        return True

    def rec(i):
        if nodes[0] > kmax:
            return
        if i == 30:
            if final_ok():
                sols[0] += 1
            return
        f = order[i]
        for v in vecs[need[f]]:
            nodes[0] += 1
            K[f] = v
            if consistent(f):
                rec(i + 1)
                if sols[0]:
                    return
            K[f] = None
    rec(0)
    print('K search: nodes', nodes[0], 'solutions found', sols[0], '(limit %d)' % kmax)


if __name__ == '__main__':
    mu, tau, Phi = load(sys.argv[1])
    ok_i, bii, biii, far = check_rsf(mu, tau, Phi)
    print('(i) ok:', ok_i, ' (ii) violations:', bii, ' (iii) violations:', biii)
    analyse(mu, tau, Phi, far)
