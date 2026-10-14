"""Fourth moments of the vertex frame and the line frame in the (-4)-eigenspace of srg(99,14,1,2).

u_x = sqrt(63) E e_x, with (u_x, u_y) = 28, -8, 1 (equal, adjacent, non-adjacent); the eigenspace has dimension 44.
Four symmetric tensors of degree 4:
  G4  = sym(g x g)                          (g the metric)
  V4  = sum over vertices x of u_x^4
  E22 = sum over edges {x,y} of sym(u_x u_x u_y u_y)
  W4  = sum over lines {a,b,c} and marked point a of sym(u_a u_a u_b u_c)
(sum over lines of q_T^4 = -V4/9 + 2 E22/27 + 4 W4/27.)  Every entry of their Gram matrix is determined by the
parameters and by the numbers n_j of lines disjoint from a line with j edges to it, n_0 = 32 - p, n_1 = 144 + 3p,
n_2 = 36 - 3p, n_3 = p (NOTE_NIGHT F3), hence is affine in the average prism number pbar. The Gram matrix must be
positive semidefinite. Exact rational arithmetic.
"""
from fractions import Fraction as Fr
from itertools import permutations

D = 44


def perm4(m):
    return sum(m[0][s[0]] * m[1][s[1]] * m[2][s[2]] * m[3][s[3]] for s in permutations(range(4)))


def ip_factory(adj):
    def ip(x, y):
        if x == y:
            return 28
        return -8 if frozenset((x, y)) in adj else 1
    return ip


def tens_ip(t1, t2, ip):
    """<sym(u_t1), sym(u_t2)> for two 4-tuples of vertices."""
    return Fr(perm4([[ip(x, y) for y in t2] for x in t1]), 24)


def g_ip(t, ip):
    """<G4, sym(u_t)>."""
    a, b, c, d = t
    return Fr(ip(a, b) * ip(c, d) + ip(a, c) * ip(b, d) + ip(a, d) * ip(b, c), 3)


def line_adj(*lines):
    adj = set()
    for l in lines:
        for i in range(3):
            for j in range(i + 1, 3):
                adj.add(frozenset((l[i], l[j])))
    return adj


def e22_terms(line):
    a, b, c = line
    return [(a, a, b, b), (a, a, c, c), (b, b, c, c)]


def w4_terms(line):
    a, b, c = line
    return [(a, a, b, c), (b, b, a, c), (c, c, a, b)]


def pair_classes():
    """Relation classes of an ordered pair of lines: name -> (T, T', adjacency)."""
    T = ("a", "b", "c")
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


def line_line(f1, f2):
    """Per-class value of sum over terms of <.,.> ; returns dict class -> Fraction."""
    out = {}
    for name, (T, T2, adj) in pair_classes().items():
        ip = ip_factory(adj)
        out[name] = sum(tens_ip(t1, t2, ip) for t1 in f1(T) for t2 in f2(T2))
    return out


def total_lines(vals, p):
    n = {0: 32 - p, 1: 144 + 3 * p, 2: 36 - 3 * p, 3: p}
    per_line = vals["same"] + 18 * vals["meet"] + sum(n[j] * vals["disj%d" % j] for j in range(4))
    return 231 * per_line


def gram(p):
    p = Fr(p)
    names = ["G4", "V4", "E22", "W4"]
    M = {}
    # G4 with everything
    M["G4", "G4"] = Fr(D * D + 2 * D, 3)
    ipv = ip_factory(set())
    M["G4", "V4"] = 99 * g_ip(("x", "x", "x", "x"), ipv)
    T = ("a", "b", "c")
    ipl = ip_factory(line_adj(T))
    M["G4", "E22"] = 231 * sum(g_ip(t, ipl) for t in e22_terms(T))
    M["G4", "W4"] = 231 * sum(g_ip(t, ipl) for t in w4_terms(T))
    # V4 with V4
    M["V4", "V4"] = 99 * Fr(28 ** 4 + 14 * 8 ** 4 + 84)
    # V4 with line-based tensors: vertex x in T (3), adjacent to exactly one point (36), none (60)
    for nm, f in (("E22", e22_terms), ("W4", w4_terms)):
        tot = Fr(0)
        # x = a (by symmetry every point of T): 3 vertices
        ip = ip_factory(line_adj(T))
        tot += 3 * sum(tens_ip(("a",) * 4, t, ip) for t in f(T))
        ip = ip_factory(line_adj(T) | {frozenset(("x", "a"))})
        tot += 36 * sum(tens_ip(("x",) * 4, t, ip) for t in f(T))
        ip = ip_factory(line_adj(T))
        tot += 60 * sum(tens_ip(("x",) * 4, t, ip) for t in f(T))
        M["V4", nm] = 231 * tot
    M["E22", "E22"] = total_lines(line_line(e22_terms, e22_terms), p)
    M["E22", "W4"] = total_lines(line_line(e22_terms, w4_terms), p)
    M["W4", "W4"] = total_lines(line_line(w4_terms, w4_terms), p)
    return names, [[M[(a, b)] if (a, b) in M else M[(b, a)] for b in names] for a in names]


def det(m):
    m = [row[:] for row in m]
    n = len(m)
    d = Fr(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if m[r][i] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != i:
            m[i], m[piv] = m[piv], m[i]
            d = -d
        d *= m[i][i]
        for r in range(i + 1, n):
            f = m[r][i] / m[i][i]
            for c in range(i, n):
                m[r][c] -= f * m[i][c]
    return d


if __name__ == "__main__":
    names, M0 = gram(0)
    _, M1 = gram(1)
    print("Gram matrix, entry = constant + slope * pbar")
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if j >= i:
                print("  <%s,%s> = %s + (%s) pbar" % (a, b, M0[i][j], M1[i][j] - M0[i][j]))
    # control: |sum_T q_T^4|^2 = 231 (324 + 12 pbar)
    c = [Fr(0), Fr(-1, 9), Fr(2, 27), Fr(4, 27)]
    for p in (0, 5):
        _, M = gram(p)
        val = sum(c[i] * c[j] * M[i][j] for i in range(4) for j in range(4))
        print("control pbar=%d: |S4|^2 = %s, expected %s" % (p, val, 231 * (324 + 12 * p)))
    print("leading principal minors and determinant, pbar from 0 to 12:")
    for p in [Fr(k, 2) for k in range(0, 25)]:
        _, M = gram(p)
        minors = [det([row[:k] for row in M[:k]]) for k in range(1, 5)]
        print("  pbar=%5.2f  minors signs %s  det4=%.6e" % (float(p), "".join("+" if x > 0 else ("0" if x == 0 else "-") for x in minors), float(minors[3])))
