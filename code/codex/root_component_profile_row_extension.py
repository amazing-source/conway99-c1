"""Complete selected additional rows while keeping all profile choices free.

Add edges incident to the requested outside vertices. For these rows,
impose degree, upper-letter quotas, and exact common-neighbour counts
with every known row and with each other new row. This is a necessary
relaxation of a full SRG completion, with no new symmetry assumption.
"""

from itertools import combinations
from root_component_p3_neighbor_support import prepare_profile, edge_failure


def extend_rows(rows, known_labels, outside_labels, domains, profile_literals,
                hubs, pool, exactly, root_count=7, known_pairs_only=False):
    hubs = tuple(sorted(set(hubs)))
    assert all(0 <= h < len(domains) for h in hubs)
    clauses = []; cells = {}; edges = {}; products = {}

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
                clauses.extend([-x, v] for x in lits)
        return cells[y, u]

    def edge(x, y):
        if x == y:
            return False
        assert x in hubs or y in hubs
        key = tuple(sorted((x, y)))
        if key not in edges:
            edges[key] = pool.new()
        return edges[key]

    def both(a, b):
        if a is False or b is False:
            return False
        if a is True:
            return b
        if b is True or a == b:
            return a
        key = tuple(sorted((a, b)))
        if key not in products:
            v = pool.new(); products[key] = v
            clauses.extend([[-v, a], [-v, b], [-a, -b, v]])
        return products[key]

    def equal(terms, target):
        fixed = sum(v is True for v in terms)
        lits = [v for v in terms if v is not True and v is not False]
        clauses.extend(exactly(lits, target-fixed, pool))

    for h in hubs:
        q = outside_labels[h]; roots = {l // 2 for l in q}
        equal([edge(h, y) for y in range(len(domains))] + [cell(h, u) for u in range(len(rows))],
              2*root_count-2)
        for l in range(2*root_count):
            equal([edge(h, y) for y, lab in enumerate(outside_labels) if l in lab]
                  + [cell(h, u) for u, lab in enumerate(known_labels) if l in lab],
                  1 if l // 2 in roots else 2)
        for u, row in enumerate(rows):
            terms = [cell(h, u)]
            terms += [cell(h, v) for v in range(len(rows)) if row & (1 << v)]
            terms += [both(edge(h, y), cell(y, u)) for y in range(len(domains))]
            equal(terms, 2-len(set(q) & set(known_labels[u])))
    if known_pairs_only:
        assert hubs == tuple(range(len(domains)))
        # Joint symmetric continuation of every profile, without the cubic
        # expansion of all still unknown outside/outside common-neighbour counts.
        partial_start = len(clauses)
        prepared = [[prepare_profile(rows, known_labels, q, p, root_count) for p in domain]
                    for q, domain in zip(outside_labels, domains)]
        for x, y in combinations(hubs, 2):
            variable = edge(x, y)
            for pi, a in enumerate(prepared[x]):
                for qi, b in enumerate(prepared[y]):
                    if edge_failure(a, b) is not None:
                        clauses.append([-profile_literals[x][pi], -profile_literals[y][qi], -variable])
        return clauses, {'hubs': hubs, 'hub_labels': list(outside_labels),
                         'edge_variables': [[x, y, v] for (x, y), v in edges.items()],
                         'added_clauses': len(clauses), 'partial_srg_clauses': len(clauses)-partial_start,
                         'known_edge_indicators': len(cells), 'common_neighbour_products': len(products),
                         'mode': 'ALL_ROWS_KNOWN_PAIR_QUOTAS_ONLY',
                         'all_outside_pair_equations_imposed': False}
    for h, k in combinations(hubs, 2):
        terms = [edge(h, k)] + [both(cell(h, u), cell(k, u)) for u in range(len(rows))]
        terms += [both(edge(h, y), edge(k, y)) for y in range(len(domains))]
        equal(terms, 2-len(set(outside_labels[h]) & set(outside_labels[k])))

    # Adding rows must also preserve all partial SRG inequalities on the
    # still unfinished rows. Each event is a conjunction of edge/cell
    # literals. A forbidden (target+1)-subset gives one guarded clause.
    partial_start = len(clauses)
    def guarded_atmost(guards, events, target):
        clean = []
        for event in events:
            if any(v is False for v in event):
                continue
            clean.append([v for v in event if v is not True])
        if target < 0:
            clauses.append([-v for v in guards]); return
        for subset in combinations(clean, target+1):
            clauses.append([-v for v in guards] + list(dict.fromkeys(-v for event in subset for v in event)))

    prepared = [[prepare_profile(rows, known_labels, q, p, root_count) for p in domain]
                for q, domain in zip(outside_labels, domains)]
    for y, domain in enumerate(domains):
        if y in hubs:
            continue
        roots = {l // 2 for l in outside_labels[y]}
        for pi, p in enumerate(domain):
            chosen = profile_literals[y][pi]; info = prepared[y][pi]
            for u, row in enumerate(rows):
                slack = 2-int(u in p)-len(set(outside_labels[y]) & set(known_labels[u]))-(info['mask'] & row).bit_count()
                guarded_atmost([chosen], [[edge(h, y), cell(h, u)] for h in hubs], slack)
            for l in range(2*root_count):
                slack = (1 if l // 2 in roots else 2)-sum(l in known_labels[u] for u in p)
                guarded_atmost([chosen], [[edge(h, y)] for h in hubs if l in outside_labels[h]], slack)
    for x, y in combinations(range(len(domains)), 2):
        events = [[edge(h, x), edge(h, y)] for h in hubs]
        if x in hubs or y in hubs:
            events.append([edge(x, y)])
        shared = len(set(outside_labels[x]) & set(outside_labels[y]))
        for pi, a in enumerate(prepared[x]):
            for qi, b in enumerate(prepared[y]):
                target = 2-shared-(a['mask'] & b['mask']).bit_count()
                guarded_atmost([profile_literals[x][pi], profile_literals[y][qi]], events, target)
    return clauses, {'hubs': hubs, 'hub_labels': [outside_labels[h] for h in hubs],
                     'edge_variables': [[x, y, v] for (x, y), v in edges.items()],
                     'added_clauses': len(clauses), 'partial_srg_clauses': len(clauses)-partial_start,
                     'known_edge_indicators': len(cells),
                     'common_neighbour_products': len(products)}


def materialize_extension(rows, known_labels, outside_labels, profiles, extension, positive):
    hubs = extension['hubs']; old_n = len(rows)
    remaining = [y for y in range(len(profiles)) if y not in hubs]
    actual = {tuple(sorted((x, y))): (v in positive) for x, y, v in extension['edge_variables']}
    def edge(x, y):
        return x != y and actual[tuple(sorted((x, y)))]
    new_rows = [row | sum(1 << (old_n+i) for i, h in enumerate(hubs) if u in profiles[h])
                for u, row in enumerate(rows)]
    for h in hubs:
        new_rows.append(sum(1 << u for u in profiles[h])
                        | sum(1 << (old_n+i) for i, k in enumerate(hubs) if edge(h, k)))
    new_profiles = [list(profiles[y])+[old_n+i for i, h in enumerate(hubs) if edge(h, y)] for y in remaining]
    return {'rows': new_rows, 'known_labels': list(known_labels)+[outside_labels[h] for h in hubs],
            'outside_labels': [outside_labels[y] for y in remaining], 'profiles': new_profiles,
            'promoted_outside_indices': list(hubs)}


def controls(known_pairs_only=False):
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    class Pool:
        top = 4
        def new(self):
            self.top += 1
            return self.top
    def eq(lits, target, pool):
        if not 0 <= target <= len(lits):
            return [[]]
        cnf = CardEnc.equals(lits, target, top_id=pool.top, encoding=EncType.seqcounter)
        pool.top = max(pool.top, cnf.nv)
        return cnf.clauses
    known = [(0, 2)]; outside = [(0, 3), (1, 2), (1, 3)]
    domains = [[[0]], [[0]], [[], [0]]]; literals = [[1], [2], [3, 4]]
    hubs = [0, 1, 2] if known_pairs_only else [0, 2]
    clauses, extension = extend_rows([0], known, outside, domains, literals, hubs, Pool(), eq, 2, known_pairs_only)
    with Solver(name='g3', bootstrap_with=clauses+[[1], [2], [3], [-4]]) as solver:
        assert solver.solve()
        actual = {v for v in solver.get_model() if v > 0}
        data = materialize_extension([0], known, outside, [[0], [0], []], extension, actual)
        if known_pairs_only:
            assert data['rows'] == [6, 9, 9, 6] and data['profiles'] == []
        else:
            assert data['rows'] == [2, 5, 2]
            assert data['profiles'] == [[0, 2]]
    return {'actual_rook_completion_extended': True, 'known_rows': len(data['rows']),
            'remaining_vertices': len(data['profiles']), 'known_pairs_only': known_pairs_only}
