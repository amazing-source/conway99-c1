"""Certify the consequence for tau of the targeted order-eleven closure."""
from fractions import Fraction as F
import gzip
import json
import sys

from higher_census_minima import ROOT
from targeted_order10_minima import SparseCertificates


def main():
    with gzip.open(ROOT/'data/codex_lab_full_order10.json.gz', 'rt', encoding='utf-8') as stream:
        old = json.load(stream)
    with gzip.open(ROOT/'data/codex_prism_house_order11.json.gz', 'rt', encoding='utf-8') as stream:
        new = json.load(stream)
    def converted(form):
        return {('1' if key == '0' else f'N{key}' if key.isdigit() else key): F(v)
                for key, v in form.items() if F(v)}
    rows = [(f'{n}:{key}', converted(form)) for n in range(6, 11)
            for key, _, _, form in old['types'][str(n)]]
    rows += [(f'11:{r["key"]}', converted(r['embedding_affine'])) for r in new['counts']]
    rows += [(name, converted(form)) for name, form in new['extension_slacks'].items()]
    rows = [(name, form) for name, form in rows if form]
    params = [f'N{i}' for i in range(1, len(old['params'])+1)]+new['new_parameters']
    objective = {k: -v for k, v in converted(new['prism_house_count']).items()}
    path = ROOT/'data/codex_prism_house_order11_bound.json'
    if '--verify-only' in sys.argv:
        report = json.loads(path.read_text())
        result = report['certificate']
    else:
        result = SparseCertificates(params, rows, normalize=True, method='highs-ipm', progress=True).minimum(objective)
        upper = -F(result['lower_bound'])
        report = {'house_count_upper_bound': str(upper), 'tau_upper_bound': str(upper/12),
                  'certificate': result,
                  'scope': 'Upper bound from 12*tau <= N(prism+house); compare with the already proved tau <= 1890.'}
    total = {}
    by_name = dict(rows)
    for name, weight in result['certificate']:
        weight = F(weight)
        assert weight >= 0
        for k, v in by_name[name].items():
            total[k] = total.get(k, F(0))+weight*v
    expected = dict(objective)
    expected['1'] = expected.get('1', F(0))-F(result['lower_bound'])
    assert all(total.get(k, 0) == expected.get(k, 0) for k in ['1']+params)
    assert F(report['house_count_upper_bound']) == -F(result['lower_bound'])
    assert F(report['tau_upper_bound']) == F(report['house_count_upper_bound'])/12
    point = result['rational_point_attaining_bound']
    if point is not None:
        point = {k: F(v) for k, v in point.items()}
        assert point['1'] == 1
        assert all(sum(v*point[k] for k, v in form.items()) >= 0 for _, form in rows)
        assert sum(v*point[k] for k, v in objective.items()) == F(result['lower_bound'])
    if '--verify-only' not in sys.argv:
        path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Exact: N(prism+house) <=', report['house_count_upper_bound'], '; tau <=', report['tau_upper_bound'],
          float(F(report['tau_upper_bound'])), '; exact attaining point:',
          result['rational_point_attaining_bound'] is not None, flush=True)


if __name__ == '__main__':
    main()
