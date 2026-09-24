"""Probe: take a random transition system tau at x (every label a random perfect matching of the other 12 labels,
no labelled 3-cycles), build the exact rooted model (rooted_model.build) and run a full CaDiCaL solve.
SAT would produce an srg(99,14,1,2); UNSAT says this tau is impossible. Also reports W-pattern statistics.
Usage: python random_tau_probe.py seed
"""
import sys, random, time, json
import tau_filter as tf, rooted_model as rm
from pysat.solvers import Cadical153
seed = int(sys.argv[1])
rng = random.Random(seed)
tau = tf.gen_random(rng)
twisting = sum(1 for a in rm.LABELS if any(tau[a][b] != rm.mate(b) for b in tau[a]))
t0 = time.time()
cnf, pool, D, grids, bad = rm.build(tau)
print(f'seed {seed}: twisting labels {twisting}/14, grids {len(grids)}, build {time.time()-t0:.0f}s', flush=True)
S = Cadical153(bootstrap_with=cnf.clauses)
t1 = time.time()
ok = S.solve()
print('result:', 'SAT !!!' if ok else 'UNSAT', f'({time.time()-t1:.0f}s)', flush=True)
if ok:
    m = set(l for l in S.get_model() if l > 0)
    json.dump({'tau': {str(a): {str(b): str(c) for b, c in tau[a].items()} for a in tau},
               'edges': [list(map(list, k)) for k, v in D.items() if v in m]}, open(f'../data/SAT_candidate_{seed}.json', 'w'))
