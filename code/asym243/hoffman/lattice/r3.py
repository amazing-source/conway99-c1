import sys, glob, os, collections
def rank_mod(M, p):
    M = [[x % p for x in row] for row in M]
    r = 0; rows = len(M); cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r
def load(fn):
    t = open(fn).read().split()
    v, b = int(t[0]), int(t[1]); a = list(map(int, t[2:2 + v * b]))
    return [a[i * b:(i + 1) * b] for i in range(v)]
stats = collections.Counter()
for fn in sorted(glob.glob(os.path.join(sys.argv[1], '*.inst'))):
    Y = load(fn); v, b = len(Y), len(Y[0])
    blocks = [[i for i in range(v) if Y[i][j]] for j in range(b)]
    assert all(len(B) == 4 for B in blocks)
    # Q mod 3 = 1 - |Bi ∩ Bj|
    Q3 = [[1 - len(set(blocks[i]) & set(blocks[j])) for j in range(b)] for i in range(b)]
    r3 = rank_mod(Q3, 3)
    w = rank_mod(Y, 3)
    # hull of W = col space of Y in F_3^22: dim W∩W^perp = w - rank(Y^T Y mod 3)
    h = w - rank_mod([[len(set(blocks[i]) & set(blocks[j])) for j in range(b)] for i in range(b)], 3)
    k = rank_mod([[Y[i][j] - 1 for j in range(b)] for i in range(v)], 3)
    stats[(os.path.basename(fn).rstrip('0123456789.inst') or 'x', w, h, k, r3)] += 1
for key, n in sorted(stats.items()): print(key, n)
