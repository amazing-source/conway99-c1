"""Compute every line-triple count of BvLS (t = 10) directly and check the model of line_triples_gen (notes/99)."""
import time
import numpy as np
import sympy as sp
import graphs, rooted
from line_triples_gen import Model, R

t0 = time.time()
A = graphs.bvls()
n = len(A)
Ls = rooted.lines(A)
Lam = len(Ls)
NL = np.zeros((n, Lam), dtype=np.int64)
for j, l in enumerate(Ls):
    for p in l:
        NL[p, j] = 1
meet = NL.T @ NL
E = NL.T @ A @ NL
Id = np.eye(Lam, dtype=bool)
rel = {'s': Id.astype(np.int64), 'm': ((meet == 1) & ~Id).astype(np.int64)}
disj = meet == 0
for e in range(4):
    rel[e] = (disj & (E == e)).astype(np.int64)
tot = sum(rel[r] for r in R)
assert tot.min() == 1 and tot.max() == 1
pi_L = rel[3].sum(1)
P = int(rel[3].sum()) // 2
Q2 = int((pi_L ** 2).sum())
print(f'BvLS: {Lam} lines, P = {P}, pi(L) values {sorted(set(pi_L.tolist()))}, Q2 = {Q2}  ({time.time()-t0:.0f}s)')
Xnum = {}
for r1 in R:
    for r2 in R:
        prod = rel[r1].astype(np.float64) @ rel[r2].astype(np.float64)
        for r3 in R:
            Xnum[(r1, r2, r3)] = int(round((prod * rel[r3]).sum()))
adjN = A @ NL
inN = NL.astype(bool)
NN = (adjN == 1) & ~inN
na = np.zeros(4, dtype=np.int64)
for N in range(Lam):
    far = np.nonzero((adjN[:, N] == 0) & ~inN[:, N])[0]
    for p in far:
        cnt = 0
        for j in np.nonzero(NL[p])[0]:
            if all(NN[q, N] for q in Ls[j] if q != p):
                cnt += 1
        na[cnt] += 1
print('n_a =', na.tolist(), f'({time.time()-t0:.0f}s)')
M = Model(10)
sub = {M.P: P, M.Q2: Q2}
sub.update({M.na[a]: int(na[a]) for a in range(4)})
for ms, sym in M.X9.items():
    sub[sym] = Xnum[ms]
bad = 0
for r1 in R:
    for r2 in R:
        for r3 in R:
            mv = sp.sympify(M.X(r1, r2, r3)).subs(sub)
            if mv != Xnum[(r1, r2, r3)]:
                bad += 1
                if bad <= 10:
                    print('  X mismatch', (r1, r2, r3), 'model', mv, 'actual', Xnum[(r1, r2, r3)])
print('X mismatches:', bad)
eqbad = [(k, a, b, ex.subs(sub)) for (k, a, b, ex) in M.equations() if ex.subs(sub) != 0]
print('equation violations:', len(eqbad), eqbad[:6])
for key in ('0', 'r', 's', 'ker'):
    G = np.array([[float(sp.sympify(x).subs(sub)) for x in row] for row in M.gram(key)])
    print(f'Gram {key}: min eigenvalue {np.linalg.eigvalsh((G + G.T) / 2).min():.4g} (scale {np.abs(G).max():.3g})')
print(f'done ({time.time()-t0:.0f}s)')
import line_triples_sdp as lts
for kern in lts.kernels(M, 3):
    G = np.array([[float(sp.sympify(sum(kern[r3] * M.X(r1, r2, r3) for r3 in R)).subs(sub)) for r2 in R] for r1 in R])
    ev = np.linalg.eigvalsh((G + G.T) / 2)
    if ev.min() < -1e-8 * max(1.0, np.abs(G).max()):
        print('KERNEL VIOLATION', ev.min(), np.abs(G).max())
print('degree<=3 Hadamard kernels checked on BvLS')
