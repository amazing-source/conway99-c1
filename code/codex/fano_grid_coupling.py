"""Exact affine competition between Fano ten-point motifs and grids.

Discover at a fixed rho, then remove that equality from the dual certificate
to obtain an unconditional affine inequality. The numerical point is not
used as an existence assertion. Only the rational dual identity is used.
"""
from fractions import Fraction as F
import argparse
import json
import time

from fano_order10_bound import load, core_check, discover, audit_recurrences
from higher_census_minima import ROOT


GEOMETRY = {
    'geometry_P>=6rho': {1: F(1), 10: F(-6)},
    'geometry_P+5rho<=1386': {0: F(1386), 1: F(-1), 10: F(-5)},
}
OUTPUT = ROOT/'data/codex_fano_grid_coupling.json'


def combine(rows, certificate):
    result = {}
    for name, weight in certificate:
        weight = F(weight)
        assert weight >= 0
        for key, value in rows[name].items():
            result[key] = result.get(key, F(0))+weight*value
    return {key: value for key, value in result.items() if value}


def main(verify_only=False, audit=False, fixed_rho=126):
    started = time.monotonic()
    source, census, graphs = load()
    core = core_check(source)
    assert core['parameter_id'] == 438
    # Parameter 1 is a prism; parameter 10 is the 3x3 rook graph.
    assert source['params'][0][:2] == [6, 29327]
    assert source['params'][9][:2] == [9, 64584018291]
    fixed = {
        f'fixed_rho>={fixed_rho}': {0: F(-fixed_rho), 10: F(1)},
        f'fixed_rho<={fixed_rho}': {0: F(fixed_rho), 10: F(-1)},
    }
    output = OUTPUT if fixed_rho == 126 else OUTPUT.with_stem(OUTPUT.stem+f'_rho{fixed_rho}')
    rows = census | GEOMETRY | fixed
    if verify_only:
        report = json.loads(output.read_text())
    else:
        conditional = discover(source, rows, core)
        coefficients = combine(rows, conditional['certificate'])
        assert coefficients == {0: F(conditional['F10_upper_bound']), 438: F(-1)}
        global_certificate = [(name, weight) for name, weight in conditional['certificate']
                              if name not in fixed]
        total = combine(rows, global_certificate)
        assert set(total) <= {0, 10, 438} and total[438] == -1
        slope = -total.get(10, F(0)); constant = total.get(0, F(0))
        report = {
            'source': 'codex_lab_full_order10.json.gz', 'core': core,
            'geometry_rows': {name: {str(k): str(v) for k, v in row.items()}
                              for name, row in GEOMETRY.items()},
            'conditional_rho': fixed_rho,
            'conditional_F10_upper_bound': conditional['F10_upper_bound'],
            'conditional_certificate': conditional['certificate'],
            'global_certificate': global_certificate,
            'rho_coefficient': str(slope), 'constant': str(constant),
            'scope': 'N(F10)+rho_coefficient*rho<=constant; necessary conditions only; no rank exclusion.'}
    conditional = combine(rows, report['conditional_certificate'])
    assert conditional == {0: F(report['conditional_F10_upper_bound']), 438: F(-1)}
    total = combine(census | GEOMETRY, report['global_certificate'])
    slope, constant = F(report['rho_coefficient']), F(report['constant'])
    assert total == {k: v for k, v in {0: constant, 10: -slope, 438: F(-1)}.items() if v}
    assert report['conditional_rho'] == fixed_rho
    assert constant-fixed_rho*slope == F(report['conditional_F10_upper_bound'])
    # Removing the geometric row as well gives a stronger inequality that
    # retains P. This is now a sum of census counts alone.
    pure_certificate = [(name, weight) for name, weight in report['global_certificate'] if name in census]
    pure = combine(census, pure_certificate)
    assert set(pure) <= {0,1,10,438} and pure[438] == -1
    if fixed_rho == 125:
        assert pure == {0:F(42273,2),1:F(-75,4),10:F(-24),438:F(-1)}
    if audit:
        used = [(name, weight) for name, weight in report['global_certificate'] if name in census]
        info = audit_recurrences(source, census, graphs, {'certificate': used})
        if not verify_only:
            report['independent_recurrence_audit'] = info
    if not verify_only:
        output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Verified N(F10) +', slope, '* rho <=', constant,
          '; at rho=', fixed_rho, ':', constant-fixed_rho*slope,
          '; a7 <=', F(2,21)*(constant-fixed_rho*slope),
          '; seconds', round(time.monotonic()-started, 1), flush=True)
    print('Census-only identity:',{k:str(v) for k,v in pure.items()},flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--audit-recurrences', action='store_true')
    parser.add_argument('--rho', type=int, default=126, choices=range(127))
    args = parser.parse_args()
    main(args.verify_only, args.audit_recurrences, args.rho)
