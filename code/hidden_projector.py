r"""Hidden-projector bounds for the far set of a line (X12), with exact rational certificates.

Setting (srg(v,k,1,2), eigenvalues r > s, line L, ball B = L + N(L), N(L) = 3 parts of size k-2, far set F):
  M = A[N(L), F],  X = J/3 - A_G - I,  M M^T = (k-2)I + 2J - A_G - A_G^2 - B_J  (ball only),
  Y = (M M^T)^+ (X - rI)   [for 99: Y = (A_G - 3I)^{-1} on U^perp, 1/12 on 1_N, 0 on sum-zero part indicators],
  B0 = rI + M^T Y M,  Pker = I - M^T (MM^T)^+ M,  B1 = B0 - (r-s) Pker,
  A_F = B0 - (r-s) Pi_s = B1 + (r-s) Pi_r   =>   B1 <= A_F <= B0   (no far-far edge needed).
For far vertices F' with known ball-neighbour sets N_w (columns of M), necessary conditions:
  (i)  Pi_s[w,w] = B0[w,w]/(r-s) >= 0,  Pi_r[w,w] = -B1[w,w]/(r-s) >= 0          (A_F[w,w] = 0 exactly);
  (ii) lambda_min(Ahat) >= s,  Ahat = [[A_B, M'], [M'^T, B0[F',F']]];
  (iii) q^T Atil q <= r ||q||^2 for sum-zero q,  Atil = [[A_B, M'], [M'^T, B1[F',F']]].
API:
  ops = BallOps(A_ball, r, s)                    # A_ball: adjacency on L + N(L) in that order (3 + 3(k-2) vertices)
  ops.test(Ncols)        -> dict(lmin, lmax, diag_ok, q_min, q_max)   (float, for search)
  ops.certify(Ncols, q, kind)  -> exact Fraction value of the violated quadratic form (None if not violated)
"""
from fractions import Fraction as Fr
import numpy as np


def _inv_exact(Mat):
    n = len(Mat)
    A = [[Fr(x) for x in row] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(Mat)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        A[c] = [x / piv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return [row[n:] for row in A]


class BallOps:
    def __init__(self, A_ball, r, s):
        A_ball = np.asarray(A_ball)
        self.r, self.s = r, s
        self.nB = len(A_ball)
        self.AB = A_ball.astype(float)
        nN = self.nB - 3
        self.nN = nN; part = nN // 3; k = part + 2
        AG = A_ball[3:, 3:].astype(np.int64)
        I = np.eye(nN, dtype=np.int64); J = np.ones((nN, nN), dtype=np.int64)
        BJ = np.zeros((nN, nN), dtype=np.int64)
        for p in range(3):
            BJ[part * p:part * (p + 1), part * p:part * (p + 1)] = 1
        MMt = (k - 2) * I + 2 * J - AG - AG @ AG - BJ
        # exact pseudo-inverse: (MM^T)^+ = (MM^T + Pi0)^{-1} - Pi0, Pi0 = projection on sum-zero part indicators
        Pi0 = [[Fr(int(BJ[i, j]), part) - Fr(1, nN) for j in range(nN)] for i in range(nN)]
        Mplus = _inv_exact([[Fr(int(MMt[i, j])) + Pi0[i][j] for j in range(nN)] for i in range(nN)])
        self.P = [[Mplus[i][j] - Pi0[i][j] for j in range(nN)] for i in range(nN)]
        Xm = [[Fr(1, 3) - int(AG[i, j]) - int(i == j) - r * int(i == j) for j in range(nN)] for i in range(nN)]
        self.Y = [[sum(self.P[i][t] * Xm[t][j] for t in range(nN)) for j in range(nN)] for i in range(nN)]
        self.Pf = np.array([[float(x) for x in row] for row in self.P])
        self.Yf = np.array([[float(x) for x in row] for row in self.Y])

    def _blocks(self, Ncols, exact=False):
        C = [list(map(int, c)) for c in Ncols]
        m = len(C)
        if exact:
            def bil(Mt, a, b):
                return sum(Mt[i][j] for i in range(self.nN) if a[i] for j in range(self.nN) if b[j])
            B0 = [[self.r * int(i == j) + bil(self.Y, C[i], C[j]) for j in range(m)] for i in range(m)]
            Pk = [[int(i == j) - bil(self.P, C[i], C[j]) for j in range(m)] for i in range(m)]
            B1 = [[B0[i][j] - (self.r - self.s) * Pk[i][j] for j in range(m)] for i in range(m)]
            return C, B0, B1
        Cm = np.array(C, dtype=float).T
        B0 = self.r * np.eye(m) + Cm.T @ self.Yf @ Cm
        B1 = B0 - (self.r - self.s) * (np.eye(m) - Cm.T @ self.Pf @ Cm)
        return C, B0, B1

    def _bordered(self, C, D):
        m = len(C)
        Mfull = np.zeros((self.nB, m))
        for j, c in enumerate(C):
            Mfull[3:, j] = c
        return np.block([[self.AB, Mfull], [Mfull.T, np.asarray(D, dtype=float)]])

    def test(self, Ncols):
        C, B0, B1 = self._blocks(Ncols)
        Ah, At = self._bordered(C, B0), self._bordered(C, B1)
        ev, V = np.linalg.eigh(Ah)
        tot = len(Ah); Q = np.eye(tot) - np.ones((tot, tot)) / tot
        ev2, V2 = np.linalg.eigh(Q @ At @ Q)
        diag_ok = bool(np.all(np.diag(B0) >= -1e-9) and np.all(np.diag(B1) <= 1e-9))
        return dict(lmin=ev[0], lmax=ev2[-1], diag_ok=diag_ok, q_min=V[:, 0], q_max=V2[:, -1])

    def certify(self, Ncols, q, kind, denom=10 ** 6):
        """Exact check with rationalised q. kind='min': returns q^T Ahat q - s||q||^2 if < 0;
        kind='max': makes q sum-zero and returns q^T Atil q - r||q||^2 if > 0.  Otherwise None."""
        C, B0, B1 = self._blocks(Ncols, exact=True)
        qq = [Fr(int(round(x * denom)), denom) for x in q]
        if kind == 'max':
            mean = sum(qq) / len(qq); qq = [x - mean for x in qq]
        D = B0 if kind == 'min' else B1
        nB, m = self.nB, len(C)
        def entry(i, j):
            if i < nB and j < nB:
                return Fr(int(self.AB[i, j]))
            if i < nB <= j:
                return Fr(C[j - nB][i - 3]) if i >= 3 else Fr(0)
            if j < nB <= i:
                return Fr(C[i - nB][j - 3]) if j >= 3 else Fr(0)
            return D[i - nB][j - nB]
        tot = nB + m
        val = sum(qq[i] * entry(i, j) * qq[j] for i in range(tot) if qq[i] for j in range(tot) if qq[j])
        nrm = sum(x * x for x in qq)
        g = val - (self.s if kind == 'min' else self.r) * nrm
        if (kind == 'min' and g < 0) or (kind == 'max' and g > 0):
            return g
        return None
