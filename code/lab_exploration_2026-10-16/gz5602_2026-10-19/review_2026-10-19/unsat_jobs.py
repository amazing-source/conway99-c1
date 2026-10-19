# Collect the (boundary, attachment, sigma) that production refuted by SAT: rerun current py_extend frontier-only
# with --all-attachments on production-EXCLUDED boundaries having sat_calls > 0; their open attachments are exactly
# the SAT-stage inputs.  Writes a job list for indep_sat.py.
import gzip, json, subprocess, sys
W, codex, cover, shard, fam, out, maxb = sys.argv[1:8]
prod = json.loads(gzip.decompress(open(shard, 'rb').read()))
idx = [c['boundary_index'] for c in prod['cases'] if c['status'].startswith('EXCLUDED')
       and c['counts'].get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0) > 0][:int(maxb)]
expect = {c['boundary_index']: c['counts'].get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0) for c in prod['cases']}
idxf = out + '.idx'; open(idxf, 'w').write(json.dumps(idx))
op = out + '.gz'
src = json.loads(gzip.decompress(open(cover, 'rb').read()))
r = subprocess.run([sys.executable, '-I', W + '/py_extend.py', codex, fam, cover, '0', str(src['boundary_count']),
                    '--all-attachments', '--outside-c2', '--indices=' + idxf, '--out=' + op], capture_output=True, text=True, timeout=280)
assert r.returncode == 0, r.stderr[-800:]
d = json.loads(gzip.decompress(open(op, 'rb').read()))
jobs = []
for c in d['cases']:
    opens = c.get('witness', {}).get('open_attachments', [])
    assert 0 < len(opens) <= expect[c["boundary_index"]], (c['boundary_index'], len(opens), expect[c['boundary_index']])
    for a in opens:
        jobs.append({'boundary_index': c['boundary_index'], 'attachment': a['attachment'], 'sigma': a['sigma'], 'expected': 'UNSAT'})
json.dump(jobs, open(out, 'w'))
print(len(idx), 'boundaries', len(jobs), 'SAT-stage attachments')
