"""Explore audited small-shell bounds with LAB's rational simplex.

Every constraint is reconstructed in Codex's c1..c7 coordinates. Returned
feasible rational points are independently checked against every row.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

from theta7_audit import basis
from theta7_certificates_audit import family

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'code/lab_theta_lp_2026-10-08'))
sys.argv = [sys.argv[0], '84']
import theta_lp_exact as solver


def main():
    forms = basis(84)
    source = json.loads((ROOT/'data/codex_joint_theta_small_shells.json').read_text())
    lows = {int(k): v for k, v in source['lower_bounds_M_q_coefficients'].items()}
    lows[4] = max(lows[4], 1431738)
    cases = []
    for r in (35, 37, 39, 41, 43):
        a, b = family(r-1, forms)
        rows = [(f'a{n}>=0', a[n]) for n in range(7, 85)]
        rows += [(f'b{n}>=0', b[n]) for n in range(1, 85)]
        for n, low in sorted(lows.items()):
            row = list(b[n]); row[0] -= low
            rows.append((f'b{n}>={low}', row))
        for n in range(1, 13):
            rows.append((f'a{7*n}>=b{n}', [x-y for x, y in zip(a[7*n], b[n])]))
        row = [-7*x-8*y for x, y in zip(a[7], a[8])]; row[0] += 55440
        rows.append(('7a7+8a8<=55440', row))
        result = solver.minimise(rows, [F(0)]*8)
        if result[0] == 'min':
            point = result[2]
            assert len(point) == 7
            values = [f[0]+sum(x*y for x, y in zip(f[1:], point)) for _, f in rows]
            assert all(x >= 0 for x in values)
            case = {'rank': r, 'status': 'feasible', 'c1_to_c7': list(map(str, point)),
                    'checked_constraints': len(rows), 'minimum_slack': str(min(values))}
        else:
            status, certificate = solver.feasible(rows)
            assert status == 'infeasible'
            weights = dict(certificate); by_label = dict(rows)
            identity = [sum(w*by_label[name][i] for name, w in weights.items()) for i in range(8)]
            assert identity[0] < 0 and not any(identity[1:]) and all(w >= 0 for w in weights.values())
            case = {'rank': r, 'status': status, 'certificate': [(name, str(w)) for name, w in certificate],
                    'negative_constant': str(identity[0])}
        print(json.dumps(case), flush=True)
        cases.append(case)
    report = {'q_precision': 84, 'lower_bounds': lows, 'cases': cases,
              'scope': 'Exact rational relaxation only; feasible points need not be integral lattice theta series.'}
    (ROOT/'data/codex_joint_theta_lp_probe.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
