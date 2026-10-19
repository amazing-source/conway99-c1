# Independent boundary completeness check for P3NB (no Codex code).  For a core: enumerate every ordered pair of
# Y-layouts (Q45, Q46 corners -> disjoint core pairs covering the core), keep those satisfying lambda/mu on the
# 16-vertex graph core + Q45 + Q46 (no Q45-Q46 edges, Y-grids = letter 4-cycles), then check every one lies in the
# orbit (under MY implementation of: flips of lines 0,1,2 stabilising the core x flips of 4,5,6 x swap 5<->6) of a
# recorded boundary; and that every recorded boundary is itself valid.
import gzip, json, sys, time
from itertools import permutations, product, combinations
cores = json.load(open(sys.argv[1])); covdir = sys.argv[2]; sel = [int(x) for x in sys.argv[3].split(",")]
CL = [(s, 2 + t) for s in range(2) for t in range(2)] + [(s, 4 + t) for s in range(2) for t in range(2)]
Y = [(8 + s, 10 + t) for s in range(2) for t in range(2)] + [(8 + s, 12 + t) for s in range(2) for t in range(2)]
LAB = CL + Y
def shared(a, b): return len(set(a) & set(b))
def matchings(vs):
    if not vs: yield (); return
    a, *rest = vs
    for b in rest:
        for t in matchings([v for v in rest if v != b]): yield ((a, b),) + t
LAYOUTS = []
for m in matchings(list(range(8))):
    for p in permutations(m):
        LAYOUTS.append(tuple((1 << a) | (1 << b) for a, b in p))
assert len(LAYOUTS) == 2520
def valid_single(core_adj, lay, g):
    # 12 vertices: core 0..7, grid labels 8..11 (= Y[4g..4g+3])
    labs = CL + Y[4 * g:4 * g + 4]
    adj = list(core_adj) + [0] * 4
    for c in range(4):
        for d in range(4):
            if c != d and c ^ d != 3: adj[8 + c] |= 1 << (8 + d)
        m = lay[c]
        for v in range(8):
            if m >> v & 1: adj[8 + c] |= 1 << v; adj[v] |= 1 << (8 + c)
    for u, v in combinations(range(12), 2):
        a = adj[u] >> v & 1
        if (adj[u] & adj[v]).bit_count() + shared(labs[u], labs[v]) > 2 - a: return False
    return True
def group(core_adj):
    # elements: (core perm p on 0..7, Y perm on 0..7)
    els = []
    lk = {frozenset(q): i for i, q in enumerate(CL)}
    yk = {frozenset(q): i for i, q in enumerate(Y)}
    E = {frozenset((u, v)) for u in range(8) for v in range(8) if core_adj[u] >> v & 1}
    for f in product(range(2), repeat=3):
        p = [lk[frozenset(2 * (l // 2) + ((l & 1) ^ f[l // 2]) for l in q)] for q in CL]
        if {frozenset((p[u], p[v])) for u, v in map(tuple, E)} != E: continue
        for g in product(range(2), repeat=3):          # flips of lines 4,5,6
            for sw in (0, 1):
                def mapl(l):
                    line, bit = divmod(l, 2)
                    if sw and line in (5, 6): line = 11 - line
                    return 2 * line + (bit ^ g[line - 4]) if line >= 4 else l   # flip indexed by ORIGINAL line
                yp = [yk[frozenset(mapl(l) if True else l for l in q)] for q in Y]
                els.append((p, yp))
    return els
def act(el, bd):
    p, yp = el
    out = [0] * 8
    for k in range(8):
        m = bd[k]; img = 0
        for v in range(8):
            if m >> v & 1: img |= 1 << p[v]
        out[yp[k]] = img
    return tuple(out)
for ci in sel:
    t0 = time.time()
    core = cores[ci]
    cadj = [0] * 8
    for u, v in core["edges"]: cadj[u] |= 1 << v; cadj[v] |= 1 << u
    V = [lay for lay in LAYOUTS if valid_single(cadj, lay, 0)]
    V2 = [lay for lay in LAYOUTS if valid_single(cadj, lay, 1)]
    assert V == V2
    T = {}
    for u, v in combinations(range(8), 2):
        T[(u, v)] = 2 - (cadj[u] >> v & 1) - shared(CL[u], CL[v]) - (cadj[u] & cadj[v]).bit_count()
    pairmask = {(1 << u) | (1 << v): (u, v) for u, v in combinations(range(8), 2)}
    mine = set()
    for A in V:
        for B in V:
            ok = True
            # Q45 corner c (letter 8+(c>>1) on line 4) vs Q46 corner d: shared letter iff same line-4 bit
            for c in range(4):
                for d in range(4):
                    if (A[c] & B[d]).bit_count() + ((c >> 1) == (d >> 1)) > 2: ok = False; break
                if not ok: break
            if not ok: continue
            cnt = {}
            for m in A + B:
                k = pairmask[m]; cnt[k] = cnt.get(k, 0) + 1
            if any(n > T[k] for k, n in cnt.items()): continue
            mine.add(A + B)
    rec = json.loads(gzip.decompress(open("%s/core_%03d.json.gz" % (covdir, ci), "rb").read()))
    recs = [tuple(bytes.fromhex(h)) for h in rec["boundaries_hex"]]
    G = group(cadj)
    clos = set()
    for b in recs:
        for el in G: clos.add(act(el, b))
    rec_valid = sum(1 for b in recs if b in mine)
    # orbit count of mine
    left = set(mine); norb = 0
    while left:
        b = next(iter(left)); norb += 1
        left -= {act(el, b) for el in G}
    print(json.dumps({"core": ci, "single_valid": len(V), "valid_pairs": len(mine), "my_orbits": norb,
                      "recorded": len(recs), "recorded_valid": rec_valid, "missing_from_cover": len(mine - clos),
                      "group_order": len(G), "sec": round(time.time() - t0, 1)}), flush=True)
