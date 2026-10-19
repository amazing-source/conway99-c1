"""Second-order count design of a root template (LAB 19/10/2026), LP feasibility probe.
Built on Codex's exact row-state catalogue (root_component_z_distribution.row_catalogue): a label w of the rectangle q
has the state z = (|N(w) cap Q_f|)_f, an integer solution of the component equations C z = b_q with 0 <= z_f <= 2 when
f meets q (f = q included) and <= 4 otherwise.  Its row is h(F) = base(q, F) - z(F).
Unknowns (all exact counts of a hypothetical Conway graph, relaxed to real numbers here):
  n[t]      number of labels of type t = (q, state);
  M[t, t']  number of ORDERED adjacent pairs (w, v) with w of type t, v of type t' (M symmetric).
Exact identities (consequences of lambda = 1, mu = 2 and the letter quotas):
  (C0) sum over the states of q of n = 4;
  (L1) for every type t and rectangle f: sum over the types t' of f of M[t, t'] = n[t] z_t(f);
  (L3) for every type t and rectangle F: sum_{t'} M[t, t'] h_t'(F) = -4 n[t] h_t(F)   (B H_F = -4 H_F, summed over the
       labels of type t; checked by hand 19/10: H_F extended by 0 is a -4 eigenvector);
  (E3) for every non-grid q: sum over the states of q of n z(q) = 2 e_q <= 4   (Codex's universal E3).
(L1) summed over the types of q, with (L3), gives Codex's moment identities Z^t Z + K = D and K = K^t: this design is at
least as strong as his first-order design, before integrality.  INFEASIBLE here = no real solution; an exact Farkas
certificate (not produced by this probe) would turn it into a solver-free exclusion.
usage: python z2_probe.py <codex code dir> <catalogue.json.gz> <index> [--all-grid-control] [--max-free=7] [--corners]"""
import gzip
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

CODEX, CAT, IDX = sys.argv[1], sys.argv[2], int(sys.argv[3])
MAXFREE = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--max-free=')), 7))
sys.path.insert(0, CODEX)
from root_component_z_distribution import RECTANGLES, row_catalogue      # noqa: E402

if '--all-grid-control' in sys.argv:
    template = {'nongrid_edges': [], 'nontrivial_component_groups': [[] for _ in range(7)]}
else:
    d = json.loads(gzip.decompress(Path(CAT).read_bytes()))
    template = d['open'][IDX]['template']
t0 = time.process_time()
cat = row_catalogue(template, max_free=MAXFREE)
assert cat['status'] == 'ROW_CATALOGUE_COMPLETE', cat['status']
nongrid = {tuple(e) for e in template['nongrid_edges']}


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


types = []                                   # (rectangle index, z tuple)
for qi, item in enumerate(cat['row_types']):
    for z in item['states']:
        types.append((qi, tuple(z)))
T = len(types)
H = np.array([[base(RECTANGLES[qi], RECTANGLES[f]) - z[f] for f in range(21)] for qi, z in types], dtype=float)
Z = np.array([z for _, z in types], dtype=float)
rect_of = np.array([qi for qi, _ in types])
by_rect = [[t for t in range(T) if rect_of[t] == qi] for qi in range(21)]
# unordered type pairs that can carry an edge: t in q, t' in q' with z_t(q') >= 1 and z_t'(q) >= 1
pairs = []
for a in range(T):
    qa = rect_of[a]
    for b in range(a, T):
        qb = rect_of[b]
        if Z[a, qb] >= 1 and Z[b, qa] >= 1:
            pairs.append((a, b))
P = len(pairs)
# variable layout: n[0..T-1], m[0..P-1]  (m = M[a,b] = M[b,a]; for a == b, m = M[a,a])
nv = T + P
rows, cols, vals, rhs = [], [], [], []
r = 0


def add_eq(entries, b):
    global r
    for c, v in entries:
        rows.append(r); cols.append(c); vals.append(v)
    rhs.append(b); r += 1


inc = [[] for _ in range(T)]               # for each type: list of (pair var, other type)
for k, (a, b) in enumerate(pairs):
    inc[a].append((T + k, b))
    if a != b:
        inc[b].append((T + k, a))
for qi in range(21):                                                        # (C0)
    add_eq([(t, 1.0) for t in by_rect[qi]], 4.0)
for t in range(T):                                                          # (L1)
    per_rect = {}
    for var, o in inc[t]:
        per_rect.setdefault(rect_of[o], []).append(var)
    for f in range(21):
        ent = [(var, 1.0) for var in per_rect.get(f, [])]
        ent.append((t, -Z[t, f]))
        add_eq(ent, 0.0)
for t in range(T):                                                          # (L3)
    for F in range(21):
        ent = {}
        for var, o in inc[t]:
            if H[o, F] != 0:
                ent[var] = ent.get(var, 0.0) + H[o, F]
        if H[t, F] != 0:
            ent[t] = ent.get(t, 0.0) + 4.0 * H[t, F]
        if ent:
            add_eq(list(ent.items()), 0.0)
CORNERS = '--corners' in sys.argv
if CORNERS:
    # Corner refinement (first order, exact): the four corners of Q_q = (2i+s, 2j+t) are four distinct labels.
    #   x[q, c, t] >= 0, sum_t x[q, c, t] = 1, sum_c x[q, c, t] = n[t]  (t a state of q);
    #   internal corner graph y[q, {c, c'}] in [0, 1]: corner c's internal degree = sum_t x[q, c, t] z_t(q);
    #   grids: the four sides (corners sharing a letter) are edges, the diagonals are not; non-grids: e_q <= 2 (E3);
    #   letter eigen-equation: for every letter l and rectangle F, sum over labels containing l of h(F) = 0 (U H = 0).
    xvar = {}
    for qi in range(21):
        for c in range(4):
            for t in by_rect[qi]:
                xvar[qi, c, t] = nv; nv += 1
    yvar = {}
    for qi in range(21):
        for c1, c2 in combinations(range(4), 2):
            yvar[qi, c1, c2] = nv; nv += 1
    for qi in range(21):
        q = RECTANGLES[qi]
        for c in range(4):
            add_eq([(xvar[qi, c, t], 1.0) for t in by_rect[qi]], 1.0)
            deg = [(xvar[qi, c, t], Z[t, qi]) for t in by_rect[qi]]
            deg += [(yvar[qi, min(c, c2), max(c, c2)], -1.0) for c2 in range(4) if c2 != c]
            add_eq(deg, 0.0)
        for t in by_rect[qi]:
            add_eq([(xvar[qi, c, t], 1.0) for c in range(4)] + [(t, -1.0)], 0.0)
        for c1, c2 in combinations(range(4), 2):
            side = bin(c1 ^ c2).count('1') == 1            # corners 2s+t: a side changes exactly one letter
            if q not in nongrid:
                add_eq([(yvar[qi, c1, c2], 1.0)], 1.0 if side else 0.0)
    for l in range(14):
        for F in range(21):
            ent = {}
            for qi, (i, j) in enumerate(RECTANGLES):
                for c in range(4):
                    s, tt = divmod(c, 2)
                    if l not in (2 * i + s, 2 * j + tt):
                        continue
                    for t in by_rect[qi]:
                        if H[t, F] != 0:
                            ent[xvar[qi, c, t]] = ent.get(xvar[qi, c, t], 0.0) + H[t, F]
            if ent:
                add_eq(list(ent.items()), 0.0)
A_eq = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
b_eq = np.array(rhs)
ub_rows, ub_cols, ub_vals, ub_rhs = [], [], [], []
ur = 0
for qi, q in enumerate(RECTANGLES):                                          # (E3)
    if q in nongrid:
        for t in by_rect[qi]:
            ub_rows.append(ur); ub_cols.append(t); ub_vals.append(Z[t, qi])
        ub_rhs.append(4.0); ur += 1
if CORNERS:
    for qi, q in enumerate(RECTANGLES):                                      # (E3) on the corner graph
        if q in nongrid:
            for c1, c2 in combinations(range(4), 2):
                ub_rows.append(ur); ub_cols.append(yvar[qi, c1, c2]); ub_vals.append(1.0)
            ub_rhs.append(2.0); ur += 1
A_ub = coo_matrix((ub_vals, (ub_rows, ub_cols)), shape=(ur, nv)).tocsr() if ur else None
bounds = [(0, 4)] * T + [(0, None)] * P + ([(0, 1)] * (nv - T - P) if CORNERS else [])
build = time.process_time() - t0
res = linprog(np.zeros(nv), A_ub=A_ub, b_ub=np.array(ub_rhs) if ur else None, A_eq=A_eq, b_eq=b_eq,
              bounds=bounds, method='highs')
out = {'index': IDX, 'corners': CORNERS, 'all_grid_control': '--all-grid-control' in sys.argv, 'free_dimension': cat['free_dimension'],
       'types': T, 'pair_variables': P, 'equalities': r, 'inequalities': ur, 'build_cpu': round(build, 2),
       'lp_status': int(res.status), 'lp_message': res.message, 'cpu_total': round(time.process_time() - t0, 2)}
DUMP = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--dump-solution=')), None)
if DUMP and res.status == 0:
    xs = res.x
    sol = {'types': [[int(qi), list(z)] for qi, z in types], 'n': [round(float(v), 6) for v in xs[:T]],
           'pairs': [[int(a), int(b), round(float(xs[T + k]), 6)] for k, (a, b) in enumerate(pairs) if xs[T + k] > 1e-9]}
    if CORNERS:
        sol['x'] = {'%d,%d,%d' % key: round(float(xs[v]), 6) for key, v in xvar.items() if xs[v] > 1e-9}
        sol['y'] = {'%d,%d,%d' % key: round(float(xs[v]), 6) for key, v in yvar.items()}
    json.dump(sol, open(DUMP, 'w'))
    out['solution_dumped'] = DUMP
print(json.dumps(out))
