# Replay a production shard with the CURRENT py_extend in frontier-only mode (--all-attachments --outside-c2, no SAT)
# and compare, boundary by boundary, with the production record (EXCLUDED records only):
#   frontier exclusions must coincide; production UNSAT (+ duplicates) must be frontier-open in the replay.
import gzip, json, subprocess, sys
W, codex, cover, shard, fam, outdir = sys.argv[1:7]
prod = json.loads(gzip.decompress(open(shard, 'rb').read()))
idx = [c['boundary_index'] for c in prod['cases'] if c['status'].startswith('EXCLUDED')]
idxf = outdir + '/replay_idx.json'; open(idxf, 'w').write(json.dumps(idx))
op = outdir + '/replay_out.json.gz'
src = json.loads(gzip.decompress(open(cover, 'rb').read()))
r = subprocess.run([sys.executable, '-I', W + '/py_extend.py', codex, fam, cover, '0', str(src['boundary_count']),
                    '--all-attachments', '--outside-c2', '--indices=' + idxf, '--out=' + op],
                   capture_output=True, text=True, timeout=290)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
rep = {c['boundary_index']: c for c in json.loads(gzip.decompress(open(op, 'rb').read()))['cases']}
mism = 0; tot = 0
for c in prod['cases']:
    if not c['status'].startswith('EXCLUDED'): continue
    tot += 1
    p = {k: v for k, v in c['counts'].items() if k not in ('max_conflicts', 'sat_calls', 'rup_checked_additions')}
    q = {k: v for k, v in rep[c['boundary_index']]['counts'].items() if k != 'max_conflicts'}
    # map replay keys to production meaning
    front = {k: v for k, v in q.items() if k.startswith('EXCLUDED_') and k != 'EXCLUDED_DUPLICATE_ROWS'}
    pf = {k: v for k, v in p.items() if k.startswith('EXCLUDED_') and k not in ('EXCLUDED_DUPLICATE_ROWS', 'EXCLUDED_PROFILE_SELECTION_UNSAT')}
    has_cache = 'EXCLUDED_DUPLICATE_ROWS' in p or any('DUPLICATE' in k for k in q)
    ok = q.get('valid_partial') == p.get('valid_partial')
    if 'EXCLUDED_DUPLICATE_ROWS' in p or not any('DUPLICATE' in k for k in q):
        # same caching behaviour: exact comparison
        ok &= front == pf
        ok &= q.get('OPEN_PASSES_PROFILE_PROPAGATION', 0) == p.get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0)
        ok &= q.get('EXCLUDED_DUPLICATE_ROWS', 0) + q.get('OPEN_DUPLICATE_ROWS', 0) == p.get('EXCLUDED_DUPLICATE_ROWS', 0)
    else:
        # production had no cache: compare distinct + duplicate totals per frontier status is not recoverable; compare sums
        ok &= sum(front.values()) + q.get('OPEN_PASSES_PROFILE_PROPAGATION', 0) + q.get('EXCLUDED_DUPLICATE_ROWS', 0) + q.get('OPEN_DUPLICATE_ROWS', 0) == p.get('valid_partial', 0)
        ok &= set(front) <= set(pf) | set()
    if not ok:
        mism += 1
        if mism <= 5: print('MISMATCH', c['boundary_index'], 'prod', p, 'replay', q)
print(json.dumps({'shard': shard.split('/')[-1], 'program': prod['program_sha256'][:8], 'excluded_records': tot, 'mismatches': mism}))
