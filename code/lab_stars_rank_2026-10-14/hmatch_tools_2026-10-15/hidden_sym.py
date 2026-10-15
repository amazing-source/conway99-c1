"""Hidden involutions of broken structures (LAB 15/10/2026, task T3, exact combinatorics).
For a structure, search all permutations p of the ten outer letters (star letters fixed) such that g = h p
(h = (0 1)(2 3)) relates the star matchings: M_1 = s_m p(M_0) and M_3 = s_l p(M_2) (matchings as sets of letter
pairs).  For each such p: is it mate-preserving (a frame symmetry), an involution, and is the whole structure
g-invariant (Gamma(g x, g y) = Gamma(x, y) on the 44 labels)?  Also reports the number of pairs fixed by g.
usage: python hidden_sym.py <json> [...]"""
import itertools, json, sys
OUT = list(range(4, 14))
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    def match(a):
        res = set()
        for i in range(n):
            for j in range(i + 1, n):
                if a in S[i] and a in S[j] and frozenset((S[i], S[j])) in E:
                    y = [t for t in S[i] if t != a][0]; z = [t for t in S[j] if t != a][0]
                    res.add(frozenset((y, z)))
        return res
    M = [match(a) for a in range(4)]
    sm = {2: 3, 3: 2}; sl = {0: 1, 1: 0}
    found = []
    for perm in itertools.permutations(OUT):
        p = dict(zip(OUT, perm))
        img0 = {frozenset(sm.get(p.get(y, y), p.get(y, y)) for y in pr) for pr in M[0]}
        if img0 != M[1]:
            continue
        img2 = {frozenset(sl.get(p.get(y, y), p.get(y, y)) for y in pr) for pr in M[2]}
        if img2 != M[3]:
            continue
        g = {0: 1, 1: 0, 2: 3, 3: 2}
        g.update(p)
        mate = all(p[y ^ 1] == p[y] ^ 1 for y in OUT)
        inv = all(p[p[y]] == y for y in OUT)
        gl = [idx[frozenset(g[y] for y in s)] for s in S]
        ginv = all((frozenset((S[gl[a]], S[gl[b]])) in E) == (frozenset((S[a], S[b])) in E) for a in range(n) for b in range(a + 1, n))
        moved = sorted(y for y in OUT if p[y] != y)
        found.append((moved, mate, inv, ginv))
    print("%s: %d permutations p with M_1 = s_m p M_0 and M_3 = s_l p M_2" % (f, len(found)))
    for moved, mate, inv, ginv in found[:12]:
        print("   p moves %s: mate-preserving %s, involution %s, whole structure g-invariant %s" % (moved, mate, inv, ginv))
