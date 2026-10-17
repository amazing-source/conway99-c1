"""Character spaces and necessary rank targets for the local G1 family.

No graph sample is read. The 44 labels form eleven regular Klein-four
orbits. The accepted two-star theorem gives a lower bound on the trivial
block rank, hence necessary nullity targets for the other three blocks.
"""
from itertools import product
from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_profile_join import LABELS

INDEX = {p:i for i, p in enumerate(LABELS)}


def action(label, first, second):
    out = []
    for x in label:
        if (x < 2 and first) or (2 <= x < 4 and second) or (x >= 4 and first != second):
            x ^= 1
        out.append(x)
    return tuple(sorted(out))


def character_bases():
    unused, orbits = set(range(44)), []
    elements = tuple(product((0, 1), repeat=2))
    while unused:
        root = min(unused)
        orbit = [INDEX[action(LABELS[root], a, b)] for a, b in elements]
        assert len(set(orbit)) == 4
        unused.difference_update(orbit)
        orbits.append(orbit)
    matrices = {}
    for chi in elements:
        matrix = [[0]*11 for _ in range(44)]
        for j, orbit in enumerate(orbits):
            for i, (a, b) in zip(orbit, elements):
                matrix[i][j] = (-1)**(chi[0]*a+chi[1]*b)
        matrices['%d%d'%chi] = matrix
    return orbits, matrices


def nullity_targets(c_left, c_right):
    # The trivial six-dimensional two-star block has nullity c, and
    # therefore rank6-c. It is a principal block of the full trivial11.
    trivial_rank_lower = 6-min(c_left, c_right)
    nontrivial_nullity_lower = 33-(30-trivial_rank_lower)
    additional = max(0, nontrivial_nullity_lower-2)  # two forced odd stars
    thresholds = [(1+a, 1+b, additional-a-b)
                  for a in range(additional+1) for b in range(additional-a+1)]
    return dict(c_left=c_left, c_right=c_right,
                trivial_block_rank_at_least=trivial_rank_lower,
                nontrivial_blocks_total_nullity_at_least=nontrivial_nullity_lower,
                additional_nontrivial_relations_at_least=additional,
                character_order=['10', '01', '11'],
                minimal_nullity_thresholds=thresholds,
                minimal_rank_upper_bounds=[tuple(11-k for k in row) for row in thresholds],
                scope='Necessary for a G1-invariant local four-star matrix with rank(T)<=30; no symmetry imposed on a full completion.')


def report():
    orbits, matrices = character_bases()
    columns = [(chi, j, [row[j] for row in matrix])
               for chi, matrix in matrices.items() for j in range(11)]
    for i, (_, _, col) in enumerate(columns):
        for j, (_, _, other) in enumerate(columns):
            assert sum(x*y for x, y in zip(col, other)) == 4*int(i == j)
    # Check the transformation type of the known star relations, without
    # reading a graph or recomputing any producer rank.
    stars = [[int(c in p) for p in LABELS] for c in range(4)]
    modes = {'00':[[x+y for x, y in zip(stars[0], stars[1])],
                  [x+y for x, y in zip(stars[2], stars[3])]],
             '10':[[x-y for x, y in zip(stars[0], stars[1])]],
             '01':[[x-y for x, y in zip(stars[2], stars[3])]]}
    for chi, vectors in modes.items():
        for vector in vectors:
            for other, _, col in columns:
                if chi != other:
                    assert sum(x*y for x, y in zip(vector, col)) == 0
    for centre in (0, 2):
        two = {i for i, p in enumerate(LABELS) if set(p) & {centre, centre+1}}
        assert sum(set(orbit) <= two for orbit in orbits) == 6
        assert all(not (set(orbit) & two) or set(orbit) <= two for orbit in orbits)
    target = nullity_targets(4, 4)
    assert target['additional_nontrivial_relations_at_least'] == 3
    assert len(target['minimal_nullity_thresholds']) == 10
    return dict(status='EXACT_CHARACTER_GEOMETRY_AND_NECESSARY_TARGETS',
                labels=LABELS, group_elements_in_orbit_order=list(product((0,1), repeat=2)),
                regular_orbits=orbits, character_bases=matrices,
                character_dimensions={'00':11,'10':11,'01':11,'11':11},
                forced_star_nullities={'00':2,'10':1,'01':1,'11':0},
                c44_target=target,
                proof='The trivial block contains a six-dimensional two-star principal block of rank6-c for each line. Thus its rank is at least6-min(c_left,c_right). Total rank<=30 leaves nontrivial nullity at least9-min(c_left,c_right). Two of these are the forced star differences.',
                validation='Exact group action, regular orbits, orthogonality and known star characters checked. No graph or peer rank audited.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, separators=(',',':'))+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], dimensions=result['character_dimensions'],
                         additional_nontrivial_relations=result['c44_target']['additional_nontrivial_relations_at_least'],
                         minimal_targets=len(result['c44_target']['minimal_nullity_thresholds']))))
