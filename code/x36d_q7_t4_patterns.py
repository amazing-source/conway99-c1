"""For local configurations (tau, eta) with t = dim ker Q = 4 (and t >= 3), record the digon pattern:
out = {d : tau(d+) = d-} (tau-digons, arcs c->d), inn = {d : eta(d+) = d-} (eta-digons, arcs d->c).
Global consistency at x: eta_c has a digon at d  <=>  tau_d has a digon at c  (h(c,d) = m(d,c))."""
import itertools
exec(open('x36c_q7_qc_nullity.py', encoding='utf-8').read().split("t0 = time.time()")[0])
from collections import Counter
pat = {1: Counter(), 2: Counter(), 3: Counter(), 4: Counter()}
for tau in reps:
    for eta in ALL:
        Q = [[(tau[w] == v) - (eta[w] == v) - 2*(pi[w] == v) - (w == v) for v in X] for w in X]
        t = 12 - rank_mod(Q)
        if t >= 1:
            out = frozenset(d for d in range(6) if tau[2*d] == 2*d+1)
            inn = frozenset(d for d in range(6) if eta[2*d] == 2*d+1)
            pat[t][(len(out), len(inn), len(out & inn))] += 1
for t in (1, 2, 3, 4):
    print('t =', t, ' (|out|, |in|, |double|) : count over tau-reps x eta ->', dict(sorted(pat[t].items())))
