"""Stream the full adjacency equations to SAT after fixing one internal star.

All C1 counts and all C2 common-neighbour equalities are encoded. For a
Conway template, its component equations and weighted-root prism budget
are added, with no canonical component code and no fixed Gram witness.
The model is weaker than the transported c4 model: no condition on the
component count at other lines is imposed. UNSAT still excludes this
labelled matching of the selected root. A SAT graph is checked exactly.

Clauses are streamed to disk to keep construction memory small. The
standalone SAT solver can export a DRAT proof for an UNSAT result.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import shutil
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_boundary_sat import Encoder
from root_component_projection_cnf import solve_file_checked
from root_component_resources import atomic_json_write, limit_research_process


class ClauseStream:
    def __init__(self, stream):
        self.stream = stream
        self.count = 0

    def append(self, row):
        self.stream.write(' '.join(map(str, row)) + (' ' if row else '') + '0\n')
        self.count += 1

    def extend(self, rows):
        for row in rows:
            self.append(row)


def encode(path, k, initial=None, component_rows=None, prism_budget=None, upper_only=False,
           literal_table=None, grid_transport=None):
    labels = tuple((a, b) for a, b in combinations(range(k), 2) if b != (a ^ 1))
    pairs = tuple(combinations(range(len(labels)), 2))
    n = len(labels); initial = initial or {}
    graph = [[False] * n for _ in range(n)]
    body = path.with_suffix('.body.tmp')
    assert not path.exists() and not body.exists()
    with body.open('w', encoding='ascii', newline='\n') as stream:
        enc = Encoder(len(pairs)); enc.clauses = ClauseStream(stream)
        for i, (u, v) in enumerate(pairs):
            graph[u][v] = graph[v][u] = bool(initial[i]) if i in initial else i+1
            if i in initial:
                enc.clause(i+1 if initial[i] else -(i+1))

        def cardinality(terms, target, equality=True):
            target -= sum(x is True for x in terms)
            variables = [x for x in terms if type(x) is not bool]
            if equality:
                enc.exactly(variables, target)
            else:
                enc.atmost(variables, target)

        if component_rows is None:
            for w, label in enumerate(labels):
                cardinality(graph[w], k-2)
                for a in range(k):
                    cardinality([graph[w][q] for q, pair in enumerate(labels) if a in pair],
                                2-int(a in label)-int((a ^ 1) in label))
        else:
            equations, bounds = component_rows
            for positions, target, _ in equations:
                cardinality([graph[pairs[i][0]][pairs[i][1]] for i in positions], target)
            for positions, bound, _ in bounds:
                cardinality([graph[pairs[i][0]][pairs[i][1]] for i in positions], bound, False)
        if prism_budget is not None:
            cardinality([graph[u][v] for u, v in pairs
                         if tuple(a//2 for a in labels[u]) == tuple(a//2 for a in labels[v])
                         and set(labels[u]) & set(labels[v])], prism_budget, False)
        table_clauses = enc.clauses.count
        if literal_table is not None:
            # An existential selector chooses one complete allowed edge row.
            # No converse implication or exactly-one selector is required.
            choices = []
            for row in literal_table:
                selector = enc.var(); choices.append(selector)
                for literal in row:
                    enc.clause(-selector, literal)
            enc.clause(*choices)
        table_clauses = enc.clauses.count-table_clauses
        c1_clauses = enc.clauses.count
        products = {}

        def conjunction(a, b):
            if type(a) is bool:
                return b if a else False
            if type(b) is bool:
                return a if b else False
            if a == b:
                return a
            key = tuple(sorted((a, b)))
            if key not in products:
                value = enc.var()
                if not upper_only:
                    enc.clause(-value, a); enc.clause(-value, b)
                enc.clause(value, -a, -b)
                products[key] = value
            return products[key]

        for u, v in pairs:
            cardinality([conjunction(graph[u][z], graph[v][z]) for z in range(n)] + [graph[u][v]],
                        2-len(set(labels[u]) & set(labels[v])), not upper_only)
        transport_info = None
        if grid_transport is not None:
            previous_products = len(products)
            transport_info = add_transport_grid_degree(enc, graph, labels, conjunction,
                                                       cardinality, *grid_transport)
            assert len(products) == previous_products, 'Corner selectors must already belong to full C2.'
        info = {'variables': enc.nv, 'clauses': enc.clauses.count,
                'c1_component_budget_clauses': c1_clauses, 'conjunctions': len(products),
                'fixed_edges': len(initial), 'all_common_neighbour_equations': len(pairs),
                'c2_upper_only': upper_only,
                'component_table_clauses': table_clauses,
                'transport_grid_degree': transport_info,
                'upper_only_proof': ('C1 gives each Gamma degree k-2; each row sum of Gamma^2+Gamma+'
                                     'label_overlap off the diagonal is 2*(n-1). All upper bounds '
                                     '<=2 therefore saturate. One-way AND variables dominate actual products.'),
                'cardinality_encoding': 'bidirectional threshold counters, O(n*min(k,n-k))'}
    with path.open('wb') as target, body.open('rb') as source:
        target.write(f'p cnf {info["variables"]} {info["clauses"]}\n'.encode('ascii'))
        shutil.copyfileobj(source, target)
    body.unlink()  # This one newly-created temporary file only.
    return labels, pairs, graph, info


def add_transport_grid_degree(enc, graph, labels, conjunction, cardinality,
                              template, root, matching, weighted_comparison=False):
    """Necessary under global c>=4: every line belongs to at least two grids.

    Components of N(L) have size 6s, with sum s=6. Four or more components
    force at least two singleton parts; each singleton is a grid on L.
    Only one complete fixed star is transported. Grid flags need imply
    actual grids; their converse is unnecessary for these lower bounds.
    """
    before = enc.clauses.count
    letter = 2*root
    outside = [w for w, label in enumerate(labels) if all(a//2 != root for a in label)]
    assert len(matching) == 6 and len(outside) == 60
    nongrids = {tuple(e) for e in template['nongrid_edges']}
    old = []
    for u, v in matching:
        assert letter in labels[u] and letter in labels[v] and graph[u][v] is True
        b = next(a for a in labels[u] if a != letter)
        c = next(a for a in labels[v] if a != letter)
        old.append(int(c == (b ^ 1) and tuple(sorted((root, b//2))) not in nongrids))
    assert sum(old) >= 2
    grid_flags = {}; corner_sizes = []; compatibility = 0; label_cuts = 0
    new_prism_terms = []

    def selected_edge(left, right):
        nonlocal compatibility
        result = enc.var()
        for x, a in left.items():
            for y, b in right.items():
                enc.clause(enc.neg(a), enc.neg(b), -result, graph[x][y])
                enc.clause(enc.neg(a), enc.neg(b), result, enc.neg(graph[x][y]))
                compatibility += 2
        return result

    def guarded_cardinality(flag, terms, bound, equality=True):
        sink = enc.clauses; enc.clauses = []
        try:
            cardinality(terms, bound, equality)
            clauses = enc.clauses
        finally:
            enc.clauses = sink
        for clause in clauses:
            enc.clause(-flag, *clause)

    for i, j in combinations(range(6), 2):
        u0, u1 = matching[i]; v0, v1 = matching[j]
        corners = []
        for u, v in ((u0, v0), (u0, v1), (u1, v0), (u1, v1)):
            choices = {}
            for w in outside:
                flag = conjunction(graph[u][w], graph[v][w])
                if flag is not False:
                    choices[w] = flag
            cardinality(list(choices.values()), 1)
            corners.append(choices)
        corner_sizes.append([len(c) for c in corners])
        flag = enc.var(); grid_flags[i, j] = flag
        # A four-cycle on these corners, together with the known base star,
        # gives the induced 3x3 grid. Extra edges are forbidden by C2.
        orthogonal = ((0, 1), (0, 2), (1, 3), (2, 3))
        if weighted_comparison:
            features = [selected_edge(corners[p], corners[q]) for p, q in orthogonal]
            new_prism_terms.extend(features)
            for feature in features:
                enc.clause(-flag, feature)
            enc.clause(flag, *(-feature for feature in features))
        else:
            for p, q in orthogonal:
                for x, a in corners[p].items():
                    for y, b in corners[q].items():
                        enc.clause(-flag, enc.neg(a), enc.neg(b), graph[x][y])
                        compatibility += 1
        # Unique exterior domination by a grid makes its four corner labels
        # a perfect matching on the eight labels unused by the four bases.
        used = {a for w in (u0, u1, v0, v1) for a in labels[w] if a != letter}
        unused = set(range(14)) - {letter, letter ^ 1} - used
        assert len(used) == 4 and len(unused) == 8
        for corner in corners:
            for w, selected in corner.items():
                if not set(labels[w]) <= unused:
                    enc.clause(-flag, enc.neg(selected)); label_cuts += 1
        for a in sorted(unused):
            guarded_cardinality(flag, [selected for corner in corners for w, selected in corner.items()
                                       if a in labels[w]], 1)
            label_cuts += 1
        # Two corners in an old grid not containing the transported root
        # would be a diagonal pair (their labels are disjoint), forcing both
        # grids to coincide. The new grid omits the old root, so this fails.
        for r, s in combinations(range(7), 2):
            if root in (r, s) or (r, s) in nongrids:
                continue
            guarded_cardinality(flag, [selected for corner in corners for w, selected in corner.items()
                                       if tuple(a//2 for a in labels[w]) == (r, s)], 1, False)
            label_cuts += 1
    for i in range(6):
        flags = [flag for pair, flag in grid_flags.items() if i in pair]
        enc.atmost([-flag for flag in flags], len(flags)-(2-old[i]))
    enc.atmost([-flag for flag in grid_flags.values()], len(grid_flags)-(7-sum(old)))
    score_info = None
    if weighted_comparison:
        lookup = {label: w for w, label in enumerate(labels)}
        opposite = [w for w, label in enumerate(labels) if (letter ^ 1) in label]
        constant = 0
        for u, v in matching:
            p = {w: graph[u][w] for w in opposite if graph[u][w] is not False}
            q = {w: graph[v][w] for w in opposite if graph[v][w] is not False}
            cardinality(list(p.values()), 1); cardinality(list(q.values()), 1)
            b = next(a for a in labels[u] if a != letter)
            c = next(a for a in labels[v] if a != letter)
            constant += int(c == (b ^ 1))
            new_prism_terms.extend([selected_edge(p, q),
                graph[u][lookup[tuple(sorted((letter ^ 1, b)))]],
                graph[v][lookup[tuple(sorted((letter ^ 1, c)))]]])
        old_prism_terms = [graph[u][v] for u, v in combinations(range(len(labels)), 2)
                          if tuple(a//2 for a in labels[u]) == tuple(a//2 for a in labels[v])
                          and set(labels[u]) & set(labels[v])]
        old_grids = 21-len(nongrids)
        from root_component_boolean_arithmetic import weighted_atmost
        terms = [(edge, 9) for edge in old_prism_terms]
        terms += [(enc.neg(edge), 9) for edge in new_prism_terms]
        terms += [(enc.neg(flag), 8) for flag in grid_flags.values()]
        bound = 9*len(new_prism_terms)+8*len(grid_flags)+9*constant+8*sum(old)-8*old_grids
        score_info = weighted_atmost(enc, terms, bound)
        score_info.update(inequality='9s(new)+8g(new)>=9s(original)+8g(original)',
                          new_prism_constant=constant, new_prism_boolean_terms=len(new_prism_terms),
                          old_root_grids=old_grids, new_known_grids=sum(old))
    return {'scope': add_transport_grid_degree.__doc__, 'global_minimum_components': 4,
            'transported_root_letter': letter, 'old_root_grid_flags': old,
            'variable_grid_flags': len(grid_flags), 'corner_domain_sizes': corner_sizes,
            'grid_label_and_intersection_cuts': label_cuts,
            'weighted_root_comparison': score_info,
            'corner_compatibility_implications': compatibility,
            'additional_clauses': enc.clauses.count-before}


def first_component_table(template, initial, directory):
    """The identical first-component normalization used by matching_global.

    Its use restricts the current labelled matching. Consequently this
    branch is NOT quotiented by flips touching the normalized component.
    """
    from root_component_local_tables import canonical_component_codes
    from root_component_propagation import LABELS, VARIABLE
    source = directory/'line_component_pattern_tables_e3_all_colours.json'
    raw = source.read_bytes(); data = json.loads(raw)
    _, root, part = min((-len(part), root, tuple(part))
                       for root, parts in enumerate(template['nontrivial_component_groups']) for part in parts)
    record = next(r for r in data['records'] if r['vertices'] == 6*len(part))
    canonical = canonical_component_codes(record)
    lookup = {p: w for w, p in enumerate(LABELS)}
    letters = [2*j+b for j in sorted(part) for b in (0, 1)]
    stars = [[lookup[tuple(sorted((2*root+a, b))) ] for b in letters] for a in (0, 1)]
    n = len(letters); within = list(combinations(range(n), 2))
    columns = [VARIABLE[tuple(sorted((stars[a][i], stars[a][j])))]
               for a in (0, 1) for i, j in within]
    columns += [VARIABLE[tuple(sorted((u, v)))] for u in stars[0] for v in stars[1]]
    rows = set()
    for pi, m0, m1 in canonical:
        bits = []
        for mi in (m0, m1):
            edges = {tuple(e) for e in record['internal_matchings'][mi]}
            bits.extend(int(pair in edges) for pair in within)
        permutation = record['cross_permutations'][pi]
        bits.extend(int(permutation[i] == j) for i in range(n) for j in range(n))
        if any(initial[column] != bit for column, bit in zip(columns, bits) if column in initial):
            continue
        rows.add(tuple(column+1 if bit else -(column+1)
                       for column, bit in zip(columns, bits) if column not in initial))
    return sorted(rows), {'root_line': root, 'part': list(part),
                         'source': str(source), 'source_sha256': hashlib.sha256(raw).hexdigest(),
                         'canonical_codes': len(canonical), 'compatible_rows': len(rows),
                         'normalization': 'Global mate flips on first-component lines, including interchange of its two stars.',
                         'arbitrary_mate_flips_of_the_fixed_star_allowed': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path)
    p.add_argument('--index', type=int)
    p.add_argument('--root-line', type=int, choices=range(7))
    p.add_argument('--matching-index', type=int)
    p.add_argument('--degree', type=int, default=14)
    p.add_argument('--conflicts', type=int, default=10000)
    p.add_argument('--build-only', action='store_true')
    p.add_argument('--upper-only', action='store_true',
                   help='Equivalent C2 upper bounds using the exact C1 row sums; fewer clauses.')
    p.add_argument('--first-component-table', action='store_true',
                   help='Use matching_global first-component normalization; do not apply unrestricted mate-flip orbits.')
    p.add_argument('--transport-grid-degree', action='store_true',
                   help='Assume global c>=4 and impose at least two grids at each transported root line.')
    p.add_argument('--weighted-root-comparison', action='store_true',
                   help='With grid transport, require the new root score9s+8g to be no smaller.')
    p.add_argument('--output-prefix', type=Path, required=True)
    p.add_argument('--solver', type=Path, default=Path('tools/win64/cadical.exe'))
    p.add_argument('--checker', type=Path, default=Path('tools/win64/drat-trim.exe'))
    a = p.parse_args(); resources = limit_research_process(1)
    assert not a.weighted_root_comparison or a.transport_grid_degree
    prefix = a.output_prefix; prefix.parent.mkdir(parents=True, exist_ok=True)
    assert not prefix.with_suffix('.json').exists()
    initial = {}; rows = None; budget = None; literal_table = None; grid_transport = None
    result = {'scope': __doc__, 'degree': a.degree, 'resources': resources,
              'encoding_version': 'star_cnf_v2_label_counts_and_weighted_score',
              'template_index': a.index, 'root_line': a.root_line, 'matching_index': a.matching_index,
              'normalised_component': False, 'fixed_gram_witness': False,
              'global_conway_exclusion': False}
    if a.directory is not None:
        assert a.degree == 14 and a.index is not None and a.matching_index is not None
        from root_component_propagation import constraints, propagate
        from root_component_complete_star import matching_cover, matching_assignments
        source = a.directory / 'root_component_templates.json'
        raw = source.read_bytes(); template = json.loads(raw)['survivors'][a.index]
        root, parts, _, cover = matching_cover(template, a.root_line)
        assert 0 <= a.matching_index < len(cover)
        matching = cover[a.matching_index]
        propagation = propagate(template, extra_initial=matching_assignments(root, matching))
        assert not propagation['conflict'], 'Handle a propagation contradiction with its own trace.'
        initial = {i: v for i, v, _ in propagation['assignments']}
        equations, bounds, _ = constraints(template); rows = equations, bounds
        grids = 21-len(template['nongrid_edges']); budget = (504-8*grids)//9
        result.update(template=template, root_line=root, component_parts=parts, matching=matching,
                      source_templates=str(source), source_templates_sha256=hashlib.sha256(raw).hexdigest(),
                      root_order='weighted_prisms_grids', root_prism_budget=budget,
                      usable_in_arbitrary_low_budget_root_frontier=False,
                      propagation=propagation)
        if a.first_component_table:
            literal_table, table_info = first_component_table(template, initial, a.directory)
            result.update(normalised_component=True, component_table=table_info)
        if a.transport_grid_degree:
            assert min(template['component_count_by_root_line']) >= 4
            grid_transport = template, root, matching, a.weighted_root_comparison
            result['global_minimum_components'] = 4
    else:
        assert a.index is None and a.matching_index is None and a.root_line is None and not a.first_component_table and not a.transport_grid_degree
    before = time.process_time()
    labels, pairs, graph, info = encode(prefix.with_suffix('.cnf'), a.degree, initial, rows, budget,
                                       a.upper_only, literal_table, grid_transport)
    result.update(encoding=info, build_cpu_seconds=time.process_time()-before, status='CNF_BUILT')
    atomic_json_write(prefix.with_suffix('.json'), result)
    print(json.dumps({'phase': 'built', **info, 'cpu_seconds': result['build_cpu_seconds']}), flush=True)
    if a.build_only:
        return
    solved = solve_file_checked(prefix.with_suffix('.cnf'), prefix, a.conflicts, a.checker, a.solver)
    result.update(solved)
    if solved['status'] == 'SAT_RELAXATION':
        assignment = {}
        for line in Path(solved['solver_log']).read_text().splitlines():
            if line.startswith('v '):
                for value in map(int, line[2:].split()):
                    if value:
                        assignment[abs(value)] = int(value > 0)
        gamma = [[int(value) if type(value) is bool else assignment[value] for value in row]
                 for row in graph]
        from conway_global_cover import reconstruct_and_check
        result['adjacency'] = reconstruct_and_check(a.degree, labels, gamma)
        result['exact_all_pair_check'] = True
        result['status'] = 'CONWAY_GRAPH_FOUND' if a.degree == 14 else 'SRG_FOUND'
    atomic_json_write(prefix.with_suffix('.json'), result)
    print(json.dumps({k: result.get(k) for k in ('status', 'checked_drat', 'solver_cpu_seconds',
                                               'exact_all_pair_check')}), flush=True)


if __name__ == '__main__':
    main()
