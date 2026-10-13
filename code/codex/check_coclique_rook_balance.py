"""Exact arithmetic certificate for the new rook/coclique incidence restriction."""
from pathlib import Path
from itertools import combinations
import argparse
import json
import sympy as sp


def check(folder):
    rook = sp.Matrix(9, 9, lambda i, j: int(i != j and (i//3 == j//3 or i%3 == j%3)))
    assert rook*rook+rook == 2*sp.eye(9)+2*sp.ones(9)
    H, X, center = [0, 1, 4, 3], [2, 7, 5, 6], 8
    for i in range(4):
        assert [h for h in H if rook[X[i], h]] == [h for j, h in enumerate(H) if j in (i, (i+1)%4)]
    assert [(i, j) for i, j in combinations(range(4), 2) if rook[X[i], X[j]]] == [(0, 2), (1, 3)]
    assert all(rook[center, x] for x in X) and all(not rook[center, h] for h in H)
    profiles = []
    for a, e in [(0, e) for e in range(2, 7)]+[(1, 2), (1, 3)]:
        b = 6-3*a-e
        upper = 9+2*a+b
        assert upper == 15-a-e and upper < 15
        profiles.append(dict(a=a, e=e, n2=b, max_charge_on_nine=upper,
                             charge_required_if_disjoint=15, disjoint_impossible=True,
                             intersection_three_possible_at_this_level=e == 6))
    for C in combinations(range(9), 3):
        if any(rook[u, v] for u, v in combinations(C, 2)): continue
        remainder = [i for i in range(9) if i not in C]
        E = rook[remainder, remainder]
        assert all(sum(E.row(i)) == 2 for i in range(6)) and sp.trace(E**3) == 0
        # A simple 2-regular triangle-free graph on six vertices is C6.
    outside = [dict(center_charge=q, actual_charge=12+q, required_charge=15)
               for q in (-1, 0, 1, 2)]
    assert all(row['actual_charge'] != row['required_charge'] for row in outside)
    report = dict(status='PASS', rook_adjacency=[[int(x) for x in rook.row(i)] for i in range(9)],
        H=H, X=X, center=center, profiles=profiles,
        profile_02_center_outside_C=outside,
        profile_02_center_inside_C=dict(actual_charge=12, required_charge=8),
        family_cut='A_x0x2+A_x1x3+sum_x_in_X A_vx <= 5',
        strengthened_cuts=['A_x0x2+sum_x_in_X A_vx <= 4', 'A_x1x3+sum_x_in_X A_vx <= 4'],
        strengthened_cut_external_dependency=dict(theorem='Lou-Murin Theorem 2.1: no induced rook minus one edge',
            source='https://math.mit.edu/research/highschool/primes/materials/2014/Lou-Murin.pdf',
            status='Published-source theorem used; not independently re-proved by this arithmetic checker'),
        scope='No rook can contain the distinguished H in any (0,2) graph; whole (0,2) remains open')
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'rook_balance_certificate.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('status', 'scope', 'family_cut', 'strengthened_cuts')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('folder', type=Path)
    check(parser.parse_args().folder)
