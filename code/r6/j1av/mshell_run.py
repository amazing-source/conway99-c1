# M-shell completion test on ALL J1a(v) support survivors (proof run; conservative tolerances).
# For each survivor (support U = 12 star labels + 3 V's, odd Gram M_U = 12I + 4G - RR^T of rank r):
#   every option (corners, cell) of each zero m_jk gives a row m_W = -4 T_{WU} - R_U r_W, and for the three m's together
#   S_{WW'} = M_{WW'} - m_W^T M_U^+ m_{W'} (M_WW = 10, M_WW' = -(r_W, r_W') since T = 0 between m's) must be PSD of rank
#   <= 15 - r.  A survivor is KILLED if no admissible triple exists.
# Conservative numerics: an option is rejected only if S_WW < -1e-6; a triple is accepted if lambda_min(S) >= -1e-6 and
# the number of eigenvalues > 1e-6 is <= 15 - r  (so borderline cases are kept, never killed).
import numpy as np, sys
from multiprocessing import Pool
exec(open('postfilter.py').read().split('recs = [tuple')[0])
ROOTS = []
for b1, b2 in [(4, 5), (4, 6), (5, 6)]:
    for s1 in (1, -1):
        for s2 in (1, -1):
            v = np.zeros(7); v[b1] = s1; v[b2] = s2; ROOTS.append(v)
TOL = 1e-6
def options(alpha, g, j, k):
    l = 3 - j - k
    Gj = [L for L in range(12) if g[L] == j]; Gk = [L for L in range(12) if g[L] == k]; Gl = [L for L in range(12) if g[L] == l]
    Glp = [L for L in Gl if alpha[L] == -1]; Glm = [L for L in Gl if alpha[L] == 1]
    for cj in Gj:
        for ck in Gk:
            if alpha[cj] == alpha[ck]: continue
            for cp in Glp:
                for cm in Glm:
                    x = np.zeros(15); x[[cj, ck, cp, cm]] = -1; x[12 + j] = 1; x[12 + k] = 1
                    for r in ROOTS: yield x, r
def test(rec):
    b, q, p1, p2, kind = rec
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed)
    MU = 12 * np.eye(15) + 4 * G - R @ R.T
    w, V = np.linalg.eigh(MU); keep = w > 1e-7; rk = int(np.sum(keep))
    P = (V[:, keep] / w[keep]) @ V[:, keep].T
    good = {}
    for (j, k) in [(0, 1), (0, 2), (1, 2)]:
        lst = []
        for x, r in options(alpha, g, j, k):
            m = -4 * x - R @ r
            s2 = 10 - m @ P @ m
            if s2 >= -TOL: lst.append((m, r, s2))
        good[(j, k)] = lst
        if not lst: return (rec, rk, 'no option for m%d%d' % (j + 1, k + 1), 0)
    ntr = 0
    A, B, C = good[(0, 1)], good[(0, 2)], good[(1, 2)]
    for o1 in A:
        for o2 in B:
            g12 = -(o1[1] @ o2[1]) - o1[0] @ P @ o2[0]
            if g12 * g12 > o1[2] * o2[2] + TOL: continue
            for o3 in C:
                g13 = -(o1[1] @ o3[1]) - o1[0] @ P @ o3[0]
                g23 = -(o2[1] @ o3[1]) - o2[0] @ P @ o3[0]
                S = np.array([[o1[2], g12, g13], [g12, o2[2], g23], [g13, g23, o3[2]]])
                ws = np.linalg.eigvalsh(S)
                if ws[0] >= -TOL and int(np.sum(ws > TOL)) <= 15 - rk:
                    ntr += 1
    return (rec, rk, 'killed (no consistent triple)' if ntr == 0 else 'SURVIVES', ntr)
if __name__ == '__main__':
    recs = [tuple(map(int, l.split())) for l in open(sys.argv[1])]
    with Pool(16) as pool:
        res = pool.map(test, recs, chunksize=32)
    from collections import Counter
    c = Counter(r[2] for r in res)
    print('records tested:', len(res))
    for k, v in c.most_common(): print('  %-34s %d' % (k, v))
    surv = [r for r in res if r[2] == 'SURVIVES']
    with open('mshell_survivors.txt', 'w') as f:
        for r in surv: f.write('%d %d %d %d %d %d\n' % (r[0] + (r[3],)))
    print('M-shell survivors written:', len(surv))
