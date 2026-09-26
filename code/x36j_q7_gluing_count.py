"""Dimension count for the q:7 gluing heuristic: number of independent near-entry functionals on symmetric forms
on F^42 vanishing on row(B) (i.e. on Sym^2(B^perp)).  Gauge: orbits (a,+)(b,eps), a<b."""
import numpy as np, itertools
blocks = range(7)
orbs = [((a, b), e) for a, b in itertools.combinations(blocks, 2) for e in (1, -1)]
n = len(orbs)
B = np.zeros((7, n))
for j, ((a, b), e) in enumerate(orbs):
    B[a, j] = 1; B[b, j] = e
assert np.allclose(B @ B.T, 12 * np.eye(7))
Pi = np.eye(n) - B.T @ B / 12
near = [(i, j) for i in range(n) for j in range(i, n) if set(orbs[i][0]) & set(orbs[j][0])]
print('near pairs (incl. diagonal):', len(near))
# symmetric tensor of Pi e_i, Pi e_j, vectorized on upper triangle
iu = np.triu_indices(n)
rows = []
for i, j in near:
    u, v = Pi[:, i], Pi[:, j]
    T = (np.outer(u, v) + np.outer(v, u)) / 2
    rows.append(T[iu])
R = np.array(rows)
r = np.linalg.matrix_rank(R, tol=1e-8)
print('independent near functionals on Sym^2(B^perp):', r, ' (Sym^2(B^perp) has dim', 35 * 36 // 2, ')')
for rk in (11, 13, 14, 15):
    print('rank', rk, ': variety dim', 35 * rk - rk * (rk - 1) // 2, ' expected completion dim', 35 * rk - rk * (rk - 1) // 2 - r)

print('--- sub-configurations: s stars (blocks 0..s-1), principal submatrix on roots meeting them ---')
for s in range(3, 8):
    S = set(range(s))
    sub = [j for j, ((a, b), e) in enumerate(orbs) if a in S or b in S]
    m = len(sub)
    Bs = B[:s][:, sub]
    Pis = np.eye(m) - Bs.T @ np.linalg.inv(Bs @ Bs.T) @ Bs
    nearS = [(i, j) for i in range(m) for j in range(i, m) if set(orbs[sub[i]][0]) & set(orbs[sub[j]][0])]
    iu2 = np.triu_indices(m)
    RR = np.array([((np.outer(Pis[:, i], Pis[:, j]) + np.outer(Pis[:, j], Pis[:, i])) / 2)[iu2] for i, j in nearS])
    rS = np.linalg.matrix_rank(RR, tol=1e-8)
    q = m - s
    out = []
    for rk in (11, 13):
        out.append('rank %d: excess %d' % (rk, rS - (q * rk - rk * (rk - 1) // 2)))
    print('s=%d: orbits %d, quotient dim %d, near entries %d, independent %d;' % (s, m, q, len(nearS), rS), '; '.join(out))
