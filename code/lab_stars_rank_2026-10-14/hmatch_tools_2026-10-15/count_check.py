"""Check of the equitable count (LAB 15/10/2026): for a component C of H_l with letters W (k lines) and an m-only label
x = {b, z} (b in {2,3}, z outer), #(neighbours of x in C n X_l) = k - [z in W] - [m in W] whenever kappa_C is in ker T.
usage: python count_check.py <json> [...]"""
import json, sys
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S)
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    others = [y for y in range(2, 14)]
    par = {y: y for y in others}
    def find(y):
        while par[y] != y:
            par[y] = par[par[y]]; y = par[y]
        return y
    for y in others:
        par[find(y)] = find(y ^ 1)
    X = [i for i in range(n) if S[i] & {0, 1}]
    lt = lambda i: [y for y in S[i] if y not in (0, 1)][0]
    for i in X:
        for j in X:
            if i < j and frozenset((S[i], S[j])) in E:
                par[find(lt(i))] = find(lt(j))
    comps = {}
    for y in others:
        comps.setdefault(find(y), set()).add(y)
    bad = 0; tot = 0
    for W in comps.values():
        k = len(W) // 2
        CX = [i for i in X if lt(i) in W]
        for i in range(n):
            s = S[i]
            if s & {0, 1} or not s & {2, 3}:
                continue
            z = [y for y in s if y not in (2, 3)][0]
            cnt = sum(1 for j in CX if frozenset((S[i], S[j])) in E)
            pred = k - (1 if z in W else 0) - (1 if 2 in W else 0)
            tot += 1
            bad += cnt != pred
    print("%s: components %s; m-only label counts checked %d, mismatches %d" % (f, [sorted(W) for W in comps.values()], tot, bad))
