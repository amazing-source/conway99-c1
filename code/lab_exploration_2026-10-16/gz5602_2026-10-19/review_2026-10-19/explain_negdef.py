# Independent rebuild of the known 16-vertex 2K2N matrix (core + Q34 + Q56 + sigma) from first principles and
# explanation of every negative known-pair deficit, in letters.
import gzip, json, sys
from itertools import combinations, permutations, product
cover, bi = sys.argv[1], int(sys.argv[2])
src = json.loads(gzip.decompress(open(cover, 'rb').read()))
core = src['core']; b = bytes.fromhex(src['boundaries_hex'][bi])
LAB = [(s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2)]          # core Q01, Q02
LAB += [(6+s, 8+t) for s, t in product(range(2), repeat=2)]                         # Q34: letters 6,7 / 8,9
LAB += [(10+s, 12+t) for s, t in product(range(2), repeat=2)]                       # Q56: letters 10,11 / 12,13
def adjset(sigma):
    A = set()
    for u, v in core['edges']: A.add(frozenset((u, v)))
    for off in (8, 12):                               # grid: adjacent iff exactly one shared letter
        for i, j in combinations(range(4), 2):
            if len(set(LAB[off+i]) & set(LAB[off+j])) == 1: A.add(frozenset((off+i, off+j)))
    for k, m in enumerate(b):
        for u in range(8):
            if m >> u & 1: A.add(frozenset((u, 8+k)))
    for c in range(4): A.add(frozenset((8+c, 12+sigma[c])))
    return A
print('core edges', [(LAB[u], LAB[v]) for u, v in core['edges']])
print('Q34 core pairs', [[LAB[u] for u in range(8) if m >> u & 1] for m in b[:4]])
print('Q56 core pairs', [[LAB[u] for u in range(8) if m >> u & 1] for m in b[4:]])
tally = {}
for sigma in permutations(range(4)):
    A = adjset(sigma)
    N = [{v for v in range(16) if frozenset((u, v)) in A} for u in range(16)]
    assert [len(x) for x in N] == [4]*8 + [5]*8
    bad = []
    for u, v in combinations(range(16), 2):
        adj = frozenset((u, v)) in A
        sh = len(set(LAB[u]) & set(LAB[v]))
        com = N[u] & N[v]
        if (1 if adj else 2) - sh - len(com) < 0:
            bad.append((LAB[u], LAB[v], 'adj' if adj else 'nonadj', 'shared', sh, 'common', [LAB[w] for w in sorted(com)]))
    tally[sigma] = bad
ok = [s for s, v in tally.items() if not v]
print('sigmas with no violation:', ok)
for s in list(tally)[:3]:
    print('sigma', s, 'first violation:', tally[s][:1])
