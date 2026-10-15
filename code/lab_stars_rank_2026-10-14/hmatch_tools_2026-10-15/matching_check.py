"""Independent exact check of the (H-MATCH) relation (LAB 15/10/2026): reads only labels and edges.
M_a = {{y, z} : {a,y} ~ {a,z}} for a = 0..3; h = (0 1)(2 3) acts on letters; (H-MATCH) at (l, m) means
M_1 = h(M_0) and M_3 = h(M_2) as sets of letter pairs.  Prints the four matchings and the verdict per half.
usage: python matching_check.py <json>"""
import json, sys
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]
E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
hm = {0: 1, 1: 0, 2: 3, 3: 2}
H = lambda y: hm.get(y, y)
M = {}
for a in range(4):
    star = [s for s in S if a in s]
    pairs = set()
    for s in star:
        nb = [t for t in star if t != s and frozenset((s, t)) in E]
        assert len(nb) == 1, "label %s has %d neighbours in its own star %d (C1 violated)" % (sorted(s), len(nb), a)
        y = [x for x in s if x != a][0]
        z = [x for x in nb[0] if x != a][0]
        pairs.add(frozenset((y, z)))
    assert len(pairs) == 6
    M[a] = pairs
    print("M_%d = %s" % (a, sorted(tuple(sorted(p)) for p in pairs)))
lhalf = M[1] == {frozenset(H(y) for y in p) for p in M[0]}
mhalf = M[3] == {frozenset(H(y) for y in p) for p in M[2]}
print("l-half M_1 = h(M_0): %s ; m-half M_3 = h(M_2): %s" % (lhalf, mhalf))
print("MATCHINGS %s" % ("h-RELATED (consistent with H-MATCH)" if lhalf and mhalf else "NOT h-related (BROKEN)"))
