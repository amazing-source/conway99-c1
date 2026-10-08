"""Sparse LP discovery, exact certificates for the order-ten raw families."""
from fractions import Fraction as F
import gzip
import json
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from sympy import Matrix, Rational

from higher_census_minima import ROOT


def load_report():
    compressed = ROOT/'data/codex_targeted_order10_census.json.gz'
    if compressed.exists():
        with gzip.open(compressed, 'rt', encoding='utf-8') as stream:
            return json.load(stream)
    return json.loads((ROOT/'data/codex_targeted_order10_census.json').read_text())


def constraints(report):
    rows = [(f'C10_{r["code"]}', {k: F(v) for k, v in r['affine_sparse'].items()})
            for r in report['counts']]
    packet = json.loads((ROOT/'data/codex_census_validation_99.json').read_text())
    stage9 = packet['stages'][-1]
    for row in stage9['counts']:
        rows.append((f'C9_{row["code"]}', {k: F(v) for k, v in
                     zip(['1']+stage9['parameters'], row['affine']) if F(v)}))
    rows += [(name, {k: F(v) for k, v in form.items()}) for name, form in report['extension_slacks'].items()]
    return rows


class SparseCertificates:
    def __init__(self, parameters, rows):
        self.parameters, self.rows = parameters, rows
        index = {name: i for i, name in enumerate(parameters)}
        ii, jj, vv = [], [], []
        self.constants = np.array([float(row.get('1', 0)) for _, row in rows])
        for i, (_, row) in enumerate(rows):
            for key, value in row.items():
                if key != '1' and value:
                    ii.append(i); jj.append(index[key]); vv.append(float(value))
        self.matrix = coo_matrix((vv, (ii, jj)), shape=(len(rows), len(parameters))).tocsr()

    def minimum(self, objective):
        cost = np.array([float(objective.get(p, 0)) for p in self.parameters])
        result = linprog(cost, A_ub=-self.matrix, b_ub=self.constants,
                         bounds=[(None, None)]*len(cost), method='highs')
        assert result.success, result.message
        support = [i for i, weight in enumerate(-result.ineqlin.marginals) if weight > 1e-8]
        matrix = Matrix([[Rational(self.rows[i][1].get(name, 0)) for i in support] for name in self.parameters])
        target = Matrix([Rational(objective.get(name, 0)) for name in self.parameters])
        weights, free = matrix.gauss_jordan_solve(target)
        if free:
            weights = weights.subs({p: 0 for p in free})
        weights = list(map(F, weights))
        assert all(weight >= 0 for weight in weights)
        identity = {}
        for i, weight in zip(support, weights):
            for key, value in self.rows[i][1].items():
                identity[key] = identity.get(key, F(0))+weight*value
        assert all(identity.get(name, 0) == objective.get(name, 0) for name in self.parameters)
        bound = objective.get('1', F(0))-identity.get('1', 0)
        point = dict(zip(self.parameters, (F(float(x)).limit_denominator(10**6) for x in result.x)))
        point['1'] = F(1)
        feasible = all(sum(value*point[name] for name, value in row.items()) >= 0 for _, row in self.rows)
        attained = feasible and sum(value*point[name] for name, value in objective.items()) == bound
        return {'lower_bound': str(bound), 'certificate': [(self.rows[i][0], str(weight))
                 for i, weight in zip(support, weights) if weight],
                'rational_point_attaining_bound': {k: str(v) for k, v in point.items()} if attained else None,
                'objective': {k: str(v) for k, v in objective.items()},
                'scope': 'Exact nonnegative rational certificate; a claimed attaining point is checked against every row.'}


def main():
    report = load_report()
    parameters = report['parameters']
    rows = constraints(report)
    if '--verify-only' in sys.argv:
        saved = json.loads((ROOT/'data/codex_targeted_order10_minima.json').read_text())
        by_name = dict(rows)
        by_name['P<=0'] = {'P': F(-1)}
        checked = 0
        for case, results in saved['cases'].items():
            for label, result in results.items():
                identity = {}
                for name, weight in result['certificate']:
                    weight = F(weight)
                    assert weight >= 0 and (case == 'P=0' or name != 'P<=0')
                    for key, value in by_name[name].items():
                        identity[key] = identity.get(key, F(0))+weight*value
                expected = {k: F(v) for k, v in result['objective'].items()}
                expected['1'] = expected.get('1', F(0))-F(result['lower_bound'])
                assert all(identity.get(k, 0) == expected.get(k, 0) for k in ['1']+parameters)
                point = result['rational_point_attaining_bound']
                if point is not None:
                    point = {k: F(v) for k, v in point.items()}
                    assert all(sum(value*point[k] for k, value in row.items()) >= 0 for _, row in rows)
                    assert case != 'P=0' or point['P'] == 0
                    assert sum(F(v)*point[k] for k, v in result['objective'].items()) == F(result['lower_bound'])
                checked += 1
                print(case, label, 'verified:', result['lower_bound'], float(F(result['lower_bound'])), flush=True)
        print('Certificates verified from compressed source, without solving:', checked, flush=True)
        return
    objectives = {q: {k: F(v) for k, v in zip(['1']+parameters, values) if F(v)}
                  for q, values in report['raw_objectives'].items()}
    joint = dict(objectives['8'])
    for key, value in objectives['6'].items():
        joint[key] = joint.get(key, F(0))+F(651, 34)*value
    objectives['8+(651/34)6'] = joint
    output = {'source': 'codex_targeted_order10_census.json.gz', 'cases': {},
              'scope': 'Raw representatives only. No bound on distinct projected vectors.'}
    for fixed in (False, True):
        solver = SparseCertificates(parameters, rows+([('P<=0', {'P': F(-1)})] if fixed else []))
        case = 'P=0' if fixed else 'unconditional'
        output['cases'][case] = {}
        for label, objective in objectives.items():
            result = solver.minimum(objective)
            output['cases'][case][label] = result
            print(case, label, '>=', result['lower_bound'], 'exact witness:',
                  result['rational_point_attaining_bound'] is not None, flush=True)
            (ROOT/'data/codex_targeted_order10_minima.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
