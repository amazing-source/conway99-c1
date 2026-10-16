"""Construct switched four-star blocks with extendible outside columns.

Disjoint root-balanced reflections preserve PSD and ranks by congruence.
Unlike the H-MATCH search, this model permits intact central matchings.
The target is actual prolongation: binary outside columns must satisfy
both kernel range equations, root counts and common-neighbour caps.
Exact Schur cuts enforce rank30 T and PSD U for each missing vertex.
Passing all individual columns is still not a simultaneous completion.
"""
import argparse
from collections import Counter
from functools import reduce
from itertools import combinations
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hmatch_joint_reflection_partition import make_cells
from hmatch_cycle_reflections import B, LABELS, new_candidate_checks
from four_star_completion_columns import prepare, column_geometry, inverse_on_range, probe_extension

OUTSIDE = [p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1)]
SCALE = 120


def cover_model(gamma, lengths):
    cells, capacity, rejected = make_cells(gamma, lengths)
    model = cp_model.CpModel()
    chosen = [model.NewBoolVar('cell_%d' % i) for i in range(len(cells))]
    for vertex in range(44):
        model.AddExactlyOne([chosen[i] for i, cell in enumerate(cells) if cell['mask'] >> vertex & 1])
    pairs = Counter()
    for i, j in combinations(range(len(cells)), 2):
        left, right = cells[i], cells[j]
        if left['mask'] & right['mask']:
            continue
        sl, sr = left['support'], right['support']
        scale = left['denominator'] * right['denominator']
        block = left['transform'] @ gamma[np.ix_(sl, sr)] @ right['transform']
        residual = left['transform'] @ capacity[np.ix_(sl, sr)] @ right['transform']
        if np.any((block != 0) & (block != scale)) or np.any(residual < 0):
            model.AddAtMostOne(chosen[i], chosen[j])
            pairs['incompatible'] += 1
        else:
            pairs['compatible'] += 1
    return model, chosen, cells, dict(cell_rejections=rejected, pairs=dict(pairs))


def add_column(model, chosen, cells, gamma, kt, ku, label):
    """Use z=120 R d to keep all kernel equations linear in cell choices."""
    prefix = '%d_%d' % label
    d = [model.NewBoolVar('d_%s_%d' % (prefix, i)) for i in range(44)]
    z = [model.NewIntVar(-SCALE, 2*SCALE, 'z_%s_%d' % (prefix, i)) for i in range(44)]
    k8, l15 = column_geometry(label)
    for kernel, offset, factor in [(kt, k8, -SCALE//8), (ku, l15, SCALE//15)]:
        for q in kernel.T:
            model.Add(sum(int(q[i])*z[i] for i in range(44)) == factor*int(q@offset))
    for r in range(14):
        count = sum(d[i] for i, p in enumerate(LABELS) if r in p)
        target = 2-int(r in label)-int((r ^ 1) in label)
        if r < 4:
            model.Add(count == target)
        else:
            model.Add(count <= target)
    for choice, cell in zip(chosen, cells):
        support, transform, denominator = cell['support'], cell['transform'], cell['denominator']
        assert SCALE % denominator == 0
        coefficients = transform @ gamma[support]
        for a, i in enumerate(support):
            model.Add(denominator*z[i] == SCALE*sum(int(transform[a, b])*d[j]
                      for b, j in enumerate(support))).OnlyEnforceIf(choice)
            model.Add(sum(int(coefficients[a, j])*z[j] for j in range(44))
                      + denominator*SCALE*d[i] <= denominator*SCALE*(2-len(set(LABELS[i]) & set(label)))).OnlyEnforceIf(choice)
    return dict(label=label, d=d, z=z)


def extract_graph(solver, chosen, cells, gamma, t8, u15):
    selected = [cell for choice, cell in zip(chosen, cells) if solver.Value(choice)]
    denominator = lcm(*(cell['denominator'] for cell in selected))
    transform = np.zeros((44, 44), dtype=np.int64)
    for cell in selected:
        support = cell['support']
        transform[np.ix_(support, support)] = (denominator//cell['denominator'])*cell['transform']
    assert np.array_equal(transform@transform, denominator**2*np.eye(44, dtype=np.int64))
    assert np.array_equal(B@transform, denominator*B)
    numerator = transform@gamma@transform
    assert not np.any(numerator % denominator**2)
    candidate = numerator//denominator**2
    verdict = new_candidate_checks(candidate)
    assert verdict in ('H_MATCH_BROKEN', 'H_MATCH_INTACT'), verdict
    assert np.array_equal(transform@t8@transform, denominator**2*(t8-8*(candidate-gamma)))
    assert np.array_equal(transform@u15@transform, denominator**2*(u15+15*(candidate-gamma)))
    return candidate, transform, denominator, verdict, [c['cycle'] for c in selected if c['cycle'] is not None]


def schur_cut(model, column, z_value, inverse, form):
    indices, numerator, denominator = inverse
    k8, l15 = column_geometry(column['label'])
    offset, factor, target = (k8, -8, 20) if form == 'T' else (l15, 15, 50)
    y = (factor*z_value-SCALE*offset)[indices].astype(object)
    w = numerator@y
    norm = int(y@w)
    bound = target*denominator*SCALE**2
    if (form == 'T' and norm == bound) or (form == 'U' and norm <= bound):
        return None
    if norm > bound:
        # Convex PSD norm: 2*y0^t Q*y <= y0^t Q*y0 + target.
        coefficients = [int(2*factor*x) for x in w]
        rhs = norm+bound+2*SCALE*int(w@offset[indices])
        divisor = reduce(gcd, [abs(rhs)]+[abs(x) for x in coefficients]) or 1
        coefficients, rhs = [x//divisor for x in coefficients], rhs//divisor
        if abs(rhs)+2*SCALE*sum(abs(x) for x in coefficients) < 2**61:
            assert sum(c*int(z_value[i]) for c, i in zip(coefficients, indices)) > rhs
            model.Add(sum(c*column['z'][i] for c, i in zip(coefficients, indices)) <= rhs)
            return form+'_SCHUR_TANGENT'
    # At normT<20 rank would rise above30. Excluding this exact z is
    # valid across all partitions, since its norm in source coordinates
    # does not depend on which partition realizes z=120 R d.
    model.AddForbiddenAssignments(column['z'], [list(map(int, z_value))])
    return form+'_SCHUR_VECTOR_NOGOOD'


def run(source, output, lengths=(4, 6, 8), seconds=45, name=None):
    started = time.monotonic()
    records = json.loads(Path(source).read_text(encoding='utf-8'))
    record = records if 'labels' in records else records[name]
    gamma, t8, u15, kt, ku = prepare(record)
    assert kt.shape[1] == 14, 'Saturated T rank30 required.'
    t_inverse, u_inverse = inverse_on_range(t8), inverse_on_range(u15)
    model, chosen, cells, details = cover_model(gamma, lengths)
    active = {OUTSIDE[0]: add_column(model, chosen, cells, gamma, kt, ku, OUTSIDE[0])}
    print(json.dumps(dict(stage='EXTENSION_MODEL', cells=len(cells), seconds=time.monotonic()-started, **details)), flush=True)
    iterations, cuts = [], Counter()
    result = dict(source_file=str(source), source_record=name, root_cycle_lengths=lengths,
                  cells=len(cells), **details, status='TIME_LIMIT',
                  scope='Joint orthogonal construction with necessary outside columns. All40 individual columns passing is not a full SRG completion.')
    while time.monotonic() < started+seconds:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = max(.01, started+seconds-time.monotonic())
        status = solver.Solve(model)
        entry = dict(status=solver.StatusName(status), active_columns=len(active), solver_seconds=solver.WallTime())
        iterations.append(entry)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            result['status'] = 'NO_EXTENDIBLE_BLOCK_IN_SWITCH_FAMILY' if status == cp_model.INFEASIBLE else solver.StatusName(status)
            print(json.dumps(entry), flush=True)
            break
        candidate, transform, denominator, verdict, cycles = extract_graph(solver, chosen, cells, gamma, t8, u15)
        witnesses, added_cuts = [], 0
        for column in active.values():
            d = np.array([solver.Value(x) for x in column['d']], dtype=np.int64)
            z = np.array([solver.Value(x) for x in column['z']], dtype=np.int64)
            assert np.array_equal(denominator*z, SCALE*(transform@d))
            k8, l15 = column_geometry(column['label'])
            assert not np.any((transform@kt).T@(-8*d-k8))
            assert not np.any((transform@ku).T@(15*d-l15))
            assert all(d[i]+int(candidate[i]@d) <= 2-len(set(p)&set(column['label'])) for i, p in enumerate(LABELS))
            for form, inverse in [('T', t_inverse), ('U', u_inverse)]:
                cut = schur_cut(model, column, z, inverse, form)
                if cut:
                    cuts[cut] += 1
                    added_cuts += 1
            witnesses.append(dict(label=column['label'], neighbours=np.flatnonzero(d).tolist()))
        entry.update(cuts_added=added_cuts, changed_edges=int(np.count_nonzero(candidate-gamma))//2)
        if added_cuts:
            print(json.dumps(entry), flush=True)
            continue
        if len(active) == 40:
            hit_file = Path(output).with_name(Path(output).stem+'_CANDIDATE.json')
            hit = dict(labels=LABELS, edges=[[i, j] for i, j in combinations(range(44), 2) if candidate[i, j]],
                       source_file=str(source), transformation_numerator=transform.tolist(), transformation_denominator=denominator,
                       exact_T_U_orthogonal_congruence=True, combinatorial_verdict=verdict,
                       chosen_root_cycles=cycles, individual_column_witnesses=witnesses,
                       scope='40 individually admissible PSD/rank columns. Their mutual compatibility has not been established.')
            hit_file.write_text(json.dumps(hit, indent=2)+'\n', encoding='utf-8')
            result.update(status='ALL_40_INDIVIDUAL_COLUMNS_ADMISSIBLE', candidate_file=str(hit_file))
            print(json.dumps(entry), flush=True)
            break
        probe = probe_extension(candidate, seconds=max(.01, min(5, started+seconds-time.monotonic())),
                                kernels=(transform@kt, transform@ku))
        entry['linear_probe'] = {k: v for k, v in probe.items() if k not in ('columns', 'failure')}
        if probe['status'] == 'ALL_LINEAR_COLUMNS_FEASIBLE':
            new_labels = [label for label in OUTSIDE if label not in active]
        else:
            label = tuple(probe['label'])
            assert label not in active or probe['status'] == 'UNKNOWN'
            new_labels = [label] if label not in active else [next(label for label in OUTSIDE if label not in active)]
        for label in new_labels:
            active[label] = add_column(model, chosen, cells, gamma, kt, ku, label)
        print(json.dumps(entry), flush=True)
    result.update(iterations=iterations, cuts=dict(cuts), active_columns=list(active), seconds=time.monotonic()-started)
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('iterations',)}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--name')
    parser.add_argument('--lengths', default='4,6,8')
    parser.add_argument('--seconds', type=float, default=45)
    args = parser.parse_args()
    run(args.source, args.output, tuple(map(int, args.lengths.split(','))), args.seconds, args.name)
