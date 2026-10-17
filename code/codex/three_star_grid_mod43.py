"""Short arithmetic obstruction for the specific Claude bridge700 boundary.

This derives a NEW nonextension certificate from its rational completion
metric. It is not a claim about every grid or every Z5-invariant boundary.
The seed's local PSD/rank30 result comes from its producer.
"""
import argparse
from pathlib import Path
import json

import sympy as sp


def certificate(domain_report, gamma_file):
    report = json.loads(Path(domain_report).read_text(encoding='utf-8-sig'))
    seed = json.loads(Path(gamma_file).read_text(encoding='utf-8-sig'))
    labels = [tuple(p) for p in report['input_labels']]
    old = {tuple(p):i for i, p in enumerate(seed['labels'])}
    gamma = [[seed['gamma'][old[p]][old[q]] for q in labels] for p in labels]
    basis = report['spectral_basis']
    N = sp.Matrix(report['inverse_numerator'])
    den = report['inverse_denominator']
    def k8(p, q):
        return 3*len(set(p).intersection(q))+sum((c ^ 1) in q for c in p)-2
    M = sp.Matrix(34, 34, lambda i, j: 24*int(i == j)-8*gamma[i][j]-k8(labels[i], labels[j]))
    H = M.extract(basis, basis)
    # Certificate of OUR newly computed completion metric, not a seed-rank scan.
    assert H*N == den*sp.eye(30)
    grid = [(0, 2), (0, 3), (1, 2), (1, 3)]
    g = sp.Matrix([int(p in grid) for p in labels])
    # Use the grid relation identified by the producer, with the reported labels.
    assert M*g == sp.zeros(34, 1)
    weights = []
    for c, d in labels:
        weights.append(1 if (c, d) in ((0, 2), (1, 2)) else
                       4 if c in (0, 1) and d >= 4 and d % 2 == 0 else
                       2 if c == 2 and d >= 4 and d % 2 == 0 else 0)
    r = sp.Matrix([weights[i] for i in basis])
    assert all(weights[i] == 0 for i in range(34) if i not in basis)
    coefficient = int(N[0, 0]) % 43
    assert coefficient and den % 43 == 0
    assert all(int(x) % 43 == 0 for x in N-coefficient*r*r.T)
    label = (3, 4)
    base = sp.Matrix([-k8(p, label) for p in labels])
    assert (g.T*base)[0] == 0
    base_weight = sum(w*int(x) for w, x in zip(weights, base))
    assert base_weight == 62
    allowed = list(range(10))
    required = base_weight*pow(16, -1, 43) % 43
    assert required == 20 and required not in allowed
    return dict(
        status='EXACT_MOD43_NONEXTENSION_CERTIFICATE',
        seed=gamma_file, remaining_label=label, modulus=43,
        inverse_denominator=den, inverse_numerator_rank_one_coefficient=coefficient,
        full_label_weights=weights, spectral_basis=basis,
        norm_condition='m_I^t H^-1 m_I=20 because the full residual rank is30.',
        inverse_certificate='H*N=d*I exactly; d is divisible by43; N=coefficient*r*r^t modulo43.',
        consequence='The norm condition implies r^t m_I=0 modulo43.',
        grid_consequence='The grid relation forces h=0 on all four grid labels for u={3,4}.',
        counts='Choose two labels {0,x}, two {1,x}, one {2,x}, with x in4..13.',
        weighted_count='Let e be the number of even x among the first four choices, f among the last choice. Then 0<=e<=4, 0<=f<=1, r^t m_I=62-32e-16f.',
        contradiction='Writing n=2e+f gives 0<=n<=9, while62-16n=0 modulo43 requires n=20 modulo43.',
        required_residue=required, allowed_integer_range=[0, 9],
        scope='Excludes this supplied boundary without local-cap enumeration or any assumed symmetry of its completion. Does not exclude all grids, all Z5 boundaries, or C1.'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain-report', required=True)
    parser.add_argument('--gamma', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = certificate(args.domain_report, args.gamma)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status', 'modulus', 'inverse_numerator_rank_one_coefficient', 'contradiction')}))


if __name__ == '__main__':
    main()
