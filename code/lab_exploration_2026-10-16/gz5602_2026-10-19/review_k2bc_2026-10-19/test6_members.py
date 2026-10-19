import gzip, json, sys, time
from fractions import Fraction
from itertools import combinations, permutations
import numpy as np
ARGS = list(sys.argv)
recs = json.load(gzip.open(ARGS[1]))['open']
theirs = json.load(open(ARGS[2]))
assert theirs['pattern'] == '45,13,26'
theirs = {int(k): v for k, v in theirs['members'].items()}
R = list(combinations(range(7), 2)); RI = {r: i for i, r in enumerate(R)}
def ri(a, b): return RI[(min(a, b), max(a, b))]
perms = np.array(list(permutations(range(7))))            # phi: normal-form line -> template line
idx = {}
for name, (x, y) in {'A': (0, 1), 'B': (0, 2), 'g45': (4, 5), 'g13': (1, 3), 'g26': (2, 6)}.items():
    idx[name] = np.array([ri(p[x], p[y]) for p in perms])
def rank(rows):
    rows = [[Fraction(v) for v in r] for r in rows]; rk = 0; ncol = 21
    for c in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c] / rows[rk][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
t0 = time.time(); mine = {}; wcalls = 0
for ti, r in enumerate(recs):
    t = r['template']
    ng = np.zeros(21, dtype=bool)
    for e in t['nongrid_edges']:
        ng[ri(*e)] = True
    ok = ng[idx['A']] & ng[idx['B']] & ~ng[idx['g45']] & ~ng[idx['g13']] & ~ng[idx['g26']]
    cand = np.nonzero(ok)[0]
    if not len(cand):
        continue
    rel = []
    for q in range(21):
        if not ng[q]:
            v = [0] * 21; v[q] = 1; rel.append(v)
    for a, groups in enumerate(t['nontrivial_component_groups']):
        for P in groups:
            v = [0] * 21
            for j in P:
                v[ri(a, j)] = 1
            rel.append(v)
    rk = rank(rel)
    tested = {}
    for k in cand:
        A, B = int(idx['A'][k]), int(idx['B'][k])
        key = (min(A, B), max(A, B))
        if key not in tested:
            v = [0] * 21; v[A] = 1; v[B] = 1; wcalls += 1
            tested[key] = rank(rel + [v]) == rk
        if tested[key]:
            mine[ti] = perms[k].tolist(); break
print('templates', len(recs), 'my members', len(mine), 'their members', len(theirs), 'rank tests', wcalls, 'secs %.0f' % (time.time() - t0))
print('their - mine (false positives?)', sorted(set(theirs) - set(mine))[:20], len(set(theirs) - set(mine)))
print('mine - their (missed)', sorted(set(mine) - set(theirs))[:20], len(set(mine) - set(theirs)))
# verify their witnesses directly
bad = 0
for ti, (a, b, c, perm) in theirs.items():
    phi = {0: a, 1: b, 2: c, 3: perm[0], 4: perm[1], 5: perm[2], 6: perm[3]}
    ng = {tuple(e) for e in recs[ti]['template']['nongrid_edges']}
    def isng(x, y): return (min(phi[x], phi[y]), max(phi[x], phi[y])) in ng
    if sorted(phi.values()) != list(range(7)) or not isng(0, 1) or not isng(0, 2) or isng(4, 5) or isng(1, 3) or isng(2, 6):
        bad += 1
print('their witnesses failing the grid / bijection test', bad)
