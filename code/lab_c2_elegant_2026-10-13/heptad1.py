"""Lab session, 2026-10-13. Mission "C2 without computation", step 2: one vector h of the heptad in the index.

Jacobi forms in three elliptic variables for (U; y1, y2, h): U odd unimodular of rank 24, (y_a, y_b) = 7 delta_ab,
(h, h) = 4, h orthogonal to y1, y2. Generators: Theta_{Z^j; y1, y2, h} * theta_3^c * (16 Delta_8)^i, with shadows.
Units: m = 4 (v,v), A = 2 (v,y1), B = 2 (v,y2), tt = 2 (v,h) (tt is even for integral AND for shadow vectors).
With t = (v,h) = tt / 2:   4E = 7 m - A^2 - B^2,   D = 4E - 7 t^2  (28 times the squared norm of the projection on the
orthogonal complement of y1, y2, h).  A coefficient depends only on D and on the class (A mod 7, B mod 7, t mod 4) up to
a global sign (checked on every generator).
Table: {(kind, (A mod 7, B mod 7, t mod 4) up to sign, D): coefficient}, kind 'I' (integral) or 'S' (shadow).
Module used by heptad1_lp.py.  Memory: about 100 MB."""
import random
import numpy as np
from jacobi_tables import MMAX, TH2, TH3, TH4D, D16, mul, series_pow

AM = 18          # |A|, |B| <= 17 whenever 7 m >= A^2 + B^2 and m <= 44
TM = 14          # |tt| <= 2 * 2 sqrt(m/4) = 2 sqrt(m) <= 13.3
NA = 2 * AM + 1
NT = 2 * TM + 1


def jacobi_part(types, shadow):
    """int64 array P[m, A, B, tt] for Z^j with the coordinate types (s, t, u) = (y1_i, y2_i, h_i)"""
    P = np.zeros((MMAX + 1, NA, NA, NT), dtype=np.int64)
    P[0, AM, AM, TM] = 1
    for s, t, u in types:
        Q = np.zeros_like(P)
        vals = [2 * k + 1 for k in range(-4, 4)] if shadow else [2 * k for k in range(-3, 4)]
        for w in vals:
            dm, da, db, dt = w * w, s * w, t * w, u * w
            if dm > MMAX:
                continue
            a0, a1 = max(0, -da), min(NA, NA - da)
            b0, b1 = max(0, -db), min(NA, NA - db)
            c0, c1 = max(0, -dt), min(NT, NT - dt)
            if a0 >= a1 or b0 >= b1 or c0 >= c1:
                continue
            Q[dm:, a0 + da:a1 + da, b0 + db:b1 + db, c0 + dt:c1 + dt] += P[:MMAX + 1 - dm, a0:a1, b0:b1, c0:c1]
        P = Q
    return P


def key_of(A, B, t, D, kind):
    c1 = (A % 7, B % 7, t % 4)
    c2 = ((-A) % 7, (-B) % 7, (-t) % 4)
    return (kind, min(c1, c2), D)


def reduce_part(P, shadow, dmax):
    """table of the Jacobi part: {(class, D_P): count}, with the consistency check"""
    out = {}
    par = 1 if shadow else 0
    nz = np.nonzero(P)
    for m, ia, ib, it in zip(*[x.tolist() for x in nz]):
        A, B, tt = ia - AM, ib - AM, it - TM
        assert (A - par) % 2 == 0 and (B - par) % 2 == 0 and tt % 2 == 0
        t = tt // 2
        D = 7 * m - A * A - B * B - 7 * t * t
        assert D >= 0, "negative discriminant"
        if D > dmax:
            continue
        if abs(A) > AM - 1 or abs(B) > AM - 1 or abs(tt) > TM - 1:
            continue
        k = key_of(A, B, t, D, "S" if shadow else "I")
        v = int(P[m, ia, ib, it])
        if k in out:
            assert out[k] == v, ("not a function of (class, D)", k, out[k], v)
        else:
            out[k] = v
    return out


def table(types, i, dmax):
    """coefficient table of Theta_{Z^j; y1, y2, h} theta_3^c (16 Delta_8)^i, entries with D <= dmax"""
    j = len(types)
    c = 24 - j - 8 * i
    assert c >= 0
    for x, y, val in ((0, 0, 7), (1, 1, 7), (2, 2, 4), (0, 1, 0), (0, 2, 0), (1, 2, 0)):
        assert sum(tp[x] * tp[y] for tp in types) == val
    out = {}
    for kind, shadow in (("I", False), ("S", True)):
        base = reduce_part(jacobi_part(types, shadow), shadow, dmax)
        if shadow:
            scal = mul(series_pow(TH2, c), [((-1) ** i) * x for x in series_pow(TH4D, 8 * i)])
        else:
            scal = mul(series_pow(TH3, c), series_pow(D16, i))
        for (kd, cl, D), v in base.items():
            for dm, x in enumerate(scal):
                if x and D + 7 * dm <= dmax:
                    out[(kd, cl, D + 7 * dm)] = out.get((kd, cl, D + 7 * dm), 0) + x * v
    return out


def random_patterns(count, seed):
    """triples (y1, y2, h) in Z^j, entries of absolute value <= 2, given as sorted lists of coordinate types"""
    rnd = random.Random(seed)
    seen = set()
    out = []
    shapes7 = [[1] * 7, [2, 1, 1, 1]]
    tries = 0
    while len(out) < count and tries < 200000:
        tries += 1
        j = rnd.randrange(6, 15)
        hvec = [0] * j
        if rnd.random() < 0.65:
            for p in rnd.sample(range(j), 4):
                hvec[p] = rnd.choice((1, -1))
        else:
            hvec[rnd.randrange(j)] = 2
        vecs = []
        ok = True
        for _ in range(2):
            found = False
            for _ in range(60):
                shape = rnd.choice(shapes7)
                if len(shape) > j:
                    continue
                v = [0] * j
                for p, val in zip(rnd.sample(range(j), len(shape)), shape):
                    v[p] = val * rnd.choice((1, -1))
                if sum(a * b for a, b in zip(v, hvec)) == 0 and all(sum(a * b for a, b in zip(v, w)) == 0 for w in vecs):
                    vecs.append(v)
                    found = True
                    break
            if not found:
                ok = False
                break
        if not ok:
            continue
        types = [(vecs[0][p], vecs[1][p], hvec[p]) for p in range(j) if (vecs[0][p], vecs[1][p], hvec[p]) != (0, 0, 0)]
        norm = tuple(sorted(max(tp, tuple(-x for x in tp)) for tp in types))
        if norm in seen:
            continue
        seen.add(norm)
        out.append(list(norm))
    return out
