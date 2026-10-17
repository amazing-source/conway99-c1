"""B, step 1 (estimate): how many line types (mu_0, mu_1, sigma) on the 12 letters {2..13} survive
  (f1) the local axioms inside N[l] (cp6 on the 24 labels of L_0 u L_1: exact counts for letters 0, 1, caps otherwise,
       pair caps common + shared + adjacent <= 2),
  (f2) c(l) = 1, (f3) T_{L(l)} >= 0 (24 x 24), (f4) A_{N[l]} >= -4 (39 vertices)?
Random sampling of (mu_0, mu_1, sigma); prints pass rates.  usage: python c1_linetypes_sample.py <samples> <seed>"""
import itertools, random, sys
import numpy as np
MATE = lambda i: i ^ 1
LET = list(range(2, 14))
def rand_matching(rng):
    p = LET[:]; rng.shuffle(p)
    m = {}
    for i in range(0, 12, 2):
        m[p[i]], m[p[i + 1]] = p[i + 1], p[i]
    return m
def build(mu0, mu1, sig):
    labs = [frozenset((0, a)) for a in LET] + [frozenset((1, a)) for a in LET]
    idx = {l: i for i, l in enumerate(labs)}
    G = np.zeros((24, 24), dtype=int)
    for a in LET:
        G[idx[frozenset((0, a))], idx[frozenset((0, mu0[a]))]] = 1
        G[idx[frozenset((1, a))], idx[frozenset((1, mu1[a]))]] = 1
        i, j = idx[frozenset((0, a))], idx[frozenset((1, sig[a]))]
        G[i, j] = G[j, i] = 1
    return labs, idx, G
def axioms(labs, G):
    # letter counts
    for i, u in enumerate(labs):
        for y in range(14):
            cnt = sum(G[i, j] for j, w in enumerate(labs) if y in w and j != i)
            c = 1 if (y in u or MATE(y) in u) else 2
            if y in (0, 1):
                if cnt != c: return False
            elif cnt > c: return False
    # pair caps
    G2 = G @ G
    for i, j in itertools.combinations(range(24), 2):
        if G2[i, j] + len(labs[i] & labs[j]) + G[i, j] > 2: return False
    return True
def connected(mu0, mu1, sig):
    adj = {a: {MATE(a), mu0[a], mu1[a], sig[a]} | {b for b in LET if sig[b] == a} for a in LET}
    seen, st = {2}, [2]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == 12
def tblock(labs, G):
    M = np.zeros((24, 24))
    for i, a in enumerate(labs):
        for j, b in enumerate(labs):
            s = len(a & b); m = sum(1 for p in a for q in b if q == MATE(p))
            M[i, j] = (24 if i == j else 0) - 8 * G[i, j] - 3 * s - m + 2
    return M
def ball(labs, G):
    # N[l] = v, 0, 1, letters 2..13, 24 labels
    V = ["v", 0, 1] + LET + labs
    n = len(V); A = np.zeros((n, n))
    pos = {x: k for k, x in enumerate(V)}
    def e(x, y): A[pos[x], pos[y]] = A[pos[y], pos[x]] = 1
    e("v", 0); e("v", 1); e(0, 1)
    for a in LET:
        e("v", a)
        if a < MATE(a): e(a, MATE(a))
        e(a, frozenset((0, a))); e(a, frozenset((1, a)))
        e(0, frozenset((0, a))); e(1, frozenset((1, a)))
    off = 3 + 12
    A[off:, off:] = G
    return A
ns, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
cnt = {"sampled": 0, "f1 axioms": 0, "f2 c=1": 0, "f3 T>=0": 0, "f4 A>=-4": 0}
for _ in range(ns):
    mu0, mu1 = rand_matching(rng), rand_matching(rng)
    perm = LET[:]; rng.shuffle(perm); sig = dict(zip(LET, perm))
    cnt["sampled"] += 1
    labs, idx, G = build(mu0, mu1, sig)
    if not axioms(labs, G): continue
    cnt["f1 axioms"] += 1
    if not connected(mu0, mu1, sig): continue
    cnt["f2 c=1"] += 1
    if np.linalg.eigvalsh(tblock(labs, G))[0] < -1e-9: continue
    cnt["f3 T>=0"] += 1
    if np.linalg.eigvalsh(ball(labs, G))[0] < -4 - 1e-9: continue
    cnt["f4 A>=-4"] += 1
print(cnt)
tot = 10395 ** 2 * 479001600
print("raw space %.3g ; estimated survivors (raw) %.3g ; divided by the symmetry ~46080*2*6: %.3g" % (
    tot, tot * cnt["f4 A>=-4"] / ns, tot * cnt["f4 A>=-4"] / ns / (46080 * 12)))
