"""Small exact checks used by the 12 October audit; standard library only."""
from itertools import permutations, combinations_with_replacement
from collections import Counter
from pathlib import Path
import json


def main():
    perms = list(permutations(range(3)))
    sign = lambda p: sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)) % 2
    path_multisets = []
    for indices in combinations_with_replacement(range(6), 6):
        if all(sum(perms[j][u] == v for j in indices) == 2
               for u in range(3) for v in range(3)):
            path_multisets.append(dict(multiplicities=[indices.count(j) for j in range(6)],
                                       odd_paths=sum(sign(perms[j]) for j in indices)))
    assert len(path_multisets) == 3
    trace_cases = []
    for m in [3, 9, 11, 33]:
        for a in range(m):
            b = m-1-a
            t = 14+3*a-4*b
            if t % m == 0 and 0 <= t//m < 99//m:
                d = t//m
                trace_cases.append(dict(cells=m, cell_size=99//m, degree=d,
                                        positive_multiplicity=a, negative_multiplicity=b,
                                        internal_handshake_possible=d*(99//m) % 2 == 0))
    assert [(c['cells'], c['cell_size'], c['degree']) for c in trace_cases
            if c['internal_handshake_possible']] == [(3,33,2), (11,9,4)]
    binary = []
    for t in range(15):
        w = 7*t
        v7 = 2*t*(11-t)
        for v14 in range(100-w):
            u = t*(2*t-11)-2*v14
            if 0 <= u <= w and 0 <= v7 and v7+v14 <= 99-w:
                binary.append(dict(weight=w, u=u, v7=v7, v14=v14))
    assert [r['weight'] for r in binary] == [0,63,77]
    # Six identity gains satisfy the parity test (zero odd paths), not sum P=2J.
    assert sum(sign(perms[0]) for _ in range(6)) == 0
    assert sum(perms[0][0] == 0 for _ in range(6)) == 6
    report = dict(permutation_order=perms, valid_six_path_multisets=path_multisets,
                  equal_cell_trace_candidates=trace_cases, binary_moment_solutions=binary,
                  parity_only_is_not_the_full_local_permutation_equation=True)
    out = Path(__file__).resolve().parents[2] / 'data/codex_asymmetry_local_checks_20261012.json'
    out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
