"""Synthetic test of the local order-2 rules (LAB, NOTE_ORDRE2_7ADIQUE §2, 20/10/2026).

Model: L = span(B) in Z^60, rank 8, Jordan type U_m + 7 U''_rho at 7 (m = 8 - rho), with the class of U_m chosen
(m = 2: 'aniso' = anisotropic plane, chi(det) = +1; 'hyper' = hyperbolic plane, chi(det) = -1).  H = 7 Pi, Pi the
projector on L (x) Q.  Every principal block H_XX is the Gram matrix of vectors of M = U''_rho + U_m(7).
Predictions (proof in the note):
  (P7) k = rho + 1 coordinates with rank_7 H_XX = rho and real rank rho + 1:  e = v_7(det H_XX) is ODD if U_m is an
       anisotropic plane (m = 2), unconstrained otherwise;
  (P8) k = 8 coordinates with rank_7 = rho and v_7(det) = m (generic second layer):
       chi(det H_XX / 7^m) = chi(det U'') chi(det U_m), constant over all such X.
usage: python o2_parity.py <seed> <rho> <aniso|hyper|any> <samples>"""
import json
import random
import sys
from fractions import Fraction

import numpy as np
import sympy as sp

P = 7


def rank_mod(M):
    A = [[int(v) % P for v in row] for row in M]
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        piv = [i for i in range(r, rows) if A[i][c] % P]
        if not piv:
            continue
        i = piv[0]
        A[r], A[i] = A[i], A[r]
        iv = pow(A[r][c], -1, P)
        A[r] = [v * iv % P for v in A[r]]
        for i2 in range(rows):
            if i2 != r and A[i2][c]:
                f = A[i2][c]
                A[i2] = [(a - f * b) % P for a, b in zip(A[i2], A[r])]
        r += 1
    return r


def kernel_mod(M):
    A = [[int(v) % P for v in row] for row in M]
    rows, cols = len(A), len(A[0])
    pivcols, r = [], 0
    for c in range(cols):
        piv = [i for i in range(r, rows) if A[i][c] % P]
        if not piv:
            continue
        i = piv[0]
        A[r], A[i] = A[i], A[r]
        iv = pow(A[r][c], -1, P)
        A[r] = [v * iv % P for v in A[r]]
        for i2 in range(rows):
            if i2 != r and A[i2][c]:
                f = A[i2][c]
                A[i2] = [(a - f * b) % P for a, b in zip(A[i2], A[r])]
        pivcols.append(c)
        r += 1
    basis = []
    for fc in [c for c in range(cols) if c not in pivcols]:
        y = [0] * cols
        y[fc] = 1
        for i, pc in enumerate(pivcols):
            y[pc] = (-A[i][fc]) % P
        basis.append(np.array(y, dtype=np.int64))
    return basis


def chi(u):
    u %= P
    return 0 if u == 0 else (1 if pow(u, 3, P) == 1 else -1)


def v7(x):
    x = Fraction(x)
    if x == 0:
        return None
    v, a, b = 0, x.numerator, x.denominator
    while a % P == 0:
        a //= P; v += 1
    while b % P == 0:
        b //= P; v -= 1
    return v


def unit7(x):
    """x / 7^v7(x) mod 7"""
    x = Fraction(x)
    a, b = x.numerator, x.denominator
    while a % P == 0:
        a //= P
    while b % P == 0:
        b //= P
    return a * pow(b, -1, P) % P


def build(rng, rho, cls):
    n, m = 60, 8 - rho
    while True:
        B0 = np.array([[rng.randrange(-3, 4) for _ in range(m)] for _ in range(n)], dtype=np.int64)
        G0 = (B0.T @ B0)
        if rank_mod(G0) < m:
            continue
        d = chi(int(sp.Matrix(G0.tolist()).det()))
        if cls == "aniso" and d != 1:
            continue
        if cls == "hyper" and d != -1:
            continue
        break
    perp = kernel_mod(B0.T)
    cols = []
    while len(cols) < rho:
        v = sum(rng.randrange(P) * b for b in perp) % P
        if not v.any() or int(v @ v) % P or any(int(v @ c) % P for c in cols):
            continue
        if rank_mod(np.array(cols + [v])) < len(cols) + 1:
            continue
        cols.append(v)
    B1 = np.array(cols, dtype=np.int64).T
    B1 = np.where(B1 > 3, B1 - 7, B1)
    B = np.concatenate([B0, B1], axis=1)
    G = sp.Matrix(B.tolist()).T * sp.Matrix(B.tolist())
    return B, G, chi(int(sp.Matrix(G0.tolist()).det()))


def main():
    seed, rho, cls, samples = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    rng = random.Random(seed)
    while True:
        B, G, chi_m = build(rng, rho, cls)
        if sp.multiplicity(7, G.det()) == rho:
            break
    Bs = sp.Matrix(B.tolist())
    Hs = 7 * Bs * G.inv() * Bs.T
    H = [[Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1])) for v in Hs.row(i)] for i in range(60)]
    m = 8 - rho
    par7 = {}
    chi8 = {}
    n7 = n8 = 0
    for _ in range(samples):
        for k in (rho + 1, 8):
            X = rng.sample(range(60), k)
            Hx = sp.Matrix([[H[i][j] for j in X] for i in X])
            Hm = [[(v.numerator * pow(v.denominator, -1, P)) % P for v in (H[i][j] for j in X)] for i in X]
            if rank_mod(Hm) != rho:
                continue
            det = Hx.det()
            if det == 0:
                continue
            det = Fraction(int(sp.fraction(det)[0]), int(sp.fraction(det)[1]))
            e = v7(det)
            if k == rho + 1:
                n7 += 1
                par7[e] = par7.get(e, 0) + 1
            if k == 8 and e == m:
                n8 += 1
                c = chi(unit7(det))
                chi8[c] = chi8.get(c, 0) + 1
    print(json.dumps({"seed": seed, "rho": rho, "class U_m": cls, "chi(det U_m)": chi_m, "v7(det G)": rho,
                      "k=rho+1: v7(det) histogram (full first layer)": {str(a): b for a, b in sorted(par7.items())},
                      "k=8, v7(det)=m: chi(unit) histogram": {str(a): b for a, b in sorted(chi8.items())},
                      "n7": n7, "n8": n8}))


if __name__ == "__main__":
    main()
