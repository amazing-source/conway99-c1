"""Exclude overlap support in flat incidence-zero kernel relations of size <=14.

The proof is combinatorial for support14 and uses the already proved spectral
prism obstruction for support12. No graph from a peer or solver is read.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_flat_c4do_obstruction import certificate as prism_certificate


PROOF = [
    "Use the same binary44-label C1/C2 and T/U PSD hypotheses as the support12 theorem. Let q have entries0,+1,-1, Bq=0 and Tq=0. Summing Bq gives sum(q)=0, so the two signs have equal size m. Also Kq=0, hence Gamma*q=3*q, and each sign induces a graph H of minimum degree at least3.",
    "For a vertex v of degree d in such an H on m vertices, H[N(v)] is a matching: an adjacent pair has at most one common neighbour. Every vertex of N(v) must have at least one neighbour outside N[v]. Each of the m-1-d nonneighbours of v meets N(v) in at most two vertices. Therefore d<=2(m-1-d), or d<=floor(2(m-1)/3). This immediately excludes m<=5 and forces cubic degree at m=6.",
    "For m=7 the maximum degree is4, and some vertex has degree4 because a cubic graph cannot have odd order. Write its neighbours as a,b,c,d and its two nonneighbours as e,f. The previous inequality is equality: N(v) is a perfect matching, each of its four vertices has one neighbour among e,f, and e,f each meet exactly two neighbours of v. Their minimum degree3 forces ef. Normalize the matching to ab,cd. Since ab already has common neighbour v, e cannot meet both a,b; similarly for cd. Thus e meets a,c and f meets b,d after renaming. This uniquely specifies H7.",
    "Its edges are va,vb,vc,vd,ab,cd,ea,ec,fb,fd,ef. Every vertex except v has degree3, and v has degree4. For a flat relation on fourteen vertices, Gamma*q=3*q therefore forces exactly one edge between the signs: the edge between their two distinguished degree4 vertices.",
    "Two vertices of one sign may share a root letter only if their number of common H-neighbours is at most1 minus their adjacency. For H7 the permitted pairs are ea,ec,fb,fd,ef,ad,bc; v has none. This compatibility graph is triangle-free. Consequently each root occurs at most twice in the sign, and every root on the label of v occurs only once.",
    "Every one of the seven labels contains a central root from{0,1,2,3}; labels in O={02,03,12,13} contain two. Thus the total central incidence is7+o, where o is the number of labels in O. If the distinguished label v were in O, two central roots would have multiplicity1 and the other two at most2, giving at most6 incidences, impossible. Otherwise one central root has multiplicity1 and the other three at most2, giving at most7 incidences. Therefore o=0. This conclusion is separate for each sign, and uses only the C2 caps once Gamma*q=3*q is known.",
    "At m=6 the previous prism classification shows that a sign contains at most one overlap label. If either sign meets O, incidence equality Bq=0 forces both to do so; their overlap labels share the same unique central root of multiplicity1. They are distinct because the signs are disjoint, so the overlap double difference is plus or minus2. The proved support12 spectral obstruction excludes this possibility. Thus q vanishes on all of O also at m=6.",
    "Conclusion: every flat incidence-zero vector in ker T supported on at most14 labels vanishes on all four overlap coordinates, which in particular proves C4DO on this class. Any flat incidence-zero kernel relation touching O, even one satisfying C4DO, has support at least16. This does not constrain nonflat coefficients or nonzero incidence, and does not prove SYM, general C4DO, N9-NG, NG5 or NG7.",
]


def adjacency(n, edges):
    rows = [set() for _ in range(n)]
    for a, b in edges:
        rows[a].add(b)
        rows[b].add(a)
    return rows


def common_cap_ok(rows):
    return all(len(rows[a] & rows[b]) <= 2-int(b in rows[a])
               for a, b in combinations(range(len(rows)), 2))


def root_compatibility(rows):
    return [(a, b) for a, b in combinations(range(len(rows)), 2)
            if len(rows[a] & rows[b]) <= 1-int(b in rows[a])]


def run():
    # Normalization: v=0; a,b,c,d=1,2,3,4; e,f=5,6.
    fixed = [(0, x) for x in range(1, 5)]+[(1, 2), (3, 4), (5, 6)]
    accepted, rejected = [], []
    for neighbours_e in combinations(range(1, 5), 2):
        neighbours_f = sorted(set(range(1, 5))-set(neighbours_e))
        edges = fixed+[(5, x) for x in neighbours_e]+[(6, x) for x in neighbours_f]
        rows = adjacency(7, edges)
        if not common_cap_ok(rows):
            rejected.append(list(neighbours_e))
            continue
        assert sorted(map(len, rows)) == [3]*6+[4]
        permitted = root_compatibility(rows)
        compatible = adjacency(7, permitted)
        assert not compatible[0]
        assert not any(c in compatible[a] and c in compatible[b]
                       for a, b in permitted for c in range(7))
        assert len(permitted) == 7
        accepted.append(dict(neighbours_e=list(neighbours_e),
                             edges=sorted([sorted(edge) for edge in edges]),
                             shared_root_permitted_pairs=permitted))
    assert len(accepted) == 4 and len(rejected) == 2
    representative = next(row for row in accepted if row['neighbours_e'] == [1, 3])
    assert representative['neighbours_e'] == [1, 3]
    assert set(map(tuple, representative['shared_root_permitted_pairs'])) == {
        (1, 4), (1, 5), (2, 3), (2, 6), (3, 5), (4, 6), (5, 6)}
    joined = representative['edges']+[[a+7, b+7] for a, b in representative['edges']]+[[0, 7]]
    rows = adjacency(14, joined)
    q = [1]*7+[-1]*7
    assert all(sum(q[j] for j in rows[i]) == 3*q[i] for i in range(14))
    assert common_cap_ok(rows)
    base = prism_certificate()
    return dict(
        status='PROVED_FLAT_INCIDENCE_ZERO_KERNEL_VANISHES_ON_OVERLAP_SUPPORT_AT_MOST_FOURTEEN',
        conclusion='q(02)=q(03)=q(12)=q(13)=0',
        corollary='A flat incidence-zero kernel relation touching O has support at least16.',
        proof=PROOF,
        seven_vertex_normalized_cases=dict(considered=6, admissible=4,
            rejected_neighbours_e=rejected, representative=representative,
            all_admissible_have_isolated_distinguished_vertex_in_root_compatibility=True,
            all_admissible_root_compatibility_graphs_triangle_free=True),
        unlabelled_signed_fourteen_core=dict(edges=joined, q=q,
            degree_histogram=dict(Counter(map(len, rows))),
            scope='Unlabelled combinatorial core only; no root labelling or44-label extension asserted.'),
        support_twelve_obstruction=base['cases'],
        hypotheses=base['hypotheses'][:-1]+['support(q)<=14'],
        scope='No general C4DO or SYM theorem, no N9-NG/NG5/NG7 exclusion, no new SRG.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = run()
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'conclusion', 'corollary', 'scope')}, indent=2))
