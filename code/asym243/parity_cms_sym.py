"""Parity skeleton on BH = VO^-(4,3) (vertices F_3^4) with eps invariant under a translation subgroup H.
Usage: python3 parity_cms_sym.py THREADS 'v1;v2;...' (generators of H as 4-digit strings over F_3)."""
import itertools, sys, time, numpy as np
import pycryptosat
V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
n = 81
Q = np.zeros((n, n), dtype=np.int64)
for a in V:
    for b in V:
        if a != b and q(sub(a, b)) == 0: Q[I[a], I[b]] = 1
nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
gens = [tuple(int(c) for c in g) for g in sys.argv[2].split(";")] if len(sys.argv) > 2 and sys.argv[2] else []
H = {(0,) * 4}
for g in gens:
    H = {add(h, tuple((k * x) % 3 for x in g)) for h in H for k in range(3)}
print("|H| =", len(H), flush=True)
s = pycryptosat.Solver(threads=int(sys.argv[1]))
nv = 0
def new():
    global nv; nv += 1; return nv
# one variable per H-orbit of edges
E = {}
for a in V:
    for b in V:
        if I[a] < I[b] and Q[I[a], I[b]] and (I[a], I[b]) not in E:
            v = new()
            for h in H:
                x, y = I[add(a, h)], I[add(b, h)]
                E[(x, y)] = E[(y, x)] = v
for P in range(n):
    for R in nb[P]:
        for S in nb[P] & nb[R]:
            if P < R < S:
                vs = [E[(P, R)], E[(R, S)], E[(P, S)]]
                # repeated variables cancel in XOR
                c = {}
                for v in vs: c[v] = c.get(v, 0) ^ 1
                vs2 = [v for v, k in c.items() if k]
                if vs2: s.add_xor_clause(vs2, False)
T = {}
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        t = new(); T[(P, R)] = t; pis = []
        for Z in sorted(nb[P] & nb[R]):
            p = new()
            c = {}
            for v in (E[(P, Z)], E[(Z, R)], p): c[v] = c.get(v, 0) ^ 1
            s.add_xor_clause([v for v, k in c.items() if k], False); pis.append(p)
        s.add_xor_clause(pis + [t], False)
        for i, j in itertools.permutations(range(6), 2): s.add_clause([t, -pis[i], pis[j]])
        for k in (1, 5):
            for cc in itertools.combinations(range(6), k):
                s.add_clause([-t] + [(-pis[i] if i in cc else pis[i]) for i in range(6)])
s.add_clause(list(T.values()))       # at least one 3/3 pair (non-coboundary)
t0 = time.time(); sat, sol = s.solve()
print("H-invariant non-coboundary parity:", "SAT" if sat else "UNSAT", f"{time.time()-t0:.1f}s", flush=True)
if sat:
    print("3/3 pairs:", sum(1 for v in T.values() if sol[v]))
    import pickle; pickle.dump({k: sol[v] for k, v in E.items()}, open("parity_sym_sol.pkl", "wb"))
