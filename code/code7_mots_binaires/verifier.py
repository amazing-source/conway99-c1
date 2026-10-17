#!/usr/bin/env python3
"""Small exact checks; standard library only. Does NOT construct a 99-SRG.

1. Check all possible count profiles in the two-moment argument.
2. Check two SRG(16,6,2,2) with different induced-C4 counts.
3. Check the separating-set bound by exact rational arithmetic.
The proofs connecting these calculations to the claims are in THEOREME.md
and AUDIT.md. No SAT solver, random sampling, or floating-point arithmetic.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb


def check_moments():
    profiles = []
    for t in range(15):
        weight = 7 * t
        if weight > 99:
            continue
        for inside10 in range(weight + 1):
            for outside14 in range(100 - weight):
                outside7 = 11 * t - inside10 - 2 * outside14
                outside0 = 99 - weight - outside7 - outside14
                if min(outside7, outside0) < 0:
                    continue
                if 2 * inside10 + outside7 + 4 * outside14 != 2 * t * t:
                    continue
                inside3 = weight - inside10
                # Independent verification in the unreduced integer moment equations.
                assert 3 * inside3 + 10 * inside10 + 7 * outside7 + 14 * outside14 == 14 * weight
                assert (9 * inside3 + 100 * inside10 + 49 * outside7 + 196 * outside14
                        == 12 * weight - (3 * inside3 + 10 * inside10) + 2 * weight**2)
                profiles.append((weight, inside3, inside10, outside0, outside7, outside14))
    expected = [(0, 0, 0, 99, 0, 0), (63, 0, 63, 0, 36, 0), (77, 0, 77, 0, 0, 22)]
    assert profiles == expected, profiles
    print('Moment profiles (weight, in3, in10, out0, out7, out14):', profiles)


def check_wl_example():
    points = list(product(range(4), repeat=2))
    steps = {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}
    rook = [[int(a != b and (a[0] == b[0] or a[1] == b[1])) for b in points] for a in points]
    shrikhande = [[int(((b[0]-a[0]) % 4, (b[1]-a[1]) % 4) in steps) for b in points] for a in points]
    for name, matrix, expected in [('Rook 4x4', rook, 36), ('Shrikhande', shrikhande, 12)]:
        assert all(matrix[i][i] == 0 and sum(matrix[i]) == 6 for i in range(16))
        assert all(matrix[i][j] == matrix[j][i] for i in range(16) for j in range(16))
        square = [[sum(matrix[i][k] * matrix[k][j] for k in range(16)) for j in range(16)] for i in range(16)]
        assert all(square[i][j] == (6 if i == j else 2) for i in range(16) for j in range(16))
        count = sum(all(sum(matrix[i][j] for j in vertices) == 2 for i in vertices)
                    for vertices in combinations(range(16), 4))
        hom_c4 = sum(value**2 for row in square for value in row)
        assert count == expected and hom_c4 == 1536
        print(f'{name}: SRG(16,6,2,2); induced C4={count}; hom(C4,G)={hom_c4}')


def check_separating_bound():
    # For a fixed pair u,v: a random m-set neither contains u,v nor
    # distinguishes them precisely when it lies among 73 other vertices.
    bound = Fraction(comb(99, 2) * comb(73, 24), comb(99, 24))
    assert bound < 1
    print('Union bound for a separating 24-set: exact rational < 1 verified')


if __name__ == '__main__':
    check_moments()
    check_wl_example()
    check_separating_bound()
    print('All finite checks passed. These checks do not prove existence/nonexistence of Conway-99.')
