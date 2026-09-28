# Exploratory probe (not the proof run): M-shell completion test on J1a(v) support survivors.
# For a survivor with odd support Gram M_U (rank r), each extra label W has row m_W = -4 T_{WU} - R_U r_W, and for any
# set of extra labels the Schur complement S_{WW'} = M_{WW'} - m_W^T M_U^+ m_{W'} must be PSD of rank <= 15 - r,
# with M_{WW} = 10 and M_{WW'} = -4 T_{WW'} - (r_W, r_{W'}).
# m_jk (j<k): T = +1 on V_j, V_k; T = -1 on its 4 corner labels: one in G_j, one in G_k, two in G_l (one per c-side),
#   2 corners with A-root in O_{c+} (alpha=-1) and 2 in O_{c-} (alpha=+1);  r_m = a root of a cell inside {4,5,6}.
#   Between m's: T = 0 (M independent, m_jk not adjacent to sigma m).
import numpy as np, itertools, sys, random
from collections import Counter
exec(open('postfilter.py').read().split('recs = [tuple')[0])
recs = [tuple(map(int, l.split())) for l in open('vertex_even_left.txt')]
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
sample = random.sample(recs, int(sys.argv[2]) if len(sys.argv) > 2 else 20)
ROOTS = []
for b1, b2 in [(4, 5), (4, 6), (5, 6)]:
    for s1 in (1, -1):
        for s2 in (1, -1):
            v = np.zeros(7); v[b1] = s1; v[b2] = s2; ROOTS.append(v)
def options(alpha, g, j, k):
    l = 3 - j - k
    Gj = [L for L in range(12) if g[L] == j]; Gk = [L for L in range(12) if g[L] == k]; Gl = [L for L in range(12) if g[L] == l]
    Glp = [L for L in Gl if alpha[L] == -1]; Glm = [L for L in Gl if alpha[L] == 1]
    out = []
    for cj in Gj:
        for ck in Gk:
            if alpha[cj] == alpha[ck]: continue          # c-side balance: G_j and G_k corners on opposite sides
            for cp in Glp:
                for cm in Glm:
                    x = np.zeros(15); x[[cj, ck, cp, cm]] = -1; x[12 + j] = 1; x[12 + k] = 1
                    for r in ROOTS: out.append((x, r))
    return out
stat = Counter(); killed = 0
for (b, q, p1, p2, kind) in sample:
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed)
    MU = 12 * np.eye(15) + 4 * G - R @ R.T
    w, V = np.linalg.eigh(MU); rk = int(np.sum(w > 1e-7))
    P = sum(np.outer(V[:, i], V[:, i]) / w[i] for i in range(15) if w[i] > 1e-7)
    good = {}
    for (j, k) in [(0, 1), (0, 2), (1, 2)]:
        lst = []
        for x, r in options(alpha, g, j, k):
            m = -4 * x - R @ r
            s2 = 10 - m @ P @ m
            if s2 > -1e-9: lst.append((m, r, s2))
        good[(j, k)] = lst
    counts = tuple(len(good[jk]) for jk in [(0, 1), (0, 2), (1, 2)])
    # triple consistency: Schur complement 3x3 PSD with rank <= 15 - rk
    ok = 0
    if min(counts) > 0:
        for o1 in good[(0, 1)]:
            for o2 in good[(0, 2)]:
                g12 = -(o1[1] @ o2[1]) - o1[0] @ P @ o2[0]
                if g12 * g12 > o1[2] * o2[2] + 1e-9: continue
                for o3 in good[(1, 2)]:
                    S = np.array([[o1[2], g12, -(o1[1] @ o3[1]) - o1[0] @ P @ o3[0]],
                                  [g12, o2[2], -(o2[1] @ o3[1]) - o2[0] @ P @ o3[0]],
                                  [0, 0, o3[2]]])
                    S[2, 0] = S[0, 2]; S[2, 1] = S[1, 2]
                    ws = np.linalg.eigvalsh(S)
                    if ws[0] > -1e-9 and int(np.sum(ws > 1e-7)) <= 15 - rk:
                        ok += 1
    stat[(rk, counts, ok > 0)] += 1
    killed += (ok == 0)
    print('survivor b=%d q=%d p1=%d p2=%d rank %d  options per m (after s2>=0) %s  consistent triples %d' % (b, q, p1, p2, rk, counts, ok))
print('sample', len(sample), ' killed by the M-shell test:', killed)
