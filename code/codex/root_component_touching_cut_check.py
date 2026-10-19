"""Check the scope, relabelling invariance and E3 gate of the new cut.

This checks the solver integration, not the LAB's core enumeration.
"""

import argparse
import copy
import gzip
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process
from root_component_grid_closure import touching_grid_closure_violations
from root_component_opposite_core import opposite_pairs
from root_component_energy_implications import add_energy_implications


def check():
    from ortools.sat.python import cp_model
    base = Path('code/lab_exploration_2026-10-16')
    data = json.loads(gzip.decompress(
        (base/'c3_root_cover/c3_open_templates_k3_12.json.gz').read_bytes()))['open']
    relations = json.loads((base/'gz5602_2026-10-19/two_term_relations_open.json').read_text())
    registry = base/'c3_hard_core_2026-10-18/c3_open_now.tsv'
    ids = [int(line.split()[1]) for line in registry.read_text().splitlines()
           if line.startswith('gz')]
    hits = {}
    for i in ids:
        pairs = [(tuple(map(int, a)), tuple(map(int, b)))
                 for a, b, kind in relations.get(str(i), {}).get('opp', [])
                 if kind == 'disjoint']
        found = touching_grid_closure_violations(data[i]['template'], pairs)
        if found:
            hits[str(i)] = found
    assert len(hits) == 24
    sample = data[3922]['template']
    exact = touching_grid_closure_violations(sample)
    assert exact == hits['3922']
    rects, pairs = opposite_pairs(sample)
    pairs = [(rects[a], rects[b]) for a, b in pairs]
    for perm in itertools.permutations(range(7)):
        def relabel(q):
            return tuple(sorted(perm[i] for i in q))
        template = {'nongrid_edges': [relabel(q) for q in sample['nongrid_edges']]}
        found = touching_grid_closure_violations(
            template, [(relabel(a), relabel(b)) for a, b in pairs])
        assert len(found) == len(exact)
        assert found[0]['shared_root'] == perm[exact[0]['shared_root']]
    changed = copy.deepcopy(sample)
    changed['nongrid_edges'].append(list(exact[0]['required_grids'][0]))
    assert not touching_grid_closure_violations(changed, pairs)
    assert not touching_grid_closure_violations(data[5602]['template'])
    gating = []
    for e3 in (False, True):
        model = cp_model.CpModel()
        counts = [[None]*21 for _ in range(21)]
        for i in range(21):
            for j in range(i, 21):
                counts[i][j] = counts[j][i] = model.new_int_var(0, 32, f'c{i}_{j}')
        result = add_energy_implications(model, counts, rects, sample, e3=e3)
        assert not model.validate(), model.validate()
        empties = sum(c.has_bool_or() and not c.bool_or.literals
                      for c in model.Proto().constraints)
        assert empties == int(e3), (e3, empties)
        assert bool(result.get('touching_grid_closure_violations')) == e3
        gating.append({'E3': e3, 'empty_clause_count': empties})
    return {
        'scope': __doc__, 'open_registry_input': str(registry),
        'open_inputs': len(ids), 'matched_template_ids': sorted(map(int, hits)),
        'matching_witnesses': hits, 'root_relabellings_checked': 5040,
        'one_missing_Y_grid_disables_cut': True,
        'old_four_X_grids_outside_scope': True, 'E3_gating': gating,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    limit_research_process(1)
    out = check()
    args.output.write_text(json.dumps(out, indent=2)+'\n', encoding='utf8')
    print(json.dumps({k: v for k, v in out.items() if k != 'matching_witnesses'}))
