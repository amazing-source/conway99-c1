"""Parity skeleton on BH = VO^-(4,3), eps invariant under a given odd-order automorphism g of BH (strict invariance
is WLOG for odd order since H^1(<g>; Z_2) = 0).  Picks conjugacy-class representatives of odd-order elements."""
import itertools, sys, time, random, numpy as np
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
G = PermutationGroup([Permutation(g) for g in gens]); print("|Aut BH| =", G.order(), flush=True)
# conjugacy classes of elements of order 3 and 5 (sample random elements, keep distinct cycle types + fixed points)
random.seed(1); reps = {}
for _ in range(4000):
    g = G.random()
    for k in (3, 5):
        if g.order() % k == 0:
            h = g ** (g.order() // k)
            key = (k, tuple(sorted(h.cycle_structure.items())))
            reps.setdefault(key, h)
print("odd-order types found:", list(reps.keys()), flush=True)
def solve(g, threads=1):
    perm = g.array_form
    s = pycryptosat.Solver(threads=threads); nv = 0
    def new():
        nonlocal nv; nv += 1; return nv
    E = {}
    for P in range(n):
        for R in nb[P]:
            if P < R and (P, R) not in E:
                v = new(); x, y = P, R
                for _ in range(g.order()):
                    E[(x, y)] = E[(y, x)] = v; x, y = perm[x], perm[y]
    def xor(vs, rhs=False):
        c = {}
        for v in vs: c[v] = c.get(v, 0) ^ 1
        vs2 = [v for v, k in c.items() if k]
        if vs2: s.add_xor_clause(vs2, rhs)
        elif rhs: s.add_clause([])
    for P in range(n):
        for R in nb[P]:
            for S_ in nb[P] & nb[R]:
                if P < R < S_: xor([E[(P, R)], E[(R, S_)], E[(P, S_)]])
    T = []
    for P in range(n):
        for R in range(P + 1, n):
            if Q[P, R]: continue
            t = new(); T.append(t); pis = []
            for Z in sorted(nb[P] & nb[R]):
                p = new(); xor([E[(P, Z)], E[(Z, R)], p]); pis.append(p)
            xor(pis + [t])
            for i, j in itertools.permutations(range(6), 2): s.add_clause([t, -pis[i], pis[j]])
            for k in (1, 5):
                for cc in itertools.combinations(range(6), k):
                    s.add_clause([-t] + [(-pis[i] if i in cc else pis[i]) for i in range(6)])
    s.add_clause(T)
    t0 = time.time(); sat, sol = s.solve()
    return sat, time.time() - t0
for key, h in reps.items():
    sat, dt = solve(h)
    print(f"order {key[0]} cycle type {key[1]}: {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)", flush=True)
