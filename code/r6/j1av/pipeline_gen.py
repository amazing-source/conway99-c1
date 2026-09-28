# Generic J1a post-pipeline for a generic-kernel run (base file with alpha per label + V rows):
#   stage 1: support-level lambda/mu rules R7, R7', C4 and the P3 tests on the kernel records (survivors + marginals);
#   stage 2: M-shell completion test (three zeros m_jk; rows known up to corners and cell; S must be PSD, rank <= 15-r).
# Usage: python pipeline_gen.py TYPE base_file records_file      TYPE in {v, iii}
import struct, sys, numpy as np
from collections import Counter
from multiprocessing import Pool
TYPE, BASEF, RECF = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(BASEF, 'rb').read(); nb = struct.unpack('<i', raw[:4])[0]
VROWS = np.array([struct.unpack('<7b', raw[4 + 7 * k: 11 + 7 * k]) for k in range(3)], dtype=float)
bases = [(struct.unpack('<12b', raw[25 + 24 * i: 37 + 24 * i]), struct.unpack('<12b', raw[37 + 24 * i: 49 + 24 * i])) for i in range(nb)]
# inner vertices (block, sign) of v1, v2, v3 read off the V rows: v = e_x - e_y  ->  (x,+), (y,-)
VIN = {k: {(int(np.argmax(VROWS[k])), 1), (int(np.argmin(VROWS[k])), -1)} for k in range(3)}
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
    alpha, g = bases[b]
    Ap = [L for L in range(12) if alpha[L] == 1]; Am = [L for L in range(12) if alpha[L] == -1]
    ed = [(Ap[i], Am[perms[q][i]]) for i in range(6)] + [(Ap[x], Ap[y]) for x, y in match6[p1]] + [(Am[x], Am[y]) for x, y in match6[p2]]
    return list(alpha), list(g), ed
def mats(alpha, g, ed):
    R = np.zeros((15, 7))
    for L in range(12):
        K = L // 2 + 1; s = 1 if L % 2 == 0 else -1
        R[L, 0] = alpha[L]; R[L, K] = alpha[L] * s
    R[12:15] = VROWS
    G = np.zeros((15, 15))
    for L in range(12): G[L, 12 + g[L]] = G[12 + g[L], L] = 1
    for x, y in [(12, 13), (13, 14), (12, 14)]: G[x, y] = G[y, x] = 1
    for x, y in ed: G[x, y] = G[y, x] = 1
    return R, G
def lam_mu_ok(alpha, g, ed):
    nbr = {L: [] for L in range(12)}
    for x, y in ed: nbr[x].append(y); nbr[y].append(x)
    def pos_inner(L):
        K = L // 2 + 1; s = 1 if L % 2 == 0 else -1; return (K, alpha[L] * s)
    def neg_inner(L):
        K, t = pos_inner(L); return (K, -t)
    for W in range(12):
        j = g[W]
        for k in range(3):
            n_in_k = sum(1 for X in nbr[W] if g[X] == k)
            sh = 1 if pos_inner(W) in VIN[k] else 0
            if k != j and n_in_k + sh > 1: return 'R7'
            if k == j and n_in_k + sh > 2: return "R7'"
    for L in range(12):
        for M in range(L + 1, 12):
            if g[L] != g[M] or alpha[L] == alpha[M]: continue
            if len(set(nbr[L]) & set(nbr[M])) + (1 if neg_inner(L) == neg_inner(M) else 0) > 1: return 'C4'
    return None
def roots_of(signed_blocks):
    # all roots s1 e_b1 + s2 e_b2 whose two signed blocks lie in the allowed set (b1 != b2)
    out = []
    for (b1, s1) in signed_blocks:
        for (b2, s2) in signed_blocks:
            if b1 < b2:
                v = np.zeros(7); v[b1] = s1; v[b2] = s2; out.append(v)
    return out
PM = lambda bs: [(b, 1) for b in bs] + [(b, -1) for b in bs]
if TYPE == 'v':      # m's lie in cells inside {4,5,6}
    MROOTS = {(0, 1): roots_of(PM([4, 5, 6])), (0, 2): roots_of(PM([4, 5, 6])), (1, 2): roots_of(PM([4, 5, 6]))}
else:                # (iii): blocks 1=d,2=e,3=f,4=g,5=h,6=i;  m12 in {d-,h,i}, m23 in {g+,h,i}, m13 in {d-,g+,h,i}
    MROOTS = {(0, 1): roots_of([(1, -1)] + PM([5, 6])), (1, 2): roots_of([(4, 1)] + PM([5, 6])),
              (0, 2): roots_of([(1, -1), (4, 1)] + PM([5, 6]))}
TOL = 1e-6
def m_options(alpha, g, j, k):
    l = 3 - j - k
    Gj = [L for L in range(12) if g[L] == j]; Gk = [L for L in range(12) if g[L] == k]; Gl = [L for L in range(12) if g[L] == l]
    Glp = [L for L in Gl if alpha[L] == -1]; Glm = [L for L in Gl if alpha[L] == 1]
    for cj in Gj:
        for ck in Gk:
            if alpha[cj] == alpha[ck]: continue
            for cp in Glp:
                for cm in Glm:
                    x = np.zeros(15); x[[cj, ck, cp, cm]] = -1; x[12 + j] = 1; x[12 + k] = 1
                    for r in MROOTS[(j, k)]: yield x, r
def full_test(rec):
    b, q, p1, p2, kind = rec
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed); Ra = np.abs(R); I = np.eye(15); J = np.ones((15, 15))
    if np.linalg.eigvalsh(12 * I - 3 * G - R @ R.T)[0] < -TOL: return (rec, 'T3o')
    if np.linalg.eigvalsh(60 * I + 15 * G - 3 * Ra @ Ra.T - 4 * J)[0] < -TOL: return (rec, 'T3e')
    lm = lam_mu_ok(alpha, g, ed)
    if lm: return (rec, lm)
    MU = 12 * I + 4 * G - R @ R.T
    w, V = np.linalg.eigh(MU); keep = w > 1e-7; rk = int(np.sum(keep))
    if w[0] < -TOL: return (rec, 'odd not PSD (marginal record confirmed)')
    P = (V[:, keep] / w[keep]) @ V[:, keep].T
    good = {}
    for jk in [(0, 1), (0, 2), (1, 2)]:
        lst = []
        for x, r in m_options(alpha, g, *jk):
            m = -4 * x - R @ r
            s2 = 10 - m @ P @ m
            if s2 >= -TOL: lst.append((m, r, s2))
        if not lst: return (rec, 'M-shell: no option for m%d%d' % (jk[0] + 1, jk[1] + 1))
        good[jk] = lst
    A, B, C = good[(0, 1)], good[(0, 2)], good[(1, 2)]
    for o1 in A:
        for o2 in B:
            g12 = -(o1[1] @ o2[1]) - o1[0] @ P @ o2[0]
            if g12 * g12 > o1[2] * o2[2] + TOL: continue
            for o3 in C:
                g13 = -(o1[1] @ o3[1]) - o1[0] @ P @ o3[0]; g23 = -(o2[1] @ o3[1]) - o2[0] @ P @ o3[0]
                ws = np.linalg.eigvalsh(np.array([[o1[2], g12, g13], [g12, o2[2], g23], [g13, g23, o3[2]]]))
                if ws[0] >= -TOL and int(np.sum(ws > TOL)) <= 15 - rk:
                    return (rec, 'SURVIVES M-shell')
    return (rec, 'M-shell: no consistent triple')
if __name__ == '__main__':
    recs = [tuple(map(int, l.split()[:5])) for l in open(RECF)]
    with Pool(16) as pool:
        res = pool.map(full_test, recs, chunksize=32)
    c = Counter(r[1] for r in res)
    print(TYPE, RECF, 'records:', len(res))
    for k, v in c.most_common(): print('  %-42s %d' % (k, v))
    with open(RECF.replace('.txt', '_pipeline_survivors.txt'), 'w') as f:
        for r in res:
            if r[1] == 'SURVIVES M-shell': f.write('%d %d %d %d %d\n' % r[0])
