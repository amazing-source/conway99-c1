"""Exact conditional dual thresholds for rank 37 with all proved bounds."""
from fractions import Fraction as F
import argparse
import json
import sys

CLI_ARGS = sys.argv[1:]

import joint_theta_lp_probe as J
from rank35_grid_audit import constraints
from rank43_coset_audit import certified_minimum


def main(order9=False):
    A, B = J.family(36, J.basis(84))
    base, const = constraints(37, -30, all_sixsets=True)
    cap = [-x for x in A[7]]+[F(0)]*2
    cap[0] += 990
    base.append(('a7<=990', cap))
    if order9:
        data = json.loads((J.ROOT/'data/codex_order9_uniform_shell_bounds.json').read_text())
        for index, name in [(3, 'b3'), (4, 'b4_seven'), (5, 'b5')]:
            low = F(data[name]['lower_bound'])
            row = list(B[index])+[F(0)]*2
            row[0] -= low
            base.append((f'order9_b{index}>={low}', row))
        base += [('order9_P<=852', const(852, p=-1)),
                 ('order9_rho<=126', const(126, rho=-1))]
    objective = [-x for x in B[4]]+[F(0)]*2
    reports = []
    for low in ((43848 if order9 else 24948), 150000, 300000, 600000, 900000):
        bound = list(B[3])+[F(0)]*2
        bound[0] -= low
        rows = base+[(f'conditional_b3>={low}', bound)]
        res = J.solver.simplex([f[1:] for _, f in rows], [-f[0] for _, f in rows], objective[1:])
        if res[0] == 'optimal':
            certificate = certified_minimum(rows, objective)
            maximum = -F(certificate['bound'])
            record = {'conditional_b3_lower_bound': low, 'maximum_b4': str(maximum),
                      'certificate_and_feasible_point': certificate}
            print('b3>=', low, ': maximum b4 =', maximum, float(maximum), flush=True)
        else:
            assert res[0] == 'unbounded'
            weights = res[1]
            value = [sum(w*f[i] for w, (_, f) in zip(weights, rows)) for i in range(10)]
            assert all(w >= 0 for w in weights) and value[0] < 0 and not any(value[1:])
            record = {'conditional_b3_lower_bound': low, 'status': 'infeasible',
                      'certificate': [(name, str(w)) for (name, _), w in zip(rows, weights) if w],
                      'negative_constant': str(value[0])}
            print('b3>=', low, ': infeasible', flush=True)
        reports.append(record)
    out = {'rank': 37, 'q_precision': 84, 'order9_consequences': order9, 'cases': reports,
           'base_rows': [(name, list(map(str, f))) for name, f in base],
           'scope': 'Conditional targets only. No new bound on b3 or b4 and no exclusion of rank37.'}
    suffix = '_order9' if order9 else ''
    (J.ROOT/f'data/codex_rank37_dual_frontier{suffix}.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--order9', action='store_true')
    main(parser.parse_args(CLI_ARGS).order9)
