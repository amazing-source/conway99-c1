"""Record the rank-free even-shadow reductions of note256.

The complete catalogue of core attachments is reused. New certificates
are a double-C4 counting contradiction and one integral Rayleigh vector.
"""
from collections import Counter
import json
import networkx as nx
import numpy as np
from norm16_schur_data import ROOT, source_data


def main():
    cores, cases, _ = source_data()
    records = []
    for ci, case in enumerate(cases):
        for oi, orbit in enumerate(case['orbits']):
            shadows = [set(r[:2]) | {8+q for q in r[2:]} for r in orbit['representative']]
            c = [[0 if i == j else len(s & t) for j, t in enumerate(shadows)] for i, s in enumerate(shadows)]
            if any(x % 2 for row in c for x in row):
                continue
            assert all(sum(row) == 4 for row in c)
            graph = nx.from_numpy_array(np.array(c))
            components = sorted(len(s) for s in nx.connected_components(graph))
            assert all(d == 2 for _, d in graph.degree())
            record = {'case': ci, 'orbit': oi, 'C': c, 'components_of_C_divided_by_2': components,
                      'D_independent_forced': True}
            if 3 in components:
                record.update({'status': 'EXCLUDED', 'reason': 'Three D require12 incidences in11 independent Z columns.'})
            elif components == [4, 4]:
                record.update({'status': 'EXCLUDED', 'reason': 'Two C4 require at least10 within-component pairs; capacity8.'})
            else:
                assert components == [8]
                record.update({'status': 'OPEN', 'allowed_forest_ids': [3, 6, 7]})
            records.append(record)
    certificate_record = next(r for r in records if (r['case'], r['orbit']) == (0, 52))
    a = [[0]*24 for _ in range(24)]
    for i in range(8):
        for j in range(8):
            a[i][8+j] = a[8+j][i] = cores[0]['representatives'][0][i][j]
    for d, r in enumerate(cases[0]['orbits'][52]['representative']):
        for p in r[:2]+[8+q for q in r[2:]]:
            a[p][16+d] = a[16+d][p] = 1
    v = [106, 101, 33, -50, -106, -101, -33, 50,
         50, 106, 33, -106, -33, 101, -50, -101,
         141, 94, 94, 0, -94, -141, -94, 0]
    norm = sum(x*x for x in v)
    value = 3*norm-sum(v[i]*a[i][j]*v[j] for i in range(24) for j in range(24))
    assert sum(v) == 0 and value == -470
    certificate_record.update({'status': 'EXCLUDED', 'reason': 'Integral Rayleigh certificate on core+D, after D independence is forced.',
                               'adjacency_core_D': a, 'certificate_vector': v,
                               'certificate_sum': sum(v), 'certificate_3norm_minus_A': value})
    data = {'scope': __doc__, 'records': records,
            'counts': dict(Counter(r['status'] for r in records)),
            'excluded_attachments': [[r['case'], r['orbit']] for r in records if r['status'] == 'EXCLUDED'],
            'remaining_even_attachments': [[r['case'], r['orbit']] for r in records if r['status'] == 'OPEN']}
    (ROOT/'data/codex_norm16_even_shadows.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: v for k, v in data.items() if k not in ('scope', 'records')}))


if __name__ == '__main__':
    main()
