"""Fifth moments of the vertex frame and the line frame in the (-4)-eigenspace of srg(99,14,1,2) (dimension 44).

Tensors of degree 5 (u_x = sqrt(63) E e_x; (u,u') = 28, -8, 1; q_T = (u_a+u_b+u_c)/3; (q_T,u_x) = 4, -2, 1 for x in
T, x adjacent to one point of T, x adjacent to none):
  V5   = sum_x u_x^5
  E32  = sum over ordered adjacent pairs (x,y) of sym(u_x^3 u_y^2)
  W311 = sum over lines and marked point a of sym(u_a^3 u_b u_c)
  W221 = sum over lines and marked point a of sym(u_a u_b^2 u_c^2)
  gV3  = sym(g x V3),  gS3 = sym(g x S3),  with V3 = sum_x u_x^3, S3 = sum_T q_T^3 (both traceless)
(sum_T q_T^5 = (-13 V5 + 10 E32 + 20 W311 + 30 W221)/243.)  Every Gram entry is affine in the average prism number.
Exact rational arithmetic; controls printed.
"""
from fractions import Fraction as Fr
from itertools import combinations, permutations

from moments4 import det, ip_factory, line_adj

D = 44
PERMS5 = list(permutations(range(5)))


def tens_ip5(t1, t2, ip):
    m = [[ip(x, y) for y in t2] for x in t1]
    s = 0
    for p in PERMS5:
        s += m[0][p[0]] * m[1][p[1]] * m[2][p[2]] * m[3][p[3]] * m[4][p[4]]
    return Fr(s, 120)


def e32_terms(line):
    return [(x, x, x, y, y) for x in line for y in line if x != y]


def w311_terms(line):
    a, b, c = line
    return [(a, a, a, b, c), (b, b, b, a, c), (c, c, c, a, b)]


def w221_terms(line):
    a, b, c = line
    return [(a, b, b, c, c), (b, a, a, c, c), (c, a, a, b, b)]


LINE_TENSORS = {"E32": e32_terms, "W311": w311_terms, "W221": w221_terms}
T = ("a", "b", "c")


def pair_classes():
    cl = {"same": (T, T, line_adj(T))}
    T2 = ("a", "b2", "c2")
    cl["meet"] = (T, T2, line_adj(T, T2))
    for j in range(4):
        T3 = ("a3", "b3", "c3")
        adj = line_adj(T, T3)
        for i in range(j):
            adj.add(frozenset((T[i], T3[i])))
        cl["disj%d" % j] = (T, T3, adj)
    return cl


def n_of(p):
    return {"same": 1, "meet": 18, "disj0": 32 - p, "disj1": 144 + 3 * p, "disj2": 36 - 3 * p, "disj3": p}


def line_line(f1, f2, p):
    tot = Fr(0)
    mult = n_of(p)
    for name, (T1, T2, adj) in pair_classes().items():
        ip = ip_factory(adj)
        tot += mult[name] * sum(tens_ip5(t1, t2, ip) for t1 in f1(T1) for t2 in f2(T2))
    return 231 * tot


def vertex_classes():
    """Classes of a vertex x relative to the line T: (multiplicity, adjacency, name of x)."""
    out = []
    for pt in T:
        out.append((1, line_adj(T), pt))                                   # x = that point
        out.append((12, line_adj(T) | {frozenset(("x", pt))}, "x"))        # x adjacent to that point only
    out.append((60, line_adj(T), "x"))                                     # x adjacent to no point
    return out


def trace_pairing(t, ip, weight):
    """<sym(g x A), sym(u_t)> = (1/10) sum_{i<j} (u_i,u_j) <A, sym(rest)>, with <A, sym(u_r)> = weight(r)."""
    s = Fr(0)
    for i, j in combinations(range(5), 2):
        rest = tuple(t[k] for k in range(5) if k not in (i, j))
        s += ip(t[i], t[j]) * weight(rest)
    return s / 10


def with_gV3(f):
    """<gV3, sum over lines of terms f>."""
    tot = Fr(0)
    for mult, adj, xname in vertex_classes():
        ip = ip_factory(adj)
        for t in f(T):
            tot += mult * trace_pairing(t, ip, lambda r: ip(xname, r[0]) * ip(xname, r[1]) * ip(xname, r[2]))
    return 231 * tot


def qval(v, T2, adj):
    """(q_T2, u_v) = 4, -2, 1."""
    if v in T2:
        return 4
    return -2 if any(frozenset((v, w)) in adj for w in T2) else 1


def with_gS3(f, p):
    """<gS3, sum over lines of terms f>."""
    tot = Fr(0)
    mult = n_of(p)
    for name, (T1, T2, adj) in pair_classes().items():
        ip = ip_factory(adj)
        for t in f(T1):
            tot += mult[name] * trace_pairing(t, ip, lambda r: qval(r[0], T2, adj) * qval(r[1], T2, adj) * qval(r[2], T2, adj))
    return 231 * tot


def with_V5(f):
    tot = Fr(0)
    for mult, adj, xname in vertex_classes():
        ip = ip_factory(adj)
        tot += mult * sum(tens_ip5((xname,) * 5, t, ip) for t in f(T))
    return 231 * tot


def gram(p):
    p = Fr(p)
    names = ["V5", "E32", "W311", "W221", "gV3", "gS3"]
    V3V3 = Fr(99 * (28 ** 3 - 14 * 8 ** 3 + 84))
    S3V3 = Fr(-8316)
    S3S3 = 1386 * (10 - p)
    c = Fr(D + 6, 10)
    M = {}
    M["V5", "V5"] = Fr(99 * (28 ** 5 - 14 * 8 ** 5 + 84))
    M["V5", "gV3"] = 28 * V3V3
    M["V5", "gS3"] = 28 * S3V3
    M["gV3", "gV3"] = c * V3V3
    M["gV3", "gS3"] = c * S3V3
    M["gS3", "gS3"] = c * S3S3
    for nm, f in LINE_TENSORS.items():
        M["V5", nm] = with_V5(f)
        M[nm, "gV3"] = with_gV3(f)
        M[nm, "gS3"] = with_gS3(f, p)
        for nm2, f2 in LINE_TENSORS.items():
            if (nm2, nm) not in M:
                M[nm, nm2] = line_line(f, f2, p)
    return names, [[M[(a, b)] if (a, b) in M else M[(b, a)] for b in names] for a in names]


if __name__ == "__main__":
    names, M0 = gram(0)
    _, M1 = gram(1)
    print("Gram matrix, entry = constant + slope * pbar")
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if j >= i:
                print("  <%s,%s> = %s + (%s) pbar" % (a, b, M0[i][j], M1[i][j] - M0[i][j]))
    coef = [Fr(-13, 243), Fr(10, 243), Fr(20, 243), Fr(30, 243), Fr(0), Fr(0)]
    for p in (0, 5):
        _, M = gram(p)
        val = sum(coef[i] * coef[j] * M[i][j] for i in range(6) for j in range(6))
        print("control pbar=%d: |S5|^2 = %s, expected %s" % (p, val, 231 * (1020 - 30 * p)))
        # second control: <S5, gS3> = <S3, trace S5> = 4 |S3|^2
        v2 = sum(coef[i] * M[i][5] for i in range(6))
        print("          <S5,gS3> = %s, expected %s" % (v2, 4 * 1386 * (10 - p)))
    print("signs of the leading principal minors and determinant:")
    for p in [Fr(k, 4) for k in range(0, 49)]:
        _, M = gram(p)
        minors = [det([row[:k] for row in M[:k]]) for k in range(1, 7)]
        print("  pbar=%5.2f  %s  det6=%.4e" % (float(p), "".join("+" if x > 0 else ("0" if x == 0 else "-") for x in minors), float(minors[5])))
