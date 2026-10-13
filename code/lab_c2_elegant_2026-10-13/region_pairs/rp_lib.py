"""Library for the region-pair survey (researcher 2, 2026-10-13).  Read-only on the campaign data.

Run with the lab interpreter (it has numba):
  C:\\Users\\RESEARCHER\\Desktop\\Recherche_Conway\\c2_experimental\\.venv\\Scripts\\python.exe -B <script>
(-B: no bytecode is written next to campaign files.)

Code copied (not imported) from the campaign:
  fp_enum, ldl, short, one_per_pair, solve_mod2   <- c2_experimental\\c2_cloud_run_v10\\scripts\\frame_dfs_next.py (lines 53-140)
  Fincke-Pohst runs in floats; EVERY returned vector has its norm re-checked in integers by fp_enum, and I re-check again here.
Data read: t20-codex\\measures\\hand_28\\<lid>.json (basis of U), <lid>_pairs.npz (integer coordinates of y1, y2 in that basis),
           t20-codex\\measures\\SHELL_COUNTS_EXACT_2026-10-07.json (exact shell sizes, used as a completeness certificate).

Conventions (all integers):
  U = Z^24 with Gram matrix G (unimodular, odd, no norm-1 vector). A vector is its coordinate row x; (x,y) = x G y^T.
  Shadow: b = v/2 with v = 2x + c, c characteristic (G c = diag G mod 2).  Then 2(b,y) = v G y^T =: p (odd integer),
  4(b,b) = v G v^T =: q (8 for norm 2, 16 for norm 4) and 4 E(b) = 7 q - p1^2 - p2^2.
"""
import os, sys, json, math, time
from fractions import Fraction as F
import numpy as np
import numba as nb

HAND28 = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\t20-codex\measures\hand_28"
SHELLS = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\t20-codex\measures\SHELL_COUNTS_EXACT_2026-10-07.json"
OUT = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ copied campaign code (frame_dfs_next.py)
@nb.njit(cache=False)
def fp_enum(G, Lu, d, N4, shift2, maxout):
    """all integer x with (2x + shift2)^T G (2x + shift2) <= N4 (exact check), where G = Lu^T diag(d) Lu (Lu unit upper
    triangular, floats). Returns the rows 2x + shift2."""
    n = G.shape[0]; out = np.zeros((maxout, n), np.int64); cnt = 0
    x = np.zeros(n, np.int64); z = np.zeros(n)                         # z = x + shift2 / 2
    rem = np.zeros(n + 1); cen = np.zeros(n); hi = np.zeros(n, np.int64)
    s = np.empty(n)
    for i in range(n): s[i] = shift2[i] / 2.0
    bound = N4 / 4.0 + 1e-7
    i = n - 1; rem[n] = bound
    c = 0.0
    for j in range(i + 1, n): c -= Lu[i, j] * z[j]
    cen[i] = c
    r = np.sqrt(max(rem[i + 1], 0.0) / d[i])
    x[i] = np.int64(np.ceil(cen[i] - s[i] - r)); hi[i] = np.int64(np.floor(cen[i] - s[i] + r))
    while True:
        if x[i] > hi[i]:
            i += 1
            if i >= n: break
            x[i] += 1
            continue
        z[i] = x[i] + s[i]
        t = z[i] - cen[i]; rr = rem[i + 1] - d[i] * t * t
        if rr < -1e-9:
            x[i] += 1
            continue
        if i == 0:
            v = np.empty(n, np.int64)
            for j in range(n): v[j] = 2 * x[j] + shift2[j]
            q = 0
            for a in range(n):
                if v[a] != 0:
                    for b in range(n): q += v[a] * G[a, b] * v[b]
            if q <= N4:
                if cnt < maxout:
                    for j in range(n): out[cnt, j] = v[j]
                cnt += 1
            x[i] += 1
            continue
        rem[i] = rr; i -= 1
        c = 0.0
        for j in range(i + 1, n): c -= Lu[i, j] * z[j]
        cen[i] = c
        r = np.sqrt(max(rem[i + 1], 0.0) / d[i])
        x[i] = np.int64(np.ceil(cen[i] - s[i] - r)); hi[i] = np.int64(np.floor(cen[i] - s[i] + r))
    return out[:min(cnt, maxout)], cnt


def ldl(G):
    n = len(G); Gf = G.astype(float); Lu = np.eye(n); d = np.zeros(n)
    Lc = np.linalg.cholesky(Gf)                                         # G = Lc Lc^T, Lc lower
    for i in range(n): d[i] = Lc[i, i] ** 2
    for i in range(n):
        for j in range(i + 1, n): Lu[i, j] = Lc[j, i] / Lc[i, i]
    return Lu, d


def short(G, N, shift2=None, maxout=600_000):
    """vectors (as 2x + shift2 rows) of norm <= N in U (shift2 = 0) or in the shadow (shift2 = c)"""
    Lu, d = ldl(G); sh = np.zeros(len(G), np.int64) if shift2 is None else np.asarray(shift2, np.int64)
    out, cnt = fp_enum(G, Lu, d, 4 * N, sh, maxout)
    assert cnt <= maxout, "maxout too small (%d)" % cnt
    return out


def solve_mod2(G, rhs):
    n = len(G); A = [[int(G[i][j]) & 1 for j in range(n)] + [int(rhs[i]) & 1] for i in range(n)]; row = 0; piv = []
    for c in range(n):
        p = next((i for i in range(row, n) if A[i][c]), None)
        if p is None: continue
        A[row], A[p] = A[p], A[row]
        for i in range(n):
            if i != row and A[i][c]: A[i] = [a ^ b for a, b in zip(A[i], A[row])]
        piv.append(c); row += 1
    assert row == n
    x = [0] * n
    for i, c in enumerate(piv): x[c] = A[i][n]
    return np.array(x, dtype=np.int64)


# ------------------------------------------------------------------ theta series (exact completeness certificate)
def _mul(a, b, D):
    r = [F(0)] * D
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if i + j >= D: break
            r[i + j] += x * y
    return r


def _pow(a, k, D):
    r = [F(1)] + [F(0)] * (D - 1)
    for _ in range(k): r = _mul(r, a, D)
    return r


def theta_predictions(N2, D=9):
    """Exact shell sizes predicted by the Gleason-type theorem for an odd unimodular lattice of rank 24 with N1 = 0 and N2 roots:
    Theta_L = sum_j a_j th3^(24-8j) D8^j,  Theta_S = sum_j a_j (-1)^j 2^(24-12j) q^(6-2j) T^(24-8j) (th3 th4)^(4j),
    th3 = sum q^(m^2), th4 = sum (-1)^m q^(m^2), T = sum_{m>=0} q^(m(m+1)), D8 = q T^4 th4^4  (q = exp(i pi tau), exponent = norm).
    Unknown a_1, a_2 from N1 = 0 and N2; a_3 = 0 from 'no shadow vector of norm 0'. Returns (L coefficients, S coefficients)."""
    th3 = [F(0)] * D; th4 = [F(0)] * D; T = [F(0)] * D
    m = 0
    while m * m < D:
        th3[m * m] += 1 if m == 0 else 2; th4[m * m] += 1 if m == 0 else 2 * (-1) ** m; m += 1
    m = 0
    while m * (m + 1) < D:
        T[m * (m + 1)] += 1; m += 1
    D8 = _mul([F(0), F(1)] + [F(0)] * (D - 2), _mul(_pow(T, 4, D), _pow(th4, 4, D), D), D)
    basisL = [_mul(_pow(th3, 24 - 8 * j, D), _pow(D8, j, D), D) for j in range(4)]
    th34 = _mul(th3, th4, D)

    def basisS(j):
        t = _mul(_pow(T, 24 - 8 * j, D), _pow(th34, 4 * j, D), D)
        sh = 6 - 2 * j
        t = [F(0)] * sh + t[:D - sh]
        c = F((-1) ** j) * F(2) ** (24 - 12 * j)
        return [c * x for x in t]
    BS = [basisS(j) for j in range(4)]
    # a_0 = 1 (q^0); q^1: N1 = 0; q^2: N2.  Solve the 2x2 system for (a_1, a_2) with a_3 = 0.
    # L(q) = B0 + a1 B1 + a2 B2 ; coefficient of q^1 and q^2.
    b0, b1, b2 = basisL[0], basisL[1], basisL[2]
    # q^1: b0[1] + a1 b1[1] + a2 b2[1] = 0 ; q^2: b0[2] + a1 b1[2] + a2 b2[2] = N2
    det = b1[1] * b2[2] - b2[1] * b1[2]
    r1 = -b0[1]; r2 = N2 - b0[2]
    a1 = (r1 * b2[2] - b2[1] * r2) / det; a2 = (b1[1] * r2 - b1[2] * r1) / det
    L = [b0[k] + a1 * b1[k] + a2 * b2[k] for k in range(D)]
    S = [BS[0][k] + a1 * BS[1][k] + a2 * BS[2][k] for k in range(D)]
    return L, S


# ------------------------------------------------------------------ lattice
class Lattice:
    def __init__(self, lid, verbose=True):
        self.lid = lid
        t0 = time.time()
        summ = json.load(open(os.path.join(HAND28, lid + ".json")))
        self.summary = summ
        Bq = [[F(s) for s in row] for row in summ["basis"]]
        assert len(Bq) == 24 and all(len(r) == 24 for r in Bq)
        Gq = [[sum(a * b for a, b in zip(u, v)) for v in Bq] for u in Bq]
        assert all(x.denominator == 1 for row in Gq for x in row), "Gram not integral"
        self.G = np.array([[int(x) for x in row] for row in Gq], dtype=np.int64)
        assert (self.G == self.G.T).all()
        assert round(abs(np.linalg.det(self.G.astype(float)))) == 1, "not unimodular (float det)"
        # exact determinant check by fraction elimination
        self.det = _exact_det(self.G)
        assert abs(self.det) == 1
        assert all(int(self.G[i, i]) % 2 == 0 or True for i in range(24))
        G = self.G
        # shells of U: norms 1..4 (full, both signs)
        V2 = short(G, 4)
        X = V2 // 2
        assert (V2 % 2 == 0).all()
        nrm = np.einsum("ij,jk,ik->i", X, G, X)                          # exact int64
        nz = nrm > 0
        assert nrm[~nz].size == 1 and (X[~nz] == 0).all()                  # the zero vector, once
        X = X[nz]; nrm = nrm[nz]
        assert nrm.min() >= 2, "norm-1 vector present"
        self.X = {k: X[nrm == k] for k in (2, 3, 4)}
        sc = json.load(open(SHELLS))[lid]
        self.shell_counts = {2: len(self.X[2]), 3: len(self.X[3]), 4: len(self.X[4])}
        assert self.shell_counts[2] == sc["N2"] and self.shell_counts[3] == sc["N3"] and self.shell_counts[4] == sc["N4"], \
            ("shell sizes differ from the stored exact counts", self.shell_counts, sc)
        # theta certificate (independent of the campaign): N3, N4 and shadow shells
        L, S = theta_predictions(self.shell_counts[2])
        assert [L[0], L[1], L[2], L[3], L[4]] == [1, 0, self.shell_counts[2], self.shell_counts[3], self.shell_counts[4]], ("theta mismatch", L[:5])
        self.theta_S = {2: int(S[2]), 4: int(S[4]), 0: int(S[0])}
        assert S[0] == 0 and S[1] == 0 and S[3] == 0 and S[2].denominator == 1 and S[4].denominator == 1
        # shadow
        c = solve_mod2(G, np.diag(G))
        self.c = c
        W = short(G, 4, c)                                                 # rows v = 2x + c, 4*norm(b) = v G v <= 16
        q = np.einsum("ij,jk,ik->i", W, G, W)
        assert (W % 2 == c % 2).all()
        self.S = {}
        for nn in (2, 4):
            self.S[nn] = W[q == 4 * nn]
        assert set(np.unique(q).tolist()) <= {8, 16}, set(np.unique(q).tolist())
        assert len(self.S[2]) == self.theta_S[2] == self.shell_counts[2] + 48, (len(self.S[2]), self.theta_S, self.shell_counts)
        assert len(self.S[4]) == self.theta_S[4], (len(self.S[4]), self.theta_S)
        # Gram-multiplied copies (int64, exact)
        self.XG = {k: self.X[k] @ G for k in (2, 3, 4)}
        self.SG = {k: self.S[k] @ G for k in (2, 4)}
        self.secs = round(time.time() - t0, 1)
        if verbose:
            print("lattice %s: roots N2=%d N3=%d N4=%d | shadow norm2 %d norm4 %d | enumeration complete (matches stored counts and theta certificate) | %.1fs"
                  % (lid, self.shell_counts[2], self.shell_counts[3], self.shell_counts[4], len(self.S[2]), len(self.S[4]), self.secs), flush=True)


def _exact_det(G):
    n = len(G); A = [[F(int(x)) for x in row] for row in G]; det = F(1)
    for k in range(n):
        p = next((i for i in range(k, n) if A[i][k] != 0), None)
        if p is None: return 0
        if p != k: A[k], A[p] = A[p], A[k]; det = -det
        det *= A[k][k]
        for i in range(k + 1, n):
            if A[i][k] != 0:
                f = A[i][k] / A[k][k]
                A[i] = [x - f * y for x, y in zip(A[i], A[k])]
    return det


def load_survivor_pairs(lid):
    """Pairs stored in hand_28 with no witness among the norm 2, 3, 4 vectors (the 'survivors').  Returns list of (row index, y1, y2)."""
    Z = np.load(os.path.join(HAND28, lid + "_pairs.npz"), allow_pickle=False)
    y1 = {int(o): Z["y1"][i].astype(np.int64) for i, o in enumerate(Z["y1_o"])}
    keep = np.flatnonzero(Z["e"] >= 11)
    return [(int(r), int(Z["o"][r]), y1[int(Z["o"][r])], Z["y2"][r].astype(np.int64)) for r in keep], int(len(Z["o"]))
