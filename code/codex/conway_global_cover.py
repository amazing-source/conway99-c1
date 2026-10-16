"""Unseeded exact SRG(k*k/2+1,k,1,2) model and complete star normalization.

Fix a vertex o. Its k neighbours form k/2 disjoint edges, numbered by
r -> r^1. Every remaining vertex is uniquely labelled {a,b}, a,b not
mates, by its two neighbours in N(o). There are k(k-2)/2 such labels.
For Gamma on these labels, the exact equations are

  sum_{q containing r} Gamma[p,q] = 2-[r in p]-[r^1 in p],
  (Gamma^2)[p,q] + Gamma[p,q] + |p intersect q| = 2, p != q.

Together with symmetric binary Gamma and zero diagonal, these equations
are EQUIVALENT to the full SRG, not just necessary local tests. Every
successful solver assignment is reconstructed and checked on all vertices.

Complete normalization: choose a root a and its star L_a. Its adjacency
is a perfect matching M on k-2 letters, which themselves carry the fixed
mate matching P. The alternating cycle half-lengths in P union M form
a partition of m=(k-2)/2. Two matchings are equivalent under permutations
of the m mate pairs and flips within those pairs iff these partitions
agree. Such relabellings extend to all roots and all pair-labelled vertices.
Thus for k=14 all candidates are covered by the eleven partitions of six.
The default model permits ALL eleven cases. No local seed, assumed graph
automorphism, H-MATCH conjecture, or prior C_p exclusion is used.

With --low-prism-flag, choose a globally minimum-prism line (t<=7 by
P<=852), and a meeting line making a non-grid flag. Such a partner is
unavoidable: a low line is in at most3 grids, accounting for at most9
of its18 meeting-line flags. Its root pair is distinguished, so star
matching normalization now has19 types: a partition of6 and the size
of the alternating component containing that distinguished pair.
We also compare t with all six other root lines, and count the grids
through the chosen line. All these restrictions preserve coverage.

A finite exhaustive specification is NOT a proven affordable solve.
UNKNOWN is never converted into an exclusion.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import factorial, prod
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for first in range(minimum, n+1):
        for rest in partitions(n-first, first):
            yield (first,)+rest


def canonical_matching(parts):
    matching = []
    start = 0
    for length in parts:
        if length == 1:
            matching.append((2*start, 2*start+1))
        else:
            for j in range(length):
                matching.append(tuple(sorted((2*(start+j)+1, 2*(start+(j+1)%length)))))
        start += length
    return sorted(matching)


def matching_type(matching, vertex_count, pointed=False):
    neighbours = [set([i ^ 1]) for i in range(vertex_count)]
    for a,b in matching:
        neighbours[a].add(b)
        neighbours[b].add(a)
    unseen = set(range(vertex_count))
    sizes = []
    marked_length = None
    while unseen:
        stack = [next(iter(unseen))]
        component = set()
        while stack:
            p = stack.pop()
            if p in component:
                continue
            component.add(p)
            stack.extend(neighbours[p]-component)
        unseen -= component
        sizes.append(len(component)//2)
        if 0 in component:
            marked_length = len(component)//2
    part = tuple(sorted(sizes))
    return (part, marked_length) if pointed else part


def matching_partition(matching, vertex_count):
    return matching_type(matching, vertex_count)


def all_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        other = vertices[pos]
        for rest in all_matchings(vertices[1:pos]+vertices[pos+1:]):
            yield ((first, other),)+rest


def coverage(k=14, enumerate_matchings=False, pointed=False):
    m = (k-2)//2
    cases = []
    for part in partitions(m):
        counts = Counter(part)
        denominator = prod(length**multiplicity*factorial(multiplicity) for length,multiplicity in counts.items())
        numerator = factorial(m)*2**(m-len(part))
        assert numerator % denominator == 0
        for marked in sorted(counts) if pointed else [None]:
            ordered = list(part)
            if marked is not None:
                ordered.remove(marked)
                ordered.insert(0, marked)
            representative = canonical_matching(ordered)
            expected = (part, marked) if pointed else part
            assert matching_type(representative, 2*m, pointed) == expected
            count = numerator//denominator
            if marked is not None:
                assert count*marked*counts[marked] % m == 0
                count = count*marked*counts[marked]//m
            cases.append(dict(partition=part, marked_component=marked,
                              canonical_matching=representative, labelled_matching_count=count))
    total = factorial(2*m)//(2**m*factorial(m))
    assert sum(case['labelled_matching_count'] for case in cases) == total
    if enumerate_matchings:
        observed = Counter(matching_type(match,2*m,pointed) for match in all_matchings(tuple(range(2*m))))
        expected = Counter({((tuple(case['partition']),case['marked_component']) if pointed
                             else tuple(case['partition'])):case['labelled_matching_count'] for case in cases})
        assert observed == expected
    return dict(root_count=k, external_mate_pairs=m, case_count=len(cases),
                distinguished_external_pair=pointed,
                all_labelled_star_matchings=total, enumeration_checked=enumerate_matchings, cases=cases,
                scope='All star matchings modulo permitted root relabellings. The remaining edges are still variables; these cases are not complete graphs.')


def build_global(k=14, normal_root=None, extra_cuts=False, gray_library=None, selected_case=None,
                 low_prism_flag=False):
    assert k >= 4 and k % 2 == 0
    normal_root = (4 if k >= 6 else 0) if normal_root is None else normal_root
    if low_prism_flag:
        assert k == 14, 'The cap P<=852 and the low-line argument are Conway-specific.'
        normal_root = 0
    assert 0 <= normal_root < k
    labels = [p for p in combinations(range(k),2) if p[1] != (p[0] ^ 1)]
    index = {p:i for i,p in enumerate(labels)}
    n = len(labels)
    model = cp_model.CpModel()
    graph = [[0]*n for _ in range(n)]
    for p,q in combinations(range(n),2):
        graph[p][q] = graph[q][p] = model.NewBoolVar('e_%d_%d' % (p,q))
    for p,label in enumerate(labels):
        model.Add(sum(graph[p]) == k-2)
        for r in range(k):
            model.Add(sum(graph[p][q] for q,other in enumerate(labels) if r in other)
                      == 2-int(r in label)-int((r ^ 1) in label))
    products = {}
    def conjunction(a,b):
        if isinstance(a,int):
            return b if a else 0
        if isinstance(b,int):
            return a if b else 0
        if a.Index() == b.Index():
            return a
        key = tuple(sorted((a.Index(),b.Index())))
        if key not in products:
            value = model.NewBoolVar('w_%d_%d' % key)
            model.AddMultiplicationEquality(value,[a,b])
            products[key] = value
        return products[key]
    for p,q in combinations(range(n),2):
        model.Add(sum(conjunction(graph[p][z],graph[q][z]) for z in range(n)) + graph[p][q]
                  == 2-len(set(labels[p])&set(labels[q])))
    cover = coverage(k,pointed=low_prism_flag)
    # Removing one complete root pair leaves consecutive mate pairs,
    # so position xor1 remains the physical mate involution.
    letters = [r for r in range(k) if r not in (normal_root,normal_root ^ 1)]
    assert all(letters[j ^ 1] == (letters[j] ^ 1) for j in range(len(letters)))
    star = [index[tuple(sorted((normal_root,r)))] for r in letters]
    selectors = [model.NewBoolVar('star_type_%d'%i) for i in range(cover['case_count'])]
    model.AddExactlyOne(selectors)
    for selector,case in zip(selectors,cover['cases']):
        for a,b in case['canonical_matching']:
            model.AddImplication(selector,graph[star[a]][star[b]])
    if selected_case is not None:
        assert 0 <= selected_case < len(selectors)
        model.Add(selectors[selected_case] == 1)
    cuts = {}
    if low_prism_flag:
        def edge(p,q):
            return graph[index[tuple(sorted(p))]][index[tuple(sorted(q))]]
        prism_edges = [edge((0,y),(1,y)) for y in range(2,k)]
        prism_count = sum(prism_edges)
        model.Add(prism_count <= 7)
        for a in range(2,k,2):
            model.Add(prism_count <= sum(edge((a,y),(a^1,y))
                                         for y in range(k) if y not in (a,a^1)))
        grid_flags = []
        for a in range(2,k,2):
            # The four cycle edges on 0a,0a*,1a,1a* together with
            # o,0,1,a,a* give a 3x3 grid; lambda=1 forces both diagonals0.
            horizontal = conjunction(edge((0,a),(0,a^1)),edge((1,a),(1,a^1)))
            vertical = conjunction(edge((0,a),(1,a)),edge((0,a^1),(1,a^1)))
            grid_flags.append(conjunction(horizontal,vertical))
        model.Add(2*sum(grid_flags) <= prism_count)
        square = [edge((0,2),(0,3)),edge((1,2),(1,3)),
                  edge((0,2),(1,2)),edge((0,3),(1,3))]
        model.Add(sum(square) <= 3)
        cuts['unavoidable_flag'] = dict(
            low_line=[0,1],nongrid_partner=[2,3],line_prisms_upper=7,
            prism_cap=852,total_lines=231,
            chosen_line_is_global_minimum=True,
            proof='sum_line t=2P<=1704<8*231. Choose a minimum-prism line. A low line belongs to at most floor(t/2)<=3 grids, hence at most9 of its18 meeting-line flags are grids. Choose a nongrid partner and normalize its mate pair to2,3.',
            source='conway_forced_low_prism_blocks.py; ../c1-codex/data/codex_order9_prism_cap.json',
            scope='An unavoidable labelled flag chosen by relabelling; not a restriction to previously constructed seeds.')
    if extra_cuts:
        assert k == 14
        from conway_five_star_defect import add_defect_cuts
        from conway_phi_defect import add_phi_cuts
        cuts['h_defect'],_ = add_defect_cuts(model,labels,graph,conjunction=conjunction)
        cuts['phi_defect'] = add_phi_cuts(model,labels,graph,conjunction=conjunction)
    if gray_library:
        assert k == 14
        from conway_gray_cuts import add_gray_cuts
        library = json.loads(Path(gray_library).read_text(encoding='utf-8'))
        applied = add_gray_cuts(model,labels,graph,library['gray_cuts'])
        cuts['gray_patterns'] = [dict(name=cut['name'],edge_count=len(cut['edges']),upper_bound=cut['upper_bound']) for cut in applied]
    info = dict(parameters=[1+k+n,k,1,2],second_neighbourhood_size=n,
                edge_variables=n*(n-1)//2,product_variables=len(products),normal_root=normal_root,
                selected_case=selected_case,covers_all_graphs=(selected_case is None),
                low_prism_flag=low_prism_flag,
                fixed_local_seed=False,assumed_automorphism=False,coverage=cover,cuts=cuts)
    return model, labels, graph, selectors, info


def reconstruct_and_check(k,labels,gamma):
    n = 1+k+len(labels)
    matrix = np.zeros((n,n),dtype=np.int64)
    matrix[0,1:k+1] = matrix[1:k+1,0] = 1
    for r in range(k):
        matrix[1+r,1+(r ^ 1)] = 1
    for i,pair in enumerate(labels,1+k):
        for r in pair:
            matrix[i,1+r] = matrix[1+r,i] = 1
    matrix[1+k:,1+k:] = gamma
    assert np.array_equal(matrix,matrix.T) and not np.any(np.diag(matrix))
    assert np.all((matrix==0)|(matrix==1)) and np.all(matrix.sum(axis=1)==k)
    square = matrix@matrix
    for p,q in combinations(range(n),2):
        assert square[p,q] == (1 if matrix[p,q] else 2)
    return matrix.tolist()


def run(output,k=14,seconds=30,build_only=False,extra_cuts=False,gray_library=None,selected_case=None,export_model=None,
        low_prism_flag=False,search_direct=False,solver_log=None):
    started = time.monotonic()
    model,labels,graph,selectors,result = build_global(k,extra_cuts=extra_cuts,gray_library=gray_library,selected_case=selected_case,
                                                     low_prism_flag=low_prism_flag)
    validation = model.Validate()
    assert not validation,validation
    result.update(build_seconds=time.monotonic()-started,model_variables=len(model.Proto().variables),
                  model_constraints=len(model.Proto().constraints),solver_time_limit=seconds,
                  status='MODEL_BUILT',complete_global_decision=False,
                  affordable_solve_proved=False,num_search_workers=1)
    if export_model:
        assert model.ExportToFile(str(export_model))
        result['exported_model'] = str(export_model)
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('coverage','cuts')},ensure_ascii=False),flush=True)
    if not build_only:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = seconds
        if search_direct:
            solver.parameters.cp_model_presolve = False
            solver.parameters.symmetry_level = 0
            solver.parameters.linearization_level = 0
            solver.parameters.cp_model_probing_level = 0
        if solver_log:
            solver.parameters.log_search_progress = True
            solver.parameters.log_to_stdout = False
            log_handle = Path(solver_log).open('w',encoding='utf-8')
            solver.log_callback = lambda message: log_handle.write(message+'\n')
        result['solver_parameters'] = str(solver.parameters)
        status = solver.Solve(model)
        if solver_log:
            log_handle.close()
            result['solver_log'] = str(solver_log)
        result.update(status=solver.StatusName(status),solver_seconds=solver.WallTime(),
                      branches=solver.NumBranches(),conflicts=solver.NumConflicts())
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            gamma = [[solver.Value(x) for x in row] for row in graph]
            result['adjacency'] = reconstruct_and_check(k,labels,gamma)
            result['successful_case'] = next(i for i,x in enumerate(selectors) if solver.Value(x))
            result['exact_all_pair_check'] = True
            result['complete_global_decision'] = True
        elif status == cp_model.INFEASIBLE:
            result['complete_global_decision'] = selected_case is None
            result['certificate_scope'] = 'Solver verdict; a portable UNSAT proof must still be produced before claiming an externally checkable exclusion.'
        result['total_seconds'] = time.monotonic()-started
        Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({key:value for key,value in result.items() if key not in ('coverage','cuts','adjacency')},ensure_ascii=False),flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--roots',type=int,default=14)
    parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--build-only',action='store_true')
    parser.add_argument('--extra-cuts',action='store_true')
    parser.add_argument('--gray-library')
    parser.add_argument('--case',type=int)
    parser.add_argument('--export-model')
    parser.add_argument('--coverage-only',action='store_true')
    parser.add_argument('--low-prism-flag',action='store_true')
    parser.add_argument('--search-direct',action='store_true',help='Disable expensive presolve, symmetry detection and LP; retain the exact model.')
    parser.add_argument('--solver-log')
    args = parser.parse_args()
    if args.coverage_only:
        result = coverage(args.roots,enumerate_matchings=True,pointed=args.low_prism_flag)
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result),flush=True)
    else:
        run(args.output,args.roots,args.seconds,args.build_only,args.extra_cuts,args.gray_library,args.case,args.export_model,
            args.low_prism_flag,args.search_direct,args.solver_log)
