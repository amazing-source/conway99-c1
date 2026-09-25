"""notes/102: the square-zero form beta.  For an SRG with p | r - s, p prime to n, N = A - rI mod p satisfies
N^2 = mu J, so N is square-zero on W = 1^perp.  beta(Nv, Nv') = v.N v' is a nondegenerate form on G = N(W), Gram
Q = A - rI + c J in the basis w_u = e_u - n^{-1} 1.  Checks, on existing graphs:
 (1) N^2 = mu J mod p ; (2) rank Q = alpha = rank_p(A - rI) - 1 ; (3) Legendre(disc beta) = eps_V (p^1 Jordan
 component of Lambda_s) times (-u|p)^alpha, u = (r-s)/p ; (4) local: M_x = Schur complement of N at B_1(x),
 M_x^2 = 0, rank M_x = alpha - rank Q_BB, disc(M_x) * disc(Q_BB) = disc(beta)  (G = G_x  perp  span g_v, v in B).
"""
import numpy as np
import eigenlattice_check as ec, genus_tools as gt


def pivots(G, p):
    """symmetric elimination over F_p: nonzero diagonal pivots of an equivalent diagonal form"""
    G = [[x % p for x in row] for row in G]; n = len(G); idx = list(range(n)); d = []
    while idx:
        i = next((a for a in idx if G[a][a]), None)
        if i is None:
            pr = next(((a, b) for a in idx for b in idx if a < b and G[a][b]), None)
            if pr is None:
                break
            a, b = pr
            for c in range(n): G[a][c] = (G[a][c] + G[b][c]) % p
            for c in range(n): G[c][a] = (G[c][a] + G[c][b]) % p
            i = a
        piv = G[i][i]; d.append(piv); inv = pow(piv, -1, p)
        rest = [a for a in idx if a != i]
        for a in rest:
            f = G[a][i] * inv % p
            if f:
                for c in range(n): G[a][c] = (G[a][c] - f * G[i][c]) % p
        for a in rest: G[a][i] = G[i][a] = 0
        idx = rest
    return d


def rank_leg(G, p):
    d = pivots(G, p); prod = 1
    for x in d: prod = prod * x % p
    return len(d), (1 if pow(prod, (p - 1) // 2, p) == 1 else -1)


def inv_mod(M, p):
    n = len(M); A = [[x % p for x in row] + [int(i == j) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        r = next(i for i in range(c, n) if A[i][c]); A[c], A[r] = A[r], A[c]
        iv = pow(A[c][c], -1, p); A[c] = [x * iv % p for x in A[c]]
        for i in range(n):
            if i != c and A[i][c]:
                f = A[i][c]; A[i] = [(a - f * b) % p for a, b in zip(A[i], A[c])]
    return [row[n:] for row in A]


def check(name, A, r, s, p):
    A = np.asarray(A, dtype=np.int64); n = len(A); I = np.eye(n, dtype=np.int64); J = np.ones((n, n), dtype=np.int64)
    A2 = A @ A; mu = int(A2[0][next(j for j in range(1, n) if A[0][j] == 0)])
    N = (A - r * I) % p
    ok1 = ((N @ N - mu * J) % p == 0).all()
    alpha = ec.rank_mod(N.tolist(), p) - 1
    ninv = pow(n, -1, p); Wm = (I - ninv * J) % p
    Q = (Wm.T @ N @ Wm) % p
    rq, eb = rank_leg(Q.tolist(), p)
    B = ec.int_kernel((A - s * I).tolist()); Gs = [[sum(a * b for a, b in zip(u, v)) for v in B] for u in B]
    js = {j: (nj, e) for j, nj, e in gt.jordan_symbol(Gs, p)}
    nV, eV = js.get(1, (0, 1)); u = (r - s) // p
    corr = 1 if alpha % 2 == 0 else (1 if pow((-u) % p, (p - 1) // 2, p) == 1 else -1)
    x = 0; X = [x] + [j for j in range(n) if A[x][j]]; Y = [j for j in range(n) if j not in X]
    NXX = [[int(N[a][b]) for b in X] for a in X]
    if ec.rank_mod(NXX, p) < len(X):
        loc = 'N_XX singular mod p: local formula n/a'
    else:
        iv = np.array(inv_mod(NXX, p), dtype=np.int64)
        M = (N[np.ix_(Y, Y)] - N[np.ix_(Y, X)] @ iv @ N[np.ix_(X, Y)]) % p
        rm, em = rank_leg(M.tolist(), p); rb, ebb = rank_leg(Q[np.ix_(X, X)].tolist(), p)
        loc = (f'M_x^2=0: {((M @ M) % p == 0).all()}, rank M_x={rm}, rank Q_BB={rb}, alpha-rankQ_BB={alpha - rb}, '
               f'eps(M_x)*eps(Q_BB)={em * ebb} vs eps_beta={eb}')
    print(f'{name} p={p}: N^2=muJ {ok1}; alpha={alpha}, rank Q={rq}; eps_beta={eb}, Jordan p^1: dim {nV}, eps_V={eV},'
          f' predicted eps_V={eb * corr}\n   local: {loc}', flush=True)


if __name__ == '__main__':
    import graphs
    check('Petersen', ec.petersen(), 1, -2, 3)
    # srg(9): p = 3 divides n, other shape
    # check('srg(9,4,1,2)', graphs.srg9(), 1, -2, 3)
    check('T(7)', ec.triangular(7), 3, -2, 5)
    check('T(8)', ec.triangular(8), 4, -2, 3)
    check('T(9)', ec.triangular(9), 5, -2, 7)
    # windmill of 99: Q_BB = F - 3I + 3J on B_1(x), fixed
    F = np.zeros((15, 15), dtype=np.int64)
    for i in range(1, 15): F[0][i] = F[i][0] = 1
    for i in range(1, 15, 2): F[i][i + 1] = F[i + 1][i] = 1
    print('99 windmill Q_BB (rank, Legendre of disc):', rank_leg(((F - 3 * np.eye(15, dtype=np.int64) + 3) % 7).tolist(), 7))
