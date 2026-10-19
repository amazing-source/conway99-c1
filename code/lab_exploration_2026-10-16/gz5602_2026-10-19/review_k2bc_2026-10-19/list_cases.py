import gzip, json, sys
from pathlib import Path
S = Path(__file__).resolve().parent.parent / 'k2bcprod' / 'shards'
zero = []; allc = []
for p in sorted(S.glob('*.json.gz')):
    d = json.loads(gzip.decompress(p.read_bytes()))
    for rec in d['cases']:
        c = rec['counts']
        allc.append((d['core_index'], rec['boundary_index'], c.get('valid_partial', 0), c.get('EXCLUDED_SYMMETRIC_ATTACHMENT', 0), c.get('sat_calls', 0)))
        if 'valid_partial' not in c:
            zero.append((d['core_index'], rec['boundary_index']))
json.dump({'zero': zero, 'all': allc}, open('cases.json', 'w'))
print('zero-leaf', len(zero), 'by core', {ci: sum(1 for c, _ in zero if c == ci) for ci in sorted(set(c for c, _ in zero))})
bad = [a for a in allc if a[2] and a[3] * 4 != a[2] * 3]
print('cases where skipped != 3/4 of leaves', len(bad), bad[:5])
print('max leaves', max(a[2] for a in allc), 'mean', sum(a[2] for a in allc) / len(allc))
