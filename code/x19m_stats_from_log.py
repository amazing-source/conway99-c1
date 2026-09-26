r"""X19m -- statistics of final survivors vs cell-killed vs block-killed configurations (seed 21, outcomes from
logs/x19l_s21.log, configurations regenerated in the same order).  Statistics:
tau cycle types over the 14 labels; max / mean triangle-family edge count e_t; special-special coincidences inside
blocks (SS, sum over blocks); number of sigma 'landings' falling on a Fano-like pattern is not assumed."""
import sys, random, itertools, re
from collections import Counter
import numpy as np
sys.path.insert(0, 'scripts')
import x19_block_lp_generic as X
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible

def tau_type(u, t):
    adj = Counter()
    for v, w in t.items():
        if v < w:
            adj[frozenset((v[0], w[0]))] += 1
    classes = [c for c in range(7) if c != u[0]]
    seen = set(); lens = []
    for c in classes:
        if c in seen: continue
        comp = {c}; st = [c]
        while st:
            a = st.pop()
            for e in adj:
                if a in e:
                    b = next(iter(e - {a})) if len(e) == 2 else a
                    if b not in comp:
                        comp.add(b); st.append(b)
        seen |= comp; lens.append(len(comp))
    return ''.join(map(str, sorted(lens)))

def stats(tau, sigma):
    tt = Counter(tau_type(u, tau[u]) for u in LAB)
    es = []
    for tri in itertools.combinations(range(7), 3):
        pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
        es.append(int(build(pairs, tau, sigma)[15:, 15:].sum() // 2))
    sinv = {c: {w: v for v, w in sigma[c].items()} for c in range(7)}
    spec = {z: X.specials(z, tau, sigma, sinv) for z in X.PAIRS}
    ss = sum(1 for R in X.BLOCKS for a, b in itertools.combinations([y for y in X.PAIRS if X.blk(y) == R], 2)
             for z in X.PAIRS if a in spec[z] and b in spec[z])
    return tt, max(es), float(np.mean(es)), float(np.var(es)), ss

outcome = {}
for line in open('logs/x19l_s21.log'):
    m = re.match(r'(\d+): (.*)', line)
    if m:
        k = int(m.group(1)); s = m.group(2)
        outcome[k] = 'final' if 'SURVIVES' in s else 'cell' if 'cell level' in s else 'block'
rng = random.Random(21); done = 0; rows = {'final': [], 'cell': [], 'block': []}
while done < 20:
    tau = {u: random_tau(u, rng) for u in LAB}
    sigma = {c: random_sigma(c, rng) for c in range(7)}
    if not all(admissible(build([frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2)
                                 for s in (0, 1) for t in (0, 1)], tau, sigma)) for tri in itertools.combinations(range(7), 3)):
        continue
    done += 1
    rows[outcome[done]].append(stats(tau, sigma))
for k, rs in rows.items():
    if not rs: continue
    tt = Counter()
    for r in rs: tt.update(r[0])
    n = len(rs)
    print(f'{k:6s} n={n}: tau types/config {dict((a, round(b/n,1)) for a, b in sorted(tt.items()))}; '
          f'max e {np.mean([r[1] for r in rs]):.1f}; mean e {np.mean([r[2] for r in rs]):.2f}; var e {np.mean([r[3] for r in rs]):.2f}; SS {np.mean([r[4] for r in rs]):.1f}')
