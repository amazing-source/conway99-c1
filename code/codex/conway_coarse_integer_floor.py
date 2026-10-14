"""Exact integer floor for the symmetry-free coarse counting budget.

Constructs a witness for the stated COARSE relaxation only. The twenty-one
matrices are not asserted to arise from a common far graph or from Conway.
No peer graph or census certificate is audited.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_coarse_counting_budget import budget


def exact_ldl_pivots(matrix):
    """Positive rational pivots certify positive definiteness."""
    residual = sp.Matrix(matrix)
    pivots = []
    for k in range(residual.rows):
        pivot = residual[k, k]
        if pivot <= 0:
            return None
        pivots.append(str(pivot))
        for i in range(k + 1, residual.rows):
            for j in range(i, residual.rows):
                value = residual[i, j] - residual[i, k] * residual[j, k] / pivot
                residual[i, j] = residual[j, i] = value
    return pivots


def floor_identity(E):
    diagonal = sum(E[i][i] for i in range(10))
    mates = sum(E[i][i ^ 1] for i in range(0, 10, 2))
    total = sum(map(sum, E))
    square = sum(x * x for row in E for x in row)
    defect = sum(E[i][i] * (E[i][i] - 2) for i in range(10))
    defect += 2 * sum(E[i][i ^ 1] * (E[i][i ^ 1] - 1) for i in range(0, 10, 2))
    defect += 2 * sum((E[i][j] - 2) * (E[i][j] - 3)
                      for i, j in combinations(range(10), 2) if j != (i ^ 1))
    assert square == 5 * total - 3 * diagonal - 8 * mates - 480 + defect
    return dict(squared_norm=square, trace=diagonal, mate_sum=mates,
                entry_sum=total, defect=defect)


def integer_coarse_witness(seconds):
    model = cp_model.CpModel()
    entries = {}
    for i in range(10):
        for j in range(i, 10):
            domain = [0, 2] if i == j else [0, 1] if j == (i ^ 1) else [2, 3]
            entries[i, j] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain), f'e_{i}_{j}')
    def entry(i, j):
        return entries[min(i, j), max(i, j)]
    model.Add(sum(entry(i, i) for i in range(10)) == 8)
    model.Add(sum(entry(i, i ^ 1) for i in range(0, 10, 2)) == 4)
    model.Add(sum(entry(i, j) for i, j in combinations(range(10), 2) if j != (i ^ 1)) == 96)
    for i in range(10):
        larger = model.NewBoolVar(f'row22_{i}')
        model.Add(sum(entry(i, j) for j in range(10)) == 20 + 2 * larger)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return dict(status=solver.StatusName(status), conclusion='No coarse witness returned.')
    E = [[int(solver.Value(entry(i, j))) for j in range(10)] for i in range(10)]
    M_t = sp.Matrix(10, 10, lambda i, j: int(j == (i ^ 1)))
    M = 6 * sp.eye(10) + 2 * (sp.ones(10) - M_t) - sp.Matrix(E)
    V = (176 * sp.eye(10) + 16 * M_t - 44 * sp.ones(10)) / 15 + sp.Matrix(E)
    pivots_M, pivots_V = exact_ldl_pivots(M), exact_ldl_pivots(V)
    assert pivots_M is not None and pivots_V is not None
    lower = floor_identity(E)
    assert lower == dict(squared_norm=504, trace=8, mate_sum=4, entry_sum=208, defect=0)
    rows = list(map(sum, E))
    assert all(row in (20, 22) for row in rows)
    # u_x counts edges from the four-label bucket to the four overlap labels.
    # This witness also has nonnegative integer u_x and the correct sum for e(O)=0.
    u = [(24 - row) // 2 for row in rows]
    assert sum(u) == 16
    return dict(status='EXACT_INTEGER_COARSE_PD_WITNESS', E=E, row_sums=rows,
                overlap_incidence_row_sums=u, overlap_edge_count=0,
                invariants=lower, original_budget=budget(E),
                positive_LDL_pivots_M=pivots_M, positive_LDL_pivots_V=pivots_V,
                per_root_21_copies=dict(squared_norm=21*504, trace=168,
                    mate_sum=84, entry_sum=4368, t=0, d=0),
                global_99_roots=dict(Q=99*21*504, P=0, Z=0,
                    old_budget_left=5*99*21*504, old_budget_right=12374208),
                scope='Independent copies satisfy the listed coarse constraints. Common adjacency realization, the full T/U forms, and rank bounds are NOT imposed.')


def equality_case_matchings():
    """Complete small local classifications, conditional on t=d=Delta=0."""
    def matchings(points):
        if not points:
            yield ()
            return
        a = points[0]
        for b in points[1:]:
            rest = tuple(x for x in points if x not in (a,b))
            for tail in matchings(rest):
                yield ((a,b),)+tail
    cycle_types = Counter()
    examined = 0
    for matching in matchings(tuple(range(12))):
        examined += 1
        collapsed = [tuple(sorted((a//2,b//2))) for a,b in matching]
        if any(a == b for a,b in collapsed) or len(set(collapsed)) != 6:
            continue
        adjacency = [set() for _ in range(6)]
        for a,b in collapsed:
            adjacency[a].add(b)
            adjacency[b].add(a)
        assert all(len(row) == 2 for row in adjacency)
        remaining, sizes = set(range(6)), []
        while remaining:
            todo = [next(iter(remaining))]
            seen = set(todo)
            while todo:
                for nxt in adjacency[todo.pop()]:
                    if nxt not in seen:
                        seen.add(nxt)
                        todo.append(nxt)
            remaining.difference_update(seen)
            sizes.append(len(seen))
        cycle_types[tuple(sorted(sizes))] += 1
    assert examined == 10395 and cycle_types == {(6,):3840, (3,3):640}
    octahedron = [(i,j) for i,j in combinations(range(6),2) if j != (i ^ 1)]
    orientations = 0
    for bits in product((0,1), repeat=12):
        out = [0]*6
        for (i,j), bit in zip(octahedron,bits):
            out[i if bit else j] += 1
        orientations += all(value == 2 for value in out)
    assert orientations == 38
    return dict(scope='Necessary if one root has t_v=d_v=0 and sum_21 Delta(E)=0. These conditions are NOT established for Conway.',
        star_matching=dict(examined_perfect_matchings=examined, allowed=4480,
            collapsed_cycle_types={'C6':3840,'C3+C3':640},
            quotient_proof='No mate edge because t_v=0. Delta=0 forbids two matching edges on any two root lines. After collapsing the six mate pairs, the matching is a simple2-regular graph on six vertices, hence C6 or two triangles.',
            relabelling_normal_forms=2),
        mate_star_bijection=dict(collapsed_graph='K6 minus a perfect matching',
            balanced_orientations_per_graph=38, labelled_missing_matchings=15,
            lifts_per_orientation=4**6, total_labelled_bijections=15*38*4**6,
            quotient_proof='The bijection has no within-line edge because t_v=d_v=0. Delta=0 allows at most one directed edge in each unordered pair of lines. Each collapsed vertex has in-degree2 and out-degree2, so the underlying graph is simple4-regular on six vertices. Assign the two source and two target labels independently at each vertex.'))


def investigate(seconds):
    started = time.monotonic()
    # Exact secants on every allowed integer entry, not a numerical LP claim.
    assert all(e*(e-2) >= 0 for e in (0, 2, 4))
    assert all(e*(e-1) >= 0 for e in range(5))
    assert all((e-2)*(e-3) >= 0 for e in range(9))
    witness = integer_coarse_witness(seconds)
    assert witness['status'] == 'EXACT_INTEGER_COARSE_PD_WITNESS'
    return dict(status='EXACT_COARSE_INTEGER_FLOOR_AND_SHARP_P_ZERO_WITNESS',
        local_identity='||E||_F^2 = 5*sum(E)-3*tr(E)-8*h-480+Delta(E)',
        nonnegative_defect='Delta(E)=sum_i Eii*(Eii-2)+2*sum_mates Eij*(Eij-1)+2*sum_nonmates (Eij-2)*(Eij-3)',
        per_root_identity='sum_21 ||E||_F^2 = 10584-16*t_v-24*d_v+sum_21 Delta(E)',
        global_identity='Q = 1047816-96*P-24*Z+Delta_global',
        necessary_budget_rewritten='5*Delta_global+448*P-72*Z<=7135128',
        strengthened_row_identity='sum_y E_xy=24-2*u_x; sum_x u_x=16-4*e(overlap)',
        row_identity_proof='Each label {a,x} with a central and x exterior has six neighbors counted with multiplicity in the four central stars. An overlap neighbor is counted twice, an exterior-bucket neighbor once. Summing four rows gives24-2*u_x. Each of the four overlap labels has four neighbors counted with multiplicity, giving sum_x u_x=16-4*e(overlap).',
        sharp_P_Z_zero_minimum=dict(Q=1047816, average_per_matrix=504,
            contradiction_threshold_average='12374208/(5*2079)',
            exact_threshold=str(sp.Rational(12374208,5*2079))),
        coarse_witness=witness,
        equality_case_local_classification=equality_case_matchings(),
        conclusion='The independent integer 10x10 compression relaxation, even with both forms positive definite and the displayed row identities, cannot force P>0 or contradiction by this budget. This is not a jointly glued Conway or a full four-star witness.',
        census_scope_correction='The earlier P=0 point concerns the supplied affine order9 census only, not all possible counting or PSD relaxations of order at most9.',
        seconds=time.monotonic()-started)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=10)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = investigate(args.seconds)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'global_identity', 'necessary_budget_rewritten', 'sharp_P_Z_zero_minimum', 'conclusion', 'seconds')}))
