"""Necessary profile constraints for extra rooted grids, without fixing matchings.

For a grid Qij in a rooted SRG(v,2r,1,2), every vertex outside Qij whose
roots meet {i,j} has zero neighbours in it. All other vertices have at
most one; for r=7 they all have exactly one. The r=7 equality must not
be imposed on the positive SRG243 control (r=11).
"""

from itertools import combinations, product

if not __debug__:
    raise RuntimeError('Grid-profile constraints require assertions; do not use python -O.')


def encode(rows, known, outside, domains, profile_literals, grid_roots,
           pool, exactly, root_count=7, physical_edges=()):
    from pysat.card import CardEnc, EncType
    grids = [tuple(sorted(g)) for g in grid_roots]
    assert len(set(grids)) == len(grids)
    assert all(len(g) == 2 and g[0] != g[1] and set(g) <= set(range(root_count)) for g in grids)
    lookup = {tuple(q): y for y, q in enumerate(outside)}
    assert len(lookup) == len(outside)
    clauses, cells, fixed, components = [], {}, {}, []

    def cell(y, u):
        if (y, u) not in cells:
            lits = [profile_literals[y][pi] for pi, p in enumerate(domains[y]) if u in p]
            if not lits:
                cells[y, u] = False
            elif len(lits) == len(domains[y]):
                cells[y, u] = True
            else:
                v = pool.new(); cells[y, u] = v
                clauses.append([-v] + lits)
                clauses.extend([-p, v] for p in lits)
        return cells[y, u]

    def card(terms, target, equality=False):
        target -= sum(v is True for v in terms)
        lits = [v for v in terms if v is not True and v is not False]
        if equality:
            clauses.extend(exactly(lits, target, pool))
        elif target < 0:
            clauses.append([])
        elif target < len(lits):
            cnf = CardEnc.atmost(lits, bound=target, top_id=pool.top, encoding=EncType.seqcounter)
            pool.top = max(pool.top, cnf.nv)
            clauses.extend(cnf.clauses)

    for i, j in grids:
        labels = [(2 * i + a, 2 * j + b) for a, b in product(range(2), repeat=2)]
        assert all(q in lookup for q in labels), 'All four grid corners must be outside the known block.'
        corners = [lookup[q] for q in labels]
        neighbours = {x: [y for y in corners if x != y and len(set(outside[x]) & set(outside[y])) == 1]
                      for x in corners}
        for x, y in combinations(corners, 2):
            key = tuple(sorted((x, y)))
            value = y in neighbours[x]
            assert key not in fixed or fixed[key] == value
            fixed[key] = value
        for u, q in enumerate(known):
            meet = bool({l // 2 for l in q} & {i, j})
            # No existing known vertex is a corner of this outside grid.
            card([cell(x, u) for x in corners], 0 if meet else 1,
                 equality=meet or root_count == 7)
        for x in corners:
            card([cell(x, u) for u in range(len(rows))], 2 * root_count - 4)
            # The two fixed grid neighbours already use part of the row quotas.
            for l in range(2 * root_count):
                target = 1 if l // 2 in {i, j} else 2
                target -= sum(l in outside[y] for y in neighbours[x])
                card([cell(x, u) for u, q in enumerate(known) if l in q], target)
            for u, row in enumerate(rows):
                terms = [cell(x, u)]
                terms += [cell(x, v) for v in range(len(rows)) if row & (1 << v)]
                terms += [cell(y, u) for y in neighbours[x]]
                card(terms, 2 - len(set(outside[x]) & set(known[u])))
        components.append({'root_pair': [i, j], 'outside_corners': corners})
    linked = []
    for x, y, v in physical_edges:
        key = tuple(sorted((x, y)))
        if key in fixed:
            clauses.append([v if fixed[key] else -v])
            linked.append([x, y, v, fixed[key]])
    return clauses, {
        'grids': components, 'forced_edges': [[x, y, value] for (x, y), value in sorted(fixed.items())],
        'linked_physical_edges': linked, 'exact_disjoint_domination': root_count == 7,
        'added_clauses': len(clauses), 'known_edge_indicators': len(cells),
        'scope': 'Necessary profile projection and partial SRG bounds for assumed grids; matching choices remain free.',
        'all_new_grid_rows_completed': False}


def controls(complete_grid_rows=False):
    """Preserve an actual BVLS243 grid and reject a forbidden chosen profile."""
    from pathlib import Path
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    from root_component_row_cut_positive_controls import load_graph, rooted_block
    root = Path(__file__).resolve().parents[2]
    graph = load_graph(root / 'data/srg243/bvls243.edges')
    _, _, labels, _, future, _, _ = rooted_block(graph, 0, 0, 191024)
    lookup = {tuple(q): v for v, q in enumerate(labels)}
    corners = [lookup[2 * i + a, 2 * j + b] for i, j in [(0, 1)]
               for a, b in product(range(2), repeat=2)]
    assert all((v in future[u]) == (len(set(labels[u]) & set(labels[v])) == 1)
               for u, v in combinations(corners, 2))
    known_ids = [v for v in range(len(labels)) if v not in corners]
    known = [labels[v] for v in known_ids]
    outside = [labels[v] for v in corners]
    rows = [sum(1 << u for u, w in enumerate(known_ids) if w in future[v]) for v in known_ids]
    actual = [[u for u, w in enumerate(known_ids) if w in future[v]] for v in corners]
    forbidden = next(u for u, q in enumerate(known) if {l // 2 for l in q} & {0, 1})
    assert forbidden not in actual[0]
    domains = [[p] for p in actual]
    domains[0].append(sorted(actual[0] + [forbidden]))
    class Pool:
        top = 0
        def new(self):
            self.top += 1
            return self.top
    pool = Pool()
    literals = [[pool.new() for _ in d] for d in domains]
    def exactly(lits, target, pool):
        if not 0 <= target <= len(lits):
            return [[]]
        cnf = CardEnc.equals(lits, bound=target, top_id=pool.top, encoding=EncType.seqcounter)
        pool.top = max(pool.top, cnf.nv)
        return cnf.clauses
    cnf, info = encode(rows, known, outside, domains, literals, [(0, 1)], pool, exactly, root_count=11)
    if complete_grid_rows:
        from root_component_profile_row_extension import extend_rows
        from root_component_signed_internal_core import encode as encode_core
        extra, core = encode_core(rows, known, outside, domains, literals, [0, 1, 2],
                                  pool, exactly, root_count=11)
        cnf.extend(extra)
        extra, extension = extend_rows(rows, known, outside, domains, literals,
                                        range(len(outside)), pool, exactly, root_count=11)
        cnf.extend(extra)
        other = {(x, y): v for x, y, v in extension['edge_variables']}
        for x, y, v in core['edge_variables']:
            w = other[x, y]
            cnf.extend([[-v, w], [v, -w]])
        for x, y, value in info['forced_edges']:
            cnf.append([other[x, y] if value else -other[x, y]])
    units = [[v if pi == 0 else -v] for d in literals for pi, v in enumerate(d)]
    with Solver(name='g3', bootstrap_with=cnf+units) as solver:
        assert solver.solve(), 'A real SRG243 grid must be retained without Conway-only domination.'
    wrong = [[literals[0][1]], [-literals[0][0]]] + [[d[0]] for d in literals[1:]]
    with Solver(name='g3', bootstrap_with=cnf+wrong) as solver:
        assert not solver.solve(), 'A profile touching a forbidden root cannot be part of the grid.'
    counts = [sum(v in future[w] for v in corners) for w in known_ids
              if not ({l // 2 for l in labels[w]} & {0, 1})]
    assert counts.count(0) == 72 and counts.count(1) == 72
    return {'actual_srg243_grid_preserved': True, 'forbidden_profile_rejected': True,
            'root_count': 11, 'disjoint_known_vertices_with_zero_grid_neighbours': counts.count(0),
            'disjoint_known_vertices_with_one_grid_neighbour': counts.count(1),
            'exact_conway_domination_applied': info['exact_disjoint_domination'],
            'joint_signed_core_and_complete_grid_rows': complete_grid_rows,
            'clauses': len(cnf)}
