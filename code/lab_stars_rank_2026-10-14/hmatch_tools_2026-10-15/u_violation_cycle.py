"""Most negative direction of U = 7 Pi - T for a broken structure, read along its twisted cycles (LAB 15/10/2026, A).
Prints lambda_min(U) on the complement of the star vectors and the eigenvector's coordinates in the natural bases
u_y = 1_0y + 1_1y, e_y = 1_0y - 1_1y (l-side), g_z = 1_2z + 1_3z, f_z = 1_2z - 1_3z (m-side), in the order of the twisted
cycles of each side (M_0 vs h(M_1), M_2 vs h(M_3)), plus the cross labels.
usage: python u_violation_cycle.py <json>"""
import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
G = np.zeros((n, n))
for a, b in d["edges"]:
    G[a, b] = G[b, a] = 1
K = np.array([[float(kval(a, b)) for b in S] for a in S])
T = 3 * np.eye(n) - G - K
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Q = np.linalg.svd(Z, full_matrices=True)[0][:, 4:]
U = 7 * PiS - T
w, V = np.linalg.eigh(Q.T @ U @ Q)
x = Q @ V[:, 0]
x = x / np.abs(x).max()
print("lambda_min(U) = %.4f (next %.4f)" % (w[0], w[1]))
hm = {0: 1, 1: 0, 2: 3, 3: 2}
H = lambda y: hm.get(y, y)
L = lambda a, b: idx[frozenset((a, b))]
for (a0, a1) in ((0, 1), (2, 3)):
    M0, M1 = {}, {}
    for (a, Mm) in ((a0, M0), (a1, M1)):
        for i in range(n):
            if a in S[i]:
                for j in range(n):
                    if j != i and a in S[j] and G[i, j]:
                        Mm[[t for t in S[i] if t != a][0]] = [t for t in S[j] if t != a][0]
    M1h = {H(p): H(q) for p, q in M1.items()}
    tw = [y for y in M0 if M0[y] != M1h[y] and y >= 4]
    order, seen = [], set()
    for y in tw:
        if y in seen:
            continue
        cyc, z, use0 = [], y, True
        while True:
            cyc.append(z); seen.add(z)
            z = M0[z] if use0 else M1h[z]
            use0 = not use0
            if z == y:
                break
        order.append(cyc)
    rest = [y for y in range(4, 14) if y not in seen]
    print("side (%d,%d) twisted cycles %s, untwisted outer letters %s" % (a0, a1, order, rest))
    for cyc in order + [rest]:
        ev = ["%+.2f" % (x[L(a0, y)] + x[L(a1, y)]) for y in cyc]
        od = ["%+.2f" % (x[L(a0, y)] - x[L(a1, y)]) for y in cyc]
        print("   letters %s\n     even (sum)  %s\n     odd (diff)  %s" % (cyc, " ".join(ev), " ".join(od)))
print("cross labels 02 03 12 13: %s" % " ".join("%+.2f" % x[L(*p)] for p in ((0, 2), (0, 3), (1, 2), (1, 3))))
