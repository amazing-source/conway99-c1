"""Type-S normalisation at the pair (0,R0) for the full model (s3full.py CNF): in the BFS-tree gauge the path through
the BFS parent of R0 has product id; the other 5 paths carry the 5 non-identity elements of S3 (120 bijections).
Global conjugation (constant gauge) preserves the tree gauge: classes = orbits of the 120 bijections under Inn(S3).
Writes one units file per class.  python3 s3classes.py"""
import itertools, sys, collections, pickle
sys.argv_saved = list(sys.argv); sys.argv = ['x']
exec(open('s3grid.py').read().split('if __name__')[0]); sys.argv = sys.argv_saved
G = list(itertools.permutations(range(3))); GI = {g: i for i, g in enumerate(G)}
comp = lambda b, a: GI[tuple(G[b][G[a][i]] for i in range(3))]
inv = lambda a: GI[tuple(sorted(range(3), key=lambda i: G[a][i]))]
ID = GI[(0, 1, 2)]
seen, dq, parent = {0}, collections.deque([0]), {}
while dq:
    u = dq.popleft()
    for v in sorted(nbs[u]):
        if v not in seen: seen.add(v); dq.append(v); parent[v] = u
R0 = min(R for R in range(1, n) if R not in nbs[0]); Zs = sorted(nbs[0] & nbs[R0]); zp = parent[R0]
assert zp in Zs and parent[zp] == 0
others = [Z for Z in Zs if Z != zp]; nonid = [g for g in range(6) if g != ID]
reps = {}
for perm in itertools.permutations(nonid):
    key = min(tuple(comp(comp(h, g), inv(h)) for g in perm) for h in range(6))
    reps.setdefault(key, perm)
X = pickle.load(open('full_s3.cnf.map', 'rb'))['X']
def gain_lit(u, v, g): return X[(u, v)][g] if u < v else X[(v, u)][inv(g)]
for c, (key, perm) in enumerate(sorted(reps.items())):
    with open(f'cls{c:02d}.units', 'w') as f:
        for Z, g in zip(others, perm): f.write(f"{gain_lit(Z, R0, g)} 0\n")   # gain Z->R0 = path product (edges at 0 are id)
print('R0', R0, 'parent', zp, 'classes', len(reps))
