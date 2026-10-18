"""Place fixed-Gram corner signatures on the actual fourteen root letters.

This relaxation has no unknown adjacency matrix. Each rectangle chooses a
genuine four-corner state, all global moments hold, and B H=0 holds letter
by letter. Short integral eigenvectors and both conditional projectors
give additional necessary pair constraints. An edge in a pair constraint
is existential and is NOT coupled to any other pair. SAT is not a graph.
INFEASIBLE is a CP-SAT verdict for one supplied Gram, not a portable proof.
No root prism budget or root normalization is imposed here.
"""

import argparse
from collections import Counter
import gzip
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sympy as sp
from ortools.sat.python import cp_model
from root_component_corner_tables import enumerate_corner_rows
from root_component_gram_enumeration import integer_psd
from root_component_propagation import LABELS, PAIRS, RECTANGLES
from root_component_resources import atomic_json_write, limit_research_process
from root_component_short_vectors import (
    short_directions, evaluations, filter_domains as short_filter,
    integer_pair_margins, add_integer_overlap_counts)
from root_component_upper_signatures import (
    data_for, filter_domains as upper_filter, corner_filter)
from root_rectangle_domains import signature_domains


def prepare(edges, raw, *, short_norm=4):
    matrix = sp.Matrix(raw)
    assert matrix == matrix.T and all(x.q == 1 for x in matrix)
    assert integer_psd(raw)
    assert integer_psd((28 * sp.eye(matrix.rows) - matrix).tolist())
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    det = int(small.det())
    adj = [[int(x) for x in row] for row in (small.inv() * det).tolist()]
    domains = {tuple(d['rectangle']): d for d in signature_domains(edges, raw)}
    short = short_directions(matrix, maximum_norm=short_norm)
    short_info = short_filter(domains, short)
    upper = data_for(edges, matrix)
    upper_info = upper_filter(edges, matrix, domains, upper)
    tables = enumerate_corner_rows(edges, matrix, domains, anchors, det, adj)
    norms = [d['norm'] for d in short['directions']]
    roots = [i for i, n in enumerate(norms) if n == 2]
    raw_rows = sum(len(t['rows']) for t in tables)
    upper_removed = short_removed = 0
    for table in tables:
        upper_counts = corner_filter(table, domains, upper)
        upper_removed += upper_counts['before'] - upper_counts['after']
        q = tuple(table['rectangle'])
        corners = RECTANGLES[q]
        hs = domains[q]['signatures']
        vals = [evaluations(h, short) for h in hs]
        kept = []
        for row in table['rows']:
            valid = True
            for e, (i, j) in zip(row[4:], combinations(range(4), 2)):
                a, b = vals[row[i]], vals[row[j]]
                c = len(set(LABELS[corners[i]]) & set(LABELS[corners[j]]))
                if integer_pair_margins(a, b, norms)[e] < 2*c or (
                        (e or c) and any(a[d] == b[d] != 0 for d in roots)):
                    valid = False
                    break
            if valid:
                kept.append(row)
        short_removed += len(table['rows']) - len(kept)
        used = sorted({s for row in kept for s in row[:4]})
        remap = {s: i for i, s in enumerate(used)}
        domains[q]['signatures'] = [hs[s] for s in used]
        table['rows'] = [[remap[s] for s in row[:4]] + row[4:] for row in kept]
    info = dict(rank=len(anchors), anchors=anchors, short_vectors=short_info,
                short_norm_counts=dict(Counter(norms)), upper_projector=upper_info,
                original_corner_rows=raw_rows, upper_corner_rows_removed=upper_removed,
                short_corner_rows_removed=short_removed,
                corner_rows=sum(len(t['rows']) for t in tables),
                signature_count=sum(len(d['signatures']) for d in domains.values()),
                empty_rectangles=[list(t['rectangle']) for t in tables if not t['rows']])
    return matrix, anchors, det, adj, domains, tables, short, upper, info


def pair_relations(edges, anchors, det, adj, domains, short, upper):
    """Exact 2x2 tests, allowing either edge value consistently in both tests."""
    positions = {q: i for i, q in enumerate(edges)}
    scale = 225 * upper['denominator']
    upper_den = 28 * scale
    norms = [d['norm'] for d in short['directions']]
    roots = [i for i, n in enumerate(norms) if n == 2]
    def inner(a, b):
        return sum(a[i] * adj[i][j] * b[j]
                   for i in range(len(anchors)) for j in range(len(anchors)))
    states = {}
    for q, item in domains.items():
        states[q] = []
        for h in item['signatures']:
            a = tuple(h[i] for i in anchors)
            v = [7*(15*int(q == e)-3*len(set(q) & set(e))+1)-15*x
                 for e, x in zip(edges, h)]
            cv = [sum(x*y for x, y in zip(row, v)) for row in upper['correction']]
            own = h[positions[q]] if q in positions else 0
            ip = 98*scale//3-14*own*scale+sum(x*x for x in h)*scale+sum(x*y for x, y in zip(v, cv))
            nl = 20*det-8*inner(a, a)
            nu = 10*upper_den//3-ip
            assert nl >= 0 and nu >= 0
            states[q].append((h, a, v, cv, nl, nu, evaluations(h, short)))
    kinds = {}
    for u, v in PAIRS:
        q, r = tuple(x//2 for x in LABELS[u]), tuple(x//2 for x in LABELS[v])
        if q == r:
            continue
        if q > r:
            q, r, u, v = r, q, v, u
        c = len(set(LABELS[u]) & set(LABELS[v]))
        m = sum((x ^ 1) in LABELS[v] for x in LABELS[u])
        kinds.setdefault((q, r, c, m), []).append((u, v))
    result = []
    checks = forbidden = 0
    for (q, r, common, mates), vertices in kinds.items():
        allowed = []
        for si, (ha, sa, va, _, nla, nua, ea) in enumerate(states[q]):
            for sj, (hb, sb, _, cvb, nlb, nub, eb) in enumerate(states[r]):
                checks += 1
                low_ip = inner(sa, sb)
                cross = (ha[positions[r]] if r in positions else 0) + (hb[positions[q]] if q in positions else 0)
                euv15 = -3*len(set(q) & set(r))+1
                up_ip = (49*euv15*(scale//15)-7*cross*scale
                         +sum(x*y for x, y in zip(ha, hb))*scale+sum(x*y for x, y in zip(va, cvb)))
                margins = integer_pair_margins(ea, eb, norms)
                root_same = any(ea[d] == eb[d] != 0 for d in roots)
                for edge in (0, 1):
                    if margins[edge] < 2*common or ((edge or common) and root_same):
                        continue
                    lo = ((2-3*common-mates-8*edge)*det-8*low_ip)
                    up = (15*edge-4*common+mates-2)*(upper_den//15)-up_ip
                    if lo*lo <= nla*nlb and up*up <= nua*nub:
                        allowed.append((si, sj))
                        break
                else:
                    forbidden += 1
        if len(allowed) < len(states[q])*len(states[r]):
            result.append((vertices, allowed))
    return result, dict(pair_types=len(kinds), pair_state_checks=checks,
                        pair_states_forbidden=forbidden, nontrivial_pair_types=len(result))


def solve(edges, raw, seconds=5, *, pairs=True, short_norm=4, progress=None):
    start = time.process_time()
    matrix, anchors, det, adj, domains, tables, short, upper, info = prepare(edges, raw, short_norm=short_norm)
    info['preparation_cpu_seconds'] = time.process_time()-start
    if progress:
        progress(dict(stage='prepared', **info))
    if info['empty_rectangles']:
        return dict(info, status='EXCLUDED_EMPTY_CORNER', portable_unsat_proof=False)
    model = cp_model.CpModel()
    selectors, indicators = [None]*84, [None]*84
    row_hs = [None]*84
    moment_terms = {ij: [] for ij in combinations_with_replacement(anchors, 2)}
    for q, corners in RECTANGLES.items():
        hs = domains[q]['signatures']
        for w in corners:
            row_hs[w] = hs
            selectors[w] = model.new_int_var(0, len(hs)-1, f's_{w}')
            flags = [model.new_bool_var(f'f_{w}_{s}') for s in range(len(hs))]
            indicators[w] = flags
            model.add_exactly_one(flags)
            model.add_map_domain(selectors[w], flags)
            for ij, terms in moment_terms.items():
                i, j = ij
                terms.extend(h[i]*h[j]*flag for h, flag in zip(hs, flags))
    for t in tables:
        q = tuple(t['rectangle'])
        rows = sorted({tuple(row[:4]) for row in t['rows']})
        model.add_allowed_assignments([selectors[w] for w in RECTANGLES[q]], rows)
    for (i, j), terms in moment_terms.items():
        model.add(sum(terms) == 7*int(matrix[i, j]))
    for letter in range(14):
        for i in anchors:
            model.add(sum(flag*h[i] for w, label in enumerate(LABELS) if letter in label
                          for flag, h in zip(indicators[w], row_hs[w])) == 0)
    info['integer_overlaps'] = add_integer_overlap_counts(model, short, [
        (h, flag) for w in range(84) for h, flag in zip(row_hs[w], indicators[w])])
    values = {q: [evaluations(h, short) for h in domains[q]['signatures']] for q in RECTANGLES}
    root_ids = [i for i, d in enumerate(short['directions']) if d['norm'] == 2]
    for di in root_ids:
        for letter in range(14):
            for sign in (-1, 1):
                model.add(sum(flag for q, corners in RECTANGLES.items() for w in corners if letter in LABELS[w]
                              for flag, h in zip(indicators[w], values[q]) if h[di] == sign) == 1)
    relations = []
    if pairs:
        relations, info['pairs'] = pair_relations(edges, anchors, det, adj, domains, short, upper)
        for vertices, allowed in relations:
            for u, v in vertices:
                model.add_allowed_assignments([selectors[u], selectors[v]], allowed)
    assert not model.validate(), model.validate()
    info.update(model_variables=len(model.proto.variables), model_constraints=len(model.proto.constraints),
                build_cpu_seconds=time.process_time()-start, root_matching_equations=28*len(root_ids))
    if progress:
        progress(dict(stage='built', **info))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.linearization_level = 0
    solver.parameters.max_time_in_seconds = max(60, 100*seconds)
    begun = time.process_time()
    done = threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time()-begun >= seconds:
                solver.stop_search()
    timer = threading.Thread(target=stop, daemon=True)
    timer.start()
    try:
        status = solver.solve(model)
    finally:
        done.set()
        timer.join()
    info.update(status=solver.status_name(status), solver_cpu_seconds=time.process_time()-begun,
                branches=solver.num_branches, conflicts=solver.num_conflicts,
                portable_unsat_proof=False, is_graph=False)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [solver.value(s) for s in selectors]
        H = [list(row_hs[w][s]) for w, s in enumerate(selected)]
        # Direct arithmetic checks of the selected signatures and labelled placements.
        for t in tables:
            assert tuple(selected[w] for w in RECTANGLES[tuple(t['rectangle'])]) in {tuple(row[:4]) for row in t['rows']}
        for letter in range(14):
            assert all(sum(H[w][i] for w, label in enumerate(LABELS) if letter in label) == 0 for i in range(len(edges)))
        assert sp.Matrix(H).T * sp.Matrix(H) == 7*matrix
        for vertices, allowed in relations:
            accepted = set(allowed)
            assert all((selected[u], selected[v]) in accepted for u, v in vertices)
        info.update(selected_signature_indices=selected, H=H, exact_placement_check=True)
    return info


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--grams', type=int, nargs='+', required=True)
    p.add_argument('--seconds', type=float, default=5)
    p.add_argument('--no-pairs', action='store_true')
    p.add_argument('--short-norm', type=int, default=4)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    blob = a.bundle.read_bytes()
    bundle = json.loads(gzip.decompress(blob) if a.bundle.suffix == '.gz' else blob)
    edges = [tuple(e) for e in bundle.get('edges', bundle.get('edge_order'))]
    result = dict(scope=__doc__, source_bundle=str(a.bundle), source_sha256=hashlib.sha256(blob).hexdigest(),
                  resources=resources, cases=[], global_conway_exclusion=False, whole_template_excluded=False,
                  uses_prism_budget=False)
    for gi in a.grams:
        def progress(info):
            print(json.dumps(dict(gram_selector=gi, **info)), flush=True)
        case = solve(edges, bundle['grams'][gi], a.seconds, pairs=not a.no_pairs,
                     short_norm=a.short_norm, progress=progress)
        case['gram_selector'] = gi
        result['cases'].append(case)
        atomic_json_write(a.output, result)
        print(json.dumps({k: v for k, v in case.items() if k not in ('H', 'selected_signature_indices')}), flush=True)


if __name__ == '__main__':
    main()
