"""Check of the side-relation lemma (LAB 15/10/2026, exact): for each component C of H_l (letters W, a union of lines),
kappa_C = 1 on the labels {0y, 1y : y in W} lies in ker T (when T >= 0) and is h-invariant; same for H_m.
usage: python side_check.py <json> [...]"""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    T = [[(3 if a == b else 0) - (1 if frozenset((S[a], S[b])) in E else 0) - kval(S[a], S[b]) for b in range(n)] for a in range(n)]
    hm = {0: 1, 1: 0, 2: 3, 3: 2}
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    for (a0, a1) in ((0, 1), (2, 3)):
        others = [y for y in range(14) if y not in (a0, a1)]
        # union-find on letters: y ~ y^1, and y ~ z when a label {a,y} is adjacent to a label {a',z} inside X
        par = {y: y for y in others}
        def find(y):
            while par[y] != y:
                par[y] = par[par[y]]; y = par[y]
            return y
        for y in others:
            par[find(y)] = find(y ^ 1)
        X = [i for i in range(n) if S[i] & {a0, a1}]
        for i in X:
            for j in X:
                if i < j and frozenset((S[i], S[j])) in E:
                    yi = [y for y in S[i] if y not in (a0, a1)][0]; yj = [y for y in S[j] if y not in (a0, a1)][0]
                    par[find(yi)] = find(yj)
        comps = {}
        for y in others:
            comps.setdefault(find(y), []).append(y)
        res = []
        for W in comps.values():
            kap = [Fr(1) if (S[i] & {a0, a1}) and ([y for y in S[i] if y not in (a0, a1)][0] in W) else Fr(0) for i in range(n)]
            inker = all(sum(T[r][c] * kap[c] for c in range(n)) == 0 for r in range(n))
            hinv = all(kap[i] == kap[hp[i]] for i in range(n))
            res.append((sorted(W), inker, hinv))
        print("%s side %s: c = %d components; (letters, in ker T, h-invariant): %s" % (f, (a0, a1), len(comps), res))
