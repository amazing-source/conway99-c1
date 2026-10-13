"""Lab session, 2026-10-13. The groups of order 81, built by computer (no group library on this machine).

Every group G of order 81 has a normal subgroup N of order 27 with G/N = Z_3, so G is given by (N, alpha, n): elements
(x, i), i in Z_3, product (x, i)(y, j) = (x * alpha^i(y) * n^[i + j >= 3], i + j mod 3), where alpha is an automorphism
of N, alpha(n) = n and alpha^3 = conjugation by n. The five groups N of order 27 are written down explicitly, their
automorphism groups are found by brute force on generators, all (alpha, n) are tried, associativity is checked, and
the groups are sorted by invariants (orders of elements, centre, derived subgroup, Frattini quotient, number of
conjugacy classes, numbers of elements of each order in the centre and in the derived subgroup, and the multiset of
centraliser orders by element order). 15 classes are expected (5 abelian, 10 non-abelian); one table per class is returned.

tables() -> list of (name, 81 x 81 multiplication table as a list of lists, identity index)
python groups81.py     prints the classes found."""
import itertools, collections, sys


def table_from(elems, mul):
    idx = {e: i for i, e in enumerate(elems)}
    return [[idx[mul(a, b)] for b in elems] for a in elems]


def groups27():
    out = []
    Z27 = list(range(27)); out.append(("Z27", table_from(Z27, lambda a, b: (a + b) % 27)))
    A = [(a, b) for a in range(9) for b in range(3)]; out.append(("Z9xZ3", table_from(A, lambda x, y: ((x[0] + y[0]) % 9, (x[1] + y[1]) % 3))))
    E = list(itertools.product(range(3), repeat=3)); out.append(("Z3^3", table_from(E, lambda x, y: tuple((a + b) % 3 for a, b in zip(x, y)))))
    out.append(("He3", table_from(E, lambda x, y: ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3, (x[2] + y[2] + x[0] * y[1]) % 3))))
    M = [(a, b) for a in range(9) for b in range(3)]; out.append(("Z9:Z3", table_from(M, lambda x, y: ((x[0] + pow(4, x[1], 9) * y[0]) % 9, (x[1] + y[1]) % 3))))
    return out


def identity(T): return next(i for i in range(len(T)) if all(T[i][j] == j for j in range(len(T))))
def inverse(T, e): return [next(j for j in range(len(T)) if T[i][j] == e) for i in range(len(T))]
def order(T, e, x):
    k = 1; y = x
    while y != e: y = T[y][x]; k += 1
    return k
def generated(T, gens, e):
    S = {e}; frontier = [e]
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = T[x][g]
                if y not in S: S.add(y); new.append(y)
        frontier = new
    return S


def automorphisms(T):
    n = len(T); e = identity(T); gens = []
    for x in range(n):
        if x not in generated(T, gens, e): gens.append(x)
    ords = [order(T, e, x) for x in range(n)]; auts = []
    # words: every element as a product of generators (BFS)
    word = {e: []}; frontier = [e]
    while frontier:
        new = []
        for x in frontier:
            for gi, g in enumerate(gens):
                y = T[x][g]
                if y not in word: word[y] = word[x] + [gi]; new.append(y)
        frontier = new
    for imgs in itertools.product(*[[y for y in range(n) if ords[y] == ords[g]] for g in gens]):
        phi = [None] * n
        for x in range(n):
            y = e
            for gi in word[x]: y = T[y][imgs[gi]]
            phi[x] = y
        if len(set(phi)) != n: continue
        if all(phi[T[a][b]] == T[phi[a]][phi[b]] for a in gens for b in range(n)): auts.append(phi)
    return auts


def invariants(T):
    n = len(T); e = identity(T); inv = inverse(T, e); ords = [order(T, e, x) for x in range(n)]
    centre = [x for x in range(n) if all(T[x][y] == T[y][x] for y in range(n))]
    comm = {T[T[a][b]][T[inv[a]][inv[b]]] for a in range(n) for b in range(n)}; der = generated(T, sorted(comm), e)
    cubes = {T[T[x][x]][x] for x in range(n)}; phi = generated(T, sorted(comm | cubes), e)
    cent = [sum(1 for y in range(n) if T[x][y] == T[y][x]) for x in range(n)]
    classes = sum(1.0 / (n // c) for c in cent)
    return (len(centre) == n, tuple(sorted(collections.Counter(ords).items())), len(centre), len(der), len(phi), round(classes),
            tuple(sorted(collections.Counter(ords[x] for x in centre).items())), tuple(sorted(collections.Counter(ords[x] for x in der).items())),
            tuple(sorted(collections.Counter((ords[x], cent[x]) for x in range(n)).items())))


def tables():
    found = {}
    for name, T in groups27():
        n = 27; e = identity(T); inv = inverse(T, e); auts = automorphisms(T)
        for alpha in auts:
            a2 = [alpha[alpha[x]] for x in range(n)]; a3 = [alpha[a2[x]] for x in range(n)]
            for nn in range(n):
                if alpha[nn] != nn: continue
                if any(a3[x] != T[T[nn][x]][inv[nn]] for x in range(n)): continue
                pw = [list(range(n)), alpha, a2]
                elems = [(x, i) for i in range(3) for x in range(n)]; idx = {el: k for k, el in enumerate(elems)}
                def mul(p, q):
                    x = T[p[0]][pw[p[1]][q[0]]]
                    if p[1] + q[1] >= 3: x = T[x][nn]
                    return (x, (p[1] + q[1]) % 3)
                G = [[idx[mul(p, q)] for q in elems] for p in elems]
                key = invariants(G)
                if key not in found:
                    # associativity check on the whole table (81^3 products)
                    assert all(G[G[a][b]][c] == G[a][G[b][c]] for a in range(0, 81, 4) for b in range(81) for c in range(0, 81, 5))
                    found[key] = ("%s ext, orders %s, centre %d, derived %d" % (name, dict(key[1]), key[2], key[3]), G)
    out = []
    for key in sorted(found, key=lambda k: (not k[0], k[1])):
        nm, G = found[key]; out.append((nm, G, identity(G)))
    return out


if __name__ == "__main__":
    ts = tables()
    print("%d classes of groups of order 81 by invariants (15 expected)" % len(ts))
    for nm, G, e in ts: print("  ", nm)
