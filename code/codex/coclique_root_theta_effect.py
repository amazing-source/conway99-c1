"""Exact rank37 theta ceilings after the all-ranks root bound b1 <= 44."""
from fractions import Fraction as F
import json
import sys

VERIFY_ONLY = '--verify-only' in sys.argv
import joint_theta_lp_probe as J
from rank43_coset_audit import certified_minimum


def main():
    old = json.loads((J.ROOT/'data/codex_rank37_dual_frontier_order9_far_triangles.json').read_text())
    a, b = J.family(36, J.basis(84))
    base = [(name, list(map(F, row))) for name, row in old['base_rows'] if name not in ('a7<=990', 'b1<=88')]
    for name, row, constant in [('a7<=842', [-v for v in a[7]], 842),
                                ('b1<=44', [-v for v in b[1]], 44),
                                ('full_census_b3>=45528', list(b[3]), -45528)]:
        row[0] += constant
        base.append((name, row+[F(0)]*2))
    root_rows = []
    for j in range(22):
        # For k=b1/2 integral: 2(k-j)(k-j-1)>=0.
        row = [x-(42+2*j)*y for x, y in zip(b[2], b[1])]
        row[0] -= 462-2*j*(j+1)
        root_rows.append((f'root_norm4_secant_{j}', row+[F(0)]*2))
    objectives = {'b4': [-v for v in b[4]]+[F(0)]*2,
                  'b4+(651/34)b3': [-x-F(651, 34)*y for x, y in zip(b[4], b[3])]+[F(0)]*2}
    path = J.ROOT/'data/codex_coclique_root_theta_effect.json'
    report = json.loads(path.read_text()) if VERIFY_ONLY else {
        'rank': 37, 'a7_cap': 842, 'b1_cap': 44, 'q_precision': 84, 'cases': {},
        'scope': 'Exact rational relaxation with proved constraints; no rank37 exclusion.'}
    for label, rows in [('root_cap44', base), ('root_cap44_and_norm4_counts', base+root_rows)]:
        if not VERIFY_ONLY:
            report['cases'][label] = {}
        by_name = dict(rows)
        for objective_label, objective in objectives.items():
            result = report['cases'][label][objective_label] if VERIFY_ONLY else certified_minimum(rows, objective)
            total = [F(0)]*10
            for name, weight in result['certificate']:
                weight = F(weight)
                assert weight >= 0
                total = [x+weight*y for x, y in zip(total, by_name[name])]
            assert total[1:] == objective[1:] and objective[0]-total[0] == F(result['bound'])
            point = list(map(F, result['point']))
            assert all(row[0]+sum(x*y for x, y in zip(row[1:], point)) >= 0 for _, row in rows)
            assert objective[0]+sum(x*y for x, y in zip(objective[1:], point)) == F(result['bound'])
            if not VERIFY_ONLY:
                report['cases'][label][objective_label] = result
            print(label, objective_label, '<=', -F(result['bound']), float(-F(result['bound'])), flush=True)
    if not VERIFY_ONLY:
        path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
