"""notes/105: independent re-implementation (different data structures and search order) of the two
enumerations of the L8 proof, as a guard against coding errors.
(1) line skeletons: every pair P must see, on the 15 Kneser triangles through it, the l-pattern of type
    A (one Petersen perfect matching: 4 on it, 0 elsewhere) or B (4 on one triangle t0, 2 on the other
    edges of the two matchings through t0, 0 elsewhere).  Search by propagation over triangles in a
    reversed order.  Expected: 30 solutions, all Fano.
(2) B/C configurations for one Fano plane (a different plane from the first check), with the statuses
    derived from first principles: C independent in the non-pencil graph, non-pencil B-B iso, B-C non-iso,
    then brute force over ALL pencil-edge statuses (21 bits) filtered by (T1) and (T2) only.
    Expected: the survivors are exactly stars and quadrilaterals (35), and the kappa system kills all."""
import itertools
from collections import Counter

cls = range(7)
pairs = [frozenset(p) for p in itertools.combinations(cls, 2)]
P_idx = {p: i for i, p in enumerate(pairs)}
tri = [frozenset(t) for t in itertools.combinations(range(21), 3)
       if all(not (pairs[a] & pairs[b]) for a, b in itertools.combinations(t, 2))]
tri_of = {i: [n for n, t in enumerate(tri) if i in t] for i in range(21)}

def matchings(i):
    link = [j for j in range(21) if not (pairs[i] & pairs[j])]
    E = [n for n in tri_of[i]]                     # triangle n through i <-> Petersen edge
    out = []
    for c in itertools.combinations(E, 5):
        cov = Counter(j for n in c for j in tri[n] if j != i)
        if len(cov) == 10 and set(cov.values()) == {1}:
            out.append(frozenset(c))
    return out

patterns = {}
for i in range(21):
    Ms = matchings(i)
    pats = []
    for M in Ms:
        pats.append({n: (4 if n in M else 0) for n in tri_of[i]})
    for t0 in tri_of[i]:
        two = [M for M in Ms if t0 in M]
        pats.append({n: 4 if n == t0 else (2 if any(n in M for M in two) else 0) for n in tri_of[i]})
    patterns[i] = pats

order = list(range(20, -1, -1))
sols = []
def rec(k, ell):
    if k == 21:
        sols.append(dict(ell)); return
    i = order[k]
    for pat in patterns[i]:
        if all(ell.get(n, v) == v for n, v in pat.items()):
            new = [n for n in pat if n not in ell]
            for n in new: ell[n] = pat[n]
            rec(k + 1, ell)
            for n in new: del ell[n]
rec(0, {})
fano_ok = 0
for s in sols:
    pencils = [tri[n] for n, v in s.items() if v == 4]
    # rebuild lines: for each pencil, missing class v, lines = pair u {v}
    lines = set()
    for t in pencils:
        v = next(c for c in cls if all(c not in pairs[j] for j in t))
        for j in t:
            lines.add(frozenset(pairs[j] | {v}))
    if len(lines) == 7 and all(len(a & b) == 1 for a, b in itertools.combinations(lines, 2)):
        fano_ok += 1
print('(1) skeletons:', len(sols), ' of which built from a Fano plane:', fano_ok, flush=True)

# (2) a different Fano plane: lines {0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}
L = [frozenset(x) for x in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
def vp(p): return next(c for c in next(l for l in L if p <= l) if c not in p)
kedge = [(a, b) for a, b in itertools.combinations(range(21), 2) if not (pairs[a] & pairs[b])]
is_pen = {e: vp(pairs[e[0]]) == vp(pairs[e[1]]) for e in kedge}
pen_edges = [e for e in kedge if is_pen[e]]
np_nbrs = {i: [j for j in range(21) if not (pairs[i] & pairs[j]) and vp(pairs[i]) != vp(pairs[j])] for i in range(21)}
def conn_even(edges):
    if not edges: return True
    if len(edges) % 2: return False
    vs = set(v for e in edges for v in e); comp = {next(iter(vs))}; grow = True
    while grow:
        grow = False
        for a, b in edges:
            if (a in comp) != (b in comp): comp |= {a, b}; grow = True
    return comp == vs
indep = []
def grow(cur, s):
    for j in range(s, 21):
        if all(k not in np_nbrs[j] for k in cur):
            indep.append(cur + [j]); grow(cur + [j], j + 1)
grow([], 0)
tri_edges = [[tuple(sorted(e)) for e in itertools.combinations(sorted(t), 2)] for t in tri]
edge_tris = {}
for n, es in enumerate(tri_edges):
    for e in es:
        edge_tris.setdefault(e, []).append(n)
def t1_ok(st, n):
    es = tri_edges[n]
    if any(e not in st for e in es):
        return True
    return sum(st[e] == 0 for e in es) != 2
surv = []
for C in indep:
    Cs = set(C)
    st = {}
    for e in kedge:
        if not is_pen[e]:
            st[e] = int((e[0] in Cs) != (e[1] in Cs))
    if not all(t1_ok(st, n) for n in range(len(tri))):
        continue
    def bt(k):
        if k == len(pen_edges):
            for i in range(21):
                G = [tuple(sorted(pairs[j])) for j in range(21)
                     if not (pairs[i] & pairs[j]) and st[tuple(sorted((i, j)))] == 1]
                if not conn_even(G):
                    return
            surv.append((tuple(sorted(tuple(sorted(pairs[c])) for c in C)), dict(st)))
            return
        e = pen_edges[k]
        for b in (0, 1):
            st[e] = b
            if all(t1_ok(st, n) for n in edge_tris[e]):
                bt(k + 1)
            del st[e]
    bt(0)
print('(2) survivors for the second Fano plane:', len(surv), Counter(len(c) for c, _ in surv))
from kappa_linear_system import system, consistent
res = Counter()
for C, st in surv:
    nu = {frozenset((tuple(sorted(pairs[a])), tuple(sorted(pairs[b])))) for (a, b), s in st.items() if s == 1}
    res[consistent(system(nu)[0])[0]] += 1
print('    kappa-system consistent?', dict(res))
