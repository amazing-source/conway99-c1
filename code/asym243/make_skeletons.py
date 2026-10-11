"""New skeleton types from a random Latin square L of order 9 (cells: part0 = rows 0..8, part1 = columns 9..17,
part2 = symbols 18..26).  Checks the pattern law: each cross pair in exactly one full triangle or exactly three
3-triangles, never both."""
import random, itertools, pickle, collections, sys
def random_latin(n, seed):
    rnd = random.Random(seed)
    # random latin square by Jacobson–Matthews would be ideal; use row/col/symbol permutations of a cyclic square
    # composed with random isotopy and a few random 'cycle switches' to destroy structure
    L = [[(r + c) % n for c in range(n)] for r in range(n)]
    for _ in range(2000):                      # random intercalate-free switching via 2-row cycle swaps
        r1, r2 = rnd.sample(range(n), 2); c0 = rnd.randrange(n)
        cyc = [c0]; c = c0
        while True:
            # column where row r1 has the symbol that row r2 has at c
            c = L[r1].index(L[r2][c])
            if c == c0: break
            cyc.append(c)
        for c in cyc: L[r1][c], L[r2][c] = L[r2][c], L[r1][c]
    pr, pc, ps = (rnd.sample(range(n), n) for _ in range(3))
    return [[ps[L[pr[r]][pc[c]]] for c in range(n)] for r in range(n)]
def check(skel):
    cov = collections.defaultdict(list)
    for (i, j, k), v in skel.items():
        for p in ((i, j), (i, k), (j, k)): cov[p].append(v)
    pats = collections.Counter(tuple(sorted(v, reverse=True)) for v in cov.values())
    return len(cov), dict(pats)
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
L = random_latin(9, seed)
assert all(len(set(row)) == 9 for row in L) and all(len({L[r][c] for r in range(9)}) == 9 for c in range(9))
R = {0, 1, 2}
s5481 = {}
for r in range(9):
    for c in range(9):
        if L[r][c] not in R: s5481[(r, 9 + c, 18 + L[r][c])] = 9
        else:
            for s in R: s5481[(r, 9 + c, 18 + s)] = 3
s0 = {}
for r in range(9):
    for c in range(9):
        for d in (0, 3, 6): s0[(r, 9 + c, 18 + (L[r][c] + d) % 9)] = 3
print("Latin square seed", seed)
print("type (54,81):", check(s5481), " type (0,243):", check(s0))
pickle.dump(s5481, open(f"skel_54_81_s{seed}.pkl", "wb")); pickle.dump(s0, open(f"skel_0_243_s{seed}.pkl", "wb"))
