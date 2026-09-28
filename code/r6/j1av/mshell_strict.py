# Strict M-shell test on the few support survivors (exact kernel orthogonality + budget), types v and iii.
# Facts (M_full = 12I - 4T - RR^T = 28 P_{-4} on all 42 labels, PSD of rank 15):
#   (K) z in ker(M_U)  =>  z in ker(M_full)  =>  m_Y . z = 0 EXACTLY for every non-support label Y   (checked in integers)
#   (B) sum over the 27 non-support labels of m_Y m_Y^T = 28 M_U - M_U^2 (tight frame), so any partial sum is <= it (PSD)
#   (S) Schur complement of the added labels PSD with rank <= 15 - rank(M_U)
# Usage: python mshell_strict.py TYPE base_file survivors_file
import sys, numpy as np, sympy as sp
TYPE, BASEF, SURVF = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = ['x', TYPE, BASEF, SURVF]
exec(open('pipeline_gen.py').read().split("if __name__ == '__main__':")[0])
TOL = 1e-6
def int_kernel(MU):
    Ms = sp.Matrix(MU.astype(int).tolist())
    basis = Ms.nullspace()
    out = []
    for v in basis:
        den = sp.ilcm(*[x.q for x in v]) if any(x.q != 1 for x in v) else 1
        out.append(np.array([int(x * den) for x in v], dtype=np.int64))
    return out
def run():
    recs = [tuple(map(int, l.split()[:5])) for l in open(SURVF)]
    from collections import Counter
    verdicts = Counter()
    for rec in recs:
        b, q, p1, p2, kind = rec
        alpha, g, ed = config(b, q, p1, p2)
        R, G = mats(alpha, g, ed)
        MU = 12 * np.eye(15) + 4 * G - R @ R.T
        ker = int_kernel(MU)
        w, V = np.linalg.eigh(MU); keep = w > 1e-7; rk = int(np.sum(keep))
        P = (V[:, keep] / w[keep]) @ V[:, keep].T
        BUD = 28 * MU - MU @ MU
        good = {}; reason = None
        for jk in [(0, 1), (0, 2), (1, 2)]:
            lst = []; nk = 0; nb_ = 0
            for x, r in m_options(alpha, g, *jk):
                mi = (-4 * x - R @ r).astype(np.int64)
                if any(int(mi @ z) != 0 for z in ker): nk += 1; continue          # (K) exact
                m = mi.astype(float)
                s2 = 10 - m @ P @ m
                if s2 < -TOL: continue
                if np.linalg.eigvalsh(BUD - np.outer(m, m))[0] < -TOL: nb_ += 1; continue   # (B) single label
                lst.append((m, r, s2))
            good[jk] = lst
            if not lst: reason = 'no option for m%d%d (kernel-orth killed %d, budget %d)' % (jk[0] + 1, jk[1] + 1, nk, nb_); break
        if reason is None:
            ntr = 0
            for o1 in good[(0, 1)]:
                for o2 in good[(0, 2)]:
                    g12 = -(o1[1] @ o2[1]) - o1[0] @ P @ o2[0]
                    if g12 * g12 > o1[2] * o2[2] + TOL: continue
                    for o3 in good[(1, 2)]:
                        g13 = -(o1[1] @ o3[1]) - o1[0] @ P @ o3[0]; g23 = -(o2[1] @ o3[1]) - o2[0] @ P @ o3[0]
                        ws = np.linalg.eigvalsh(np.array([[o1[2], g12, g13], [g12, o2[2], g23], [g13, g23, o3[2]]]))
                        if ws[0] < -TOL or int(np.sum(ws > TOL)) > 15 - rk: continue
                        Bp = BUD - np.outer(o1[0], o1[0]) - np.outer(o2[0], o2[0]) - np.outer(o3[0], o3[0])
                        if np.linalg.eigvalsh(Bp)[0] < -TOL: continue                 # (B) for the triple
                        ntr += 1
            reason = 'SURVIVES (%d triples)' % ntr if ntr else 'no consistent triple under (K)+(B)+(S)'
        verdicts[reason.split(' (')[0] if reason.startswith('no option') else reason] += 1
        print('b=%d q=%d p1=%d p2=%d rank=%d kernel-dim=%d : %s' % (b, q, p1, p2, rk, len(ker), reason), flush=True)
    print('SUMMARY', TYPE, dict(verdicts))
run()
