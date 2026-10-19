# Independent enumeration of Q12 attachments (no Codex colour code) vs py_extend.Attachments.
# att[g][j] = corner of grid g whose label is joined to Q12 corner j.
import gzip, json, runpy, sys
from itertools import combinations, permutations, product
W, codex, cover, fam, idxs = sys.argv[1:6]; SHARD = sys.argv[7] if len(sys.argv) > 7 else None
idxs = [int(i) for i in idxs.split(',')] if idxs != 'zero' else None
src = json.loads(gzip.decompress(open(cover, 'rb').read())); core = src['core']
# load py_extend definitions without running a case: fake cover file with a non-COMPLETE status
fake = W + '/../_review_fake.json.gz'
import os, tempfile
tmpd = sys.argv[6]
fake = tmpd + '/fake_noop.json.gz'
open(fake, 'wb').write(gzip.compress(json.dumps({'status': 'NOOP', 'core_index': -1, 'core': core}).encode()))
sys.argv = ['py_extend.py', codex, fam, fake, '0', '0']
mod = runpy.run_path(W + '/py_extend.py', run_name='py_extend_review')
Att = mod['Attachments'](core)
YR = {"K3": ((4, 5), (4, 6), (5, 6)), "P3": ((4, 5), (4, 6)), "2K2": ((3, 4), (5, 6)), "K2": ((4, 5),)}[fam]
NG = len(YR)
CORE = [(s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2)]
Q12 = [(2 + j // 2, 4 + j % 2) for j in range(4)]
YL = [[(2*a + c // 2, 2*b + c % 2) for c in range(4)] for a, b in YR]
T = {(u, v): core['T']['%d-%d' % (u, v)] for u, v in combinations(range(8), 2)}
deg = [[2 - len(set(CORE[v]) & set(Q12[j])) for v in range(8)] for j in range(4)]
def forb(e, j):
    u, v = e; return bool(set(CORE[u]) & set(CORE[v]) & set(Q12[j]))
def pair(m):
    return tuple(v for v in range(8) if m >> v & 1)
def extendable(fixed):
    # fixed: list of (edge, colour) for Y labels.  Colour the remaining copies of T.
    cls = [set() for _ in range(4)]; d = [list(deg[j]) for j in range(4)]
    rem = dict(T)
    for e, j in fixed:
        if e in cls[j] or forb(e, j): return False
        cls[j].add(e); rem[e] -= 1
        for v in e:
            d[j][v] -= 1
            if d[j][v] < 0: return False
        if rem[e] < 0: return False
    copies = [e for e, n in sorted(rem.items()) for _ in range(n)]
    if sum(sum(x) for x in d) != 2 * len(copies): return False
    def bt(i):
        if i == len(copies):
            return all(x == 0 for row in d for x in row)
        e = copies[i]; u, v = e
        for j in range(4):
            if e in cls[j] or forb(e, j) or d[j][u] == 0 or d[j][v] == 0: continue
            if i > 0 and copies[i-1] == e and j < last[i-1]: continue   # symmetry between equal copies
            cls[j].add(e); d[j][u] -= 1; d[j][v] -= 1; last[i] = j
            if bt(i + 1): return True
            cls[j].discard(e); d[j][u] += 1; d[j][v] += 1
        return False
    last = [0] * len(copies)
    return bt(0)
def mine(bd):
    res = set()
    masks = [list(bd[4*g:4*g+4]) for g in range(NG)]
    for cols in product(permutations(range(4)), repeat=NG):     # cols[g][j] = corner coloured j
        ok = True; fixed = []
        for g in range(NG):
            for j in range(4):
                fixed.append((pair(masks[g][cols[g][j]]), j))
        for g, h in combinations(range(NG), 2):
            for j in range(4):
                mg, mh = masks[g][cols[g][j]], masks[h][cols[h][j]]
                if mg == mh: ok = False
                if bin(mg & mh).count('1') + len(set(YL[g][cols[g][j]]) & set(YL[h][cols[h][j]])) > 1: ok = False
        if ok and extendable(fixed):
            res.add(tuple(tuple(c) for c in cols))
    return res
if idxs is None:
    sh = json.loads(gzip.decompress(open(SHARD, 'rb').read()))
    idxs = [c['boundary_index'] for c in sh['cases'] if c['status'].startswith('EXCLUDED') and c['counts'].get('valid_partial', 0) == 0]
bad = 0
for bi in idxs:
    bd = tuple(bytes.fromhex(src['boundaries_hex'][bi]))
    theirs = set(Att.for_boundary(bd)); ours = mine(bd)
    if theirs != ours:
        bad += 1; print('DIFF', bi, len(theirs), len(ours), sorted(theirs ^ ours)[:4])
    else:
        print('same', bi, len(ours))
print('boundaries', len(idxs), 'differences', bad)
