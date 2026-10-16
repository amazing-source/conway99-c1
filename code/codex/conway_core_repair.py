"""Rebuild deleted seed vertices together with new Conway vertices.

A PSD principal core with T rank29 and U rank39 leaves one Schur
dimension in each global Gram, handled by binary column domains and
sign variables. Lower-rank cores use exact PSD/rank checks and finite
forbidden-assignment cuts on small residual principal matrices.
No old kernel is imposed on the repaired vertices.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_completion_columns import prepare, inverse_on_range
from hmatch_cycle_reflections import LABELS, B, new_candidate_checks
from hmatch_pure_switch_kernel_gate import integer_kernel
from four_star_complete import sr_graph, is_srg
from schur_domain_join import residual_rank_check
from odd9_endpoint_mate_family import exact_psd

ALL_LABELS = [p for p in combinations(range(14), 2) if p[1] != (p[0] ^ 1)]
DISC_CLASSES = ((2,14),(1,7))


def disc_check(determinant, form):
    """Apply the peer-proved DISC necessary classes using integers only.

    LAB messages886-887 supply the global lattice theorem. This routine
    constructs new Schur determinant consequences, not an independent
    audit of that theorem. Both parity possibilities are retained.
    """
    assert determinant > 0
    checks = []
    for square_class in DISC_CLASSES[form]:
        quotient, remainder = divmod(determinant,square_class)
        root = isqrt(quotient)
        passes = remainder == 0 and root*root == quotient
        checks.append(dict(square_class=square_class,remainder=remainder,quotient=str(quotient),floor_sqrt=str(root),passes=passes))
    return dict(determinant=str(determinant),allowed=any(c['passes'] for c in checks),tests=checks)


def positive_principal_set(matrix, size):
    chosen = []
    for i in range(len(matrix)):
        trial = chosen+[i]
        psd, rank, _ = exact_psd([[matrix[a][b] for b in trial] for a in trial])
        if psd and rank == len(trial):
            chosen = trial
            if len(chosen) == size:
                return chosen
    return None


def offsets(p, q):
    common = len(set(p)&set(q))
    mates = sum((r ^ 1) in q for r in p)
    return 3*common+mates-2, 4*common-mates+2


def column_domain(label, core_labels, gamma, kernels, inverses, budgets, seconds, limit=10000, disc_context=None):
    size = len(core_labels)
    model = cp_model.CpModel()
    d = [model.NewBoolVar('d_%d'%i) for i in range(size)]
    k8 = np.array([offsets(p, label)[0] for p in core_labels], dtype=np.int64)
    l15 = np.array([offsets(p, label)[1] for p in core_labels], dtype=np.int64)
    for form, kernel, offset, denominator, sign in [('T', kernels[0], k8, 8, -1), ('U', kernels[1], l15, 15, 1)]:
        for q in kernel.T:
            rhs = sign*int(q@offset)
            if rhs % denominator:
                return dict(label=label, complete=True, domains=[], status='INTEGER_RANGE_OBSTRUCTION', form=form)
            model.Add(sum(int(q[i])*d[i] for i in range(size)) == rhs//denominator)
    incidence = np.array([[int(r in p) for p in core_labels] for r in range(14)], dtype=np.int64)
    for r in range(14):
        target = 2-int(r in label)-int((r ^ 1) in label)
        count = sum(d[i] for i, p in enumerate(core_labels) if r in p)
        absent = 12-int(incidence[r].sum())-int(r in label)
        model.Add(count <= target)
        model.Add(count >= max(0, target-absent))
    for i, p in enumerate(core_labels):
        model.Add(d[i]+sum(int(gamma[i,j])*d[j] for j in range(size)) <= 2-len(set(p)&set(label)))
    capacity = 2-gamma-gamma@gamma-incidence.T@incidence
    for i, j in combinations(range(size), 2):
        assert capacity[i,j] >= 0
        if capacity[i,j] == 0:
            model.Add(d[i]+d[j] <= 1)
    model.Add(sum(d) <= 12)
    ti, tn, td = inverses[0]
    ui, un, ud = inverses[1]
    domains, stats = [], Counter()
    disc_obstructions = []

    class Collect(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            values = np.array([self.Value(x) for x in d], dtype=np.int64)
            bt = (-8*values-k8)[ti].astype(object)
            bu = (15*values-l15)[ui].astype(object)
            rt = 20*td-int(bt@tn@bt)
            ru = 50*ud-int(bu@un@bu)
            stats['linear_binary_columns'] += 1
            if rt < 0 or (budgets[0] == 0 and rt):
                stats['T_SCHUR_FAILURE'] += 1
                return
            if ru < 0 or (budgets[1] == 0 and ru):
                stats['U_SCHUR_FAILURE'] += 1
                return
            if disc_context:
                for f,residual in enumerate((rt,ru)):
                    if budgets[f] == 1 and residual:
                        determinant, remainder = divmod(disc_context[f]*residual,inverses[f][2])
                        assert remainder == 0
                        check = disc_check(determinant,f)
                        if not check['allowed']:
                            stats['DISC_%s_FAILURE'%('T','U')[f]] += 1
                            if len(disc_obstructions) < 16:
                                disc_obstructions.append(dict(form=('T','U')[f],neighbours=np.flatnonzero(values).tolist(),
                                    schur_numerator=str(residual),schur_denominator=str(inverses[f][2]),**check))
                            return
            domains.append(dict(neighbours=np.flatnonzero(values).tolist(),
                T_coordinates=list(map(int, bt)), U_coordinates=list(map(int, bu)),
                T_residual=str(rt), U_residual=str(ru)))
            if len(domains) >= limit:
                self.StopSearch()

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.max_time_in_seconds = max(.01, seconds)
    status = solver.Solve(model, Collect())
    return dict(label=label, status=solver.StatusName(status),
                complete=status in (cp_model.OPTIMAL, cp_model.INFEASIBLE),
                domains=domains, statistics=dict(stats), solver_seconds=solver.WallTime(),disc_obstructions=disc_obstructions)


def signed_join(core_labels, gamma, missing, domains, inverses, budgets, seconds, full=False, disc_context=None):
    """Exact assembly using the two remaining Schur rank budgets."""
    started = time.monotonic()
    assert all(b >= 0 for b in budgets)
    size, count = len(core_labels), len(missing)
    model = cp_model.CpModel()
    choices = [model.NewIntVar(0, len(domain)-1, 'choice_%d'%i) for i, domain in enumerate(domains)]
    signs = {f:[model.NewBoolVar('sign_%d_%d'%(f, i)) for i in range(count)] for f in range(2) if budgets[f] == 1}
    for group in signs.values():
        model.Add(group[0] == 0)
    graph = [[0]*(size+count) for _ in range(size+count)]
    for i in range(size):
        for j in range(size):
            graph[i][j] = int(gamma[i,j])
    for i, domain in enumerate(domains):
        for c in range(size):
            bits = [int(c in d['neighbours']) for d in domain]
            if min(bits) == max(bits):
                variable = bits[0]
            else:
                variable = model.NewBoolVar('adj_%d_%d'%(c, size+i))
                model.AddElement(choices[i], bits, variable)
            graph[c][size+i] = graph[size+i][c] = variable
    coordinates = [[(np.array(d['T_coordinates'], dtype=object), np.array(d['U_coordinates'], dtype=object),
                     int(d['T_residual']), int(d['U_residual'])) for d in domain] for domain in domains]
    tn, td, un, ud = inverses[0][1], inverses[0][2], inverses[1][1], inverses[1][2]
    products_t = [[tn@d[0] for d in domain] for domain in coordinates]
    products_u = [[un@d[1] for d in domain] for domain in coordinates]
    masks = [[sum(1 << c for c in d['neighbours']) for d in domain] for domain in domains]
    pair_common = {}
    pair_stats = []
    for i, j in combinations(range(count), 2):
        if time.monotonic() >= started+seconds:
            return dict(status='TABLE_TIME_LIMIT', complete=False, pair_statistics=pair_stats)
        k8, l15 = offsets(missing[i], missing[j])
        allowed = []
        failed_pairs = []
        root_common = len(set(missing[i])&set(missing[j]))
        for ai, left in enumerate(coordinates[i]):
            for aj, right in enumerate(coordinates[j]):
                common = (masks[i][ai]&masks[j][aj]).bit_count()
                if common+root_common > 2:
                    continue
                pt = int(left[0]@products_t[j][aj])
                pu = int(left[1]@products_u[j][aj])
                for edge in (0, 1):
                    if common+root_common+edge > 2:
                        continue
                    rt = td*(-8*edge-k8)-pt
                    ru = ud*(15*edge-l15)-pu
                    determinants = [left[2]*right[2]-rt*rt, left[3]*right[3]-ru*ru]
                    if any(det < 0 or (budgets[f] <= 1 and det != 0) for f,det in enumerate(determinants)):
                        if len(domains[i])*len(domains[j]) <= 16:
                            failed_pairs.append(dict(left_choice=ai,right_choice=aj,edge=edge,
                                T_residual_entries=list(map(str,(left[2],rt,right[2]))),T_denominator=str(td),
                                U_residual_entries=list(map(str,(left[3],ru,right[3]))),U_denominator=str(ud),
                                T_determinant_numerator=str(left[2]*right[2]-rt*rt),
                                U_determinant_numerator=str(left[3]*right[3]-ru*ru)))
                        continue
                    parity_options = [([int((rt,ru)[f] < 0)] if (rt,ru)[f] else [0,1]) for f in signs]
                    allowed.extend((ai, aj, edge, common, *parities) for parities in product(*parity_options))
        pair_stats.append(dict(left=i, right=j, pairs=len(domains[i])*len(domains[j]), allowed_rows=len(allowed)))
        if not allowed:
            return dict(status='INCOMPATIBLE_COLUMN_PAIR', complete=True, empty_pair=[missing[i], missing[j]],
                        pair_statistics=pair_stats, exact_pair_obstructions=failed_pairs)
        edge = model.NewBoolVar('edge_%d_%d'%(i,j))
        common_var = model.NewIntVar(0,2-root_common,'common_core_%d_%d'%(i,j))
        pair_common[i,j] = common_var
        parities = [model.NewBoolVar('parity_%d_%d_%d'%(f,i,j)) for f in signs]
        for group, parity in zip(signs.values(), parities):
            model.AddBoolXOr([group[i], group[j], parity.Not()])
        model.AddAllowedAssignments([choices[i], choices[j], edge, common_var, *parities], allowed)
        graph[size+i][size+j] = graph[size+j][size+i] = edge
    labels = list(core_labels)+list(missing)
    if not full:
        # In the complete84 case, PSD plus the global rank/trace identity
        # already proves all SRG constraints. For a partial block, impose
        # its combinatorial conditions explicitly.
        incidence = np.array([[int(r in p) for p in labels] for r in range(14)], dtype=np.int64)
        products = {}
        def conjunction(x, y):
            if isinstance(x, int):
                return y if x else 0
            if isinstance(y, int):
                return x if y else 0
            if x.Index() == y.Index():
                return x
            key = tuple(sorted((x.Index(), y.Index())))
            if key not in products:
                z = model.NewBoolVar('and_%d_%d'%key)
                model.AddMultiplicationEquality(z, [x,y])
                products[key] = z
            return products[key]
        for i, label in enumerate(labels):
            model.Add(sum(graph[i]) <= 12)
            for r in range(14):
                target = 2-int(r in label)-int((r ^ 1) in label)
                total = sum(graph[i][j] for j, p in enumerate(labels) if r in p)
                model.Add(total <= target)
                if int(incidence[r].sum()) == 12:
                    model.Add(total == target)
        for i, j in combinations(range(len(labels)), 2):
            root_common = len(set(labels[i])&set(labels[j]))
            if j < size:
                # Direct domain indicators retain the correlation between
                # two entries of the same new column without AND variables.
                terms = []
                for v, domain in enumerate(domains):
                    flags = [int((mask >> i & 1) and (mask >> j & 1)) for mask in masks[v]]
                    if min(flags) == max(flags):
                        terms.append(flags[0])
                    else:
                        flag = model.NewBoolVar('old_pair_%d_%d_col_%d'%(i,j,v))
                        model.AddElement(choices[v],flags,flag)
                        terms.append(flag)
                model.Add(sum(terms) <= 2-root_common-int(gamma[i,j])-int(gamma[i]@gamma[j]))
            elif i >= size:
                model.Add(graph[i][j]+pair_common[i-size,j-size]
                          +sum(conjunction(graph[i][z],graph[j][z]) for z in range(size,len(labels))) <= 2-root_common)
            else:
                model.Add(graph[i][j]+sum(conjunction(graph[i][z], graph[j][z]) for z in range(len(labels))) <= 2-root_common)
    iterations, rank_cuts = 0, []
    while True:
        remaining = started+seconds-time.monotonic()
        if remaining <= 0:
            return dict(status='ASSEMBLY_TIME_LIMIT',complete=False,pair_statistics=pair_stats,rank_cuts=rank_cuts,iterations=iterations)
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = remaining
        status = solver.Solve(model)
        iterations += 1
        result = dict(status=solver.StatusName(status), complete=status in (cp_model.OPTIMAL, cp_model.INFEASIBLE),
                      pair_statistics=pair_stats, solver_seconds=solver.WallTime(), seconds=time.monotonic()-started,
                      iterations=iterations,rank_cuts=rank_cuts)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            return result
        values = [solver.Value(x) for x in choices]
        adjacency = np.array([[x if isinstance(x, int) else solver.Value(x) for x in row] for row in graph], dtype=np.int64)
        residuals = []
        incompatible = False
        for f, (inverse, scale, diagonal) in enumerate(zip(inverses, (-8,15), (20,50))):
            residual = [[0]*count for _ in range(count)]
            for i in range(count):
                residual[i][i] = coordinates[i][values[i]][2+f]
                for j in range(i):
                    geometry = offsets(missing[i], missing[j])[f]
                    cross = scale*int(adjacency[size+i,size+j])-geometry
                    residual[i][j] = residual[j][i] = inverse[2]*cross-int(coordinates[i][values[i]][f]@inverse[1]@coordinates[j][values[j]][f])
            residuals.append(residual)
            witness = None
            disc_certificate = None
            if disc_context and budgets[f]:
                proposed = positive_principal_set(residual,budgets[f])
                if proposed is not None:
                    minor = int(sp.Matrix([[residual[a][b] for b in proposed] for a in proposed]).det(method='domain-ge'))
                    determinant,remainder = divmod(disc_context[f]*minor,inverse[2]**budgets[f])
                    assert remainder == 0
                    check = disc_check(determinant,f)
                    if not check['allowed']:
                        witness = proposed
                        disc_certificate = check
            if witness is None and not residual_rank_check(residual,budgets[f]):
                witness = list(range(count))
                for i in list(witness):
                    trial = [j for j in witness if j != i]
                    principal = [[residual[a][b] for b in trial] for a in trial]
                    if trial and not residual_rank_check(principal,budgets[f]):
                        witness = trial
            if witness is not None:
                incompatible = True
                variables = [choices[i] for i in witness]
                forbidden = [values[i] for i in witness]
                free_pairs = []
                for i,j in combinations(witness,2):
                    if i > j:
                        i,j = j,i
                    left,right = coordinates[i][values[i]],coordinates[j][values[j]]
                    k8,l15 = offsets(missing[i],missing[j])
                    common = (masks[i][values[i]]&masks[j][values[j]]).bit_count()+len(set(missing[i])&set(missing[j]))
                    possible_edges = []
                    for edge in (0,1):
                        if common+edge > 2:
                            continue
                        rt = td*(-8*edge-k8)-int(left[0]@products_t[j][values[j]])
                        ru = ud*(15*edge-l15)-int(left[1]@products_u[j][values[j]])
                        dets = [left[2]*right[2]-rt*rt,left[3]*right[3]-ru*ru]
                        if all(det >= 0 and (budgets[g] > 1 or det == 0) for g,det in enumerate(dets)):
                            possible_edges.append(edge)
                    assert int(adjacency[size+i,size+j]) in possible_edges
                    if len(possible_edges) > 1:
                        variables.append(graph[size+i][size+j])
                        forbidden.append(int(adjacency[size+i,size+j]))
                        free_pairs.append([missing[i],missing[j]])
                model.AddForbiddenAssignments(variables,[forbidden])
                principal = [[residual[a][b] for b in witness] for a in witness]
                psd,rank,reason = exact_psd(principal)
                rank_cuts.append(dict(form=('T','U')[f],rank_budget=budgets[f],
                    labels=[missing[i] for i in witness],domain_indices=[values[i] for i in witness],
                    free_edge_pairs=free_pairs,edge_values=forbidden[len(witness):],
                    violation='DISC' if disc_certificate else 'RANK_BUDGET' if psd else 'NOT_PSD',observed_rank=rank if psd else None,
                    disc_certificate=disc_certificate,
                    exact_psd_reason=reason,denominator=str(inverse[2]),
                    residual_numerator=[[str(residual[a][b]) for b in witness] for a in witness]))
        if incompatible:
            if iterations <= 5 or iterations % 25 == 0:
                print(json.dumps(dict(stage='SMALL_SCHUR_CUTS',iterations=iterations,cuts=len(rank_cuts))),flush=True)
            continue
        incidence = np.array([[int(r in p) for p in labels] for r in range(14)], dtype=np.int64)
        c2 = adjacency@adjacency+adjacency+incidence.T@incidence
        np.fill_diagonal(c2, 0)
        assert not np.any(c2 > 2)
        assert not np.any(adjacency.sum(axis=1) > 12)
        result.update(assignment=values, labels=labels, adjacency=adjacency.tolist(),
                      T_residual_numerator=residuals[0], U_residual_numerator=residuals[1])
        if full:
            full_graph = sr_graph(adjacency, labels, 14)
            assert is_srg(full_graph, 14)
            result['adjacency99'] = full_graph.tolist()
        return result


def run(source, repair_file, repair_index, output, outside=(4,6), full=False, restore_only=False, seconds=60, per_column=5, disc=False):
    started = time.monotonic()
    record = json.loads(Path(source).read_text(encoding='utf-8'))
    gamma, t8, u15, _, _ = prepare(record)
    repair = json.loads(Path(repair_file).read_text(encoding='utf-8'))['repairs'][repair_index]
    core = repair['core_indices']
    labels = [LABELS[i] for i in core]
    cg, ct, cu = (a[np.ix_(core,core)] for a in (gamma,t8,u15))
    kernels = integer_kernel(ct), integer_kernel(cu)
    inverses = inverse_on_range(ct), inverse_on_range(cu)
    budgets = 30-len(inverses[0][0]), 40-len(inverses[1][0])
    assert all(b >= 0 for b in budgets)
    disc_context = tuple(int(sp.Matrix(matrix[np.ix_(inverse[0],inverse[0])].tolist()).det(method='domain-ge'))
                         for matrix,inverse in zip((ct,cu),inverses)) if disc else None
    deleted = [LABELS[i] for i in repair['removed_indices']]
    missing = ([p for p in ALL_LABELS if p not in labels] if full
               else deleted if restore_only else [tuple(outside)]+deleted)
    print(json.dumps(dict(stage='CORE', size=len(core), T_rank=len(inverses[0][0]), U_rank=len(inverses[1][0]),
                          deleted=deleted, missing=len(missing), seconds=time.monotonic()-started)), flush=True)
    report = dict(source_file=str(source), repair_file=str(repair_file), repair_index=repair_index,
                  core_indices=core, core_labels=labels, missing_labels=missing, rank_budgets=budgets,
                  inverse_denominators=[str(inv[2]) for inv in inverses], columns=[], status='INCOMPLETE')
    if disc_context:
        report.update(disc_enabled=True,core_principal_determinants=list(map(str,disc_context)),
                      disc_theorem_source='LAB messages886-887; necessary global classes T:2 or14, U:1 or7. No parity lemma assumed.')
        for f in range(2):
            if budgets[f] == 0:
                check = disc_check(disc_context[f],f)
                if not check['allowed']:
                    report.update(status='NO_COMPLETION_CORE_DISC',core_disc_obstruction=dict(form=('T','U')[f],**check))
                    Path(output).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
                    print(json.dumps(dict(status=report['status'],form=('T','U')[f])),flush=True)
                    return report
    domains = []
    for label in missing:
        remaining = started+seconds-time.monotonic()
        if remaining <= 0:
            break
        entry = column_domain(label, labels, cg, kernels, inverses, budgets, min(per_column,remaining),disc_context=disc_context)
        report['columns'].append(entry)
        print(json.dumps(dict(stage='COLUMN', label=label, complete=entry['complete'], count=len(entry['domains']),
                              status=entry['status'], statistics=entry.get('statistics'))), flush=True)
        if entry['complete'] and not entry['domains']:
            report.update(status='NO_COMPLETION_OF_CORE', empty_label=label)
            break
        if not entry['complete']:
            break
        domains.append(entry['domains'])
        if label in LABELS and not disc:
            original = LABELS.index(label)
            neighbours = np.flatnonzero(gamma[original,core]).tolist()
            assert any(d['neighbours']==neighbours for d in entry['domains']), 'The new domain model must retain the accepted original column.'
    if len(domains) == len(missing):
        joined = signed_join(labels,cg,missing,domains,inverses,budgets,max(.01,started+seconds-time.monotonic()),full,disc_context)
        report['assembly'] = joined
        print(json.dumps({k:v for k,v in joined.items() if k not in ('labels','adjacency','adjacency99','T_residual_numerator','U_residual_numerator','pair_statistics','rank_cuts','exact_pair_obstructions')}
                         | dict(rank_cuts=len(joined.get('rank_cuts',[])),pair_witnesses=len(joined.get('exact_pair_obstructions',[])))),flush=True)
        if 'adjacency' in joined:
            report['status'] = 'SRG99_CONSTRUCTED' if full else 'PARTIAL_REPAIR_CONSTRUCTED'
            hit_file = Path(output).with_name(Path(output).stem+'_CONSTRUCTION.json')
            hit_file.write_text(json.dumps(joined,indent=2)+'\n',encoding='utf-8')
            report['construction_file'] = str(hit_file)
            if not full:
                index = {tuple(p):i for i,p in enumerate(joined['labels'])}
                order = [index[p] for p in LABELS]
                g44 = np.array(joined['adjacency'],dtype=np.int64)[np.ix_(order,order)]
                verdict = new_candidate_checks(g44)
                assert verdict in ('H_MATCH_BROKEN','H_MATCH_INTACT')
                report['central_matching_verdict'] = verdict
                report['changed_seed_edges'] = int(np.count_nonzero(g44-gamma))//2
                seed_file = Path(output).with_name(Path(output).stem+'_SEED44.json')
                seed_file.write_text(json.dumps(dict(labels=LABELS,edges=[[i,j] for i,j in combinations(range(44),2) if g44[i,j]],
                                                     source_file=str(source),repair_report=str(output),combinatorial_verdict=verdict),indent=2)+'\n',encoding='utf-8')
                report['repaired_seed_file'] = str(seed_file)
        elif joined['complete']:
            assert not restore_only or disc, 'The new reconstruction model must retain the accepted original seed.'
            report['status'] = 'NO_COMPLETION_OF_CORE'
    report['seconds'] = time.monotonic()-started
    Path(output).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('columns','assembly','core_labels','core_indices','missing_labels')}),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--repairs',required=True)
    parser.add_argument('--repair-index',type=int,default=0)
    parser.add_argument('--output',required=True)
    parser.add_argument('--outside',default='4,6')
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--restore-only',action='store_true')
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--per-column',type=float,default=5)
    parser.add_argument('--disc',action='store_true',help='Use the global lattice square classes supplied by LAB886-887 as construction cuts.')
    args=parser.parse_args()
    run(args.source,args.repairs,args.repair_index,args.output,tuple(map(int,args.outside.split(','))),
        args.full,args.restore_only,args.seconds,args.per_column,args.disc)
