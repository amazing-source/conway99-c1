r"""X19c -- survey: random locally admissible maximal-torsion local data (tau, sigma) at x, block-level system with
(P2); count certified-infeasible vs feasible; save the feasible ones (survivors) for analysis.
Optional: allow in-block sigma edges (sigma_c(v) = mate(v), the S-coincidences of L18)."""
import sys, random, itertools, pickle, time
sys.path.insert(0, 'scripts')
from x19b_certify import certify
from x14_triangle_supports import LAB, random_tau, build, admissible
mate = lambda l: (l[0], 1 - l[1])

def random_sigma_S(c, rng, allow_S):
    others = [l for l in LAB if l[0] != c]
    while True:
        perm = others[:]; rng.shuffle(perm)
        s = dict(zip(others, perm))
        if all(s[b] != b and (allow_S or s[b] != mate(b)) for b in others):
            return s

if __name__ == '__main__':
    seed, n, allow_S = int(sys.argv[1]), int(sys.argv[2]), bool(int(sys.argv[3]))
    rng = random.Random(seed)
    done = inf = feas = 0; surv = []
    t0 = time.time()
    while done < n:
        tau = {u: random_tau(u, rng) for u in LAB}
        sigma = {c: random_sigma_S(c, rng, allow_S) for c in range(7)}
        ok = all(admissible(build([frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2)
                                   for s in (0, 1) for t in (0, 1)], tau, sigma))
                 for tri in itertools.combinations(range(7), 3))
        if not ok:
            continue
        done += 1
        delta, val, den = certify(tau, sigma)
        if den:
            inf += 1
        else:
            feas += 1; surv.append(dict(tau=tau, sigma=sigma, delta=delta))
        print(f'{done}: {"INFEASIBLE (certified)" if den else "feasible"}  delta={delta:.3f}', flush=True)
    pickle.dump(surv, open(f'data/x19_survivors_s{seed}_S{int(allow_S)}.pkl', 'wb'))
    print(f'TOTAL seed {seed} allow_S {allow_S}: {inf} certified infeasible, {feas} feasible, of {n}; {time.time()-t0:.0f}s')
