"""A small internal core from a signed sum of upper-letter quotas.

Choose root indices S. Partition Gamma into A (two S roots), M (one),
and B (none). For every u,
    neighbours_B(u)-neighbours_A(u) = 2r-2-4|S|+2|roots(u) intersect S|.
This is degree minus the sum of letter quotas over S. Introduce only
the unknown edges inside C=(A union B) minus the already known block;
the M edges cancel. Add all SRG upper bounds visible inside K union C.
In 2K2N with S={0,1,2}, C has 20 vertices, and its internal signed
degree is exactly 2 at each vertex. No graph symmetry is assumed.
"""

from itertools import combinations, product

if not __debug__:
    raise RuntimeError('Signed-core checks require assertions; do not use python -O.')


def encode(rows, known, outside, domains, profile_literals, selected_roots,
           pool, exactly, root_count=7, forbid_q12_grid=False):
    from pysat.card import CardEnc, EncType
    roots = set(selected_roots)
    assert roots and roots < set(range(root_count))
    assert all(len(q) == 2 and q[0]//2 != q[1]//2 for q in list(known)+list(outside))
    labels = [tuple(q) for q in list(known)+list(outside)]
    expected = {(2*i+a, 2*j+b) for i, j in combinations(range(root_count), 2)
                for a, b in product(range(2), repeat=2)}
    assert len(labels) == len(expected) and set(labels) == expected, 'Account for every Gamma vertex.'
    def score(q):
        return 1-sum(l//2 in roots for l in q)
    known_score = [score(q) for q in known]
    outside_score = [score(q) for q in outside]
    core = [u for u, s in enumerate(outside_score) if s]
    positive = [u for u in core if outside_score[u] == 1]
    negative = [u for u in core if outside_score[u] == -1]
    clauses = []; cells = {}; edges = {}; products = {}; bounds = set()

    def cell(y, u):
        if (y, u) not in cells:
            lits = [profile_literals[y][pi] for pi, p in enumerate(domains[y]) if u in p]
            if not lits:
                cells[y, u] = False
            elif len(lits) == len(domains[y]):
                cells[y, u] = True
            else:
                var = pool.new(); cells[y, u] = var
                clauses.append([-var]+lits)
                clauses.extend([-p, var] for p in lits)
        return cells[y, u]

    def edge(x, y):
        if x == y:
            return False
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
            var = pool.new(); products[key] = var
            clauses.extend([[-var, a], [-var, b], [-a, -b, var]])
        return products[key]

    def negate(a):
        return not a if isinstance(a, bool) else -a

    def cleaned(terms, target):
        return ([v for v in terms if v is not True and v is not False],
                target-sum(v is True for v in terms))

    def equal(terms, target):
        lits, residual = cleaned(terms, target)
        clauses.extend(exactly(lits, residual, pool))

    def atmost(terms, target):
        lits, residual = cleaned(terms, target)
        if residual < 0:
            clauses.append([])
            return
        if residual >= len(lits):
            return
        key = (tuple(sorted(lits)), residual)
        if key in bounds:
            return
        bounds.add(key)
        cnf = CardEnc.atmost(lits, bound=residual, top_id=pool.top, encoding=EncType.seqcounter)
        pool.top = max(pool.top, cnf.nv); clauses.extend(cnf.clauses)

    for x in core:
        rhs = 2*root_count-2-4*len(roots)+2*sum(l//2 in roots for l in outside[x])
        plus = [edge(x, y) for y in positive if y != x]
        plus += [cell(x, u) for u, s in enumerate(known_score) if s == 1]
        minus = [edge(x, y) for y in negative if y != x]
        minus += [cell(x, u) for u, s in enumerate(known_score) if s == -1]
        equal(plus+[negate(v) for v in minus], rhs+len(minus))
        # Upper bounds for the known row / new core row pairs.
        for u, row in enumerate(rows):
            terms = [cell(x, u)]
            terms += [cell(x, v) for v in range(len(rows)) if row & (1 << v)]
            terms += [both(edge(x, y), cell(y, u)) for y in core if y != x]
            atmost(terms, 2-len(set(outside[x]) & set(known[u])))
        for l in range(2*root_count):
            terms = [cell(x, u) for u, q in enumerate(known) if l in q]
            terms += [edge(x, y) for y in core if y != x and l in outside[y]]
            atmost(terms, 1 if l//2 in {v//2 for v in outside[x]} else 2)
        atmost([cell(x, u) for u in range(len(rows))]+[edge(x, y) for y in core if y != x], 2*root_count-2)
    for x, y in combinations(core, 2):
        terms = [edge(x, y)]
        terms += [both(cell(x, u), cell(y, u)) for u in range(len(rows))]
        terms += [both(edge(x, z), edge(y, z)) for z in core if z not in (x, y)]
        atmost(terms, 2-len(set(outside[x]) & set(outside[y])))
    if forbid_q12_grid:
        assert root_count == 7 and roots == {0, 1, 2}
        assert len(negative) == 4 and {tuple(l//2 for l in outside[u]) for u in negative} == {(1, 2)}
        assert len(core) == 20
        # Under 2K2N, 4 or more Q12 edges would give the already excluded
        # 2K2 family. The caller must establish the 2K2N family hypotheses.
        atmost([edge(x, y) for x, y in combinations(negative, 2)], 3)
    return clauses, {'root_subset': sorted(roots), 'core_indices': core,
                     'positive_indices': positive, 'negative_indices': negative,
                     'edge_variables': [[x, y, v] for (x, y), v in sorted(edges.items())],
                     'added_clauses': len(clauses), 'products': len(products),
                     'forbid_q12_grid': forbid_q12_grid,
                     'scope': 'Necessary signed internal-core equations and partial SRG upper bounds.'}


def encode_many(rows, known, outside, domains, profile_literals, root_subsets,
                pool, exactly, root_count=7, forbid_q12_grid=False):
    """Couple several necessary cores through identical physical edges.

    Profile literals are already shared. Every duplicate edge variable is
    equated to its first representative; independent edge assignments on
    overlapping cores would only give a weaker relaxation.
    """
    subsets = [sorted(set(s)) for s in root_subsets]
    assert subsets and len({tuple(s) for s in subsets}) == len(subsets)
    if len(subsets) == 1:
        return encode(rows, known, outside, domains, profile_literals, subsets[0],
                      pool, exactly, root_count, forbid_q12_grid)
    assert not forbid_q12_grid, 'The Q12 exclusion is currently exposed only for a single 2K2N core.'
    clauses, components, representatives, links = [], [], {}, []
    for roots in subsets:
        extra, info = encode(rows, known, outside, domains, profile_literals,
                             roots, pool, exactly, root_count)
        clauses.extend(extra)
        components.append(info)
        for x, y, v in info['edge_variables']:
            key = (x, y)
            if key in representatives:
                w = representatives[key]
                clauses.extend([[-v, w], [v, -w]])
                links.append([v, w])
            else:
                representatives[key] = v
    return clauses, {
        'root_subsets': subsets, 'components': components,
        'core_indices': sorted({x for c in components for x in c['core_indices']}),
        'edge_variables': [[x, y, v] for (x, y), v in sorted(representatives.items())],
        'shared_edge_equalities': links, 'added_clauses': len(clauses),
        'products': sum(c['products'] for c in components),
        'forbid_q12_grid': False,
        'scope': 'Necessary signed cores with common profile literals and identified shared edges.'}


def controls(all_known_pair_rows=False, root_subsets=None):
    from pathlib import Path
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    from root_component_row_cut_positive_controls import load_graph, rooted_block
    root = Path(__file__).resolve().parents[2]
    graph = load_graph(root/'data/srg243/bvls243.edges')
    rows, known, outside, domains, future, _, _ = rooted_block(graph, 1, 210 if all_known_pair_rows else 180, 191020)
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
    cnf, info = encode_many(rows, known, outside, domains, literals,
                            root_subsets or [[0, 1, 2]], pool, exactly, root_count=11)
    all_info = None
    if all_known_pair_rows:
        from root_component_profile_row_extension import extend_rows
        extra, all_info = extend_rows(rows, known, outside, domains, literals, range(len(outside)),
                                      pool, exactly, root_count=11, known_pairs_only=True)
        cnf.extend(extra)
        other = {(x, y): v for x, y, v in all_info['edge_variables']}
        for x, y, v in info['edge_variables']:
            w = other[x, y]; cnf.extend([[-v, w], [v, -w]])
    units = [[literal if pi == 0 else -literal] for d in literals for pi, literal in enumerate(d)]
    units += [[v if y in future[x] else -v] for x, y, v in info['edge_variables']]
    if all_info:
        units += [[v if y in future[x] else -v] for x, y, v in all_info['edge_variables']]
    with Solver(name='g3', bootstrap_with=cnf+units) as solver:
        assert solver.solve(), 'The actual SRG243 and its edges must satisfy the same encoder.'
    # Aliases must equal the representatives even when profiles are held fixed.
    # This tests the coupling, rather than merely checking two separate cores.
    alias_control = None
    if info.get('shared_edge_equalities'):
        v, w = info['shared_edge_equalities'][0]
        with Solver(name='g3', bootstrap_with=cnf+units+[[v, w], [-v, -w]]) as solver:
            assert not solver.solve(), 'One physical edge cannot take two values.'
        alias_control = True
    return {'actual_srg243_with_fixed_real_edges_passes': True, 'root_count': 11,
            'core_vertices': len(info['core_indices']), 'core_edges': len(info['edge_variables']),
            'clauses': len(cnf), 'q12_family_exclusion_applied_to_243': False,
            'component_count': len(info.get('components', [info])),
            'shared_edge_equalities': len(info.get('shared_edge_equalities', [])),
            'opposite_alias_values_rejected': alias_control}
