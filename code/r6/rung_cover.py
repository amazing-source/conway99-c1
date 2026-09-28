# Data check (exact, no solver): rung coverage of the 754 open classes, and what the classes outside R8 contain.
import sys, json
from collections import Counter
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-rank17')
import kstar_scan as S
D = 'C:/home/researcher/Desktop/c1_recherche/data/rank17/'
open_ = set(json.load(open(D + 'open_after_sol.json')))
files = ['K_Z17', 'K_E8', 'K_D12p', 'K_E72p', 'K_D82p', 'K_A15p', 'K_A11E6p']
has = {n: set() for n in (5, 6, 7, 8)}; tri = {}; nvec = {}
for f in files:
    d = json.load(open(D + f + '.json', encoding='utf-8'))
    tag = f[2:]
    for rec in d['K']:
        key = '%s:%d' % (tag, rec['id'])
        if key not in open_: continue
        H = S.inv_times7(rec['K_gram'])
        sv = S.short_vectors(H, 8)
        nvec[key] = Counter(a for a, x in sv)
        for a, x in sv: has[a].add(key)
        ip = lambda x, y: sum(x[p] * H[p][q] * y[q] for p in range(15) for q in range(15))
        for i in range(len(sv)):
            for j in range(i + 1, len(sv)):
                (a, x), (b, y) = sv[i], sv[j]
                t = ip(x, y)
                for s in (1, -1):
                    c = a + b - 2 * s * t
                    if 5 <= c <= 8:
                        tri.setdefault(key, set()).add(tuple(sorted((a, b, c))))
allk = set(nvec)
import itertools
for r in (1, 2):
    for comb in itertools.combinations((5, 6, 7, 8), r):
        cov = set().union(*[has[n] for n in comb])
        print('rungs', comb, 'cover', len(cov), 'missing', len(allk - cov))
rest = allk - has[8]
print('classes outside R8:', len(rest))
print('  their short-vector content (n5,n6,n7 counts):', Counter(tuple(sorted(nvec[k].items())) for k in rest).most_common(12))
print('  with a triple:', sum(1 for k in rest if k in tri), Counter(t for k in rest for t in tri.get(k, ())))
print('  with n=5:', len(rest & has[5]), ' with n=7:', len(rest & has[7]))
