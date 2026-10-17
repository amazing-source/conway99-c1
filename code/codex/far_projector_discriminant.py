"""Audit the local constants in the far-lattice discriminant identity.

For a connected, layer-regular cubic near graph G, verify using exact
determinants that det(E Z^B) = 4*tau(G)/(81*7^36), where
E = (3I-A+J/9)/7 is the full SRG's minus-four projector and |B|=39.
This checks the local identity, not existence of an SRG completion.
"""
import argparse
import json
from pathlib import Path

import sympy as sp

from generic_star_apex_audit import cyclic_ball


def audit(g):
    g = sp.Matrix(g)
    assert g.shape == (36, 36) and g == g.T
    assert all(x in (0, 1) for x in g) and all(g[i, i] == 0 for i in range(36))
    assert all(sum(g[i, j] for j in range(12*a, 12*a+12)) == 1
               for i in range(36) for a in range(3))
    h = 3*sp.eye(36)-g
    tau = h[:35, :35].det(method='domain-ge')
    assert tau > 0  # Connectedness, via the tree cofactor.
    adjacency = sp.zeros(39)
    adjacency[:3, :3] = sp.ones(3)-sp.eye(3)
    adjacency[3:, 3:] = g
    for a in range(3):
        for p in range(12*a, 12*a+12):
            adjacency[a, p+3] = adjacency[p+3, a] = 1
    e63 = 9*(3*sp.eye(39)-adjacency)+sp.ones(39)
    kernel = (adjacency+4*sp.eye(39))[:, :3]
    assert e63*kernel == sp.zeros(39, 3)
    kernel_gram = kernel.T*kernel
    assert kernel_gram == 21*sp.eye(3)+9*sp.ones(3)
    assert kernel_gram.det() == 21168
    # These three rows make an identity matrix: the integer kernel is
    # primitive, and the other 36 projected columns generate E Z^B.
    removed = [3, 15, 27]
    assert kernel.extract(removed, range(3)) == sp.eye(3)
    kept = [i for i in range(39) if i not in removed]
    integer_determinant = e63.extract(kept, kept).det(method='domain-ge')
    assert integer_determinant == 4*9**34*tau
    # The positive determinant proves that the displayed kernel is full.
    projected_determinant = sp.Rational(integer_determinant, 63**36)
    assert projected_determinant == sp.Rational(4*tau, 81*7**36)
    # Quotient blocks on apex/layer constants: constant and contrast.
    constant = sp.Matrix([[sp.Rational(4, 3), -8], [-sp.Rational(2, 3), 4]])/7
    contrast = sp.Matrix([[4, -12], [-1, 3]])/7
    assert constant.det() == contrast.det() == 0
    assert constant.trace() == sp.Rational(16, 21) and contrast.trace() == 1
    return {'adjacency': [list(map(int, g.row(i))) for i in range(36)],
            'spanning_trees': int(tau), 'tau_mod7': int(tau % 7),
            'kernel_gram_determinant': 21168,
            'integer_projected_gram_determinant': str(integer_determinant),
            'projected_lattice_determinant': str(projected_determinant),
            'verified_identity': 'det(E Z^B) = 4 tau / (81 * 7^36)'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--balls', type=Path, nargs='*')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding='utf-8'))
        for entry in report:
            assert entry['audit'] == audit(entry['audit']['adjacency'])
    else:
        inputs = [(p.stem, json.loads(p.read_text(encoding='utf-8'))['adjacency']) for p in args.balls] if args.balls else [('cyclic(2,4,1)', cyclic_ball())]
        report = [{'source': name, 'audit': audit(g)} for name, g in inputs]
        args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'verified': len(report), 'tree_counts': [r['audit']['spanning_trees'] for r in report]}))


if __name__ == '__main__':
    main()
