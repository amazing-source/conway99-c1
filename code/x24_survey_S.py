r"""X24 -- the S-coincidence stratum, never sampled so far: local data at x WITH m in-block sigma edges
{P_s Q_t} ~ {P_(1-s) Q_(1-t)} (sigma_P(v) = mate(v), which forces the partner coincidence sigma_Q(u) = mate(u) on the same
edge).  Max twist on tau as always.  Pipeline: locally admissible (35 triangle supports) -> block level (P2 with
e(R) > 0) -> cell level (X19i).  Short tests only (<= 250 s per LP).
usage: python x24_survey_S.py <seed> <n_admissible> <m>"""
import sys, random, itertools, pickle, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'scripts')
import x19_block_lp_generic as X
import x19i_cells as XC
from x14_triangle_supports import LAB, random_tau, build, admissible
mate = lambda l: (l[0], 1 - l[1])

# an in-block sigma edge is BOTH sigma-specials of its two ends: keep each special neighbour once
_specials = X.specials
def _specials_dedup(y, tau, sigma, sinv):
    out = []
    for w in _specials(y, tau, sigma, sinv):
        if w not in out:
            out.append(w)
    return out
X.specials = _specials_dedup

def sigma_with_S(rng, m):
    """m in-block sigma edges in distinct blocks, then random completion without further coincidences."""
    blocks = list(itertools.combinations(range(7), 2))
    while True:
        fixed = {c: {} for c in range(7)}          # fixed[c][v] = sigma_c(v)   (from c_0-side label v to c_1-side)
        ok = True
        for (P, Q) in rng.sample(blocks, m):
            s, t = rng.randint(0, 1), rng.randint(0, 1)
            # edge {P_s, Q_t} ~ {P_(1-s), Q_(1-t)}
            for (C, a, D, b) in ((P, s, Q, t), (Q, t, P, s)):
                # seen from class C: pairs {C_a, D_b} and {C_(1-a), D_(1-b)}
                v, w = ((D, b), (D, 1 - b)) if a == 0 else ((D, 1 - b), (D, b))
                if v in fixed[C] or w in fixed[C].values():
                    ok = False
                fixed[C][v] = w
        if not ok:
            continue
        sig = {}
        for c in range(7):
            others = [l for l in LAB if l[0] != c]
            dom = [v for v in others if v not in fixed[c]]
            cod = [w for w in others if w not in fixed[c].values()]
            for _ in range(2000):
                rng.shuffle(cod)
                if all(w not in (v, mate(v)) for v, w in zip(dom, cod)):
                    sig[c] = dict(fixed[c]); sig[c].update(zip(dom, cod)); break
            else:
                ok = False; break
        if ok:
            return sig

def s_count(sigma):
    return sum(1 for c in range(7) for v, w in sigma[c].items() if w == mate(v))

def block_ok(tau, sigma):
    A, b, nv, T = X.build_lp(tau, sigma, True)[0]
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, 1), method='highs', options=dict(time_limit=120))
    return res.status

def cell_ok(tau, sigma):
    out = XC.build(tau, sigma)
    if out is None:
        return 'no types'
    A, b, nv = out
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, None), method='highs-ipm', options=dict(time_limit=290))
    return res.status

if __name__ == '__main__':
    seed, n, m = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    done = tried = 0; surv = []; undet = []
    t0 = time.time()
    while done < n:
        tau = {u: random_tau(u, rng) for u in LAB}
        sigma = sigma_with_S(rng, m)
        tried += 1
        if not all(admissible(build([frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2)
                                     for s in (0, 1) for t in (0, 1)], tau, sigma))
                   for tri in itertools.combinations(range(7), 3)):
            continue
        done += 1
        sc = s_count(sigma)
        bs = block_ok(tau, sigma)
        if bs != 0:
            print(f'{done} (S-count {sc}, tried {tried}): killed at block level (status {bs})', flush=True); continue
        cs = cell_ok(tau, sigma)
        if cs == 2:
            print(f'{done} (S-count {sc}): block survivor, killed at cell level (status 2)', flush=True); continue
        if cs != 0:
            undet.append(dict(tau=tau, sigma=sigma))
            pickle.dump(undet, open(f'data/x24_undet_s{seed}_m{m}.pkl', 'wb'))
            print(f'{done} (S-count {sc}): block survivor, cell level UNDETERMINED (status {cs}, time limit)', flush=True)
            continue
        surv.append(dict(tau=tau, sigma=sigma))
        print(f'{done} (S-count {sc}): SURVIVES block and cell levels', flush=True)
        pickle.dump(surv, open(f'data/x24_surv_s{seed}_m{m}.pkl', 'wb'))
    print(f'TOTAL seed {seed} m {m}: {n} admissible of {tried} tried; cell survivors {len(surv)}; {time.time()-t0:.0f}s',
          flush=True)
