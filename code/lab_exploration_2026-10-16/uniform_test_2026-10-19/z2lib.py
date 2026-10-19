"""Second-order count design of a root template (LAB 19/10/2026): exact integer system and Farkas certificates.
Same model as z2_probe.py (see its docstring and NOTE_TEST_UNIFORME_2026-10-19.md), written as a library:
  build_system(template, corners)  -> integer system  A_eq x = b_eq,  A_ub x <= b_ub,  0 <= x <= u  (u finite, valid);
  find_certificate(system)         -> exact rational multipliers (y_eq free, y_ub >= 0, y_up >= 0) with
                                      c = A_eq^T y_eq + A_ub^T y_ub + y_up >= 0  and  beta = b_eq.y_eq + b_ub.y_ub + u.y_up < 0,
                                      which proves that no x satisfies the system (for x >= 0: 0 <= c.x <= beta < 0);
  check_certificate(system, cert)  -> exact re-check with Python integers and fractions only.
Variables: n[t] (labels of type t = (rectangle, state)), M[pair] (ordered adjacent pairs between two types, symmetric),
and with corners=True x[q, c, t] (corner c of Q_q has state t) and y[q, c, c'] (internal edge between two corners).
Upper bounds: n <= 4; M[t, t'] <= 4 min(z_t(q'), z_t'(q)) (since M[t, t'] = sum over labels w of type t of the
neighbours of w of type t' <= n[t] z_t(q')); x, y <= 1."""
import json
from fractions import Fraction
from itertools import combinations
from math import gcd


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


def build_system(template, rectangles, catalogue, corners=False):
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    types = [(qi, tuple(z)) for qi, item in enumerate(catalogue['row_types']) for z in item['states']]
    T = len(types)
    H = [[base(rectangles[qi], rectangles[f]) - z[f] for f in range(21)] for qi, z in types]
    Z = [list(z) for _, z in types]
    rect_of = [qi for qi, _ in types]
    by_rect = [[t for t in range(T) if rect_of[t] == qi] for qi in range(21)]
    pairs = [(a, b) for a in range(T) for b in range(a, T) if Z[a][rect_of[b]] >= 1 and Z[b][rect_of[a]] >= 1]
    names = ['n:%d' % t for t in range(T)] + ['m:%d:%d' % p for p in pairs]
    upper = [4] * T + [4 * min(Z[a][rect_of[b]], Z[b][rect_of[a]]) for a, b in pairs]
    eq, beq, ub, bub, eqname, ubname = [], [], [], [], [], []
    inc = [[] for _ in range(T)]
    for k, (a, b) in enumerate(pairs):
        inc[a].append((T + k, b))
        if a != b:
            inc[b].append((T + k, a))
    for qi in range(21):
        eq.append({t: 1 for t in by_rect[qi]}); beq.append(4); eqname.append('C0:%d' % qi)
    for t in range(T):
        per = {}
        for var, o in inc[t]:
            per.setdefault(rect_of[o], []).append(var)
        for f in range(21):
            row = {var: 1 for var in per.get(f, [])}
            if Z[t][f]:
                row[t] = row.get(t, 0) - Z[t][f]
            if row:
                eq.append(row); beq.append(0); eqname.append('L1:%d:%d' % (t, f))
    for t in range(T):
        for F in range(21):
            row = {}
            for var, o in inc[t]:
                if H[o][F]:
                    row[var] = row.get(var, 0) + H[o][F]
            if H[t][F]:
                row[t] = row.get(t, 0) + 4 * H[t][F]
            row = {k: v for k, v in row.items() if v}
            if row:
                eq.append(row); beq.append(0); eqname.append('L3:%d:%d' % (t, F))
    for qi, q in enumerate(rectangles):
        if q in nongrid:
            ub.append({t: Z[t][qi] for t in by_rect[qi] if Z[t][qi]}); bub.append(4); ubname.append('E3n:%d' % qi)
    if corners:
        xv, yv = {}, {}
        for qi in range(21):
            for c in range(4):
                for t in by_rect[qi]:
                    xv[qi, c, t] = len(names); names.append('x:%d:%d:%d' % (qi, c, t)); upper.append(1)
        for qi in range(21):
            for c1, c2 in combinations(range(4), 2):
                yv[qi, c1, c2] = len(names); names.append('y:%d:%d:%d' % (qi, c1, c2)); upper.append(1)
        for qi in range(21):
            q = rectangles[qi]
            for c in range(4):
                eq.append({xv[qi, c, t]: 1 for t in by_rect[qi]}); beq.append(1); eqname.append('X1:%d:%d' % (qi, c))
                row = {xv[qi, c, t]: Z[t][qi] for t in by_rect[qi] if Z[t][qi]}
                for c2 in range(4):
                    if c2 != c:
                        row[yv[qi, min(c, c2), max(c, c2)]] = -1
                eq.append(row); beq.append(0); eqname.append('XD:%d:%d' % (qi, c))
            for t in by_rect[qi]:
                row = {xv[qi, c, t]: 1 for c in range(4)}
                row[t] = -1
                eq.append(row); beq.append(0); eqname.append('XN:%d:%d' % (qi, t))
            for c1, c2 in combinations(range(4), 2):
                if q not in nongrid:
                    side = bin(c1 ^ c2).count('1') == 1
                    eq.append({yv[qi, c1, c2]: 1}); beq.append(1 if side else 0); eqname.append('YG:%d:%d:%d' % (qi, c1, c2))
            if q in nongrid:
                ub.append({yv[qi, c1, c2]: 1 for c1, c2 in combinations(range(4), 2)}); bub.append(2); ubname.append('E3y:%d' % qi)
        for l in range(14):
            for F in range(21):
                row = {}
                for qi, (i, j) in enumerate(rectangles):
                    for c in range(4):
                        s, tt = divmod(c, 2)
                        if l in (2 * i + s, 2 * j + tt):
                            for t in by_rect[qi]:
                                if H[t][F]:
                                    row[xv[qi, c, t]] = row.get(xv[qi, c, t], 0) + H[t][F]
                row = {k: v for k, v in row.items() if v}
                if row:
                    eq.append(row); beq.append(0); eqname.append('UH:%d:%d' % (l, F))
    return {'types': types, 'pairs': pairs, 'names': names, 'upper': upper, 'eq': eq, 'beq': beq, 'eqname': eqname,
            'ub': ub, 'bub': bub, 'ubname': ubname, 'corners': corners, 'Z': Z, 'rect_of': rect_of, 'by_rect': by_rect}


def add_triangles(S, rectangles):
    """Third-order layer (lambda = 1 at the root, exact):
    every label w = {l1, l2} has exactly one neighbour sharing l1 and one sharing l2 (its partners on the two lines
    {letter, w, partner}); its 10 other label-neighbours form 5 adjacent pairs (the 5 lines through w made of labels),
    and w, v, v' pairwise share no letter on such a line (so each root line is used at most twice by the 3 labels).
    Aggregated by type t (rectangle q, state z):
      S[t, a, q']  partners of the type-t labels via their letter on line a, lying in q' (q' contains a);
      Y[t, q', q''] incidences (type-t label, label-line through it) whose two other labels lie in q', q'' (q' <= q'').
      (S1) sum_{q' contains a} S[t, a, q'] = n[t]                      for each line a of q;
      (Y1) sum_{q' <= q''} Y[t, q', q''] = 5 n[t];
      (Y2) n[t] z_t(q') = sum_a S[t, a, q'] + 2 Y[t, q', q'] + sum_{q'' != q'} Y[t, q', q''];
      (S3) for q != q' with the common line a: sum_{t in q} S[t, a, q'] = sum_{t' in q'} S[t', a, q];
      (Y3) for distinct q1, q2, q3: A(q1|q2,q3) = A(q2|q1,q3) = A(q3|q1,q2), and A(q1|q1,q3) = 2 A(q3|q1,q1),
           where A(q|q',q'') = sum_{t in q} Y[t, q', q''] (the same label-lines counted from each vertex);
      support: Y[t, q', q''] only when no root line occurs three times in q, q', q''."""
    Z, rect_of, by_rect = S['Z'], S['rect_of'], S['by_rect']
    names, upper, eq, beq, eqname = S['names'], S['upper'], S['eq'], S['beq'], S['eqname']
    T = len(S['types'])
    sv, yv = {}, {}
    for t in range(T):
        q = rectangles[rect_of[t]]
        for a in q:
            for qp in range(21):
                if a in rectangles[qp] and Z[t][qp] >= 1:
                    sv[t, a, qp] = len(names); names.append('s:%d:%d:%d' % (t, a, qp)); upper.append(4)
        for qp in range(21):
            for qpp in range(qp, 21):
                lines = list(q) + list(rectangles[qp]) + list(rectangles[qpp])
                if any(lines.count(x) > 2 for x in set(lines)):
                    continue
                need_p = 2 if qp == qpp else 1
                if Z[t][qp] < need_p or Z[t][qpp] < 1:
                    continue
                yv[t, qp, qpp] = len(names); names.append('yy:%d:%d:%d' % (t, qp, qpp)); upper.append(20)
    for t in range(T):
        q = rectangles[rect_of[t]]
        for a in q:
            row = {sv[k]: 1 for k in sv if k[0] == t and k[1] == a}
            row[t] = row.get(t, 0) - 1
            eq.append(row); beq.append(0); eqname.append('S1:%d:%d' % (t, a))
        row = {v: 1 for k, v in yv.items() if k[0] == t}
        row[t] = row.get(t, 0) - 5
        eq.append(row); beq.append(0); eqname.append('Y1:%d' % t)
        for qp in range(21):
            row = {}
            for a in q:
                if (t, a, qp) in sv:
                    row[sv[t, a, qp]] = 1
            for (tt, x1, x2), v in yv.items():
                if tt != t:
                    continue
                if x1 == qp and x2 == qp:
                    row[v] = row.get(v, 0) + 2
                elif x1 == qp or x2 == qp:
                    row[v] = row.get(v, 0) + 1
            if Z[t][qp]:
                row[t] = row.get(t, 0) - Z[t][qp]
            if row:
                eq.append(row); beq.append(0); eqname.append('Y2:%d:%d' % (t, qp))
    for q1 in range(21):
        for q2 in range(q1 + 1, 21):
            common = set(rectangles[q1]) & set(rectangles[q2])
            if len(common) != 1:
                continue
            a = next(iter(common))
            row = {}
            for t in by_rect[q1]:
                if (t, a, q2) in sv:
                    row[sv[t, a, q2]] = row.get(sv[t, a, q2], 0) + 1
            for t in by_rect[q2]:
                if (t, a, q1) in sv:
                    row[sv[t, a, q1]] = row.get(sv[t, a, q1], 0) - 1
            if row:
                eq.append(row); beq.append(0); eqname.append('S3:%d:%d' % (q1, q2))

    def A(q, qp, qpp):
        x1, x2 = min(qp, qpp), max(qp, qpp)
        return {yv[t, x1, x2]: 1 for t in by_rect[q] if (t, x1, x2) in yv}

    def add_diff(r1, r2, f1, f2, name):
        row = {}
        for k, v in r1.items():
            row[k] = row.get(k, 0) + f1 * v
        for k, v in r2.items():
            row[k] = row.get(k, 0) - f2 * v
        row = {k: v for k, v in row.items() if v}
        if row:
            eq.append(row); beq.append(0); eqname.append(name)
    for q1 in range(21):
        for q2 in range(q1 + 1, 21):
            for q3 in range(q2 + 1, 21):
                a1, a2, a3 = A(q1, q2, q3), A(q2, q1, q3), A(q3, q1, q2)
                add_diff(a1, a2, 1, 1, 'Y3:%d:%d:%d:a' % (q1, q2, q3))
                add_diff(a1, a3, 1, 1, 'Y3:%d:%d:%d:b' % (q1, q2, q3))
    for q1 in range(21):
        for q3 in range(21):
            if q3 != q1:
                add_diff(A(q1, q1, q3), A(q3, q1, q1), 1, 2, 'Y3d:%d:%d' % (q1, q3))
    S['triangles'] = True
    return S


def find_certificate(S, scale=10 ** 7):
    """Elastic primal first (always feasible, robust): minimise the total violation of the equalities; if it is > 0,
    the KKT multipliers give a Farkas certificate (y_eq = -lambda_eq, y_ub = -lambda_ub, y_up = -lambda_upper; the
    lower-bound multipliers are the coefficient vector c >= 0).  Falls back to the explicit dual LP otherwise."""
    cert = _elastic_certificate(S, scale)
    if cert['status'] == 'CERTIFICATE':
        return cert
    alt = _dual_certificate(S, scale)
    return alt if alt['status'] == 'CERTIFICATE' else cert


def _rational_cert(S, yeq_f, yub_f, yup_f, scale):
    nv = len(S['names'])
    yeq = [Fraction(round(x * scale), scale) for x in yeq_f]
    yub = [max(Fraction(0), Fraction(round(x * scale), scale)) for x in yub_f]
    cvec = [Fraction(0)] * nv
    for i, row in enumerate(S['eq']):
        if yeq[i]:
            for j, a in row.items():
                cvec[j] += yeq[i] * a
    for k, row in enumerate(S['ub']):
        if yub[k]:
            for j, a in row.items():
                cvec[j] += yub[k] * a
    yup = [max(Fraction(0), Fraction(round(x * scale), scale)) for x in yup_f]
    for j in range(nv):
        if cvec[j] + yup[j] < 0:
            yup[j] = -cvec[j]
    cert = {'y_eq': {S['eqname'][i]: str(y) for i, y in enumerate(yeq) if y},
            'y_ub': {S['ubname'][k]: str(y) for k, y in enumerate(yub) if y},
            'y_up': {S['names'][j]: str(y) for j, y in enumerate(yup) if y}}
    chk = check_certificate(S, cert)
    cert['check'] = chk
    cert['status'] = 'CERTIFICATE' if chk['valid'] else 'ROUNDING_FAILED'
    return cert


def _elastic_certificate(S, scale):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    nv, me, mu = len(S['names']), len(S['eq']), len(S['ub'])
    r, c, v = [], [], []
    for i, row in enumerate(S['eq']):
        for j, a in row.items():
            r.append(i); c.append(j); v.append(a)
        r.append(i); c.append(nv + i); v.append(1.0)          # s+
        r.append(i); c.append(nv + me + i); v.append(-1.0)    # s-
    Aeq = coo_matrix((v, (r, c)), shape=(me, nv + 2 * me)).tocsr()
    r, c, v = [], [], []
    for k, row in enumerate(S['ub']):
        for j, a in row.items():
            r.append(k); c.append(j); v.append(a)
    Aub = coo_matrix((v, (r, c)), shape=(mu, nv + 2 * me)).tocsr() if mu else None
    obj = np.concatenate([np.zeros(nv), np.ones(2 * me)])
    bounds = [(0, u) for u in S['upper']] + [(0, None)] * (2 * me)
    res = linprog(obj, A_ub=Aub, b_ub=np.array(S['bub'], float) if mu else None, A_eq=Aeq,
                  b_eq=np.array(S['beq'], float), bounds=bounds, method='highs')
    if res.status != 0:
        return {'status': 'NO_CERTIFICATE', 'message': 'elastic LP: ' + res.message}
    if res.fun < 1e-7:
        return {'status': 'FEASIBLE_DESIGN', 'violation': float(res.fun)}
    yeq = -np.asarray(res.eqlin.marginals)
    yub = -np.asarray(res.ineqlin.marginals) if mu else np.zeros(0)
    yup = -np.asarray(res.upper.marginals)[:nv]
    return _rational_cert(S, yeq, yub, yup, scale)


def _dual_certificate(S, scale):
    """Explicit Farkas dual (kept as a fallback)."""
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    nv, me, mu = len(S['names']), len(S['eq']), len(S['ub'])
    # dual variables: y_eq (me, free), y_ub (mu, >= 0), y_up (nv, >= 0); constraint: A^T y + y_up >= 0
    r, c, v = [], [], []
    for i, row in enumerate(S['eq']):
        for j, a in row.items():
            r.append(j); c.append(i); v.append(-a)
    for k, row in enumerate(S['ub']):
        for j, a in row.items():
            r.append(j); c.append(me + k); v.append(-a)
    for j in range(nv):
        r.append(j); c.append(me + mu + j); v.append(-1.0)
    A = coo_matrix((v, (r, c)), shape=(nv, me + mu + nv)).tocsr()          # -(A^T y + y_up) <= 0
    obj = np.array(list(S['beq']) + list(S['bub']) + list(S['upper']), dtype=float)
    bounds = [(None, None)] * me + [(0, None)] * (mu + nv)
    res = linprog(obj, A_ub=A, b_ub=np.zeros(nv), A_eq=obj.reshape(1, -1), b_eq=np.array([-1.0]),
                  bounds=bounds, method='highs')
    if res.status != 0:
        return {'status': 'NO_CERTIFICATE', 'message': res.message}
    yv = res.x
    yeq = [Fraction(round(x * scale), scale) for x in yv[:me]]
    yub = [max(Fraction(0), Fraction(round(x * scale), scale)) for x in yv[me:me + mu]]
    cvec = [Fraction(0)] * nv
    for i, row in enumerate(S['eq']):
        if yeq[i]:
            for j, a in row.items():
                cvec[j] += yeq[i] * a
    for k, row in enumerate(S['ub']):
        if yub[k]:
            for j, a in row.items():
                cvec[j] += yub[k] * a
    yup = [max(Fraction(0), Fraction(round(x * scale), scale)) for x in yv[me + mu:]]
    for j in range(nv):
        if cvec[j] + yup[j] < 0:
            yup[j] = -cvec[j]
    cert = {'y_eq': {S['eqname'][i]: str(y) for i, y in enumerate(yeq) if y},
            'y_ub': {S['ubname'][k]: str(y) for k, y in enumerate(yub) if y},
            'y_up': {S['names'][j]: str(y) for j, y in enumerate(yup) if y}}
    chk = check_certificate(S, cert)
    cert['check'] = chk
    cert['status'] = 'CERTIFICATE' if chk['valid'] else 'ROUNDING_FAILED'
    return cert


def check_certificate(S, cert):
    """Exact check, Python integers and fractions only."""
    index_eq = {n: i for i, n in enumerate(S['eqname'])}
    index_ub = {n: k for k, n in enumerate(S['ubname'])}
    index_var = {n: j for j, n in enumerate(S['names'])}
    nv = len(S['names'])
    cvec = [Fraction(0)] * nv
    beta = Fraction(0)
    for name, y in cert['y_eq'].items():
        y = Fraction(y); i = index_eq[name]
        for j, a in S['eq'][i].items():
            cvec[j] += y * a
        beta += y * S['beq'][i]
    for name, y in cert['y_ub'].items():
        y = Fraction(y); k = index_ub[name]
        assert y >= 0
        for j, a in S['ub'][k].items():
            cvec[j] += y * a
        beta += y * S['bub'][k]
    for name, y in cert['y_up'].items():
        y = Fraction(y); j = index_var[name]
        assert y >= 0
        cvec[j] += y
        beta += y * S['upper'][j]
    negative = sum(1 for x in cvec if x < 0)
    return {'valid': negative == 0 and beta < 0, 'negative_coefficients': negative, 'beta': str(beta),
            'multipliers': len(cert['y_eq']) + len(cert['y_ub']) + len(cert['y_up'])}
