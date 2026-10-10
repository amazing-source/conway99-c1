"""Exploration: couple B-to-D cell margins and Z-to-D moments, before edges.

This is a linear relaxation; a feasible point is not an SRG completion.
"""
from collections import Counter
from itertools import combinations
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from norm16_schur_data import ROOT, source_data


def instance(ci, oi, fid):
    cores, cases, forests = source_data()
    core = np.array(cores[ci]['representatives'][0], dtype=np.int64)
    attachment = cases[ci]['orbits'][oi]['representative']
    a = np.zeros((24, 24), dtype=np.int64)
    a[:8, 8:16], a[8:16, :8] = core, core.T
    for d, r in enumerate(attachment):
        for p in r[:2]+[8+q for q in r[2:]]:
            a[p, 16+d] = a[16+d, p] = 1
    common = a @ a
    c = common[16:, 16:].copy()
    np.fill_diagonal(c, 0)
    rowmasks = [sum(1 << j for j, v in enumerate(row) if v) for row in a]
    saturated = [((1 << i) | (1 << j)) for i, j in combinations(range(24), 2)
                 if common[i, j] == 2-a[i, j]]
    pairs = list(combinations(range(8), 2))
    rhs, labels, variables, entries = [], [], [], []
    def equation(label, value):
        labels.append(label)
        rhs.append(int(value))
        return len(rhs)-1
    cells = {(p, q): equation(('cell', p, q), 2-core[p, q]-common[p, 8+q])
             for p in range(8) for q in range(8)
             if 2-core[p, q]-common[p, 8+q] > 0}
    margins = {(p, d): equation(('core_D', p, d), 2-a[p, 16+d]-common[p, 16+d])
               for p in range(16) for d in range(8)}
    zrows = [equation(('D_Z', d), 4) for d in range(8)]
    dpairs = {pair: equation(('pair_D', *pair), 2-c[pair]) for pair in pairs}
    f = next(f for f in forests if f['id'] == fid)
    degree_hist = Counter(map(sum, f['adjacency_Z']))
    zsizes = {r: equation(('Z_size', r), degree_hist.get(r-2, 0)) for r in range(2, 5)}
    def variable(label, rows):
        vi = len(variables)
        variables.append(label)
        entries.extend((r, vi, 1) for r in rows)
    stable_masks = [mask for mask in range(256)
                    if not any(c[d, e] == 2 and (mask >> d & mask >> e & 1) for d, e in pairs)]
    for (p, q), eq in cells.items():
        for dm in stable_masks:
            value = (1 << p) | (1 << (8+q)) | (dm << 16)
            if any((value & row).bit_count() > 2-((value >> i) & 1) for i, row in enumerate(rowmasks)):
                continue
            if any(value & pair == pair for pair in saturated):
                continue
            ds = [d for d in range(8) if dm >> d & 1]
            rows = [eq]+[margins[v, d] for d in ds for v in (p, 8+q)]
            rows += [dpairs[pair] for pair in combinations(ds, 2)]
            variable(('B', p, q, dm), rows)
    for dm in stable_masks:
        r = dm.bit_count()
        if r not in zsizes or not degree_hist.get(r-2):
            continue
        ds = [d for d in range(8) if dm >> d & 1]
        variable(('Z', dm), [zsizes[r]]+[zrows[d] for d in ds]+[dpairs[pair] for pair in combinations(ds, 2)])
    rows, columns, values = zip(*entries)
    matrix = coo_matrix((values, (rows, columns)), shape=(len(rhs), len(variables))).tocsr()
    return matrix, np.array(rhs), variables, labels


if __name__ == '__main__':
    results = []
    for ci, oi in [(0, 226), (0, 241), (0, 242), (4, 1), (4, 2)]:
        for fid in (3, 6, 7):
            m, rhs, variables, labels = instance(ci, oi, fid)
            answer = linprog(np.zeros(len(variables)), A_eq=m, b_eq=rhs, bounds=(0, None), method='highs')
            item = {'case': ci, 'orbit': oi, 'forest': fid, 'variables': len(variables), 'equations': len(rhs), 'status': int(answer.status), 'message': answer.message}
            if answer.success:
                item['max_integrality_distance'] = float(np.max(abs(answer.x-np.rint(answer.x))))
                item['max_equality_residual'] = float(np.max(abs(m @ answer.x-rhs)))
            results.append(item)
            print(json.dumps(item), flush=True)
    (ROOT/'data/codex_norm16_even_margins_probe.json').write_text(json.dumps({'scope': __doc__, 'results': results}, indent=2)+'\n')
