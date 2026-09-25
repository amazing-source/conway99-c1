"""notes/109: what the slot propagation fixes in the L14 configuration |C| = 2
(a0 = (0,0) and b0 = (1,0) twist classes {2,3}; nothing else twists)."""
import itertools
from collections import Counter
from slot_calculus import build, propagate, PAIRS, VERT, cls
from slot_tests import configs

twist = {(0, 0): {2, 3}, (1, 0): {2, 3}}
for k, cfg in enumerate(configs(twist)):
    var, lo, hi, eqs, inc = build(cfg)
    ok, lo2, hi2, log = propagate(lo, hi, eqs)
    fixed1 = Counter(); free = Counter(); fixed0 = Counter()
    for (y, R), j in var.items():
        P = cls(y)
        key = (tuple(sorted(P)), tuple(sorted(R)))
        if lo2[j] == hi2[j] == 1: fixed1[key] += 1
        elif lo2[j] == hi2[j] == 0: fixed0[key] += 1
        else: free[key] += 1
    perfect = [k for k in fixed1 if fixed1[k] == 4 and fixed1.get((k[1], k[0]), 0) == 4]
    print(f'config {k}: incomplete {sorted(tuple(sorted(P)) for P in inc)}')
    print(f'  Kneser pairs with a forced perfect matching: {len(perfect)//2} of 105')
    print(f'  variables fixed to 1: {sum(fixed1.values())}, fixed to 0: {sum(fixed0.values())}, free: {sum(free.values())}')
    fp = sorted(set(k for k in free))
    print('  pairs with free variables:', [k for k in fp][:30])
    if k == 0:
        break
