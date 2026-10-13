"""Lab session, 2026-10-13. Mission "C2 without computation", step 2: independent control of the one-h space.

The generators of h1_tables_<DMAX>.pkl use Z^j and E8 only. Here: U = D12+ + Z^12 by direct enumeration, with
   y1 = ((1/2)^12 ; 1,1,1,1,0^8),  y2 = ((1/2)^6,(-1/2)^6 ; 1,1,-1,-1,0^8),  h = (0^12 ; 1,-1,1,-1,0^8).
Test: on the entries computed from vectors with m = 4 (v,v) <= MTEST, the generators keep their rank and the new
table does not raise it (ranks modulo a 61-bit prime).
python validate_d12_h.py <DMAX> <MTEST>        one process, about a minute, < 1 GB."""
import sys, pickle
import numpy as np
import heptad1 as H
from jacobi_tables import MMAX, TH2, TH3, series_pow

DMAX, MTEST = int(sys.argv[1]), int(sys.argv[2])
r1 = [1] * 12
r2 = [1] * 6 + [-1] * 6
I12 = np.zeros((MMAX + 1, H.NA, H.NA, H.NT), dtype=np.int64)
S12 = np.zeros_like(I12)


def rec(cur, ssq, par):
    if len(cur) == 12:
        tot = sum(cur)
        A = sum(a * b for a, b in zip(cur, r1)) // 2
        B = sum(a * b for a, b in zip(cur, r2)) // 2
        if abs(A) > H.AM or abs(B) > H.AM:
            return
        if par == 0:
            (I12 if (tot // 2) % 2 == 0 else S12)[ssq, A + H.AM, B + H.AM, H.TM] += 1
        else:
            (I12 if (tot - 12) % 4 == 0 else S12)[ssq, A + H.AM, B + H.AM, H.TM] += 1
        return
    for v in range(-7, 8):
        if (v - par) % 2 == 0 and (par == 1 or v % 2 == 0) and ssq + v * v <= MTEST:
            cur.append(v)
            rec(cur, ssq + v * v, par)
            cur.pop()


rec([], 0, 0)
rec([], 0, 1)
assert int(I12[8].sum()) == 264 and int(I12[12].sum()) == 2048 and int(S12[4].sum()) == 24, "D12+ shells"
types = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]
import heptad1_e8_conv as HC
out = {}
for kind, base, shadow in (("I", I12, False), ("S", S12, True)):
    Pz = HC.convolve(base.copy(), types, shadow)
    scal = series_pow(TH2 if shadow else TH3, 8)
    F = np.zeros_like(Pz)
    for dm, x in enumerate(scal):
        if x:
            F[dm:] += int(x) * Pz[:MMAX + 1 - dm]
    F[MTEST + 1:] = 0                                     # only vectors with m <= MTEST are complete
    for k, v in H.reduce_part(F, shadow, DMAX).items():
        out[k] = v
desc, tabs = pickle.load(open("h1_tables_%d.pkl" % DMAX, "rb"))
# keys testable: those whose smallest representative has m <= MTEST
def min_m(key):
    kind, (a7, b7, t4), D = key
    best = None
    par = 1 if kind == "S" else 0
    for A in range(-13, 14):
        if (A - par) % 2 or A % 7 != a7:
            continue
        for B in range(-13, 14):
            if (B - par) % 2 or B % 7 != b7:
                continue
            for t in (-2, -1, 0, 1, 2, 3):
                if t % 4 != t4:
                    continue
                num = D + A * A + B * B + 7 * t * t
                if num % 7 == 0:
                    m = num // 7
                    if best is None or m < best:
                        best = m
    return best
allkeys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
keys = [k for k in allkeys if (min_m(k) is not None and min_m(k) <= MTEST)]
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
r1_ = rank_mod(G + [[out.get(k, 0) for k in keys]])
print("entries tested: %d of %d (smallest representative with m <= %d); non-zero in the new table: %d" % (len(keys), len(allkeys), MTEST, sum(1 for k in keys if out.get(k, 0))))
print("rank of the %d generators on these entries: %d ; with the table of (D12+ + Z^12; y1, y2, h): %d  ->  %s" % (
    len(tabs), r0, r1_, "in the span" if r1_ == r0 else "NOT in the span: the generators do not span the space"))
