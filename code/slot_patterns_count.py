"""list twisting patterns with |N| = k (see slot_frontier.py) and the number of tau/rho configurations each"""
import sys, itertools
from math import prod
from slot_frontier_lib import graphs, patterns, n_configs
k = int(sys.argv[1])
tot = 0
for es in graphs(k):
    for T in patterns(es):
        n = n_configs(T)
        tot += 1
        print(sorted(es), {f'{l[0]}{"+-"[l[1]]}': ''.join(map(str, sorted(v))) for l, v in T.items()}, 'configs:', n, flush=True)
print('patterns:', tot)
