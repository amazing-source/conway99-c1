# J1a (iii): second shell (apex A13, t=1 zeros u1,u2,u2',u3, D-partners D1,D2,D3) on the 16 M-shell survivors.
# For every label of the shell, enumerate its possible rows to the support U (corners + cell), using only certain local rules:
#   u ~ v_k only:   +1 at V_k; corners = 3 A-roots + 1 sigmaA-root (a D-pair on one label allowed -> entry 0);
#                   c_k(u) <= 1 (lambda with v_k), c_i(u) <= 2; 2 corners in O_c+ and 2 in O_c-; u not in O(inner of v_k).
#   D_k ~ v_k, sigma v_k:  0 at every V; corners 2 A + 2 sigmaA; c_k, sc_k <= 1 (lambda); c_i, sc_i <= 1 (i != k, mu with
#                   common nbr sigma v_k / v_k); 2+2 sides; not in O(inner of v_k) nor O(inner of sigma v_k).
#   A13 ~ v1, sigma v3: +1 at V1, -1 at V3; corners 2 A + 2 sigmaA; c_1 = 0, c_2 <= 1, sc_3 = 0, sc_2 <= 1; 2+2 sides;
#                   not in O(d+), O(e-), O(f-), O(g+).
# A row m_Y = -4 x - R_U r_Y is admissible only if (K) m_Y . z = 0 EXACTLY for every z in ker M_U, and
# (B) BUD - m_Y m_Y^T is PSD, where BUD = 28 M_U - M_U^2 - (the M-triple's m m^T).  A survivor dies if some label has no row.
import sys, itertools, numpy as np, sympy as sp
sys.argv = ['x', 'iii', 'base_iii.bin', 'iii_records_pipeline_survivors.txt']
exec(open('pipeline_gen.py').read().split("if __name__ == '__main__':")[0])
TOL = 1e-6
VINNER = {0: [(1, 1), (2, -1)], 1: [(2, 1), (3, -1)], 2: [(3, 1), (4, -1)]}      # inner vertices of v1, v2, v3
SINNER = {k: [(b, -s) for (b, s) in VINNER[k]] for k in range(3)}             # inner vertices of sigma v_k
ALLROOTS = []
for b1 in range(1, 7):
    for b2 in range(b1 + 1, 7):
        for s1 in (1, -1):
            for s2 in (1, -1):
                v = np.zeros(7, dtype=np.int64); v[b1] = s1; v[b2] = s2; ALLROOTS.append(((b1, s1), (b2, s2), v))
def cells_avoiding(forbidden, used_labels):
    out = []
    for sb1, sb2, v in ALLROOTS:
        if sb1 in forbidden or sb2 in forbidden: continue
        key = tuple(v) if v[np.nonzero(v)[0][0]] > 0 else tuple(-v)     # label = {v, -v}
        if key in used_labels: continue
        out.append(v)
    return out
def star_rootinfo(alpha):
    # for each label L: A-root side (c-sign) and sigmaA-root side
    info = {}
    for L in range(12):
        info[L] = {'A_side': -alpha[L], 'S_side': alpha[L]}   # rep (c+) has h = alpha: A-root in O_c+ iff alpha = -1
    return info
def row_options(alpha, g, nA, nS, vrow, cmax, scmax):
    # corners: nA A-labels (-1) and nS sigmaA-labels (+1); a label may carry both (D-pair -> 0); side balance 2+2
    info = star_rootinfo(alpha); labs = range(12)
    for Aset in itertools.combinations(labs, nA):
        cnt = [0, 0, 0]
        for L in Aset: cnt[g[L]] += 1
        if any(cnt[k] > cmax[k] for k in range(3)): continue
        for Sset in itertools.combinations(labs, nS):
            scnt = [0, 0, 0]
            for L in Sset: scnt[g[L]] += 1
            if any(scnt[k] > scmax[k] for k in range(3)): continue
            plus = sum(1 for L in Aset if info[L]['A_side'] == 1) + sum(1 for L in Sset if info[L]['S_side'] == 1)
            if plus != 2: continue
            x = np.zeros(15, dtype=np.int64)
            for L in Aset: x[L] -= 1
            for L in Sset: x[L] += 1
            x[12:15] = vrow
            yield x
def main():
    recs = [tuple(map(int, l.split()[:5])) for l in open('iii_records_pipeline_survivors.txt')]
    for rec in recs:
        b, q, p1, p2, kind = rec
        alpha, g, ed = config(b, q, p1, p2)
        R, G = mats(alpha, g, ed); Ri = R.astype(np.int64)
        MU = (12 * np.eye(15) + 4 * G - R @ R.T).astype(np.int64)
        ker = [np.array([int(x * sp.ilcm(*[y.q for y in v])) for x in v], dtype=np.int64) for v in sp.Matrix(MU.tolist()).nullspace()]
        w, V = np.linalg.eigh(MU.astype(float)); keep = w > 1e-7; rk = int(np.sum(keep)); P = (V[:, keep] / w[keep]) @ V[:, keep].T
        BUD = 28 * MU - MU @ MU
        # the unique M-triple (recompute with the strict rules)
        good = {}
        for jk in [(0, 1), (0, 2), (1, 2)]:
            lst = []
            for x, r in m_options(alpha, g, *jk):
                mi = (-4 * x - R @ r).astype(np.int64)
                if any(int(mi @ z) != 0 for z in ker): continue
                if 10 - mi @ P @ mi < -TOL: continue
                lst.append((mi, r))
            good[jk] = lst
        triples = []
        for o1 in good[(0, 1)]:
            for o2 in good[(0, 2)]:
                for o3 in good[(1, 2)]:
                    Bp = BUD - np.outer(o1[0], o1[0]) - np.outer(o2[0], o2[0]) - np.outer(o3[0], o3[0])
                    if np.linalg.eigvalsh(Bp.astype(float))[0] < -TOL: continue
                    ms = [o1, o2, o3]
                    S = np.array([[(10 if i == j else -(ms[i][1] @ ms[j][1])) - ms[i][0] @ P @ ms[j][0] for j in range(3)] for i in range(3)], dtype=float)
                    ws = np.linalg.eigvalsh(S)
                    if ws[0] < -TOL or int(np.sum(ws > TOL)) > 15 - rk: continue
                    triples.append((o1, o2, o3, Bp))
        used = set()
        for (o1, o2, o3, Bp) in triples[:1]:
            for o in (o1, o2, o3):
                v = o[1].astype(np.int64); used.add(tuple(v) if v[np.nonzero(v)[0][0]] > 0 else tuple(-v))
        verdict = []
        for (o1, o2, o3, Bp) in triples:
            specs = {
                'u1':  (3, 1, np.array([1, 0, 0]), [1, 2, 2], [1, 1, 1], VINNER[0]),
                'u2':  (3, 1, np.array([0, 1, 0]), [2, 1, 2], [1, 1, 1], VINNER[1]),
                'u3':  (3, 1, np.array([0, 0, 1]), [2, 2, 1], [1, 1, 1], VINNER[2]),
                'D1':  (2, 2, np.array([0, 0, 0]), [1, 1, 1], [1, 1, 1], VINNER[0] + SINNER[0]),
                'D2':  (2, 2, np.array([0, 0, 0]), [1, 1, 1], [1, 1, 1], VINNER[1] + SINNER[1]),
                'D3':  (2, 2, np.array([0, 0, 0]), [1, 1, 1], [1, 1, 1], VINNER[2] + SINNER[2]),
                'A13': (2, 2, np.array([1, 0, -1]), [0, 1, 2], [2, 1, 0], [(1, 1), (2, -1), (3, -1), (4, 1)]),
            }
            TALLOW = {'u1': [[0, -1], [0, -1], [0]], 'u2': [[0, -1], [0], [0, -1]], 'u3': [[0], [0, -1], [0, -1]],
                      'D1': [[0], [0], [0]], 'D2': [[0], [0], [0]], 'D3': [[0], [0], [0]], 'A13': [[0, 1, -1]] * 3}
            counts = {}
            for name, (nA, nS, vrow, cmax, scmax, forb) in specs.items():
                cells = cells_avoiding(set(forb), used)
                n = 0
                for x in row_options(alpha, g, nA, nS, vrow, cmax, scmax):
                    base = -4 * x
                    for r in cells:
                        mi = base - Ri @ r
                        if any(int(mi @ z) != 0 for z in ker): continue
                        mf = mi.astype(float)
                        if 10 - mf @ P @ mf < -TOL: continue
                        if np.linalg.eigvalsh((Bp - np.outer(mi, mi)).astype(float))[0] < -TOL: continue
                        ms = [o1, o2, o3]; okT = False
                        for Ts in itertools.product(*[TALLOW[name][j] for j in range(3)]):
                            S = np.zeros((4, 4))
                            for i in range(3):
                                for j in range(3):
                                    S[i, j] = (10 if i == j else -(ms[i][1] @ ms[j][1])) - ms[i][0] @ P @ ms[j][0]
                                S[i, 3] = S[3, i] = -4 * Ts[i] - (ms[i][1] @ r) - ms[i][0] @ P @ mf
                            S[3, 3] = 10 - mf @ P @ mf
                            ws = np.linalg.eigvalsh(S)
                            if ws[0] >= -TOL and int(np.sum(ws > TOL)) <= 15 - rk: okT = True; break
                        if not okT: continue
                        n += 1
                counts[name] = n
            verdict.append(counts)
        print('b=%d q=%d p1=%d p2=%d  kernel-dim %d  M-triples %d  shell-2 admissible rows per label: %s' % (b, q, p1, p2, len(ker), len(triples), verdict), flush=True)
main()
