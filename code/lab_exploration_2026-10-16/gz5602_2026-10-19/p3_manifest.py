"""Assemble the P3 (or K3, same format) coverage of the LAB py_extend.py production (LAB 19/10/2026).
Never certifies an omitted or non-excluded boundary.  Checks, for every orbit representative of the 114 shared-pair
cores (paircore_orbits16.json):
  * the boundary cover exists; a cover with status EXCLUDED_Q12_COLOUR_FACTORS must also be excluded in Codex's
    colour-factor file (independent record, 'EXCLUDED_COLOUR_FACTORS' with no colouring);
  * otherwise every boundary index 0..n-1 appears in exactly one shard case, with the cover's boundary_hex, from a shard
    whose source_sha256 is the cover's sha256, whose status is EXCLUDED_*, and whose counts are consistent (every
    attachment is refuted: valid_partial = sum of the EXCLUDED_* counts; sat_calls = number of RUP-checked UNSAT).
It does not repeat the search.
usage: python p3_manifest.py <cover dir> <shard dir> <orbits16.json> <codex colour factors json> <out.json>"""
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


def read(p):
    raw = Path(p).read_bytes()
    return json.loads(gzip.decompress(raw) if str(p).endswith('.gz') else raw)


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


cover_dir, shard_dir, orbits, colours, out = map(Path, sys.argv[1:6])
reps = read(orbits)['representatives']
colour = {r['core_index']: r for r in read(colours)['results']}
covers, seen, missing = {}, {}, []
for ci in reps:
    p = cover_dir / ('core_%03d.json.gz' % ci)
    if not p.exists():
        missing.append(ci); continue
    c = read(p)
    assert c['core_index'] == ci
    covers[ci] = {'path': str(p), 'sha256': digest(p), 'status': c['status'], 'n': c.get('boundary_count', 0),
                  'hex': c.get('boundaries_hex', [])}
    if c['status'] == 'EXCLUDED_Q12_COLOUR_FACTORS':
        r = colour[ci]
        assert r['status'] == 'EXCLUDED_COLOUR_FACTORS' and not r['colourings'], ci
    else:
        assert c['status'] == 'COMPLETE_BOUNDARY_COVER' and len(c['boundaries_hex']) == c['boundary_count']
        seen[ci] = bytearray(c['boundary_count'])
files, programs, totals = [], Counter(), Counter()
for p in sorted(shard_dir.glob('*.json.gz')):
    d = read(p)
    ci = d['core_index']
    assert ci in seen, (p, ci)
    assert d['source_sha256'] == covers[ci]['sha256'], (p, 'source hash')
    assert d['total_boundaries'] == covers[ci]['n']
    programs[d['program_sha256']] += 1
    for rec in d['cases']:
        bi = rec['boundary_index']
        assert 0 <= bi < covers[ci]['n'] and not seen[ci][bi], (ci, bi, 'duplicate or invalid')
        assert rec['boundary_hex'] == covers[ci]['hex'][bi], (ci, bi, 'hex')
        assert rec['status'] == 'EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER', (ci, bi, rec['status'])
        cnt = rec['counts']
        exc = sum(v for k, v in cnt.items() if k.startswith('EXCLUDED_'))
        assert cnt.get('valid_partial', 0) == exc, (ci, bi, cnt)
        assert cnt.get('sat_calls', 0) == cnt.get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0), (ci, bi, cnt)
        seen[ci][bi] = 1
        totals.update({k: v for k, v in cnt.items() if k != 'max_conflicts'})
    files.append({'path': str(p), 'sha256': digest(p), 'core': ci, 'cases': len(d['cases']),
                  'program_sha256': d['program_sha256'], 'flags': d['flags'][:3]})
covered = {ci: sum(v) for ci, v in seen.items()}
complete = not missing and all(covered[ci] == covers[ci]['n'] for ci in seen)
res = {'scope': __doc__, 'complete': complete, 'family_excluded': complete,
       'missing_covers': missing, 'covered_by_core': covered,
       'expected_by_core': {ci: covers[ci]['n'] for ci in seen},
       'colour_factor_cores': [ci for ci in covers if covers[ci]['status'] == 'EXCLUDED_Q12_COLOUR_FACTORS'],
       'boundaries_total': sum(covers[ci]['n'] for ci in seen), 'boundaries_covered': sum(covered.values()),
       'attachment_totals': dict(totals), 'program_sha256_counts': dict(programs),
       'covers': {ci: {k: covers[ci][k] for k in ('path', 'sha256', 'status', 'n')} for ci in covers},
       'colour_factor_file': {'path': str(colours), 'sha256': digest(colours)},
       'orbits_file': {'path': str(orbits), 'sha256': digest(orbits)}, 'shards': files}
assert not out.exists()
out.write_text(json.dumps(res, indent=1))
print(json.dumps({k: res[k] for k in ('complete', 'boundaries_total', 'boundaries_covered', 'missing_covers',
                                      'colour_factor_cores', 'attachment_totals', 'program_sha256_counts')}))
