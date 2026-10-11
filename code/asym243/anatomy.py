import numpy as np, itertools, collections
from lib243 import load_edges
from golay import golay_coords
G, H, allsy = golay_coords()
idx = {s: i for i, s in enumerate(allsy)}
A = load_edges("bvls243.edges"); B = load_edges("twin243_switched.edges"); D = B - A
hs = [np.array(H[:, p] % 3) for p in range(11)]
# coset leader of every syndrome: (support tuple, values)
leader = {}
for s in allsy:
    leader[s] = None
leader[(0,)*5] = ()
for p in range(11):
    for a in (1, 2):
        leader[tuple((a * hs[p]) % 3)] = ((p, a),)
for p, q in itertools.combinations(range(11), 2):
    for a in (1, 2):
        for b in (1, 2):
            leader[tuple((a * hs[p] + b * hs[q]) % 3)] = ((p, a), (q, b))
assert all(v is not None for v in leader.values())
T = [allsy[i] for i in (0, 1, 2)]
print("T =", [leader[t] for t in T])
line_dir = [p for p in range(11) if tuple(hs[p]) in T][0]
print("line direction h_%d" % line_dir)
stats = collections.Counter()
for wi in range(243):
    if not D[wi].any(): continue
    w = np.array(allsy[wi]); lw = leader[allsy[wi]]
    rem = [leader[tuple((np.array(allsy[j]) - w) % 3)] for j in np.nonzero(D[wi] == -1)[0]]
    add = [leader[tuple((np.array(allsy[j]) - w) % 3)] for j in np.nonzero(D[wi] == 1)[0]]
    # classify removed directions relative to support of w and line direction
    sw = {p for p, _ in lw}
    def cls_rem(l):
        (p, a), = l
        return 'line' if p == line_dir else ('own' if p in sw else 'other')
    def cls_add(l):
        ps = {p for p, _ in l}
        return (len(ps & sw), line_dir in ps)
    stats[(tuple(sorted(collections.Counter(map(cls_rem, rem)).items())),
           tuple(sorted(collections.Counter(map(cls_add, add)).items())))] += 1
for k, v in stats.items(): print(v, k)
# first example in detail
for wi in range(243):
    if D[wi].any():
        w = np.array(allsy[wi]); print("w leader", leader[allsy[wi]])
        print(" kept far nbrs:", sorted(leader[tuple((np.array(allsy[j]) - w) % 3)] for j in np.nonzero((A[wi] == 1) & (D[wi] == 0))[0]))
        print(" removed:", sorted(leader[tuple((np.array(allsy[j]) - w) % 3)] for j in np.nonzero(D[wi] == -1)[0]))
        print(" added:", sorted(leader[tuple((np.array(allsy[j]) - w) % 3)] for j in np.nonzero(D[wi] == 1)[0]))
        break
