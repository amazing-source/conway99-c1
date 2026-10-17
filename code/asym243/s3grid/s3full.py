"""Full S3-gain model of 3-fold covers of BH along a regular spread (note 165): srg(243,22,1,2) <=>
 (i) gains g_e in S3 on the 810 edges, consistent around the 270 line-triangles, and
 (ii) for each of the 2430 non-adjacent pairs, the 6 path products g_ZR o g_PZ form one of the 3 multisets
      {S3 once each}, {A3 twice each}, {reflections twice each}  (brute-force: these are all with sum = 2J).
Gauge: g = id on a BFS tree from 0.
Modes: control (no extra constraint; must be SAT = a Z3-cover such as BvLS),
       s3 (pair (0,R0) of type 'S3 once each' = nontrivial sign class, WLOG by rank 3 + Jorgensen).
Usage: python3 s3full.py MODE OUT.cnf"""
import itertools, sys, collections
sys.argv_saved = list(sys.argv); sys.argv = ['x']
exec(open(__file__.replace('s3full.py', 's3grid.py')).read().split('if __name__')[0])
sys.argv = sys.argv_saved
G = list(itertools.permutations(range(3))); GI = {g: i for i, g in enumerate(G)}
comp = lambda b, a: GI[tuple(G[b][G[a][i]] for i in range(3))]          # b o a
inv = lambda a: GI[tuple(sorted(range(3), key=lambda i: G[a][i]))]
ID = GI[(0, 1, 2)]
EVEN = [g for g in range(6) if sum(G[g][i] > G[g][j] for i in range(3) for j in range(i + 1, 3)) % 2 == 0]
ODD = [g for g in range(6) if g not in EVEN]
mode, out = sys.argv[1], sys.argv[2]
nv = 0; cls = []
def new():
    global nv; nv += 1; return nv
def exactly_one(vs):
    cls.append(list(vs))
    for a, b in itertools.combinations(vs, 2): cls.append([-a, -b])
X = {}
for i in range(n):
    for j in adj[i]:
        if i < j: X[(i, j)] = [new() for _ in range(6)]; exactly_one(X[(i, j)])
def gain(u, v, g):   # literal "gain u->v equals g"
    return X[(u, v)][g] if u < v else X[(v, u)][inv(g)]
seen, dq, tree = {0}, collections.deque([0]), []
while dq:
    u = dq.popleft()
    for v in sorted(nbs[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: cls.append([gain(u, v, ID)])
for d in dirs:
    for x in range(n):
        y = I[add(V[x], d)]; z = I[add(V[y], d)]
        if x < y and x < z:
            for a in range(6):
                for b in range(6): cls.append([-gain(x, y, a), -gain(y, z, b), gain(x, z, comp(b, a))])
TYPES = {}
for P in range(n):
    for R in range(P + 1, n):
        if R in nbs[P]: continue
        Zs = sorted(nbs[P] & nbs[R]); Y = []
        for Z in Zs:
            yv = [new() for _ in range(6)]; exactly_one(yv); Y.append(yv)
            for a in range(6):
                for b in range(6): cls.append([-gain(P, Z, a), -gain(Z, R, b), yv[comp(b, a)]])
        tS, tA, tF = new(), new(), new(); cls.append([tS, tA, tF]); TYPES[(P, R)] = (tS, tA, tF)
        for h in range(6): cls.append([-tS] + [Y[k][h] for k in range(6)])           # S: every element appears
        for t, keep, kill in ((tA, EVEN, ODD), (tF, ODD, EVEN)):
            for k in range(6):
                for h in kill: cls.append([-t, -Y[k][h]])
                for h in keep: cls.append([-t, -Y[k][h]] + [Y[m][h] for m in range(6) if m != k])   # appears >= 2
            for h in keep: cls.append([-t] + [Y[k][h] for k in range(6)])
if mode == 's3':
    R0 = min(R for R in range(1, n) if R not in nbs[0]); cls.append([TYPES[(0, R0)][0]])
with open(out, 'w') as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
import pickle; pickle.dump({'X': X, 'G': G}, open(out + '.map', 'wb'))
print(mode, 'vars', nv, 'clauses', len(cls))
