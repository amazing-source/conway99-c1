"""Look for non-coboundary parity classes invariant under an involution of BH (a restriction, used to FIND solutions).
Involution invariance of the class: g*eps = eps + delta f; we impose strict g*eps = eps + delta f with f free."""
import itertools, sys, time, random, pickle, numpy as np
import pycryptosat
from sympy.combinatorics import Permutation, PermutationGroup
sys.path.insert(0, ".")
from lib243 import aut
V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
n = 81
Q = np.zeros((n, n), dtype=np.int64)
for a in V:
    for b in V:
        if a != b and q(sub(a, b)) == 0: Q[I[a], I[b]] = 1
nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
o, orb, gens = aut(Q)
G = PermutationGroup([Permutation(g) for g in gens])
random.seed(3); reps = {}
for _ in range(20000):
    g = G.random(); k = g.order()
    if k % 2 == 0:
        h = g ** (k // 2); a = h.array_form
        fixed = [x for x in range(81) if a[x] == x]
        fe = sum(1 for x in range(81) for y in range(x + 1, 81) if Q[x, y] and {a[x], a[y]} == {x, y})
        swapped_adj = sum(1 for x in range(81) if a[x] != x and Q[x, a[x]])
        reps.setdefault((len(fixed), fe, swapped_adj), a)
print("involution types:", sorted(reps), flush=True)
def solve(perm, threads, tlimit):
    s = pycryptosat.Solver(threads=threads, time_limit=tlimit); nv = 0
    def new():
        nonlocal nv; nv += 1; return nv
    E = {}
    for P in range(n):
        for R in nb[P]:
            if P < R: E[(P, R)] = E[(R, P)] = new()
    F = [new() for _ in range(n)]
    for P in range(n):                  # eps(gP,gR) = eps(P,R) + f(P) + f(R)
        for R in nb[P]:
            if P < R: s.add_xor_clause([E[(perm[P], perm[R])], E[(P, R)], F[P], F[R]], False)
    for P in range(n):
        for R in nb[P]:
            for S_ in nb[P] & nb[R]:
                if P < R < S_: s.add_xor_clause([E[(P, R)], E[(R, S_)], E[(P, S_)]], False)
    T = []
    for P in range(n):
        for R in range(P + 1, n):
            if Q[P, R]: continue
            t = new(); T.append(t); pis = []
            for Z in sorted(nb[P] & nb[R]):
                p = new(); s.add_xor_clause([E[(P, Z)], E[(Z, R)], p], False); pis.append(p)
            s.add_xor_clause(pis + [t], False)
            for i, j in itertools.permutations(range(6), 2): s.add_clause([t, -pis[i], pis[j]])
            for k in (1, 5):
                for cc in itertools.combinations(range(6), k):
                    s.add_clause([-t] + [(-pis[i] if i in cc else pis[i]) for i in range(6)])
    s.add_clause(T)
    t0 = time.time(); sat, sol = s.solve()
    return sat, time.time() - t0, (sol, E) if sat else None
for key, a in sorted(reps.items()):
    sat, dt, data = solve(a, 1, float(sys.argv[1]) if len(sys.argv) > 1 else 600)
    print(f"involution type {key}: {sat} ({dt:.0f}s)", flush=True)
    if sat:
        sol, E = data
        pickle.dump({"perm": a, "eps": {k: sol[v] for k, v in E.items()}}, open(f"parity_inv_{key[0]}_{key[1]}_{key[2]}.pkl", "wb"))
