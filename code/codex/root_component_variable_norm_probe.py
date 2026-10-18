"""Refine a Gram-free aggregate design by universally valid variable-norm cuts.

The witness suggests integer combinations of H columns; ONLY the integer
coefficients are retained. Their norms remain free in every subsequent
solve. A failure of the witness alone is never a template exclusion.
"""

import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_z_design import solve_design
from root_component_variable_norm_cuts import separate


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--catalogue', type=Path, required=True)
    p.add_argument('--seconds', type=float, default=5)
    p.add_argument('--rounds', type=int, default=10)
    p.add_argument('--support', type=int, choices=(1,2,3), default=3)
    p.add_argument('--cuts-per-round', type=int, default=8)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert a.rounds >= 1 and a.cuts_per_round >= 1 and not a.output.exists()
    resources = limit_research_process(1)
    template = json.loads(a.bundle.read_text(encoding='utf-8-sig'))['template']
    catalogue = json.loads(a.catalogue.read_text(encoding='utf-8-sig'))['catalogue']
    assert catalogue['status'] == 'ROW_CATALOGUE_COMPLETE'
    directions = []
    result = {'scope': __doc__, 'source_bundle': str(a.bundle), 'source_catalogue': str(a.catalogue),
              'rounds': [], 'resources': resources, 'uses_Gram_cover': False,
              'uses_prism_budget': False, 'global_conway_exclusion': False, 'portable_unsat_proof': False}
    start = time.process_time()
    for round_index in range(a.rounds):
        design = solve_design(template, catalogue, a.seconds, True, True, eigen_directions=directions)
        record = {'round': round_index, 'cuts_before': len(directions), 'design': design}
        result['rounds'].append(record)
        if design['status'] == 'INFEASIBLE':
            result['status'] = 'TEMPLATE_CP_INFEASIBLE'
        elif design['status'] not in ('OPTIMAL','FEASIBLE'):
            result['status'] = 'UNKNOWN'
        else:
            separation = separate(catalogue, design['row_multisets'], a.support)
            record['separation'] = separation
            if not separation['violating_directions']:
                result['status'] = 'NO_VIOLATION_IN_SEARCHED_DIRECTIONS'
            else:
                for violation in separation['violating_directions'][:a.cuts_per_round]:
                    d = violation['direction']
                    assert d not in directions, 'Existing cut violated: encoder or witness error.'
                    directions.append(d)
                result['status'] = 'REFINING'
        result.update(directions=directions, cpu_seconds=time.process_time()-start)
        atomic_json_write(a.output, result)
        print(json.dumps({'round': round_index, 'design': design['status'], 'status': result['status'],
                          'cuts': len(directions), 'cpu_seconds': result['cpu_seconds'],
                          'violating_directions': len(record.get('separation',{}).get('violating_directions',[]))}), flush=True)
        if result['status'] != 'REFINING':
            break
    if result['status'] == 'REFINING':
        result['status'] = 'ROUND_LIMIT_NO_EXCLUSION'
        atomic_json_write(a.output, result)


if __name__ == '__main__':
    main()
