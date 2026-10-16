"""Non-liftable mod-7 kernel vectors of 8T on a four-star block (exploration, LAB 16/10/2026).
ker_7 = {g in F_7^44 : 8T_S g = 0 mod 7};  N_7 = reduction mod 7 of the saturated integral kernel of T_S.
The quotient ker_7 / N_7 has dimension rank_Q - rank_F7 (the 7-adic drop).  We print a reduced basis of a complement,
with supports in label notation, to see what a drop looks like (grid blocks drop by up to 5).
usage: python f7_kernel_look.py <dir to search> [want_rank_Q want_rank_F7] | --file <json>"""
import itertools
import json
import os
import sys

import numpy as np
import sympy as sp

MATE = lambda i: i ^ 1


def t8(S, E):
    n = len(S)
    M = np.zeros((n, n), dtype=np.int64)
    for i, a in enumerate(S):
        for j, b in enumerate(S):
            s = len(a & b)
            m = sum(1 for p in a for q in b if q == MATE(p))
            M[i, j] = (24 if i == j else 0) - 8 * (1 if frozenset((a, b)) in E else 0) - 3 * s - m + 2
    return M


def rref_mod(M, p):
    A = [[int(x) % p for x in row] for row in M]
    rows, cols = len(A), len(A[0])
    piv = []
    r = 0
    for c in range(cols):
        k = next((i for i in range(r, rows) if A[i][c]), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    return A[:r], piv


def null_mod(M, p):
    R, piv = rref_mod(M, p)
    cols = len(M[0])
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        g = [0] * cols
        g[f] = 1
        for i, c in enumerate(piv):
            g[c] = (-R[i][f]) % p
        basis.append(g)
    return basis


def load(path):
    d = json.load(open(path))
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
    S = [l for l in L if l & {0, 1, 2, 3}]
    return S, E


def pick(root, wq, w7):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".json"):
                continue
            try:
                S, E = load(os.path.join(dp, f))
            except Exception:
                continue
            if len(S) != 44:
                continue
            M = t8(S, E)
            ev = np.linalg.eigvalsh(M.astype(float))
            if ev[0] < -1e-6 or int(np.sum(ev > 1e-6)) != wq:
                continue
            if len(rref_mod(M.tolist(), 7)[0]) == w7:
                return os.path.join(dp, f)
    return None


if "--file" in sys.argv:
    path = sys.argv[sys.argv.index("--file") + 1]
else:
    wq, w7 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (30, 25)
    path = pick(sys.argv[1], wq, w7)
print("block:", path)
S, E = load(path)
M = t8(S, E)
k7 = null_mod(M.tolist(), 7)
ker = sp.Matrix(M.tolist()).nullspace()
Kint = []
for v in ker:
    den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = sp.igcd(g, x)
    Kint.append([x // g for x in w])
# saturate at 7: while the reduction mod 7 is dependent, divide a suitable combination by 7
changed = True
while changed:
    changed = False
    R, piv = rref_mod(Kint, 7) if Kint else ([], [])
    if len(R) < len(Kint):
        # find a combination sum c_i K_i = 0 mod 7 with some c_i != 0
        Mt = [[Kint[i][j] for i in range(len(Kint))] for j in range(44)]
        rel = null_mod(Mt, 7)
        c = rel[0]
        vec = [sum((c[i] if c[i] <= 3 else c[i] - 7) * Kint[i][j] for i in range(len(Kint))) for j in range(44)]
        assert all(x % 7 == 0 for x in vec)
        vec = [x // 7 for x in vec]
        i0 = next(i for i in range(len(c)) if c[i])
        Kint[i0] = vec
        changed = True
print("rank_Q %d, rank_F7 %d, dim ker_7 %d, dim N mod 7 %d" % (44 - len(ker), 44 - len(k7), len(k7),
                                                               len(rref_mod(Kint, 7)[0])))
# complement of N_7 in ker_7, reduced
basisN = rref_mod(Kint, 7)[0]
comp = []
for g in k7:
    if len(rref_mod(basisN + comp + [g], 7)[0]) > len(basisN) + len(comp):
        comp.append(g)
# reduce the complement modulo N_7 to small support (greedy: subtract N_7 combinations to clear entries)
Rc, pivc = rref_mod(basisN + comp, 7)
names = ["".join(str(t) for t in sorted(l)) for l in S]
print("complement directions (rref of N_7 + complement, rows beyond N_7 shown):")
Rn, pivn = rref_mod(basisN, 7)
full, pivf = rref_mod(basisN + comp, 7)
extra = [row for row, pcol in zip(full, pivf) if pcol not in pivn]
for row in extra:
    supp = [(names[j], row[j] if row[j] <= 3 else row[j] - 7) for j in range(44) if row[j]]
    print("   support %d: %s" % (len(supp), supp))
