"""Letter shadow of the 7-adic drop (exploration, LAB 16/10/2026).
8T_S is the Schur complement (x 8) of 3I - A_W, W = {v} + N(v) + S (59 vertices), with respect to the 15x15 block on
{v} + N(v), which is invertible over Z_(7).  So g in ker_7(8T_S) <=> the extension x = (x_v, x_N, g), with
x_{v,N} = X^{-1} (0, B_S g), satisfies A_W x = 3x (mod 7): a mod-7 eigenvector of the 59-vertex ball, eigenvalue 3 = -4.
For each block we print, for ker_7, N_7 and the drop: the letter values x_N (and x_v), to see whether the drop is
visible on the 15 vertices {v} + N(v).
usage: python f7_letters.py <block json> [<block json> ...]"""
import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f7_classform import t8, rref_mod, null_mod, int_kernel, saturate7, MATE  # noqa: E402
from f7_kernel_look import load  # noqa: E402


def inv_mod(M, p):
    n = len(M)
    A = [[int(x) % p for x in r] + [1 if i == j else 0 for j in range(n)] for i, r in enumerate(M)]
    R, piv = rref_mod(A, p)
    assert piv[:n] == list(range(n))
    return [r[n:] for r in R[:n]]


def letter_ext(S, g):
    """x on {v} + 14 letters: solve X (x_v, x_N) = (0, B g) with X = [[3, -1^T], [-1, 3I - M]] (mod 7)"""
    X = [[0] * 15 for _ in range(15)]
    X[0][0] = 3
    for r in range(14):
        X[0][1 + r] = -1
        X[1 + r][0] = -1
        X[1 + r][1 + r] = 3
        X[1 + r][1 + MATE(r)] = -1
    Xi = inv_mod(X, 7)
    rhs = [0] + [sum(g[i] for i, l in enumerate(S) if r in l) % 7 for r in range(14)]
    x = [sum(Xi[i][j] * rhs[j] for j in range(15)) % 7 for i in range(15)]
    return x


def bal(v):
    return [x if x <= 3 else x - 7 for x in v]


for path in sys.argv[1:]:
    S, E = load(path)
    M = t8(S, E)
    k7 = null_mod(M.tolist(), 7)
    N7 = rref_mod(saturate7(int_kernel(M.tolist())), 7)[0]
    nu = len(N7)
    print("block %s: nu %d, dim ker_7 %d, drop %d" % (path.replace("\\", "/").split("/")[-1], nu, len(k7),
                                                       len(k7) - nu))
    xl_N = [letter_ext(S, g) for g in N7]
    xl_K = [letter_ext(S, g) for g in k7]
    rN = len(rref_mod(xl_N, 7)[0]) if xl_N else 0
    rK = len(rref_mod(xl_K, 7)[0]) if xl_K else 0
    print("  dim of letter shadows: N_7 -> %d, ker_7 -> %d" % (rN, rK))
    print("  letter shadow of N_7 (rref, order v,0..13):")
    for r in rref_mod(xl_N, 7)[0]:
        print("    ", bal(r))
    # complement directions of ker_7 over N_7, reduced against N_7
    comp = []
    for g in k7:
        if len(rref_mod(N7 + comp + [g], 7)[0]) > len(N7) + len(comp):
            comp.append(g)
    full, pivf = rref_mod(N7 + comp, 7)
    Rn, pivn = rref_mod(N7, 7)
    extra = [row for row, pc in zip(full, pivf) if pc not in pivn]
    print("  letter shadow of the drop directions:")
    for g in extra:
        print("    ", bal(letter_ext(S, g)))
