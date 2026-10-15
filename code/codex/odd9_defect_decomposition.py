"""Replace universal ODD9 by exact formulas for its possible defect.

Producer message843 supplies the binary counterexamples. This module
does not re-read or re-certify them. Its default computation checks new
geometric identities and one abstract mixed-parity kernel example.
Optional relation analysis consumes a supplied odd relation, subtracts
the two forced star differences, and describes its coefficients.
"""
from collections import Counter
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import argparse
import json

import sympy as sp


LABELS = [(i, j) for i, j in combinations(range(14), 2)
          if i < 4 and j != (i ^ 1)]
INDEX = {p: i for i, p in enumerate(LABELS)}


def geometry():
    h = [INDEX[tuple(sorted(x ^ 1 if x < 4 else x for x in p))] for p in LABELS]
    reps = [i for i in range(44) if i < h[i]]
    F = sp.zeros(44, 22)
    for j, i in enumerate(reps):
        F[i, j], F[h[i], j] = 1, -1
    Wfull = sp.Matrix(44, 2, lambda i, c:
                      int(2*c in LABELS[i])-int(2*c+1 in LABELS[i]))
    W = F.T*Wfull/2
    B = sp.Matrix(14, 44, lambda a, i: int(a in LABELS[i]))
    K = sp.Matrix(44, 44, lambda i, j: sp.Rational(
        3*len(set(LABELS[i]) & set(LABELS[j]))
        +sum((x ^ 1) in LABELS[j] for x in LABELS[i])-2, 8))
    L = sp.Matrix(44, 44, lambda i, j: sp.Rational(
        4*len(set(LABELS[i]) & set(LABELS[j]))
        -sum((x ^ 1) in LABELS[j] for x in LABELS[i])+2, 15))
    return dict(h=h, reps=reps, F=F, W=W, Wfull=Wfull, B=B, K=K, L=L)


def defect_budget(nu, c_left, c_right, gain_left, gain_right,
                  pure_even_dimension, pure_odd_dimension):
    """Use producer dimensions; no kernel, PSD or graph ranks are recomputed."""
    a, b = pure_even_dimension, pure_odd_dimension
    s = nu-a-b
    if s < 0 or a < 2 or b < 2:
        raise ValueError('Inconsistent dimensions for a kernel containing four stars.')
    sides = []
    for c, gain in ((c_left, gain_left), (c_right, gain_right)):
        d = 9-gain
        eta = d-(b-2)
        if not 0 <= eta <= s:
            raise ValueError('Inconsistent mixed-parity correction.')
        e = 12+c-nu+d
        if e < 0:
            raise ValueError('Negative residual even rank increment.')
        sides.append(dict(c=c, odd_rank_gain=gain, ODD9_defect=d,
                          pure_odd_extra_relations=b-2, mixed_parity_correction=eta,
                          residual_even_rank_increment=e))
    return dict(nu=nu, pure_even_dimension=a, pure_odd_dimension=b,
                noninvariant_dimension=s, dimension_N_plus_hN=nu+s, sides=sides)


def primitive(vector):
    denominator = lcm(*(int(x.q) for x in vector))
    entries = [int(x*denominator) for x in vector]
    common = gcd(*entries)
    if not common:
        return None
    entries = [x//common for x in entries]
    if next(x for x in entries if x) < 0:
        entries = [-x for x in entries]
    return entries


def normalize_odd_relation(relation, labels=LABELS):
    """Remove forced star differences from a producer-supplied h-odd relation.

    Kernel membership is a producer hypothesis, not checked here. The
    operation is exact and returns a primitive vector of zero incidence.
    """
    labels = [tuple(sorted(p)) for p in labels]
    if len(labels) != 44 or set(labels) != set(LABELS):
        raise ValueError('Expected the44 four-star labels.')
    n = sp.Matrix([sp.Rational(x) for x in relation])
    if n.shape != (44, 1):
        raise ValueError('Expected one full44-coordinate relation.')
    n = n.extract([labels.index(p) for p in LABELS], [0])
    g = geometry()
    if any(n[g['h'][i]] != -n[i] for i in range(44)):
        raise ValueError('The supplied relation is not h-odd.')
    n -= g['Wfull']*(g['Wfull'].T*n)/24
    assert g['B']*n == sp.zeros(14, 1)
    answer = primitive(n)
    if answer is None:
        return dict(status='ONLY_FORCED_STAR_DIFFERENCES')
    O = [i for i, p in enumerate(LABELS) if p[1] < 4]
    outer = [answer[i] for i in range(44) if i not in O]
    return dict(status='NORMALIZED_EXTRA_ODD_RELATION', labels=LABELS,
                primitive_vector=answer, overlap_values=[answer[i] for i in O],
                outer_value_histogram=dict(sorted(Counter(outer).items())),
                outer_even_coordinates=sum(x % 2 == 0 for x in outer),
                outer_zero_coordinates=outer.count(0), height=max(map(abs, answer)),
                root_incidence='ZERO_BY_NORMALIZATION',
                scope='Producer kernel membership is assumed; no graph is read.')


def abstract_mixed_fixture(g):
    stars = sp.Matrix(44, 4, lambda i, c: int(c in LABELS[i]))
    n = sp.zeros(44, 1)
    for label, value in (((0, 4), 1), ((1, 4), 1), ((0, 5), -1), ((1, 5), -1),
                         ((2, 6), 1), ((3, 6), -1), ((2, 7), -1), ((3, 7), 1)):
        n[INDEX[label]] = value
    N = sp.Matrix.hstack(stars, n)
    hN = N.extract(g['h'], range(5))
    nu = N.rank()
    a, b = nu-(N-hN).rank(), nu-(N+hN).rank()
    cs, gains, rhos = [], [], []
    for center in (2, 0):
        new = [INDEX[c, y] for c in (center, center+1) for y in range(4, 14)]
        cs.append(nu-N.extract(new, range(5)).rank()-1)
        C = sp.Matrix(10, 44, lambda y, i:
                      int(LABELS[i] in ((center, y+4), (center+1, y+4))))
        rhos.append((C*N).rank())
        gains.append(11+cs[-1]-nu+rhos[-1])
    result = defect_budget(nu, *cs, *gains, a, b)
    assert cs == [1, 1] and gains == [8, 9] and (a, b) == (2, 2)
    result.update(scope='Abstract kernel subspace, not a graph or a Conway border.',
                  even_sum_projection_ranks=rhos)
    return result


PROOF = [
    'Let V+ and V- be the eigenspaces of h=(01)(23) on the44 labels. Each has dimension22. The two forced odd star differences u0,u1 are orthogonal with squared norm24. For the normalized orbit lift F/sqrt(2), let W=F^t[u0,u1]/2. Then W^tW=12I, K-=WW^t/4 and L-=WW^t/3. C1 gives Gamma*u0=Gamma*u1=0.',
    'On the20-dimensional orthogonal complement of W inside V-, T-=3I-Gamma- and U-=4I+Gamma-. Here Gamma-=F^t Gamma F/2, whether or not Gamma commutes with h. Under full T PSD, the kernel of this compression lifts to kerT. Thus the multiplicity of eigenvalue3 of Gamma- equals b-2, where b=dim(kerT intersect V-). Both PSD conditions allow eigenvalues in[-4,3]; positivity does not make the upper endpoint strict. When Gamma commutes with h, Gamma- is an integer signed quotient with entries Gamma(rep_i,rep_j)-Gamma(rep_i,h(rep_j)).',
    'The old two-star kernel is generated by its c component indicators and the one star difference. Every component of the weighted network is closed under the star flip F and outer mate M. On the overlap h acts as FM and elsewhere as F, so each component indicator is h-even. The difference is h-odd. Therefore the old kernel has even/odd dimensions(c,1), even without assuming full h symmetry.',
    'Put N=kerT, nu=dimN, a=dim(N intersect V+), b=dim(N intersect V-), and s=nu-a-b. Then dim(N+hN)=nu+s. For the new side, let C_m sum the two coordinates2y,3y and rho=rank(C_m N). Set K_m=N intersect kerC_m. It has dimension nu-rho and contains the direct sum of the b pure odd relations and c_l old pure even relations. The quotient has dimension eta_l=nu-rho-b-c_l.',
    'The map K_m/(pure odd N + old pure even N) into N/(pure even N + pure odd N) is injective: if the class is pure-even-plus-pure-odd, its even part has zero new coordinates, hence belongs to the old even kernel. Consequently0<=eta_l<=s. Combining with the exact projection formula gives d_l=9-gain_odd_l=b-2+eta_l. A right-side formula holds similarly. If N is h-invariant, s=0 and both gains equal11-b; full adjacency symmetry is sufficient but not necessary.',
    'With no symmetry assumption, the residual rank gain after adding the odd vectors is e_l=(44-nu)-(23-c_l)-(9-d_l)=12+c_l-nu+d_l. A separately proved bound e_l>=k gives nu<=12+c_l+d_l-k. It is invalid to drop d_l after ODD9 has been refuted. No claim is made that an earlier conditional lemma supplies k in a new setting.',
    'For the producer h-invariant nullity14 cases with gains8/8, b=3,a=11 and e_l=c_l-1,e_m=c_m-1. Within this class, min(c_l,c_m)>=2 is equivalent to both residual even increments being at least1. This is a reformulation, not a proof of the component bound. The producer nullity9 case with gains5/5 has b=6,a=3.',
    'Any supplied pure h-odd extra relation can be made orthogonal to u0,u1 by subtracting their projections. Its root-letter incidence is then zero, so Gamma*n=3n. After clearing denominators, it cannot have odd coordinates at every exterior vertex. Indeed C1 gives e(O,F)=16-4e(O)<=16, leaving at least24 exterior vertices with no O neighbour. At such a vertex, an all-odd exterior vector would give an even Gamma*n but an odd3n. This strengthens the earlier parity obstruction by removing the condition n|O=0.',
    'The default abstract fixture has nu5, a=b=2,s=1,c_l=c_m=1, gains8/9 and eta_l=1,eta_m=0. It demonstrates that the mixed-parity term is necessary in the linear-algebra formula. It is not a graph and does not establish realizability under C1/C2 geometry.'
]


def report():
    g = geometry()
    F, W = g['F'], g['W']
    assert F.T*F == 2*sp.eye(22)
    assert W.T*W == 12*sp.eye(2)
    assert F.T*g['K']*F/2 == W*W.T/4
    assert F.T*g['L']*F/2 == W*W.T/3
    assert g['B']*F*(sp.eye(22)-W*W.T/12) == sp.zeros(14, 22)
    types = ((2, 2), (3, 2), (4, 2), (5, 2), (2, 3),
             (3, 3), (4, 3), (2, 4), (3, 4))
    return dict(status='UNIVERSAL_ODD9_REFUTED_CORRECTED_DEFECT_IDENTITIES',
                counterexample_provenance='LAB message843 exact producer results accepted without re-verification.',
                geometric_projector_identities='EXACT_PASS',
                odd_quotient_representatives=[LABELS[i] for i in g['reps']],
                forced_odd_vectors=W.tolist(),
                producer_nullity14_budgets=[defect_budget(14, c, d, 8, 8, 11, 3) for c, d in types],
                producer_nullity9_budget=defect_budget(9, 2, 2, 5, 5, 3, 6),
                abstract_mixed_fixture=abstract_mixed_fixture(g), proof=PROOF)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--odd-relations', type=Path,
                        help='JSON with relations as a list of44-entry vectors; optional labels.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.odd_relations:
        source = json.loads(args.odd_relations.read_text(encoding='utf-8-sig'))
        result = dict(profiles=[normalize_odd_relation(n, source.get('labels', LABELS))
                                for n in source['relations']])
    else:
        result = report()
    encoded = json.dumps(result, indent=2, default=lambda x: int(x) if x.is_Integer else str(x))
    if args.output:
        args.output.write_text(encoded+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('proof', 'forced_odd_vectors', 'odd_quotient_representatives',
                      'producer_nullity14_budgets')}, indent=2,
                     default=lambda x: int(x) if x.is_Integer else str(x)))


if __name__ == '__main__':
    main()
