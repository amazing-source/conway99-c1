# Independent confirmation on (v) survivors: kernel of M_U (integer, exact), and m12-option orthogonality.
import sys, numpy as np, sympy as sp
sys.argv = ['x', 'v', 'base_v_gen.bin', 'v_mshell_surv.txt']
exec(open('pipeline_gen.py').read().split("if __name__ == '__main__':")[0])
recs = [tuple(map(int, l.split()[:5])) for l in open('v_mshell_surv.txt')]
worst = []
for idx in [0, 100, 200, 287]:
    b, q, p1, p2, kind = recs[idx]
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed)
    MU = (12 * np.eye(15) + 4 * G - R @ R.T).astype(int)
    K = sp.Matrix(MU.tolist()).nullspace()
    Kint = [sp.Matrix([x * sp.ilcm(*[y.q for y in v]) for x in v]) for v in K]
    assert all((sp.Matrix(MU.tolist()) * v).is_zero_matrix for v in Kint)
    # numpy SVD kernel for comparison
    U_, s, Vt = np.linalg.svd(MU.astype(float)); nk = int(np.sum(s < 1e-9))
    dots = []
    for x, r in m_options(alpha, g, 0, 1):
        mi = (-4 * x - R @ r).astype(int)
        dots.append(max(abs(int(sum(int(mi[i]) * int(v[i]) for i in range(15)))) for v in Kint))
    print('survivor #%d b=%d: exact kernel dim %d (numpy %d); kernel vectors (integer):' % (idx, b, len(Kint), nk))
    for v in Kint: print('    ', list(v))
    print('   m12 options: %d, min over options of max |m.z| = %d  (0 would mean an admissible option)' % (len(dots), min(dots)))
