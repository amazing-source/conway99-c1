"""Run the Gram-free count pipeline on one indexed component catalogue entry.

The input's Gram witnesses and budgets are ignored. Exact certificates
are checked by the standalone integer reader. CP verdicts retain their
distinct status and do not become portable certificates.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_z_distribution import RECTANGLES, row_catalogue
from root_component_z_design_certificate import linear_system, find_certificate, reduce_diagonal_system
from root_component_z_design_verify import verify
from root_component_z_design import solve_design
from root_component_z_joint import build_joint, solve_joint


def run(source, index, output, design_seconds=5, joint_seconds=0, reduce=False):
    output.mkdir(parents=True, exist_ok=True)
    assert not any(output.iterdir()), 'A new or empty output directory is required.'
    resources = limit_research_process(1)
    started = time.process_time()
    raw = source.read_bytes()
    document = json.loads(gzip.decompress(raw) if source.suffix == '.gz' else raw)
    records = document['open'] if 'open' in document else document['survivors']
    record = records[index]
    template = record.get('template', record)
    partition_path, catalogue_path = output / 'partition.json', output / 'catalogue.json'
    atomic_json_write(partition_path, {'template_index': index, 'template': template,
                                      'source_path': str(source), 'source_sha256': hashlib.sha256(raw).hexdigest()})
    catalogue = row_catalogue(template)
    atomic_json_write(catalogue_path, {'catalogue': catalogue, 'source_bundle': str(partition_path)})
    result = {'template_index': index, 'resources': resources, 'source_path': str(source),
              'catalogue_status': catalogue['status'], 'free_dimension': catalogue.get('free_dimension'),
              'uses_Gram_cover': False, 'uses_prism_budget': False, 'global_conway_exclusion': False}
    def checkpoint(status):
        result.update(status=status, cpu_seconds=time.process_time() - started)
        atomic_json_write(output / 'result.json', result)
        print(json.dumps({k: v for k, v in result.items() if k != 'resources'}), flush=True)
    if catalogue['status'] != 'ROW_CATALOGUE_COMPLETE':
        checkpoint(catalogue['status'])
        return result
    result['row_state_count'] = sum(len(item['states']) for item in catalogue['row_types'])
    if any(not item['states'] for item in catalogue['row_types']):
        result['empty_row_types'] = [item['rectangle'] for item in catalogue['row_types'] if not item['states']]
        checkpoint('EMPTY_ROW_CATALOGUE')
        return result
    checkpoint('ROW_CATALOGUE_COMPLETE')
    columns, equations, bounds = linear_system(template, catalogue, degree_histograms=True)
    if reduce:
        equations, bounds = reduce_diagonal_system(columns, equations, bounds, fallback_full=True)
    certificate = find_certificate(columns, equations, bounds)
    certificate.update(template=template, rectangles=[list(q) for q in RECTANGLES],
                       source_catalogue=str(catalogue_path),
                       source_catalogue_sha256=hashlib.sha256(catalogue_path.read_bytes()).hexdigest(),
                       column_order=[{'rectangle': list(RECTANGLES[q]), 'state_index': s} for q, s, z in columns],
                       uses_Gram_cover=False, uses_prism_budget=False, uses_universal_E3_exclusion=True,
                       uses_degree_histogram_bounds=True, global_conway_exclusion=False)
    certificate_path = output / 'certificate.json'
    atomic_json_write(certificate_path, certificate)
    result['separator_status'] = certificate['status']
    if certificate['status'] == 'EXCLUDED_BY_INTEGER_CERTIFICATE':
        checked = verify(certificate_path, catalogue_path)
        atomic_json_write(output / 'verification.json', checked)
        result.update(integer_certificate_checked=True, constant_upper_bound=checked['constant_upper_bound'])
        checkpoint('EXCLUDED_BY_INTEGER_CERTIFICATE')
        return result
    if design_seconds <= 0:
        checkpoint('NO_CERTIFICATE_FOUND')
        return result
    design = solve_design(template, catalogue, seconds=design_seconds, exclude_three_edges=True)
    atomic_json_write(output / 'design.json', {'design': design})
    result['design_status'] = design['status']
    result['design_cpu_seconds'] = design['cpu_seconds']
    if design['status'] == 'INFEASIBLE':
        result['portable_unsat_proof'] = False
        checkpoint('DESIGN_CP_INFEASIBLE')
        return result
    if joint_seconds <= 0:
        checkpoint('AGGREGATE_DESIGN_ONLY' if design['status'] in ('FEASIBLE', 'OPTIMAL') else 'UNKNOWN')
        return result
    model, labels, graph = build_joint(14, catalogue['row_types'], template['nongrid_edges'])
    joint = solve_joint(model, labels, graph, 14, joint_seconds)
    atomic_json_write(output / 'joint.json', joint)
    result.update(joint_status=joint['status'], joint_cpu_seconds=joint['cpu_seconds'],
                  joint_variables=joint['model_variables'], joint_constraints=joint['model_constraints'])
    if joint.get('exact_srg_verified'):
        checkpoint('SRG99_FOUND_AND_CHECKED')
    elif joint['status'] == 'INFEASIBLE':
        result['portable_unsat_proof'] = False
        checkpoint('JOINT_CP_INFEASIBLE')
    else:
        checkpoint('UNKNOWN')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--output-directory', type=Path, required=True)
    p.add_argument('--design-seconds', type=float, default=5)
    p.add_argument('--joint-seconds', type=float, default=0)
    p.add_argument('--reduce-certificate', action='store_true')
    a = p.parse_args()
    run(a.source, a.index, a.output_directory, a.design_seconds, a.joint_seconds, a.reduce_certificate)


if __name__ == '__main__':
    main()
