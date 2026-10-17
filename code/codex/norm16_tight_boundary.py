"""Explore the exact boundary moments of one tight-cut norm16 support.

Local base-column masks cover every possible simple vertex; the LP assigns
multiplicities and all missing common neighbours of the 35-vertex base.
Feasible does not construct edges among simples. Infeasibility is reported
as exact only when an integral Farkas certificate passes exact checks.
"""
from itertools import combinations
from math import lcm
from fractions import Fraction
import argparse
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from norm16_schur_data import ROOT, source_data
from norm16_independent_catalogue import adjacency


def boundary(seed):
    cores, cases, forests = source_data()
    ci, oi = seed['case'], seed['orbit']
    core = cores[ci]['representatives'][0]
    attachment = cases[ci]['orbits'][oi]['representative']
    forest = next(f for f in forests if f['id'] == seed['forest'])
    a = adjacency(core, attachment, forest, seed['D_Z_row_masks'])
    common = a @ a
    row_masks = [sum(1 << i for i,v in enumerate(row) if v) for row in a]
    saturated = [(1 << i) | (1 << j) for i,j in combinations(range(35),2) if common[i,j] == 2-a[i,j]]
    data = json.loads((ROOT/'data/codex_norm16_shadow_connectivity.json').read_text())
    record = next(r for r in data['records'] if (r['case'],r['orbit']) == (ci,oi))
    u,v = record['tight_subsets']
    ext_masks = []
    for ud in [None]+u:
        for vd in [None]+v:
            ds = [d for d in (ud,vd) if d is not None]
            dm = sum(1 << (16+d) for d in ds)
            for zs in combinations(range(24,35),1+len(ds)):
                ext = dm | sum(1 << z for z in zs)
                if not any(ext & pair == pair for pair in saturated):
                    ext_masks.append(ext)
    labels, rhs, columns, entries = [], [], [], []
    def equation(label,target):
        labels.append(label);rhs.append(int(target));return len(rhs)-1
    vertex_rows = [equation(['degree',i],14-int(sum(a[i]))) for i in range(35)]
    pair_rows = {(i,j):equation(['pair',i,j],2-int(a[i,j])-int(common[i,j])) for i,j in combinations(range(35),2)}
    cells = []
    for p,q in combinations(range(16),2):
        if p>=8 or q<8:
            continue
        copies = 2-int(a[p,q])-int(common[p,q])
        if not copies:
            continue
        cr = equation(['cell',p,q-8],copies)
        ncols = 0
        for ext in ext_masks:
            mask = ext | (1 << p) | (1 << q)
            if any(mask & pair == pair for pair in saturated):
                continue
            if any((mask & row).bit_count() > 2-((mask >> i) & 1) for i,row in enumerate(row_masks)):
                continue
            neighbours = [i for i in range(35) if mask >> i & 1]
            eqs = [cr]+[vertex_rows[i] for i in neighbours]+[pair_rows[i,j] for i,j in combinations(neighbours,2)]
            col = len(columns);columns.append(mask)
            entries.extend((eq,col,1) for eq in eqs)
            ncols += 1
        cells.append({'cell':[p,q-8],'multiplicity':copies,'columns':ncols})
    if entries:
        ri,ci,vs = zip(*entries)
        matrix = coo_matrix((vs,(ri,ci)),shape=(len(rhs),len(columns)),dtype=np.int64).tocsr()
    else:
        matrix = coo_matrix((len(rhs),0),dtype=np.int64).tocsr()
    return matrix,np.array(rhs,dtype=np.int64),labels,columns,cells


def solve(seed):
    matrix,rhs,labels,columns,cells = boundary(seed)
    result = {'seed':seed,'scope':__doc__,'columns':len(columns),'equations':len(rhs),'cells':cells}
    answer = linprog(np.zeros(len(columns)),A_eq=matrix,b_eq=rhs,bounds=(0,None),method='highs')
    result['LP_status'] = int(answer.status)
    result['message'] = answer.message
    if answer.success:
        result['positive_weights'] = [{'mask':mask,'weight':float(x)} for mask,x in zip(columns,answer.x) if x>1e-8]
        result['max_residual'] = float(np.max(abs(matrix @ answer.x-rhs)))
        return result
    if answer.status != 2:
        return result
    dual = linprog(rhs,A_ub=-matrix.T,b_ub=np.zeros(len(columns)),bounds=(-1,1),method='highs')
    if dual.success and dual.fun < -1e-8:
        for max_denominator in (1,2,6,60,1000):
            rational = [Fraction(float(x)).limit_denominator(max_denominator) for x in dual.x]
            denominator = lcm(*(v.denominator for v in rational))
            y = [int(v*denominator) for v in rational]
            # Python integer sums, not fixed-width floating point arithmetic.
            m = matrix.tocsc()
            margins = [sum(int(m.data[k])*y[int(m.indices[k])] for k in range(m.indptr[j],m.indptr[j+1])) for j in range(m.shape[1])]
            dot = sum(int(b)*v for b,v in zip(rhs,y))
            if dot < 0 and min(margins,default=0)>=0:
                result['exact_Farkas'] = {'rhs_dot':dot,'minimum_column_dot':min(margins,default=0),
                    'nonzero_row_coefficients':[{'row':labels[i],'coefficient':v} for i,v in enumerate(y) if v]}
                break
    return result


def verify_saved_certificate(path):
    result = json.loads((ROOT/path).read_text())
    matrix,rhs,labels,columns,_ = boundary(result['seed'])
    index = {tuple(label):i for i,label in enumerate(labels)}
    cert = result.get('exact_sparse_Farkas',result.get('exact_Farkas'))
    if cert is None:
        raise ValueError('No exact certificate is stored in this file.')
    y = [0]*len(rhs)
    for entry in cert['nonzero_row_coefficients']:
        y[index[tuple(entry['row'])]] = int(entry['coefficient'])
    m = matrix.tocsc()
    margins = [sum(int(m.data[k])*y[int(m.indices[k])] for k in range(m.indptr[j],m.indptr[j+1])) for j in range(m.shape[1])]
    dot = sum(int(b)*v for b,v in zip(rhs,y))
    assert dot < 0 and min(margins,default=0)>=0
    assert dot == cert['rhs_dot'] and min(margins,default=0) == cert['minimum_column_dot']
    return {'verified_exactly':True,'columns':len(columns),'rhs_dot':dot,'nonzero_coefficients':sum(v!=0 for v in y)}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source',default='data/codex_norm16_tight_seed_sample.json')
    p.add_argument('--output',default='data/codex_norm16_tight_boundary_first.json')
    p.add_argument('--verify',help='Read a saved certificate and check integer inequalities, without solving an LP.')
    args = p.parse_args()
    if args.verify:
        print(json.dumps(verify_saved_certificate(args.verify)))
        raise SystemExit(0)
    if args.source.endswith('.jsonl'):
        with (ROOT/args.source).open() as stream:seed=json.loads(next(stream))
    else:
        source=json.loads((ROOT/args.source).read_text())
        seed=source['seeds'][0] if 'seeds' in source else source
    result = solve(seed)
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('positive_weights','cells','exact_Farkas','scope')},indent=2))
    if 'exact_Farkas' in result:
        print('EXACT_FARKAS',result['exact_Farkas']['rhs_dot'],len(result['exact_Farkas']['nonzero_row_coefficients']))
