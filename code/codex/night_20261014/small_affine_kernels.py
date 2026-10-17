"""Finite support classification for unequal-sum small projection collisions.

For P=(27I-9A+J)/63 and integral h with Ph=0 and ||h||_1<=16,
sum(h) is 0 or +/-9. The zero-sum case is treated separately.
Orient the other case to sum(h)=9. Then either h is a grid indicator,
or h=1_S-1_T with T a triangle, |S|=12, S disjoint and nonadjacent to T,
and the induced graph on S is four-regular. All entries are 0,+/-1.

This script quotients the exact C++ support enumeration by isomorphism and
bounds the number of induced copies using explicit embedding orders. It
does not claim that any surviving support extends to a C1 graph.
"""
from collections import Counter
from math import prod
from pathlib import Path
import json

from small_positive_three_supports import embedding_bound, valid


def canonical(rows):
    """Individualization/refinement, with exact automorphism count at leaves."""
    n = len(rows)

    def refine(cells):
        while True:
            masks = [sum(1 << v for v in cell) for cell in cells]
            result = []
            for cell in cells:
                buckets = {}
                for v in cell:
                    signature = tuple((rows[v] & mask).bit_count() for mask in masks)
                    buckets.setdefault(signature, []).append(v)
                result.extend(buckets[key] for key in sorted(buckets))
            if len(result) == len(cells):
                return result
            cells = result

    def search(cells):
        cells = refine(cells)
        choices = [(len(cell), i) for i, cell in enumerate(cells) if len(cell) > 1]
        if not choices:
            order = [cell[0] for cell in cells]
            code = tuple(sum(1 << j for j, w in enumerate(order) if rows[v] >> w & 1)
                         for v in order)
            return code, 1
        _, index = min(choices)
        answer, count = None, 0
        for v in cells[index]:
            split = cells[:index] + [[v], [w for w in cells[index] if w != v]] + cells[index+1:]
            code, ways = search(split)
            if answer is None or code < answer:
                answer, count = code, ways
            elif code == answer:
                count += ways
        return answer, count

    return search([list(range(n))])


def classify(path):
    records = [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines()]
    summary = records[-1]['summary']
    assert summary['complete'] and summary['leaves'] == len(records)-1
    types = {}
    for record in records[:-1]:
        rows = record['rows']
        assert len(rows) == summary['order'] and valid(rows)
        assert all(row.bit_count() == 4 for row in rows)
        key, automorphisms = canonical(rows)
        if key in types:
            assert types[key]['automorphisms'] == automorphisms
            types[key]['enumeration_multiplicity'] += 1
        else:
            types[key] = dict(rows=list(key), automorphisms=automorphisms,
                              enumeration_multiplicity=1)
    return summary, [types[key] for key in sorted(types)]


def automorphism_count(rows):
    """Independent adjacency-preserving bijection search; no color refinement."""
    n = len(rows)
    mapping = {}

    def search(used):
        if len(mapping) == n:
            return 1
        options = []
        for x in range(n):
            if x in mapping:
                continue
            candidates = [y for y in range(n) if not used >> y & 1 and
                          all(((rows[x] >> u) & 1) == ((rows[y] >> v) & 1)
                              for u, v in mapping.items())]
            options.append((len(candidates), x, candidates))
        _, x, candidates = min(options)
        answer = 0
        for y in candidates:
            mapping[x] = y
            answer += search(used | 1 << y)
            del mapping[x]
        return answer

    return search(0)


def main():
    data = Path(__file__).resolve().parents[3] / 'data' / 'codex_night_20261014'
    report = {}
    for n in [9, 12]:
        summary, types = classify(data / f'affine_regular_{n}.jsonl')
        histogram = Counter()
        for item in types:
            rows = item['rows']
            assert automorphism_count(rows) == item['automorphisms']
            triangles = sum((rows[x] & rows[y]).bit_count()
                            for x in range(n) for y in range(x+1, n) if rows[x] >> y & 1)//3
            item['triangles'] = triangles
            histogram[triangles] += 1
            item['embedding_bound'] = embedding_bound(rows)
            assert prod(factor for _, factor in item['embedding_bound']['order_and_choice_bounds']) == item['embedding_bound']['labeled_embeddings']
            item['induced_copy_bound'] = item['embedding_bound']['labeled_embeddings']//item['automorphisms']
            # For a twelve-support, these are multiplicities of S-pairs in X.
            residual = [[0 if x == y else 2-((rows[x] >> y) & 1)-(rows[x] & rows[y]).bit_count()
                         for y in range(n)] for x in range(n)]
            if n == 12:
                assert all(sum(row) == 6 for row in residual)
            else:
                assert all(not any(row) for row in residual)
        report[n] = dict(enumeration=summary, types=types, type_count=len(types),
                         types_by_number_of_triangles=dict(sorted(histogram.items())),
                         all_induced_copies_bound=sum(item['induced_copy_bound'] for item in types))
        print(json.dumps(dict(order=n, nodes=summary['nodes'], leaves=summary['leaves'],
                              types=len(types), triangles=dict(sorted(histogram.items())),
                              copies_bound=report[n]['all_induced_copies_bound'])), flush=True)
    assert report[9]['type_count'] == 1 and report[9]['types'][0]['automorphisms'] == 72
    # Each S determines its T uniquely: the three zeros of (A-3I)1_S.
    report['nonzero_sum_signed_l1_16_kernel_bound'] = 2*(191+report[12]['all_induced_copies_bound'])
    report['all_signed_l1_16_projection_kernel_bound'] = 313434 + report['nonzero_sum_signed_l1_16_kernel_bound']
    (data / 'small_affine_kernels.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if isinstance(key, str)}), flush=True)


if __name__ == '__main__':
    main()
