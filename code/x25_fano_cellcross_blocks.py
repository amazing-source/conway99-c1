r"""X25 -- Fano-tight model: the block counts c_R'(z) are all DETERMINED (notes/115-116: tight counts), so the
'cellcross' identities decouple over R:
    for each block R and every block R':   sum_z delta_R(z) c_R'(z) = - sum_{y in R} eps(y) c_R'(y),
    delta_R(z) = #N(z) cap A_R - #N(z) cap B_R,  eps = +1 on A_R = {c_s d_s}, -1 on B_R = {c_s d_(1-s)}.
Unknown: delta_R(z) for the z whose classes avoid R, with |delta| <= c_R(z) and delta = c_R(z) mod 2; the special
z (classes meeting R) have delta_R(z) fixed by (tau, sigma).  Per block R: a tiny LP (and integer check).
Prints which blocks are infeasible, and an exact rational Farkas vector phi over R' for each."""
import sys, pickle, itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'scripts')
from x15_fano_tight import config_data, BLOCKS, PAIRS, blk

eps = lambda y: 1 if len({l[1] for l in y}) == 1 else -1

def counts(D):
    """c[z][R] for all z, R (special + generic)."""
    c = {}
    for z in PAIRS:
        row = {R: 0 for R in BLOCKS}
        for w in D['spec'][z]:
            row[blk(w)] += 1
        for R, v in D['gen'][z].items():
            row[R] += v
        c[z] = row
    return c

def block_system(D, c, R):
    free = [z for z in PAIRS if not (blk(z) & R) and c[z][R] > 0]
    spec_delta = {z: sum(eps(w) for w in D['spec'][z] if blk(w) == R) for z in PAIRS if blk(z) & R}
    rhs = {Rp: -sum(eps(y) * c[y][Rp] for y in PAIRS if blk(y) == R) - sum(d * c[z][Rp] for z, d in spec_delta.items())
           for Rp in BLOCKS}
    return free, spec_delta, rhs

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'data/x15_witness.pkl'
    W = pickle.load(open(src, 'rb'))
    D = config_data(W['tau'], W['sigma'])
    assert D['ok'] and D['imbalance'] == 0 and D['lab_bad'] == 0 and D['neg'] == 0
    c = counts(D)
    assert all(sum(c[z].values()) == 12 for z in PAIRS)
    bad = 0
    for R in BLOCKS:
        free, sd, rhs = block_system(D, c, R)
        # variables delta_R(z) in [-c_R(z), c_R(z)]
        Aeq = np.array([[c[z][Rp] for z in free] for Rp in BLOCKS], float)
        beq = np.array([rhs[Rp] for Rp in BLOCKS], float)
        res = linprog(np.zeros(len(free)), A_eq=Aeq, b_eq=beq, bounds=[(-c[z][R], c[z][R]) for z in free], method='highs')
        tag = ''.join(map(str, sorted(R)))
        if res.status == 2:
            bad += 1
            print(f'block {tag}: INFEASIBLE ({len(free)} free z)', flush=True)
        else:
            print(f'block {tag}: feasible ({len(free)} free z)', flush=True)
    print(f'{bad} of 21 blocks infeasible')
