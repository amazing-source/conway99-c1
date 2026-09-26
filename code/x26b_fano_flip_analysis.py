r"""X26b -- Fano-tight, Psi obstruction, flip analysis.  tot_R = sum_{X in R} sum_s x_{X_s} D^R_X(s), with
x_{X_s} = (-1)^{s + f(X_s, L)} (f = flip bit of tau_{X_s} on the line L of R) and
D^R_X(s) = theta_R(X_s Z_0) - theta_R(X_s Z_1)  (Z = third point of L; the pairs X_s Z_u are the tau-partners).
The D's depend on sigma only.  Per Fano line L: 6 signs x, 3 conditions tot_R = 0 (R = the 3 blocks of L).
Prints, for a given sigma, which lines admit a sign solution (brute force 2^6), and the flip-independent parity test."""
import sys, pickle, itertools
sys.path.insert(0, 'scripts')
from x15_fano_tight import PHI, PAIRS, blk, landing, FANO
from x26_fano_psi import Psi

def theta(R, z, X, tau, sigma, sinv):
    """theta_R(z) for z in block {X, Z} (X in R, Z third point): s_R(landing via X) * eta."""
    psi, s, M = Psi(R)                       # M = third point of R's line
    e, f = sorted(z); Pz, Qz, a, b = landing(z, tau, sigma, sinv)
    a_X = a if e[0] == X else b
    a_Z = b if e[0] == X else a
    eta = 1 if a_Z == PHI[(M, a_X)] else -1
    assert eta == 1 or a_Z == PHI[(X, a_X)]
    return s[a_X] * eta

def D_values(tau, sigma):
    sinv = {P: {w: v for v, w in sigma[P].items()} for P in range(7)}
    out = {}
    for L in FANO:
        for X, Y in itertools.permutations(L, 2):
            R = frozenset((X, Y)); Z = PHI[(X, Y)]
            for s_ in (0, 1):
                d = theta(R, frozenset({(X, s_), (Z, 0)}), X, tau, sigma, sinv) - \
                    theta(R, frozenset({(X, s_), (Z, 1)}), X, tau, sigma, sinv)
                out[(R, X, s_)] = d
    return out

def line_solvable(L, D):
    P, Q, M = L
    blocks = [frozenset((P, Q)), frozenset((P, M)), frozenset((Q, M))]
    labs = [(c, s) for c in L for s in (0, 1)]
    sols = []
    for signs in itertools.product((1, -1), repeat=6):
        x = dict(zip(labs, signs))
        if all(sum(x[(X, s)] * D[(R, X, s)] for X in R for s in (0, 1)) == 0 for R in blocks):
            sols.append(x)
    par = {''.join(map(str, sorted(R))): sum(1 for X in R for s in (0, 1) if D[(R, X, s)] != 0) % 2 for R in blocks}
    return len(sols), par

if __name__ == '__main__':
    f = sys.argv[1] if len(sys.argv) > 1 else 'data/x15_witness.pkl'
    W = pickle.load(open(f, 'rb'))
    D = D_values(W['tau'], W['sigma'])
    # actual flips of the given tau: x_{X_s} = (-1)^{s + f}; recover from tau: tau_{X_s}(Z_0) = Y_t  ->  check tot_R
    for L in FANO:
        n, par = line_solvable(L, D)
        print('line', L, ': sign solutions', n, '/ 64;  parity of #nonzero D per block', par)
