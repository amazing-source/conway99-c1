"""C1, lab session, 2026-10-09. Partner kernels of one quadrangle (NOTE 17.83). No rank hypothesis, no hypothesis on prisms.

Setting (Codex's note 221): S = triangles 012 and 345 with cross edges 03, 14 and no other edge between them; D = the eight
vertices with two neighbours in S (6:{0,3} 7:{1,4} 8:{2,3} 9:{2,4} 10:{0,5} 11:{1,5} 12,13:{2,5}); H = S + D; a "type" is the
set of edges inside D (21 optional pairs). 174 types survive Codex's exact tests (notes 221, 222).

New fact used here: the quadrangle 0-3-4-1 has a second pair of opposite edges, 0-1 and 3-4, whose lines are {0,3,6} and
{1,4,7}. When 6 and 7 are not adjacent, S* = {0,3,6} + {1,4,7} is again an occurrence of the motif (cross edges 0-1 and
3-4), so its own kernel H* = S* + D* must be one of the 174 types too, and the induced graph on H u H* (at most 20
vertices) must satisfy the common-neighbour bounds and the two exact positivity conditions of note 221.
D* = {2, 5, d(1,6), d(4,6), d(0,7), d(3,7), and the two common neighbours of 6 and 7}; some of these are vertices of D
(11 if 6~11, 9 if 6~9, 10 if 7~10, 8 if 7~8, 12 or 13 if adjacent to both 6 and 7), the others are new vertices whose
neighbours in S are forced (exactly {1}, {4}, {0}, {3}; a subset of {2,5} other than {2,5} for the last two).

For every surviving type with 6 not adjacent to 7 the program enumerates ALL completions of H u H*:
  - the type of H* ranges over the labelled survivors (the 174 orbits under the group of order 8 of note 221);
  - the adjacencies of the new vertices to the vertices of D outside D* are free;
  - kept: common neighbours <= 2 - adjacency for every pair, and 27I - 9A + J >= 0, 44I + 11A - 2J >= 0 on the union
    (floating test with exact rational confirmation of every rejection).
A type with no completion cannot occur in a strongly regular graph (99,14,1,2).

usage: python quad_partner_kernels.py <Codex data folder> <output json> [first index] [last index] [time limit in s] [limit per type in s]
One process; memory below 300 MB; the time limit stops cleanly between types (the output lists the types done)."""
import sys, os, json, time, itertools
from fractions import Fraction
import numpy as np

DATA = sys.argv[1]; OUT = sys.argv[2]
FIRST = int(sys.argv[3]) if len(sys.argv) > 3 else 0
LAST = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
TLIM = float(sys.argv[5]) if len(sys.argv) > 5 else 270.0
PER_TYPE = float(sys.argv[6]) if len(sys.argv) > 6 else 60.0     # a type not finished in that time is recorded as UNKNOWN, never as excluded
T0 = time.time()

core = json.load(open(os.path.join(DATA, "codex_twisted_prism_core.json")))
OPT = [tuple(e) for e in core["optional_edges"]]; OPTI = {e: i for i, e in enumerate(OPT)}
prof = json.load(open(os.path.join(DATA, "codex_core_component_profiles.json")))
SURV = [c["bits"] for c in prof["cores"]]; assert len(SURV) == 174
S_EDGES = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4)]
MASK = {6: (0, 3), 7: (1, 4), 8: (2, 3), 9: (2, 4), 10: (0, 5), 11: (1, 5), 12: (2, 5), 13: (2, 5)}
FORBIDDEN = [e for e in itertools.combinations(range(6, 14), 2) if e not in OPTI]; assert len(FORBIDDEN) == 7

# the group of order 8 of note 221 (automorphisms of S acting on the masks, and the swap of 12 and 13)
ALPHA = {0: 1, 1: 0, 2: 2, 3: 4, 4: 3, 5: 5, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 12, 13: 13}
BETA = {0: 3, 1: 4, 2: 5, 3: 0, 4: 1, 5: 2, 6: 6, 7: 7, 8: 10, 9: 11, 10: 8, 11: 9, 12: 12, 13: 13}
GAMMA = {**{i: i for i in range(12)}, 12: 13, 13: 12}
def compose(g, h): return {i: g[h[i]] for i in range(14)}
GROUP = [{i: i for i in range(14)}]
changed = True
while changed:
    changed = False
    for g in list(GROUP):
        for h in (ALPHA, BETA, GAMMA):
            k = compose(h, g)
            if k not in GROUP: GROUP.append(k); changed = True
assert len(GROUP) == 8
def act(bits, g):
    out = 0
    for i, (u, v) in enumerate(OPT):
        if bits >> i & 1:
            e = tuple(sorted((g[u], g[v]))); out |= 1 << OPTI[e]
    return out
def canon(bits): return min(act(bits, g) for g in GROUP)
assert all(canon(b) == b or canon(b) in SURV for b in SURV)
CANON_SURV = {canon(b) for b in SURV}; assert len(CANON_SURV) == 174
LABELLED = sorted({act(b, g) for b in SURV for g in GROUP})
ORB = {b: c["orbit_size"] for c in core["cores"] for b in [c["bits"]]}
assert all(len({act(b, g) for g in GROUP}) == ORB[b] for b in SURV if b in ORB)

def base_adj(bits):
    adj = [0] * 14
    def e(u, v): adj[u] |= 1 << v; adj[v] |= 1 << u
    for u, v in S_EDGES: e(u, v)
    for d, (a, b) in MASK.items(): e(d, a); e(d, b)
    for i, (u, v) in enumerate(OPT):
        if bits >> i & 1: e(u, v)
    return adj

def ok_pairs(adj, n):
    """common neighbours <= 2 - adjacency for every pair of the first n vertices"""
    for u in range(n):
        au = adj[u]
        for v in range(u + 1, n):
            if bin(au & adj[v]).count("1") > (1 if au >> v & 1 else 2): return False
    return True

def psd_exact(M):
    """exact test that the integer symmetric matrix M is positive semidefinite (rational elimination, singular case included)"""
    n = len(M); A = [[Fraction(x) for x in r] for r in M]; live = list(range(n))
    while live:
        if any(A[i][i] < 0 for i in live): return False
        p = next((i for i in live if A[i][i] > 0), None)
        if p is None: return all(A[i][j] == 0 for i in live for j in live)
        live.remove(p); pp = A[p][p]
        for i in live:
            if A[i][p] != 0:
                f = A[i][p] / pp
                for j in live: A[i][j] -= f * A[p][j]
    return True

STAT = {"float_reject": 0, "exact_reject": 0, "exact_overturn": 0, "borderline_exact": 0}
EXACT = os.environ.get("EXACT", "0") == "1"       # EXACT=1: every rejection by positivity is confirmed in exact rational arithmetic
def positive(adj, n):
    A = np.zeros((n, n))
    for u in range(n):
        au = adj[u]
        for v in range(n):
            if au >> v & 1: A[u, v] = 1.0
    I = np.eye(n); J = np.ones((n, n))
    for Q in (27 * I - 9 * A + J, 44 * I + 11 * A - 2 * J):
        m = np.linalg.eigvalsh(Q)[0]
        if m > 1e-6: continue
        if m < -1e-6 and not EXACT: STAT["float_reject"] += 1; return False
        good = psd_exact([[int(round(x)) for x in row] for row in Q.tolist()])
        if m < -1e-6:
            if good: STAT["exact_overturn"] += 1
            else: STAT["exact_reject"] += 1
        else: STAT["borderline_exact"] += 1
        if not good: return False
    return True

STAR_S = {0: 0, 1: 3, 2: 6, 3: 1, 4: 4, 5: 7}            # label in H* -> vertex, for the six vertices of S*
def interface(bits):
    b = lambda u, v: bits >> OPTI[(u, v)] & 1
    return b(6, 11), b(6, 9), b(7, 10), b(7, 8), [k for k in (12, 13) if b(6, k) and b(7, k)]

def partners(bits, every=None):
    """partner types of the labelled type 'bits' (6 not adjacent to 7): canonical type -> one completion of H u H*"""
    b = lambda u, v: bits >> OPTI[(u, v)] & 1
    assert not b(6, 7)
    adj0 = base_adj(bits); assert ok_pairs(adj0, 14)
    i611, i69, i710, i78, both = interface(bits)
    star = dict(STAR_S); star[6] = 2; star[7] = 5
    new = []                                             # (label in H*, forced neighbours in H, allowed sets of neighbours among {2,5})
    for lab, ident, old, smask, other in ((8, i611, 11, 1, 6), (9, i69, 9, 4, 6), (10, i710, 10, 0, 7), (11, i78, 8, 3, 7)):
        if ident: star[lab] = old
        else: new.append((lab, (smask, other), ((),)))
    labs = [12, 13]
    for k in both: star[labs.pop(0)] = k
    for lab in labs: new.append((lab, (6, 7), ((), (2,), (5,))))      # a common neighbour of 6, 7 adjacent to 2 and 5 would be 12 or 13
    m = len(new); old_labels = [l for l in range(6, 14) if l in star]
    cands = [c for c in LABELLED
             if all((c >> OPTI[(p, q)] & 1) == (adj0[star[p]] >> star[q] & 1) for p, q in OPT if p in star and q in star)]
    deadline = time.time() + PER_TYPE
    def with_vertices(masks_and_edges):
        """adjacency of H plus the listed new vertices; item = (set of neighbours in H, list of earlier new indices it is adjacent to)"""
        a = adj0[:]
        for t, (mk, back) in enumerate(masks_and_edges):
            v = 14 + t; a.append(0)
            for x in mk: a[v] |= 1 << x; a[x] |= 1 << v
            for u in back: a[v] |= 1 << (14 + u); a[14 + u] |= 1 << v
        return a
    # every admissible neighbourhood in H of each new vertex, independently of the partner type
    valid = []
    for lab, forced, s_opts in new:
        opts = []
        for so in s_opts:
            for r in range(7):
                for extra in itertools.combinations(range(8, 14), r):
                    mk = frozenset(forced) | frozenset(so) | frozenset(extra)
                    a = with_vertices([(mk, [])])
                    if ok_pairs(a, 15) and positive(a, 15): opts.append(mk)
        valid.append(opts)
    memo = {}
    def pair_ok(i, mi, j, mj, x):
        key = (i, mi, j, mj, x)
        if key not in memo:
            a = with_vertices([(mi, []), (mj, [0] if x else [])])
            memo[key] = ok_pairs(a, 16) and positive(a, 16)
        return memo[key]
    def cbit(c, p, q):
        e = (p, q) if p < q else (q, p)
        return c >> OPTI[e] & 1 if e in OPTI else 0      # the seven other pairs of D* are never adjacent
    found = {}; tested = 0
    def rec(k, chosen, c):
        if time.time() > deadline: raise TimeoutError
        if k == m:
            items = [(chosen[t], [u for u in range(t) if cbit(c, new[t][0], new[u][0])]) for t in range(m)]
            a = with_vertices(items)
            if ok_pairs(a, 14 + m) and positive(a, 14 + m):
                if every is not None: every.append((c, a)); return None      # collect every completion instead of stopping at the first
                return {"partner_labelled": c, "vertices": 14 + m, "new": [{"label": new[t][0], "neighbours_in_H": sorted(chosen[t]),
                        "earlier_new": items[t][1]} for t in range(m)]}
            return None
        lab = new[k][0]
        for mk in valid[k]:
            if any((star[l] in mk) != bool(cbit(c, lab, l)) for l in old_labels): continue
            if any(not pair_ok(u, chosen[u], k, mk, cbit(c, new[u][0], lab)) for u in range(k)): continue
            w = rec(k + 1, chosen + [mk], c)
            if w is not None: return w
        return None
    for c in cands:
        cc = canon(c)
        if cc in found and every is None: continue
        tested += 1
        w = rec(0, [], c)
        if w is not None: found[cc] = w
    return found, tested, len(cands), [len(v) for v in valid]

if __name__ == "__main__":
    res = json.load(open(OUT)) if os.path.exists(OUT) else {"types": {}}
    todo = [b for i, b in enumerate(SURV) if FIRST <= i < LAST and str(b) not in res["types"]]
    for b in todo:
        if time.time() - T0 > TLIM: break
        t1 = time.time()
        if b >> OPTI[(6, 7)] & 1:
            res["types"][str(b)] = {"prism_partner": True}; continue
        try: found, tested, ncand, nvalid = partners(b)
        except TimeoutError:
            res["types"][str(b)] = {"prism_partner": False, "unknown": True, "seconds": round(time.time() - t1, 2)}
            json.dump(res, open(OUT, "w")); continue
        res["types"][str(b)] = {"prism_partner": False, "partners": sorted(found), "candidates_labelled": ncand, "searched": tested, "admissible_neighbourhoods": nvalid,
                                "sizes": sorted({w["vertices"] for w in found.values()}), "seconds": round(time.time() - t1, 2),
                                "witness": {str(k): w for k, w in found.items()}}
        json.dump(res, open(OUT, "w"))
    res["stat"] = STAT; res["labelled_survivors"] = len(LABELLED); res["exact_mode"] = EXACT
    json.dump(res, open(OUT, "w"))
    done = res["types"]; np_ = [b for b in done if not done[b]["prism_partner"]]
    unk = [b for b in np_ if done[b].get("unknown")]
    dead = [b for b in np_ if not done[b].get("unknown") and not done[b]["partners"]]
    print("types done %d of 174; with 6 not adjacent to 7: %d; UNKNOWN (time limit) %d; without any partner: %d" % (len(done), len(np_), len(unk), len(dead)))
    print("labelled survivors %d; positivity: %s; exact mode %s; elapsed %.0f s" % (len(LABELLED), STAT, EXACT, time.time() - T0))
    if dead: print("no partner:", dead)
