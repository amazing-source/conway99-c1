"""Controls for the histogram encoder, explicitly not Conway graph examples."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_resources import atomic_json_write, limit_research_process
from root_component_short_column_histograms import (
    add_histogram_tables, histogram_facets, histogram_rows, linear_bounds, witness_histograms,
)


def fixture(record):
    """Realize counts as bounded rectangle-row entries, without claiming C1."""
    e, p2, m3, m2 = record
    half = 28-7*e
    p1, m1 = half-3*p2-m2-3*m3, half-p2-3*m2-6*m3
    rectangles = list(combinations(range(7), 2))
    target = rectangles[0]
    values = [[0]*4 for _ in rectangles]
    own = { (0,4): [2,2,2,2], (1,2): [2,2,1,1],
            (2,0): [1,1,1,1], (2,1): [2,1,1,0] }[e, p2]
    values[0] = own
    shared = [(qi, w) for qi, q in enumerate(rectangles) if qi and set(q) & set(target) for w in range(4)]
    disjoint = [(qi, w) for qi, q in enumerate(rectangles) if not set(q) & set(target) for w in range(4)]
    neg = [-2]*m2+[-1]*m1
    pos = [-3]*m3+[1]*(p1-own.count(1))
    assert len(neg) <= len(shared) and len(pos) <= len(disjoint)
    for (qi, w), value in zip(shared, neg):
        values[qi][w] = value
    for (qi, w), value in zip(disjoint, pos):
        values[qi][w] = value
    rows = []
    for qi, q in enumerate(rectangles):
        base = 3*int(q == target)+1-len(set(q) & set(target))
        states = []
        for h in values[qi]:
            state = [0]*len(rectangles)
            state[0] = base-h
            assert 0 <= state[0] <= (2 if set(q) & set(target) else 4)
            states.append(state)
        rows.append({'rectangle': list(q), 'states': states})
    return rectangles, rows


def run():
    allowed = histogram_rows()
    forbidden = [(2,0,0,2), (1,2,1,1), (0,4,2,1)]
    records = []
    for record, expected in [(r, True) for r in allowed] + [(r, False) for r in forbidden]:
        rectangles, rows = fixture(record)
        model = cp_model.CpModel()
        terms = []
        for qi, item in enumerate(rows):
            for si, z in enumerate(item['states']):
                multiplicity = model.new_int_var(0, 1, f'x_{qi}_{si}')
                model.add(multiplicity == 1)
                terms.append((qi, z, multiplicity))
        add_histogram_tables(model, rectangles, {rectangles[0]}, terms)
        assert not model.validate(), model.validate()
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = 2
        status = solver.solve(model)
        assert status == (cp_model.OPTIMAL if expected else cp_model.INFEASIBLE)
        actual = witness_histograms(rows, {rectangles[0]})[0]
        assert actual['histogram'] == list(record) and actual['admissible'] == expected
        assert actual['sum'] == 0 and actual['squared_norm'] == 56-14*record[0]
        columns = [(qi, si, z) for qi, item in enumerate(rows) for si, z in enumerate(item['states'])]
        for bound in linear_bounds(columns, rectangles, {rectangles[0]}):
            a, b, c = bound['normal']
            assert sum(bound['coefficients']) == 2*(a*record[0]+b*record[2]+c*record[3])
            if expected:
                assert sum(bound['coefficients']) <= bound['upper']
        records.append({'histogram': list(record), 'expected_admissible': expected, 'status': solver.status_name(status)})
    facets = histogram_facets()
    assert facets == ((1,1,0,2), (2,2,1,8), (5,5,1,11), (11,12,2,24))
    return {'status': 'HISTOGRAM_ENCODER_CONTROLS_PASSED', 'allowed_histograms': len(allowed),
            'rejected_norm_correct_histograms': len(forbidden), 'facets': facets, 'records': records,
            'scope': 'Synthetic bounded count rows test the encoder; none is claimed to be a Conway graph.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    result = run()
    result['resources'] = resources
    atomic_json_write(a.output, result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','resources')}))
