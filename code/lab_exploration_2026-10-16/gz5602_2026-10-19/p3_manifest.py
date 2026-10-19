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
  * (review 19/10, 07:30 UTC) every cover's embedded core equals paircores8.json[ci]; optional pins: --program-sha=HEX
    (every shard and second-pass record ran that program), --codex-dir=DIR (their Codex module hashes are those of the
    files in DIR), --cover-symmetry=STRING (every cover was built under that group); the output records the enforced
    configuration, the cover symmetries, the full flags of every shard and the Codex module hashes.
usage: python p3_manifest.py <cover dir> <shard dir> <orbits json> <codex colour factors json> <out.json> [--residual DIR]
       [--family P3|P3NB|GEN [--yr=.. --extra=..]] [--program-sha=HEX] [--codex-dir=DIR] [--cover-symmetry=STRING]
       (P3NB / GEN: orbits json = <cover dir>/core_reps_flips.json)"""
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


ALLOWED_FLAGS = {'--sat', '--lean', '--enc=seq', '--all-attachments', '--verbose'}   # --verbose only logs
ALLOWED_EXCLUSIONS = {'EXCLUDED_NEGATIVE_KNOWN_DEFICIT', 'EXCLUDED_NEGATIVE_LETTER_DEFICIT', 'EXCLUDED_EMPTY_VERTEX_DOMAIN',
                      'EXCLUDED_PROFILE_CAPACITY', 'EXCLUDED_PROFILE_PROPAGATION', 'EXCLUDED_INCLUSION',
                      'EXCLUDED_OUTSIDE_PROFILE_C2', 'EXCLUDED_PROFILE_SELECTION_UNSAT', 'EXCLUDED_DUPLICATE_ROWS',
                      'EXCLUDED_SYMMETRIC_ATTACHMENT'}


GEN_CFG = [a for a in sys.argv if a.startswith(('--yr=', '--extra='))]
_opt = lambda name: next((a.split('=', 1)[1] for a in sys.argv if a.startswith(name + '=')), None)
PIN_PROGRAM = _opt('--program-sha')
CODEX_DIR = _opt('--codex-dir')
PIN_SYMMETRY = _opt('--cover-symmetry')
CODEX_SHA = None
if CODEX_DIR is not None:
    CODEX_SHA = {}


def check_provenance(d):
    if PIN_PROGRAM is not None:
        assert d['program_sha256'] == PIN_PROGRAM, ('program hash', d['program_sha256'])
    if CODEX_DIR is not None:
        mods = d['codex_modules_sha256']
        assert mods, 'no Codex module hashes recorded'
        for name, h in mods.items():
            if name not in CODEX_SHA:
                CODEX_SHA[name] = hashlib.sha256((Path(CODEX_DIR) / name).read_bytes()).hexdigest()
            assert h == CODEX_SHA[name], ('Codex module hash', name)


def check_flags(d, family):
    fl = [f for f in d['flags'] if not f.startswith(('--indices=', '--out=', '--conflicts='))]
    if family == 'GEN':                       # the configuration must be exactly the one being assembled
        cfg = sorted(f for f in fl if f.startswith(('--yr=', '--extra=')))
        assert cfg == sorted(GEN_CFG) and len(cfg) == 2, ('GEN configuration', cfg, GEN_CFG)
        fl = [f for f in fl if not f.startswith(('--yr=', '--extra='))]
    assert set(fl) <= ALLOWED_FLAGS and '--sat' in fl and '--lean' in fl and '--enc=seq' in fl, ('flags', d['flags'])
    assert d['summary']['family'] == family, ('family', d['summary']['family'], family)


cover_dir, shard_dir, orbits, colours, out = map(Path, sys.argv[1:6])
RESID = next((Path(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == "--residual"), None)
FAMILY = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--family"), "P3")
assert FAMILY in ("P3", "P3NB", "GEN"), FAMILY      # P3NB: covers under the core flip group (28 types), no colour-factor cores
pending = {}
reps = read(orbits)['representatives']
if FAMILY != 'P3':
    # recompute the flip orbits of the 114 labelled cores independently (letter flips of lines 0, 1, 2; no swap) and
    # require the orbits file to list exactly one representative per orbit (review 19/10: do not trust the cover writer)
    from itertools import product as _prod
    _cores = read(Path(__file__).with_name('paircores8.json'))
    _CL = [(2 * i + s_, 2 * j + t_) for (i, j) in ((0, 1), (0, 2)) for s_, t_ in _prod(range(2), repeat=2)]
    _LK = {q: k for k, q in enumerate(_CL)}
    _flips = [[_LK[tuple(sorted(x ^ f[x // 2] for x in q))] for q in _CL] for f in _prod(range(2), repeat=3)]
    _key = lambda c, pm: tuple(sorted(tuple(sorted((pm[u], pm[v]))) for u, v in c['edges']))
    _orb = {}
    for ci_, c_ in enumerate(_cores):
        _orb.setdefault(min(_key(c_, pm) for pm in _flips), []).append(ci_)
    assert len(_cores) == 114 and len(_orb) == len(reps), ('flip orbits', len(_orb), len(reps))
    assert sorted(min(_key(_cores[r], pm) for pm in _flips) for r in reps) == sorted(_orb), 'orbits file does not hit every flip orbit once'
colour = {r['core_index']: r for r in read(colours)['results']}
ALL_CORES = read(Path(__file__).with_name('paircores8.json'))
covers, seen, missing, symmetries = {}, {}, [], set()
for ci in reps:
    p = cover_dir / ('core_%03d.json.gz' % ci)
    if not p.exists():
        missing.append(ci); continue
    c = read(p)
    assert c['core_index'] == ci
    if 'core' in c:
        assert c['core'] == ALL_CORES[ci], ('cover core differs from paircores8.json', ci)
    symmetries.add(c.get('symmetry'))
    if PIN_SYMMETRY is not None and c['status'] == 'COMPLETE_BOUNDARY_COVER':
        assert c.get('symmetry') == PIN_SYMMETRY, ('cover symmetry', ci, c.get('symmetry'))
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
    check_provenance(d)
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
                  'program_sha256': d['program_sha256'], 'flags': d['flags'],
                  'codex_modules_sha256': d.get('codex_modules_sha256')})
second = 0
if RESID is not None:
    for p in sorted(RESID.glob('*.json.gz')):
        d = read(p)
        ci = d['core_index']
        assert d['source_sha256'] == covers[ci]['sha256'] and '--all-attachments' in d['flags'], p
        check_flags(d, FAMILY)
        check_provenance(d)
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
       'configuration': {'family': FAMILY, 'gen_configuration': sorted(GEN_CFG), 'pinned_program_sha256': PIN_PROGRAM,
                         'pinned_cover_symmetry': PIN_SYMMETRY, 'codex_dir': CODEX_DIR,
                         'codex_modules_sha256_checked': CODEX_SHA},
       'cover_symmetries': sorted(s for s in symmetries if s is not None),
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
