"""Lab session, 2026-10-13. Mission "C2 without computation": independent control of the 61-dimensional space.

The generators of gen_tables_<EMAX>.pkl are built from Z^j and E8 only. Here the coefficient table of a lattice of
another kind is computed by direct enumeration and tested for membership in their span:
   U = D12+ + Z^12   (D12+ = D12 u (D12 + (1/2)^12), odd unimodular of rank 12),
   y1 = ((1/2)^12 ; 1,1,1,1,0^8),   y2 = ((1/2)^6,(-1/2)^6 ; 1,1,-1,-1,0^8)    (norm 7, orthogonal).
Shadow of D12+: the integer vectors of odd coordinate sum and the half-integer vectors with an odd number of minus
signs modulo D12 (i.e. D12^* minus D12+).
Test: on the table entries whose smallest representative has m = 4 (v,v) <= MTEST, the generators keep rank 61 and
adding the table of U does not raise the rank (ranks modulo a 61-bit prime).
python validate_d12.py <EMAX> <MTEST>        one process, about a minute, memory small."""
import sys, pickle, itertools
import numpy as np
import jacobi_tables as JT
import jacobi_e8 as JE

EMAX, MTEST = int(sys.argv[1]), int(sys.argv[2])
MM = JT.MMAX
AM = JT.AMAX
r1 = [1] * 12                                # doubled coordinates of (1/2)^12
r2 = [1] * 6 + [-1] * 6


def d12_arrays():
    """arrays [m, A, B] (m = 4 norm, A = 2 (v,r1), B = 2 (v,r2)) for D12+ (integral) and for its shadow"""
    n = 2 * AM + 1
    I = np.zeros((MM + 1, n, n), dtype=object)
    S = np.zeros((MM + 1, n, n), dtype=object)
    lim = MTEST                               # enumerate norms up to MTEST / 4 only

    def rec(cur, ssq, par):
        if len(cur) == 12:
            x = cur
            tot = sum(x)
            m = ssq
            A = sum(a * b for a, b in zip(x, r1)) // 2
            B = sum(a * b for a, b in zip(x, r2)) // 2
            if abs(A) > AM or abs(B) > AM:
                return
            if par == 0:                      # integer vector x/2: coordinate sum tot/2
                (I if (tot // 2) % 2 == 0 else S)[m, A + AM, B + AM] += 1
            else:                             # half-integer vector: in D12 + (1/2)^12 iff sum of x = 12 mod 4 ... see below
                (I if (tot - 12) % 4 == 0 else S)[m, A + AM, B + AM] += 1
            return
        for v in range(-7, 8):
            if (v - par) % 2 == 0 and (par == 1 or v % 2 == 0) and ssq + v * v <= lim:
                cur.append(v)
                rec(cur, ssq + v * v, par)
                cur.pop()

    rec([], 0, 0)
    rec([], 0, 1)
    return I, S


I12, S12 = d12_arrays()
# controls: D12+ has no vector of norm 1, 264 of norm 2, 2048 of norm 3 (the half-integer ones), and its shadow has 24 of norm 1
tot = lambda Arr, m: int(Arr[m].sum())
assert tot(I12, 0) == 1 and tot(I12, 4) == 0 and tot(I12, 8) == 264 and tot(I12, 12) == 2048 and tot(S12, 4) == 24, "D12+ shells"
types = [(1, 1), (1, 1), (1, -1), (1, -1)]
out = {}
for kind, base, shadow in (("I", I12, False), ("S", S12, True)):
    Pz = JE.convolve(base.copy(), types, shadow)
    scal = JT.series_pow(JT.TH2 if shadow else JT.TH3, 8)
    F = np.zeros_like(Pz)
    for dm, x in enumerate(scal):
        if x:
            F[dm:] += x * Pz[:MM + 1 - dm]
    par = 1 if shadow else 0
    for m in range(MTEST + 1):
        for A in range(-JT.SAFE, JT.SAFE + 1):
            if (A - par) % 2:
                continue
            for B in range(-JT.SAFE, JT.SAFE + 1):
                if (B - par) % 2:
                    continue
                e4 = 7 * m - A * A - B * B
                v = int(F[m, A + AM, B + AM])
                if e4 < 0:
                    assert v == 0
                    continue
                if e4 > 4 * EMAX:
                    continue
                cl = min((A % 7, B % 7), ((-A) % 7, (-B) % 7))
                key = (kind, cl, e4)
                if key in out:
                    assert out[key] == v, ("not a function of (E, class)", key, out[key], v, m, A, B)
                else:
                    out[key] = v
desc, tabs = pickle.load(open("gen_tables_%d.pkl" % EMAX, "rb"))
keys = sorted(k for k in out if any(t.get(k, 0) for t in tabs) or out[k])
P = (1 << 61) - 1


def rank_mod(Mat):
    A = [[int(x) % P for x in row] for row in Mat]
    rows = len(A)
    r = 0
    for c in range(len(A[0])):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], P - 2, P)
        A[r] = [(x * inv) % P for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % P for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


G = [[t.get(k, 0) for k in keys] for t in tabs]
r0 = rank_mod(G)
r1_ = rank_mod(G + [[out[k] for k in keys]])
print("table of (D12+ + Z^12; y1, y2): %d entries tested (integral %d, shadow %d), smallest E present: integral %s, shadow %s" % (
    len(keys), sum(1 for k in keys if k[0] == "I"), sum(1 for k in keys if k[0] == "S"),
    min(k[2] / 4 for k in keys if k[0] == "I" and out[k] and k[2] > 0), min(k[2] / 4 for k in keys if k[0] == "S" and out[k])))
print("rank of the generators on these entries: %d ; with the new table: %d   ->  %s" % (
    r0, r1_, "the new table lies in the span (control passed)" if r0 == 61 and r1_ == 61 else "CONTROL FAILED or not conclusive"))
