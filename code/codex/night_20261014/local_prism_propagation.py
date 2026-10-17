"""Short CNF cuts for every Conway prism star and every rooted grid tile.

No SAT solver is needed for these exact checks. The graph equations are
A^2+A=12I+2J. The norm-14 argument is proved in the current night journal.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import json


def forbid_exactly_one_missing(variables):
    """Exclude weight k-1 among k positive edge variables (k=3 or k=4)."""
    if len(variables) not in (3,4) or len(set(variables)) != len(variables):
        raise ValueError('Three or four distinct positive edge variables required')
    if any(v <= 0 for v in variables):
        raise ValueError('Variables must be positive integers')
    return [[v if i == missing else -v for i,v in enumerate(variables)]
            for missing in range(len(variables))]


def prism_partner_clauses(partners, variable):
    """Partners of one triangle, each tuple ordered by its three base neighbors.

    `variable(u,v)` returns the positive SAT variable of graph edge {u,v}.
    These partners must already be known triangles joined in prism to the
    same base triangle. Alignment is forced by mu=2. This emits zero units
    for off-alignment edges and 3 clauses for the 3 aligned edges per pair.
    """
    if len({v for t in partners for v in t}) != 3*len(partners):
        raise ValueError('Distinct prism partners must be vertex-disjoint')
    clauses = []
    for first,second in combinations(partners,2):
        if len(first) != 3 or len(second) != 3:
            raise ValueError('A partner is an ordered triangle')
        for i,j in product(range(3), repeat=2):
            if i != j:
                clauses.append([-variable(first[i],second[j])])
        clauses.extend(forbid_exactly_one_missing(
            [variable(first[i],second[i]) for i in range(3)]))
    return clauses


def grid_tile_clauses(cycle_edge_variables):
    """Four local matching edges of Q_ij around a fixed vertex: no weight 3."""
    return forbid_exactly_one_missing(cycle_edge_variables)


def graph(order, edges):
    a = [[0]*order for _ in range(order)]
    for i,j in edges:
        a[i][j] = a[j][i] = 1
    return a


def excess_common_neighbor(a):
    for i,j in combinations(range(len(a)),2):
        common = [k for k in range(len(a)) if a[i][k] and a[j][k]]
        allowed = 1 if a[i][j] else 2
        if len(common) > allowed:
            return dict(pair=[i,j], adjacent=bool(a[i][j]), common=common)
    return None


def norm14_obstruction(a):
    """Return a valid norm-14 obstruction for an induced 9-vertex graph.

    General sufficient rule: 17 edges, min degree>=3, and two degree-3
    vertices sharing a degree-4 vertex. On S, f=4-degree; outside S, f<=1.
    All negative values are then >=-1, and positive pairs can have no
    common zero-valued neighbor, by the journal's saturation argument.
    """
    if len(a) != 9:
        return None
    degrees = list(map(sum,a))
    if sum(degrees) != 34 or min(degrees) < 3:
        return None
    for i,j in combinations(range(9),2):
        if degrees[i] == degrees[j] == 3:
            for k in range(9):
                if degrees[k] == 4 and a[i][k] and a[j][k]:
                    return dict(positive_pair=[i,j], zero_common_neighbor=k,
                                norm_squared=14)
    return None


def check():
    truth_tables = {}
    for n in (3,4):
        clauses = forbid_exactly_one_missing(list(range(1,n+1)))
        rejected = []
        for bits in product((False,True),repeat=n):
            satisfied = all(any(bits[abs(v)-1] == (v>0) for v in c)
                            for c in clauses)
            assert satisfied == (sum(bits) != n-1)
            if not satisfied:
                rejected.append(list(map(int,bits)))
        truth_tables[str(n)] = dict(clauses=clauses, rejected=rejected)

    # A-B and B-C are normalized prisms. Enumerate every possible matching
    # from A to C, not only the aligned ones (34 possibilities altogether).
    base = [(3*r+i,3*r+j) for r in range(3) for i,j in combinations(range(3),2)]
    base += [(i,3+i) for i in range(3)] + [(3+i,6+i) for i in range(3)]
    cases = []
    for size in range(4):
        for sources in combinations(range(3),size):
            for targets in permutations(range(3),size):
                matching = list(zip(sources,targets))
                a = graph(9,base+[(i,6+j) for i,j in matching])
                local = excess_common_neighbor(a)
                small_norm = norm14_obstruction(a) if local is None else None
                status = 'local common-neighbor violation' if local else (
                    'norm-14 obstruction' if small_norm else 'passes these necessary cuts')
                if local is None:
                    assert all(i == j for i,j in matching)
                if local is None and small_norm is None:
                    assert size in (0,1,3)
                cases.append(dict(matching=matching, status=status,
                                  witness=local or small_norm))
    counts = {status:sum(c['status']==status for c in cases)
              for status in ('local common-neighbor violation','norm-14 obstruction',
                             'passes these necessary cuts')}
    assert len(cases) == 34 and list(counts.values()) == [26,3,5]

    # The grid tile: delete any one edge of the cell's 4-cycle from a 3x3
    # rook grid. Its two degree-3 vertices have the third point of their
    # grid line as a zero-valued common neighbor.
    rook_edges = [(i,j) for i,j in combinations(range(9),2)
                  if i//3 == j//3 or i%3 == j%3]
    tile = [(4,5),(5,8),(7,8),(4,7)]
    tile_witnesses = []
    for missing in tile:
        a = graph(9,[e for e in rook_edges if e != missing])
        assert excess_common_neighbor(a) is None
        witness = norm14_obstruction(a)
        assert witness is not None
        tile_witnesses.append(dict(missing=missing, **witness))

    variable_pairs = list(combinations(range(6),2))
    variables = {pair:i+1 for i,pair in enumerate(variable_pairs)}
    star_clauses = prism_partner_clauses([(0,1,2),(3,4,5)],
        lambda x,y: variables[tuple(sorted((x,y)))])
    assert len(star_clauses) == 9
    return dict(status='exact checks pass', triple_triangle_cases=counts,
                cases=cases, truth_tables=truth_tables,
                grid_tile_witnesses=tile_witnesses,
                general_consequence='R squared is zero on intersecting triangle pairs and on disjoint triangle pairs joined by exactly two edges',
                solver_size=dict(prism_partner_pair='6 units and 3 ternary clauses',
                                 rooted_grid_tile='4 clauses of length 4',
                                 all_rooted_grid_tiles='99*21*4 = 8316 clauses before duplicate removal, if all local coordinates exist'),
                scope='Necessary propagation only; no completion or entire C1 exclusion')


if __name__ == '__main__':
    report = check()
    out = Path('data/codex_night_20261014/local_prism_propagation.json')
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ('cases','truth_tables','grid_tile_witnesses')},indent=2))
