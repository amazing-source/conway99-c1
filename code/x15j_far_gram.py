"""X15j -- far-block Gram matrices of the hidden projector, block-constant f on the far set of L_c:
   U = 7 Gram(Pi_{-4} 1_R) = 12I + N^T Y N - N_F     (must be PSD, rank <= 8)
   T = 7 Gram(Pi_3 1_R)    = N_F + 16I - N^T (Y+7P) N  (must be PSD, rank <= 18)
   U + T = 7 Gram(Pi_ker 1_R) = 28 I - 7 N^T P N."""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
from x15_fano_tight import *
from x15h_test_solution import sigma_from
from x15f_farblock import ball, profile

def ball_ops(AG):
    nN = len(AG); part = nN // 3
    I = np.eye(nN); J = np.ones((nN, nN))
    BJ = np.kron(np.eye(3), np.ones((part, part)))
    MMt = 12 * I + 2 * J - AG - AG @ AG - BJ
    P = np.linalg.pinv(MMt)
    Y = P @ (J / 3 - AG - I - 3 * I)
    return P, Y

def far_grams(D, cc):
    N, AG = ball(D, cc)
    P, Y = ball_ops(AG)
    far = [R for R in BLOCKS if cc not in R]
    Nh = np.array([profile(D, N, R) for R in far]).T
    NF = np.array([[D['N'][D['BI'][R], D['BI'][Rp]] for Rp in far] for R in far], float)
    U = 12 * np.eye(15) + Nh.T @ Y @ Nh - NF
    T = NF + 16 * np.eye(15) - Nh.T @ (Y + 7 * P) @ Nh
    return far, U, T

if __name__ == '__main__':
    x = np.load('data/x15g_KBL.npy')
    D = config_data(fano_tau(random.Random(1)), sigma_from(x))
    for cc in range(7):
        far, U, T = far_grams(D, cc)
        eu = np.linalg.eigvalsh(U); et = np.linalg.eigvalsh(T)
        print(f'class {cc}: U eig min {eu.min():+.4f}, rank {np.sum(eu > 1e-7)} | T eig min {et.min():+.4f}, rank {np.sum(np.abs(et) > 1e-7)}'
              f' | diag U {np.round(np.diag(U), 3).tolist()}')
        print('      diag T', np.round(np.diag(T), 3).tolist())
