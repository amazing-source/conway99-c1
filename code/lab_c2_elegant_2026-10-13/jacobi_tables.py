"""Lab session, 2026-10-13. Mission "C2 without computation", step 1.
Explicit Jacobi forms in the space where the theta series of (U; y1, y2) lives, and their coefficient tables.

A generator is  F = Theta_{Z^j; y}(tau; z1, z2) * theta_3^c * (16 Delta_8)^i,   j + c + 8 i = 24,
where y = (y1, y2) is a pair of orthogonal vectors of norm 7 of Z^j (given by the list of the pairs (y1_t, y2_t)).
Its shadow is  Theta^sh_{Z^j; y} * theta_2^c * (-1)^i theta_4(2 tau)^(8i)   (Conway-Sloane: the shadow of
theta_3^a Delta_8^r is (-1/16)^r theta_2^a theta_4(2 tau)^(8r); control: theta_3^8 - 16 Delta_8 = theta of E8, whose shadow
theta_2^8 + theta_4(2 tau)^8 is again the theta series of E8, checked below).
Units: m = 4 (v,v), A = 2 (v,y1), B = 2 (v,y2); integral vectors have A, B even, shadow vectors A, B odd;
E = 7 (v,v) - (v,y1)^2 - (v,y2)^2 = (7 m - A^2 - B^2) / 4.
A coefficient depends only on E and on the class (A mod 7, B mod 7) up to sign (checked on every generator).
Table of a generator: {('I' or 'S', class, 4E): coefficient}, for 4E <= 4 EMAX.
Used as a module by forcing_lp.py.   Memory: small."""
import numpy as np

MMAX = 44      # m <= MMAX
AMAX = 26      # |A|, |B| <= AMAX in the arrays
SAFE = 18      # entries are read only for |A|, |B| <= SAFE (7 m >= A^2 + B^2 and m <= 44 give |A| <= 17)


def series_pow(base, p):
    out = [0] * (MMAX + 1)
    out[0] = 1
    for _ in range(p):
        out = mul(out, base)
    return out


def mul(s, t):
    out = [0] * (MMAX + 1)
    for i, x in enumerate(s):
        if x:
            for j, y in enumerate(t):
                if y and i + j <= MMAX:
                    out[i + j] += x * y
    return out


TH3 = [0] * (MMAX + 1)
TH2 = [0] * (MMAX + 1)
TH4 = [0] * (MMAX + 1)
for k in range(-8, 9):
    if 4 * k * k <= MMAX:
        TH3[4 * k * k] += 1
        TH4[4 * k * k] += (-1) ** k
    if (2 * k + 1) ** 2 <= MMAX:
        TH2[(2 * k + 1) ** 2] += 1
TH4D = [0] * (MMAX + 1)                                  # theta_4(2 tau): exponents 8 k^2 in the unit m
for k in range(-3, 4):
    if 8 * k * k <= MMAX:
        TH4D[8 * k * k] += (-1) ** k
D16 = mul(series_pow(TH2, 4), series_pow(TH4, 4))       # 16 Delta_8
assert D16[4] == 16 and all(D16[m] == 0 for m in range(4))


def jacobi_part(types, shadow):
    """array P[m, A + AMAX, B + AMAX] = number of v in Z^j (or in its shadow) with these values"""
    n = 2 * AMAX + 1
    P = np.zeros((MMAX + 1, n, n), dtype=object)
    P[0, AMAX, AMAX] = 1
    for s, t in types:
        Q = np.zeros_like(P)
        vals = [2 * k + 1 for k in range(-4, 4)] if shadow else [2 * k for k in range(-3, 4)]     # twice the coordinate
        for w in vals:
            dm = w * w
            da = s * w
            db = t * w
            if dm > MMAX:
                continue
            a0, a1 = max(0, -da), min(n, n - da)
            b0, b1 = max(0, -db), min(n, n - db)
            Q[dm:, a0 + da:a1 + da, b0 + db:b1 + db] += P[:MMAX + 1 - dm, a0:a1, b0:b1]
        P = Q
    return P


def table(types, i, emax4):
    """coefficient table of the generator (types, i); emax4 = 4 EMAX"""
    j = len(types)
    c = 24 - j - 8 * i
    assert c >= 0
    assert sum(s * s for s, t in types) == 7 and sum(t * t for s, t in types) == 7 and sum(s * t for s, t in types) == 0
    out = {}
    for kind, shadow in (("I", False), ("S", True)):
        P = jacobi_part(types, shadow)
        if shadow:
            scal = mul(series_pow(TH2, c), [((-1) ** i) * x for x in series_pow(TH4D, 8 * i)])
        else:
            scal = mul(series_pow(TH3, c), series_pow(D16, i))
        F = np.zeros_like(P)
        for dm, x in enumerate(scal):
            if x:
                F[dm:] += x * P[:MMAX + 1 - dm]
        par = 1 if shadow else 0
        for m in range(MMAX + 1):
            for A in range(-SAFE, SAFE + 1):
                if (A - par) % 2:
                    continue
                for B in range(-SAFE, SAFE + 1):
                    if (B - par) % 2:
                        continue
                    e4 = 7 * m - A * A - B * B
                    v = int(F[m, A + AMAX, B + AMAX])
                    if e4 < 0:
                        assert v == 0, "vector with E < 0"
                        continue
                    if e4 > emax4:
                        continue
                    cl = min((A % 7, B % 7), ((-A) % 7, (-B) % 7))
                    key = (kind, cl, e4)
                    if key in out:
                        assert out[key] == v, ("not a function of (E, class)", key, out[key], v, m, A, B)
                    else:
                        out[key] = v
    return out


def patterns():
    """pairs of orthogonal vectors of norm 7 with entries of absolute value <= 2, as multisets of coordinate types"""
    T = [(s, t) for s in range(-2, 3) for t in range(-2, 3) if (s, t) != (0, 0)]
    T = [x for x in T if x > (-x[0], -x[1])]                                 # one of each pair +-(s,t)
    out = []

    def rec(start, cur, a, b, c):
        if a > 7 or b > 7:
            return
        if a == 7 and b == 7:
            if c == 0:
                out.append(tuple(cur))
            return
        for u in range(start, len(T)):
            s, t = T[u]
            cur.append((s, t))
            rec(u, cur, a + s * s, b + t * t, c + s * t)
            cur.pop()

    rec(0, [], 0, 0, 0)
    return out


# control of the shadow rule on E8: theta_3^8 - 16 Delta_8 and theta_2^8 + theta_4(2 tau)^8 are the same series 1 + 240 q^2 + ...
_e8 = [a - b for a, b in zip(series_pow(TH3, 8), D16)]
_e8s = [a + b for a, b in zip(series_pow(TH2, 8), series_pow(TH4D, 8))]
assert _e8 == _e8s and _e8[8] == 240 and _e8[4] == 0, "shadow rule"
