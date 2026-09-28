"""Is 'Identity H' (2 gamma = -2 beta + 20 + o - nu_z^2 - nu_z'^2) automatic for arbitrary star matchings?
Star 1: 12 points = 10 X-points with s = +-1 (5 each) and 2 zero points z, z'. mu, tau = arbitrary perfect matchings
(mu may meet tau). beta = sum_o s_o (s_tau(o) - s_mu(o)); gamma = sum_o s_o s_{tau(mu(o))}; o1 = #{o : exactly one of
tau(o), mu(o) in {z,z'}}; nu_z = -(s_tau(z) - s_mu(z)). Random test only (a check of a hand identity, not a search)."""
import random
def rand_pm(n, rng):
    p = list(range(n)); rng.shuffle(p); m = [0] * n
    for i in range(0, n, 2): m[p[i]], m[p[i + 1]] = p[i + 1], p[i]
    return m
rng = random.Random(7); bad = 0; tested = 0
s = [1] * 5 + [-1] * 5 + [0, 0]; Z = {10, 11}
for _ in range(200000):
    mu, tau = rand_pm(12, rng), rand_pm(12, rng)
    # alignment rule beta_o in {0,1,2} for every X-point (necessary in a witness); skip configurations violating it
    bo = [s[o] * (s[tau[o]] - s[mu[o]]) for o in range(10)]
    if min(bo) < 0: continue
    tested += 1
    beta = sum(bo); gamma = sum(s[o] * s[tau[mu[o]]] for o in range(10))
    o1 = sum(1 for o in range(10) if (tau[o] in Z) != (mu[o] in Z))
    nu = [-(s[tau[z]] - s[mu[z]]) for z in (10, 11)]
    if 2 * gamma != -2 * beta + 20 + o1 - nu[0] ** 2 - nu[1] ** 2: bad += 1
print('configurations with all beta_o >= 0:', tested, '| violating identity H:', bad)
