r"""Block-type census of the y-pairs of a rigid D_{2m} > D_m^2 envelope (C1 27/09, notes/143 s.4). Tiny, no search.
Usage: python blocktypes_census.py <id>  (reads envelopes/U/<id>.json and data/finishC/ypairs/gpairs_<id>.json)"""
import json, sys
from fractions import Fraction as F
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\Users\RESEARCHER\Desktop\c1_recherche\code')
from y_pairs import setup, root_system
lid = sys.argv[1]
env = json.load(open(r'C:\Users\RESEARCHER\Desktop\c99_structures_lab\involution\envelopes\U\%s.json' % lid))
pairs = json.load(open(r'C:\Users\RESEARCHER\Desktop\c1_recherche\data\finishC\ypairs\gpairs_%s.json' % lid))['pairs']
B, Gi, Bf, R, X3, Snew = setup(env['gens'])
Ssimp, comp, marks, A, P = root_system(R)
Pj = [Ssimp[c].T @ np.linalg.inv(Ssimp[c] @ Ssimp[c].T) @ Ssimp[c] for c in comp]
nc = len(comp)
blocks, rep = {}, {}
for b in Snew:
    nz = tuple(i for i in range(nc) if np.linalg.norm(Pj[i] @ b) > 1e-6)
    blocks[nz] = blocks.get(nz, 0) + 1
    rep.setdefault(nz, b)
print('components', nc, 'block supports', blocks)
def ytype(y, X, Xp, b):
    t = float((Pj[X] @ y) @ (Pj[X] @ b))
    I, H = (X, Xp) if abs(t - round(t)) < 1e-6 else (Xp, X)
    e = round(float(y @ Pj[I] @ y)); nh = round(float(y @ Pj[H] @ y)); f = (nh - 1) // 2
    kind = 'E%d' % e if e else ('F%d' % f if f else 'O')
    if e and f: kind = 'BAD'
    return kind, I, e + 2 * f
combos, sums, mixed = Counter(), Counter(), 0
for pr in pairs:
    y1 = np.array([float(F(x)) for x in pr[0]]); y2 = np.array([float(F(x)) for x in pr[1]])
    per, s1, s2, hasmix = [], 0, 0, False
    for (X, Xp), b in rep.items():
        k1, I1, x1 = ytype(y1, X, Xp, b); k2, I2, x2 = ytype(y2, X, Xp, b)
        s1 += x1; s2 += x2
        rel = '=' if I1 == I2 else 'x'
        a, c = sorted([k1, k2])
        per.append('%s%s%s' % (a, rel, c))
        if (k1[0], k2[0]) in {('E', 'F'), ('F', 'E')}: hasmix = True
    sums[(s1, s2)] += 1
    mixed += hasmix
    combos[' | '.join(sorted(per))] += 1
print('extra sums', dict(sums), 'pairs', len(pairs), 'with a mixed E/F block', mixed)
for k, v in combos.most_common():
    print('%5d  %s' % (v, k))
