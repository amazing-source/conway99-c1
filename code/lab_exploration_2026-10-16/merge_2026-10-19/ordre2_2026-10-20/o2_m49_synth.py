"""Exact check of the 7-adic order-2 algebra of H = 7 Pi (LAB, NOTE_ORDRE2_7ADIQUE §1, 20/10/2026).

Synthetic model (no srg needed: only "Pi = orthogonal projector of rank 8 on R^60, 7 Pi 7-integral, rank_7(7 Pi) = rho"):
L = span(B), B = [B0 | B1] integer 60 x 8 with B0^T B0 invertible mod 7, B1 totally isotropic mod 7 and orthogonal to B0
mod 7 (Jordan type U_(8-rho) + 7 U''_rho at 7, as for Lambda_-(T) in NOTE_RESEAUX_DE_DROITE §2).  H = 7 B G^{-1} B^T.
Checked exactly (Fractions):
  (0) H^2 = 7H, H 7-integral, rank_7 H = rho;  H = -U D U^T (mod 7) with U = B1, D solved;
  (1) U^T U = 0 (mod 7);
  (M49) U D (I + Q D) U^T = U D U^T S + S U D U^T (mod 7), S = (H + U D U^T)/7, Q = U^T U / 7;
  (a) U^T S y = 0 (mod 7) for y in K = ker(U^T mod 7);  (b) N + N^T = Q + D^{-1} (mod 7), N = U^T S C D^{-1}, C^T U = I;
  (c) next order: y^T (S - S^2) z = 0 (mod 7) for y, z in K;
  each again after changing the integer lifts U -> U + 7Y, D -> D + 7D' (statements must not depend on the lift);
  (d) a deliberately wrong H' (one entry of S shifted, H' = H + 7 E_ab + 7 E_ba) violates (M49) - negative control.
usage: python o2_m49_synth.py <seed> <rho>"""
import json
import random
import sys
from fractions import Fraction

import numpy as np
import sympy as sp

P = 7


def modp(x):
    """Fraction or int with denominator prime to 7 -> residue mod 7"""
    if isinstance(x, Fraction):
        assert x.denominator % P, "not 7-integral"
        return (x.numerator * pow(x.denominator, -1, P)) % P
    return int(x) % P


def mat_mod(M):
    return np.array([[modp(v) for v in row] for row in M], dtype=np.int64)


def rank_mod(M):
    return sp.Matrix(M.tolist()).rank(iszerofunc=lambda v: v % P == 0) if False else _rank_mod(M)


def _rank_mod(M):
    A = M.copy() % P
    r = 0
    rows, cols = A.shape
    for c in range(cols):
        piv = [i for i in range(r, rows) if A[i, c] % P]
        if not piv:
            continue
        i = piv[0]
        A[[r, i]] = A[[i, r]]
        A[r] = A[r] * pow(int(A[r, c]), -1, P) % P
        for i2 in range(rows):
            if i2 != r and A[i2, c]:
                A[i2] = (A[i2] - A[i2, c] * A[r]) % P
        r += 1
    return r


def kernel_mod(M):
    """basis of {y : M y = 0 mod 7}"""
    A = M.copy() % P
    rows, cols = A.shape
    pivcols, r = [], 0
    for c in range(cols):
        piv = [i for i in range(r, rows) if A[i, c] % P]
        if not piv:
            continue
        i = piv[0]
        A[[r, i]] = A[[i, r]]
        A[r] = A[r] * pow(int(A[r, c]), -1, P) % P
        for i2 in range(rows):
            if i2 != r and A[i2, c]:
                A[i2] = (A[i2] - A[i2, c] * A[r]) % P
        pivcols.append(c)
        r += 1
    free = [c for c in range(cols) if c not in pivcols]
    basis = []
    for fc in free:
        y = np.zeros(cols, dtype=np.int64)
        y[fc] = 1
        for i, pc in enumerate(pivcols):
            y[pc] = (-A[i, fc]) % P
        basis.append(y)
    return basis


def build(seed, rho):
    rng = random.Random(seed)
    n, m0 = 60, 8 - rho
    while True:
        B0 = np.array([[rng.randrange(-3, 4) for _ in range(m0)] for _ in range(n)], dtype=np.int64)
        if _rank_mod((B0.T @ B0) % P) == m0:
            break
    perp = kernel_mod((B0.T % P))          # vectors v with B0^T v = 0 mod 7
    cols = []
    tries = 0
    while len(cols) < rho:
        tries += 1
        v = sum(rng.randrange(P) * b for b in perp) % P
        if not v.any() or int(v @ v) % P:
            continue
        if any(int(v @ c) % P for c in cols):
            continue
        if _rank_mod(np.array(cols + [v]).T) < len(cols) + 1:
            continue
        cols.append(v)
    B1 = np.array(cols, dtype=np.int64).T
    B1 = np.where(B1 > 3, B1 - 7, B1)       # small integer lift
    return np.concatenate([B0, B1], axis=1), B1


def main():
    seed, rho = int(sys.argv[1]), int(sys.argv[2])
    att = 0
    while True:
        B, B1 = build(seed + 1000 * att, rho)
        Bs = sp.Matrix(B.tolist())
        G = Bs.T * Bs
        if sp.multiplicity(7, G.det()) == rho:
            break
        att += 1
    Hs = 7 * Bs * G.inv() * Bs.T
    H = [[Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1])) for v in Hs.row(i)] for i in range(60)]
    out = {"seed": seed, "rho": rho, "det G": str(G.det()), "v7(det G)": sp.multiplicity(7, G.det())}
    # (0)
    Hm = sp.Matrix(H)
    out["H^2 = 7H"] = bool((Hm * Hm - 7 * Hm).is_zero_matrix)
    Hmod = mat_mod(H)
    out["rank_7 H"] = _rank_mod(Hmod)
    rng = random.Random(seed + 99)

    def checks(U, D, Hrows):
        """all order-2 statements for the integer lifts U (60 x rho), D (rho x rho)"""
        Hq = sp.Matrix(Hrows)
        Us, Ds = sp.Matrix(U.tolist()), sp.Matrix(D.tolist())
        res = {}
        R0 = Hq + Us * Ds * Us.T
        res["H = -UDU^T mod 7"] = all(modp(Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1]))) == 0 for v in R0)
        S = R0 / 7
        UtU = (U.T @ U)
        res["U^T U = 0 mod 7"] = bool((UtU % P == 0).all())
        Q = sp.Matrix((UtU // 7).tolist())
        lhs = Us * Ds * (sp.eye(rho) + Q * Ds) * Us.T
        rhs = Us * Ds * Us.T * S + S * Us * Ds * Us.T
        diff = lhs - rhs
        res["(M49)"] = all(modp(Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1]))) == 0 for v in diff)
        Kb = kernel_mod((U.T % P))
        UtS = Us.T * S
        res["(a) U^T S K = 0"] = all(
            modp(Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1]))) == 0 for y in Kb[:12] for v in (UtS * sp.Matrix(y.tolist())))
        # C with C^T U = I mod 7 (then exact enough mod 7): pick rho rows where U is invertible mod 7
        rows = None
        for comb in __import__("itertools").combinations(range(60), rho):
            if _rank_mod(U[list(comb)] % P) == rho:
                rows = list(comb)
                break
        Ui = sp.Matrix((U[rows] % P).tolist()).inv_mod(P)
        C = sp.zeros(60, rho)
        for i, rr in enumerate(rows):
            for j in range(rho):
                C[rr, j] = Ui[j, i]
        Dinv = Ds.inv_mod(P)
        Nm = Us.T * S * C * Dinv
        cond_b = Nm + Nm.T - Q - Dinv
        res["(b) N + N^T = Q + D^-1"] = all(modp(Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1]))) == 0 for v in cond_b)
        SS = S - S * S
        ok_c = True
        for y in Kb[:8]:
            for z in Kb[:8]:
                v = (sp.Matrix(y.tolist()).T * SS * sp.Matrix(z.tolist()))[0, 0]
                if modp(Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1]))):
                    ok_c = False
        res["(c) y^T (S - S^2) z = 0 on K"] = ok_c
        return res

    # D from H = -U D U^T mod 7 on rho rows where U invertible
    U = B1.copy()
    rows = None
    for comb in __import__("itertools").combinations(range(60), rho):
        if _rank_mod(U[list(comb)] % P) == rho:
            rows = list(comb)
            break
    Ui = sp.Matrix((U[rows] % P).tolist()).inv_mod(P)
    Hsub = sp.Matrix([[Hmod[i, j] for j in rows] for i in rows])
    D = (-(Ui * Hsub * Ui.T)).applyfunc(lambda v: v % P)
    D = np.array(D.tolist(), dtype=np.int64)
    D = (D + D.T) * 4 % P          # symmetrise (4 = 1/2 mod 7)
    out["lift 1"] = checks(U, D, H)
    Y = np.array([[rng.randrange(-3, 4) for _ in range(rho)] for _ in range(60)], dtype=np.int64)
    Dp = np.array([[rng.randrange(-3, 4) for _ in range(rho)] for _ in range(rho)], dtype=np.int64)
    Dp = Dp + Dp.T
    out["lift 2 (U+7Y, D+7D')"] = checks(U + 7 * Y, D + 7 * Dp, H)
    # negative control: perturb one off-diagonal entry of H by 7 (i.e. S by 1)
    a, b = 3, 17
    H2 = [row[:] for row in H]
    H2[a][b] += 7
    H2[b][a] += 7
    out["negative control (H + 7E_ab + 7E_ba)"] = checks(U, D, H2)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
