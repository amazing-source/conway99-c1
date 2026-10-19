import gzip, json, hashlib, sys
from pathlib import Path
from collections import Counter
S = Path(sys.argv[1])
shards = sorted((S / 'k2bcprod' / 'shards').glob('*.json.gz'))
covers = {int(p.name[5:8]): p for p in (S / 'pybd_k2bc_all').glob('core_*.json.gz')}
cov = {}
for ci, p in covers.items():
    raw = p.read_bytes(); d = json.loads(gzip.decompress(raw))
    cov[ci] = (hashlib.sha256(raw).hexdigest(), d)
print('covers', len(cov), 'symmetry strings', Counter(d['symmetry'] for _, d in cov.values()))
print('cover families', Counter(d.get('family') for _, d in cov.values()))
print('cover statuses', Counter(d.get('status') for _, d in cov.values()))
print('boundary byte lengths', Counter(len(bytes.fromhex(h)) for _, d in cov.values() for h in d['boundaries_hex']))
print('total boundaries', sum(d['boundary_count'] for _, d in cov.values()))
progs = Counter(); mods = Counter(); flags = Counter(); stat = Counter(); keys = Counter(); fam = Counter()
per_core = Counter(); bad = []
tot = Counter()
for p in shards:
    d = json.loads(gzip.decompress(p.read_bytes()))
    progs[d['program_sha256']] += 1
    mods[json.dumps(d['codex_modules_sha256'], sort_keys=True)] += 1
    flags[' '.join(d['flags'])[:0] + ' '.join(f for f in d['flags'] if not f.startswith('--out='))] += 1
    fam[d['summary']['family']] += 1
    ci = d['core_index']
    if d['source_sha256'] != cov[ci][0]:
        bad.append((p.name, 'source sha mismatch'))
    for rec in d['cases']:
        stat[rec['status']] += 1; per_core[ci] += 1
        for k, v in rec['counts'].items():
            keys[k] += 1
            if k != 'max_conflicts':
                tot[k] += v
print('programs', progs)
print('codex modules', mods)
print('flags', flags)
print('families', fam)
print('case statuses', stat)
print('count keys', keys)
print('totals', dict(tot))
print('bad', bad)
print('cases per core vs cover', all(per_core[ci] == cov[ci][1]['boundary_count'] for ci in cov), sorted(set(cov) - set(per_core)))
