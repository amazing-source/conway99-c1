"""Exhaustive search of Cayley covers of BH by exponent-3 central extensions (gauge reduced):
B strictly upper triangular (alternating part of the cocycle; symmetric parts are gauge),
a = 0 on the basis vectors e_i (linear gauge)."""
import itertools, numpy as np, pickle
from heis import Sbar, reps, check, bil, rank3

neg = lambda s: tuple((-np.array(s)) % 3)
basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]
assert all(b in Sbar for b in basis)
reps_list = sorted({min(s, neg(s)) for s in Sbar})
free = [r for r in reps_list if r not in basis and neg(r) not in basis]
print("free a-values:", len(free))
ut = [(i, j) for i in range(4) for j in range(i + 1, 4)]
# precompute for vectorised check: for each delta, the 6 (s1,s2)
sols = []
for Uvals in itertools.product(range(3), repeat=6):
    U = np.zeros((4, 4), dtype=int)
    for (i, j), v in zip(ut, Uvals): U[i, j] = v
    for avals in itertools.product(range(3), repeat=len(free)):
        av = {b: 0 for b in basis}
        for r, v in zip(free, avals): av[r] = v
        for r in list(av):
            av[neg(r)] = (-av[r] + bil(U, r, r)) % 3
        if check(av, U):
            sols.append((Uvals, avals))
print("solutions", len(sols))
cnt = {}
for Uvals, _ in sols:
    U = np.zeros((4, 4), dtype=int)
    for (i, j), v in zip(ut, Uvals): U[i, j] = v
    rk = rank3(((U - U.T) % 3).tolist()); cnt[rk] = cnt.get(rk, 0) + 1
print("rank of commutator form -> #solutions:", cnt)
pickle.dump(sols, open("heis_brute.pkl", "wb"))
