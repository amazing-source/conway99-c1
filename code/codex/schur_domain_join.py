"""Exact finite assembly of column domains when one Gram rank is saturated.

T fixes every missing adjacency entry. The U Schur residual must be PSD
of its prescribed rank. In rank1, all2x2 minors vanishing is insufficient:
one also needs globally compatible signs, checked against an anchor.
All arithmetic affecting a verdict is integral. Time limits are explicit.
"""
from collections import Counter
from itertools import combinations
import time

import numpy as np

from odd9_endpoint_mate_family import exact_psd


def residual_rank_check(matrix, target, final=False):
    size = len(matrix)
    if not size:
        return not final or target == 0
    if target == 0:
        return not any(any(row) for row in matrix)
    if target == 1:
        if any(matrix[i][i] < 0 for i in range(size)):
            return False
        anchor = next((i for i in range(size) if matrix[i][i]), None)
        if anchor is None:
            return not any(any(row) for row in matrix) and not final
        pivot = matrix[anchor][anchor]
        return all(matrix[i][j]*pivot == matrix[i][anchor]*matrix[j][anchor]
                   for i in range(size) for j in range(size))
    psd, rank, _ = exact_psd(matrix)
    return psd and (rank == target if final else rank <= target)


def join_domains(domains, t_inverse, u_inverse, offsets, residual_rank,
                 t_scale=8, u_scale=15, seconds=30, max_solutions=1,
                 partial_check=None, leaf_check=None):
    """domains[i] contains T/U coordinates and scaled U residual diagonals.

    offsets(i,j) returns the two integer geometric offsets. Their signs
    are T_ij=-t_scale*edge-K_ij and U_ij=u_scale*edge-L_ij.
    partial_check/leaf_check may impose graph conditions not captured by
    Gram compatibility. A candidate is reported only after leaf_check.
    max_solutions=0 requests exhaustive enumeration within the time budget.
    """
    started = time.monotonic()
    _, tn, td = t_inverse
    _, un, ud = u_inverse
    count = len(domains)
    coordinates = [[(np.array(d['T_coordinates'], dtype=object),
                     np.array(d['U_coordinates'], dtype=object),
                     int(d['U_residual_numerator'])) for d in domain] for domain in domains]
    for domain in domains:
        for d in domain:
            assert int(d['U_residual_denominator']) == ud
            assert int(d['U_residual_numerator']) >= 0
    cache, stats, solutions = {}, Counter(), []
    interrupted, reached_limit = False, False

    def pair(i, ai, j, aj):
        if i > j:
            i, ai, j, aj = j, aj, i, ai
        key = (i, ai, j, aj)
        if key in cache:
            return cache[key]
        stats['pair_products'] += 1
        bt, bu, diag_i = coordinates[i][ai]
        ct, cu, diag_j = coordinates[j][aj]
        kt, lu = offsets(i, j)
        edge_num = -int(bt@tn@ct)-td*kt
        divisor = td*t_scale
        if edge_num not in (0, divisor):
            cache[key] = None
            stats['nonbinary_forced_edge'] += 1
            return None
        edge = edge_num//divisor
        residual = ud*(u_scale*edge-lu)-int(bu@un@cu)
        if residual_rank == 0:
            allowed = not (diag_i or diag_j or residual)
        elif residual_rank == 1:
            allowed = residual**2 == diag_i*diag_j
        else:
            allowed = residual**2 <= diag_i*diag_j
        cache[key] = (edge, residual) if allowed else None
        if not allowed:
            stats['U_pair_failure'] += 1
        return cache[key]

    def visit(possible, selected):
        nonlocal interrupted, reached_limit
        if time.monotonic() > started+seconds:
            interrupted = True
            return
        stats['nodes'] += 1
        if len(selected) == count:
            order = sorted(selected)
            residual = [[coordinates[i][selected[i]][2] if i == j else pair(i, selected[i], j, selected[j])[1]
                         for j in order] for i in order]
            if not residual_rank_check(residual, residual_rank, final=True):
                stats['wrong_final_U_rank'] += 1
                return
            if leaf_check and not leaf_check(selected, pair):
                stats['leaf_graph_failure'] += 1
                return
            solutions.append(dict(assignment=[selected[i] for i in range(count)],
                edges=[[i, j] for i, j in combinations(range(count), 2) if pair(i, selected[i], j, selected[j])[0]],
                U_residual_numerator=residual, U_residual_denominator=str(ud)))
            if max_solutions and len(solutions) >= max_solutions:
                reached_limit = True
            return
        vertex = min((i for i in range(count) if i not in selected), key=lambda i: len(possible[i]))
        for value in possible[vertex]:
            selected[vertex] = value
            order = sorted(selected)
            residual = [[coordinates[i][selected[i]][2] if i == j else pair(i, selected[i], j, selected[j])[1]
                         for j in order] for i in order]
            if not residual_rank_check(residual, residual_rank):
                stats['U_joint_failure'] += 1
                del selected[vertex]
                continue
            if partial_check and not partial_check(selected, pair):
                stats['partial_graph_failure'] += 1
                del selected[vertex]
                continue
            remaining = [list(values) for values in possible]
            feasible = True
            for j in range(count):
                if j in selected:
                    continue
                remaining[j] = [aj for aj in possible[j] if pair(vertex, value, j, aj) is not None]
                if not remaining[j]:
                    stats['empty_propagated_domain'] += 1
                    feasible = False
                    break
            if feasible:
                visit(remaining, selected)
            del selected[vertex]
            if interrupted or reached_limit:
                return

    if all(domains):
        visit([list(range(len(domain))) for domain in domains], {})
    else:
        stats['empty_initial_domain'] = 1
    return dict(status='FOUND' if solutions else ('TIME_LIMIT' if interrupted else 'NO_ASSEMBLY'),
                exhaustive=not (interrupted or reached_limit), solutions=solutions,
                statistics=dict(stats), seconds=time.monotonic()-started)
