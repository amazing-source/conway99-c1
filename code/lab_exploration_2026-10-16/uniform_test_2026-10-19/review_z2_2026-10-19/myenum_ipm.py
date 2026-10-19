"""Independent state enumeration + primal LP for the z2 design (reviewer re-implementation)."""
import gzip, json, sys, time
from itertools import combinations, product
import numpy as np
METHOD = 'highs-ipm'
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

RECT = list(combinations(range(7), 2))
RI = {q: i for i, q in enumerate(RECT)}

def base(q, f):
    s = len(set(q) & set(f))
    return {2: 2, 1: 0, 0: 1}[s]

def parts_of(template):
    parts = []
    for a in range(7):
        groups = [list(P) for P in template['nontrivial_component_groups'][a]]
        used = set(j for P in groups for j in P)
        for j in range(7):
            if j != a and j not in used:
                groups.append([j])
        for P in groups:
            parts.append([RI[tuple(sorted((a, j)))] for j in P])
    return parts

def states(template, qi):
    """per-line join: for each line a, enumerate the 6-vector on the star of a; then join (different from DFS-by-coordinate)."""
    q = RECT[qi]
    hi = [2 if set(q) & set(f) else 4 for f in RECT]
    parts = parts_of(template)
    # brute force by line: line a's star coordinates
    star = {a: [RI[tuple(sorted((a, j)))] for j in range(7) if j != a] for a in range(7)}
    line_parts = {a: [P for P in parts if all(a in RECT[f] for f in P)] for a in range(7)}
    # enumerate assignments line by line with full consistency on shared coordinates
    sols = []
    def rec(a, z):
        if a == 7:
            sols.append(tuple(z[f] for f in range(21))); return
        coords = [f for f in star[a] if f not in z]
        for vals in product(*[range(hi[f] + 1) for f in coords]):
            zz = dict(z); zz.update(zip(coords, vals))
            if all(sum(zz[f] for f in P) == sum(base(q, RECT[f]) for f in P) for P in line_parts[a]):
                rec(a + 1, zz)
    rec(0, {})
    return sols

def build_and_solve(template, use_E3=True, use_upper=True, verbose=True):
    t0 = time.process_time()
    types = [(qi, z) for qi in range(21) for z in states(template, qi)]
    T = len(types)
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    rq = [qi for qi, _ in types]
    Z = [z for _, z in types]
    H = [[base(RECT[qi], RECT[F]) - z[F] for F in range(21)] for qi, z in types]
    pairs = [(a, b) for a in range(T) for b in range(a, T) if Z[a][rq[b]] >= 1 and Z[b][rq[a]] >= 1]
    nv = T + len(pairs)
    rows_eq = []  # list of dict col->coef, rhs
    # C0
    for qi in range(21):
        rows_eq.append(({t: 1 for t in range(T) if rq[t] == qi}, 4))
    # adjacency of types via pairs: for each t, list of (col, other)
    nb = [[] for _ in range(T)]
    for k, (a, b) in enumerate(pairs):
        nb[a].append((T + k, b))
        if b != a:
            nb[b].append((T + k, a))
    for t in range(T):
        for f in range(21):
            row = {}
            for col, o in nb[t]:
                if rq[o] == f:
                    row[col] = row.get(col, 0) + 1
            row[t] = row.get(t, 0) - Z[t][f]
            row = {k: v for k, v in row.items() if v}
            if row:
                rows_eq.append((row, 0))
        for F in range(21):
            row = {}
            for col, o in nb[t]:
                row[col] = row.get(col, 0) + H[o][F]
            row[t] = row.get(t, 0) + 4 * H[t][F]
            row = {k: v for k, v in row.items() if v}
            if row:
                rows_eq.append((row, 0))
    rows_ub = []
    if use_E3:
        for qi in range(21):
            if RECT[qi] in nongrid:
                rows_ub.append(({t: Z[t][qi] for t in range(T) if rq[t] == qi and Z[t][qi]}, 4))
    def mat(rows):
        r, c, v = [], [], []
        for i, (row, _) in enumerate(rows):
            for j, a in row.items():
                r.append(i); c.append(j); v.append(a)
        return coo_matrix((v, (r, c)), shape=(len(rows), nv)).tocsr(), np.array([b for _, b in rows], float)
    Aeq, beq = mat(rows_eq)
    if rows_ub:
        Aub, bub = mat(rows_ub)
    else:
        Aub, bub = None, None
    if use_upper:
        ub = [4] * T + [4 * min(Z[a][rq[b]], Z[b][rq[a]]) for a, b in pairs]
    else:
        ub = [None] * nv
    res = linprog(np.zeros(nv), A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=list(zip([0] * nv, ub)), method=METHOD, options={'time_limit': 240.0})
    return {'types': T, 'pairs': len(pairs), 'eq': len(rows_eq), 'ub': len(rows_ub), 'status': res.status,
            'message': res.message[:90], 'cpu': round(time.process_time() - t0, 2),
            'state_sets': {qi: sorted(z for q2, z in types if q2 == qi) for qi in range(21)}}

if __name__ == '__main__':
    CAT = sys.argv[1]
    idxs = [int(x) for x in sys.argv[2].split(',')]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'full'
    d = json.loads(gzip.decompress(open(CAT, 'rb').read()))
    for g in idxs:
        T = d['open'][g]['template']
        r = build_and_solve(T, use_E3=(mode != 'noE3'), use_upper=(mode != 'noupper'))
        ss = r.pop('state_sets')
        r['state_counts'] = [len(ss[qi]) for qi in range(21)]
        print(g, mode, json.dumps(r), flush=True)
        json.dump({str(k): v for k, v in ss.items()}, open('states_%d.json' % g, 'w'))
