"""Propagation filter on transition systems at a root x of srg(99,14,1,2).
For a given tau (14 perfect matchings), build the exact rooted model (rooted_model.build) and classify:
  'UP'      : refuted by unit propagation alone (level 0)
  'UNSAT'   : refuted within the conflict budget
  'UNKNOWN' : survives the budget
Generators:
  random     : independent uniform random perfect matchings tau_a (rejecting 3-cycles in the trail system)
  kmate R    : start from mate, then re-randomise R labels' matchings
Usage: python tau_filter.py random N [budget]   |   python tau_filter.py kmate R N [budget]
"""
import sys, random, time, json
from pysat.solvers import Cadical153, Glucose4
import rooted_model as rm

LABELS = rm.LABELS
mate = rm.mate


def random_matching(rng, a):
    others = [b for b in LABELS if b[0] != a[0]]
    rng.shuffle(others)
    m = {}
    for i in range(0, len(others), 2):
        m[others[i]], m[others[i + 1]] = others[i + 1], others[i]
    return m


def has_3cycle(tau):
    for a in LABELS:
        for b, c in tau[a].items():
            # trail b -a- c ; 3-cycle iff tau[c][a] == b
            if tau[c][a] == b:
                return True
    return False


def gen_random(rng):
    while True:
        tau = {a: random_matching(rng, a) for a in LABELS}
        if not has_3cycle(tau):
            return tau


def gen_kmate(rng, R):
    while True:
        tau = {a: {b: mate(b) for b in LABELS if b[0] != a[0]} for a in LABELS}
        for a in rng.sample(LABELS, R):
            tau[a] = random_matching(rng, a)
        if not has_3cycle(tau):
            return tau


def classify(tau, budget):
    cnf, pool, D, grids, bad = rm.build(tau)
    if bad:
        return 'FIXED', len(grids)
    S = Glucose4(bootstrap_with=cnf.clauses)
    ok, _ = S.propagate()
    if not ok:
        return 'UP', len(grids)
    S.conf_budget(budget)
    r = S.solve_limited()
    return {False: 'UNSAT', True: 'SAT!!', None: 'UNKNOWN'}[r], len(grids)


def main():
    mode = sys.argv[1]
    rng = random.Random(int(time.time()))
    if mode == 'random':
        N = int(sys.argv[2]); budget = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
        gen = lambda: gen_random(rng)
    else:
        R, N = int(sys.argv[2]), int(sys.argv[3]); budget = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
        gen = lambda: gen_kmate(rng, R)
    stats = {}
    for k in range(N):
        tau = gen()
        t0 = time.time()
        res, g = classify(tau, budget)
        stats[res] = stats.get(res, 0) + 1
        print(f'#{k}: grids={g} -> {res} ({time.time()-t0:.1f}s)', flush=True)
        if res in ('UNKNOWN', 'SAT!!'):
            json.dump({str(a): {str(b): str(c) for b, c in m.items()} for a, m in tau.items()},
                      open(f'../data/tau_survivor_{mode}_{int(time.time())}_{k}.json', 'w'))
    print('summary:', stats)


if __name__ == '__main__':
    main()
