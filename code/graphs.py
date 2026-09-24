"""Control graphs for the C1 research (all built from scratch, checked on load).

(lambda, mu) = (1, 2) family, i.e. partial quadrangles PQ(2, t, 2):
  srg9()      srg(9,4,1,2)     = K3 x K3 (3x3 rook graph), H(2,3)
  bvls()      srg(243,22,1,2)  = Berlekamp-van Lint-Seidel (Cayley on F_3^5, ternary Golay)
(lambda, mu) = (0, 2) family ("q = 2" analogue, lines of size 2):
  clebsch()   srg(16,5,0,2)    = folded 5-cube (a quotient of the 5-cube)
  gewirtz()   srg(56,10,0,2)   = Gewirtz graph (NOT a quotient of the 10-cube: 56 does not divide 2^10)
other lambda = 1 graphs (lines of size 3, mu != 2):
  gq22()      srg(15,6,1,3)    = collinearity graph of GQ(2,2)
  gq24()      srg(27,10,1,5)   = collinearity graph of GQ(2,4) (complement of the Schlaefli graph)
"""
import itertools
import numpy as np


def srg_params(A):
    """Return (n,k,lam,mu) if A is the adjacency matrix of an SRG, else None."""
    A = np.asarray(A, dtype=np.int64)
    n = A.shape[0]
    if not (A == A.T).all() or A.diagonal().any():
        return None
    deg = A.sum(1)
    if (deg != deg[0]).any():
        return None
    k = int(deg[0])
    A2 = A @ A
    off = ~np.eye(n, dtype=bool)
    lam_vals = set(A2[(A == 1) & off].tolist())
    mu_vals = set(A2[(A == 0) & off].tolist())
    if len(lam_vals) > 1 or len(mu_vals) > 1:
        return None
    return n, k, (lam_vals.pop() if lam_vals else None), (mu_vals.pop() if mu_vals else None)


def _cayley(V, S, add):
    ix = {v: i for i, v in enumerate(V)}
    n = len(V)
    A = np.zeros((n, n), dtype=np.int64)
    for v in V:
        for s in S:
            A[ix[v], ix[add(v, s)]] = 1
    return A


def srg9():
    V = list(itertools.product(range(3), repeat=2))
    A = np.array([[1 if (u != v and (u[0] == v[0] or u[1] == v[1])) else 0 for v in V] for u in V], dtype=np.int64)
    assert srg_params(A) == (9, 4, 1, 2)
    return A


def _nullspace_mod(G, p):
    G = np.array(G, dtype=np.int64) % p
    r, c = G.shape
    piv = []
    row = 0
    for col in range(c):
        pr = next((i for i in range(row, r) if G[i, col]), None)
        if pr is None:
            continue
        G[[row, pr]] = G[[pr, row]]
        G[row] = (G[row] * pow(int(G[row, col]), -1, p)) % p
        for i in range(r):
            if i != row and G[i, col]:
                G[i] = (G[i] - G[i, col] * G[row]) % p
        piv.append(col)
        row += 1
        if row == r:
            break
    free = [j for j in range(c) if j not in piv]
    basis = []
    for f in free:
        v = np.zeros(c, dtype=np.int64)
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-G[i, f]) % p
        basis.append(v)
    return np.array(basis)


def bvls(return_coords=False):
    """srg(243,22,1,2): Cayley graph on F_3^5, connection set = +- columns of a parity-check matrix
    of the [11,6,5] ternary Golay code (cyclic, generator x^5+x^4-x^3+x^2-1 over F_3)."""
    g = [2, 0, 1, 2, 1, 1]  # coefficients low -> high of x^5 + x^4 + 2x^3 + x^2 + 2 (= x^5+x^4-x^3+x^2-1)
    G = np.zeros((6, 11), dtype=np.int64)
    for s in range(6):
        G[s, s:s + 6] = g
    H = _nullspace_mod(G, 3)
    assert H.shape == (5, 11) and not ((G @ H.T) % 3).any()
    cols = [tuple(int(t) for t in H[:, i]) for i in range(11)]
    neg = lambda v: tuple((-np.array(v)) % 3)
    S = sorted(set(cols) | {neg(c) for c in cols})
    assert len(S) == 22
    V = list(itertools.product(range(3), repeat=5))
    A = _cayley(V, S, lambda v, s: tuple((np.array(v) + np.array(s)) % 3))
    assert srg_params(A) == (243, 22, 1, 2)
    if return_coords:
        return A, V, S
    return A


def clebsch():
    V = list(itertools.product(range(2), repeat=4))
    S = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 1, 1)]
    A = _cayley(V, S, lambda v, s: tuple((a + b) % 2 for a, b in zip(v, s)))
    assert srg_params(A) == (16, 5, 0, 2)
    return A


def _golay24_octads():
    """Extended binary Golay code from the quadratic-residue construction (length 23 QR code + parity)."""
    g = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]  # x^11+x^10+x^6+x^5+x^4+x^2+1, low -> high
    B = np.zeros((12, 23), dtype=np.int64)
    for s in range(12):
        B[s, s:s + 12] = g
    B = np.hstack([B, (B.sum(1) % 2)[:, None]])
    words = []
    for bits in itertools.product(range(2), repeat=12):
        w = (np.array(bits) @ B) % 2
        if w.sum() == 8:
            words.append(frozenset(np.nonzero(w)[0].tolist()))
    assert len(words) == 759, len(words)
    return words


def gewirtz():
    octads = _golay24_octads()
    p, q, r = 0, 1, 2
    hexads = [o - {p, q} for o in octads if p in o and q in o]  # S(3,6,22) on 22 points
    assert len(hexads) == 77
    V = [h for h in hexads if r not in h]
    assert len(V) == 56
    A = np.array([[1 if (u != v and not (u & v)) else 0 for v in V] for u in V], dtype=np.int64)
    assert srg_params(A) == (56, 10, 0, 2)
    return A


def gq22():
    """GQ(2,2) = W(2): points = 15 pairs... use the classical model: points = 2-subsets of {0..5},
    lines = partitions of {0..5} into three pairs; collinear iff disjoint."""
    V = list(itertools.combinations(range(6), 2))
    A = np.array([[1 if (u != v and not set(u) & set(v)) else 0 for v in V] for u in V], dtype=np.int64)
    assert srg_params(A) == (15, 6, 1, 3)
    return A


def gq24():
    """Collinearity graph of GQ(2,4): complement of the Schlaefli graph. Schlaefli graph: 27 vertices;
    use the model: vertices = 27 lines of a cubic surface, labelled a_i, b_i (i=1..6), c_ij; two lines
    skew in the Schlaefli graph convention. Collinearity graph of GQ(2,4) = 'intersecting lines' graph (degree 10)."""
    V = [('a', i) for i in range(6)] + [('b', i) for i in range(6)] + [('c', i, j) for i, j in itertools.combinations(range(6), 2)]

    def meet(u, v):
        if u == v:
            return False
        tu, tv = u[0], v[0]
        if tu == 'a' and tv == 'a' or tu == 'b' and tv == 'b':
            return False
        if {tu, tv} == {'a', 'b'}:
            return u[1] != v[1]
        if tu == 'c' and tv == 'c':
            return not set(u[1:]) & set(v[1:])
        c, o = (u, v) if tu == 'c' else (v, u)
        return o[1] in c[1:]

    A = np.array([[1 if meet(u, v) else 0 for v in V] for u in V], dtype=np.int64)
    assert srg_params(A) == (27, 10, 1, 5), srg_params(A)
    return A


ALL = {'srg9': srg9, 'bvls': bvls, 'clebsch': clebsch, 'gewirtz': gewirtz, 'gq22': gq22, 'gq24': gq24}

if __name__ == '__main__':
    for name, f in ALL.items():
        A = f()
        ev = np.round(np.linalg.eigvalsh(A.astype(float)), 6)
        vals, cnt = np.unique(ev, return_counts=True)
        print(name, srg_params(A), dict(zip(vals.tolist(), cnt.tolist())))
