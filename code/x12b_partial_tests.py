r"""X12b -- Rayleigh certificates on (ball + far vertices with known boundary sets), using the hidden projector.

For a subset F' of far vertices with known 6-sets N_w (ball neighbours):
   B0[w,w'] = r*delta + 1_{N_w}^T Y 1_{N_w'},  Y = (MM^T)^+ (X - rI),  and  A_F' <= B0[F',F']   (Pi_s >= 0)
   B1 = B0 - (r-s) Pi_ker,  Pi_ker[w,w'] = delta - 1_{N_w}^T (MM^T)^+ 1_{N_w'},  and  A_F' >= B1[F',F']   (Pi_r >= 0)
Necessary:  lambda_min( [[A_B, M_F'], [M_F'^T, B0]] ) >= s   and   lambda_max on sum-zero( [[A_B, M_F'], [., B1]] ) <= r.
(MM^T, X, Y depend on the ball only.)
Checks: BvLS with the true boundary sets (must pass) and with scrambled boundary sets (negative control, should fail).
"""
import sys, os, random
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'c1_recherche', 'code'))
import graphs


def ball_setup(A):
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
                    return L, N, F
    raise ValueError


def operators(AG, r):
    n = len(AG); I = np.eye(n); J = np.ones((n, n))
    part = n // 3
    BJ = np.zeros((n, n))
    for p in range(3):
        BJ[part * p:part * (p + 1), part * p:part * (p + 1)] = 1
    k = part + 2
    MMt = (k - 2) * I + 2 * J - AG - AG @ AG - BJ
    Xop = J / 3 - AG - I
    P = np.linalg.pinv(MMt, rcond=1e-9)
    return MMt, Xop, P, P @ (Xop - r * I)


def tests(A_B, Mcols, P, Y, r, s):
    """A_B: ball adjacency (L then N(L)); Mcols: list of 0/1 vectors on N(L) (one per known far vertex)."""
    nB = len(A_B); m = len(Mcols); nN = Mcols[0].shape[0] if m else 0
    Mfull = np.zeros((nB, m))
    for j, c in enumerate(Mcols):
        Mfull[nB - nN:, j] = c
    Cm = np.array(Mcols).T                              # nN x m
    B0 = r * np.eye(m) + Cm.T @ Y @ Cm
    Pker = np.eye(m) - Cm.T @ P @ Cm
    B1 = B0 - (r - s) * Pker
    Ahat = np.block([[A_B, Mfull], [Mfull.T, B0]])
    Atil = np.block([[A_B, Mfull], [Mfull.T, B1]])
    lmin = np.linalg.eigvalsh(Ahat).min()
    tot = nB + m
    Q = np.eye(tot) - np.ones((tot, tot)) / tot         # projector on sum-zero vectors
    lmax = np.linalg.eigvalsh(Q @ Atil @ Q).max()
    return lmin, lmax


def bvls_check(seed=1):
    A = graphs.bvls(); r, s = 4, -5
    L, N, F = ball_setup(A)
    B = L + N
    A_B = A[np.ix_(B, B)].astype(float)
    AG = A[np.ix_(N, N)].astype(float)
    MMt, Xop, P, Y = operators(AG, r)
    Mtrue = [A[np.ix_(N, [w])].astype(float)[:, 0] for w in F]
    rng = random.Random(seed)
    sub = rng.sample(range(len(F)), 40)
    lmin, lmax = tests(A_B, [Mtrue[i] for i in sub], P, Y, r, s)
    print(f'[BvLS true boundary sets, 40 far vertices] lambda_min(Ahat) = {lmin:.4f} (>= {s}),  '
          f'lambda_max(Atil | sum-zero) = {lmax:.4f} (<= {r})')
    # negative control: scramble the part-0 pairs among the chosen far vertices
    bad = 0
    for t in range(20):
        cols = [Mtrue[i].copy() for i in sub]
        part = len(N) // 3
        p0 = [c[:part].copy() for c in cols]
        rng.shuffle(p0)
        for c, q in zip(cols, p0):
            c[:part] = q
        lmin2, lmax2 = tests(A_B, cols, P, Y, r, s)
        bad += (lmin2 < s - 1e-7) or (lmax2 > r + 1e-7)
    print(f'[BvLS scrambled part-0 pairs] certificate fires in {bad}/20 trials')


if __name__ == '__main__':
    bvls_check()
