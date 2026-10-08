"""Triangular, exact induced-embedding identities for targeted dense families.

Delete a vertex of degree <=2. Its labelled extension count is fixed by
SRG parameters. Subtract all strict supersets of its prescribed neighbours;
each has more edges, so recursion terminates at minimum-degree-three types.
The resulting counts are representatives, not distinct projected vectors.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
import gzip
import time

from higher_census_minima import ROOT
from higher_vertex_census import ir_orders
from seven_vertex_census import decode, encode


def add_scaled(target, source, scale):
    for key, value in source.items():
        target[key] = target.get(key, F(0))+scale*value
        if not target[key]:
            del target[key]


def canonical(adj):
    code, orders = ir_orders(adj)
    return code, len(orders)


def admissible(adj):
    return all((adj[i] & adj[j]).bit_count() <= (1 if adj[i] >> j & 1 else 2)
               for i, j in combinations(range(len(adj)), 2))


def load_stage(packet, n):
    stage = next(s for s in packet['stages'] if s['order'] == n)
    names = ['1']+stage['parameters']
    graphs, embedded = {}, {}
    for row in stage['counts']:
        adj = tuple(row['adjacency_bits'])
        code, aut = canonical(adj)
        graphs[code] = decode(n, code)
        embedded[code] = {name: aut*F(value) for name, value in zip(names, row['affine']) if F(value)}
    return stage, graphs, embedded


class TriangularCensus:
    def __init__(self, n, v, k, lower, dense=None):
        self.n, self.v, self.k, self.lower = n, v, k, lower
        self.dense = dense
        self.forms, self.graphs, self.equations, self.new_parameters = {}, {}, {}, set()
        self.started = time.monotonic()

    def solve(self, adj):
        code, aut = canonical(adj)
        if code in self.forms:
            return self.forms[code]
        adj = decode(self.n, code)
        self.graphs[code] = adj
        candidates = [i for i in range(self.n) if adj[i].bit_count() <= 2]
        if not candidates:
            if self.dense is not None:
                result = dict(self.dense[code])
            else:
                name = f'C{self.n}_{code}'
                self.new_parameters.add(name)
                result = {name: F(aut)}
            self.forms[code] = result
            return result
        # Prefer an adjacent pair: its unique common neighbour is especially rigid.
        def priority(i):
            ns = [j for j in range(self.n) if adj[i] >> j & 1]
            return (len(ns), int(len(ns) == 2 and bool(adj[ns[0]] >> ns[1] & 1)))
        vertex = max(candidates, key=priority)
        order = [i for i in range(self.n) if i != vertex]
        smaller = decode(self.n-1, encode(adj, order))
        mask = sum(1 << j for j, i in enumerate(order) if adj[vertex] >> i & 1)
        chosen = [i for i in range(self.n-1) if mask >> i & 1]
        if len(chosen) == 0:
            budget = self.v-(self.n-1)
        elif len(chosen) == 1:
            budget = self.k-smaller[chosen[0]].bit_count()
        else:
            a, b = chosen
            budget = (1 if smaller[a] >> b & 1 else 2)-(smaller[a] & smaller[b]).bit_count()
        small_code, _ = canonical(smaller)
        result = {key: budget*value for key, value in self.lower[small_code].items() if budget*value}
        rest = ((1 << (self.n-1))-1) ^ mask
        additional = rest
        supergraphs = Counter()
        while additional:
            enlarged = mask | additional
            extension = tuple(smaller[i] | (((enlarged >> i) & 1) << (self.n-1))
                              for i in range(self.n-1))+(enlarged,)
            if admissible(extension):
                extension_code, _ = canonical(extension)
                supergraphs[extension_code] += 1
                add_scaled(result, self.solve(extension), -1)
            additional = (additional-1) & rest
        self.equations[code] = {'lower_code': small_code, 'budget': budget,
                                'supergraphs': dict(supergraphs)}
        self.forms[code] = result
        if len(self.forms) % 250 == 0:
            print('Solved', len(self.forms), 'types;', len(self.new_parameters), 'dense invariants;',
                  round(time.monotonic()-self.started, 1), 'seconds', flush=True)
        return result

    def verify_equations(self):
        for code, equation in self.equations.items():
            residual = dict(self.forms[code])
            add_scaled(residual, self.lower[equation['lower_code']], -equation['budget'])
            for other, multiplicity in equation['supergraphs'].items():
                add_scaled(residual, self.forms[other], multiplicity)
            assert not residual, code


def verify_nine(packet):
    _, _, lower = load_stage(packet, 8)
    _, graphs, reference = load_stage(packet, 9)
    solver = TriangularCensus(9, packet['srg_parameters'][0], packet['srg_parameters'][1], lower,
                             dense=reference)
    checked = 0
    for code, adj in graphs.items():
        if min(row.bit_count() for row in adj) < 2:
            continue
        assert solver.solve(adj) == reference[code], code
        checked += 1
    solver.verify_equations()
    print('Order-nine independent triangular recurrence:', checked, 'counts agree', flush=True)
    return checked


def partial_extension_slacks(solver):
    """Omitted induced types have nonnegative counts, giving valid inequalities.

    This uses every marked extension equation met by the targeted type set,
    not only the triangular equations used to express the types.
    """
    lhs, rhs = {}, {}
    n = solver.n
    for code, adj in solver.graphs.items():
        _, aut = canonical(adj)
        count = {key: value/aut for key, value in solver.forms[code].items()}
        flags = Counter()
        for vertex in range(n):
            order = [i for i in range(n) if i != vertex]
            smaller = decode(n-1, encode(adj, order))
            neighbours = [j for j, i in enumerate(order) if adj[vertex] >> i & 1]
            small_code, orders = ir_orders(smaller)
            for size in range(3):
                for chosen in combinations(neighbours, size):
                    mask = sum(1 << i for i in chosen)
                    orbit = {sum(1 << i for i, j in enumerate(order) if mask >> j & 1)
                             for order in orders}
                    flag = (small_code, min(orbit))
                    flags[flag] += 1
                    if flag not in rhs:
                        if not chosen:
                            budget = solver.v-(n-1)
                        elif len(chosen) == 1:
                            budget = solver.k-smaller[chosen[0]].bit_count()
                        else:
                            a, b = chosen
                            budget = (1 if smaller[a] >> b & 1 else 2)-(smaller[a] & smaller[b]).bit_count()
                        rhs[flag] = {key: value*F(len(orbit)*budget, len(orders))
                                     for key, value in solver.lower[small_code].items()}
        for flag, multiplicity in flags.items():
            add_scaled(lhs.setdefault(flag, {}), count, multiplicity)
    result = {}
    for flag, form in rhs.items():
        add_scaled(form, lhs[flag], -1)
        result[f'extension_{flag[0]}_{flag[1]}'] = {key: value for key, value in form.items() if value}
    return result


def run():
    packet = json.loads((ROOT/'data/codex_census_validation_99.json').read_text())
    checked = verify_nine(packet)
    _, _, lower6 = load_stage(packet, 6)
    _, graphs7, reference7 = load_stage(packet, 7)
    validation = TriangularCensus(7, 99, 14, lower6)
    validation.graphs, validation.forms = graphs7, reference7
    assert not any(partial_extension_slacks(validation).values())
    print('All order-seven marked extension identities verified exactly', flush=True)
    stage9, _, lower = load_stage(packet, 9)
    stage5 = next(s for s in packet['stages'] if s['order'] == 5)
    dense5 = [row for row in stage5['counts'] if row['edges'] == 6]
    assert len(dense5) == 2
    solver = TriangularCensus(10, 99, 14, lower)
    target_graphs = {}
    for a, first in enumerate(dense5):
        for second in dense5[a:]:
            adj = tuple(first['adjacency_bits'])+tuple(x << 5 for x in second['adjacency_bits'])
            target_graphs[canonical(adj)[0]] = adj
            for i in range(5):
                for j in range(5, 10):
                    joined = list(adj)
                    joined[i] |= 1 << j
                    joined[j] |= 1 << i
                    joined = tuple(joined)
                    if admissible(joined):
                        target_graphs[canonical(joined)[0]] = joined
    for first in dense5:
        for second in stage5['counts']:
            if second['edges'] != 5:
                continue
            adj = tuple(first['adjacency_bits'])+tuple(x << 5 for x in second['adjacency_bits'])
            target_graphs[canonical(adj)[0]] = adj
    targets, raw_families = [], {6: {}, 8: {}}
    for code, adj in sorted(target_graphs.items()):
        _, aut = canonical(adj)
        embedded = solver.solve(adj)
        count = {key: value/aut for key, value in embedded.items()}
        mult = Counter()
        for positive in combinations(range(10), 5):
            pm = sum(1 << i for i in positive)
            nm = 1023 ^ pm
            ep = sum((adj[i] & pm).bit_count() for i in positive)//2
            en = sum((adj[i] & nm).bit_count() for i in range(10) if nm >> i & 1)//2
            cross = sum((adj[i] & nm).bit_count() for i in positive)
            q = 30-2*(ep+en-cross)
            if q in raw_families:
                mult[q] += 1
        for q, multiplicity in mult.items():
            add_scaled(raw_families[q], count, multiplicity)
        targets.append({'code': code, 'signed_multiplicities': dict(mult)})
        print('Target', code, 'done;', len(solver.forms), 'dependency types', flush=True)
    solver.verify_equations()
    names = ['1']+stage9['parameters']+sorted(solver.new_parameters)
    def vector(form):
        return [form.get(name, F(0)) for name in names]
    records = []
    for code, embedded in sorted(solver.forms.items()):
        adj = solver.graphs[code]
        _, aut = canonical(adj)
        form = {key: value/aut for key, value in embedded.items()}
        records.append({'code': code, 'adjacency_bits': list(adj), 'automorphisms': aut,
                        'affine_sparse': {key: str(value) for key, value in sorted(form.items())}})
    report = {'method': 'Exact triangular induced-embedding recurrences; targeted dependency closure only.',
              'order9_counts_reproduced': checked, 'order7_all_marked_extensions_verified': True,
              'parameters': names[1:], 'targets': targets,
              'dependency_graph_types': len(solver.forms), 'new_dense_parameters': len(solver.new_parameters),
              'counts': records, 'embedding_equations': solver.equations,
              'raw_objectives': {q: list(map(str, vector(raw))) for q, raw in raw_families.items()},
              'scope': 'Raw signed representatives only; no mass-ten collision bound or rank exclusion.'}
    print('Exact formulas:', len(solver.forms), 'types;', len(solver.new_parameters), 'new parameters', flush=True)
    extensions = partial_extension_slacks(solver)
    print('Additional extension inequalities:', len(extensions), flush=True)
    report['extension_slacks'] = {name: {key: str(value) for key, value in sorted(form.items())}
                                for name, form in extensions.items()}
    path = ROOT/'data/codex_targeted_order10_census.json.gz'
    with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
        stream.write((json.dumps(report, indent=2)+'\n').encode('utf-8'))
    print('Saved compressed exact census:', path.name, flush=True)


if __name__ == '__main__':
    run()
