"""Short integer checks for the new defect lemmas and propagation witnesses."""

from pathlib import Path
from itertools import combinations
import json

BASE = Path(__file__).resolve().parents[2]
DATA = BASE/'data'/'codex_coclique_defects'


def check_grid_identity():
    # Every independent subset of the 3x3 grid, including nonmaximum ones.
    neighbours = [{j for j in range(9) if i != j and (i//3 == j//3 or i%3 == j%3)}
                  for i in range(9)]
    checked = 0
    for mask in range(1 << 9):
        c = {i for i in range(9) if (mask >> i)&1}
        if any(neighbours[i] & c for i in c):
            continue
        delta = 3-len(c)
        q = [2-(2 if i in c else 0)-len(neighbours[i] & c) for i in range(9)]
        assert all(sum(q[j] for j in neighbours[i]) == q[i]+2*delta for i in range(9))
        assert sum(q) == 6*delta
        assert sum(x*x for x in q) == delta*(2*delta+6)
        checked += 1
    return checked


def check_six_vertex_lemma():
    pairs = list(combinations(range(6), 2))
    max_edges, extremal = 0, 0
    for mask in range(1 << len(pairs)):
        if mask.bit_count() < 9:
            continue
        neighbours = [set() for _ in range(6)]
        for t, (i, j) in enumerate(pairs):
            if (mask >> t)&1:
                neighbours[i].add(j)
                neighbours[j].add(i)
        if any(len(neighbours[i] & neighbours[j]) > 2-(j in neighbours[i]) for i, j in pairs):
            continue
        max_edges = max(max_edges, mask.bit_count())
        assert mask.bit_count() == 9
        assert all(len(row) == 3 for row in neighbours)
        triangles = [set(t) for t in combinations(range(6), 3)
                     if all(j in neighbours[i] for i, j in combinations(t, 2))]
        assert len(triangles) == 2 and not (triangles[0] & triangles[1])
        # At most three new vertices can each meet two old vertices:
        # only the three matching edges still have common-neighbour capacity.
        eligible = [(i, j) for i, j in pairs if len(neighbours[i] & neighbours[j]) < 2-(j in neighbours[i])]
        assert len(eligible) == 3
        extremal += 1
    assert max_edges == 9 and extremal == 60
    return dict(max_edges=max_edges, labelled_prisms=extremal)


def check_certificate(path):
    result = json.loads(path.read_text())
    proof = result['propagation']
    assert proof['status'] == 'CONTRADICTION'
    eqs, values = proof['equations'], {}
    for step in proof['assignments']:
        v, value = step['variable'], step['value']
        eq = eqs[step['equation']]
        assert v in eq['variables'] and v not in values
        need = eq['rhs']-sum(values.get(x, 0) for x in eq['variables'])
        free = sum(x not in values for x in eq['variables'])
        assert (value == 0 and need == 0) or (value == 1 and need == free)
        values[v] = value
    eq = eqs[proof['equation']]
    need = eq['rhs']-sum(values.get(x, 0) for x in eq['variables'])
    free = sum(x not in values for x in eq['variables'])
    assert need < 0 or need > free
    assert need == proof['residual_rhs'] and free == proof['remaining_variables']
    return dict(assignments=len(values), residual_rhs=need, available=free)


def main():
    report = dict(grid_independent_sets=check_grid_identity(), six_vertex_lemma=check_six_vertex_lemma())
    report['propagation_certificates'] = {
        p.stem: check_certificate(p)
        for p in sorted(DATA.glob('core_*_linear_completion.json'))}
    positive = json.loads((DATA/'grid9_positive_control_gluing_pairs_linear_completion.json').read_text())
    assert positive['full_srg_check'] and not positive['violations']
    report['full_grid9_reconstruction'] = 'PASS'
    report['status'] = 'PASS'
    (DATA/'checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
