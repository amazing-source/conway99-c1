"""The rank margin of c = 1 in interlacing form (exact).  H = N(l) u Y (56 vertices: letters 2..13, the 24 labels of l,
the 20 far labels {2s},{3s} of m) is an induced subgraph of the srg (14, 3^54, -4^44), so Conway forces
lambda_2 = ... = lambda_12 (A_H) = 3: multiplicity of 3 at least 11.  Omega = l u H (59) forces 14 copies.
For c = 1 positive four-star data sides: exact multiplicity of 3 (rank of A - 3I over Q via two large primes, which is
exact up to the primes dividing all minors; we print both), lambda_2, and where the 3-eigenvectors live.
usage: python c1_margin56.py <distinct_cache.jsonl> <max sides>"""
import itertools
import json
import sys
from collections import Counter

import numpy as np

LAB = [frozenset((a, b)) for a, b in itertools.combinations(range(14), 2) if b != a ^ 1]
S = [l for l in LAB if l & {0, 1, 2, 3}]
XL = [l for l in S if l & {0, 1}]
Y = [l for l in S if not (l & {0, 1})]


def k8(a, b):
    return 3 * len(a & b) + sum(1 for x in a for y in b if y == x ^ 1) - 2


def rank_mod(M, p):
    A = [[int(x) % p for x in row] for row in M]
    r, rows, cols = 0, len(A), len(A[0])
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return r


def relabel(L, EE, side):
    perm = list(range(14))
    if side == 1:
        perm[0], perm[2], perm[1], perm[3] = 2, 0, 3, 1
    f = lambda l: frozenset(perm[x] for x in l)
    return [f(l) for l in L], set(frozenset((f(a), f(b))) for a, b in EE)


def build_H(EE, with_l=False):
    V = [("L", a) for a in range(2, 14)] + XL + Y
    if with_l:
        V = [("P", "v"), ("P", 0), ("P", 1)] + V
    pos = {x: i for i, x in enumerate(V)}
    n = len(V)
    A = np.zeros((n, n), dtype=np.int64)
    def e(x, y):
        A[pos[x], pos[y]] = A[pos[y], pos[x]] = 1
    for a in range(2, 14, 2):
        e(("L", a), ("L", a + 1))
    for w in XL + Y:
        for a in w:
            if a >= 2:
                e(("L", a), w)
    for x, y in itertools.combinations(XL + Y, 2):
        if frozenset((x, y)) in EE:
            e(x, y)
    if with_l:
        e(("P", "v"), ("P", 0)); e(("P", "v"), ("P", 1)); e(("P", 0), ("P", 1))
        for a in range(2, 14):
            e(("P", "v"), ("L", a))
        for w in XL:
            for r in (0, 1):
                if r in w:
                    e(("P", r), w)
    return V, A


def gl_connected(EE):
    V, A = build_H(EE)
    n36 = 12 + 24
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for w in range(n36):
            if A[u, w] and w not in seen:
                seen.add(w); st.append(w)
    deg_ok = all(A[i, :n36].sum() == 3 for i in range(n36))
    return len(seen) == n36, deg_ok


def main():
    mx = int(sys.argv[2])
    P1, P2 = 1000000007, 998244353
    tally56, tally59, tallynu = Counter(), Counter(), Counter()
    lam2s = []
    done = 0
    supp = Counter()
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        for side in (0, 1):
            L, EE = relabel(S0, E0, side)
            conn, degok = gl_connected(EE)
            if not (conn and degok):
                continue
            # positivity of T_S
            idx = {l: i for i, l in enumerate(S)}
            G = np.zeros((44, 44))
            for i, j in itertools.combinations(range(44), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], float)
            T8 = 24 * np.eye(44) - 8 * G - K8
            if np.linalg.eigvalsh(T8 / 8)[0] < -1e-9:
                continue
            nu = 44 - rank_mod(T8.astype(np.int64).tolist(), P1)
            V, A = build_H(EE)
            M = (A - 3 * np.eye(len(V), dtype=np.int64)).tolist()
            m56 = len(V) - min(rank_mod(M, P1), rank_mod(M, P2))
            ev = np.linalg.eigvalsh(A.astype(float))[::-1]
            V59, A59 = build_H(EE, with_l=True)
            M59 = (A59 - 3 * np.eye(len(V59), dtype=np.int64)).tolist()
            m59 = len(V59) - min(rank_mod(M59, P1), rank_mod(M59, P2))
            tally56[m56] += 1
            tally59[m59] += 1
            tallynu[nu] += 1
            lam2s.append(ev[1])
            # where do the 3-eigenvectors live (numerical basis)
            w, U = np.linalg.eigh(A.astype(float))
            B3 = U[:, np.abs(w - 3) < 1e-7]
            if B3.shape[1]:
                mass_N = float((B3[:36, :] ** 2).sum() / B3.shape[1])
                supp[round(mass_N, 1)] += 1
            done += 1
            if done >= mx:
                break
        if done >= mx:
            break
    print("positive c(l) = 1 sides examined:", done)
    print("nu(T_S) (Conway >= 14):", dict(sorted(tallynu.items())))
    print("mult of 3 in A_H, H = N(l) u Y, 56 vertices (Conway >= 11):", dict(sorted(tally56.items())))
    print("mult of 3 in A_Omega, Omega = l u N(l) u Y, 59 vertices (Conway >= 14):", dict(sorted(tally59.items())))
    print("lambda_2(A_H): min %.4f max %.4f" % (min(lam2s), max(lam2s)))
    print("mass of the 3-eigenspace on N(l) (vs Y), per eigenvector, histogram:", dict(sorted(supp.items())))


if __name__ == "__main__":
    main()
