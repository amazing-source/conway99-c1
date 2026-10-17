"""Keep a certified adjacency fixed and enumerate all945 outer mate choices.

This is a new finite family of labelled geometries, not an audit of the
producer graph. C1, C2, binary adjacency and the odd T/U blocks are
inherited from the producer. Only the changed C1-prime constraints and
even T/U blocks are tested. Counts are mate assignments, not isomorphism
classes or new SRGs. The source also supplies its certified odd kernel.
"""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
import json
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from odd9_defect_decomposition import LABELS, normalize_odd_relation
except ImportError:
    from codex_odd9_defect_decomposition import LABELS, normalize_odd_relation

INDEX = {p: i for i, p in enumerate(LABELS)}


def graph(data):
    labels = [tuple(x) for x in data['labels']]
    G = np.zeros((44, 44), dtype=np.int64)
    for i, j in data['edges']:
        G[i, j] = G[j, i] = 1
    order = [labels.index(p) for p in LABELS]
    return G[np.ix_(order, order)]


def exact_psd(matrix):
    """Fraction-free symmetric elimination; positive pivots preserve PSD.

    The current matrix is a positive multiple of a Schur complement.
    A negative diagonal or a nonzero row at zero diagonal rejects PSD.
    Bareiss division keeps all entries integral. No eigenvalue tolerance.
    """
    A = [[int(x) for x in row] for row in matrix]
    previous, rank = 1, 0
    while A:
        if any(A[i][i] < 0 for i in range(len(A))):
            return False, rank, 'NEGATIVE_SCHUR_DIAGONAL'
        if any(A[i][i] == 0 and any(A[i]) for i in range(len(A))):
            return False, rank, 'ZERO_DIAGONAL_NONZERO_ROW'
        pivot = next((i for i in range(len(A)) if A[i][i]), None)
        if pivot is None:
            return True, rank, 'ZERO_SCHUR_COMPLEMENT'
        keep = [i for i in range(len(A)) if i != pivot]
        value = A[pivot][pivot]
        reduced = []
        for i in keep:
            row = []
            for j in keep:
                numerator = value*A[i][j]-A[i][pivot]*A[pivot][j]
                quotient, remainder = divmod(numerator, previous)
                assert not remainder
                row.append(quotient)
            reduced.append(row)
        A, previous, rank = reduced, value, rank+1
    return True, rank, 'FULL_POSITIVE_RANK'


def matchings(left):
    if not left:
        yield []
        return
    x = left[0]
    for y in left[1:]:
        for tail in matchings([z for z in left if z not in (x, y)]):
            yield [(x, y)]+tail


def components(G, mate, central):
    labels = [p for p in LABELS if central in p or central+1 in p]
    parent = list(range(24))
    lookup = {p: i for i, p in enumerate(labels)}

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def join(i, j):
        parent[root(i)] = root(j)

    for i, p in enumerate(labels):
        c = next(x for x in p if x in (central, central+1))
        y = next(x for x in p if x != c)
        join(i, lookup[tuple(sorted((c ^ 1, y)))])
        join(i, lookup[tuple(sorted((c, mate[y])))])
        for j in range(i):
            if G[INDEX[p], INDEX[labels[j]]]:
                join(i, j)
    return len({root(i) for i in range(24)})


def coefficient_profiles(source):
    cases = []
    for name, data in source.items():
        normalized = [normalize_odd_relation(n, data['labels'])
                      for n in data['odd_kernel_basis_label_coordinates']]
        distinct = {tuple(p['primitive_vector']): p for p in normalized
                    if 'primitive_vector' in p}
        for p in distinct.values():
            n = p['primitive_vector']
            p['outer_rows_by_star'] = [[n[INDEX[c, y]] for y in range(4, 14)] for c in range(4)]
        cases.append(dict(name=name, producer_certificates=data['certificates'],
                          normalized_extra_relations=list(distinct.values())))
    comparisons = []
    if len(cases) == 2 and all(len(c['normalized_extra_relations']) == 1 for c in cases):
        rows = [c['normalized_extra_relations'][0]['outer_rows_by_star'] for c in cases]
        G, H = [graph(source[c['name']]) for c in cases]
        options = [[j+4 for j in range(10) if (rows[0][0][y], rows[0][2][y])
                    == (rows[1][0][j], rows[1][2][j])] for y in range(10)]
        for choice in product(*options):
            if len(set(choice)) != 10:
                continue
            perm = dict(enumerate(range(4))) | {i+4: x for i, x in enumerate(choice)}
            mapped = [INDEX[tuple(sorted(perm[x] for x in p))] for p in LABELS]
            comparisons.append(dict(outer_permutation_to_second=choice,
                full_adjacency_difference_nonzeros=int(np.count_nonzero(G-H[np.ix_(mapped, mapped)])),
                preserves_outer_mates=all(perm[y ^ 1] == (perm[y] ^ 1) for y in range(4, 14))))
    return dict(scope='New coefficient statistics and explicit alignments, no producer rank/PSD/kernel audit.',
                cases=cases, relation_aligned_quotient_comparisons=comparisons)


def enumerate_mates(data):
    G = graph(data)
    B = np.array([[int(a in p) for p in LABELS] for a in range(14)], dtype=np.int64)
    h = [INDEX[tuple(sorted(x ^ 1 if x < 4 else x for x in p))] for p in LABELS]
    reps = [i for i in range(44) if i < h[i]]
    F = np.zeros((44, 22), dtype=np.int64)
    for j, i in enumerate(reps):
        F[i, j] = F[h[i], j] = 1
    BP = B@F
    gram = BP.T@BP
    assert not np.any(gram % 2)
    gp = F.T@G@F//2
    I, J = np.eye(22, dtype=np.int64), np.ones((22, 22), dtype=np.int64)
    T0 = 24*I-8*gp-3*(gram//2)+4*J
    U0 = 60*I+15*gp-2*gram-4*J
    star_counts = G@B.T
    allowed = {(y, z) for y in range(4, 14) for z in range(y+1, 14)
               if all(star_counts[i, z] <= 1 for i, p in enumerate(LABELS) if y in p)
               and all(star_counts[i, y] <= 1 for i, p in enumerate(LABELS) if z in p)}
    histogram, verdicts, accepted = Counter(), [], []
    for number, matching in enumerate(matchings(list(range(4, 14)))):
        if any(pair not in allowed for pair in matching):
            histogram['C1prime_rejected'] += 1
            verdicts.append('C1prime')
            continue
        mate = [1, 0, 3, 2]+list(range(4, 14))
        for a, b in matching:
            mate[a], mate[b] = b, a
        correction = BP.T@BP[mate]
        assert not np.any(correction % 2)
        correction //= 2
        t = exact_psd(T0-correction)
        if not t[0]:
            histogram['T_even_rejected'] += 1
            verdicts.append('T:'+t[2])
            continue
        u = exact_psd(U0+correction)
        if not u[0]:
            histogram['U_even_rejected'] += 1
            verdicts.append('U:'+u[2])
            continue
        c = [components(G, mate, central) for central in (0, 2)]
        nu = data['odd_kernel_dim_exact']+22-t[1]
        accepted.append(dict(matching_id=number, outer_mates=matching,
                             T_even_rank=t[1], U_even_rank=u[1],
                             nullity_T=nu, components=c))
        histogram['accepted'] += 1
        verdicts.append('PSD')
    assert len(verdicts) == 945
    O = [i for i, p in enumerate(LABELS) if p[1] < 4]
    outer = [i for i in range(44) if i not in O]
    edge_frequencies = Counter(tuple(pair) for x in accepted for pair in x['outer_mates'])
    mate_union = {y: set() for y in range(4, 14)}
    for y, z in edge_frequencies:
        mate_union[y].add(z)
        mate_union[z].add(y)
    colors, todo, bipartite = {4: 0}, [4], True
    while todo:
        y = todo.pop()
        for z in mate_union[y]:
            if z not in colors:
                colors[z] = 1-colors[y]
                todo.append(z)
            elif colors[z] == colors[y]:
                bipartite = False
    partition_witness = None
    if (bipartite and len(colors) == 10 and len(edge_frequencies) == 25
            and all(len(a) == 5 for a in mate_union.values()) and len(accepted) == 120):
        positive = sorted(y for y in colors if colors[y] == 0)
        negative = sorted(y for y in colors if colors[y] == 1)
        q = np.array([0 if p[1] < 4 else (1 if p[1] in positive else -1)
                      for p in LABELS], dtype=np.int64)
        # A new equitable vector of the fixed adjacency, not a recheck
        # of any supplied T-kernel or PSD certificate.
        assert np.array_equal(G@q, 2*q) and int(q@q) == 40
        assert all(v == 24 for v in edge_frequencies.values())
        partition_witness = dict(positive_outer_letters=positive, negative_outer_letters=negative,
            vector_labels=LABELS, vector=[int(x) for x in q], fixed_adjacency_eigenvalue=2,
            exact_energy='q^t*T(M)*q=-8 times the number of mate pairs lying within a part',
            consequence='T PSD forces every mate pair across the two five-element parts; exactly5!=120 choices.',
            sufficient='All120 cross matchings have exact PSD even blocks, as recorded by this enumeration.')
    return dict(total_outer_matchings=945, compatible_mate_pairs=len(allowed),
                forbidden_mate_pairs=[(y, z) for y in range(4, 14) for z in range(y+1, 14)
                                      if (y, z) not in allowed],
                counts=dict(histogram),
                accepted_nullity_histogram=dict(Counter(x['nullity_T'] for x in accepted)),
                accepted_component_histogram={str(k): v for k, v in sorted(Counter(
                    tuple(x['components']) for x in accepted).items())},
                overlap_edges=int(G[np.ix_(O, O)].sum())//2,
                overlap_outer_edges=int(G[np.ix_(O, outer)].sum()),
                accepted_even_rank_histogram={str(k): v for k, v in sorted(Counter(
                    (x['T_even_rank'], x['U_even_rank']) for x in accepted).items())},
                partition_witness=partition_witness,
                accepted=accepted, verdicts_in_matching_generator_order=verdicts)


PROOF = [
    'Only the perfect matching M on the ten exterior root letters changes. The adjacency Gamma and all incidence labels stay fixed. Binary adjacency, C1 central counts and C2 common-neighbour bounds are inherited from the certified producer; C2 depends on label intersection, not M. An exterior pair(y,z) is an allowed new mate exactly when each of the four rows containing y has at most one Gamma neighbour in exterior star z, and conversely. All other C1-prime inequalities are inherited. Thus admissible rematings are exactly the perfect matchings in this compatibility graph.',
    'The pure h-odd geometry K-,L- depends only on the two forced star differences, not on the exterior matching. The odd T/U blocks and their ranks are therefore inherited unchanged. For the even orbit lift F with columns e_i+e_hi, set Bp=BF. The integer blocks are8T+=24I-8Gamma+-(3Bp^tBp+Bp^tMBp)/2+4J and15U+=60I+15Gamma+-(4Bp^tBp-Bp^tMBp)/2-4J. These are the only positivity calculations needed for a new M.',
    'Every matching on ten letters is generated once by pairing the smallest remaining letter recursively; there are945. Compatible cases undergo fraction-free symmetric Schur elimination on the changed22-dimensional even blocks. Positive pivots and zero final Schur complement certify PSD and rank; a negative diagonal or a nonzero row at zero diagonal certifies non-PSD. Exact Bareiss division is asserted at every update. No floating-point classification is used in this report.',
    'Counts refer to labelled mate choices for ONE fixed44-vertex partial adjacency. They are not counts of nonisomorphic graphs or complete SRGs. For this source the overlap grid has no exterior edges, so the two-star weighted networks always contain its component and at least one exterior component: min c>=2 is automatic in this particular family, regardless of PSD. Hence this experiment cannot settle B-prime in the non-grid setting.',
    'A stronger necessity certificate explains the census. Let t be+1 on{4,7,8,11,12} and-1 on{5,6,9,10,13}; lift q(c,y)=t_y and q|O=0. The fixed adjacency satisfies Gamma*q=2q, and q has squared norm40. Its incidence is0 on the central letters and4t on the exterior letters. Therefore q^t*K(M)*q=60+2t^tMt, and q^t*T(M)*q=-20-2t^tMt=-8r, where r is the number of mate pairs within a part. Positivity forces r=0. The120 remaining cross matchings have been certified exactly by the even-block elimination, proving necessity and sufficiency within this fixed-adjacency family.'
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--coefficient-output', type=Path)
    args = parser.parse_args()
    source = json.loads(args.input.read_text(encoding='utf-8-sig'))
    # Small algebraic fixtures for this new exact elimination, not peer objects.
    assert exact_psd([[1, 2], [2, 4]])[:2] == (True, 1)
    assert not exact_psd([[0, 1], [1, 0]])[0]
    assert not exact_psd([[1, 2], [2, 3]])[0]
    own = np.array([[1, 2, 3], [2, -1, 4], [3, 1, 7], [0, 1, -1]])
    assert exact_psd(own@own.T)[:2] == (True, 3)
    name, data = next(iter(source.items()))
    start = time.perf_counter()
    result = enumerate_mates(data)
    result.update(status='EXACT_FINITE_REMATING_FAMILY', source=str(args.input.resolve()),
                  fixed_adjacency_source=name, seconds=time.perf_counter()-start,
                  producer_certificates_accepted=data['certificates'], proof=PROOF)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    if args.coefficient_output:
        profiles = coefficient_profiles(source)
        profiles['source'] = str(args.input.resolve())
        args.coefficient_output.write_text(json.dumps(profiles, indent=2)+'\n', encoding='utf-8')
    summary = {k: v for k, v in result.items() if k not in
               ('accepted', 'verdicts_in_matching_generator_order', 'proof')}
    if summary['partition_witness']:
        summary['partition_witness'] = {k: v for k, v in summary['partition_witness'].items()
                                        if k not in ('vector', 'vector_labels')}
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
