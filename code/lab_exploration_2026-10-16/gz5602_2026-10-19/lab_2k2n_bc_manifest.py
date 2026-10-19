"""Assemble the 2K2N B/C-mark production (LAB 19/10/2026).  Never certifies an omitted class or mark.
Checks, for every class of k2k2n_residual_classes.json (the 816 exact classes of the 1006 residual 2K2N attachments of
stage 1, i.e. every 2K2N attachment not excluded by the stage-1 model of the 2K2 two-stage manifest):
  * its report classNNNN.json exists, names the same core, border and representative sigma, and has the 8 marks
    Q13 Q14 Q15 Q16 Q23 Q24 Q25 Q26, each EXCLUDED by an attempt whose frontier was EXCLUDED_PROFILE_SELECTION_UNSAT
    with a drat-trim -U 's VERIFIED' proof (proof_check recorded), or, for the attempts listed in TRIVIAL (where
    Codex's checker raised because drat-trim exits 1 on a 'trivial UNSAT' formula), by an independent unit-propagation
    conflict on the saved native CNF (re-run here);
  * the LAB source and wrapper hashes are the same in every report.
Scope: an exclusion of (class, mark) excludes every member (B, sigma') of the class with the transported mark; the
stabiliser of a border maps the eight B/C rectangles onto themselves, so a 2K2N template whose normal form (witness)
has at least one B/C grid is excluded (all its stage-1 survivors die with any B/C mark).
usage: python lab_2k2n_bc_manifest.py <classes json> <production dir> <out.json>"""
import gzip
import hashlib
import json
import os
import sys
from pathlib import Path

CLASSES, PROD, OUT = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
if sys.flags.optimize:
    raise SystemExit('assertions required')
assert not OUT.exists()
items = json.load(open(CLASSES))['items']
MARKS = [[1, 3], [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6]]
TRIVIAL = {(399, (2, 3)), (399, (2, 4))}


def unit_propagation_conflict(path):
    op = gzip.open if str(path).endswith('.gz') else open
    clauses = []
    with op(path, 'rt') as f:
        for line in f:
            if line.startswith(('p', 'c')) or not line.strip():
                continue
            clauses.append([int(x) for x in line.split()][:-1])
    assign, changed = {}, True
    while changed:
        changed = False
        for c in clauses:
            if any(assign.get(abs(l)) == (l > 0) for l in c if abs(l) in assign):
                continue
            free = [l for l in c if abs(l) not in assign]
            if not free:
                return True
            if len(free) == 1:
                assign[abs(free[0])] = free[0] > 0; changed = True
    return False


hashes, missing, bad, trivial_checked = set(), [], [], []
for idx, it in enumerate(items):
    p = PROD / ('class%04d.json' % idx)
    if not p.exists():
        missing.append(idx); continue
    r = json.load(open(p))
    assert (r['core_index'], r['boundary_index'], r['representative_sigma']) == (it['core_index'], it['boundary_index'], it['representative_sigma']), idx
    hashes.add((r['lab_source_sha256'], r['wrapper_sha256']))
    assert [m['grid'] for m in r['marks']] == MARKS, (idx, 'marks')
    for m in r['marks']:
        key = (idx, tuple(m['grid']))
        if key in TRIVIAL:
            cnf = PROD / ('class%04d' % idx) / ('m%d%d_row1.native.cnf' % tuple(m['grid']))
            if not cnf.exists():                     # committed copy keeps the CNF gzipped
                cnf = cnf.with_name(cnf.name + '.gz')
            assert unit_propagation_conflict(cnf), key
            trivial_checked.append([idx, m['grid'], str(cnf.name)])
            continue
        if m['status'] != 'EXCLUDED':
            bad.append([idx, m['grid'], m['status']]); continue
        att = m['attempts'][-1]
        assert att['excluded'] and att['status'] == 'EXCLUDED_PROFILE_SELECTION_UNSAT', key
        pc = att['proof_check']
        assert pc['checker'] == 'drat-trim -U' and pc['rup_only'] and pc['empty_clause_verified'], key
complete = not missing and not bad and len(hashes) == 1
res = {'scope': __doc__, 'complete': complete, 'classes': len(items), 'missing': missing, 'not_excluded': bad,
       'trivial_unsat_marks_checked_by_unit_propagation': trivial_checked, 'source_and_wrapper_hashes': sorted(hashes),
       'classes_file_sha256': hashlib.sha256(open(CLASSES, 'rb').read()).hexdigest()}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps({k: res[k] for k in ('complete', 'classes', 'missing', 'not_excluded', 'trivial_unsat_marks_checked_by_unit_propagation')}))
