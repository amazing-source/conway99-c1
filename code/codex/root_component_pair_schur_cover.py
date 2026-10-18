"""Exact pairwise Schur and short-lattice cuts for a variable Gram cover.

The existing individual/corner tables define every signature state. For each
Gram, forbid only pairs violating a two-by-two principal minor of either
conditional projector, or the proved integral short-vector overlap bounds.
All arithmetic is integral. No Gram or vertex signature is selected as seed.
"""

import argparse
from collections import defaultdict
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_low_budget_transport import digest
from root_component_propagation import LABELS, PAIRS, RECTANGLES
from root_component_signature_moments import gram_matrix
from root_component_short_vectors import short_directions, evaluations, integer_pair_margins
from root_component_upper_signatures import data_for
import sympy as sp


def pair_types():
    """Record actual rectangle pairs and common/mate-common label counts."""
    result = defaultdict(list)
    for u, v in PAIRS:
        q, r = tuple(a // 2 for a in LABELS[u]), tuple(a // 2 for a in LABELS[v])
        if q > r:
            q, r, u, v = r, q, v, u
        common = len(set(LABELS[u]) & set(LABELS[v]))
        mates = sum((a ^ 1) in LABELS[v] for a in LABELS[u])
        result[q, r, common, mates].append((u, v))
    return result


def prepare(template, cover, progress=None):
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    corners = {tuple(t['rectangle']): t for t in cover['corner_signature_tables']}
    assert set(corners) == set(RECTANGLES)
    assert all(t['rows'] for t in corners.values())
    used = {q: defaultdict(set) for q in corners}
    for q, table in corners.items():
        for row in table['rows']:
            used[q][row[0]].update(row[1:5])
    edges = [tuple(e) for e in template['nongrid_edges']]
    positions = {q: i for i, q in enumerate(edges)}
    lift = sp.Matrix([[sp.Rational(*x) for x in row] for row in cover['lift_matrix']])
    kinds = pair_types()
    forbidden = {key: [] for key in kinds}
    checks = lower_reject = upper_reject = integer_reject = 0
    for gi, values in enumerate(cover['gram_anchor_values']):
        matrix = gram_matrix(cover, values)
        anchors = list(matrix.rref()[1])
        small = matrix.extract(anchors, anchors)
        det = int(small.det())
        assert det > 0
        adj = [[int(x) for x in row] for row in (small.inv()*det).tolist()]
        upper = data_for(edges, matrix)
        scale = 225*upper['denominator']
        upper_den = 28*scale
        short = short_directions(matrix)
        norms = tuple(d['norm'] for d in short['directions'])
        root_ids = [i for i, n in enumerate(norms) if n == 2]

        def inner(a, b):
            return sum(a[i]*adj[i][j]*b[j] for i in range(len(anchors)) for j in range(len(anchors)))

        states = {}
        for q in corners:
            states[q] = {}
            for si in sorted(used[q].get(gi, ())):
                reduced = corners[q]['catalog'][si]
                full = lift*sp.Matrix(reduced)
                assert all(x.q == 1 for x in full)
                h = tuple(int(x) for x in full)
                assert tuple(h[a] for a in cover['anchors']) == tuple(reduced)
                small_h = tuple(h[a] for a in anchors)
                v = tuple(7*(15*int(q == e)-3*len(set(q)&set(e))+1)-15*x
                          for e, x in zip(edges, h))
                cv = tuple(sum(a*b for a, b in zip(row, v)) for row in upper['correction'])
                own = h[positions[q]] if q in positions else 0
                ip = 98*scale//3-14*own*scale+sum(x*x for x in h)*scale+sum(a*b for a,b in zip(v,cv))
                nu = 10*upper_den//3-ip
                nl = 20*det-8*inner(small_h, small_h)
                assert nu >= 0 and nl >= 0
                states[q][si] = (h, small_h, v, cv, nl, nu, evaluations(h, short))

        for key in kinds:
            q, r, common, mates = key
            euv15 = 15*int(q == r)-3*len(set(q)&set(r))+1
            base8 = 2-3*common-mates
            for si, a in states[q].items():
                ha, sa, va, _, nla, nua, ea = a
                for sj, b in states[r].items():
                    hb, sb, _, cvb, nlb, nub, eb = b
                    lower_ip = inner(sa, sb)
                    cross = (ha[positions[r]] if r in positions else 0)+(hb[positions[q]] if q in positions else 0)
                    upper_ip = (49*euv15*(scale//15)-7*cross*scale
                                +sum(x*y for x,y in zip(ha,hb))*scale+sum(x*y for x,y in zip(va,cvb)))
                    margins = integer_pair_margins(ea, eb, norms)
                    root_same = any(ea[i] == eb[i] != 0 for i in root_ids)
                    for edge in (0, 1):
                        checks += 1
                        low = ((base8-8*edge)*det-8*lower_ip)**2 > nla*nlb
                        up = ((15*edge-4*common+mates-2)*(upper_den//15)-upper_ip)**2 > nua*nub
                        integer = margins[edge] < 2*common or ((edge or common) and root_same)
                        if low or up or integer:
                            forbidden[key].append([gi, si, sj, edge])
                            lower_reject += low
                            upper_reject += up
                            integer_reject += bool(integer)
        if progress:
            progress(gi, sum(len(rows) for rows in forbidden.values()))
    tables = [{'rectangles': [list(q), list(r)], 'common_labels': c, 'mate_common_labels': m,
               'rows': rows} for (q,r,c,m), rows in forbidden.items() if rows]
    return dict(cover, pair_signature_forbidden_tables=tables,
                pair_signature_scope=__doc__, pair_signature_stats={
                    'gram_count_unchanged': cover['gram_count'], 'pair_types': len(kinds),
                    'nonempty_forbidden_tables': len(tables), 'candidate_rows': checks,
                    'forbidden_rows': sum(len(t['rows']) for t in tables),
                    'lower_schur_rejections': lower_reject, 'upper_schur_rejections': upper_reject,
                    'integer_overlap_rejections': integer_reject})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); resources = limit_research_process(1)
    assert not a.output.exists()
    source = json.loads(a.cover.read_text(encoding='utf-8-sig'))
    record = next(r for r in source['records'] if r['template_index'] == a.index)
    templates = a.directory/'root_component_templates.json'
    template = json.loads(templates.read_text(encoding='utf-8-sig'))['survivors'][a.index]
    start = time.process_time()
    prepared = prepare(template, record, lambda i,n: print(json.dumps({
        'gram_processed': i+1, 'gram_total': record['gram_count'], 'forbidden_rows': n,
        'cpu_seconds': time.process_time()-start}), flush=True))
    result = deepcopy(source)
    result['records'] = [prepared if r['template_index'] == a.index else r for r in result['records']]
    result['pair_table_preparation'] = {'scope': __doc__, 'template_index': a.index,
        'source_cover': str(a.cover), 'source_cover_sha256_lf': digest(a.cover),
        'templates_sha256_lf': digest(templates), 'resources': resources,
        'cpu_seconds': time.process_time()-start, 'newly_excluded_grams': 0}
    atomic_json_write(a.output, result)
    print(json.dumps(prepared['pair_signature_stats']), flush=True)


if __name__ == '__main__':
    main()
