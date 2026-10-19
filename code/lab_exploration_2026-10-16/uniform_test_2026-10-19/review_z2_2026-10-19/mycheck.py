"""Reviewer's exact row-wise checker of an explicit certificate, on the reviewer's own enumeration (states_<g>.json)."""
import json, gzip, sys
from fractions import Fraction as Fr
from itertools import combinations
RECT = list(combinations(range(7), 2)); NAME = ['%d%d' % q for q in RECT]
def base(q, f):
    return {2: 2, 1: 0, 0: 1}[len(set(q) & set(f))]

def check(template, g, cert):
    st = json.load(open('states_%d.json' % g))
    types = [(qi, tuple(z)) for qi in range(21) for z in st[str(qi)]]
    key = {('%s:%s' % (NAME[qi], ''.join(map(str, z)))): t for t, (qi, z) in enumerate(types)}
    T = len(types); rq = [q for q, _ in types]; Z = [z for _, z in types]
    H = [[base(RECT[q], RECT[F]) - z[F] for F in range(21)] for q, z in types]
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    pairs = {}
    for a in range(T):
        for b in range(a, T):
            if Z[a][rq[b]] >= 1 and Z[b][rq[a]] >= 1:
                pairs[(a, b)] = len(pairs)
    col = {('n', t): t for t in range(T)}
    for (a, b), k in pairs.items():
        col[('m', a, b)] = T + k
    nv = T + len(pairs)
    c = [Fr(0)] * nv; beta = Fr(0)
    def mcol(a, b):
        return col[('m', min(a, b), max(a, b))]
    for k, v in cert['y_eq'].items():
        y = Fr(v); f = k.split('|')
        if f[0] == 'C0':
            qi = NAME.index(f[1])
            for t in range(T):
                if rq[t] == qi: c[t] += y
            beta += 4 * y
        elif f[0] == 'L1':
            t = key[f[1]]; fi = NAME.index(f[2])
            c[t] -= y * Z[t][fi]
            for o in range(T):
                if rq[o] == fi and Z[t][fi] >= 1 and Z[o][rq[t]] >= 1:
                    c[mcol(t, o)] += y
        elif f[0] == 'L3':
            t = key[f[1]]; F = NAME.index(f[2])
            c[t] += y * 4 * H[t][F]
            for o in range(T):
                if Z[t][rq[o]] >= 1 and Z[o][rq[t]] >= 1:
                    c[mcol(t, o)] += y * H[o][F]
        else:
            raise ValueError(k)
    for k, v in cert['y_ub'].items():
        y = Fr(v); f = k.split('|'); assert f[0] == 'E3n' and y >= 0
        qi = NAME.index(f[1]); assert RECT[qi] in nongrid
        for t in range(T):
            if rq[t] == qi: c[t] += y * Z[t][qi]
        beta += 4 * y
    for k, v in cert['y_up'].items():
        y = Fr(v); f = k.split('|'); assert y >= 0
        if f[0] == 'n':
            t = key[f[1]]; c[t] += y; beta += 4 * y
        else:
            a, b = key[f[1]], key[f[2]]; j = mcol(a, b)
            c[j] += y; beta += y * 4 * min(Z[a][rq[b]], Z[b][rq[a]])
    neg = sum(1 for x in c if x < 0)
    return {'valid': neg == 0 and beta < 0, 'neg': neg, 'beta': str(beta), 'nv': nv}

if __name__ == '__main__':
    CAT, CF = sys.argv[1], sys.argv[2]
    cf = json.load(open(CF))
    g = cf['template_index']
    T = json.loads(gzip.decompress(open(CAT, 'rb').read()))['open'][g]['template']
    print(g, json.dumps(check(T, g, cf['certificate_explicit'])))
