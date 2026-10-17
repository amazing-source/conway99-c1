"""Apply the no-P4 rectangle theorem after rotating the root inside a line.

In a coloured cubic component of N(L), every colour induces a matching.
Let (u,v,w) be a triangle using the three colours, and let (u',v',w') be
their same-colour mates. Their induced graph cannot have exactly two
edges. For example u'~v',u'~w',v'!~w' gives, rooted at u, a forbidden
P4 rectangle on the two other points of L together with v',w'.

This is stronger than checking the rectangles at the original root only.
It uses no chosen completion and applies to every Conway line component.
"""

import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process


def reject_reason(record, code):
    p, ma, mb = code
    permutation = record['cross_permutations'][p]
    n = len(permutation)
    mates = []
    for mi in (ma, mb):
        row = [None] * n
        for x, y in record['internal_matchings'][mi]:
            row[x], row[y] = y, x
        mates.append(row)
    for i in range(n):
        if permutation[i] != i:
            continue
        edges = [mates[0][i] == (i ^ 1), mates[1][i] == (i ^ 1),
                 permutation[mates[0][i]] == mates[1][i]]
        if sum(edges) == 2:
            return {'triangle_index': i, 'mate_edges': list(map(int, edges))}
    return None


def check_witness(record, code, reason):
    """Check the nine-vertex obstruction encoded by the new rule itself."""
    p, ma, mb = code
    permutation = record['cross_permutations'][p]
    n = len(permutation)
    graph = [set() for _ in range(3 + 3*n)]
    def edge(x, y):
        graph[x].add(y); graph[y].add(x)
    for a in range(3):
        for b in range(a+1, 3): edge(a,b)
        for i in range(n): edge(a,3+a*n+i)
    mates = [[i ^ 1 for i in range(n)]]
    for mi in (ma, mb):
        row = [None] * n
        for x,y in record['internal_matchings'][mi]: row[x],row[y] = y,x
        mates.append(row)
    for c in range(3):
        for i,j in enumerate(mates[c]):
            if i<j: edge(3+c*n+i,3+c*n+j)
    for i in range(n):
        edge(3+i,3+n+i); edge(3+i,3+2*n+i)
        edge(3+n+i,3+2*n+permutation[i])
    i = reason['triangle_index']
    opposite = [3+c*n+mates[c][i] for c in range(3)]
    middle = next(c for c in range(3) if sum(v in graph[opposite[c]] for v in opposite) == 2)
    others = [c for c in range(3) if c != middle]
    root = 3+middle*n+i
    a,b = others
    corners = [a,b,opposite[a],opposite[b]]
    assert sum(y in graph[x] for x in corners for y in corners)//2 == 3
    assert sorted(sum(y in graph[x] for y in corners) for x in corners) == [1,1,2,2]
    assert opposite[a] in graph[opposite[middle]] and opposite[b] in graph[opposite[middle]]
    assert all(v in graph[root] for v in (middle,opposite[middle],3+a*n+i,3+b*n+i))
    return {'root': root, 'rectangle': corners, 'shared_endpoint_label': opposite[middle]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    resources = limit_research_process(4)
    data = json.loads(args.source.read_text())
    reports = []
    for record in data['records']:
        keep, witness = [], None
        for code in record['component_code_triples']:
            reason = reject_reason(record, code)
            if reason is None:
                keep.append(code)
            elif witness is None:
                witness = dict(code=code, reason=reason, **check_witness(record, code, reason))
        report = {'vertices': record['vertices'], 'before': len(record['component_code_triples']),
                  'after': len(keep), 'first_exact_obstruction': witness}
        if record['vertices'] == 6: assert report['before'] == report['after'] == 1
        record['component_code_triples'] = keep
        record['rotated_rectangle_filter'] = report
        reports.append(report)
        print(json.dumps(report), flush=True)
    data['additional_necessary_condition'] = __doc__
    args.output.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
    args.report.write_text(json.dumps({'scope':__doc__,'source':str(args.source),'resources':resources,
                                      'records':reports},indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__': main()
