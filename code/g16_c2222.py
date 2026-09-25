"""notes/112: pattern (2,2,2,2) on the 4-cycle 0-1-2-3: both labels of each cycle class twist its two neighbours.
Lemma A (notes/112) forces every shadow map: rho_v swaps the two labels of each neighbouring class.  Test the 2^8
tau choices with the first-order slot calculus."""
from collections import Counter
from slot_calculus import Config, build, propagate, LAB, CL, mate
from slot_tests import base, matchings_no_mate
from slot_lp import lp_check
import itertools

CYC = [0, 1, 2, 3]
nb = {v: [CYC[(v - 1) % 4], CYC[(v + 1) % 4]] for v in CYC}
tw_labels = [(v, s) for v in CYC for s in (0, 1)]
choices = [list(matchings_no_mate([(c, s) for c in sorted(nb[l[0]]) for s in (0, 1)])) for l in tw_labels]
stats = Counter()
for ms in itertools.product(*choices):
    tau, rho = base()
    for l, m in zip(tw_labels, ms):
        for a, b in m:
            tau[l][a] = b; tau[l][b] = a
    for v in CYC:                       # rho_v swaps the two labels of each neighbouring class (Lemma A)
        for u in nb[v]:
            rho[v][(u, 0)] = (u, 1); rho[v][(u, 1)] = (u, 0)
    cfg = Config(tau, rho)
    st, _ = lp_check(cfg)
    stats[st] += 1
print(dict(stats))
