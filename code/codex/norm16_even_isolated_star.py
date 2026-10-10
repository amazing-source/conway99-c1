"""Bounded local completion of one forced isolated Z star (D independent).

The B neighbours of z are selected from core/D types and matched so N(z)
induces7K2. All common-neighbour upper bounds on the37-vertex support
are enforced. Feasibility here is not an SRG completion.
"""
from itertools import combinations
import argparse
import json
from math import lcm
import time
import numpy as np
import sympy as sp
from ortools.sat.python import cp_model
from norm16_even_margins_probe import instance
from norm16_schur_data import ROOT, source_data
from norm16_independent_catalogue import positive_semidefinite


def spectral_linear_cut(a, masks, chosen, chosen_edges):
    """A global exact Rayleigh cut, with floats used only to find coefficients.

    Set the base coefficients to beta and each selected B coefficient to
    v_i = mask_i.w. All column sums of the selected masks are fixed, hence
    the sum of this test vector is fixed. Its quadratic form for
    27I-9A+J is consequently linear in the selection and matching variables.
    The returned integer inequality is valid for every completion.
    """
    nbase, nsel = len(a), len(chosen)
    full = np.zeros((nbase+nsel, nbase+nsel), dtype=np.int64)
    full[:nbase, :nbase] = a
    full[nbase:, :nbase] = masks[chosen]
    full[:nbase, nbase:] = masks[chosen].T
    locations = {i: k for k, i in enumerate(chosen)}
    for i, j in chosen_edges:
        full[nbase+locations[i], nbase+locations[j]] = 1
        full[nbase+locations[j], nbase+locations[i]] = 1
    q9 = 27*np.eye(len(full), dtype=np.int64)-9*full+np.ones_like(full)
    transform = np.zeros((len(full), 2*nbase), dtype=np.int64)
    transform[:nbase, :nbase] = np.eye(nbase, dtype=np.int64)
    transform[nbase:, nbase:] = masks[chosen]
    values, vectors = np.linalg.eigh(transform.T @ q9 @ transform)
    if values[0] >= -1e-8:
        return None
    candidate = vectors[:, 0]/max(abs(vectors[:, 0]))
    for scale in (16, 64, 256, 1024):
        coeff = np.rint(scale*candidate).astype(np.int64)
        test = transform @ coeff
        value = int(test @ q9 @ test)
        if value >= 0:
            continue
        beta, w = coeff[:nbase], coeff[nbase:]
        v = masks @ w
        total = int(sum(beta)+(masks[chosen].sum(axis=0) @ w))
        constant = int(27*(beta @ beta)-9*(beta @ a @ beta))+total*total
        linear = 27*v*v-18*v*(masks @ beta)
        assert constant+sum(int(linear[i]) for i in chosen)-18*sum(int(v[i])*int(v[j]) for i,j in chosen_edges) == value
        return constant, linear, v, beta.tolist(), w.tolist(), value
    return None


def solve(ci, oi, pair, seconds, spectral_pairs=True, full_spectral=False):
    cores, cases, _ = source_data()
    core = np.array(cores[ci]['representatives'][0], dtype=int)
    a = np.zeros((25, 25), dtype=int)
    a[:8, 8:16], a[8:16, :8] = core, core.T
    for d, r in enumerate(cases[ci]['orbits'][oi]['representative']):
        for p in r[:2]+[8+q for q in r[2:]]:
            a[p, 16+d] = a[16+d, p] = 1
    for d in pair:
        a[24, 16+d] = a[16+d, 24] = 1
    common = a @ a
    caps = 2-a-common
    np.fill_diagonal(caps, 0)
    _, _, labels, _ = instance(ci, oi, 3)
    types = [label for label in labels if label[0] == 'B']
    masks, common_rows, kept = [], [], []
    for label in types:
        _, p, q, dm = label
        mask = np.array([int(i in (p, 8+q)) if i < 16 else ((dm >> (i-16)) & 1) if i < 24 else 1 for i in range(25)])
        row = a @ mask
        if np.any(row > 2-mask):
            continue
        if any(mask[i] and mask[j] and caps[i, j] <= 0 for i, j in combinations(range(25), 2)):
            continue
        masks.append(mask)
        common_rows.append(row)
        kept.append(label)
    types = kept
    scale, costs = None, None
    removed_single = 0
    if spectral_pairs:
        m9 = 27*np.eye(25, dtype=np.int64)-9*a+np.ones((25,25), dtype=np.int64)
        assert positive_semidefinite(m9.tolist())
        inverse = sp.Matrix(m9).inv()
        denominator = lcm(*(int(v.q) for v in inverse))
        inverse_integer = np.array(denominator*inverse, dtype=object)
        k = np.array([[1-9*int(v) for v in row] for row in masks], dtype=object)
        costs = k @ inverse_integer @ k.T
        scale = 9*denominator
        keep = [i for i in range(len(types)) if 3*scale+denominator-int(costs[i,i]) >= 0]
        removed_single = len(types)-len(keep)
        types = [types[i] for i in keep]
        masks = [masks[i] for i in keep]
        common_rows = [common_rows[i] for i in keep]
        costs = costs[np.ix_(keep, keep)]
    n = len(types)
    masks = np.array(masks)
    common_rows = np.array(common_rows)
    model = cp_model.CpModel()
    xs = [model.new_bool_var(f'b{i}') for i in range(n)]
    model.add(sum(xs) == 12)
    for p in range(16):
        model.add(sum(xs[i] for i in range(n) if masks[i, p]) == int(2-common[p, 24]))
    for d in range(8):
        model.add(sum(xs[i] for i in range(n) if masks[i, 16+d]) == 2-int(d in pair))
    for p, q in combinations(range(24), 2):
        active = [xs[i] for i in range(n) if masks[i, p] and masks[i, q]]
        if active:
            model.add(sum(active) <= int(caps[p, q]))
    partner = [[] for _ in range(n)]
    edge_variables = {}
    incompatible = matching_edges = 0
    for i, j in combinations(range(n), 2):
        nonadj_ok = adjacent_ok = True
        if spectral_pairs:
            di = 3*scale+denominator-int(costs[i,i])
            dj = 3*scale+denominator-int(costs[j,j])
            v0 = denominator-int(costs[i,j])
            nonadj_ok = di*dj-v0*v0 >= 0
            adjacent_ok = di*dj-(v0-scale)**2 >= 0
        if int(masks[i] @ masks[j]) > 2:
            model.add(xs[i]+xs[j] <= 1)
            incompatible += 1
            continue
        matching_possible = True
        # The common z must be the unique common neighbour of a matching edge.
        if int(masks[i] @ masks[j]) != 1:
            matching_possible = False
        # A B touching a D-neighbour of z already has its partner in N(z).
        if sum(masks[i, 16+d] for d in pair) or sum(masks[j, 16+d] for d in pair):
            matching_possible = False
        if np.any(common_rows[i, :24]+masks[j, :24] > 2-masks[i, :24]) or np.any(common_rows[j, :24]+masks[i, :24] > 2-masks[j, :24]):
            matching_possible = False
        if not adjacent_ok:
            matching_possible = False
        if matching_possible:
            edge = model.new_bool_var(f'e{i}_{j}')
            partner[i].append(edge)
            partner[j].append(edge)
            edge_variables[i,j] = edge
            matching_edges += 1
        if not nonadj_ok:
            model.add(xs[i]+xs[j] <= 1+edge_variables.get((i,j),0))
    for i in range(n):
        if sum(masks[i, 16+d] for d in pair):
            continue
        model.add(sum(partner[i]) == xs[i])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    answer = cp_model.UNKNOWN
    started_search = time.monotonic()
    cuts = []
    linear_cuts = []
    full_psd = False
    while True:
        remaining = seconds-(time.monotonic()-started_search)
        if remaining <= 0:
            break
        solver.parameters.max_time_in_seconds = remaining
        answer = solver.solve(model)
        if answer not in (cp_model.OPTIMAL, cp_model.FEASIBLE) or not full_spectral:
            break
        chosen = [i for i in range(n) if solver.value(xs[i])]
        r = [[(3*scale if i == j else 0)+denominator-int(costs[i,j])
              -(scale if (min(i,j),max(i,j)) in edge_variables and solver.value(edge_variables[min(i,j),max(i,j)]) else 0)
              for j in chosen] for i in chosen]
        if positive_semidefinite(r):
            full_psd = True
            break
        selected_edges = [(i,j) for (i,j), edge in edge_variables.items() if solver.value(edge)]
        global_cut = spectral_linear_cut(a, masks, chosen, selected_edges)
        if global_cut is not None:
            constant, linear, v, beta, w, value = global_cut
            terms = [int(linear[i])*xs[i] for i in range(n) if linear[i]]
            terms += [-18*int(v[i])*int(v[j])*edge for (i,j), edge in edge_variables.items() if v[i] and v[j]]
            model.add(sum(terms) >= -constant)
            linear_cuts.append({'beta': beta, 'w': w, 'negative_value_on_rejected_frame': value})
            if len(linear_cuts) % 10 == 0:
                print(json.dumps({'case': ci, 'orbit': oi, 'D_pair': pair, 'global_Rayleigh_cuts': len(linear_cuts), 'elapsed_search': time.monotonic()-started_search}), flush=True)
            continue
        subset = list(range(len(chosen)))
        for drop in list(subset):
            smaller = [i for i in subset if i != drop]
            if smaller and not positive_semidefinite([[r[i][j] for j in smaller] for i in smaller]):
                subset = smaller
        ids = [chosen[i] for i in subset]
        literals = [xs[i].Not() for i in ids]
        for i,j in combinations(ids,2):
            edge = edge_variables.get((min(i,j),max(i,j)))
            if edge is not None:
                literals.append(edge.Not() if solver.value(edge) else edge)
        model.add_bool_or(literals)
        cuts.append(len(ids))
        if len(cuts) % 20 == 0:
            print(json.dumps({'case': ci, 'orbit': oi, 'D_pair': pair, 'PSD_cuts': len(cuts), 'elapsed_search': time.monotonic()-started_search}), flush=True)
    if full_spectral and not full_psd and answer in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        answer = cp_model.UNKNOWN
    result = {'case': ci, 'orbit': oi, 'D_pair': pair, 'candidates': n, 'incompatible_pairs': incompatible,
              'matching_edges': matching_edges, 'status': solver.status_name(answer), 'seconds': solver.wall_time, 'branches': solver.num_branches,
              'exact_spectral_minors_through_2': spectral_pairs, 'single_candidates_removed_spectrally': removed_single,
              'full_PSD_found': full_psd, 'exact_PSD_cut_sizes': cuts, 'global_Rayleigh_cuts': linear_cuts, 'total_search_seconds': time.monotonic()-started_search}
    if answer in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [i for i in range(n) if solver.value(xs[i])]
        result['chosen_types'] = [types[i] for i in chosen]
        result['matching_B_edges'] = []
        for ii, i in enumerate(chosen):
            for jj, j in enumerate(chosen):
                if jj <= ii:
                    continue
                shared = set(v.index for v in partner[i]) & set(v.index for v in partner[j])
                if any(solver.boolean_value(model.get_bool_var_from_proto_index(index)) for index in shared):
                    result['matching_B_edges'].append([ii, jj])
        full = np.zeros((37, 37), dtype=int)
        full[:25, :25] = a
        full[25:, :25] = masks[chosen]
        full[:25, 25:] = masks[chosen].T
        for i, j in result['matching_B_edges']:
            full[25+i, 25+j] = full[25+j, 25+i] = 1
        cm = full @ full
        assert all(cm[i, j] <= 2-full[i, j] for i, j in combinations(range(37), 2))
        result['adjacency'] = full.tolist()
        result['spectral_probe_min_3I_A_J9'] = float(np.linalg.eigvalsh(3*np.eye(37)-full+np.ones((37,37))/9)[0])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--orbit', type=int, default=226)
    parser.add_argument('--seconds', type=float, default=3)
    parser.add_argument('--full-spectral', action='store_true')
    parser.add_argument('--max-pairs', type=int, default=1)
    parser.add_argument('--output')
    args = parser.parse_args()
    r = source_data()[1][args.case]['orbits'][args.orbit]['representative']
    ss = [set(d[:2]) | {8+q for q in d[2:]} for d in r]
    results = []
    for pair in combinations(range(8), 2):
        if ss[pair[0]] & ss[pair[1]]:
            continue
        item = solve(args.case, args.orbit, list(pair), args.seconds, full_spectral=args.full_spectral)
        results.append(item)
        print(json.dumps({k: v for k, v in item.items() if k not in ('adjacency', 'chosen_types', 'matching_B_edges', 'global_Rayleigh_cuts')}), flush=True)
        if item['status'] in ('FEASIBLE', 'OPTIMAL'):
            break
        if len(results) >= args.max_pairs:
            break
    path = ROOT/(args.output or f'data/codex_norm16_isolated_star_{args.case}_{args.orbit}.json')
    path.write_text(json.dumps({'scope': __doc__, 'seconds_per_pair': args.seconds, 'all_pairs_attempted': len(results) == 20,
                               'exhaustive_exclusion': len(results) == 20 and all(r['status'] == 'INFEASIBLE' for r in results), 'results': results}, indent=2)+'\n')
