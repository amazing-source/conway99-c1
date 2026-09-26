r"""X26 -- Fano-tight model: the explicit obstruction functional Psi_R of the per-block 'cellcross' system.

For a block R = {P,Q}, M = Phi(P,Q), C4 = the 4 classes off the line PQM, M_M = the 2 pairs of C4 whose third
point is M, s = +1 on one M_M pair and -1 on the other:
    Psi_R = sum_{c in C4} s(c) [9 e_{Mc} + e_{Pc} + e_{Qc}] + 4 (e_{c1c2} - e_{c3c4}).
Fact (checked exactly over all 8 landings of every pair): <c(z), Psi_R> = 0 whenever blk(z) avoids R and c_R(z) > 0.
Hence, in any srg(99,14,1,2), at a Fano-tight vertex, cellcross forces  I_R := <rhs_R, Psi_R> / 24 = 0  for all R.
This script evaluates I_R on Fano-tight configurations (the witness, or fresh ones: sigma from the KBLDP system,
tau flips by local search for local admissibility, as in X21), and checks the closed formula
    <rhs_R, Psi_R> = -6 sum_{y in R} eps(y) [ s(a_{z_P(y)}) eta_{z_P(y)} + s(a_{z_Q(y)}) eta_{z_Q(y)} ]
(z_P(y), z_Q(y): tau-partners of y in the blocks PM, QM; a_z: landing class of z via its P- (or Q-) label;
 eta_z = +1 if the landing via M is Phi(M, a_z), -1 if it is Phi(P, a_z)).
usage: python x26_fano_psi.py witness | python x26_fano_psi.py <seed> <n>"""
import sys, pickle, itertools, random, time
import numpy as np
sys.path.insert(0, 'scripts')
from x15_fano_tight import config_data, PHI, BLOCKS, PAIRS, blk, landing
from x25_fano_cellcross_blocks import counts, block_system, eps

def Psi(R):
    P, Q = sorted(R); M = PHI[(P, Q)]
    C4 = [c for c in range(7) if c not in (P, Q, M)]
    MM = [frozenset((c, d)) for c, d in itertools.combinations(C4, 2) if PHI[(c, d)] == M]
    s = {c: (1 if c in MM[0] else -1) for c in C4}
    psi = {Rp: 0 for Rp in BLOCKS}
    for c in C4:
        psi[frozenset((M, c))] += 9 * s[c]; psi[frozenset((P, c))] += s[c]; psi[frozenset((Q, c))] += s[c]
    for e in MM:
        psi[e] += 4 * s[next(iter(e))]
    return psi, s, M

def I_vector(tau, sigma):
    D = config_data(tau, sigma)
    assert D['ok'] and D['imbalance'] == 0 and D['lab_bad'] == 0 and D['neg'] == 0
    c = counts(D)
    sinv = {P: {w: v for v, w in sigma[P].items()} for P in range(7)}
    out = {}
    for R in BLOCKS:
        psi, s, M = Psi(R)
        free, sd, rhs = block_system(D, c, R)
        assert all(sum(c[z][Rp] * psi[Rp] for Rp in BLOCKS) == 0 for z in free)
        val = sum(rhs[Rp] * psi[Rp] for Rp in BLOCKS)
        # closed formula
        P, Q = sorted(R); tot = 0
        for y in PAIRS:
            if blk(y) != R: continue
            for u in y:                                  # u = the P- or Q-label of y; z = tau_u partner of y
                v = next(iter(y - {u}))
                z = frozenset({u, tau[u][v]})
                assert blk(z) == frozenset((u[0], M))
                e, f = sorted(z); Pz, Qz, a, b = landing(z, tau, sigma, sinv)
                a_u = a if e == u else b                     # landing via u's class
                a_M = b if e == u else a                     # landing via M
                eta = 1 if a_M == PHI[(M, a_u)] else -1
                assert eta == 1 or a_M == PHI[(u[0], a_u)]
                tot += eps(y) * s[a_u] * eta
        assert val == -6 * tot, (R, val, tot)
        assert val % 24 == 0
        out[''.join(map(str, sorted(R)))] = val // 24
    return out

if __name__ == '__main__':
    if sys.argv[1] == 'witness':
        W = pickle.load(open('data/x15_witness.pkl', 'rb'))
        I = I_vector(W['tau'], W['sigma'])
        print('witness I_R:', I, ' violated blocks:', sum(1 for v in I.values() if v))
        sys.exit()
    from scipy.optimize import milp, Bounds
    import x15n_ilp_p2 as N
    import x15g_ilp as G
    from x15h_test_solution import sigma_from
    from x21_fano_cells import admissible_tau
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed); nprng = np.random.default_rng(seed)
    C, nrows = N.build('KBLDP')
    for trial in range(n):
        t0 = time.time()
        res = milp(c=nprng.normal(size=N.NTOT), constraints=[C], integrality=np.ones(N.NTOT), bounds=Bounds(0, 1),
                   options=dict(time_limit=200, disp=False))
        if res.x is None:
            print(f'trial {trial}: no KBLDP solution', flush=True); continue
        sig = sigma_from(np.rint(res.x[:G.NV]))
        tau = admissible_tau(sig, rng)
        if tau is None:
            print(f'trial {trial}: no admissible tau', flush=True); continue
        I = I_vector(tau, sig)
        pickle.dump(dict(tau=tau, sigma=sig), open(f'data/x26_fano_s{seed}_{trial}.pkl', 'wb'))
        print(f'trial {trial}: violated blocks {sum(1 for v in I.values() if v)}/21  I = {I}  [{time.time()-t0:.0f}s]',
              flush=True)
