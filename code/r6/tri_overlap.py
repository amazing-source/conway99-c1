# Data check (exact, no solver): which open classes contain which short-triple types; overlaps.
import sys, json
from collections import Counter
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-rank17')
import kstar_scan as S
D = 'C:/home/researcher/Desktop/c1_recherche/data/rank17/'
open_ = set(json.load(open(D + 'open_after_sol.json')))
files = ['K_Z17', 'K_E8', 'K_D12p', 'K_E72p', 'K_D82p', 'K_A15p', 'K_A11E6p']
sets = {}; minn = {}; has6 = set(); has8 = set(); cnt = Counter()
for f in files:
    d = json.load(open(D + f + '.json', encoding='utf-8'))
    tag = f[2:]
    for rec in d['K']:
        key = '%s:%d' % (tag, rec['id'])
        if key not in open_: continue
        H = S.inv_times7(rec['K_gram'])
        sv = S.short_vectors(H, 8)
        ns = [a for a, x in sv]
        minn[key] = min(ns)
        if 6 in ns: has6.add(key)
        if 8 in ns: has8.add(key)
        ip = lambda x, y: sum(x[p] * H[p][q] * y[q] for p in range(15) for q in range(15))
        for i in range(len(sv)):
            for j in range(i + 1, len(sv)):
                (a, x), (b, y) = sv[i], sv[j]
                t = ip(x, y)
                for s in (1, -1):
                    c = a + b - 2 * s * t
                    if 5 <= c <= 8:
                        sets.setdefault(tuple(sorted((a, b, c))), set()).add(key)
allk = set(minn)
print('open', len(allk), ' with n=6:', len(has6), ' with n=8:', len(has8), ' with 6 or 8:', len(has6 | has8))
for k, v in sorted(sets.items()): print(k, len(v))
A = sets.get((6, 8, 8), set()); B = sets.get((6, 6, 8), set()); C = sets.get((5, 5, 6), set())
print('688&668', len(A & B), ' 688&556', len(A & C), ' 668&556', len(B & C), ' union', len(A | B | C))
print('556 only (not 688/668):', len(C - A - B), ' 668 not 688:', len(B - A))
print('min n distribution of 556 classes:', Counter(minn[k] for k in C))
print('min n distribution of the 359 classes with no triple:', Counter(minn[k] for k in allk - (A | B | C)))
print('no-triple classes with n=6:', len(has6 & (allk - (A|B|C))), ' with n=8 but no n=6:', len((has8 - has6) & (allk - (A|B|C))))
