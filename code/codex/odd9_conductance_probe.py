"""New conductance-sign statistic on a producer-certified four-star border.

No input rank, PSD test, or automorphism group is recomputed. This tests the
new proposed explanation 'the odd Schur matrix is an ordinary Laplacian'.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from odd9_network_schur import line_network, TWO_LABELS


def probe(path):
    raw = Path(path).read_bytes()
    data = json.loads(raw.decode('utf-8-sig'))
    labels = tuple(tuple(sorted(p)) for p in data['labels'])
    index = {p: i for i, p in enumerate(labels)}
    gamma = data.get('gamma', data.get('adjacency'))
    if gamma is None:
        gamma = sp.zeros(44)
        for i, j in data['edges']:
            gamma[i, j] = gamma[j, i] = 1
    gamma = sp.Matrix(gamma)
    old = [index[p] for p in TWO_LABELS]
    network = line_network(gamma.extract(old, old))
    f = sp.zeros(44, 10)
    for j, y in enumerate(range(4, 14)):
        f[index[2, y], j], f[index[3, y], j] = 1, -1
    p = sp.zeros(10, 9)
    for j in range(9):
        p[j, j], p[9, j] = 1, -1
    odd = f*p
    q = gamma.extract(old, range(44))*odd
    keep = network['retained']
    qg = q.extract(keep, range(9))
    s9 = 8*odd.T*(3*sp.eye(44)-gamma)*odd-64*qg.T*network['grounded'].inv(method='DM')*qg
    left_inverse = (p.T*p).inv()*p.T
    s10 = left_inverse.T*s9*left_inverse
    assert s10*sp.ones(10, 1) == sp.zeros(10, 1) and p.T*s10*p == s9
    signs = Counter(int(sp.sign(s10[i, j])) for i, j in combinations(range(10), 2))
    positive = [(s10[i, j], i+4, j+4) for i, j in combinations(range(10), 2) if s10[i, j] > 0]
    value, y, z = max(positive, default=(0, None, None))
    return dict(status='NEW_ODD_EFFECTIVE_CONDUCTANCE_STATISTIC', source=str(path), sha256=sha256(raw).hexdigest(),
                off_diagonal_sign_counts=dict(signs), ordinary_nonnegative_conductance_laplacian=not positive,
                largest_positive_off_diagonal=dict(outer_letters=[y, z], value_in_8T_gram=str(value)),
                conclusion='The ordinary nonnegative-conductance Laplacian explanation is refuted on this certified border.' if positive else 'This sample has the proposed sign property; it does not establish the universal claim.',
                scope='Only new exact Schur coefficients computed. Producer admissibility, PSD and ranks are accepted, not re-audited. ODD9 itself is not refuted by a positive off-diagonal entry.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = probe(args.input)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))
