"""Classify flat incidence-zero C4DO violations of support at most twelve.

The 832 generated objects are twelve-label SUPPORT CORES, not complete
four-star blocks. Exact positive Gram matrices on these cores do not
certify a 44-label extension. No producer graph is read.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_doubly_odd_kernel import INDEX, prism_options


def partial_matchings(vertices):
    if not vertices:
        yield []
        return
    first, *tail = vertices
    yield from partial_matchings(tail)
    for second in tail:
        for rest in partial_matchings([x for x in tail if x != second]):
            yield [(first, second)]+rest


def embed(pairs):
    mapping, letter = {}, 4
    for first, second in pairs:
        mapping[first], mapping[second] = letter, letter+1
        letter += 2
    for vertex in range(5):
        if vertex not in mapping:
            mapping[vertex] = letter
            letter += 2
    return [mapping[i] for i in range(5)]


def exact_psd(matrix):
    """Exact rational symmetric elimination; also count the positive pivots."""
    a = [[Fraction(int(x)) for x in row] for row in matrix]
    pivots = []
    for i in range(len(a)):
        pivot = a[i][i]
        if pivot < 0 or (pivot == 0 and any(a[i][j] for j in range(i+1, len(a)))):
            return dict(psd=False, failed_index=i)
        if pivot == 0:
            continue
        pivots.append(str(pivot))
        for j in range(i+1, len(a)):
            for k in range(j, len(a)):
                value = a[j][k]-a[j][i]*a[i][k]/pivot
                a[j][k] = a[k][j] = value
    return dict(psd=True, rank=len(pivots), positive_pivots=pivots)


PROOF = [
    "Assume Gamma is binary and its pairs have at most one common neighbour when adjacent and at most two otherwise (the actual C2 caps are stronger). Let q have entries0,+1,-1, satisfy Bq=0 and Tq=0. Then Gamma*q=3*q because K*q=0. Both signs occur, and every positive vertex has at least three positive neighbours; similarly for the negative vertices.",
    "A graph on at most six vertices with those common-neighbour caps and minimum degree three must be a triangular prism on six vertices. A degree-five vertex is impossible because its neighbours have degree at most two. For degree four on six vertices, each of its four neighbours must meet the sole non-neighbour, producing four common neighbours for a nonadjacent pair. Hence the graph is cubic. On fewer than six vertices this is impossible. On six vertices, the three neighbours of a vertex must contain an edge (otherwise the two remaining vertices have three common neighbours); the remaining edges then force the triangular prism.",
    "Consequently support at most twelve forces six positive and six negative vertices, each sign inducing a prism. Each vertex already has exactly three same-sign neighbours, so Gamma*q=3*q forbids edges between the two prisms.",
    "Inside a prism, triangle edges already have one common prism neighbour and nonadjacent pairs already have two. Thus a root letter can be shared only by the two endpoints of a vertical matching edge. Each root occurs at most twice and each prism vertex has at most one repeated root letter.",
    "Let o be the number of overlap labels in one prism. Its central-letter incidence sum is6+o, and every one of the four central roots occurs at most twice, so o<=2. If o=2, every central root occurs twice, and an overlap label would have two repeated roots, impossible. Hence o<=1. Bq=0 gives the same root multiplicities for both prisms and hence the same o. A nonzero overlap double difference requires o=1 for each sign, with different overlap labels.",
    "The central multiplicities are then(1,2,2,2). Both overlap labels meet the unique multiplicity-one central root. By a central mate-preserving permutation and sign reversal normalize them to positive02 and negative03. The three other central roots close all three vertical edges in both prisms. No exterior root can repeat within a prism, so exactly five exterior letters a,b,c,d,e occur, once in each sign.",
    "Normalize the positive labels to(02,2a,1b,1c,3d,3e). Disjointness of the signs leaves two negative forms up to permutations within the positive pairs: (03,3a,1d,1e,2b,2c), or(03,3b,1a,1d,2c,2e). These exhaust whether the negative singleton at3 uses a or one of b,c. It cannot use d or e.",
    "The mate involution restricted to these five exterior letters is a partial matching:1 empty,10 one-edge,15 two-edge choices. Every such partial matching extends to the ten exterior roots. This gives2*26=52 covering support types; they are not asserted pairwise nonisomorphic. Each prism has four choices of its two triangles with the fixed vertical matching, giving16 orientations per support, or832 labelled core representatives.",
    "Only the twelve-label principal T and U matrices and the local incidence/common-neighbour capacities are imposed here. Their positivity does not supply the missing32 labels, the complete star equalities on44 labels, the full Gram ranks or a Conway graph. This classification does not cover general integer kernel coefficients, nonzero incidence Bq, or support larger than twelve.",
]


def run():
    start = time.monotonic()
    patterns = list(partial_matchings(list(range(5))))
    assert len(patterns) == 26
    assert Counter(map(len, patterns)) == {0: 1, 1: 10, 2: 15}
    records, summary, representative = [], Counter(), None
    local_edges = list(combinations(range(6), 2))
    for matching in patterns:
        a, b, c, d, e = embed(matching)
        positive = [(0, 2), (2, a), (1, b), (1, c), (3, d), (3, e)]
        negatives = [
            [(0, 3), (3, a), (1, d), (1, e), (2, b), (2, c)],
            [(0, 3), (3, b), (1, a), (1, d), (2, c), (2, e)],
        ]
        for kind, negative in enumerate(negatives):
            labels = positive+negative
            assert len(set(labels)) == 12
            q = np.array([1]*6+[-1]*6, dtype=np.int64)
            B = np.array([[int(root in p) for p in labels] for root in range(14)], dtype=np.int64)
            assert not np.any(B@q)
            options = [prism_options([INDEX[p] for p in part]) for part in (positive, negative)]
            assert [len(x) for x in options] == [4, 4]
            K8 = np.array([[3*len(set(p) & set(r))+sum((x ^ 1) in r for x in p)-2
                            for r in labels] for p in labels], dtype=np.int64)
            U0 = np.array([[60*int(i == j)-4*len(set(p) & set(r))+sum((x ^ 1) in r for x in p)-2
                            for j, r in enumerate(labels)] for i, p in enumerate(labels)], dtype=np.int64)
            ranks = Counter()
            for left_index, right_index in product(range(4), repeat=2):
                G = np.zeros((12, 12), dtype=np.int64)
                for offset, row in ((0, options[0][left_index]), (6, options[1][right_index])):
                    for value, (i, j) in zip(row, local_edges):
                        G[offset+i, offset+j] = G[offset+j, offset+i] = value
                assert np.array_equal(G@q, 3*q)
                square = G@G
                assert all(square[i, j] <= 2-G[i, j]-len(set(labels[i]) & set(labels[j]))
                           for i, j in combinations(range(12), 2))
                assert all(sum(G[i, j] for j, r in enumerate(labels) if root in r)
                           <= 2-int(root in p)-int((root ^ 1) in p)
                           for i, p in enumerate(labels) for root in range(14))
                T8 = 24*np.eye(12, dtype=np.int64)-8*G-K8
                U15 = U0+15*G
                tc, uc = exact_psd(T8), exact_psd(U15)
                assert tc['psd'] and uc['psd']
                assert not np.any(T8@q)
                ranks[tc['rank'], uc['rank']] += 1
                summary[len(matching), kind, tc['rank'], uc['rank']] += 1
                if representative is None:
                    representative = dict(labels=labels, edges=[[i, j] for i, j in combinations(range(12), 2) if G[i, j]],
                                          q=q.tolist(), overlap_double_difference=2,
                                          T8=T8.tolist(), U15=U15.tolist(), T_certificate=tc, U_certificate=uc)
            records.append(dict(partial_mate_matching=matching, kind=kind,
                                exterior_letters=[a, b, c, d, e], positive=positive, negative=negative,
                                rank_histogram=[dict(T_rank=t, U_rank=u, count=n) for (t, u), n in ranks.items()]))
    return dict(status='EXACT_FLAT_SUPPORT_TWELVE_CORE_CLASSIFICATION',
                support_types=52, cores=832, all_core_T_U_psd=True,
                proof=PROOF, records=records, representative=representative,
                summary=[dict(mate_pairs=p, kind=k, T_rank=t, U_rank=u, count=n)
                         for (p, k, t, u), n in summary.items()], seconds=time.monotonic()-start,
                scope='Twelve-label support cores only; no44-label extension and no general C4DO, ODDCONST or N9-NG proof.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = run()
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('proof', 'records', 'representative')}, indent=2))
