"""2K2N residual classes x B/C grid marks (LAB 19/10/2026), with Codex's wrapper root_component_lab_profile_export.py
(main a4089769) and the archived LAB 2K2N source (sha c140d0e9, the one of Codex's case000).  For each class
representative (core, border, sigma) of k2k2n_residual_classes.json and each B/C mark Q1d, Q2d (d = 3..6) it runs the
ladder of models
   one completed grid row: corner 1, then 0, 2, 3 (corners in lexicographic label order), no signed core;
   the four grid rows, no signed core;
   the four grid rows with Codex's signed root core 0 1 2 and --forbid-q12-grid (this one uses the 2K2 closure);
and stops at the first certified UNSAT: frontier EXCLUDED_PROFILE_SELECTION_UNSAT whose proof was checked by drat-trim -U
('s VERIFIED', RUP only).  All profile choices to the 16 known labels stay free in every model; the grid constraints
are those of Codex's note GRILLES_BC_PROFILS_2K2N_2026_10_19.txt (exact domination for r = 7).
Scope: an exclusion of (class, mark) excludes every member (B, sigma') of the class WITH the transported mark; the
stabiliser of a border maps the set of the eight B/C rectangles onto itself, so a class whose 8 marks are excluded
cannot occur in a graph having at least one B/C grid.  It says nothing about a residual with no B/C grid.
The duplicate artefacts of each run (row_cut_cnf.json.gz, row_cut_proof.rup.gz = the same clauses and proof as the
native pair, and the per-run copy of the LAB source) are deleted after their hashes are checked; the drat-trim input
pair native.cnf.gz + native.input.rup.gz is kept for every exclusion.
usage: python lab_2k2n_bc_driver.py <codex root> <lab source> <cover dir> <classes json> <out dir> <k> <N>
       [--only=i,j,...] [--cpu=c]   (worker k of N takes the classes i = k mod N; --cpu pins this worker)"""
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit('refusing to run with python -O: the checks are assert statements')
ROOT, LAB, COVERS, CLASSES, OUT = map(Path, sys.argv[1:6])
K, N = int(sys.argv[6]), int(sys.argv[7])
ONLY = next((set(map(int, a.split('=', 1)[1].split(','))) for a in sys.argv if a.startswith('--only=')), None)
CPU = next((int(a.split('=', 1)[1]) for a in sys.argv if a.startswith('--cpu=')), None)
if CPU is not None and sys.platform == 'win32':        # children inherit the mask; Codex's limiter keeps its first CPU
    import ctypes
    k32 = ctypes.WinDLL('kernel32', use_last_error=True)
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert k32.SetProcessAffinityMask(k32.GetCurrentProcess(), 1 << CPU), ctypes.get_last_error()
    k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    k32.SetPriorityClass(k32.GetCurrentProcess(), 0x00004000)
WRAP = ROOT / 'code/codex/root_component_lab_profile_export.py'
PY = sys.executable
LAB_SHA = hashlib.sha256(LAB.read_bytes()).hexdigest()
MARKS = [(i, j) for i in (1, 2) for j in (3, 4, 5, 6)]
LADDER = [('row1', [1], False, 20), ('row0', [0], False, 20), ('row2', [2], False, 20), ('row3', [3], False, 20),
          ('rows4', [0, 1, 2, 3], False, 120), ('rows4s', [0, 1, 2, 3], True, 300)]
items = json.load(open(CLASSES))['items']
OUT.mkdir(parents=True, exist_ok=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(prefix, it, mark, hubs, signed, cpu_s):
    cover = COVERS / ('core_%03d.json.gz' % it['core_index'])
    cmd = [PY, '-I', '-u', '-X', 'utf8', str(WRAP), str(LAB), str(cover), '--index', str(it['boundary_index']),
           '--family', '2K2N', '--sigma', *map(str, it['representative_sigma']), '--outside-grid', str(mark[0]),
           str(mark[1]), '--extend-rows', *map(str, hubs), '--row-cut-cpu-seconds', str(cpu_s),
           '--proof-checker', 'native', '--output', str(prefix.with_suffix('.json'))]
    if signed:
        cmd += ['--signed-root-core', '0', '1', '2', '--forbid-q12-grid']
    t = time.time()
    with prefix.with_suffix('.driver.log').open('wb') as log:
        r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT,
                           creationflags=0x08000000 if sys.platform == 'win32' else 0)
    # v2 (19/10 13:10 local): a failing wrapper run is an inconclusive attempt, never an exclusion (e.g. drat-trim
    # exits 1 on a 'trivial UNSAT' formula although it prints 's VERIFIED'; Codex's checker then raises).  The ladder
    # moves on to the next model.
    return time.time() - t, sha(cover), r.returncode


def check(prefix, it, mark, hubs, signed, cover_sha, ref):
    result = json.loads(gzip.decompress(prefix.with_suffix('.lab_result.json.gz').read_bytes()))
    learning = json.loads(prefix.with_suffix('.row_cut_learning.json').read_text())
    used = json.loads(prefix.with_suffix('.row_cut_input.json').read_text())
    assert used['lab_source_sha256'] == LAB_SHA
    if ref.get('input') is None:
        ref['input'] = used
    else:
        assert used == ref['input'], 'the fixed block changed between two runs of one class'
    corners = [y for y, q in enumerate(used['outside_labels']) if {l // 2 for l in q} == set(mark)]
    assert len(corners) == 4 and [corners[c] for c in ref['corner_ids']] == hubs
    assert result['boundary_source_sha256'] == cover_sha and result['boundary_index'] == it['boundary_index']
    assert result['sigma'] == it['representative_sigma'] and result['attachments'] == []
    assert learning['outside_grid_constraints']['grids'] == [{'root_pair': list(mark), 'outside_corners': corners}]
    assert learning['extension']['hubs'] == hubs
    assert ('signed_internal_core' in learning) == signed
    if signed:
        assert learning['signed_internal_core']['forbid_q12_grid']
    assert gzip.decompress(prefix.with_suffix('.lab_source.py.gz').read_bytes()) == LAB.read_bytes()
    front = result['frontier']
    proof = front.get('proof_check') or {}
    excluded = (front['status'] == 'EXCLUDED_PROFILE_SELECTION_UNSAT' and proof.get('empty_clause_verified') is True
                and proof.get('rup_only') is True and proof.get('checker') == 'drat-trim -U')
    if excluded:
        assert prefix.with_suffix('.native.cnf.gz').exists() and prefix.with_suffix('.native.input.rup.gz').exists()
        assert 's VERIFIED' in prefix.with_suffix('.native.log').read_text(errors='replace').splitlines()
    return excluded, front['status'], learning['rounds'][-1]['cpu_seconds'], front.get('conflicts'), front['clauses'], proof


def prune(prefix, keep_input):
    for suf in ('.row_cut_cnf.json.gz', '.row_cut_proof.rup.gz', '.lab_source.py.gz') + (() if keep_input else ('.row_cut_input.json',)):
        f = prefix.with_suffix(suf)
        if f.exists():
            f.unlink()


for idx, it in enumerate(items):
    if idx % N != K or (ONLY is not None and idx not in ONLY):
        continue
    rep_path = OUT / ('class%04d.json' % idx)
    if rep_path.exists():
        continue
    cdir = OUT / ('class%04d' % idx)
    cdir.mkdir(exist_ok=True)
    report = {'scope': __doc__.split('\n')[0], 'class_index': idx, 'core_index': it['core_index'],
              'boundary_index': it['boundary_index'], 'boundary_hex': it['boundary_hex'],
              'representative_sigma': it['representative_sigma'], 'members': it['members'],
              'lab_source_sha256': LAB_SHA, 'wrapper_sha256': sha(WRAP), 'marks': []}
    ref = {}
    first = True
    t_class = time.time()
    for mark in MARKS:
        row = {'grid': list(mark), 'status': None, 'attempts': []}
        for name, cids, signed, cpu_s in LADDER:
            prefix = cdir / ('m%d%d_%s' % (mark[0], mark[1], name))
            if ref.get('input') is None:
                # outside label order of the LAB 2K2N model (identical for every class; re-checked after the run)
                outside = json.load(open(ROOT / 'data/codex_short_columns_20261018/shared_2k2n_residuals_20261019/'
                                         'case000.row_cut_input.json'))['outside_labels']
            else:
                outside = ref['input']['outside_labels']
            corners = [y for y, q in enumerate(outside) if {l // 2 for l in q} == set(mark)]
            hubs = [corners[c] for c in cids]
            ref['corner_ids'] = cids
            wall, cover_sha, rc = run(prefix, it, mark, hubs, signed, cpu_s)
            if rc != 0:
                row['attempts'].append({'model': name, 'grid_row_corners': cids, 'signed_core': signed,
                                        'status': 'WRAPPER_ERROR', 'returncode': rc, 'excluded': False,
                                        'wall_seconds': round(wall, 2), 'prefix': str(prefix.relative_to(OUT))})
                continue
            excluded, status, cpu, conflicts, clauses, proof = check(prefix, it, mark, hubs, signed, cover_sha, ref)
            prune(prefix, keep_input=first)
            first = False
            att = {'model': name, 'grid_row_corners': cids, 'signed_core': signed, 'status': status,
                   'excluded': excluded, 'search_cpu_seconds': cpu, 'conflicts': conflicts, 'clauses': clauses,
                   'wall_seconds': round(wall, 2), 'prefix': str(prefix.relative_to(OUT))}
            if excluded:
                att['proof_check'] = {k: proof.get(k) for k in ('checker', 'rup_only', 'empty_clause_verified',
                                                                 'input_additions', 'checker_sha256', 'artifacts')}
            row['attempts'].append(att)
            if excluded:
                row['status'] = 'EXCLUDED'
                row['excluded_by'] = name
                break
        if row['status'] is None:
            row['status'] = 'OPEN'
        report['marks'].append(row)
    report['all_eight_marks_excluded'] = all(r['status'] == 'EXCLUDED' for r in report['marks'])
    report['wall_seconds'] = round(time.time() - t_class, 1)
    tmp = rep_path.with_suffix('.tmp')
    tmp.write_text(json.dumps(report, indent=1))
    tmp.replace(rep_path)
    print(json.dumps({'class': idx, 'core': it['core_index'], 'border': it['boundary_index'],
                      'all8': report['all_eight_marks_excluded'],
                      'by': [r.get('excluded_by', 'OPEN') for r in report['marks']], 'wall': report['wall_seconds']}),
          flush=True)
