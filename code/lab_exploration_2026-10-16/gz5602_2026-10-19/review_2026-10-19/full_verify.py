# End-to-end independent re-verification of production EXCLUDED boundaries (2K2N stage 1 / 2K2 stage 2).
# Attachments from an independent search (colour classes by backtracking), every sigma, known checks, then
# CryptoMiniSat on the independent profile model.  Any SAT = a production exclusion not reproduced.
import gzip, json, sys, time
from itertools import combinations, permutations, product
sys.argv_saved = list(sys.argv)
cover, fam, shard, pylib, lo, hi = sys.argv[1:7]
sys.argv = ['indep_sat.py', cover, fam, 'none', pylib]
import importlib.util
spec = importlib.util.spec_from_file_location('indep', sys.argv_saved[0].rsplit('full_verify.py', 1)[0] + 'indep_sat.py')
ind = importlib.util.module_from_spec(spec); spec.loader.exec_module(ind)
src = json.loads(gzip.decompress(open(cover, 'rb').read())); core = src['core']
prod = json.loads(gzip.decompress(open(shard, 'rb').read()))
cases = [c for c in prod['cases'] if c['status'].startswith('EXCLUDED')][int(lo):int(hi)]
CORE = [(s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2)]
Q12 = [(2 + j // 2, 4 + j % 2) for j in range(4)]
YL = [[(2*a + c // 2, 2*b + c % 2) for c in range(4)] for a, b in ((3, 4), (5, 6))]
T = {(u, v): core['T']['%d-%d' % (u, v)] for u, v in combinations(range(8), 2)}
deg = [[2 - len(set(CORE[v]) & set(Q12[j])) for v in range(8)] for j in range(4)]
def forb(e, j):
    return bool(set(CORE[e[0]]) & set(CORE[e[1]]) & set(Q12[j]))
def extendable(fixed):
    cls = [set() for _ in range(4)]; d = [list(r) for r in deg]; rem = dict(T)
    for e, j in fixed:
        if e in cls[j] or forb(e, j): return False
        cls[j].add(e); rem[e] -= 1
        if rem[e] < 0: return False
        for v in e:
            d[j][v] -= 1
            if d[j][v] < 0: return False
    copies = [e for e, n in sorted(rem.items()) for _ in range(n)]; last = [0] * len(copies)
    def bt(i):
        if i == len(copies): return all(x == 0 for r in d for x in r)
        e = copies[i]; u, v = e
        for j in range(4):
            if e in cls[j] or forb(e, j) or d[j][u] == 0 or d[j][v] == 0: continue
            if i and copies[i-1] == e and j < last[i-1]: continue
            cls[j].add(e); d[j][u] -= 1; d[j][v] -= 1; last[i] = j
            if bt(i + 1): return True
            cls[j].discard(e); d[j][u] += 1; d[j][v] += 1
        return False
    return bt(0)
def pair(m): return tuple(v for v in range(8) if m >> v & 1)
def attachments(bd):
    if fam == '2K2N': return [None]
    out = []; masks = [list(bd[0:4]), list(bd[4:8])]
    for cols in product(permutations(range(4)), repeat=2):
        ok = True
        for j in range(4):
            mg, mh = masks[0][cols[0][j]], masks[1][cols[1][j]]
            if mg == mh or bin(mg & mh).count('1') + len(set(YL[0][cols[0][j]]) & set(YL[1][cols[1][j]])) > 1: ok = False
        if ok and extendable([(pair(masks[g][cols[g][j]]), j) for g in range(2) for j in range(4)]):
            out.append(cols)
    return out
t0 = time.time(); tally = {'known_violation': 0, 'unsat': 0, 'sat': 0}; disagree = []
for c in cases:
    bd = tuple(bytes.fromhex(src['boundaries_hex'][c['boundary_index']]))
    assert c['boundary_hex'] == src['boundaries_hex'][c['boundary_index']]
    for att in attachments(bd):
        for sg in permutations(range(4)):
            M = ind.model(core, bd, fam, att, sg)
            if M is None: tally['known_violation'] += 1; continue
            r, _ = ind.sat(M)
            if r.startswith('UNSAT'): tally['unsat'] += 1
            else: tally['sat'] += 1; disagree.append((c['boundary_index'], att, sg))
print(json.dumps({'shard': shard.split('/')[-1], 'range': [int(lo), int(hi)], 'boundaries': len(cases), **tally,
                  'NOT_REPRODUCED': disagree[:5], 'seconds': round(time.time() - t0)}), flush=True)
