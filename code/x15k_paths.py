"""X15k -- second-order block identities (P2):  for all blocks R, R' (R = R' allowed)
     sum_z cnt(z,R) cnt(z,R')  =  12 |R cap R'| + sum_{y in R, w in R', y != w} (2 - |y cap w|)  -  N(R,R')
(the 2-path count between blocks inside Delta_x, from (A_Delta^2)_{yw} = lambda/mu minus shared labels)."""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
from x15_fano_tight import *
from x15h_test_solution import sigma_from

def cnt_matrix(D):
    C = np.zeros((84, 21))
    for i, z in enumerate(PAIRS):
        for j, R in enumerate(BLOCKS):
            if R == blk(z):
                continue
            if R & blk(z):
                C[i, j] = sum(1 for w in D['spec'][z] if blk(w) == R)
            else:
                C[i, j] = D['gen'][z][R]
    return C

def p2_defect(D):
    C = cnt_matrix(D)
    LHS = C.T @ C
    RHS = np.zeros((21, 21))
    for a, R in enumerate(BLOCKS):
        for b, Rp in enumerate(BLOCKS):
            s = 12 * 4 if R == Rp else 0
            for y in PAIRS:
                if blk(y) != R:
                    continue
                for w in PAIRS:
                    if blk(w) != Rp or w == y:
                        continue
                    s += 2 - len(y & w)
            s -= D['N'][D['BI'][R], D['BI'][Rp]]
            RHS[a, b] = s
    return LHS - RHS

if __name__ == '__main__':
    x = np.load('data/x15g_KBL.npy')
    D = config_data(fano_tau(random.Random(1)), sigma_from(x))
    Df = p2_defect(D)
    print('KBL solution: P2 defect: max |.|', np.abs(Df).max(), ' number of nonzero entries', int((np.abs(Df) > 1e-9).sum()), 'of 441')
    print('diagonal defects', Df.diagonal().astype(int).tolist())
