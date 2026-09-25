"""notes/103 sec. 9: which functions f : AGL(2,2) -> F_2 give a CONSTANT parity sum_R f(psi_R) over all 58 fact-C
solutions?  (Coordinates: P = (s_i, s_j), P' = (s_i, s_k).)  Compute the solution space and the constants."""
import itertools
import numpy as np

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]
target = {u: {z: (1 if z[0] == u[0] else 2) for z in V} for u in V}
img = [[V.index(f[u]) for u in V] for f in bij]
sols = []
for ms in itertools.combinations_with_replacement(range(24), 6):
    ok = True
    for a, u in enumerate(V):
        c = [0, 0, 0, 0]
        for t in ms:
            c[img[t][a]] += 1
        if any(c[b] != target[u][z] for b, z in enumerate(V)):
            ok = False; break
    if ok:
        v = np.zeros(24, dtype=np.int64)
        for t in ms:
            v[t] += 1
        sols.append(v % 2)
S = np.array(sols)
D = (S[1:] + S[0]) % 2                     # differences


def rank2(M):
    M = M.copy() % 2; r = 0
    for c in range(M.shape[1]):
        p = next((i for i in range(r, M.shape[0]) if M[i, c]), None)
        if p is None:
            continue
        M[[r, p]] = M[[p, r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]:
                M[i] = (M[i] + M[r]) % 2
        r += 1
    return r


rD = rank2(D)
print('solutions', len(S), '; rank of differences', rD, '-> dim of F (functions with constant parity) =', 24 - rD)
# is the constant ever 1?  f in D-perp with <f, S0> = 1 exists iff S0 not in span(D)
print('S0 in span(differences)?', rank2(np.vstack([D, S[:1]])) == rD,
      ' => an f with constant 1 exists iff this is False')

# explicit description: label each affine map by (S3 type of its linear part, translation t)
add = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
name = {(0, 1): 'i', (1, 0): 'o', (1, 1): 'A'}
def lab(f):
    t = f[(0, 0)]
    L = ''.join(name[add(f[v], t)] for v in [(1, 1), (0, 1), (1, 0)])
    return L + '+' + ''.join(map(str, t))
labels = [lab(f) for f in bij]
# nullspace of D (functions f with D f = 0), over F_2
def nullspace(M):
    M = M.copy() % 2; n = M.shape[1]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, M.shape[0]) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] = (M[i] + M[r]) % 2
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]; basis = []
    for fc in free:
        v = np.zeros(n, dtype=np.int64); v[fc] = 1
        for i, pc in enumerate(piv):
            if M[i, fc]: v[pc] = 1
        basis.append(v)
    return basis
B = nullspace(D)
print('basis of F (maps where f = 1), with its constant <f, S0>:')
for v in B:
    print('  c=%d' % (int(v @ S[0]) % 2), sorted(labels[i] for i in range(24) if v[i]))
