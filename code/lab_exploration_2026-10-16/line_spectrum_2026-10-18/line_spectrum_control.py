"""Positive control (srg(v,k,1,2) given as an edge list) of the line-spectrum theorem (LAB, 18/10/2026).
For a line L: N(L) = vertices adjacent to exactly one point of L, G_L = induced (cubic) graph on N(L),
D_L = vertices at distance 2 from L, N_L = 0/1 incidence N(L) x D_L, eigenvalues of Gamma: k, r > 0 > s.
Prediction (proof in LINE_SPECTRUM_2026-10-18.md):
  K' := ker N_L^T minus span{g_alpha} (g_alpha(v) = alpha(p(v)), alpha sum-zero on L) consists of eigenvalue-3 vectors of
  G_L (component indicators) when k = 14, and is 0 when k > 14;  sum over K' of (theta-r)(theta-s) = 0;
  spec Gamma[D_L] = {k-6} + r^{m_r'} + s^{m_s'} + {-1-theta : theta in spec(G_L) minus 3 (once), 0 (twice), K'};
  m_r', m_s' = dims of the r- and s-eigenspaces of Gamma supported on D_L.
usage: python line_spectrum_control.py <file.edges> [max_lines]"""
import sys
import numpy as np
path = sys.argv[1]
maxl = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
E = [tuple(map(int, l.split()[:2])) for l in open(path) if l.strip()]
n = max(max(e) for e in E) + 1
A = np.zeros((n, n))
for a, b in E:
    A[a, b] = A[b, a] = 1
k = int(A.sum(1)[0])
I = np.eye(n)
assert np.array_equal(A @ A + A, (k - 2) * I + 2 * np.ones((n, n))), "not srg(v,k,1,2)"
r = (-1 + np.sqrt(1 + 4 * (k - 2))) / 2; s = -1 - r
lines = sorted({tuple(sorted((a, b, c))) for a in range(n) for b in np.nonzero(A[a])[0] if b > a
                for c in np.nonzero(A[a] * A[b])[0] if c > b})
print(path.split("/")[-1], "n", n, "k", k, "r", r, "s", s, "lines", len(lines))
def mult(ev, x, tol=1e-6):
    return int(np.sum(np.abs(ev - x) < tol))
bad = 0; stats = {}
for L in lines[:maxl]:
    Ls = set(L)
    NL = [v for v in range(n) if v not in Ls and A[v, list(L)].sum() == 1]
    DL = [v for v in range(n) if v not in Ls and A[v, list(L)].sum() == 0]
    AG = A[np.ix_(NL, NL)]; AD = A[np.ix_(DL, DL)]; N = A[np.ix_(NL, DL)]
    assert (AG.sum(1) == 3).all() and (AD.sum(1) == k - 6).all() and (N.sum(1) == k - 4).all() and (N.sum(0) == 6).all()
    # components of G_L
    comp = -np.ones(len(NL), int); c = 0
    for i in range(len(NL)):
        if comp[i] >= 0: continue
        st = [i]; comp[i] = c
        while st:
            x = st.pop()
            for y in np.nonzero(AG[x])[0]:
                if comp[y] < 0: comp[y] = c; st.append(y)
        c += 1
    rk = np.linalg.matrix_rank(N)
    kappa = len(NL) - rk
    # K' = ker N^T orthogonal to g_alpha: its A_G spectrum
    U, S_, Vt = np.linalg.svd(N.T)            # N.T : D x N(L);  kernel of N.T in R^{N(L)} = right null space
    null = Vt[rk:].T                          # basis of ker N^T (columns)
    p = [int(np.nonzero(A[v, list(L)])[0][0]) for v in NL]
    galpha = np.array([[1.0 if p[i] == 0 else (-1.0 if p[i] == 1 else 0.0) for i in range(len(NL))],
                       [1.0 if p[i] == 0 else (-1.0 if p[i] == 2 else 0.0) for i in range(len(NL))]]).T
    assert np.allclose(N.T @ galpha, 0)
    # orthogonal complement of g_alpha inside ker N^T
    Q, _ = np.linalg.qr(galpha)
    P = null - Q @ (Q.T @ null)
    u, sv, _ = np.linalg.svd(P, full_matrices=False)
    Kp = u[:, sv > 1e-8]
    thK = np.linalg.eigvalsh(Kp.T @ AG @ Kp) if Kp.shape[1] else np.array([])
    balance = float(np.sum((thK - r) * (thK - s))) if len(thK) else 0.0
    evD = np.sort(np.linalg.eigvalsh(AD)); evG = np.sort(np.linalg.eigvalsh(AG))
    # E_r, E_s of Gamma supported on D_L: dim ker N_L restricted eigenvectors = multiplicities on ker N
    nullD = np.linalg.svd(N)[2][rk:].T        # ker N in R^{D}
    evW = np.linalg.eigvalsh(nullD.T @ AD @ nullD) if nullD.shape[1] else np.array([])
    mr, ms = mult(evW, r), mult(evW, s)
    assert mr + ms == len(evW), "ker N_L not spanned by r/s eigenvectors"
    # predicted spectrum of Gamma[D_L]
    G = list(evG)
    def remove(lst, x):
        j = int(np.argmin([abs(t - x) for t in lst])); assert abs(lst[j] - x) < 1e-6, (x, lst[j]); lst.pop(j)
    remove(G, 3.0); remove(G, 0.0); remove(G, 0.0)
    for t in thK: remove(G, t)
    pred = np.sort(np.array([k - 6.0] + [r] * mr + [s] * ms + [-1 - t for t in G]))
    ok = len(pred) == len(evD) and np.allclose(pred, evD, atol=1e-6)
    kp = Kp.shape[1]
    key = (c, kp, mr, ms, ok, round(balance, 6))
    stats[key] = stats.get(key, 0) + 1
    if not ok or abs(balance) > 1e-6 or (k > 14 and kp > 0) or (k == 14 and any(abs(t - 3) > 1e-6 for t in thK)):
        bad += 1
print("lines tested", sum(stats.values()), "violations", bad)
print("(c, dim K', m_r', m_s', spectrum formula ok, balance): count")
for kk, vv in sorted(stats.items()):
    print("  ", kk, vv)
