import sys, time, json, gzip
from collections import Counter
from pathlib import Path
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
prog = M.load_program(M.COVERS / 'core_000.json.gz')
shards = {}
for p in sorted((M.SC / 'k2bcprod' / 'shards').glob('*.json.gz')):
    d = json.loads(gzip.decompress(p.read_bytes()))
    for rec in d['cases']:
        shards[(d['core_index'], rec['boundary_index'])] = rec['counts']
cases = [(int(a), int(b)) for a, b in (x.split(':') for x in ARGS[1].split(','))]
t0 = time.time(); tot = Counter()
for ci, bi in cases:
    cv = M.cover(ci); core = cv['core']; bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    leaves = [a for a, _ in prog.gen_attachments(core, bd)]
    st = {}
    for a in leaves:
        st[tuple(a)] = prog.frontier(prog.materialize(core, bd, a), True)['status']
    canon_counts = Counter(st[a] for a in st if prog.attachment_canon(a) == a)
    orbit_ok = all(st[a].startswith('EXCLUDED') for a in st)
    # orbits: every member maps to a canonical leaf that is itself a leaf
    orb_closed = all(prog.attachment_canon(a) in st for a in st)
    shard = shards[(ci, bi)]
    shard_counts = Counter({k: v for k, v in shard.items() if k.startswith('EXCLUDED_') and k != 'EXCLUDED_SYMMETRIC_ATTACHMENT'})
    same = canon_counts == shard_counts and shard.get('valid_partial', 0) == len(leaves)
    tot['leaves'] += len(leaves); tot['bad'] += (not orbit_ok); tot['mismatch'] += (not same)
    print(ci, bi, 'leaves', len(leaves), 'all members excluded', orbit_ok, 'orbits closed', orb_closed,
          'canonical counts == shard', same, dict(Counter(st.values())), flush=True)
print(dict(tot), 'secs %.0f' % (time.time() - t0))
