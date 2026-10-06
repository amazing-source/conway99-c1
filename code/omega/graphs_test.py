"""Known srg used as controls (adjacency matrices as numpy arrays)."""
import itertools, numpy as np

def paley9():
    F = [(a, b) for a in range(3) for b in range(3)]
    A = np.zeros((9, 9), dtype=int)
    for i, (a, b) in enumerate(F):
        for j, (c, d) in enumerate(F):
            if i != j and (a == c or b == d): A[i, j] = 1
    return A

def petersen():
    V = list(itertools.combinations(range(5), 2)); n = len(V)
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if not set(V[i]) & set(V[j]): A[i, j] = 1
    return A

def clebsch():
    V = list(itertools.product(range(2), repeat=4)); n = 16
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            d = sum(a != b for a, b in zip(V[i], V[j]))
            if d == 1 or d == 4: A[i, j] = 1
    return A

def bvls243():
    G = np.array([[1,0,0,0,0,0,1,1,1,1,1],[0,1,0,0,0,0,0,1,2,2,1],[0,0,1,0,0,0,1,0,1,2,2],
                  [0,0,0,1,0,0,2,1,0,1,2],[0,0,0,0,1,0,2,2,1,0,1],[0,0,0,0,0,1,1,2,2,1,0]])
    # parity check H (5 x 11) of the ternary Golay [11,6] code: rows orthogonal to G mod 3
    dual = []
    for w in itertools.product(range(3), repeat=11):
        if all(sum(a * b for a, b in zip(w, g)) % 3 == 0 for g in G) and any(w):
            dual.append(w)
            if len(dual) > 400: break
    H = []
    def span(M):
        S = set()
        for c in itertools.product(range(3), repeat=len(M)):
            S.add(tuple((np.array(c) @ np.array(M)) % 3))
        return S
    for w in dual:
        if len(span(H + [w])) == 3 ** (len(H) + 1): H.append(w)
        if len(H) == 5: break
    H = np.array(H)
    synd = lambda v: tuple((H @ np.array(v)) % 3)
    allsy = sorted(itertools.product(range(3), repeat=5)); idx = {s: i for i, s in enumerate(allsy)}
    unit = []
    for p in range(11):
        for a in (1, 2):
            e = [0] * 11; e[p] = a; unit.append(synd(e))
    A = np.zeros((243, 243), dtype=int)
    for s in allsy:
        for u in unit:
            t = tuple((np.array(s) + np.array(u)) % 3); A[idx[s], idx[t]] = 1
    return A

def is_srg(A, n, k, lam, mu):
    A = np.array(A); I = np.eye(n, dtype=int); J = np.ones((n, n), dtype=int)
    return bool((A @ A == k * I + lam * A + mu * (J - I - A)).all() and (A == A.T).all() and not np.diag(A).any())
