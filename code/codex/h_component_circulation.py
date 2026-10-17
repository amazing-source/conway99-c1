"""Exact orientation criterion inside a pair of ordinary line components.

Use the producer's component partitions. For W in H_l not containing m and
Z in H_m not containing l, their even component kernels force zero column
sums of B on L_W and R_Z separately. Each broken h-edge-orbit is one signed
edge in a bipartite multigraph on L_W and R_Z; a doubly broken block has both
the parallel and the crossed edge. This module tests precisely these linear
component equations, not C1/C2, positivity, or global graph existence.
"""
import argparse
from itertools import product
import json
from pathlib import Path
import random

import sympy as sp
from sympy.polys.matrices import DomainMatrix


def classify_tile(channels, left_nodes, right_nodes):
    """Necessary AND sufficient for the tile's component-sum equations.

    Nodes are h-orbits, not individual graph vertices. In the ordering L<R,
    a parallel channel contributes -epsilon at both ends, a crossed channel
    contributes -epsilon at L and +epsilon at R (twice the relevant B entry).
    The result includes a constructive sign assignment when one exists.
    """
    channels = [tuple(item) for item in channels]
    left, right = set(left_nodes), set(right_nodes)
    if left & right:
        raise ValueError('Disjoint left and right orbit sets are required.')
    if len(set(channels)) != len(channels):
        raise ValueError('A channel may occur only once; parallel and crossed may coexist.')
    adjacency = {}
    for edge, (i, j, kind) in enumerate(channels):
        if i not in left or j not in right or kind not in ('parallel', 'crossed'):
            raise ValueError('Expected channels (left_node,right_node,parallel/crossed).')
        adjacency.setdefault(i, []).append(edge)
        adjacency.setdefault(j, []).append(edge)

    def other(edge, vertex):
        i, j, _ = channels[edge]
        return j if vertex == i else i

    def coefficient(edge, vertex):
        i, j, kind = channels[edge]
        return -1 if vertex == i or kind == 'parallel' else 1

    unseen = set(adjacency)
    components = []
    while unseen:
        root = min(unseen)
        vertices, edges, stack = {root}, set(), [root]
        unseen.remove(root)
        while stack:
            vertex = stack.pop()
            for edge in adjacency[vertex]:
                edges.add(edge)
                neighbour = other(edge, vertex)
                if neighbour not in vertices:
                    vertices.add(neighbour)
                    unseen.remove(neighbour)
                    stack.append(neighbour)
        components.append((sorted(vertices), sorted(edges)))

    details = []
    equations_rank = 0
    obstructed = False
    signs = [None]*len(channels)
    for vertices, edges in components:
        odd_degrees = [v for v in vertices if len(adjacency[v]) % 2]
        crossed = sum(channels[e][2] == 'crossed' for e in edges)
        # A row dependence requires y_L=-s_e*y_R, where s_e=+1 parallel,
        # -1 crossed. It survives iff every cycle has even crossed parity.
        potential = {vertices[0]: 1}
        stack, balanced = [vertices[0]], True
        while stack:
            v = stack.pop()
            for edge in adjacency[v]:
                w = other(edge, v)
                wanted = -coefficient(edge, v)*coefficient(edge, w)*potential[v]
                if w in potential:
                    balanced &= potential[w] == wanted
                else:
                    potential[w] = wanted
                    stack.append(w)
        rank = len(vertices)-int(balanced)
        equations_rank += rank
        possible = not odd_degrees and crossed % 2 == 0
        obstructed |= not possible
        detail = dict(vertices=vertices, edges=len(edges), crossed_channels=crossed,
                      odd_degree_vertices=odd_degrees, every_cycle_even_crossed=bool(balanced),
                      equation_rank=rank, sign_dimension=len(edges)-rank,
                      component_equations_solvable=possible)
        details.append(detail)
        if not possible:
            continue

        # Hierholzer's walk works with parallel edges because edges have IDs.
        remaining = {v: list(adjacency[v]) for v in vertices}
        used = set()
        walk_vertices, incoming = [vertices[0]], [None]
        reverse_vertices, reverse_edges = [], []
        while walk_vertices:
            v = walk_vertices[-1]
            while remaining[v] and remaining[v][-1] in used:
                remaining[v].pop()
            if remaining[v]:
                edge = remaining[v].pop()
                used.add(edge)
                walk_vertices.append(other(edge, v))
                incoming.append(edge)
            else:
                reverse_vertices.append(walk_vertices.pop())
                edge = incoming.pop()
                if edge is not None:
                    reverse_edges.append(edge)
        tour_vertices = list(reversed(reverse_vertices))
        tour_edges = list(reversed(reverse_edges))
        assert len(tour_edges) == len(edges) and tour_vertices[0] == tour_vertices[-1]
        signs[tour_edges[0]] = 1
        for k in range(1, len(tour_edges)):
            previous, edge, vertex = tour_edges[k-1], tour_edges[k], tour_vertices[k]
            signs[edge] = -coefficient(previous, vertex)*coefficient(edge, vertex)*signs[previous]
        root = tour_vertices[0]
        assert coefficient(tour_edges[-1], root)*signs[tour_edges[-1]] + coefficient(tour_edges[0], root)*signs[tour_edges[0]] == 0

    if not obstructed:
        assert all(sum(coefficient(e, v)*signs[e] for e in adjacency[v]) == 0 for v in adjacency)
    dimension = len(channels)-equations_rank
    return dict(status='NO_ORIENTATION_FOR_COMPONENT_EQUATIONS' if obstructed else 'COMPONENT_EQUATIONS_SOLVABLE',
                channels=len(channels), active_vertices=len(adjacency), components=details,
                linear_rank=equations_rank, linear_dimension=dimension,
                sign_assignment=signs if not obstructed else None,
                sign_trial_bound=0 if obstructed else 2**dimension,
                scope='Necessary and sufficient ONLY for these component column-sum equations. Full star equations, graph admissibility, positivity and rank are additional. The component partitions must be supplied correctly; active components meeting the other root line need extra O terms.')


def report():
    square = [(0, 3, 'parallel'), (1, 3, 'parallel'),
              (1, 4, 'parallel'), (0, 4, 'parallel')]
    one_bad = [(0, 3, 'crossed')]+square[1:]
    two_shared = one_bad+[(0, 5, 'crossed'), (2, 5, 'parallel'),
                          (2, 6, 'parallel'), (0, 6, 'parallel')]
    two_disjoint = one_bad+[(2, 5, 'crossed'), (7, 5, 'parallel'),
                            (7, 6, 'parallel'), (2, 6, 'parallel')]
    doubled_pair = [(0, 3, 'parallel'), (0, 3, 'crossed')]
    two_doubled = doubled_pair+[(0, 4, 'parallel'), (0, 4, 'crossed')]
    cases = {}
    for name, channels, left in (
            ('ordinary_square', square, [0, 1]),
            ('one_odd_crossed_square', one_bad, [0, 1]),
            ('two_odd_squares_sharing_vertex', two_shared, [0, 1, 2]),
            ('two_odd_squares_disjoint', two_disjoint, [0, 1, 2, 7]),
            ('isolated_double_break', doubled_pair, [0]),
            ('two_double_breaks_sharing_vertex', two_doubled, [0])):
        cases[name] = classify_tile(channels, left, [3, 4, 5, 6])
    assert cases['ordinary_square']['linear_dimension'] == 1
    for name in ('one_odd_crossed_square', 'two_odd_squares_disjoint', 'isolated_double_break'):
        assert cases[name]['status'] == 'NO_ORIENTATION_FOR_COMPONENT_EQUATIONS'
    for name in ('two_odd_squares_sharing_vertex', 'two_double_breaks_sharing_vertex'):
        assert cases[name]['status'] == 'COMPONENT_EQUATIONS_SOLVABLE'
        assert cases[name]['linear_dimension'] == 1
    # Independent literal sign census on new small channel multigraphs.
    rng = random.Random(803)
    all_channels = [(i, j, kind) for i in range(3) for j in range(3, 6)
                    for kind in ('parallel', 'crossed')]
    for trial in range(32):
        channels = rng.sample(all_channels, trial % 9)
        result = classify_tile(channels, range(3), range(3, 6))
        matrix = sp.zeros(6, len(channels))
        for k, (i, j, kind) in enumerate(channels):
            matrix[i, k], matrix[j, k] = -1, -1 if kind == 'parallel' else 1
        assert DomainMatrix.from_Matrix(matrix).rank() == result['linear_rank']
        count = sum(all(sum(int(matrix[i, j])*signs[j] for j in range(len(channels))) == 0 for i in range(6))
                    for signs in product((-1, 1), repeat=len(channels)))
        assert bool(count) == (result['status'] == 'COMPONENT_EQUATIONS_SOLVABLE')
        assert count <= result['sign_trial_bound']
    return dict(status='EXACT_COMPONENT_TILE_CIRCULATION_CRITERION',
                hypotheses='Two ordinary component indicators kappa_W,kappa_Z are in kerT and h-even; W does not contain m, Z does not contain l. Work in their rectangular L_W x R_Z tile, with all broken h-edge-orbits included, including both channels for a doubly broken block.',
                theorem='The tile component equations admit signs iff every active vertex has even channel degree and every connected component has an even number of crossed channels.',
                dimension='For E channels and V active vertices, rank=V-c_bal, where c_bal is the number of connected components in which every cycle has even crossed parity. Therefore the exact linear dimension is E-V+c_bal. Balanced total crossed parity and balanced every-cycle parity are different conditions.',
                proof=[
                    'The two even kernel indicators give B^T*kappa_W=B^T*kappa_Z=0. For each channel between i in L_W and j in R_Z, twice its endpoint coefficients are(-1,-1) for parallel,(-1,+1) for crossed. Thus the equations are a signed incidence system in signs epsilon.',
                    'A vertex sum of signs can vanish only at even degree. In a connected component, sum the equations on the L side and on the R side, then subtract: the sum of epsilon over crossed channels is zero. Their number must be even.',
                    'Conversely, all even degrees give a closed Euler tour. Assign a sign to its first edge; at each successive vertex, assign the next sign so the two consecutive endpoint contributions cancel. Closing the tour is consistent iff (-1)^E times the product of endpoint ratios is+1. E is even in an Eulerian bipartite graph, so this is precisely even crossed parity. All vertex contributions cancel pairwise, including repeated visits and parallel edges.',
                    'A row dependence propagates y_j=-s_e*y_i, s_e=+1 parallel and-1 crossed. It has one free coordinate on a connected component iff all cycle crossed parities are even, otherwise none. This proves the rank formula without an eigenvalue calculation.',
                    'Two individually obstructed odd-crossed squares sharing a vertex can support a joint circulation: each square alone cannot cancel at the shared vertex, while their contributions can cancel together. Thus forbidding each odd-crossed cycle separately would be UNSOUND; the solvability parity belongs to each connected component, not every cycle.'
                ],
                own_examples=cases,
                own_small_multigraphs_against_literal_sign_census=32,
                limitations='This characterizes only the stated component equations. No actual peer mean read or new Conway family excluded. A feasible circulation is not a constructed SRG or even a complete admissible border.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'theorem', 'dimension', 'own_small_multigraphs_against_literal_sign_census', 'limitations')}))
