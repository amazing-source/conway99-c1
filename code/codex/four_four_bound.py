"""Combine the completed (4,4) pair-loss audit with exact order-nine counts."""
from fractions import Fraction as F
import json

from higher_census_minima import ROOT, certify


def main():
    nine = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    eight = json.loads((ROOT/'data/codex_order8_census.json').read_text())
    width = len(nine['parameters'])+1
    graph_rows = [(str(r['code']), list(map(F, r['affine']))) for r in nine['counts']]
    physical = {'P': [F(0), F(1)]+[F(0)]*(width-2),
                'H': [F(133056), F(-6), F(-1, 4)]+[F(0)]*(width-3),
                'rho': dict(graph_rows)['13262907120']}
    for row in eight['counts']:
        if min(row['degrees']) >= 3:
            physical[f'C8_{row["code"]}'] = list(map(F, row['affine']))+[F(0)]*(width-len(row['affine']))
    def form(c=0, tau=0, omega=0, B=0, **terms):
        result = [F(c)]+[F(0)]*(width-1)
        for name, coefficient in terms.items():
            result = [x+coefficient*y for x, y in zip(result, physical[name])]
        return result+list(map(F, [tau, omega, B]))
    def minus(row):
        return [-x for x in row]
    rows = [(name, row+[F(0)]*3) for name, row in graph_rows]
    rows += [('tau>=0', form(tau=1)), ('Omega>=0', form(omega=1)),
             ('2tau<=5P', form(P=5, tau=-2)), ('tau<=2P+3rho', form(P=2, rho=3, tau=-1)),
             ('Omega<=H', form(H=1, omega=-1)), ('tau>=6rho-231', form(c=231, rho=-6, tau=1))]
    raw = json.loads((ROOT/'data/codex_order9_raw_family_minima.json').read_text())
    N4 = list(map(F, raw['Q4_edges9_3_cross0']['objective']))
    rows.append(('8tau<=N4', N4+[F(-8), F(0), F(0)]))
    six = form(3826746, P=90, rho=-4572, tau=-48, B=-1)
    seven = form(5939010, P=66, H=14, rho=-13572, tau=-480, omega=-98, B=-1)
    full = form(8105328, P=-252, H=-8, rho=-13572, tau=-3274, omega=-370, B=-1,
                C8_2022000=-66, C8_5683824=-28, C8_5691760=-120,
                C8_127305925=-110, C8_128354469=-156, C8_245715219=-64,
                C8_127242964=-F(668, 3))
    rows += [('six_bound', minus(six)), ('seven_bound', minus(seven))]
    objective = form(B=1)
    report = {'physical_order': list(physical), 'parameters': nine['parameters']+['tau', 'Omega', 'B'],
              'new_bound_row': list(map(str, minus(full))), 'cases': {}}
    for p in [None, 0]:
        current = rows if p is None else [(name, [row[0]+p*row[1]]+row[2:]) for name, row in rows]
        obj = objective if p is None else [objective[0]+p*objective[1]]+objective[2:]
        extra = minus(full) if p is None else [-full[0]-p*full[1]]+[-x for x in full[2:]]
        label = 'unconditional' if p is None else f'P={p}'
        case = {}
        for add in [False, True]:
            rr = current+([('four_four_bound', extra)] if add else [])
            result = certify(rr, obj)
            case['with_four_four' if add else 'previous'] = result
            print(label, 'new family', add, 'B >=', result['lower_bound'], flush=True)
        report['cases'][label] = case
    report['scope'] = 'Exact consequence of safe pair-loss subtraction; counts no unaudited (6,3) or (7,1) family.'
    (ROOT/'data/codex_four_four_bound.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
