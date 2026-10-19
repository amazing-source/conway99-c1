# Independent check of py_boundary covers (no Codex imports).  For a core and family:
#  S = all valid ordered states (each grid: perfect matching inside supp(T) + layout with forced oppositions;
#      multiset of edges <= T; grids sharing a root: same core pair => different letter on that root);
#  O = union of orbits of the cover's states under (core stabiliser) x (Y relabellings);
#  check S == O, cover states are orbit minima, one per orbit.  Memory < 300 MB.
import gzip, json, sys
from itertools import combinations, permutations, product
W, famdir, fam, cis = sys.argv[1], sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4].split(',')]
GR = {"K3": ((0, 1), (0, 2), (1, 2)), "P3": ((0, 1), (0, 2)), "K2": ((0, 1),), "2K2": ((0, 1), (2, 3)), "2K2N": ((0, 1), (2, 3))}[fam]
NR = 4 if fam.startswith("2K2") else 3
NG = len(GR)
CORE = tuple((s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2))
cores = json.load(open(W + "/paircores8.json"))

def perfect_matchings(vs):
    if not vs:
        yield (); return
    a = vs[0]
    for b in vs[1:]:
        rest = [v for v in vs if v not in (a, b)]
        for m in perfect_matchings(rest):
            yield ((a, b),) + m

def stabilisers(core):
    E = {tuple(sorted(e)) for e in core['edges']}
    look = {q: i for i, q in enumerate(CORE)}
    out = []
    for swap in (0, 1):
        roots = (0, 2, 1) if swap else (0, 1, 2)
        for fl in product(range(2), repeat=3):
            p = [look[tuple(sorted(2*roots[l//2] + ((l % 2) ^ fl[l//2]) for l in q))] for q in CORE]
            if {tuple(sorted((p[u], p[v]))) for u, v in E} == E:
                out.append(p)
    return out

def ygroup():
    out = []
    G = set(GR)
    for p in permutations(range(NR)):
        if {tuple(sorted((p[a], p[b]))) for a, b in GR} != G:
            continue
        for f in product(range(2), repeat=NR):
            m = {}
            for g, (a, b) in enumerate(GR):
                na, nb = sorted((p[a], p[b])); ng = GR.index((na, nb))
                for s, t in product(range(2), repeat=2):
                    let = {p[a]: s ^ f[a], p[b]: t ^ f[b]}
                    m[(g, 2*s + t)] = (ng, 2*let[na] + let[nb])
            out.append(m)
    return out

YG = ygroup()
for ci in cis:
    core = cores[ci]
    T = {(u, v): core['T']['%d-%d' % (u, v)] for u, v in combinations(range(8), 2)}
    nb = [set() for _ in range(8)]
    for u, v in core['edges']:
        nb[u].add(v); nb[v].add(u)
    # per-grid options: (edges tuple per corner)
    opts = []
    for M in perfect_matchings(list(range(8))):
        if any(T[e] == 0 for e in M):
            continue
        forced = [(i, j) for i, j in combinations(range(4), 2)
                  if any(set(M[j]) <= nb[v] for v in M[i]) or any(set(M[i]) <= nb[v] for v in M[j])]
        for lay in permutations(range(4)):          # lay[c] = edge index at corner c
            pos = {e: c for c, e in enumerate(lay)}
            if all(pos[i] ^ pos[j] == 3 for i, j in forced):
                opts.append(tuple((1 << M[e][0]) | (1 << M[e][1]) for e in lay))
    shared = [(g, h, GR[g].index(r), GR[h].index(r)) for g in range(NG) for h in range(g+1, NG) for r in set(GR[g]) & set(GR[h])]
    S = set()
    for combo in product(opts, repeat=NG):
        cnt = {}
        for lay in combo:
            for m in lay:
                cnt[m] = cnt.get(m, 0) + 1
        if any(n > T[tuple(v for v in range(8) if m >> v & 1)] for m, n in cnt.items()):
            continue
        ok = True
        for g, h, kg, kh in shared:
            sg, sh = 1 - kg, 1 - kh            # bit index of the shared root's letter in the corner number
            for c1 in range(4):
                for c2 in range(4):
                    if combo[g][c1] == combo[h][c2] and ((c1 >> sg) & 1) == ((c2 >> sh) & 1):
                        ok = False
        if ok:
            S.add(bytes(x for lay in combo for x in lay))
    stabs = stabilisers(core)
    def mapmask(p, m):
        return sum(1 << p[v] for v in range(8) if m >> v & 1)
    def orbit(st):
        res = set()
        for p in stabs:
            s = [mapmask(p, b) for b in st]
            for m in YG:
                img = [0] * (4 * NG)
                for g in range(NG):
                    for c in range(4):
                        ng, nc = m[(g, c)]
                        img[4*ng + nc] = s[4*g + c]
                res.add(bytes(img))
        return res
    cov = json.loads(gzip.decompress(open('%s/core_%03d.json.gz' % (famdir, ci), 'rb').read()))
    if cov['status'] != 'COMPLETE_BOUNDARY_COVER':
        print(ci, cov['status'], 'valid ordered states', len(S)); continue
    reps = [bytes.fromhex(h) for h in cov['boundaries_hex']]
    O = set(); minima_ok = True; overlap = 0
    for r in reps:
        orb = orbit(r)
        if min(orb) != r: minima_ok = False
        if O & orb: overlap += 1
        O |= orb
    print(json.dumps({'core': ci, 'family': fam, 'cover_reps': len(reps), 'valid_ordered_states': len(S),
                      'orbit_union': len(O), 'S_subset_O': S <= O, 'O_subset_S': O <= S,
                      'reps_are_orbit_minima': minima_ok, 'orbits_overlapping': overlap,
                      'stabiliser_order': len(stabs), 'Ygroup_order': len(YG)}), flush=True)
