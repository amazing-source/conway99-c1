"""rel(A) = dim of kernel profiles on Y supported on the m-blocks of the outer lines in A (both sides l and m),
plus the parts of H_l and H_m as sets of lines (index 0..4 outer lines, 'm'/'l' the block line).
usage: python rel_table.py <json>"""
import json, sys, itertools
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
LINES = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
def rk(M):
    if len(M) == 0: return 0
    w = np.linalg.eigvalsh(M); return int(np.sum(w > 1e-7))
f = sys.argv[1]
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
G = np.zeros((n, n))
for a, b in d["edges"]: G[a, b] = G[b, a] = 1
K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
def parts(a, b, other):
    # lines: outer 0..4 and the other block line; union-find via sigma_a, sigma_b, tau_a edges + mates
    letters = [y for y in range(14) if y not in (a, b)]
    par = {y: y for y in letters}
    def fd(x):
        while par[x] != x: x = par[x]
        return x
    def un(x, y): par[fd(x)] = fd(y)
    for y in letters: un(y, y ^ 1)
    for s in (a, b):
        for y in letters:
            for z in letters:
                if z != y and G[idx[frozenset((s, y))], idx[frozenset((s, z))]]: un(y, z)
    for y in letters:
        for z in letters:
            if G[idx[frozenset((a, y))], idx[frozenset((b, z))]]: un(y, z)
    name = lambda y: other if y in (0, 1, 2, 3) else str(LINES.index((y & ~1, y | 1)))
    groups = {}
    for y in letters[::1]:
        groups.setdefault(fd(y), set()).add(name(y))
    return sorted(sorted(g) for g in groups.values())
print(f, "parts H_l:", parts(0, 1, 'm'), " parts H_m:", parts(2, 3, 'l'))
for side, (a, b) in (("m-blocks over X_l", (2, 3)), ("l-blocks over X_m", (0, 1))):
    base_stars = {0, 1} if a == 2 else {2, 3}
    X = [i for i in range(n) if S[i] & base_stars]
    base = rk(T[np.ix_(X, X)])
    blocks = [[idx[frozenset((s, y))] for s in (a, b) for y in ln] for ln in LINES]
    out = []
    for k in range(1, 6):
        for A in itertools.combinations(range(5), k):
            cur = X + sum((blocks[j] for j in A), [])
            g = rk(T[np.ix_(cur, cur)]) - base
            out.append("%s:%d" % ("".join(map(str, A)), 4 * k - g))
    print("  rel (%s): %s" % (side, " ".join(out)))
