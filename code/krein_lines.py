"""Krein / Delsarte inequality for the LINE vectors of an srg(n, 2t+2, 1, 2)  (pure mathematics; tiny computations).

Line vector: w_L = E_s 1_L (projection of the line's indicator on the eigenspace of the negative eigenvalue s).
Gram entries depend only on local data: same line, meeting lines, disjoint lines joined by e edges (e in 0..3).
For 99: 7 * Gram = K with K = 4 (same), 0 (meeting), 1 - e (disjoint), K^2 = 21 K, K 1 = 0.
Schoenberg / Delsarte: for unit vectors u_i on S^{m-1}, sum_{i,j} G_k(<u_i,u_j>) >= 0 for every Gegenbauer
polynomial G_k of S^{m-1}.  k = 3: G_3(t) = t^3 - 3t/(m+2); with sum_{ij} t_ij = 0 this is  sum_{ij} t_ij^3 >= 0.
Per-line counts (derived in notes/70): n3 = pi(L) (prisms through L), n2 = 6t - 3pi, n1 = 6t^2 - 12t + 3pi,
n0 = D - 6t^2 + 6t - pi, D = n(t+1)/3 - 1 - 3t.
Output: (1) BvLS: direct numerical check of every formula; (2) the bound for 99:  P <= 1155.
"""
import numpy as np
import sympy as sp
import graphs, rooted


def line_data(A):
    A = np.asarray(A, dtype=float)
    n = len(A)
    k = int(A[0].sum())
    t = (k - 2) // 2
    ev = np.linalg.eigvalsh(A)
    s = round(ev.min())
    r = round(sorted(set(np.round(ev, 6)))[-2])
    Es = (A - r * np.eye(n) - (k - r) / n * np.ones((n, n))) / (s - r)
    L = rooted.lines(A)
    N = np.zeros((n, len(L)))
    for j, l in enumerate(L):
        N[list(l), j] = 1
    G = N.T @ Es @ N
    E = N.T @ A @ N          # e(L,M) for disjoint lines, 4 for meeting, 6 for L = M
    M = N.T @ N              # |L cap M|
    return n, k, t, r, s, L, N, G, E, M


def check_bvls():
    A = graphs.bvls()
    n, k, t, r, s, L, N, G, E, M = line_data(A)
    nl = len(L)
    c = 9 * (k - r) / n
    # formulas for Gram entries
    pred = np.where(M == 3, (6 - 3 * r - c) / (s - r), np.where(M == 1, (4 - r - c) / (s - r), (E - c) / (s - r)))
    print(f'BvLS: n={n} k={k} t={t} r={r} s={s} lines={nl} | Gram formula max error {np.abs(pred - G).max():.2e}')
    disj = (M == 0)
    pis = [(disj[i] & (E[i] == 3)).sum() for i in range(nl)]
    D = n * (t + 1) // 3 - 1 - 3 * t
    ok = all((disj[i] & (E[i] == 2)).sum() == 6 * t - 3 * pis[i]
             and (disj[i] & (E[i] == 1)).sum() == 6 * t * t - 12 * t + 3 * pis[i]
             and (disj[i] & (E[i] == 0)).sum() == D - 6 * t * t + 6 * t - pis[i] for i in range(nl))
    print(f'      per-line counts n_e(pi) correct for all lines: {ok}; pi(L) values: {sorted(set(pis))}')
    u = G / G[0, 0]
    m = int(round(np.trace(G @ np.linalg.pinv(G))))
    print(f'      span dim {m}; sum t = {u.sum():.2e}; sum t^3 = {(u ** 3).sum():.4f} (must be >= 0); '
          f'predicted per line (from pi): {per_line_cube(n, k, r, s, t, np.mean(pis)) * nl:.4f}')


def per_line_cube(n, k, r, s, t, pi):
    """sum_M <u_L,u_M>^3 for one line, as a function of pi (normalised Gram)."""
    c = 9 * (k - r) / n
    self_ = 6 - 3 * r - c
    meet = 4 - r - c
    D = n * (t + 1) / 3 - 1 - 3 * t
    ne = {3: pi, 2: 6 * t - 3 * pi, 1: 6 * t * t - 12 * t + 3 * pi, 0: D - 6 * t * t + 6 * t - pi}
    tot = self_ ** 3 + 3 * t * meet ** 3 + sum(ne[e] * (e - c) ** 3 for e in ne)
    return tot / self_ ** 3


def bound_99():
    pi, P = sp.symbols('pi P')
    n, k, r, s, t = 99, 14, 3, -4, 6
    expr = sp.nsimplify(per_line_cube(n, k, r, s, t, pi))
    print('99: sum_M t_LM^3 per line =', sp.simplify(expr), ' -> summed over lines with sum pi = 2P:',
          sp.simplify(231 * expr.subs(pi, 2 * P / 231)), '>= 0  =>  P <=', sp.solve(231 * expr.subs(pi, 2 * P / 231), P))
    # refinement: joint Gegenbauer matrix of points and lines (points: t = 1, -2/7, 1/28)
    G3 = lambda x: x ** 3 - sp.Rational(3, 46) * x
    Spp = 99 * (G3(1) + 14 * G3(sp.Rational(-2, 7)) + 84 * G3(sp.Rational(1, 28)))
    a, b, f = 2 / sp.sqrt(28), -1 / sp.sqrt(28), sp.Rational(1, 2) / sp.sqrt(28)
    Spl = 231 * (3 * G3(a) + 36 * G3(b) + 60 * G3(f))
    Sll = sp.expand(231 * 231 * 0 + (13860 - 12 * P) / 64)
    sol = sp.solve(sp.Eq(Spl ** 2, Spp * Sll), P)
    print(f'99: joint points+lines (2x2 Gegenbauer matrix PSD): S_pp = {float(Spp):.4f}, S_pl = {float(Spl):.4f} '
          f'=> P <= {float(sol[0]):.2f}')


if __name__ == '__main__':
    check_bvls()
    bound_99()
