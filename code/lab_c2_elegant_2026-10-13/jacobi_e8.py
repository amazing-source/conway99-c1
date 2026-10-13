"""Lab session, 2026-10-13. Mission "C2 without computation", step 1.
Generators with a part in E8:  Theta_{E8 + Z^j; y} * theta_3^c * (16 Delta_8)^i,  8 + j + c + 8 i = 24,
y_a = (r_a, w_a) with r_a in E8 and w_a in Z^j.  The shadow of E8 is E8 itself.
Same units and same tables as jacobi_tables.py (module used by span_rank.py).   Memory: small."""
import numpy as np
from jacobi_tables import MMAX, AMAX, SAFE, TH2, TH3, TH4D, D16, mul, series_pow

_E8 = None


def e8_vectors():
    """vectors of E8 of norm <= MMAX / 4, in doubled coordinates (all even or all odd, sum = 0 mod 4)"""
    global _E8
    if _E8 is not None:
        return _E8
    out = []

    def rec(cur, ssq, tot, par):
        if len(cur) == 8:
            if tot % 4 == 0:
                out.append(tuple(cur))
            return
        for x in range(-7, 8):
            if (x - par) % 2 == 0 and ssq + x * x <= MMAX:
                cur.append(x)
                rec(cur, ssq + x * x, tot + x, par)
                cur.pop()

    rec([], 0, 0, 0)
    rec([], 0, 0, 1)
    _E8 = np.array(out, dtype=np.int64)
    norms = (_E8 * _E8).sum(1) // 4
    assert [int((norms == k).sum()) for k in (0, 2, 4, 6, 8, 10)] == [1, 240, 2160, 6720, 17520, 30240], "E8 shells"
    return _E8


def e8_part(r1, r2):
    """array [m, A, B] for v in E8: m = 4 (v,v), A = 2 (v,r1), B = 2 (v,r2); r1, r2 in doubled coordinates"""
    V = e8_vectors()
    m = (V * V).sum(1)
    A = (V @ np.array(r1)) // 2
    B = (V @ np.array(r2)) // 2
    n = 2 * AMAX + 1
    P = np.zeros((MMAX + 1, n, n), dtype=object)
    ok = (np.abs(A) <= AMAX) & (np.abs(B) <= AMAX)
    for mm, a, b in zip(m[ok].tolist(), A[ok].tolist(), B[ok].tolist()):
        P[mm, a + AMAX, b + AMAX] += 1
    return P


def convolve(P, types, shadow):
    n = 2 * AMAX + 1
    for s, t in types:
        Q = np.zeros_like(P)
        vals = [2 * k + 1 for k in range(-4, 4)] if shadow else [2 * k for k in range(-3, 4)]
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


def table_e8(r1, r2, types, i, emax4):
    j = len(types)
    c = 24 - 8 - j - 8 * i
    assert c >= 0
    n1 = sum(x * x for x in r1) // 4
    n2 = sum(x * x for x in r2) // 4
    ip = sum(x * y for x, y in zip(r1, r2)) // 4
    assert n1 + sum(s * s for s, t in types) == 7 and n2 + sum(t * t for s, t in types) == 7
    assert ip + sum(s * t for s, t in types) == 0
    out = {}
    base = e8_part(r1, r2)
    for kind, shadow in (("I", False), ("S", True)):
        P = convolve(base.copy(), types, shadow)
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


def z_patterns(na, nb, ip):
    """multisets of coordinate types (s, t) with sum s^2 = na, sum t^2 = nb, sum s t = ip"""
    T = [(s, t) for s in range(-2, 3) for t in range(-2, 3) if (s, t) != (0, 0)]
    T = [x for x in T if x > (-x[0], -x[1])]
    out = []

    def rec(start, cur, a, b, c):
        if a > na or b > nb:
            return
        if a == na and b == nb:
            if c == ip:
                out.append(tuple(cur))
            return
        for u in range(start, len(T)):
            s, t = T[u]
            cur.append((s, t))
            rec(u, cur, a + s * s, b + t * t, c + s * t)
            cur.pop()

    rec(0, [], 0, 0, 0)
    return out
