"""Independent check of structures' out_kstar_ladder.json (C1, 28/09): for every y-pair NOT killed by Sol (min 7|k|^2 >= 5),
min over nonzero kappa in K* of n = 7|kappa|^2, from the stored K Gram only (D = 49 GK^-1 integral, Fincke-Pohst z D z <= 7*9)."""
import sys, json, os, time
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
sys.path.insert(0, 'C:/home/researcher/Desktop/c1_recherche/code')
from rank17_ypairs import short_vectors_chunked
from envelope_trap import inverse_exact
DATA = 'C:/home/researcher/Desktop/c1_recherche/data/rank17'
L = json.load(open('C:/home/researcher/Desktop/conway99-rank17/out_kstar_ladder.json'))
theirs = {(r['V'], r['id']): r['min7'] for r in L}
tags = sorted({t for t, _ in theirs})
mine, bad, t0 = {}, [], time.time()
for tag in tags:
    K = json.load(open(os.path.join(DATA, 'K_%s.json' % tag)))
    for rec in K['K']:
        if (tag, rec['id']) not in theirs:
            continue
        G = [[int(x) for x in r] for r in rec['K_gram']]
        Gi = inverse_exact(G)
        assert all((x * 49).denominator == 1 for r in Gi for x in r)
        D = [[int(x * 49) for x in r] for r in Gi]
        X, nrm = short_vectors_chunked(D, 7 * 9)
        ns = sorted({int(v) // 7 for v in nrm.tolist() if v and v % 7 == 0})
        assert all(v % 7 == 0 for v in nrm.tolist())
        m = ns[0] if ns else None
        mine[(tag, rec['id'])] = m
        if m != theirs[(tag, rec['id'])]:
            bad.append((tag, rec['id'], m, theirs[(tag, rec['id'])]))
    print(tag, 'done', len(mine), '%.0fs' % (time.time() - t0), flush=True)
print('pairs', len(mine), 'of', len(theirs), '| min n distribution', dict(sorted(Counter(mine.values()).items(), key=str)))
print('disagreements', len(bad), bad[:10])
