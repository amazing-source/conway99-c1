"""Test all eight possible B/C-grid marks on ONE fixed 2K2N attachment.

Completing four marked grid rows keeps the matching choices free.
Even eight exclusions require the extra hypothesis that a B/C grid exists;
they do not exclude the unmarked 2K2N attachment or the whole family.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process

if not __debug__:
    raise RuntimeError('Marked-grid probes require assertions; do not use python -O.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('lab_source', type=Path)
    p.add_argument('boundary', type=Path)
    p.add_argument('source_input', type=Path)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--sigma', type=int, nargs=4, required=True)
    p.add_argument('--prefix-stem', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--cpu-seconds', type=float, default=5)
    p.add_argument('--grid-row-corners', type=int, nargs='+', default=[0, 1, 2, 3],
                   help='Complete only these corner rows, numbered 0..3 in lexicographic letter order.')
    p.add_argument('--no-signed-core', action='store_true',
                   help='Try the smaller grid/row model without the signed core or the prior 2K2 exclusion.')
    p.add_argument('--grid', type=int, nargs=2, action='append',
                   help='Limit the probe to these B/C grid marks; the default covers all eight.')
    a = p.parse_args()
    assert not a.report.exists()
    selected_corners = sorted(set(a.grid_row_corners))
    assert selected_corners and set(selected_corners) <= set(range(4))
    all_marks = [(i, j) for i in (1, 2) for j in (3, 4, 5, 6)]
    marks = [tuple(g) for g in a.grid] if a.grid else all_marks
    assert len(set(marks)) == len(marks) and all(g in all_marks for g in marks)
    resources = limit_research_process(1)
    source = json.loads(a.source_input.read_text(encoding='utf-8'))
    assert {tuple(l // 2 for l in q) for q in source['known_labels']} == {(0, 1), (0, 2), (3, 4), (5, 6)}
    cover_raw = a.boundary.read_bytes()
    boundary_sha = hashlib.sha256(cover_raw).hexdigest()
    source_sha = hashlib.sha256(a.lab_source.read_bytes()).hexdigest()
    assert source['lab_source_sha256'] == source_sha
    report = {'scope': 'One fixed 2K2N attachment with at least one B/C grid; no unmarked-family verdict.',
              'requires_at_least_one_bc_grid': True, 'unmarked_2k2n_case_excluded': False,
              'boundary_file': str(a.boundary), 'boundary_sha256': boundary_sha,
              'boundary_index': a.index, 'sigma': a.sigma, 'lab_source_sha256': source_sha,
              'resources': resources, 'records': [], 'complete': False}
    report.update(selected_grid_marks=marks, completed_grid_corners=selected_corners,
                  uses_signed_core=not a.no_signed_core)
    wrapper = Path(__file__).with_name('root_component_lab_profile_export.py')
    for i, j in marks:
        prefix = a.prefix_stem.with_name(a.prefix_stem.name + f'{i}{j}_rows')
        result_path = prefix.with_suffix('.lab_result.json.gz')
        corners = [y for y, q in enumerate(source['outside_labels']) if {l // 2 for l in q} == {i, j}]
        assert len(corners) == 4
        hubs = [corners[c] for c in selected_corners]
        reused = result_path.exists()
        command = [sys.executable, '-I', '-u', '-X', 'utf8', str(wrapper),
                   str(a.lab_source), str(a.boundary), '--index', str(a.index),
                   '--family', '2K2N', '--sigma', *map(str, a.sigma),
                   '--outside-grid', str(i), str(j), '--extend-rows', *map(str, hubs),
                   '--row-cut-cpu-seconds', str(a.cpu_seconds),
                   '--output', str(prefix.with_suffix('.json'))]
        if not a.no_signed_core:
            command += ['--signed-root-core', '0', '1', '2', '--forbid-q12-grid']
        started = time.monotonic()
        if not reused:
            with prefix.with_suffix('.driver.log').open('wb') as log:
                run = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                     creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            if run.returncode:
                report['records'].append({'grid': [i, j], 'status': 'ERROR', 'returncode': run.returncode,
                                          'prefix': str(prefix), 'log': str(log.name)})
                atomic_json_write(a.report, report, indent=2)
                raise RuntimeError(f'Marked grid {i}{j} failed; inspect its driver log.')
        result = json.loads(gzip.decompress(result_path.read_bytes()))
        learning = json.loads(prefix.with_suffix('.row_cut_learning.json').read_text())
        used_input = json.loads(prefix.with_suffix('.row_cut_input.json').read_text())
        assert used_input == source, 'A previous run on a different fixed block cannot be reused.'
        assert result['boundary_source_sha256'] == boundary_sha and result['boundary_index'] == a.index
        assert result['sigma'] == a.sigma and result['attachments'] == []
        assert learning['outside_grid_constraints']['grids'] == [{'root_pair': [i, j], 'outside_corners': corners}]
        assert learning['extension']['hubs'] == hubs
        if a.no_signed_core:
            assert 'signed_internal_core' not in learning
        else:
            assert learning['signed_internal_core']['forbid_q12_grid']
        front = result['frontier']
        proof = front.get('proof_check', {})
        excluded = front['status'] == 'EXCLUDED_PROFILE_SELECTION_UNSAT' and proof.get('empty_clause_verified') is True
        if excluded:
            assert proof['rup_only'] is True
            assert prefix.with_suffix('.native.cnf.gz').exists() and prefix.with_suffix('.native.input.rup.gz').exists()
        row = {'grid': [i, j], 'prefix': str(prefix), 'status': 'EXCLUDED' if excluded else front['status'],
               'reused_existing_certificate': reused, 'elapsed_seconds': time.monotonic() - started,
               'search_cpu_seconds': learning['rounds'][-1]['cpu_seconds'],
               'conflicts': front.get('conflicts'), 'clauses': front['clauses'],
               'proof_check': proof if excluded else None}
        report['records'].append(row)
        atomic_json_write(a.report, report, indent=2)
        print(json.dumps({k: row[k] for k in ('grid', 'status', 'search_cpu_seconds', 'reused_existing_certificate')}), flush=True)
    report['complete'] = True
    report['all_eight_bc_grid_marks_excluded'] = (set(marks) == set(all_marks)
                                               and all(r['status'] == 'EXCLUDED' for r in report['records']))
    atomic_json_write(a.report, report, indent=2)


if __name__ == '__main__':
    main()
