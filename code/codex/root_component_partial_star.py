"""Completion and exhaustive refinement of a PARTIAL root component template.

Each known_partitions entry is null or a full partition of the other six
root lines, INCLUDING singleton parts. Null means unknown, never six prisms.
Only the anchor's star matching is fixed. Unknown partitions and rectangle
types remain variables. An infeasible node excludes every descendant;
UNKNOWN never excludes a node or licenses skipping its descendants.

The initial c=1/c=2 factory uses global root relabellings before any other
line is specified. It produces 11+23 representatives. Subsequent refinement
enumerates labelled set partitions and preserves the entire parent node.
"""
import argparse
from collections import Counter
import copy
from itertools import combinations, product
import json
from math import factorial, prod
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate
from root_component_complete_star import matching_assignments, peak_memory_bytes, solve_branch, add_universal_root_cuts


class PartialContradiction(Exception):
    pass


def template_from_node(node):
    partitions = node['known_partitions']
    assert len(partitions) == 7
    groups = []; counts = []; states = {}
    for root, parts in enumerate(partitions):
        if parts is None:
            groups.append(None); counts.append(None)
            continue
        flat = [j for part in parts for j in part]
        assert parts and all(part for part in parts)
        assert len(flat) == 6 and set(flat) == set(range(7)) - {root}
        counts.append(len(parts))
        groups.append([sorted(part) for part in parts if len(part) > 1])
        for part in parts:
            for j in part:
                pair = tuple(sorted((root, j))); grid = len(part) == 1
                if pair in states and states[pair] != grid:
                    raise PartialContradiction({'kind': 'incompatible_grid_status', 'pair': pair})
                states[pair] = grid
    anchor = node['anchor_root_line']
    assert anchor in range(7) and partitions[anchor] is not None
    return {'partial': True, 'nontrivial_component_groups': groups,
            'component_count_by_root_line': counts,
            'known_grid_edges': [list(e) for e in sorted(states) if states[e]],
            'nongrid_edges': [list(e) for e in sorted(states) if not states[e]]}


def anchor_matching(node):
    root = node['anchor_root_line']; letter = 2*root
    matching = node['anchor_matching_letters']
    flat = [x for edge in matching for x in edge]
    assert len(matching) == 6 and all(len(edge) == 2 for edge in matching)
    assert len(flat) == 12 and set(flat) == set(range(14)) - {letter, letter^1}
    part_of = {j: i for i, part in enumerate(node['known_partitions'][root]) for j in part}
    if any(part_of[a//2] != part_of[b//2] for a, b in matching):
        raise PartialContradiction({'kind': 'matching_crosses_known_components'})
    lookup = {pair: w for w, pair in enumerate(LABELS)}
    return tuple(sorted(tuple(sorted((lookup[tuple(sorted((letter,a)))],
                                     lookup[tuple(sorted((letter,b)))]))) for a,b in matching))


def initial_nodes(component_counts=(1, 2)):
    from conway_global_cover import partitions, canonical_matching
    nodes = []
    for sizes in partitions(6):
        if len(sizes) not in component_counts:
            continue
        parts = []; start = 1
        for size in sizes:
            parts.append(list(range(start, start+size))); start += size
        for types in product(*(list(partitions(size)) for size in sizes)):
            # Equal-size component blocks can still be permuted globally.
            if any(sizes[i] == sizes[j] and types[i] > types[j]
                   for i in range(len(sizes)) for j in range(i+1, len(sizes))):
                continue
            matching = []; weight = 1
            for part, cycle_type in zip(parts, types):
                letters = [a for j in part for a in (2*j, 2*j+1)]
                matching.extend([[letters[a], letters[b]] for a,b in canonical_matching(cycle_type)])
                multiplicities = Counter(cycle_type)
                weight *= factorial(len(part))*2**(len(part)-len(cycle_type)) // prod(
                    length**multiplicity*factorial(multiplicity) for length,multiplicity in multiplicities.items())
            for size, multiplicity in Counter(sizes).items():
                kinds = Counter(types[i] for i in range(len(sizes)) if sizes[i] == size)
                weight *= factorial(multiplicity)//prod(factorial(v) for v in kinds.values())
            nodes.append({'initial_case': len(nodes), 'component_sizes': sizes,
                          'internal_cycle_types': types, 'labelled_matching_count': weight,
                          'known_partitions': [parts] + [None]*6, 'anchor_root_line': 0,
                          'anchor_matching_letters': matching, 'root_prism_budget': 51,
                          'minimum_root_components_for_refinement': len(sizes),
                          'symmetry_reduction_scope': 'Applied at the initial node only, with exactly one known partition.'})
    return nodes


def set_partitions(items):
    """All labelled set partitions, without ordering the blocks."""
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for parts in set_partitions(items[1:]):
        yield ((first,),) + parts
        for i in range(len(parts)):
            yield parts[:i] + ((first,) + parts[i],) + parts[i+1:]


def expand_node(node, line):
    assert node['known_partitions'][line] is None
    minimum = node.get('minimum_root_components_for_refinement', 1)
    children = []; inconsistent = 0; too_small = 0
    for parts in set_partitions(j for j in range(7) if j != line):
        if len(parts) < minimum:
            too_small += 1
            continue
        child = copy.deepcopy(node)
        child['known_partitions'][line] = [list(p) for p in parts]
        try:
            template_from_node(child)
        except PartialContradiction:
            inconsistent += 1
            continue
        children.append(child)
    return children, {'split_line': line, 'labelled_partitions': 203,
                      'below_declared_root_minimum': too_small,
                      'incompatible_grid_status': inconsistent,
                      'children': len(children), 'exhaustive_within_parent_scope': True}


def add_partial_root_gram(model, graph, template):
    """Universal 21-rectangle Gram, with variable unknown grid statuses."""
    from ortools.sat.python import cp_model
    edges = list(RECTANGLES); m = len(edges)
    grid = {tuple(e) for e in template['known_grid_edges']}
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    matrix = [[None]*m for _ in range(m)]
    for i, edge in enumerate(edges):
        values = [0] if edge in grid else [4,6,8] if edge in nongrid else [0,4,6,8]
        matrix[i][i] = model.new_int_var_from_domain(cp_model.Domain.from_values(values), f'partial_R_{i}_{i}')
        model.add(matrix[i][i] == 8-2*sum(graph[u][v] for u,v in combinations(RECTANGLES[edge],2)))
        for j in range(i):
            other = edges[j]; common = bool(set(edge)&set(other))
            entry = model.new_int_var(-8, 0 if common else 4, f'partial_R_{j}_{i}')
            matrix[i][j] = matrix[j][i] = entry
            model.add(entry == (0 if common else 4)-sum(graph[u][v] for u in RECTANGLES[edge] for v in RECTANGLES[other]))
            square = model.new_int_var(0,64,f'partial_R_square_{j}_{i}')
            diagonal_product = model.new_int_var(0,64,f'partial_R_diagonal_product_{j}_{i}')
            model.add_multiplication_equality(square,[entry,entry])
            model.add_multiplication_equality(diagonal_product,[matrix[i][i],matrix[j][j]])
            model.add(square <= diagonal_product)
    for i in range(m):
        for line in range(7):
            model.add(sum(matrix[i][j] for j,e in enumerate(edges) if line in e) == 0)
    return {'rectangles': 21, 'unknown_grid_statuses': 21-len(grid)-len(nongrid),
            'principal_minors_order2': 210, 'kernel_dimension_from_complete_template_used': False}


def build_node(node, transport=True, residual_eigen=2, transport_level='full'):
    from conway_global_cover import build_global
    from root_component_exact_triangles import add_exact_triangle_structure
    from root_component_matching_rotation import add_fixed_matching_rotation
    from root_component_rotated_residual import add_rotated_residual_cuts
    from root_component_rotated_gram import add_gram_cuts, add_eigen_cuts, complete_stars, add_gram_kernel_cuts
    try:
        template = template_from_node(node); matching = anchor_matching(node)
    except PartialContradiction as error:
        return None, None, {'status': 'STRUCTURAL_CONTRADICTION', 'conflict': error.args[0]}
    root = node['anchor_root_line']
    propagation = propagate(template, extra_initial=matching_assignments(root, matching))
    if propagation['status'] == 'PROPAGATION_CONTRADICTION':
        return None, None, {'status': propagation['status'], 'propagation': propagation}
    fixed = {PAIRS[i]:v for i,v,_ in propagation['assignments']}
    model, labels, graph, selectors, info = build_global(normalize_star=False, initial_edges=fixed)
    assert tuple(labels) == LABELS and not selectors
    equations, bounds, _ = constraints(template)
    for items, target, _ in equations:
        model.add(sum(graph[PAIRS[i][0]][PAIRS[i][1]] for i in items) == target)
    for items, upper, _ in bounds:
        model.add(sum(graph[PAIRS[i][0]][PAIRS[i][1]] for i in items) <= upper)
    budget = node.get('root_prism_budget')
    if budget is not None:
        assert budget == 51
        model.add(sum(graph[u][v] for corners in RECTANGLES.values() for u,v in combinations(corners,2)
                      if set(LABELS[u])&set(LABELS[v])) <= budget)
    info.update(status='MODEL_BUILT', known_lines=[i for i,p in enumerate(node['known_partitions']) if p is not None],
                known_grid_edges=template['known_grid_edges'], known_nongrid_edges=template['nongrid_edges'],
                partial_component_equations=len(equations), propagated_fixed_edges=len(fixed),
                root_prism_budget=budget, fixed_gram_witness=False, uses_minimum_four_tables=False)
    info['universal_root_cuts'] = add_universal_root_cuts(model,graph,template)
    info['root_gram'] = add_partial_root_gram(model,graph,template)
    info['triangles'] = add_exact_triangle_structure(model,graph,template)
    assert transport_level in ('corners', 'residual', 'gram', 'eigen', 'full')
    if transport:
        fixed_graph, rectangles, rotation = add_fixed_matching_rotation(model,graph,template,root)
        if len(rectangles) == 15 and transport_level != 'corners':
            rotation['residuals'] = add_rotated_residual_cuts(model,fixed_graph,rectangles,tight_bounds=True)
            if transport_level in ('gram', 'eigen', 'full'):
                rotation['gram'] = add_gram_cuts(model,rectangles,'all')
                rotation['gram_kernel'] = add_gram_kernel_cuts(model,rectangles)
            if residual_eigen and transport_level in ('eigen', 'full'):
                rotation['eigen'] = add_eigen_cuts(model,fixed_graph,rectangles,residual_eigen)
            if transport_level == 'full':
                for _,vectors,_ in complete_stars(rectangles):
                    for line in range(7):
                        incident = [v for pair,v in vectors.items() if line in pair]
                        for coordinate in range(98):
                            model.add(sum(v[coordinate] for v in incident) == 0)
                rotation['incident_zero_sum_equations'] = 686
        elif len(rectangles) != 15:
            assert rotation.get('empty_corner_domain')
            model.add(False)
        rotation['level'] = transport_level
        info['transport'] = rotation
    info.update(model_variables=len(model.proto.variables),model_constraints=len(model.proto.constraints))
    return model, graph, info


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('nodes', type=Path, nargs='?')
    p.add_argument('--index', type=int, default=0)
    p.add_argument('--make-initial', action='store_true')
    p.add_argument('--expand-line', type=int, choices=range(7))
    p.add_argument('--seconds', type=float, default=30)
    p.add_argument('--no-transport', action='store_true')
    p.add_argument('--transport-level', choices=('corners', 'residual', 'gram', 'eigen', 'full'), default='full')
    p.add_argument('--log-search', action='store_true')
    p.add_argument('--build-only', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); resources = limit_research_process(1)
    if args.output.exists(): raise FileExistsError(args.output)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    if args.make_initial:
        nodes = initial_nodes()
        atomic_json_write(args.output,{'scope':__doc__,'initial_nodes':len(nodes),'nodes':nodes})
        print(json.dumps({'initial_nodes':len(nodes),'counts':dict(Counter(len(n['component_sizes']) for n in nodes))}))
        return
    assert args.nodes is not None
    node = json.loads(args.nodes.read_text(encoding='utf-8-sig'))['nodes'][args.index]
    if args.expand_line is not None:
        nodes, info = expand_node(node,args.expand_line)
        atomic_json_write(args.output,{'scope':__doc__,'parent':node,'coverage':info,'nodes':nodes})
        print(json.dumps(info)); return
    assert args.seconds > 0
    start = time.process_time()
    model,graph,info = build_node(node,transport=not args.no_transport,transport_level=args.transport_level)
    result = {'scope':__doc__,'node':node,'source_file':str(args.nodes),'source_index':args.index,
              'resources':resources,'model':info,'build_cpu_seconds':time.process_time()-start,
              'status':'NOT_RUN','portable_unsat_proof':False,'global_conway_exclusion':False,
              'options':{'seconds':args.seconds,'transport':not args.no_transport,'transport_level':args.transport_level}}
    atomic_json_write(args.output,result)
    print(json.dumps({'phase':'model_ready','build_cpu_seconds':result['build_cpu_seconds'],
                      'variables':info.get('model_variables',0),'peak_rss_bytes':peak_memory_bytes()}),flush=True)
    if model is None:
        result.update(status='INFEASIBLE',method=info['status'],cpu_seconds=0,branches=0,conflicts=0)
    elif not args.build_only:
        result.update(solve_branch(model,graph,args.seconds,args.log_search))
    result['process_peak_rss_bytes'] = peak_memory_bytes()
    result['all_descendants_excluded'] = result['status']=='INFEASIBLE'
    atomic_json_write(args.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('scope','model','node','adjacency')}),flush=True)


if __name__ == '__main__': main()
