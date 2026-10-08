"""Exact targeted dependency closure for prism plus an anticomplete house.

Prism plus prism already has minimum degree three, hence the triangular
recursion alone makes it a new independent order-twelve parameter.
Each twin-prism pair gives twelve distinct prism-house induced copies.
"""
from collections import Counter
from fractions import Fraction as F
import gzip
import json
import sys
import time

from higher_census_minima import ROOT
from targeted_order10_census import canonical, partial_extension_slacks, TriangularCensus
from seven_vertex_census import decode, encode
sys.path.insert(0, str(ROOT/'code/lab_theta_lp_2026-10-08'))
import census2 as lab


def graph(n, edges):
    adj = [0]*n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return tuple(adj)


PRISM = graph(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5)])
HOUSE = graph(5, [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4), (4, 0)])


def union(a, b):
    return tuple(a)+tuple(row << len(a) for row in b)


def add(out, form, factor):
    for key, value in form.items():
        out[key] = out.get(key, F(0))+factor*value
        if not out[key]:
            del out[key]


class Target:
    def __init__(self, lower):
        self.lower = lower
        self.forms, self.graphs, self.equations, self.dense = {}, {}, {}, {}
        self.start = time.monotonic()

    def solve(self, adj):
        n = len(adj)
        assert n == 11
        key, perm = lab.canon(n, adj)
        if key in self.forms:
            return self.forms[key]
        adj = lab.relabel(n, adj, perm)
        self.graphs[key] = adj
        low = [v for v in range(n) if adj[v].bit_count() <= 2]
        if not low:
            aut = lab.aut_order(n, adj)
            self.dense[key] = aut
            out = {f'C11_{key}': F(aut)}
        else:
            def priority(v):
                neighbours = [u for u in range(n) if adj[v] >> u & 1]
                return len(neighbours), int(len(neighbours) == 2 and bool(adj[neighbours[0]] >> neighbours[1] & 1))
            vertex = max(low, key=priority)
            keep = [v for v in range(n) if v != vertex]
            small = tuple(sum(1 << j for j, u in enumerate(keep) if adj[v] >> u & 1) for v in keep)
            mask = sum(1 << j for j, v in enumerate(keep) if adj[vertex] >> v & 1)
            chosen = [i for i in range(10) if mask >> i & 1]
            if len(chosen) == 0:
                budget = 89
            elif len(chosen) == 1:
                budget = 14-small[chosen[0]].bit_count()
            else:
                u, v = chosen
                budget = (1 if small[u] >> v & 1 else 2)-(small[u] & small[v]).bit_count()
            lower_key, _ = lab.canon(10, small)
            out = {name: budget*F(value) for name, value in self.lower[lower_key].items() if budget*F(value)}
            other = Counter()
            for bigger in lab.admissible_sets(10, small, mask):
                if bigger == mask:
                    continue
                extended = lab.extend(10, small, bigger)
                child_key, _ = lab.canon(11, extended)
                other[child_key] += 1
                add(out, self.solve(extended), -1)
            self.equations[key] = {'lower_key': lower_key, 'budget': budget, 'supergraphs': dict(other)}
        self.forms[key] = out
        if len(self.forms) % 500 == 0:
            print('Order11 closure:', len(self.forms), 'types;', len(self.dense), 'dense;',
                  round(time.monotonic()-self.start, 1), 'seconds', flush=True)
        return out

    def verify(self):
        for key, eq in self.equations.items():
            out = dict(self.forms[key])
            add(out, {k: F(v) for k, v in self.lower[eq['lower_key']].items()}, -eq['budget'])
            for other, multiplicity in eq['supergraphs'].items():
                add(out, self.forms[other], multiplicity)
            assert not out, key


def main():
    with gzip.open(ROOT/'data/codex_lab_full_order10.json.gz', 'rt', encoding='utf-8') as stream:
        source = json.load(stream)
    lower = {key: form for key, _, _, form in source['types']['10']}
    target = Target(lower)
    adj = union(PRISM, HOUSE)
    form = target.solve(adj)
    key, _ = lab.canon(11, adj)
    aut = lab.aut_order(11, adj)
    target.verify()
    # Keep every marked extension inequality visible from this closure,
    # including those not selected by the triangular elimination.
    marked = TriangularCensus(11, 99, 14, {})
    for old_key, graph_rows in target.graphs.items():
        code, _ = canonical(graph_rows)
        marked.graphs[code] = decode(11, code)
        marked.forms[code] = target.forms[old_key]
        for vertex in range(11):
            small = decode(10, encode(graph_rows, [v for v in range(11) if v != vertex]))
            small_code, _ = canonical(small)
            lab_key, _ = lab.canon(10, small)
            marked.lower[small_code] = {k: F(v) for k, v in lower[lab_key].items()}
    slacks = partial_extension_slacks(marked)
    twins = union(PRISM, PRISM)
    assert all(row.bit_count() == 3 for row in twins)
    # Deleting any vertex leaves this same prism-house type.
    for vertex in range(12):
        keep = [v for v in range(12) if v != vertex]
        small = tuple(sum(1 << j for j, u in enumerate(keep) if twins[v] >> u & 1) for v in keep)
        assert lab.canon(11, small)[0] == key
    report = {'target': 'prism + anticomplete house', 'lab_key': key, 'automorphisms': aut,
              'dependency_types': len(target.forms), 'new_dense_order11_parameters': len(target.dense),
              'prism_house_count': {k: str(v/aut) for k, v in form.items()},
              'counts': [{'key': k, 'adjacency_bits': list(target.graphs[k]),
                          'embedding_affine': {name: str(value) for name, value in f.items()}}
                         for k, f in target.forms.items()],
              'embedding_equations': target.equations,
              'extension_slacks': {name: {k: str(v) for k, v in form.items()}
                                   for name, form in slacks.items()},
              'new_parameters': [f'C11_{k}' for k in sorted(target.dense)],
              'prism_prism': {'order': 12, 'minimum_degree': 3, 'triangular_dependency_types': 1,
                              'new_independent_parameter': True},
              'twin_inequality': '12*tau <= N(prism + anticomplete house)',
              'scope': 'Exact dependency closure and count formulas; no new bound on tau until certified optimisation.'}
    path = ROOT/'data/codex_prism_house_order11.json.gz'
    with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
        stream.write((json.dumps(report, indent=2)+'\n').encode('utf-8'))
    print('Verified closure:', len(target.forms), 'types,', len(target.dense), 'new dense parameters;',
          'target automorphisms', aut, '; marked extension inequalities', len(slacks), flush=True)


if __name__ == '__main__':
    main()
