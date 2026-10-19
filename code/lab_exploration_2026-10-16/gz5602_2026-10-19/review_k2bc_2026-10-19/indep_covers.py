"""Independent recomputation (reviewer): (a) labelled 2-regular cores on Q01 u Q02 under lambda/mu/quota/line-0 equality
and e(A), e(B) not in {3,4}; compare with paircores8.json; (b) for every flip-orbit representative listed in
core_reps_flips.json, all boundaries (Q45 grid labels -> core pairs) passing direct C2 / letter checks on the
12-vertex known graph, reduced by MY group (core flip stabiliser x <swap 4,5, flips 4,5,6>); compare orbit by orbit
with the cover files."""
import gzip, json, sys
from itertools import combinations, permutations, product
from pathlib import Path
GZ = Path(sys.argv[1]); SC = Path(sys.argv[2])
core_labels = [(0 + s, 2 + t) for s in (0, 1) for t in (0, 1)] + [(0 + s, 4 + t) for s in (0, 1) for t in (0, 1)]
def quota(lab, l):
    return 2 - (l in lab) - ((l ^ 1) in lab)
def shared(a, b):
    return len(set(a) & set(b))
def check_graph(labs, adj, eq_line0=()):
    n = len(labs)
    nb = [set(j for j in range(n) if adj[i][j]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c = len(nb[i] & nb[j]) + shared(labs[i], labs[j])
            if c > (1 if adj[i][j] else 2):
                return False
        for l in range(14):
            k = sum(1 for j in nb[i] if l in labs[j])
            if k > quota(labs[i], l):
                return False
        if len(nb[i]) > 12:
            return False
    for i in eq_line0:
        for l in (0, 1):
            if sum(1 for j in nb[i] if l in labs[j]) != 1:
                return False
    return True
pairs = list(combinations(range(8), 2))
cores = []
for es in combinations(pairs, 8):
    deg = [0] * 8
    for u, v in es:
        deg[u] += 1; deg[v] += 1
    if deg != [2] * 8:
        continue
    adj = [[0] * 8 for _ in range(8)]
    for u, v in es:
        adj[u][v] = adj[v][u] = 1
    if not check_graph(core_labels, adj, eq_line0=range(8)):
        continue
    eA = sum(1 for u, v in es if u < 4 and v < 4); eB = sum(1 for u, v in es if u >= 4 and v >= 4)
    if eA in (3, 4) or eB in (3, 4):
        continue
    cores.append(frozenset(es))
ref = json.load(open(GZ / 'paircores8.json'))
refset = [frozenset(tuple(e) for e in c['edges']) for c in ref]
print('my cores', len(cores), 'ref cores', len(ref), 'same set', set(cores) == set(refset), 'ref distinct', len(set(refset)))
# deficit T check
bad_T = 0
for c in ref:
    es = set(tuple(e) for e in c['edges']); nb = [set() for _ in range(8)]
    for u, v in es:
        nb[u].add(v); nb[v].add(u)
    for u, v in pairs:
        t = 2 - ((u, v) in es) - shared(core_labels[u], core_labels[v]) - len(nb[u] & nb[v])
        if c['T']['%d-%d' % (u, v)] != t:
            bad_T += 1
print('T mismatches', bad_T)
# flips of lines 0,1,2 acting on core labels
def flip_lab(lab, f):
    return tuple(sorted(x ^ f[x // 2] if x // 2 < 3 else x for x in lab))
cidx = {q: i for i, q in enumerate(core_labels)}
FL = [f for f in product((0, 1), repeat=3)]
def core_img(es, f):
    return frozenset(tuple(sorted((cidx[flip_lab(core_labels[u], f)], cidx[flip_lab(core_labels[v], f)]))) for u, v in es)
orbits = {}
for i, es in enumerate(refset):
    key = min(sorted(core_img(es, f)) for f in FL)
    orbits.setdefault(tuple(key), []).append(i)
reps = json.load(open(SC / 'pybd_k2bc_all' / 'core_reps_flips.json'))['representatives']
print('flip orbits', len(orbits), 'reps listed', len(reps), 'one rep per orbit', sorted(min(o) for o in orbits.values()) == sorted(reps) or all(sum(1 for r in reps if r in o) == 1 for o in orbits.values()))
# boundaries
y_labels = [(8 + s, 10 + t) for s in (0, 1) for t in (0, 1)]       # Q45 corners 2s+t
labs12 = core_labels + y_labels
def y_img(lab, perm45, f):
    # f = flips of (4,5,6); perm45 = swap lines 4 and 5 or not
    out = []
    for x in lab:
        line, bit = x // 2, x % 2
        if line in (4, 5, 6):
            bit ^= f[line - 4]
            if perm45 and line in (4, 5):
                line = 9 - line
        out.append(2 * line + bit)
    return tuple(sorted(out))
yidx = {q: i for i, q in enumerate(y_labels)}
tot_my = tot_cov = 0; allok = True
for ci in reps:
    es = refset[ci]
    stab = [f for f in FL if core_img(es, f) == es]
    valid = set()
    for mt in permutations(range(8)):
        # corner c sees pair (mt[2c], mt[2c+1]); canonical ordering inside pairs and of pairs per corner handled by set
        bd = tuple(frozenset((mt[2 * c], mt[2 * c + 1])) for c in range(4))
        if bd in valid:
            continue
        adj = [[0] * 12 for _ in range(12)]
        for u, v in es:
            adj[u][v] = adj[v][u] = 1
        for i, j in combinations(range(4), 2):
            if i ^ j != 3:
                adj[8 + i][8 + j] = adj[8 + j][8 + i] = 1
        for c in range(4):
            for u in bd[c]:
                adj[u][8 + c] = adj[8 + c][u] = 1
        if check_graph(labs12, adj):
            valid.add(bd)
    # orbits under my group
    G = [(f, p, g) for f in stab for p in (0, 1) for g in product((0, 1), repeat=3)]
    def img(bd, f, p, g):
        new = [None] * 4
        for c in range(4):
            nc = yidx[y_img(y_labels[c], p, g)]
            new[nc] = frozenset(cidx[flip_lab(core_labels[u], f)] for u in bd[c])
        return tuple(new)
    seen = set(); my_orbits = []
    for bd in sorted(valid, key=lambda b: [sorted(x) for x in b]):
        if bd in seen:
            continue
        orb = {img(bd, *gg) for gg in G}
        assert orb <= valid, 'group does not preserve validity'
        seen |= orb; my_orbits.append(orb)
    cov = json.loads(gzip.decompress((SC / 'pybd_k2bc_all' / ('core_%03d.json.gz' % ci)).read_bytes()))
    cb = [tuple(frozenset(v for v in range(8) if m >> v & 1) for m in bytes.fromhex(h)) for h in cov['boundaries_hex']]
    in_valid = all(b in valid for b in cb)
    hits = [sum(1 for b in cb if b in orb) for orb in my_orbits]
    ok = in_valid and all(h == 1 for h in hits) and len(cb) == len(my_orbits)
    allok &= ok
    tot_my += len(my_orbits); tot_cov += len(cb)
    print(ci, 'stab', len(stab), 'valid', len(valid), 'my orbits', len(my_orbits), 'cover', len(cb), 'cover valid', in_valid, 'hits/orbit', set(hits), 'OK' if ok else 'MISMATCH')
print('total my orbits', tot_my, 'total cover', tot_cov, 'ALL OK', allok)
