r"""X26d -- put Psi-compatible flip assignments (X26c) of a Fano-tight sigma through the full cell-level LP (X19i).
usage: python x26d_cells_on_psi_flips.py <config.pkl> <k1,k2,...>"""
import sys, pickle
sys.path.insert(0, 'scripts')
from x21_fano_cells import tau_from
import x19i_cells as XC
if __name__ == '__main__':
    W = pickle.load(open(sys.argv[1], 'rb'))
    F = pickle.load(open(sys.argv[1].replace('.pkl', '_psi_flips.pkl'), 'rb'))
    for k in map(int, sys.argv[2].split(',')):
        tau = tau_from(F[k])
        print(f'assignment {k}: cell level -> {XC.solve(tau, W["sigma"])}', flush=True)
        pickle.dump(dict(tau=tau, sigma=W['sigma']), open(sys.argv[1].replace('.pkl', f'_psiflip{k}.pkl'), 'wb'))
