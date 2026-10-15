"""Census of twists, pure rows and kernel dimensions over a set of structures (LAB 15/10/2026, mechanism A).
For each structure: nu (exact), dim N+ (exact h-even kernel), dim N_h (exact: N n ker Delta), which halves are broken,
the twisted alternating cycles of each side (lengths), and the number of PURE twisted rows per side (rows {a0, y}, y on a
twisted cycle, whose Delta-row is supported in the own star L_a0).  Prints a histogram of the tuples.
usage: python twist_census.py <json> [...]"""
import json, sys
from collections import Counter
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int


def rank(rows):
    B = [[Fr(x) for x in r] for r in rows]
    rk = 0
    if not B:
        return 0
    for c in range(len(B[0])):
        p = next((i for i in range(rk, len(B)) if B[i][c] != 0), None)
        if p is None:
            continue
        B[rk], B[p] = B[p], B[rk]
        for i in range(len(B)):
            if i != rk and B[i][c] != 0:
                f = B[i][c] / B[rk][c]
                B[i] = [a - f * b for a, b in zip(B[i], B[rk])]
        rk += 1
    return rk


hm = {0: 1, 1: 0, 2: 3, 3: 2}
H = lambda y: hm.get(y, y)
tab = Counter()
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    G = [[1 if frozenset((S[a], S[b])) in E else 0 for b in range(n)] for a in range(n)]
    hp = [idx[frozenset(H(y) for y in s)] for s in S]
    M8 = [[(24 if a == b else 0) - 8 * G[a][b] - int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
    N = nullspace_int(M8)
    nu = len(N)
    D = [[G[a][b] - G[hp[a]][hp[b]] for b in range(n)] for a in range(n)]
    # N_h = N n ker Delta: rank of Delta restricted to N
    DN = [[sum(D[a][k] * v[k] for k in range(n)) for a in range(n)] for v in N]
    nh = nu - rank(DN) if N else 0
    # N+ : even kernel vectors = N n {h-even}; dim = nu - rank of the h-odd parts
    odd = [[v[i] - v[hp[i]] for i in range(n)] for v in N]
    nplus_in_N = nu - rank(odd)
    halves, cyc_l, pure = [], [], []
    for (a0, a1) in ((0, 1), (2, 3)):
        M0, M1 = {}, {}
        for (a, Mm) in ((a0, M0), (a1, M1)):
            for i in range(n):
                if a in S[i]:
                    for j in range(n):
                        if j != i and a in S[j] and G[i][j]:
                            Mm[[t for t in S[i] if t != a][0]] = [t for t in S[j] if t != a][0]
        M1h = {H(x): H(y) for x, y in M1.items()}
        tw = [y for y in M0 if M0[y] != M1h[y]]
        halves.append(bool(tw))
        seen, lens = set(), []
        for y in tw:
            if y in seen:
                continue
            L, x, use0 = 0, y, True
            while True:
                seen.add(x)
                L += 1
                x = M0[x] if use0 else M1h[x]
                use0 = not use0
                if x == y:
                    break
            lens.append(L)
        cyc_l.append(tuple(sorted(lens)))
        npure = 0
        for y in tw:
            r = idx[frozenset((a0, y))]
            if all(D[r][j] == 0 for j in range(n) if a0 not in S[j]):
                npure += 1
        pure.append(npure)
    key = (nu, nh, nplus_in_N, "PSD" if d.get("psd") else "-", "l" if halves[0] else ".", "m" if halves[1] else ".",
           cyc_l[0], cyc_l[1], pure[0], pure[1])
    tab[key] += 1
print("(nu, dim N_h, dim N+ (even kernel), PSD, l-half broken, m-half broken, l-cycle lengths, m-cycle lengths, "
      "pure l-rows, pure m-rows): count")
for k, v in sorted(tab.items(), key=lambda kv: (-kv[0][0], -kv[1])):
    print("  ", k, v)
