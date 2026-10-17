"""Exact geometric and proved-shell consequences of the order-nine census.

No distinctness assumption is made about the new order-eight/nine families.
Shell bounds use only collision-audited families of notes 179 and 181.
"""
from fractions import Fraction as F
from math import floor, lcm
import json

from higher_census_minima import ROOT, certify
from higher_vertex_census import ir_orders


def read(n):
    data = json.loads((ROOT/f'data/codex_order{n}_census.json').read_text())
    rows = [(str(r['code']), list(map(F, r['affine']))) for r in data['counts']]
    return data, rows


def save(name, data):
    (ROOT/f'data/{name}.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')


def proof(rows, objective):
    result = certify(rows, objective)
    result['objective'] = list(map(str, objective))
    return result


def main():
    for n in (8, 9):
        data, rows = read(n)
        width = len(data['parameters'])+1
        P = [F(0), F(1)]+[F(0)]*(width-2)
        result = proof(rows, [-x for x in P])
        result['integer_upper_bound'] = floor(-F(result['lower_bound']))
        denominator = lcm(*(F(w).denominator for _, w in result['certificate']))
        result['integer_identity'] = {
            'P_multiplier': denominator,
            'graph_count_weights': [(name, int(F(w)*denominator)) for name, w in result['certificate']],
            'right_hand_side': str(-F(result['lower_bound'])*denominator)}
        save(f'codex_order{n}_prism_cap', result)
        print('Order', n, 'P <=', -F(result['lower_bound']), flush=True)
    H = [F(133056), F(-6), F(-1, 4)]+[F(0)]*(width-3)
    grid = tuple(sum(1 << j for j in range(9) if i != j and
                     (i//3 == j//3 or i % 3 == j % 3)) for i in range(9))
    grid_code = ir_orders(grid)[0]
    rho = dict(rows)[str(grid_code)]
    caps = {'grid_code': grid_code, 'parameters': data['parameters']}
    for name, objective in [('rho', rho), ('H', H),
                            ('P+2H/3', [x+F(2, 3)*y for x, y in zip(P, H)])]:
        result = proof(rows, [-x for x in objective])
        caps[name] = result
        print(name, '<=', -F(result['lower_bound']), flush=True)
    save('codex_order9_geometry_caps', caps)
    shells = {}
    for name, c, p, h, r in [('b3', 66528, -18, 0, -72),
                              ('b4_six', 3826746, -30, 0, -4572),
                              ('b4_seven', 5939010, -1134, -84, -13572),
                              ('b5', 35123088, -168, 0, -7212)]:
        objective = [p*a+h*b+r*d for a, b, d in zip(P, H, rho)]
        objective[0] += c
        result = proof(rows, objective)
        shells[name] = result
        print(name, '>=', result['lower_bound'], flush=True)
    save('codex_order9_uniform_shell_bounds', shells)
    assert F(caps['rho']['lower_bound']) == -126
    assert {name: F(result['lower_bound']) for name, result in shells.items()} == {
        'b3': 43848, 'b4_six': 3227994, 'b4_seven': 3371634, 'b5': 34087368}


if __name__ == '__main__':
    main()
