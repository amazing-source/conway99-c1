# Sanity check of the triangle-rooted spectral relation on BvLS = srg(243,22,1,2):
# for a triangle T: F = far set, M = graph on N_1(T), S = N_1 x F adjacency.
# Claim: SF + MS + S = 2J ; spec(F) \ {k-6, r, s} = -1 - spec(M on block-zero-sum space) \ {r, s}.
import itertools, numpy as np
# ternary Golay: generator g(x) = x^5 + x^4 - x^3 + x^2 - 1  (coefficients low->high)
g = [-1, 0, 1, -1, 1, 1]
def polymod(p):
    p = [c % 3 for c in p]
    while len(p) >= 6:
        c = p[-1]
        if c:
            sh = len(p) - 6
            for i, gi in enumerate(g):
                p[sh + i] = (p[sh + i] - c * gi) % 3
        p.pop()
    return tuple(p + [0] * (5 - len(p)))
H = [polymod([0] * i + [1]) for i in range(11)]
S = set()
for h in H:
    S.add(h); S.add(tuple((-c) % 3 for c in h))
assert len(S) == 22 and (0,)*5 not in S
V = list(itertools.product(range(3), repeat=5)); idx = {v: i for i, v in enumerate(V)}
n = len(V)
A = np.zeros((n, n), dtype=int)
for v in V:
    for s in S:
        w = tuple((a + b) % 3 for a, b in zip(v, s))
        A[idx[v], idx[w]] = 1
A2 = A @ A
I = np.eye(n, dtype=int); J = np.ones((n, n), dtype=int)
assert (A2 == 20 * I - A + 2 * J).all(), 'not srg(243,22,1,2)'
print('BvLS ok: srg(243,22,1,2)')
# a triangle through 0
x = 0; nb = np.nonzero(A[x])[0]
y = nb[0]; z = [w for w in nb if A[y, w]][0]
T = [x, y, z]
N1 = {t: [w for w in np.nonzero(A[t])[0] if w not in T] for t in T}
far = [w for w in range(n) if w not in T and not any(A[w, t] for t in T)]
order = N1[x] + N1[y] + N1[z]
M = A[np.ix_(order, order)].astype(float)
F = A[np.ix_(far, far)].astype(float)
Sm = A[np.ix_(order, far)].astype(float)
print('|N1| =', len(order), ' |F| =', len(far), ' M cubic:', set(M.sum(1)), ' F degree:', set(F.sum(1)))
lhs = Sm @ F + M @ Sm + Sm
print('SF + MS + S == 2J :', np.allclose(lhs, 2))
# block-zero-sum space V0
m = len(order) // 3
B = np.zeros((len(order), 3))
for i in range(3): B[i*m:(i+1)*m, i] = 1
Q, _ = np.linalg.qr(np.hstack([B, np.random.randn(len(order), len(order) - 3)]))
V0 = Q[:, 3:]
muV0 = np.sort(np.linalg.eigvalsh(V0.T @ M @ V0))
evF = np.sort(np.linalg.eigvalsh(F))
r, s = 4, -5
pred = sorted([-1 - mu for mu in muV0 if abs(mu*mu + mu - 20) > 1e-6])
rest = [e for e in evF if abs(e - 16) > 1e-6 and abs(e - r) > 1e-6 and abs(e - s) > 1e-6]
print('#F eigenvalues other than 16, r, s:', len(rest), ' predicted:', len(pred))
print('max |difference| :', np.max(np.abs(np.array(sorted(rest)) - np.array(pred))) if len(rest) == len(pred) else 'length mismatch')
print('mult r in F:', sum(abs(e - r) < 1e-6 for e in evF), ' mult s in F:', sum(abs(e - s) < 1e-6 for e in evF))
