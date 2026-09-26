"""Interlacing check: odd ball matrix (19x19, principal submatrix of S) must have spectrum in [-4, 3];
even ball (20x20 incl. x, principal submatrix of A_even in orthonormal orbit basis) spectrum in [-4,3] except top <= 14.
Over all tau classes x all eta: how many violate?"""
import numpy as np
exec(open('x36c_q7_qc_nullity.py', encoding='utf-8').read().split("t0 = time.time()")[0])
def balls(tau, eta):
    h = [pi[eta[w]] for w in X]; tm = [pi[tau[pi[w]]] for w in X]
    V = ['x', 'u', 'ub'] + [('X', w) for w in X] + [('U', w) for w in X] + [('B', w) for w in X]
    idx = {v: i for i, v in enumerate(V)}; n = len(V); A = np.zeros((n, n))
    def e(a, b): A[idx[a], idx[b]] = A[idx[b], idx[a]] = 1
    e('x', 'u'); e('x', 'ub'); e('u', 'ub')
    for w in X:
        e('x', ('X', w)); e('u', ('U', w)); e('ub', ('B', w))
        e(('X', w), ('X', pi[w])); e(('U', w), ('U', tau[w])); e(('B', w), ('B', tm[w]))
        e(('X', w), ('U', w)); e(('X', w), ('B', w)); e(('U', w), ('B', h[w]))
    th = {'x': 'x', 'u': 'ub', 'ub': 'u'}
    for w in X: th[('X', w)] = ('X', pi[w]); th[('U', w)] = ('B', pi[w]); th[('B', w)] = ('U', pi[w])
    reps = ['u'] + [('X', 2*d) for d in range(6)] + [('U', w) for w in X]
    So = np.array([[A[idx[a], idx[b]] - A[idx[a], idx[th[b]]] for b in reps] for a in reps])
    # even: orthonormal basis e_x, (e_v + e_sv)/sqrt2
    Se = np.zeros((20, 20)); er = ['x'] + reps
    for i, a in enumerate(er):
        for j, b in enumerate(er):
            if a == 'x' and b == 'x': Se[i, j] = 0
            elif a == 'x': Se[i, j] = (A[idx['x'], idx[b]] + A[idx['x'], idx[th[b]]]) / np.sqrt(2)
            elif b == 'x': Se[i, j] = (A[idx[a], idx['x']] + A[idx[th[a]], idx['x']]) / np.sqrt(2)
            else: Se[i, j] = A[idx[a], idx[b]] + A[idx[a], idx[th[b]]]
    return So, Se
viol_o = viol_e = tot = 0; worst_o = worst_e = -9
for tau in reps:
    for eta in ALL[::7]:
        So, Se = balls(tau, eta); tot += 1
        eo = np.linalg.eigvalsh(So); ee = np.linalg.eigvalsh(Se)
        mo = eo[-1]; me = ee[-2]
        worst_o = max(worst_o, mo); worst_e = max(worst_e, me)
        if mo > 3 + 1e-9 or eo[0] < -4 - 1e-9: viol_o += 1
        if me > 3 + 1e-9 or ee[0] < -4 - 1e-9: viol_e += 1
print('tested', tot, 'odd violations', viol_o, 'max odd eig %.4f' % worst_o, '| even violations', viol_e, 'max 2nd even eig %.4f' % worst_e)
