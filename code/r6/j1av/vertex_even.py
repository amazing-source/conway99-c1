# Vertex-level sigma-even test (hand-derived, notes/151 s8):
# the sigma-even (-4)-eigenspace of A is 22-dimensional, so 63 P_{-4} restricted to the 23 sigma-even coordinates
# {sqrt2 e_x, (e_{b+}+e_{b-})/sqrt2 (7 blocks), (e_l+e_{sigma l})/sqrt2 (15 support labels)} must be PSD of rank <= 22.
# In these coordinates the matrix is the INTEGER matrix
#   [[56, -16*1_7^T, 2*1_15^T], [-16*1_7, 18I+2J, 2J-9|R|^T], [2*1_15, 2J-9|R|, 27I+2J-9G]]      (D_UU = 0 in J1a)
# so det = 0 exactly (Bareiss) is necessary.  Usage: python vertex_even.py records_file [random N]
import struct, sys, random, numpy as np
from fractions import Fraction
from multiprocessing import Pool
raw = open('base.bin', 'rb').read(); nb = struct.unpack('<i', raw[:4])[0]
bases = [struct.unpack('<6b12b', raw[4 + 18 * i: 22 + 18 * i]) for i in range(nb)]
perms = []
def gen(arr, k):
    if k == 6: perms.append(arr[:]); return
    for i in range(k, 6):
        arr[k], arr[i] = arr[i], arr[k]; gen(arr, k + 1); arr[k], arr[i] = arr[i], arr[k]
gen(list(range(6)), 0)
match6 = []
for j in range(1, 6):
    rest = [x for x in range(1, 6) if x != j]
    for t in [((rest[0], rest[1]), (rest[2], rest[3])), ((rest[0], rest[2]), (rest[1], rest[3])), ((rest[0], rest[3]), (rest[1], rest[2]))]:
        match6.append([(0, j), t[0], t[1]])
def config(b, q, p1, p2):
    rec = bases[b]; a, g = rec[:6], rec[6:]
    alpha = [a[L // 2] for L in range(12)]
    Ap = [L for L in range(12) if alpha[L] == 1]; Am = [L for L in range(12) if alpha[L] == -1]
    ed = [(Ap[i], Am[perms[q][i]]) for i in range(6)] + [(Ap[x], Ap[y]) for x, y in match6[p1]] + [(Am[x], Am[y]) for x, y in match6[p2]]
    return alpha, list(g), ed
def Mve(alpha, g, ed):
    Ra = np.zeros((15, 7), dtype=np.int64)
    for L in range(12):
        K = L // 2 + 1; Ra[L, 0] = 1; Ra[L, K] = 1
    Ra[12, 1] = Ra[12, 2] = Ra[13, 2] = Ra[13, 3] = Ra[14, 3] = Ra[14, 1] = 1
    G = np.zeros((15, 15), dtype=np.int64)
    for L in range(12): G[L, 12 + g[L]] = G[12 + g[L], L] = 1
    for x, y in [(12, 13), (13, 14), (12, 14)]: G[x, y] = G[y, x] = 1
    for x, y in ed: G[x, y] = G[y, x] = 1
    M = np.zeros((23, 23), dtype=np.int64)
    M[0, 0] = 56; M[0, 1:8] = M[1:8, 0] = -16; M[0, 8:] = M[8:, 0] = 2
    M[1:8, 1:8] = 18 * np.eye(7, dtype=np.int64) + 2
    M[1:8, 8:] = 2 - 9 * Ra.T; M[8:, 1:8] = 2 - 9 * Ra
    M[8:, 8:] = 27 * np.eye(15, dtype=np.int64) + 2 - 9 * G
    return M
def bareiss_det(M):
    A = [[int(x) for x in row] for row in M]; n = len(A); sign = 1; prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None: return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]
def evaluate(rec):
    b, q, p1, p2 = rec[:4]
    M = Mve(*config(b, q, p1, p2))
    w = np.linalg.eigvalsh(M.astype(float))
    return (rec, bareiss_det(M), w[0], np.sum(np.abs(w) < 1e-7))
if __name__ == '__main__':
    if sys.argv[1] == 'random':
        random.seed(3); recs = [(random.randrange(nb), random.randrange(720), random.randrange(15), random.randrange(15), -1) for _ in range(int(sys.argv[2]))]
    else:
        recs = [tuple(map(int, l.split())) for l in open(sys.argv[1])]
    with Pool(16) as pool:
        res = pool.map(evaluate, recs, chunksize=64)
    nz = [r for r in res if r[1] != 0]; zero = [r for r in res if r[1] == 0]
    print('configurations:', len(res), '  det != 0 (KILLED by the vertex sigma-even rank bound):', len(nz), '  det == 0:', len(zero))
    if zero:
        psd = sum(1 for r in zero if r[2] > -1e-7)
        print('  among det==0: PSD', psd, ' not PSD', len(zero) - psd, '  nullity histogram', np.bincount([r[3] for r in zero]))
        with open('vertex_even_left.txt', 'w') as f:
            for r in zero:
                if r[2] > -1e-7: f.write('%d %d %d %d %d\n' % r[0])
    print('sample dets:', [r[1] for r in res[:6]])
