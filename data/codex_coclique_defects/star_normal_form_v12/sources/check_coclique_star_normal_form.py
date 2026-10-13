"""Finite coverage certificate for a new representative choice, not a C1 audit."""
from collections import Counter
from itertools import permutations, product
from pathlib import Path
import argparse
import hashlib
import json

from ortools.sat.python import cp_model
from coclique_star_normal_form import PATTERNS, NAMES, fixed_edges, star_vertices, add_constraints


def matchings(vertices):
    if not vertices:
        yield frozenset()
        return
    a, *rest = vertices
    for b in rest:
        for smaller in matchings([v for v in rest if v != b]):
            yield smaller | {(a, b)}


def coverage():
    # This generator does not use the proposed normal forms.
    admissible = {m for m in matchings(list(range(10))) if (2, 3) not in m}
    assert len(admissible) == 840
    classified = Counter()
    orbits = []
    for pattern in PATTERNS:
        orbit = set()
        for y, c, z in product(permutations(range(2)), permutations(range(2, 4)),
                               permutations(range(4, 10))):
            relabel = y+c+z
            orbit.add(frozenset(tuple(sorted((relabel[a], relabel[b]))) for a, b in pattern))
        orbits.append(orbit)
    assert [len(orbit) for orbit in orbits] == [90, 360, 360, 30]
    assert set().union(*orbits) == admissible
    assert sum(map(len, orbits)) == len(admissible)
    for matching in admissible:
        yc = sum(a < 2 and b in (2, 3) for a, b in matching)
        classified['YY' if (0, 1) in matching else f'YC{yc}'] += 1
    assert classified == dict(zip(NAMES, (90, 360, 360, 30)))
    # Exhaustively check the actual selector/edge encoder on the local
    # object. All nonlocal signatures are equal; negative edges are 1 so
    # the charge consequences introduce no accidental local restriction.
    model = cp_model.CpModel()
    fixed = fixed_edges()
    variable = {}
    for i in range(4):
        vs = star_vertices(i)
        for a in range(10):
            for b in range(a+1, 10):
                pair = tuple(sorted((vs[a], vs[b])))
                if pair not in fixed:
                    variable[pair] = model.NewBoolVar(f'a{pair[0]}_{pair[1]}')
    def edge(u, v):
        key = tuple(sorted((u, v)))
        if key in fixed:
            return fixed[key]
        if key in variable:
            return variable[key]
        return int(v in (37, 38) or u in (37, 38))
    choices = add_constraints(model, edge)
    # The remaining Z-Z endpoint signatures are equal in this mock.
    # Pin each star's selectors and check every type.
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = 5
    for index in range(4):
        probe = model.clone()
        for i in range(4):
            probe.Add(choices[i][index] == 1)
        status = solver.Solve(probe)
        assert status == cp_model.OPTIMAL, (index, solver.StatusName(status))
        for i in range(4):
            vs = star_vertices(i)
            actual = frozenset((a, b) for a in range(10) for b in range(a+1, 10)
                               if solver.Value(edge(vs[a], vs[b])))
            assert actual == PATTERNS[index]
    return dict(status='PASS', all_admissible_matchings=len(admissible),
                disjoint_orbit_sizes=dict(classified), canonical_types=4,
                local_encoder_types_checked=4, shared_fixed_edges=len(fixed),
                scope='Coverage under S2(Y) x S2(C) x S6(Z); no C1 branch excluded')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    args.folder.mkdir(parents=True, exist_ok=True)
    report = coverage()
    report['source_sha256'] = {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ('coclique_star_normal_form.py', Path(__file__).name)}
    (args.folder/'coverage.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
