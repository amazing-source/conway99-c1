"""Independent verifier of a second-order count-design certificate (LAB 19/10/2026).  Python standard library only:
no solver, no floating point, no numpy/sympy, and none of the code that produced the certificate.
It recomputes from the template alone:
  1. the complete catalogue of row states of every rectangle q: all integer z in Z^21 with 0 <= z_f <= 2 when f meets
     q (f = q included) and 0 <= z_f <= 4 otherwise, satisfying every component equation of the template
     (for each root line i and each part S of its partition, sum_{j in S} z(Q_ij) = sum_{j in S} base(q, Q_ij));
  2. every variable of the design: n(t) for each type t = (q, z), and m{t, t'} for each unordered pair of types
     (t in q, t' in q') with z_t(q') >= 1 and z_t'(q) >= 1; their valid upper bounds n <= 4, m <= 4 min(z_t(q'), z_t'(q));
  3. the coefficient of every variable in the certificate's combination, column by column:
       C0|q        sum_t n(t) = 4
       L1|t|f      sum_{t' in f} M(t, t') - z_t(f) n(t) = 0
       L3|t|F      sum_{t'} M(t, t') h_t'(F) + 4 h_t(F) n(t) = 0,   h_t(F) = base(q, F) - z_t(F)
       E3n|q       sum_t z_t(q) n(t) <= 4   (q non-grid; universal E3)
     with M(t, t') = M(t', t) = m{t, t'};
and accepts iff every coefficient is >= 0, every inequality and upper-bound multiplier is >= 0, every key names an
existing constraint or variable, and the combined constant is < 0.  Then no non-negative x satisfies the system.
usage: python z2_verify.py <catalogue.json.gz> <certificate.json>"""
import gzip
import json
import sys
from fractions import Fraction
from itertools import combinations

CAT, CERT = sys.argv[1], sys.argv[2]
if sys.flags.optimize:
    raise SystemExit('assertions required')
cert_file = json.load(open(CERT))
template = json.loads(gzip.decompress(open(CAT, 'rb').read()))['open'][cert_file['template_index']]['template']
cert = cert_file['certificate_explicit']
RECT = list(combinations(range(7), 2))
NAME = ['%d%d' % q for q in RECT]
nongrid = {tuple(e) for e in template['nongrid_edges']}


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


# component equations: list of (support rectangles indices, rhs function of q)
parts = []
for i, groups in enumerate(template['nontrivial_component_groups']):
    used = {j for P in groups for j in P}
    for P in [list(P) for P in groups] + [[j] for j in range(7) if j != i and j not in used]:
        parts.append([RECT.index(tuple(sorted((i, j)))) for j in P])
coord_parts = [[pi for pi, sup in enumerate(parts) if f in sup] for f in range(21)]
assert all(len(c) == 2 for c in coord_parts)


def states_of(qi):
    q = RECT[qi]
    hi = [2 if set(q) & set(f) else 4 for f in RECT]
    rhs = [sum(base(q, RECT[f]) for f in sup) for sup in parts]
    order = sorted(range(21), key=lambda f: coord_parts[f])           # close the equations of a line early
    remaining = [len(sup) for sup in parts]
    partial = [0] * len(parts)
    maxleft = [sum(hi[f] for f in sup) for sup in parts]
    z = [0] * 21
    out = []

    def rec(k):
        if k == 21:
            out.append(tuple(z)); return
        f = order[k]
        for v in range(hi[f] + 1):
            ok = True
            for pi in coord_parts[f]:
                p = partial[pi] + v
                left = maxleft[pi] - hi[f]
                if p > rhs[pi] or p + left < rhs[pi] or (remaining[pi] == 1 and p != rhs[pi]):
                    ok = False; break
            if not ok:
                continue
            z[f] = v
            for pi in coord_parts[f]:
                partial[pi] += v; maxleft[pi] -= hi[f]; remaining[pi] -= 1
            rec(k + 1)
            for pi in coord_parts[f]:
                partial[pi] -= v; maxleft[pi] += hi[f]; remaining[pi] += 1
        z[f] = 0
    rec(0)
    return out


types = []
for qi in range(21):
    for z in states_of(qi):
        types.append((qi, z))
key_of = ['%s:%s' % (NAME[qi], ''.join(map(str, z))) for qi, z in types]
index = {k: t for t, k in enumerate(key_of)}
H = [[base(RECT[qi], RECT[F]) - z[F] for F in range(21)] for qi, z in types]
rect_of = [qi for qi, _ in types]
Fr = Fraction
y = {}
for part in ('y_eq', 'y_ub', 'y_up'):
    for k, v in cert[part].items():
        y[(part, k)] = Fr(v)
# key validation
for (part, k), v in y.items():
    kind = k.split('|')[0]
    if part == 'y_eq':
        assert kind in ('C0', 'L1', 'L3'), k
    elif part == 'y_ub':
        assert kind == 'E3n' and v >= 0, k
        assert tuple(int(c) for c in k.split('|')[1]) in nongrid, k
    else:
        assert kind in ('n', 'm') and v >= 0, k
    fields = k.split('|')
    if kind in ('L1', 'L3', 'n', 'm'):
        for fld in fields[1:]:
            if ':' in fld:
                assert fld in index, ('unknown type in certificate', k)
    if kind == 'm':
        a, b = index[fields[1]], index[fields[2]]
        assert types[a][1][rect_of[b]] >= 1 and types[b][1][rect_of[a]] >= 1, k


def g(part, k):
    return y.get((part, k), Fr(0))


L1 = {}
L3 = {}
for (part, k), v in y.items():
    f = k.split('|')
    if f[0] == 'L1':
        L1[(index[f[1]], RECT.index(tuple(int(c) for c in f[2])))] = v
    elif f[0] == 'L3':
        L3[(index[f[1]], RECT.index(tuple(int(c) for c in f[2])))] = v
L3_row = [[L3.get((t, F), Fr(0)) for F in range(21)] for t in range(len(types))]
negative = 0
checked = 0
beta = Fr(0)
for qi in range(21):
    beta += 4 * g('y_eq', 'C0|' + NAME[qi])
    if RECT[qi] in nongrid:
        beta += 4 * g('y_ub', 'E3n|' + NAME[qi])
for t, (qi, z) in enumerate(types):                                    # columns n(t)
    c = g('y_eq', 'C0|' + NAME[qi])
    c -= sum(L1.get((t, f), 0) * z[f] for f in range(21))
    c += 4 * sum(L3_row[t][F] * H[t][F] for F in range(21))
    if RECT[qi] in nongrid:
        c += g('y_ub', 'E3n|' + NAME[qi]) * z[qi]
    up = g('y_up', 'n|' + key_of[t])
    c += up
    beta += up * 4
    checked += 1
    if c < 0:
        negative += 1
T = len(types)
for a in range(T):                                                     # columns m{a, b}
    qa = rect_of[a]
    for b in range(a, T):
        qb = rect_of[b]
        if types[a][1][qb] < 1 or types[b][1][qa] < 1:
            continue
        ka, kb = key_of[a], key_of[b]
        c = L1.get((a, qb), Fr(0)) + sum(L3_row[a][F] * H[b][F] for F in range(21))
        if a != b:
            c += L1.get((b, qa), Fr(0)) + sum(L3_row[b][F] * H[a][F] for F in range(21))
        up = g('y_up', 'm|%s|%s' % (ka, kb)) + (g('y_up', 'm|%s|%s' % (kb, ka)) if a != b else 0)
        c += up
        beta += up * 4 * min(types[a][1][qb], types[b][1][qa])
        checked += 1
        if c < 0:
            negative += 1
res = {'template_index': cert_file['template_index'], 'types': T, 'variables_checked': checked,
       'negative_coefficients': negative, 'beta': str(beta), 'valid': negative == 0 and beta < 0,
       'state_counts': [sum(1 for qi, _ in types if qi == q) for q in range(21)],
       'certifier_state_counts': cert_file.get('state_counts')}
res['catalogue_agrees'] = res['state_counts'] == res['certifier_state_counts']
print(json.dumps(res))
