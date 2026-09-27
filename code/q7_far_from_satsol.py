"""Run the q:7 far test on a complete local solution produced by structures' sat_local.py (file cfg_satsol.json:
{'cfg': {'mu': [...], 'tau': [...]}, 'Phi': {str([a, a']): [b, d]}}).  C1, 27/09.
Steps: Z = 3I + X^T P^- X (mod 7) at the block; t_c, det Q_c; g- = 20 is forced if det is a square (K anisotropic, r = I),
otherwise g- in {18, 20} (18: T_FF = Z; 20: K hyperbolic, r = diag(1, -1)).  K search (q7_far_test.far_K_search: entries in
{0, +-1}, zero diagonal, total row counts, X K = 0, K^T K = 0, rank 2), then on every complete K the per-block counts F1:
for every far f and block z != c, #{far g through z : T_fg != 0} + #{labels of s_f in z} = base_z - 2 [z in supp D(f)],
base = 2 (z in supp f) or 4, with D(f) a far orbit at T = 0 (or, for a cancelling shadow {l}, the block of l).
Usage: python q7_far_from_satsol.py path/to/cfg_satsol.json"""
import sys, json, itertools
import numpy as np
from q7_far_test import analyze, far_K_search, legendre, P7


def load(path):
    d = json.load(open(path))
    mu = {i: int(v) for i, v in enumerate(d['cfg']['mu'])}
    tau = {i: int(v) for i, v in enumerate(d['cfg']['tau'])}
    Phi = {frozenset(json.loads(k)): tuple(v) for k, v in d['Phi'].items()}
    assert len(Phi) == 60
    return mu, tau, Phi


def per_block_ok(T, D, S):
    """T: 30 x 30 lifted far block; D: build() data (far reps); S: 12 x 30 shadows."""
    far = D['far']
    n = len(far)
    supp = [set(a // 2 for a in far[f][0]) for f in range(n)]
    for f in range(n):
        s = S[:, f]
        canc = None
        # a cancelling shadow has a label l with Phi(z) and Phi(sigma z) both containing l: then s_f(l) = 0 there;
        # detect via support size 2 (the construction keeps s = 1_Phi(z) - 1_Phi(sigma z))
        cnt = {}
        for z in range(6):
            nz_far = sum(1 for g in range(n) if g != f and z in supp[g] and T[f, g] != 0)
            lab = sum(1 for l in (2 * z, 2 * z + 1) if s[l] != 0)
            cnt[z] = nz_far + lab
        base = {z: (2 if z in supp[f] else 4) for z in range(6)}
        deficit = {z: base[z] - cnt[z] for z in range(6)}
        if any(v not in (0, 2) for v in deficit.values()):
            return False, (f, 'deficit values', deficit)
        dz = {z for z, v in deficit.items() if v == 2}
        if int((s != 0).sum()) == 2:                    # cancelling shadow: D(f) in star(c), one block of deficit
            if len(dz) != 1:
                return False, (f, 'cancelling shadow but deficit blocks', dz)
        else:
            if len(dz) != 2:
                return False, (f, 'deficit blocks', dz)
            cands = [g for g in range(n) if g != f and supp[g] == dz and T[f, g] == 0]
            if not cands:
                return False, (f, 'no far orbit at T = 0 on the deficit pair', dz)
    return True, None


def main(path):
    mu, tau, Phi = load(path)
    out, D = analyze(mu, tau, Phi)
    print({k: v for k, v in out.items() if k not in ('rigid',)}, 'rigid orbits:', out.get('rigid'))
    if not out.get('balanced'):
        print('X not in im P: unbalanced torsion (t > 0), use the regime analysis'); return
    if out['t'] != 0:
        print('t_c > 0: this driver handles t_c = 0 only'); return
    dsq = out['leg'] == 1
    runs = [(20, dsq)] if dsq else [(18, False), (20, False)]
    for g, sq in runs:
        if g == 18:
            st, info = far_K_search(D['Z'], D['X'], D['S'], det_square=False, g=18)
            print('g- = 18 (T_FF = Z):', st)
            continue
        st, info = far_K_search(D['Z'], D['X'], D['S'], det_square=sq)
        sols = info.pop('solutions', [])
        print('g- = 20, K %s:' % ('anisotropic' if sq else 'hyperbolic'), st, {k: v for k, v in info.items() if k != 'r'})
        good = 0
        for K in sols:
            R = (K @ info['r'] @ K.T) % P7
            T = (D['Z'] + R) % P7
            T = np.where(T == 6, -1, T)
            ok, why = per_block_ok(T, D, D['S'])
            good += ok
        if sols:
            print('   per-block counts F1: %d of %d K-solutions survive' % (good, len(sols)))


if __name__ == '__main__':
    main(sys.argv[1])
