"""Audit far-triangle differences and exploit all collision multiplicities.

The class inequality is valid for every nonnegative integer class size.
Finite counts and every LP certificate use exact arithmetic.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json

from higher_census_minima import ROOT, certify
from joint_theta_small_shells import decode


def finite_audit():
    source = json.loads((ROOT/'data/codex_six_vertex_grid_audit.json').read_text())
    raw = [0, 0]
    contributing = []
    for row in source['census']['counts']:
        adj = decode(6, row['code'])
        multiplicity = 0
        for triple in combinations(range(6), 3):
            positive = sum(1 << i for i in triple)
            negative = 63 ^ positive
            if all((adj[i] & (positive if positive >> i & 1 else negative)).bit_count() == 2
                   and not (adj[i] & (negative if positive >> i & 1 else positive))
                   for i in range(6)):
                multiplicity += 1
        if multiplicity:
            contributing.append({'code': row['code'], 'signed_multiplicity': multiplicity})
            raw[0] += multiplicity*row['constant']
            raw[1] += multiplicity*row['prism_coefficient']
    assert raw == [7392, -2]
    # Two disjoint anticomplete prisms, modulo their indicator difference.
    triangles = [(0, 1, 2), (3, 4, 5)]
    vectors = []
    for offset in (0, 6):
        for positive in triangles:
            for negative in triangles:
                v = [0]*12
                for i in positive:
                    v[i+offset] = 1
                for i in negative:
                    v[i+6-offset] = -1
                vectors.append(tuple(v))
    relation = [1]*6+[-1]*6
    quotient = lambda v: tuple(x-v[0]*y for x, y in zip(v, relation))
    histogram = Counter(Counter(map(quotient, vectors)).values())
    assert len(set(vectors)) == 8 and histogram == {2: 4}
    return {'signed_raw_affine_in_P': raw, 'contributing_types': contributing,
            'twin_pair_quotient_class_histogram': dict(histogram),
            'unordered_collision_pairs_per_twin_pair': 4}


def main():
    audit = finite_audit()
    nine = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    graph_rows = [(str(r['code']), list(map(F, r['affine']))) for r in nine['counts']]
    width = len(nine['parameters'])+1
    P = [F(0), F(1)]+[F(0)]*(width-2)
    rho = dict(graph_rows)['13262907120']
    def form(c=0, p=0, r=0, tau=0, B=0):
        row = [p*x+r*y for x, y in zip(P, rho)]
        row[0] += c
        return row+[F(tau), F(B)]
    rows = [(name, row+[F(0), F(0)]) for name, row in graph_rows]
    rows += [('tau>=0', form(tau=1)), ('2tau<=5P', form(p=5, tau=-2)),
             ('tau<=2P+3rho', form(p=2, r=3, tau=-1)),
             ('tau>=6rho-231', form(c=231, r=-6, tau=1))]
    raw = json.loads((ROOT/'data/codex_order9_raw_family_minima.json').read_text())
    N4 = list(map(F, raw['Q4_edges9_3_cross0']['objective']))
    rows.append(('8tau<=N4', N4+[F(-8), F(0)]))
    # Old b3 bound, plus exact lower bounds for the disjoint new family.
    old = form(66528, p=-18, r=-72)
    rows.append(('previous_b3', [-x for x in old[:-1]]+[F(1)]))
    class_bounds = {}
    R = form(7392, p=-2)
    for k in range(1, 9):
        # m - C(m,2) when k=1. For every integer m>=1,
        # 1 - [2m/(k+1)-2*C(m,2)/(k*(k+1))]
        # = (m-k)*(m-k-1)/(k*(k+1)) >= 0.
        gain = [2*x/F(k+1) for x in R]
        gain[-2] -= F(8, k*(k+1))
        lower = [x+y for x, y in zip(old, gain)]
        row = [-x for x in lower]
        row[-1] = 1
        rows.append((f'far_triangle_classes_k={k}', row))
        class_bounds[str(k)] = list(map(str, lower))
    objective = form(B=1)
    report = {'finite_audit': audit, 'parameters': nine['parameters']+['tau', 'b3'],
              'graph_count_source': 'data/codex_order9_census.json (append two zero coordinates)',
              'additional_rows': [(name, list(map(str, row))) for name, row in rows[len(graph_rows):]],
              'class_bound_rows': class_bounds, 'cases': {}}
    for p in (None, 0):
        rr = rows if p is None else [(name, [row[0]+p*row[1]]+row[2:]) for name, row in rows]
        obj = objective if p is None else [objective[0]+p*objective[1]]+objective[2:]
        result = certify(rr, obj)
        result['objective'] = list(map(str, obj))
        name = 'unconditional' if p is None else 'P=0'
        report['cases'][name] = result
        print(name, 'b3 >=', result['lower_bound'], flush=True)
    report['scope'] = 'Proved distinct norm-six vectors, disjoint from the previously counted norm-six families.'
    (ROOT/'data/codex_far_triangle_shell_bound.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
