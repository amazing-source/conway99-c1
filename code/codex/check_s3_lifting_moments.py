"""Finite check of the new exact F3 moment criterion, not of the old graphs."""
from itertools import product
from pathlib import Path
import json


def main():
    results = []
    for q in (1, 2):
        total = accepted = 0
        for values in product(range(3), repeat=3*q):
            total += 1
            balanced = all(values.count(i) == q for i in range(3))
            moments = (sum(values) % 3 == 0
                       and sum(x*x for x in values) % 3 == 2*q % 3)
            assert moments == balanced, (q, values)
            accepted += moments
        assert accepted == {1: 6, 2: 90}[q]
        results.append(dict(length=3*q, tuples=total, solutions=accepted,
                            first_moment=0, second_moment=2*q % 3))
    report = dict(field=3, results=results,
                  claim='Exact balance iff the two moment equations, for lengths 3 and 6 only.',
                  graph_exclusions=0)
    out = Path(__file__).resolve().parents[2] / 'data/codex_s3_lifting_moments.json'
    out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
