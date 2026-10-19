"""Package the seven LAB 2K2 residuals, including exact transports.

This assembles our continuation certificates, not the LAB's exhaustive
census. It refuses to report complete residual coverage if any source
attachment lacks a checked refutation. No SAT search is repeated.
"""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write
from root_component_profile_row_cuts import RowCutOracle
from root_component_known_block_isomorphism import check as check_mapping
from root_component_row_cut_certificate import sha256
from root_component_2k2_profile_canonical import check_cnf_position

REPO = Path(__file__).resolve().parents[2]


def relative(path):
    return Path(path).resolve().relative_to(REPO).as_posix()


def source_certificate(directory, index, case):
    overrides_path=directory/'preferred_runs.json'
    overrides=json.loads(overrides_path.read_text(encoding='utf-8')) if overrides_path.exists() else {}
    prefix = directory / overrides.get(str(index), 'case%03d.json' % index)
    assert prefix.resolve().parent == directory.resolve()
    input_path = prefix.with_suffix('.row_cut_input.json')
    learning_path = prefix.with_suffix('.row_cut_learning.json')
    cnf_path = prefix.with_suffix('.row_cut_cnf.json.gz')
    recovered = directory / ('case%03d_recovered_certificate.json' % index)
    original = prefix.with_suffix('.lab_result.json.gz')
    if recovered.exists():
        result = json.loads(recovered.read_text(encoding='utf-8'))
        checked = result['proof_check']; result_path = recovered
    elif original.exists():
        result = json.loads(gzip.decompress(original.read_bytes()))
        assert result['attachments'] == case['attachment'] and result['sigma'] == case['sigma']
        assert result['boundary_hex'] == case['boundary_hex']
        if result['frontier']['status'] != 'EXCLUDED_PROFILE_SELECTION_UNSAT':
            return None
        checked = result['frontier']['proof_check']; result_path = original
    else:
        return None
    assert checked['empty_clause_verified'] is True and checked['rup_only'] is True
    inp = json.loads(input_path.read_text(encoding='utf-8'))
    for name in ('rows', 'known_labels', 'outside_labels'):
        assert inp[name] == case[name]
    learning = json.loads(learning_path.read_text(encoding='utf-8'))
    assert learning['terminal_status'] == 'UNSAT_WITH_NECESSARY_ROW_CUTS'
    assert learning['rounds'][-1]['answer'] is False
    clauses = json.loads(gzip.decompress(cnf_path.read_bytes()))
    oracle = RowCutOracle(inp['rows'], inp['known_labels'], inp['outside_labels'], inp['domains'])
    literals = inp['profile_literals']; suffix = []; kinds = Counter()
    for round_ in learning['rounds']:
        for cut in round_.get('violated_cuts', []):
            assert oracle.check_cut(cut)
            guards = cut.get('guards', [(cut.get('outside_index'), cut.get('profile_index'))])
            suffix.append([-literals[y][p] for y, p in guards] +
                          [literals[y][p] for y, p in cut['support_options']])
            kinds[cut.get('kind', 'row_quota')] += 1
    assert len(suffix) == learning['clauses_added']
    assert not suffix or clauses[-len(suffix):] == suffix
    canonical=check_cnf_position(inp,learning,clauses,len(suffix))
    # Bind the verified DIMACS exactly to the mathematical clauses above.
    nv = max((abs(v) for c in clauses for v in c), default=0)
    dimacs = 'p cnf %d %d\n' % (nv, len(clauses))
    dimacs += ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)
    native_cnf = next(name for name in checked['artifacts'] if name.endswith('.native.cnf.gz'))
    assert hashlib.sha256(dimacs.encode('ascii')).hexdigest() == checked['artifacts'][native_cnf]['uncompressed_sha256']
    required = [input_path, learning_path, cnf_path, result_path,
                Path(checked['log'])]
    parts_path=prefix.with_suffix('.native_parts.json')
    packed=json.loads(parts_path.read_text(encoding='utf-8'))['artifacts'] if parts_path.exists() else {}
    for name,meta in checked['artifacts'].items():
        if name in packed:
            part_meta=packed[name]
            assert meta['compressed_bytes']==part_meta['compressed_bytes']
            if (directory/name).exists():assert sha256(directory/name)==part_meta['compressed_sha256']
            meta.update(part_meta)
            for part in part_meta['parts']:
                path=directory/part['name']
                assert path.stat().st_size==part['bytes'] and sha256(path)==part['sha256']
                required.append(path)
        else:required.append(directory/name)
    if packed:required.append(parts_path)
    assert all(p.exists() for p in required)
    cert = {
        'scope': 'One attachment, all its profile choices; family completeness is supplied separately by LAB.',
        'core_index': case['core_index'], 'boundary_hex': case['boundary_hex'],
        'attachment': case['attachment'], 'sigma': case['sigma'],
        'status': 'EXCLUDED_ATTACHMENT_BY_CHECKED_CONTINUATION',
        'empty_clause_verified': True, 'proof_check': checked,
        'necessary_clauses_checked': len(suffix), 'clause_kinds': dict(kinds),
        'sat_selections_refuted': sum(r['answer'] is True for r in learning['rounds']),
        'solve_learning_cpu_seconds': learning['rounds'][-1]['cpu_seconds'],
        'exact_augmented_cnf_matches_checked_dimacs': True,
        'canonical_profile_reduction': canonical,
        'files': {relative(p): sha256(p) for p in required},
    }
    out = prefix.with_suffix('.certificate.json'); atomic_json_write(out, cert)
    return out


def assemble(directory, allow_partial=False):
    resources = limit_research_process(1)
    materialized = json.loads((directory/'cases.json').read_text(encoding='utf-8'))
    cases = materialized['cases']
    assert materialized['catalogue_sha256'] == sha256(directory/'catalogue.json')
    groups = json.loads((directory/'isomorphisms.json').read_text(encoding='utf-8'))['classes']
    first = directory.parent/'shared_2k2_core006_b547_attachment_summary.json'
    first_data = json.loads(first.read_text(encoding='utf-8'))
    assert first_data['proof_check']['empty_clause_verified'] is True
    first_input = json.loads((directory.parent/'shared_2k2_core006_b547_continuation.row_cut_input.json').read_text(encoding='utf-8'))
    for name in ('rows','known_labels','outside_labels'):
        assert first_input[name] == cases[0][name]
    assert first_data['attachments'] == cases[0]['attachment'] and first_data['sigma'] == cases[0]['sigma']
    assert first_data['boundary_hex'] == cases[0]['boundary_hex']
    sources = {0: first}; entries = []; missing = []
    for group in groups:
        rep = group['representative']
        if rep not in sources:
            sources[rep] = source_certificate(directory, rep, cases[rep])
        if sources[rep] is None:
            missing.extend(m['case_index'] for m in group['members']); continue
        for member in group['members']:
            index = member['case_index']; case = cases[index]
            entry = {name: case[name] for name in ('core_index','boundary_hex','attachment','sigma')}
            entry.update(status='EXCLUDED_CHECKED_CONTINUATION', empty_clause_verified=True,
                         path=relative(sources[rep]), sha256=sha256(sources[rep]), case_index=index)
            mapping = member['mapping_from_representative']
            if mapping is not None:
                assert check_mapping(cases[rep], case, mapping)
                entry.update(status='EXCLUDED_EXACT_ROOT_LETTER_TRANSPORT', mapping=mapping,
                             source_case_index=rep,
                             source_attachment=cases[rep]['attachment'], source_sigma=cases[rep]['sigma'])
            entries.append(entry)
    assert sorted([e['case_index'] for e in entries]+missing) == list(range(len(cases)))
    assert len(cases) == 7
    assert allow_partial or not missing, ('Uncertified residuals', missing)
    result = {'scope': 'Seven residual attachments only; use LAB two-stage manifest for family completeness.',
              'resources': resources, 'certificates': sorted(entries,key=lambda e:e['case_index']),
              'missing_case_indices': sorted(missing), 'all_seven_residuals_excluded': not missing,
              'global_Conway_exclusion': False}
    out = directory/'certificates_for_lab.json'; atomic_json_write(out, result)
    print(json.dumps({'certified': len(entries), 'missing': missing, 'output': str(out)}), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path); p.add_argument('--allow-partial', action='store_true')
    a = p.parse_args(); assemble(a.directory, a.allow_partial)
