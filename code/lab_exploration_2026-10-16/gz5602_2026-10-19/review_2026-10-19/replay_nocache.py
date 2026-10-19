import gzip, json, subprocess, sys
W, codex, cover, shard, fam, outdir = sys.argv[1:7]
prod = json.loads(gzip.decompress(open(shard, 'rb').read()))
idx = [c['boundary_index'] for c in prod['cases'] if c['status'].startswith('EXCLUDED')]
idxf = outdir + '/replay_idx.json'; open(idxf, 'w').write(json.dumps(idx))
op = outdir + '/replay_out.json.gz'
src = json.loads(gzip.decompress(open(cover, 'rb').read()))
r = subprocess.run([sys.executable, '-I', W + '/py_extend.py', codex, fam, cover, '0', str(src['boundary_count']),
                    '--all-attachments', '--outside-c2', '--indices=' + idxf, '--out=' + op], capture_output=True, text=True, timeout=290)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
rep = {c['boundary_index']: c for c in json.loads(gzip.decompress(open(op, 'rb').read()))['cases']}
mism = 0
for c in prod['cases']:
    if not c['status'].startswith('EXCLUDED'): continue
    p = c['counts']; q = rep[c['boundary_index']]['counts']
    unsat_p = p.get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0) + (p.get('EXCLUDED_DUPLICATE_ROWS', 0) * 0)
    open_q = q.get('OPEN_PASSES_PROFILE_PROPAGATION', 0) + q.get('OPEN_DUPLICATE_ROWS', 0)
    frt_p = sum(v for k, v in p.items() if k.startswith('EXCLUDED_') and k not in ('EXCLUDED_PROFILE_SELECTION_UNSAT',))
    frt_q = sum(v for k, v in q.items() if k.startswith('EXCLUDED_'))
    ok = (p['valid_partial'] == q['valid_partial'] and unsat_p == open_q and frt_p == frt_q)
    if not ok:
        mism += 1
        if mism <= 3: print('MISMATCH', c['boundary_index'], p, q)
print(json.dumps({'shard': shard.split('/')[-1], 'program': prod['program_sha256'][:8], 'records': len(idx), 'mismatches': mism}))
