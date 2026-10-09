"""C1, lab session, 2026-10-09. Independent check of the laptop session's reduction of the (4,8) sweep to one ball per
isomorphism class (its reps48.py / actc.c, commit cb4ff9ec1 of conway99-c2-aws).
  python iso_check_reps48.py <folder with its code, types files, act22_c.txt, act48.txt, reps48.txt> <sample size> <seed>
Its claim: for a small type s, the balls (s, b) and (s, g.b) are isomorphic when the order g of the layers fixes s.
Check done here WITHOUT its action code: the two balls are built by its make_ball (the same function the sweep uses) and
compared as graphs on 36 vertices with a partition into three layers, by networkx (VF2), trying the six permutations
of the layers. Positive sample: random balls that are not representatives, against their representative: all must be
isomorphic. Negative control: random pairs of representatives of different classes for the same s: none should be.
Also checked on the whole list: every ball belongs to exactly one class of reps48.txt and the class sizes add up.
Sample size 0 = complete mode: EVERY non-representative ball against its representative (about half an hour).
One process, below 1 GB."""
import sys, os, random, itertools, time
import networkx as nx
folder = os.path.abspath(sys.argv[1]); nsample = int(sys.argv[2]); random.seed(int(sys.argv[3])); os.chdir(folder); sys.path.insert(0, folder)
from multi import make_ball
from sweep48 import SMALL, REPS, big_key
t0 = time.time(); load = lambda p: [list(map(int, l.split())) for l in open(p) if l.strip()]
a2 = load("act22_c.txt"); a4 = load("act48.txt"); small_all = load("types_m2.txt"); p0 = [i for i, v in enumerate(small_all) if v[12] == 0]
lines = [l for l in open("types_m4_p0.txt").read().split("\n") if l.strip()]; reps = load("reps48.txt"); ID = [(0, 1, 2)] * 2
stab = {s: [g for g in range(6) if a2[p0[s]][g] == p0[s]] for s in REPS}
repset = {(s, b) for s, b, k in reps}; assert len(repset) == len(reps)
tot = 0
for s in REPS:                                                         # every ball in exactly one class, sizes add up
    cls = {}
    for b in range(len(a4)): cls.setdefault(min(a4[b][g] for g in stab[s]), set()).add(b)
    assert set(cls) == {b for (s2, b) in repset if s2 == s}, "representatives differ from the minima of the classes"
    assert all(len(cls[b]) == k for s2, b, k in reps if s2 == s); tot += sum(len(c) for c in cls.values())
assert tot == 3 * len(a4); print("classes: %d balls in %d classes, sizes consistent with reps48.txt" % (tot, len(reps)))
def graph(s, b):
    adj, lay, comp = make_ball([SMALL[s], big_key(lines[b])], ID); G = nx.Graph()
    for v in range(36): G.add_node(v, lay=lay[v])
    for v in range(36):
        for w in adj[v]: G.add_edge(v, w)
    assert all(d == 3 for _, d in G.degree()); return G
def iso(G, H):
    for perm in itertools.permutations(range(3)):
        if nx.is_isomorphic(G, H, node_match=lambda x, y, perm=perm: perm[x["lay"]] == y["lay"]): return perm
    return None
if nsample == 0:                                                       # complete mode: every non-representative ball against its representative
    import json
    pos = fail = 0; cache = {}; bad = []
    for s in REPS:
        for b in range(len(a4)):
            r = min(a4[b][g] for g in stab[s])
            if r == b: continue
            if (s, r) not in cache: cache.clear(); cache[(s, r)] = graph(s, r)
            if iso(graph(s, b), cache[(s, r)]) is None: fail += 1; bad.append((s, b, r)); print("NOT ISOMORPHIC: ball (%d, %d) and its representative (%d, %d)" % (s, b, s, r), flush=True)
            else: pos += 1
            if (pos + fail) % 20000 == 0: print("   %d done, %d not isomorphic   [%.0f s]" % (pos + fail, fail, time.time() - t0), flush=True)
    print("COMPLETE: %d non-representative balls, isomorphic to their representative: %d, not isomorphic: %d   [%.0f s]" % (pos + fail, pos, fail, time.time() - t0))
    json.dump({"non_representatives": pos + fail, "isomorphic": pos, "not_isomorphic": bad, "classes": len(reps)}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "iso_check_reps48_complete.json"), "w")); sys.exit(0)
pos = fail = 0
while pos + fail < nsample:
    s = random.choice(REPS); b = random.randrange(len(a4)); r = min(a4[b][g] for g in stab[s])
    if r == b: continue
    p = iso(graph(s, b), graph(s, r))
    if p is None: fail += 1; print("NOT ISOMORPHIC: ball (%d, %d) and its representative (%d, %d)" % (s, b, s, r))
    else: pos += 1
print("positive sample: %d non-representative balls, isomorphic to their representative: %d, not isomorphic: %d   [%.0f s]" % (pos + fail, pos, fail, time.time() - t0), flush=True)
neg = hit = 0; bys = {s: [b for (s2, b) in repset if s2 == s] for s in REPS}
while neg < nsample:
    s = random.choice(REPS); b1, b2 = random.sample(bys[s], 2); neg += 1
    if iso(graph(s, b1), graph(s, b2)) is not None: hit += 1; print("ISOMORPHIC representatives of different classes: (%d, %d) and (%d, %d)" % (s, b1, s, b2))
print("negative control: %d pairs of representatives of different classes, isomorphic: %d   [%.0f s]" % (neg, hit, time.time() - t0))
