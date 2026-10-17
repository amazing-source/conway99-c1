"""Compare all 3875 targeted formulas with LAB's independent full census."""
from fractions import Fraction as F
import gzip
import json
import sys

from higher_census_minima import ROOT
from seven_vertex_census import canon
from higher_vertex_census import ir_orders

sys.path.insert(0, str(ROOT/'code/lab_theta_lp_2026-10-08'))
import census2 as lab


def main():
    with gzip.open(ROOT/'data/codex_lab_full_order10.json.gz', 'rt', encoding='utf-8') as stream:
        source = json.load(stream)
    with gzip.open(ROOT/'data/codex_targeted_order10_census.json.gz', 'rt', encoding='utf-8') as stream:
        targeted = json.load(stream)
    conversion = {'0': '1'}
    for i, (n, _, adjacency) in enumerate(source['params'], 1):
        if n == 6:
            name = 'P'
        elif n == 7:
            name = 'H'
        elif n == 8:
            name = f'C8_{canon(tuple(adjacency))[0]}'
        else:
            name = f'C{n}_{ir_orders(tuple(adjacency))[0]}'
        conversion[str(i)] = name
    forms = {key: form for key, _, _, form in source['types']['10']}
    for row in targeted['counts']:
        key, _ = lab.canon(10, row['adjacency_bits'])
        actual = {conversion[k]: F(value)/row['automorphisms']
                  for k, value in forms[key].items() if F(value)}
        expected = {k: F(value) for k, value in row['affine_sparse'].items() if F(value)}
        assert actual == expected, row['code']
    assert len(source['types']['10']) == 42430 and len(source['params']) == 549
    print('Exact agreement:', len(targeted['counts']), 'targeted order-ten formulas;',
          'full census:', len(source['types']['10']), 'types and', len(source['params']), 'parameters', flush=True)


if __name__ == '__main__':
    main()
