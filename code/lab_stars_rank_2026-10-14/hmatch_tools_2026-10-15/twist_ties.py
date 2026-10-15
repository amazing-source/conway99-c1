"""Twisted cycles and the even kernel (LAB 15/10/2026, mechanism A, exact).

For a structure: N+ = h-even kernel vectors (exact, coordinates = values on the 22 h-orbits of labels).  For each side
(l: star letters 0,1, twist = M_0 versus h(M_1) on the letters other than 0,1; m: M_2 versus h(M_3)) list the
alternating cycles of the symmetric difference, and for each cycle report the dimension of the profile of N+ on the
corresponding orbits {0y, 1h(y)} (resp. {2y, 3h(y)}), the predicted ties 'value at y = value at y'' for letters at the same
parity on the cycle, and whether they hold.  Also: every row r of Delta = Gamma - h Gamma h gives sum_j Delta(r, j) n(j) = 0
for n in N+; we print, per twisted letter y, the support of Delta on the row {a, y} split into star blocks.
usage: python twist_ties.py <json>"""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int

d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
G = [[1 if frozenset((S[a], S[b])) in E else 0 for b in range(n)] for a in range(n)]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
H = lambda y: hm.get(y, y)
hp = [idx[frozenset(H(y) for y in s)] for s in S]
reps = sorted({min(i, hp[i]) for i in range(n)})
orb = {i: reps.index(min(i, hp[i])) for i in range(n)}
K8 = [[int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
M8 = [[(24 if a == b else 0) - 8 * G[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
# even kernel: x = sum_O y_O (1_r + 1_{hr}); T x = 0  <=>  M8 Q y = 0 with Q the 44 x 22 orbit incidence
Q = [[1 if orb[i] == o else 0 for o in range(22)] for i in range(n)]
MQ = [[sum(M8[i][k] * Q[k][o] for k in range(n)) for o in range(22)] for i in range(n)]
# nullspace of the 44 x 22 matrix MQ
A = [[Fr(x) for x in row] for row in MQ]
piv, r = [], 0
for c in range(22):
    p = next((i for i in range(r, n) if A[i][c] != 0), None)
    if p is None:
        continue
    A[r], A[p] = A[p], A[r]
    inv = 1 / A[r][c]
    A[r] = [x * inv for x in A[r]]
    for i in range(n):
        if i != r and A[i][c] != 0:
            f = A[i][c]
            A[i] = [a - f * b for a, b in zip(A[i], A[r])]
    piv.append(c); r += 1
Nplus = []
for f in [c for c in range(22) if c not in piv]:
    v = [Fr(0)] * 22; v[f] = Fr(1)
    for i, c in enumerate(piv):
        v[c] = -A[i][f]
    Nplus.append(v)
print("dim N+ (h-even kernel) = %d" % len(Nplus))


def matching(a):
    res = {}
    for i in range(n):
        if a in S[i]:
            for j in range(n):
                if j != i and a in S[j] and G[i][j]:
                    res[[t for t in S[i] if t != a][0]] = [t for t in S[j] if t != a][0]
    return res


def rank(rows):
    B = [r_[:] for r_ in rows]
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


for (a0, a1) in ((0, 1), (2, 3)):
    M0, M1 = matching(a0), matching(a1)
    M1h = {H(x): H(y) for x, y in M1.items()}          # h(M_1) as a matching on the letters other than a0, a1
    letters = sorted(M0)
    seen = set()
    cycles = []
    for y in letters:
        if y in seen or M0[y] == M1h[y]:
            continue
        cyc = [y]
        seen.add(y)
        x, use0 = y, True
        while True:
            x = M0[x] if use0 else M1h[x]
            use0 = not use0
            if x == y:
                break
            cyc.append(x)
            seen.add(x)
        cycles.append(cyc)
    print("side (%d,%d): twisted alternating cycles (M_%d vs h(M_%d)): %s" % (a0, a1, a0, a1, cycles))
    for cyc in cycles:
        os_ = [orb[idx[frozenset((a0, y))]] for y in cyc]
        prof = [[v[o] for o in os_] for v in Nplus]
        dimp = rank([list(col) for col in zip(*prof)]) if prof else 0
        ties_odd = all(v[os_[0]] == v[os_[k]] for v in Nplus for k in range(0, len(cyc), 2))
        ties_even = all(v[os_[1]] == v[os_[k]] for v in Nplus for k in range(1, len(cyc), 2))
        print("   cycle %s: profile dimension of N+ on its %d orbits = %d ; ties at odd positions %s, at even positions %s"
              % (cyc, len(cyc), dimp, ties_odd, ties_even))
        for y in cyc:
            row = idx[frozenset((a0, y))]
            dl = {}
            for j in range(n):
                dv = G[row][j] - G[hp[row]][hp[j]]
                if dv:
                    dl.setdefault("".join(map(str, sorted(S[j] & {0, 1, 2, 3}))) or "-", []).append(
                        ("+" if dv > 0 else "-") + "".join(map(str, sorted(S[j]))))
            print("      Delta row {%d,%d}: %s" % (a0, y, dl))
