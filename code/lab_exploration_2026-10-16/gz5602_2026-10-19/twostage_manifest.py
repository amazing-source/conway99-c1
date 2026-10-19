"""Assemble a two-stage family coverage (LAB 19/10/2026), e.g. 2K2 = stage 1 '2K2N' (Q_bc unknown, all boundaries)
then stage 2 '2K2' (Q_bc grid with its Q12 attachments) on the stage-1 survivors only.
Valid because the stage-1 constraints are a subset of the stage-2 ones (every stage-2 configuration restricts to a
stage-1 configuration with the same boundary).  Never certifies an omitted or non-excluded boundary.
For every orbit representative of the 114 shared-pair cores:
  * if Codex's colour-factor file says EXCLUDED_COLOUR_FACTORS (no colouring), the core is excluded for the stage-2
    family (Q_bc grid) by the factor lemma, whatever stage 1 says;
  * otherwise every boundary 0..n-1 of the cover must have an EXCLUDED record in the stage-1 shard or in the stage-2
    shard, both shards citing the cover's sha256, with consistent counts (all attachments refuted).
  * optional third source (--residual DIR --certificates JSON): a border whose --all-attachments record (residual
    shard) lists open attachments is excluded iff that record accounts for every attachment (valid_partial = EXCLUDED_*
    + OPEN_*) and EVERY listed open (attachment, sigma) has an external certificate with status EXCLUDED_* and a
    verified empty clause (Codex's continuation cuts), matched on core, border hex, attachment and sigma.
usage: python twostage_manifest.py <cover dir> <stage1 dir> <stage2 dir> <orbits16.json> <colour factors json> <out.json>
                                   [--residual DIR --certificates FILE.json]"""
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


cover_dir, st1, st2, orbits, colours, out = map(Path, sys.argv[1:7])
RESID = next((Path(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == "--residual"), None)
CERTF = next((Path(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == "--certificates"), None)
CERTS = {}
CERTROOT = next((Path(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == "--certificate-root"), None)
if CERTF is not None:
    for c in read(CERTF)["certificates"]:
        if c["status"].startswith("EXCLUDED") and c.get("empty_clause_verified") is True:
            if CERTROOT is not None:             # open every referenced certificate file and check its sha256
                for k in ("certificate", "certificate_path", "path"):
                    if k in c and isinstance(c[k], str):
                        f = CERTROOT / c[k]
                        assert f.exists(), ("missing certificate file", c[k])
                        want = c.get("certificate_sha256") or c.get("sha256")
                        assert want and digest(f) == want, ("certificate hash", c[k])
                        break
                else:
                    raise SystemExit("certificate entry without a file reference: %r" % (c,))
            CERTS[(c["core_index"], c["boundary_hex"], json.dumps(c["attachment"]), json.dumps(c["sigma"]))] = c
reps = read(orbits)['representatives']
colour = {r['core_index']: r for r in read(colours)['results']}
res_cores = {}; totals = Counter(); files = []; programs = Counter(); complete = True


def check_case(rec, cover):
    bi = rec['boundary_index']
    assert rec['boundary_hex'] == cover['boundaries_hex'][bi], ('hex', bi)
    if rec['status'] != 'EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER':
        return False
    cnt = rec['counts']
    assert all(k in ALLOWED_EXCLUSIONS for k in cnt if k.startswith('EXCLUDED_')), ('unexpected exclusion kind', cnt)
    exc = sum(v for k, v in cnt.items() if k.startswith('EXCLUDED_'))
    assert cnt.get('valid_partial', 0) == exc, (bi, cnt)
    assert cnt.get('sat_calls', 0) == cnt.get('EXCLUDED_PROFILE_SELECTION_UNSAT', 0), (bi, cnt)
    totals.update({k: v for k, v in cnt.items() if k != 'max_conflicts'})
    return True


for ci in reps:
    cp = cover_dir / ('core_%03d.json.gz' % ci)
    r = colour[ci]
    if r['status'] == 'EXCLUDED_COLOUR_FACTORS' and not r['colourings']:
        res_cores[ci] = {'status': 'EXCLUDED_COLOUR_FACTORS (factor lemma, Codex file)'}
        continue
    cover = read(cp); h = digest(cp)
    assert cover['core_index'] == ci and cover['status'] == 'COMPLETE_BOUNDARY_COVER'
    assert cover.get('family') in ('2K2N', '2K2'), ('cover family', cover.get('family'))
    n = cover['boundary_count']; assert len(cover['boundaries_hex']) == n
    done = bytearray(n); by = Counter()
    for stage, d_ in (('stage1', st1), ('stage2', st2)):
        for p in sorted(d_.glob('core%03d_*.json.gz' % ci)):
            d = read(p)
            assert d['core_index'] == ci and d['source_sha256'] == h and d['total_boundaries'] == n, p
            check_flags(d, '2K2N' if stage == 'stage1' else '2K2')
            programs[(stage, d['program_sha256'], tuple(d['flags'][:1]))] += 1
            files.append({'path': str(p), 'sha256': digest(p), 'stage': stage, 'cases': len(d['cases']),
                          'program_sha256': d['program_sha256']})
            for rec in d['cases']:
                if check_case(rec, cover):
                    if not done[rec['boundary_index']]:
                        done[rec['boundary_index']] = 1; by[stage] += 1
    if RESID is not None:
        for p in sorted(RESID.glob('core%03d_*.json.gz' % ci)):
            d = read(p)
            assert d['core_index'] == ci and d['source_sha256'] == h and '--all-attachments' in d['flags'], p
            check_flags(d, '2K2')
            files.append({'path': str(p), 'sha256': digest(p), 'stage': 'residual', 'cases': len(d['cases'])})
            for rec in d['cases']:
                bi = rec['boundary_index']
                assert rec['boundary_hex'] == cover['boundaries_hex'][bi]
                if done[bi]:
                    continue
                if check_case(rec, cover):
                    done[bi] = 1; by['residual'] += 1; continue
                cnt = rec['counts']
                tot = sum(v for k, v in cnt.items() if k.startswith(('EXCLUDED_', 'OPEN_')))
                opens = rec.get('witness', {}).get('open_attachments', [])
                if cnt.get('valid_partial') != tot or not opens:
                    continue
                if all((ci, rec['boundary_hex'], json.dumps(a['attachment']), json.dumps(a['sigma'])) in CERTS for a in opens):
                    done[bi] = 1; by['residual+certificates'] += 1
    ok = sum(done) == n
    complete &= ok
    res_cores[ci] = {'status': 'EXCLUDED_ALL_BOUNDARIES' if ok else 'INCOMPLETE', 'boundaries': n,
                     'excluded': sum(done), 'by_stage': dict(by), 'cover_sha256': h}
res = {'scope': __doc__, 'complete': complete, 'family_excluded': complete, 'cores': res_cores,
       'attachment_totals': dict(totals), 'programs': {str(k): v for k, v in programs.items()},
       'colour_factor_file': {'path': str(colours), 'sha256': digest(colours)},
       'orbits_file': {'path': str(orbits), 'sha256': digest(orbits)}, 'shards': files}
assert not out.exists()
out.write_text(json.dumps(res, indent=1))
print(json.dumps({'complete': complete, 'cores': {c: (v['status'], v.get('excluded'), v.get('boundaries'))
                                                  for c, v in res_cores.items()}, 'attachment_totals': dict(totals)}))
