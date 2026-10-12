"""Lab session, 2026-10-12. CAYLEY CENSUS on the regular subgroups of the automorphism group of a given graph:
for every regular subgroup N of order 243 (maximal subgroups of the normal Sylow 3-subgroup, as in regular_subgroups.py),
ALL partial difference sets D of N with parameters (243,22,1,2) are enumerated (CryptoMiniSat, 121 variables; each
solution is blocked together with its conjugates under the Sylow 3-subgroup of Aut, which normalises N), and the Cayley graphs are classified by local invariants at the identity: number of
3x3 grids through the vertex and the numbers of lines parallel to its 11 lines.
D = D^-1, |D| = 22, and for every d != e:  #{a in D : a^-1 d in D} = 1 if d in D, 2 otherwise.
python cayley_census.py <edge file> <max solutions per group> [first group] [last group] [reference edge files ...]
(environment PYLIB = directory of pycryptosat, OUTDIR = where unidentified graphs are written). One representative per
local invariant is compared with the references by a direct isomorphism test.
Memory: small."""
import sys, os, itertools, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
import pycryptosat
import aut_tools as T, regular_subgroups as RS


def regular_groups(A):
    n = len(A); ident = tuple(range(n))
    o, gens, base, sizes = T.aut_group(A); gens = [tuple(g) for g in gens]
    G = RS.generate(gens, ident); ords = {g: RS.order(g, ident) for g in G}
    P = {g for g in G if ords[g] in (1, 3, 9, 27, 81, 243)}
    assert RS.generate(list(P), ident) == P, "Sylow 3-subgroup not normal"
    Pl = sorted(P); Pgens = []; cur = {ident}
    for g in Pl:
        if g not in cur: Pgens.append(g); cur = RS.generate(Pgens, ident)
        if len(cur) == len(P): break
    phi_gens = {RS.mul(RS.mul(g, g), g) for g in Pl}
    for a in Pgens:
        for b in Pl: phi_gens.add(RS.mul(RS.mul(a, b), RS.mul(RS.inv(a), RS.inv(b))))
    Phi = RS.generate(list(phi_gens), ident)
    rep = {}; cosets = []
    for g in Pl:
        if g in rep: continue
        c = {RS.mul(g, f) for f in Phi}
        for x in c: rep[x] = len(cosets)
        cosets.append(c)
    q = len(cosets); tab = [[rep[RS.mul(next(iter(cosets[i])), next(iter(cosets[j])))] for j in range(q)] for i in range(q)]; e = rep[ident]
    def sub_gen(Sx):
        Sx = set(Sx) | {e}; ch = True
        while ch:
            ch = False
            for a in list(Sx):
                for b in list(Sx):
                    c = tab[a][b]
                    if c not in Sx: Sx.add(c); ch = True
        return frozenset(Sx)
    r = 0
    while 3 ** r < q: r += 1
    hyper = {Sx for Sx in (sub_gen(c) for c in itertools.combinations(range(q), r - 1)) if len(Sx) == q // 3}
    out = []
    for Hc in sorted(hyper, key=sorted):
        N = set().union(*[cosets[i] for i in Hc])
        if all(all(g[x] != x for x in range(n)) for g in N if g != ident): out.append((N, ords, P))
    return out


def local_invariant(adj):
    """(grids through vertex 0, sorted numbers of lines parallel to the 11 lines through vertex 0)"""
    x = 0; third = lambda a, b: next(iter(adj[a] & adj[b]))
    lines = sorted({tuple(sorted((y, third(x, y)))) for y in adj[x]}); g = 0
    for (a, a2), (b, b2) in itertools.combinations(lines, 2):
        sec = lambda u, w: next(v for v in adj[u] & adj[w] if v != x)
        c = [sec(a, b), sec(a, b2), sec(a2, b), sec(a2, b2)]
        if c[1] in adj[c[0]] and c[2] in adj[c[0]] and c[3] in adj[c[1]] and c[3] in adj[c[2]]: g += 1
    par = []
    for (y, z) in lines:
        cnt = 0
        for w in adj[x]:
            if w in (y, z): continue
            w1 = [t for t in adj[w] & adj[y] if t != x][0]; w2 = [t for t in adj[w1] & adj[z] if t != y][0]
            if w2 in adj[w]: cnt += 1
        par.append(cnt)
    return g, tuple(sorted(par))


def census(N, n, maxsol, P=()):
    """P: permutations normalising N (here the Sylow 3-subgroup, in which N has index 3); the images of every
    solution under the conjugations x -> p x p^-1 are blocked too (they give isomorphic Cayley graphs)."""
    ident = tuple(range(n)); elt = {g[0]: g for g in N}; assert len(elt) == n
    conj = set()
    for p in P:
        pi = RS.inv(p); conj.add(tuple(p[elt[x][pi[0]]] for x in range(n)))     # index of p x p^-1 = (p x p^-1)(0)
    conj = sorted(conj)
    invp = {x: RS.inv(elt[x]) for x in range(n)}
    inv_idx = [invp[x][0] for x in range(n)]
    var = {}; nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    for a in range(1, n):
        if a not in var: v = new(); var[a] = v; var[inv_idx[a]] = v
    cache = {}
    def AND(a, b):
        if a == b: return a
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            t = new(); cl.extend([[-t, a], [-t, b], [t, -a, -b]]); cache[k] = t
        return cache[k]
    def exactly(lits, k):
        prev = None
        for l in lits:
            cur = [None] + [new() for _ in range(k + 1)]
            for j in range(1, k + 2):
                pj = prev[j] if prev else None
                if pj is not None: cl.append([-pj, cur[j]])
                if j == 1: cl.append([-l, cur[j]])
                elif prev: cl.append([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cl.append(c + [l])
                if j > 1: cl.append(c + ([prev[j - 1]] if prev else []))
            prev = cur
        if k >= 1: cl.append([prev[k]])
        cl.append([-prev[k + 1]])
    reps = sorted({min(a, inv_idx[a]) for a in range(1, n)})
    exactly([var[a] for a in reps], 11)
    for d in reps:
        lits = [AND(var[a], var[invp[a][d]]) for a in range(1, n) if a != d]
        exactly(lits + [var[d]], 2)
    s = pycryptosat.Solver(); s.add_clauses(cl)
    classes = collections.Counter(); examples = {}; nsol = 0
    while nsol < maxsol:
        sat, sol = s.solve()
        if not sat: return classes, examples, nsol, True
        D = [a for a in range(1, n) if sol[var[a]]]; nsol += 1
        adj = [set() for _ in range(n)]
        for x in range(n):
            g = elt[x]
            for d in D: adj[x].add(g[d])                      # x = g(0) ~ g(d(0)) = g(d)
        key = local_invariant(adj); classes[key] += 1
        if key not in examples: examples[key] = adj
        blocks = {tuple(sorted({var[c[a]] for a in D})) for c in conj} | {tuple(sorted({var[a] for a in D}))}
        for b in blocks: s.add_clause([-v for v in b])
    return classes, examples, nsol, False


if __name__ == "__main__":
    # python cayley_census.py <edge file> <max solutions per group> [first group] [last group] [reference edge files ...]
    import numpy as np
    A = T.load(sys.argv[1]); n = len(A); maxsol = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    g0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; g1 = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 6
    refs = [(os.path.basename(p), T.load(p)) for p in [sys.argv[1]] + sys.argv[5:]]
    groups = regular_groups(A); print("%d regular subgroups of order 243" % len(groups), flush=True)
    outdir = os.environ.get("OUTDIR")
    for gi, (N, ords, P) in enumerate(groups):
        if gi < g0 or gi > g1: continue
        t0 = time.time(); oc = sorted(collections.Counter(ords[g] for g in N).items())
        classes, examples, nsol, complete = census(N, n, maxsol, P)
        print("group %d (element orders %s): %d partial difference sets up to conjugation by the Sylow subgroup (%s, %.0f s)" % (gi, oc, nsol, "complete" if complete else "STOPPED at the limit", time.time() - t0), flush=True)
        for key, c in sorted(classes.items()):
            adj = examples[key]; B = np.zeros((n, n), dtype=np.int64)
            for a in range(n):
                for b in adj[a]: B[a, b] = 1
            name = next((nm for nm, R in refs if T.find_iso(B, R) is not None), None)
            print("     grids at a vertex %d, parallel lines of its 11 lines %s : %d sets; first one isomorphic to: %s" % (key[0], key[1], c, name if name else "NONE OF THE REFERENCES  <== NEW ?"), flush=True)
            if outdir and name is None:
                with open(os.path.join(outdir, "cayley_g%d_grids%d_%s.edges" % (gi, key[0], "-".join(map(str, key[1])))), "w", newline="\n") as f:
                    for a in range(n):
                        for b in sorted(adj[a]):
                            if a < b: f.write("%d %d\n" % (a, b))
