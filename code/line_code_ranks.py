# notes/110 sec. 3. Sanity check of the "line code contains its dual" lemma on BvLS srg(243,22,1,2) (t+1 = 11 lines per point).
# Predicted: rank_2(N) >= 133 + 55 = 188 (even part V_{-5}, dim 110); rank_5(N) >= 111 + 66 = 177 (V_4, dim 132).
import sys, itertools, numpy as np
sys.path.insert(0, '.')
import graphs

def rank_mod(M, p):
    M = np.array(M, dtype=np.int64) % p
    r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0: continue
        i = r + nz[0]
        M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        col = M[:, c].copy(); col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size: M[nzr] = (M[nzr] - np.outer(col[nzr], M[r])) % p
        r += 1
        if r == rows: break
    return r

def lines_of(A):
    n = len(A); L = set()
    for u in range(n):
        for v in np.nonzero(A[u])[0]:
            if v > u:
                w = [x for x in np.nonzero(A[u] & A[v])[0]]
                assert len(w) == 1
                L.add(tuple(sorted((u, int(v), int(w[0])))))
    return sorted(L)

A = graphs.bvls()
L = lines_of(A)
n = len(A); print('lines', len(L))
N = np.zeros((n, len(L)), dtype=np.int64)
for j, l in enumerate(L):
    for p in l: N[p, j] = 1
assert ((N @ N.T) == 11 * np.eye(n, dtype=np.int64) + A).all()
for p in (2, 5, 3, 7, 11):
    print(f'p={p}: rank N = {rank_mod(N, p)}, rank NN^T = {rank_mod(N @ N.T, p)}')
