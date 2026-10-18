"""Unseeded Conway completion using a complete internal-star matching cover.

For each root line, partition its other six lines into the template's
components. A component of size 6s has 2s vertices in each star, so its
internal star has (2s-1)!! possible perfect matchings. Their Cartesian
product is exhaustive without any relabelling or automorphism assumption.
Choose the line with the smallest product. Only this one star is fixed;
the opposite matching, the cross permutation, and the Gram remain free.

This model uses no minimum-four table, frozen frontier, local P/M1 catalogue,
or Gram witness. A template is excluded only if every matching is excluded.
An INFEASIBLE CP-SAT verdict is not a portable UNSAT certificate.
"""

import argparse
import ctypes
import gc
import gzip
import hashlib
from itertools import combinations, product
import json
from math import prod
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_propagation import LABELS, RECTANGLES, variable


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    assert len(vertices) % 2 == 0
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        for tail in perfect_matchings(vertices[1:i] + vertices[i+1:]):
            yield ((u, v),) + tail


def component_parts(template, root):
    parts = [tuple(sorted(p)) for p in template['nontrivial_component_groups'][root]]
    grouped = [j for p in parts for j in p]
    assert len(set(grouped)) == len(grouped) and root not in grouped
    parts += [(j,) for j in range(7) if j != root and j not in grouped]
    assert set(j for p in parts for j in p) == set(range(7)) - {root}
    assert len(parts) == template['component_count_by_root_line'][root]
    return sorted(parts)


def matching_cover(template, root=None):
    counts = [prod(prod(range(1, 2*len(p), 2)) for p in component_parts(template, r))
              for r in range(7)]
    if root is None:
        root = min(range(7), key=lambda r: (counts[r], r))
    parts = component_parts(template, root)
    lookup = {p: w for w, p in enumerate(LABELS)}
    vertices = [[lookup[tuple(sorted((2*root, a)))] for j in p for a in (2*j, 2*j+1)]
                for p in parts]
    cover = [tuple(sorted(edge for matching in selection for edge in matching))
             for selection in product(*(tuple(perfect_matchings(vs)) for vs in vertices))]
    assert len(cover) == counts[root] == len(set(cover))
    star = {w for vs in vertices for w in vs}
    assert len(star) == 12
    assert all({w for edge in matching for w in edge} == star for matching in cover)
    return root, parts, counts, cover


def matching_assignments(root, matching):
    star = [w for w, p in enumerate(LABELS) if 2*root in p]
    edges = set(matching)
    assert len(edges) == 6
    return {variable(u, v): int((u, v) in edges) for u, v in combinations(star, 2)}


def peak_memory_bytes():
    """OS high-water resident memory for this process, not an estimate."""
    if sys.platform == 'win32':
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [('cb', wintypes.DWORD), ('faults', wintypes.DWORD)] + [
                (name, ctypes.c_size_t) for name in
                ('peak_rss', 'rss', 'peak_paged', 'paged', 'peak_nonpaged',
                 'nonpaged', 'pagefile', 'peak_pagefile')]
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        api = ctypes.WinDLL('psapi', use_last_error=True)
        api.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        counters = Counters(); counters.cb = ctypes.sizeof(counters)
        if not api.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return int(counters.peak_rss)
    import resource
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == 'darwin' else 1024*value)


def add_universal_root_cuts(model, graph, template):
    """E3 and connected-component Gram cuts; no previous Gram is fixed."""
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    for edge in nongrid:
        model.add(sum(graph[u][v] for u, v in combinations(RECTANGLES[edge], 2)) <= 2)
    cuts = 0
    for root in range(7):
        for part in template['nontrivial_component_groups'][root]:
            # For a proper cut of a connected component the Gram cut weight
            # is negative and even. Its absolute value counts Gamma edges
            # between the corresponding unions of four-vertex rectangles.
            for mask in range(1, 1 << (len(part)-1)):
                left = [part[i] for i in range(len(part)) if mask & (1 << i)]
                right = [j for j in part if j not in left]
                entries = [graph[u][v] for i in left for j in right
                           for u in RECTANGLES[tuple(sorted((root, i)))]
                           for v in RECTANGLES[tuple(sorted((root, j)))]]
                model.add(sum(entries) >= 2)
                cuts += 1
    return {'nongrid_E3_bounds': len(nongrid), 'connected_component_cuts': cuts}


def build_branch(template, root, matching, residual_eigen=2, transport=True):
    from root_component_global import build
    from root_component_exact_triangles import add_exact_triangle_structure
    from root_component_matching_rotation import add_fixed_matching_rotation
    from root_component_rotated_residual import add_rotated_residual_cuts
    from root_component_rotated_gram import add_gram_cuts, add_eigen_cuts, complete_stars
    model, graph, info = build(template, {'cuts': [], 'root_prism_budget': 51},
                               extra_initial=matching_assignments(root, matching))
    if model is None:
        return model, graph, info
    info['universal_root_cuts'] = add_universal_root_cuts(model, graph, template)
    info['triangles'] = add_exact_triangle_structure(model, graph, template)
    if transport:
        fixed, rectangles, rotation = add_fixed_matching_rotation(model, graph, template, root)
        if len(rectangles) == 15:
            rotation['residuals'] = add_rotated_residual_cuts(model, fixed, rectangles, tight_bounds=True)
            rotation['gram'] = add_gram_cuts(model, rectangles, 'all')
            if residual_eigen:
                rotation['eigen'] = add_eigen_cuts(model, fixed, rectangles, residual_eigen)
            zero_sums = 0
            for _, vectors, _ in complete_stars(rectangles):
                for line in range(7):
                    incident = [vector for pair, vector in vectors.items() if line in pair]
                    assert len(incident) == 6
                    for coordinate in range(98):
                        model.add(sum(v[coordinate] for v in incident) == 0)
                        zero_sums += 1
            rotation['incident_zero_sum_equations'] = zero_sums
        else:
            assert rotation.get('empty_corner_domain')
            model.add(False)
        info['transport'] = rotation
    info['model_variables'] = len(model.proto.variables)
    info['model_constraints'] = len(model.proto.constraints)
    return model, graph, info


def solve_branch(model, graph, seconds, log_search=False):
    from ortools.sat.python import cp_model
    from conway_global_cover import reconstruct_and_check
    error = model.validate()
    if error:
        raise ValueError(error)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.linearization_level = 0
    solver.parameters.max_presolve_iterations = 1
    solver.parameters.log_search_progress = log_search
    solver.parameters.max_time_in_seconds = max(600, seconds*100)
    start_cpu = time.process_time(); start_wall = time.monotonic()
    done = threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time() - start_cpu >= seconds:
                solver.stop_search()
    timer = threading.Thread(target=stop, daemon=True); timer.start()
    try:
        status = solver.solve(model)
    finally:
        done.set(); timer.join()
    result = {'status': solver.status_name(status), 'cpu_seconds': time.process_time()-start_cpu,
              'wall_seconds': time.monotonic()-start_wall, 'deterministic_time': solver.response_proto.deterministic_time,
              'branches': solver.num_branches, 'conflicts': solver.num_conflicts}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        gamma = [[solver.value(x) for x in row] for row in graph]
        result['adjacency'] = reconstruct_and_check(14, LABELS, gamma)
        result['exact_all_pair_check'] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('templates', type=Path)
    parser.add_argument('--index', type=int, required=True)
    parser.add_argument('--root-line', type=int, choices=range(7))
    parser.add_argument('--matching-indices', type=int, nargs='+')
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--residual-eigen', type=int, default=2)
    parser.add_argument('--no-transport', action='store_true', help='Weaker model for a measured comparison.')
    parser.add_argument('--log-search', action='store_true')
    parser.add_argument('--stop-after-unknown', action='store_true',
                        help='Pilot only: leave remaining matchings unprocessed after a timeout.')
    parser.add_argument('--plan-only', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    resources = limit_research_process(1)
    if args.output.exists():
        raise FileExistsError('Use a fresh report, never overwrite a previous verdict.')
    raw = args.templates.read_bytes()
    data = json.loads(gzip.decompress(raw) if args.templates.suffix == '.gz' else raw)
    templates = data['templates']
    template = templates[args.index]
    root, parts, counts, cover = matching_cover(template, args.root_line)
    selected = list(range(len(cover))) if args.matching_indices is None else args.matching_indices
    assert len(set(selected)) == len(selected) and set(selected) <= set(range(len(cover)))
    assert args.seconds > 0 and args.residual_eigen >= 0
    result = {'scope': __doc__, 'source_file': str(args.templates),
              'source_sha256': hashlib.sha256(raw).hexdigest(), 'template_index': args.index,
              'template': template, 'root_line': root, 'component_parts': parts,
              'matching_count_by_line': counts, 'matching_cover': cover,
              'matching_branches': [], 'all_matching_branches_processed': False,
              'status': 'NOT_RUN', 'resources': resources, 'root_prism_budget': 51,
              'options': {'seconds_per_matching': args.seconds, 'residual_eigen': args.residual_eigen,
                          'transport': not args.no_transport, 'stop_after_unknown': args.stop_after_unknown},
              'fixed_gram_witness': False, 'uses_minimum_four_tables': False,
              'fixed_opposite_matching': False, 'fixed_cross_permutation': False,
              'portable_unsat_proof': False, 'global_conway_exclusion': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    atomic_json_write(args.output, result)
    print(json.dumps({'phase': 'cover_ready', 'template_index': args.index, 'root_line': root,
                      'part_sizes': list(map(len, parts)), 'matching_count': len(cover)}), flush=True)
    if args.plan_only:
        return
    for mi in selected:
        start_cpu = time.process_time(); start_wall = time.monotonic()
        model, graph, info = build_branch(template, root, cover[mi], args.residual_eigen, not args.no_transport)
        branch = {'matching_index': mi, 'model': info, 'build_cpu_seconds': time.process_time()-start_cpu,
                  'build_wall_seconds': time.monotonic()-start_wall}
        print(json.dumps({'phase': 'model_ready', 'matching_index': mi,
                          'build_cpu_seconds': branch['build_cpu_seconds'],
                          'variables': info.get('model_variables', 0),
                          'process_peak_rss_bytes': peak_memory_bytes()}), flush=True)
        if model is None:
            assert info['status'] == 'PROPAGATION_CONTRADICTION'
            branch.update(status='INFEASIBLE', method='exact_binary_propagation',
                          cpu_seconds=0, wall_seconds=0, branches=0, conflicts=0)
        else:
            branch.update(solve_branch(model, graph, args.seconds, args.log_search))
        branch['process_peak_rss_bytes'] = peak_memory_bytes()
        result['matching_branches'].append(branch)
        result['process_peak_rss_bytes'] = branch['process_peak_rss_bytes']
        result['memory_scope'] = 'OS process high-water RSS, cumulative across this template, includes building and solving.'
        processed = {b['matching_index'] for b in result['matching_branches']}
        result['all_matching_branches_processed'] = processed == set(range(len(cover)))
        result['status'] = 'UNKNOWN'
        if result['all_matching_branches_processed'] and all(b['status']=='INFEASIBLE' for b in result['matching_branches']):
            result['status'] = 'INFEASIBLE'
        if any(b.get('exact_all_pair_check') for b in result['matching_branches']):
            result['status'] = 'CONWAY_GRAPH_FOUND'
        atomic_json_write(args.output, result)
        print(json.dumps({'phase': 'verdict', 'matching_index': mi, 'status': branch['status'],
                          'cpu_seconds': branch['cpu_seconds'], 'build_cpu_seconds': branch['build_cpu_seconds'],
                          'peak_rss_bytes': branch['process_peak_rss_bytes'],
                          'template_status': result['status']}), flush=True)
        del model, graph, info
        gc.collect()
        if result['status'] == 'CONWAY_GRAPH_FOUND':
            break
        if args.stop_after_unknown and branch['status'] == 'UNKNOWN':
            break


if __name__ == '__main__':
    main()
