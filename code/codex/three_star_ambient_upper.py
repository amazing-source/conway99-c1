"""The necessary complementary Gram U=7*Pi_SS-T_SS for Conway boundaries.

All rejections have integer witnesses. Floating eigenvectors, when useful,
only propose short vectors whose negative quadratic value is then exact.
"""
import argparse
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import json

import numpy as np
import sympy as sp


LABELS = tuple(p for p in combinations(range(14), 2)
               if p[1] != (p[0] ^ 1) and set(p).intersection((0, 1, 2)))


def upper15(gamma):
    return sp.Matrix(34, 34, lambda i, j:
        60*int(i == j)+15*gamma[i][j]-4*len(set(LABELS[i]).intersection(LABELS[j]))
        +sum((c ^ 1) in LABELS[j] for c in LABELS[i])-2)


def integer_vector(vector):
    denominator = lcm(*(int(x.q) for x in vector))
    out = [int(x*denominator) for x in vector]
    common = gcd(*out)
    out = [x//common for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out


def psd_or_witness(matrix):
    n = matrix.rows
    def reject(vector):
        q = sp.Matrix(vector)
        value = int((q.T*matrix*q)[0])
        assert value < 0
        return dict(psd=False, integer_witness=list(map(int, q)), quadratic_value=value)
    approximate = np.array(matrix.tolist(), dtype=float)
    values, vectors = np.linalg.eigh(approximate)
    if values[0] < 0:
        v = vectors[:, 0]/max(abs(vectors[:, 0]))
        for scale in (1, 2, 4, 8, 16, 32, 64, 128, 512, 2048):
            q = [int(round(scale*x)) for x in v]
            if (sp.Matrix(q).T*matrix*sp.Matrix(q))[0] < 0:
                return reject(q)
    # Exact congruence elimination also handles singular PSD matrices.
    M = matrix.copy()
    basis = [sp.eye(n).col(i) for i in range(n)]
    for i in range(n):
        pivot = M[i, i]
        if pivot < 0:
            return reject(integer_vector(basis[i]))
        if pivot == 0:
            j = next((j for j in range(i+1, n) if M[i, j]), None)
            if j is not None:
                t = -(M[j, j]+1)/(2*M[i, j])
                return reject(integer_vector(basis[j]+t*basis[i]))
            continue
        for j in range(i+1, n):
            basis[j] -= (M[i, j]/pivot)*basis[i]
        for j in range(i+1, n):
            for k in range(j, n):
                value = M[j, k]-M[j, i]*M[i, k]/pivot
                M[j, k] = M[k, j] = value
    return dict(psd=True, method='exact rational congruence pivots')


def orientation_cuts(gamma):
    results = []
    for other_signs in product((-1, 1), repeat=4):
        signs = {4:1, 5:-1}
        for c, value in zip((6, 8, 10, 12), other_signs):
            signs[c], signs[c+1] = value, -value
        q = [signs.get(p[1], 0) for p in LABELS]
        same = sum(gamma[i][j] for i in range(34) for j in range(i+1, 34)
                   if q[i] and q[i] == q[j])
        cross = sum(gamma[i][j] for i in range(34) for j in range(i+1, 34)
                    if q[i]*q[j] == -1)
        results.append(dict(signs=[signs[c] for c in (4, 6, 8, 10, 12)],
                            same_sign_edges=same, opposite_sign_edges=cross,
                            required_difference_at_most=45,
                            satisfied=(cross-same <= 45), q_gamma_q=2*(same-cross),
                            integer_witness=q))
    return results


def analyse(gamma):
    cuts = orientation_cuts(gamma)
    failures = [c for c in cuts if not c['satisfied']]
    U15 = upper15(gamma)
    if failures:
        q = sp.Matrix(failures[0]['integer_witness'])
        result = dict(psd=False, integer_witness=list(map(int, q)),
                      quadratic_value=int((q.T*U15*q)[0]))
        assert result['quadratic_value'] < 0
    else:
        result = psd_or_witness(U15)
    return dict(status='AMBIENT_UPPER_GRAM_PSD' if result['psd'] else 'NO_CONWAY_COMPLETION',
                complementary_gram=result, orientation_cut_violations=failures,
                orientation_cut_count=16,
                formula='15U=60I+15Gamma-4*intersection+mate_incidence-2J',
                meaning='Every actual Conway boundary has U=7Pi_SS-T_SS PSD; this is stronger than T_SS<=7I.',
                scope='Necessary condition for every SRG(99,14,1,2), independent of its automorphism group.')


def load_gamma(path):
    raw = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    labels = [tuple(sorted(p)) for p in raw['labels']]
    assert len(labels) == 34 and set(labels) == set(LABELS)
    index = {p:i for i, p in enumerate(labels)}
    return [[int(raw['gamma'][index[p]][index[q]]) for q in LABELS] for p in LABELS]


def self_test():
    assert psd_or_witness(sp.Matrix([[1, 1], [1, 1]]))['psd']
    assert not psd_or_witness(sp.Matrix([[0, 1], [1, 0]]))['psd']
    assert not psd_or_witness(sp.Matrix([[1, 2], [2, 1]]))['psd']
    intersection = sp.Matrix(34, 34, lambda i, j: len(set(LABELS[i]).intersection(LABELS[j])))
    mate = sp.Matrix(34, 34, lambda i, j: sum((c ^ 1) in LABELS[j] for c in LABELS[i]))
    Pi120 = 120*sp.eye(34)-11*intersection-mate+2*sp.ones(34)
    fractional = (2*sp.ones(34)-intersection-mate)/10
    assert upper15(fractional.tolist()) == Pi120/2  # U=4Pi for our fractional witness.
    assert psd_or_witness(Pi120/2)['psd']
    for cut in orientation_cuts([[0]*34 for _ in range(34)]):
        q = sp.Matrix(cut['integer_witness'])
        assert (q.T*q)[0] == 30
        assert (q.T*Pi120*q)[0] == 2700  # q Pi q =45/2.
        K8 = 3*intersection+mate-2*sp.ones(34)
        assert (q.T*K8*q)[0] == 180       # q K q =45/2.
    return dict(status='OWN_AMBIENT_GRAM_PRIMITIVES_PASS', orientations=16)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--output', required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    result = self_test() if args.self_test else analyse(load_gamma(args.gamma))
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    summary = {k:result[k] for k in ('status', 'orientations') if k in result}
    if 'complementary_gram' in result:
        summary['upper_PSD'] = result['complementary_gram']['psd']
        summary['orientation_violations'] = len(result['orientation_cut_violations'])
        summary['negative_witness_value'] = result['complementary_gram'].get('quadratic_value')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
