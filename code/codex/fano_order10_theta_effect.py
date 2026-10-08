"""Exact rank-37 theta consequences of the newly proved a7 <= 842."""
from fractions import Fraction as F
import json
import sys

VERIFY_ONLY = '--verify-only' in sys.argv

import joint_theta_lp_probe as J
from rank43_coset_audit import certified_minimum


def main():
    source = json.loads((J.ROOT/'data/codex_rank37_dual_frontier_order9_far_triangles.json').read_text())
    a, b = J.family(36, J.basis(84))
    base = [(name, list(map(F, form))) for name, form in source['base_rows'] if name != 'a7<=990']
    far_triangle_lower = json.loads((J.ROOT/'data/codex_far_triangle_shell_bound.json').read_text())
    low = F(far_triangle_lower['cases']['unconditional']['lower_bound'])
    row = list(b[3])+[F(0)]*2
    row[0] -= low
    base.append((f'full_census_b3>={low}', row))
    objectives = {'b4': [-x for x in b[4]]+[F(0)]*2,
                  'b4+(651/34)b3': [-x-F(651, 34)*y for x, y in zip(b[4], b[3])]+[F(0)]*2}
    path = J.ROOT/'data/codex_fano_order10_theta_effect.json'
    report = json.loads(path.read_text()) if VERIFY_ONLY else {
        'rank': 37, 'q_precision': 84, 'cases': {},
        'scope': 'Exact rational theta relaxation, with proved bounds only. No rank-37 exclusion.'}
    for cap in (990, 842):
        row = [-x for x in a[7]]+[F(0)]*2
        row[0] += cap
        rows = base+[(f'a7<={cap}', row)]
        if not VERIFY_ONLY:
            report['cases'][str(cap)] = {}
        by_name = dict(rows)
        for label, objective in objectives.items():
            result = report['cases'][str(cap)][label] if VERIFY_ONLY else certified_minimum(rows, objective)
            total = [F(0)]*10
            for name, weight in result['certificate']:
                weight = F(weight)
                assert weight >= 0
                total = [x+weight*y for x, y in zip(total, by_name[name])]
            assert total[1:] == objective[1:]
            assert objective[0]-total[0] == F(result['bound'])
            point = list(map(F, result['point']))
            assert all(form[0]+sum(x*y for x, y in zip(form[1:], point)) >= 0 for _, form in rows)
            assert objective[0]+sum(x*y for x, y in zip(objective[1:], point)) == F(result['bound'])
            if not VERIFY_ONLY:
                report['cases'][str(cap)][label] = result
            print('a7 <=', cap, ':', label, '<=', -F(result['bound']), float(-F(result['bound'])), flush=True)
    if not VERIFY_ONLY:
        path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
