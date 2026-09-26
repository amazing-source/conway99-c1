r"""X19l -- full pipeline on a fresh sample: locally admissible maximal-torsion (tau, sigma) -> block-level (P2) LP
-> cell-level LP (X19i) for block survivors -> Triangle Lemma for cell survivors.  Saves the final survivors."""
import sys, random, itertools, pickle, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'scripts')
import x19_block_lp_generic as X
import x19i_cells as XC
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible

def block_ok(tau, sigma):
    built, msg = X.build_lp(tau, sigma, True)
    A, b, nv, T = built
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, 1), method='highs', options=dict(time_limit=120))
    return res.status == 0

def cell_ok(tau, sigma):
    A, b, nv = XC.build(tau, sigma)
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, None), method='highs-ipm', options=dict(time_limit=250))
    return res.status == 0, res.status

if __name__ == '__main__':
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    done = nb = nc = 0; final = []
    t0 = time.time()
    while done < n:
        tau = {u: random_tau(u, rng) for u in LAB}
        sigma = {c: random_sigma(c, rng) for c in range(7)}
        if not all(admissible(build([frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2)
                                     for s in (0, 1) for t in (0, 1)], tau, sigma))
                   for tri in itertools.combinations(range(7), 3)):
            continue
        done += 1
        if not block_ok(tau, sigma):
            print(f'{done}: killed at block level', flush=True); continue
        nb += 1
        ok, st = cell_ok(tau, sigma)
        if not ok:
            print(f'{done}: block survivor, killed at cell level (status {st})', flush=True); continue
        nc += 1; final.append(dict(tau=tau, sigma=sigma))
        print(f'{done}: SURVIVES block and cell levels', flush=True)
    pickle.dump(final, open(f'data/x19l_final_s{seed}.pkl', 'wb'))
    print(f'TOTAL seed {seed}: {n} admissible; block survivors {nb}; cell survivors {nc}; {time.time()-t0:.0f}s', flush=True)
