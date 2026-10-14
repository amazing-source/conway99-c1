"""Global mixed-relation budgets, without a local symmetry hypothesis.

Uses the established G9 identity and the accepted grid bound rho<=126.
Enumerates a NEW statistic on grid graphs: pairs forced to have >=4 mixed
relations, then aggregates that statistic over the 99 vertices.
No producer's local border, rank or PSD certificate is recomputed.
"""
import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import time


PAIRS = tuple(combinations(range(7), 2))


def exceptional_profile():
    """Gray-code enumeration of all labelled graphs on seven vertices."""
    degrees = [0]*7
    degree_counts = [7]+[0]*6
    adjacency = [0]*7
    edge_count = 0
    gray = 0
    accepted = 0
    profile = {}
    for index in range(1 << 21):
        if index:
            bit = (index & -index).bit_length()-1
            u, v = PAIRS[bit]
            change = -1 if adjacency[u] & (1 << v) else 1
            for x in (u, v):
                degree_counts[degrees[x]] -= 1
                degrees[x] += change
                degree_counts[degrees[x]] += 1
            adjacency[u] ^= 1 << v
            adjacency[v] ^= 1 << u
            edge_count += change
            gray ^= 1 << bit
        if degree_counts[5]:
            continue
        accepted += 1
        a = degree_counts[0]+degree_counts[1]
        b = degree_counts[2]+degree_counts[3]
        c_mask = sum(1 << i for i in range(7) if degrees[i] == 4)
        bc_edges = sum((adjacency[i] & c_mask).bit_count()
                       for i in range(7) if degrees[i] in (2, 3))
        bad = a*(13-a)//2+b*(b-1)//2+bc_edges
        old = profile.get(edge_count)
        if old is None or bad < old['forced_pairs_at_least4']:
            profile[edge_count] = dict(forced_pairs_at_least4=bad,
                                       witness_edge_mask=gray,
                                       witness_degrees=list(degrees))
    # Check the new compressed statistic by its direct definition on extrema.
    for e, record in profile.items():
        mask = record['witness_edge_mask']
        edges = [p for bit, p in enumerate(PAIRS) if mask & (1 << bit)]
        assert len(edges) == e
        deg = [sum(x in p for p in edges) for x in range(7)]
        assert deg == record['witness_degrees'] and 5 not in deg
        f = [3+d//2 for d in deg]
        demands = [12-f[u]-f[v]+int((u, v) in edges) for u, v in PAIRS]
        assert sum(x >= 4 for x in demands) == record['forced_pairs_at_least4']
        odd = sum(d % 2 for d in deg)
        assert sum(demands) == 126-5*e+3*odd
    return dict(labelled_graphs=1 << 21,
                graphs_without_degree5=accepted,
                minimum_by_edge_count={str(e): value for e, value in sorted(profile.items())})


def aggregate(profile, vertices=99, max_grid_incidences=1134):
    """Exact integer relaxation: no compatibility between grid graphs imposed."""
    options = [(int(e), r['forced_pairs_at_least4'])
               for e, r in profile['minimum_by_edge_count'].items()]
    inf = 10**9
    previous = [inf]*(max_grid_incidences+1)
    previous[0] = 0
    predecessors = []
    for _ in range(vertices):
        current = [inf]*(max_grid_incidences+1)
        choice = [-1]*(max_grid_incidences+1)
        for used, value in enumerate(previous):
            if value == inf:
                continue
            for e, bad in options:
                total = used+e
                if total <= max_grid_incidences and value+bad < current[total]:
                    current[total] = value+bad
                    choice[total] = e
        previous = current
        predecessors.append(choice)
    best_used = min(range(len(previous)), key=lambda e: previous[e])
    minimum = previous[best_used]
    types = {}
    used = best_used
    for row in reversed(predecessors):
        e = row[used]
        assert e >= 0
        types[e] = types.get(e, 0)+1
        used -= e
    assert used == 0 and sum(types.values()) == vertices
    assert sum(e*n for e, n in types.items()) == best_used
    assert sum(profile['minimum_by_edge_count'][str(e)]['forced_pairs_at_least4']*n
               for e, n in types.items()) == minimum
    return dict(vertices=vertices, maximum_grid_incidences=max_grid_incidences,
                minimum_forced_pairs_at_least4=minimum,
                relaxation_attainer_grid_incidences=best_used,
                relaxation_attainer_edge_count_multiplicities=types,
                scope='Independent vertex grid graphs only; the attainer is not a Conway graph.')


def add_proof(result):
    profile = result['grid_graph_profile']['minimum_by_edge_count']
    slacks = {int(e): 13*r['forced_pairs_at_least4']+20*int(e)-273
              for e, r in profile.items()}
    assert min(slacks.values()) == 0
    small = {e: s for e, s in slacks.items() if s <= 8}
    assert small == {0: 0, 12: 6, 13: 0, 14: 7}
    assert 99*273-20*1134 == 4347
    assert 13*334 < 4347 <= 13*335
    assert 13*335+20*1133 < 99*273
    assert 1134 % 13 == 3
    assert result['global_integer_relaxation']['minimum_forced_pairs_at_least4'] == 336
    result.update(
        no_symmetry_assumption=True,
        definitions={
            'rho': 'Total number of induced nine-vertex 3x3 grids.',
            'G_v': 'Graph on the seven triangle-lines through v; an edge means the two lines lie in a grid.',
            'g_l': 'Degree of line l in G_v; degree5 is impossible by the accepted component theorem.',
            'c_l': 'Number of components of the two-star even-sector graph H_l; c_l<=3+floor(g_l/2).',
            'm_lm': 'dim ker(T_S44) - (2+c_l+c_m-epsilon_lm), the number of mixed relations beyond the separate line relations.',
            'delta_lm': '30-rank(T_S44)>=0 in a genuine Conway completion, by the accepted G9 identity.',
            'o_v': 'Number of odd degrees in G_v.',
            'h_v': 'sum_l(3+floor(g_l/2)-c_l)>=0.',
            'Delta_v': 'sum_{l<m} delta_lm.',
            'b_v': 'Number of pairs forced to have m_lm>=4 by the grid graph and the upper bounds on c_l.'},
        exact_identities=[
            'm_lm=12-c_l-c_m+epsilon_lm+delta_lm',
            'sum_{l<m}m_lm=126-5e(G_v)+3o_v+6h_v+Delta_v',
            'sum_v e(G_v)=9rho',
            'sum_{v,l<m}m_lm=12474-45rho+3sum_v o_v+6sum_v h_v+sum_v Delta_v'],
        sum_proof=[
            'Each line appears in six pairs. Also sum_l floor(g_l/2)=e(G_v)-o_v/2 by the handshaking identity.',
            'Summing the accepted G9 mixed-relation formula gives the stated local identity. Each nine-vertex grid contributes once at each of its nine vertices, hence sum_v e(G_v)=9rho.',
            'The accepted exact certificate P+5rho<=1386 and the geometric inequality P>=6rho give rho<=126. The global sum is therefore at least6804; the average over2079 pairs is at least36/11.',
            'Consequently sum(max(m_lm-3,0))>=567, with additional positive contributions from the displayed o,h,delta terms and from pairs with fewer than3 mixed relations.'],
        exceptional_count_proof=[
            'Set f(g)=3+floor(g/2). Every pair has m_lm>=12-f(g_l)-f(g_m)+epsilon_lm, independently of its actual smaller component counts or nonnegative delta.',
            'Partition the seven vertices of G_v into A (degrees0,1), B (2,3), C (4), D (6). A degree5 cannot occur. The forced pairs are all pairs incident with A, all pairs within B, and the edges between B and C. Pairs A,D are edges because D is universal.',
            'Thus b_v=|A|(13-|A|)/2+binom(|B|,2)+e(B,C). Exhaustive Gray-code enumeration computes its exact minimum for every edge count; the retained witnesses establish attainability in this grid-graph relaxation only.',
            'The profile certifies 13b_v+20e(G_v)>=273. Summing and using sum e<=1134 first gives B=sum b_v>=335.',
            'If B=335, sum e must equal1134 and the sum of vertex slacks is at most8. The only possible individual minima with slack<=8 are (e,b,slack)=(0,21,0),(13,1,0),(12,3,6),(14,0,7). A nonminimal b adds at least13 to the slack.',
            'There is at most one of the last two types. Therefore sum e is congruent to0,1 or-1 modulo13, contrary to1134 congruent3. Hence B>=336.',
            'The independent relaxation attains336 with12 graphs having0 edges,84 having13 edges and3 having14 edges. This does not assert compatibility of these99 grid graphs inside a single Conway graph.'],
        integer_certificate=dict(local_inequality='13*b+20*e>=273',
                                 minimum_slacks_by_edge_count=slacks,
                                 possible_slacks_when_total_at_most8=small,
                                 contradiction_residues_mod13=[0, 1, 12],
                                 required_residue_mod13=3),
        other_consequence='At least18 of the99 vertices have some pair with at least4 mixed relations: vertices without one have at least14 grids, whereas the total incidence budget is1134.',
        accepted_inputs=[
            'G9 and the component interpretation P9, communicated by Claude778, accepted without reproducing his local samples or their ranks.',
            'Exact stored certificate c1-codex/data/codex_prism_plus_five_grids_cap.json: P+5rho<=1386. Its15 nonnegative rational terms use the accepted order9 census.',
            'Geometric uniqueness of grid completion of a prism pair:6rho<=P; proof already recorded in the current journal.'],
        scope='Necessary conditions for a hypothetical Conway graph, not a construction, an upper bound on mixed relations, or a nonexistence proof.',
        solver_consequence='A completion must satisfy the global mass budget and at least336 four-star flags with m>=4. A search restricted everywhere to m<=3 is impossible. No generic rank-constraint encoding or speedup is claimed.',
        validation='New grid-pair statistic checked directly on all extremal witnesses; exact integer dynamic programming agrees with the short slack/residue certificate. No peer PSD seed or rank recomputed.')
    return result


def investigate():
    started = time.monotonic()
    profile = exceptional_profile()
    result = dict(status='EXACT_GLOBAL_MIXED_RELATION_BUDGET',
                  grid_graph_profile=profile,
                  global_integer_relaxation=aggregate(profile),
                  accepted_grid_bound=126,
                  total_root_line_pairs=99*21,
                  mixed_relation_sum_lower=12474-45*126,
                  average_lower=str(Fraction(12474-45*126, 99*21)),
                  excess_above3_lower=12474-45*126-3*99*21)
    result = add_proof(result)
    result['seconds'] = time.monotonic()-started
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = investigate()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))
