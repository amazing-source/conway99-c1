"""Exact class counts of line graphs G_T by Burnside's lemma (LAB 20/10/2026, NOTE_ENUM37.md).

Object: classes C0, C1, C2 of size n = 2m (n = 12 for Conway), partner matching i <-> i^1 in each class, three bijections
s01, s12, s20; equivalence = partner-preserving relabelling of each class (B_m = Z2 wr S_m) and permutation of the classes.

Decomposition (proved in NOTE_ENUM37.md, section 1): sigma = s20 s12 s01 has a cycle type lambda |- n (an invariant), and
the classes of type lambda <-> orbits of A_lambda on triples (M0, M1, M2) of perfect matchings of [n], where for the
canonical cross structure F_lambda (s01 = s12 = id, s20 = sigma) the group A_lambda = Stab(F_lambda) consists of
    id   : (g, g, g)        g in C = C(sigma)          image (gM0, gM1, gM2)
    rho  : (g, g, g sigma)  g in C                     image (g sigma M2, g M0, g M1)
    rho^2: (g, g sigma, g sigma)                       image (g sigma M1, g sigma M2, g M0)
    (12) : (h, h sigma, h sigma)  h in R = {h : h sigma h^-1 = sigma^-1}   image (h M0, h sigma M2, h sigma M1)
    (01) : (h, h, h sigma)                             image (h M1, h M0, h sigma M2)
    (02) : (h, h, h)                                   image (h M2, h M1, h M0)
Burnside:  N_lambda = [ sum_{g in C} f(g)^3 + 2 sum_{g in C} f(sigma g^3) + 3 sum_{h in R} f(h) f(h^2) ] / (6 z_lambda),
f(p) = number of perfect matchings invariant under p (depends on the cycle type).  The sums are computed exactly from the
wreath-product structure C = prod_k Z_k wr S_{m_k} (formulas in the note), and cross-checked:
  * against explicit enumeration of C and R inside S_n (small n, or small z_lambda at n = 12)          (--check-explicit)
  * the total against an independent Burnside count over the relabelling group H = B_m^3 x| S3 acting on bijection
    triples (no lambda decomposition):
      N = [ sum_mu n_mu^3 z_mu^3 + 2 |B|^2 sum_mu n_mu z_mu + 3 |B| sum_mu a_mu n_mu z_mu r_mu ] / (6 |B|^3)
    n_mu = #{p in B: type p = mu}, a_mu = #{p in B: type p^2 = mu}, z_mu = |C_{S_n}(mu)|, r_mu = #square roots in S_n.
usage: python enum37_burnside.py [m=6] [--check-explicit] [--json out.json]
"""
import itertools
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction


# ------------------------------------------------------------------------------------------------ partitions / types
def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


def type_of_partition(lam, n):
    v = [0] * (n + 1)
    for p in lam:
        v[p] += 1
    return tuple(v)


def partition_of_type(t):
    out = []
    for k in range(len(t) - 1, 0, -1):
        out += [k] * t[k]
    return tuple(out)


def zee(t):
    """centralizer order in S_n of a permutation with cycle-count vector t"""
    z = 1
    for k in range(1, len(t)):
        z *= k ** t[k] * math.factorial(t[k])
    return z


def dfact(x):  # (x)!! for odd x >= -1
    r = 1
    while x > 1:
        r *= x
        x -= 2
    return r


def f_pm(t):
    """number of perfect matchings of [n] invariant under a permutation of type t"""
    r = 1
    for k in range(1, len(t)):
        c = t[k]
        if k % 2:
            if c % 2:
                return 0
            r *= dfact(c - 1) * k ** (c // 2)
        else:
            r *= sum(math.comb(c, 2 * j) * dfact(2 * j - 1) * k ** j for j in range(c // 2 + 1))
    return r


def sqrt_count(t):
    """number of square roots in S_n of a permutation of type t"""
    r = 1
    for k in range(1, len(t)):
        c = t[k]
        if k % 2:
            r *= sum(math.comb(c, 2 * j) * dfact(2 * j - 1) * k ** j for j in range(c // 2 + 1))
        else:
            if c % 2:
                return 0
            r *= dfact(c - 1) * k ** (c // 2)
    return r


def addv(a, b):
    return tuple(x + y for x, y in zip(a, b))


def conv(A, B):
    out = defaultdict(int)
    for ka, va in A.items():
        for kb, vb in B.items():
            out[addv(ka, kb) if not isinstance(ka[0], tuple) else (addv(ka[0], kb[0]), addv(ka[1], kb[1]))] += va * vb
    return dict(out)


def unit(n, joint=False):
    z = tuple([0] * (n + 1))
    return {(z, z): 1} if joint else {z: 1}


def cyc(n, length, count):
    v = [0] * (n + 1)
    if count:
        v[length] += count
    return tuple(v)


# ------------------------------------------------------------------------------------------------ wreath-product sums
def beta_cycle_poly(n, k, ell, kind):
    """distribution of the contribution of one cycle (length ell) of the cycle permutation beta in Z_k wr S_m:
    kind 'id'  : g itself,   kind 'cube': sigma g^3,   kind 'rev': (h, h^2) for a reverser h."""
    out = defaultdict(int)
    w = k ** (ell - 1)
    for s in range(k):
        if kind == "id":
            gg = math.gcd(s, k)
            out[cyc(n, ell * k // gg, gg)] += w
        elif kind == "cube":
            if ell % 3:
                t = (3 * s + ell) % k
                gg = math.gcd(t, k)
                out[cyc(n, ell * k // gg, gg)] += w
            else:
                t = (s + ell // 3) % k
                gg = math.gcd(t, k)
                out[cyc(n, (ell // 3) * k // gg, 3 * gg)] += w
        else:  # reverser, parameter s = c (ell odd: reflection constant) or d (ell even: translation)
            if ell % 2:
                if k % 2:
                    nsol = 1
                else:
                    nsol = 2 if s % 2 == 0 else 0
                th = addv(cyc(n, ell, nsol), cyc(n, 2 * ell, (k - nsol) // 2))
                out[(th, cyc(n, ell, k))] += w
            else:
                gg = math.gcd(s, k)
                L = ell * k // gg
                out[(cyc(n, L, gg), cyc(n, L // 2, 2 * gg))] += w
    return dict(out)


def block_dist(n, k, m, kind):
    """distribution over Z_k wr S_m (resp. its reverser coset) of the cycle type contribution"""
    joint = kind == "rev"
    total = defaultdict(int)
    for mu in partitions(m):
        tmu = type_of_partition(mu, m)
        nb = math.factorial(m) // zee(tmu)
        D = unit(n, joint)
        for ell in mu:
            D = conv(D, beta_cycle_poly(n, k, ell, kind))
        for key, v in D.items():
            total[key] += nb * v
    return dict(total)


def lambda_sums(lam, n):
    t = type_of_partition(lam, n)
    Did, Dcube, Drev = unit(n), unit(n), unit(n, True)
    for k in range(1, n + 1):
        if t[k]:
            Did = conv(Did, block_dist(n, k, t[k], "id"))
            Dcube = conv(Dcube, block_dist(n, k, t[k], "cube"))
            Drev = conv(Drev, block_dist(n, k, t[k], "rev"))
    return Did, Dcube, Drev


def count_lambda(lam, n):
    t = type_of_partition(lam, n)
    z = zee(t)
    Did, Dcube, Drev = lambda_sums(lam, n)
    assert sum(Did.values()) == z and sum(Dcube.values()) == z and sum(Drev.values()) == z
    S_id = sum(v * f_pm(k) ** 3 for k, v in Did.items())
    S_rot = sum(v * f_pm(k) for k, v in Dcube.items())
    S_ref = sum(v * f_pm(k1) * f_pm(k2) for (k1, k2), v in Drev.items())
    num = S_id + 2 * S_rot + 3 * S_ref
    assert num % (6 * z) == 0, (lam, num, 6 * z)
    return {"lambda": list(lam), "z": z, "S_id": S_id, "S_rot": S_rot, "S_ref": S_ref, "N": num // (6 * z),
            "free_estimate": f_pm(type_of_partition((1,) * n, n)) ** 3 / (6 * z)}


# ------------------------------------------------------------------------------------------------ independent total
def total_via_H(m):
    n = 2 * m
    # distribution of S_n cycle types over B_m = Z2 wr S_m
    Bd = block_dist(n, 2, m, "id")
    order_B = 2 ** m * math.factorial(m)
    assert sum(Bd.values()) == order_B

    def square_type(t):
        v = [0] * (n + 1)
        for L in range(1, n + 1):
            if t[L]:
                if L % 2:
                    v[L] += t[L]
                else:
                    v[L // 2] += 2 * t[L]
        return tuple(v)

    a = defaultdict(int)
    for t, c in Bd.items():
        a[square_type(t)] += c
    S1 = sum(c ** 3 * zee(t) ** 3 for t, c in Bd.items())
    S2 = order_B ** 2 * sum(c * zee(t) for t, c in Bd.items())
    S3 = order_B * sum(a[t] * Bd.get(t, 0) * zee(t) * sqrt_count(t) for t in a)
    num = S1 + 2 * S2 + 3 * S3
    assert num % (6 * order_B ** 3) == 0
    return num // (6 * order_B ** 3), {"S1": S1, "S2": S2, "S3": S3}


# ------------------------------------------------------------------------------------------------ explicit check
def perm_type(p):
    n = len(p)
    seen = [False] * n
    v = [0] * (n + 1)
    for i in range(n):
        if not seen[i]:
            L = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            v[L] += 1
    return tuple(v)


def compose(a, b):  # (a b)(i) = a(b(i))
    return tuple(a[b[i]] for i in range(len(b)))


def inverse(a):
    r = [0] * len(a)
    for i, j in enumerate(a):
        r[j] = i
    return tuple(r)


def canonical_sigma(lam):
    """the permutation of [n] whose cycles are consecutive blocks of lengths lam (in the given order)"""
    n = sum(lam)
    p = list(range(n))
    pos = 0
    for L in lam:
        for j in range(L):
            p[pos + j] = pos + (j + 1) % L
        pos += L
    return tuple(p)


def explicit_sums(lam):
    """enumerate C(sigma) and R(sigma) inside S_n by brute force (n <= 8) -> the three distributions"""
    n = sum(lam)
    sig = canonical_sigma(lam)
    sinv = inverse(sig)
    Did, Dcube, Drev = defaultdict(int), defaultdict(int), defaultdict(int)
    for g in itertools.permutations(range(n)):
        gs = compose(g, sig)
        if gs == compose(sig, g):
            Did[perm_type(g)] += 1
            g3 = compose(g, compose(g, g))
            Dcube[perm_type(compose(sig, g3))] += 1
        if gs == compose(sinv, g):        # g sigma g^-1 = sigma^-1
            Drev[(perm_type(g), perm_type(compose(g, g)))] += 1
    return dict(Did), dict(Dcube), dict(Drev)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    m = int(args[0]) if args else 6
    n = 2 * m
    out_json = None
    if "--json" in sys.argv:
        out_json = sys.argv[sys.argv.index("--json") + 1]
    rows = []
    for lam in partitions(n):
        rows.append(count_lambda(lam, n))
    if "--check-explicit" in sys.argv and n <= 8:
        for lam in partitions(n):
            e = explicit_sums(lam)
            f = lambda_sums(lam, n)
            assert e[0] == {k: v for k, v in f[0].items() if v}, ("id", lam)
            assert e[1] == {k: v for k, v in f[1].items() if v}, ("cube", lam)
            assert e[2] == {k: v for k, v in f[2].items() if v}, ("rev", lam)
        print("explicit enumeration of C(sigma), R(sigma) agrees with the wreath formulas for all %d partitions of %d"
              % (len(rows), n))
    total = sum(r["N"] for r in rows)
    tH, parts = total_via_H(m)
    pm = dfact(n - 1)
    print("n = %d: %d partitions, total classes %d ; independent H-Burnside total %d ; agree: %s"
          % (n, len(rows), total, tH, total == tH))
    print("free-action estimate PM^3/6 = %.6e ; exact/estimate = %.9f" % (pm ** 3 / 6, total / (pm ** 3 / 6)))
    rows.sort(key=lambda r: r["N"])
    for r in rows:
        print("%-28s z=%-10d N=%-14d free-est=%.4e ratio=%.4f" % ("(" + ",".join(map(str, r["lambda"])) + ")", r["z"],
                                                                   r["N"], r["free_estimate"],
                                                                   r["N"] / r["free_estimate"]))
    if out_json:
        with open(out_json, "w") as fh:
            json.dump({"n": n, "total": total, "total_H": tH, "rows": rows}, fh, indent=1)


if __name__ == "__main__":
    main()
