"""Assemble the P3 (or K3, same format) coverage of the LAB py_extend.py production (LAB 19/10/2026).
Never certifies an omitted or non-excluded boundary.  Checks, for every orbit representative of the 114 shared-pair
cores (paircore_orbits16.json):
  * the boundary cover exists; a cover with status EXCLUDED_Q12_COLOUR_FACTORS must also be excluded in Codex's
    colour-factor file (independent record, 'EXCLUDED_COLOUR_FACTORS' with no colouring);
  * otherwise every boundary index 0..n-1 appears in exactly one shard case, with the cover's boundary_hex, from a shard
    whose source_sha256 is the cover's sha256, whose status is EXCLUDED_*, and whose counts are consistent (every
    attachment is refuted: valid_partial = sum of the EXCLUDED_* counts; sat_calls = number of RUP-checked UNSAT).
It does not repeat the search.
  * optional --residual DIR: a border whose production record is not excluded (UNKNOWN at the conflict budget, or SAT)
    is covered when a second-pass record (--all-attachments, larger budget) in DIR excludes it, with the same source
    hash, border hex and consistent counts (no OPEN_* entry).
usage: python p3_manifest.py <cover dir> <shard dir> <orbits json> <codex colour factors json> <out.json> [--residual DIR]
       [--family P3|P3NB]   (P3NB: orbits json = pybd_p3nb_all/core_reps_flips.json)"""
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit('refusing to run with python -O: the checks are assert statements')


def read(p):
    raw = Path(p).read_bytes()
    return json.loads(gzip.decompress(raw) if str(p).endswith('.gz') else raw)


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


ALLOWED_FLAGS = {'--sat', '--lean', '--enc=seq', '--all-attachments'}
ALLOWED_EXCLUSIONS = {'EXCLUDED_NEGATIVE_KNOWN_DEFICIT', 'EXCLUDED_NEGATIVE_LETTER_DEFICIT', 'EXCLUDED_EMPTY_VERTEX_DOMAIN',
                      'EXCLUDED_PROFILE_CAPACITY', 'EXCLUDED_PROFILE_PROPAGATION', 'EXCLUDED_INCLUSION',
                      'EXCLUDED_OUTSIDE_PROFILE_C2', 'EXCLUDED_PROFILE_SELECTION_UNSAT', 'EXCLUDED_DUPLICATE_ROWS'}


def check_flags(d, family):
    fl = [f for f in d['flags'] if not f.startswith(('--indices=', '--out=', '--conflicts='))]
    assert set(fl) <= ALLOWED_FLAGS and '--sat' in fl and '--lean' in fl and '--enc=seq' in fl, ('flags', d['flags'])
    assert d['summary']['family'] == family, ('family', d['summary']['family'], family)


cover_dir, shard_dir, orbits, colours, out = map(Path, sys.argv[1:6])
RESID = next((Path(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == "--residual"), None)
FAMILY = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--family"), "P3")
assert FAMILY in ("P3", "P3NB"), FAMILY      # P3NB: covers under the core flip group (28 types), no colour-factor cores
pending = {}
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
        assert FAMILY == 'P3', 'colour-factor exclusion needs Q12 to be a grid'
        r = colour[ci]
        assert r['status'] == 'EXCLUDED_COLOUR_FACTORS' and not r['colourings'], ci
    else:
        assert c['status'] == 'COMPLETE_BOUNDARY_COVER' and len(c['boundaries_hex']) == c['boundary_count']
        assert c.get('family') == FAMILY, ('cover family', c.get('family'))
        seen[ci] = bytearray(c['boundary_count'])
files, programs, totals = [], Counter(), Counter()
for p in sorted(shard_dir.glob('*.json.gz')):
    d = read(p)
    ci = d['core_index']
    assert ci in seen, (p, ci)
    assert d['source_sha256'] == covers[ci]['sha256'], (p, 'source hash')
    assert d['total_boundaries'] == covers[ci]['n']
    check_flags(d, FAMILY)
    programs[d['program_sha256']] += 1
    for rec in d['cases']:
        bi = rec['boundary_index']
        assert 0 <= bi < covers[ci]['n'] and not seen[ci][bi], (ci, bi, 'duplicate or invalid')
        assert rec['boundary_hex'] == covers[ci]['hex'][bi], (ci, bi, 'hex')
        if rec['status'] != 'EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER':
            pending[(ci, bi)] = rec['status']; seen[ci][bi] = 2       # 2 = present but not excluded (yet)
            continue
        cnt = rec['counts']
        assert all(k in ALLOWED_EXCLUSIONS for k in cnt if k.startswith('EXCLUDED_')), ('unexpected exclusion kind', cnt)
        exc = sum(v for k, v in cnt.items() if k.startswith('EXCLUDED_'))
        assert cnt.get('valid_partial', 0) == exc, (ci, bi, cnt)
        assert cnt.get('sat_calls', 0) == cnt.get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0), (ci, bi, cnt)
        seen[ci][bi] = 1
        totals.update({k: v for k, v in cnt.items() if k != 'max_conflicts'})
    files.append({'path': str(p), 'sha256': digest(p), 'core': ci, 'cases': len(d['cases']),
                  'program_sha256': d['program_sha256'], 'flags': d['flags'][:3]})
second = 0
if RESID is not None:
    for p in sorted(RESID.glob('*.json.gz')):
        d = read(p)
        ci = d['core_index']
        assert d['source_sha256'] == covers[ci]['sha256'] and '--all-attachments' in d['flags'], p
        check_flags(d, FAMILY)
        for rec in d['cases']:
            bi = rec['boundary_index']
            assert rec['boundary_hex'] == covers[ci]['hex'][bi]
            if seen[ci][bi] != 2 or rec['status'] != 'EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER':
                continue
            cnt = rec['counts']
            assert not any(k.startswith('OPEN_') for k in cnt)
            assert all(k in ALLOWED_EXCLUSIONS for k in cnt if k.startswith('EXCLUDED_')), ('unexpected exclusion kind', cnt)
            assert cnt.get('valid_partial', 0) == sum(v for k, v in cnt.items() if k.startswith('EXCLUDED_'))
            assert cnt.get('sat_calls', 0) == cnt.get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0)
            seen[ci][bi] = 1; second += 1; pending.pop((ci, bi), None)
            files.append({'path': str(p), 'sha256': digest(p), 'core': ci, 'cases': 1, 'stage': 'second_pass'})
covered = {ci: sum(1 for x in v if x == 1) for ci, v in seen.items()}
complete = not missing and all(covered[ci] == covers[ci]['n'] for ci in seen)
res = {'scope': __doc__, 'complete': complete, 'family_excluded': complete,
       'missing_covers': missing, 'covered_by_core': covered,
       'expected_by_core': {ci: covers[ci]['n'] for ci in seen},
       'colour_factor_cores': [ci for ci in covers if covers[ci]['status'] == 'EXCLUDED_Q12_COLOUR_FACTORS'],
       'boundaries_total': sum(covers[ci]['n'] for ci in seen), 'boundaries_covered': sum(covered.values()),
       'attachment_totals': dict(totals), 'program_sha256_counts': dict(programs),
       'second_pass_exclusions': second, 'still_pending': [[c, b, st] for (c, b), st in sorted(pending.items())],
       'covers': {ci: {k: covers[ci][k] for k in ('path', 'sha256', 'status', 'n')} for ci in covers},
       'colour_factor_file': {'path': str(colours), 'sha256': digest(colours)},
       'orbits_file': {'path': str(orbits), 'sha256': digest(orbits)}, 'shards': files}
assert not out.exists()
out.write_text(json.dumps(res, indent=1))
print(json.dumps({k: res[k] for k in ('complete', 'boundaries_total', 'boundaries_covered', 'missing_covers',
                                      'second_pass_exclusions', 'still_pending',
                                      'colour_factor_cores', 'attachment_totals', 'program_sha256_counts')}))
