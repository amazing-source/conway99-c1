"""Exact SAT encoding of "complete this partial graph to a strongly regular graph (v, k, lam, mu)".

Night of 13-14 October 2026. One process; memory: the clause list is held in RAM (declared bound 2 GB).

A partial graph is a symmetric table with entries True, False or None (unknown). Every unknown pair gets one
Boolean variable. For every pair u < v the number of common neighbours must be lam if u ~ v and mu otherwise, and
every vertex must have degree k. Counters are sequential counters with full equivalence, so that "at least" and
"at most" can both be asserted. Constants are propagated at encoding time.

Instances:
  selftest      v = 9, k = 4, lam = 1, mu = 2, nothing fixed: must be SAT (the 3 x 3 grid).
  affine        srg(99,14,1,2) seen from a vertex x at which all 14 matchings respect the blocks (target T1).
"""
import itertools
import sys

T, F = "T", "F"


class Enc:
    def __init__(self):
        self.nv = 0
        self.clauses = []

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, *lits):
        self.clauses.append(lits)

    @staticmethod
    def neg(a):
        if a == T:
            return F
        if a == F:
            return T
        return -a

    def AND(self, a, b):
        if a == F or b == F:
            return F
        if a == T:
            return b
        if b == T:
            return a
        if a == b:
            return a
        if a == -b:
            return F
        v = self.new()
        self.add(-v, a)
        self.add(-v, b)
        self.add(v, -a, -b)
        return v

    def OR(self, a, b):
        return self.neg(self.AND(self.neg(a), self.neg(b)))

    def assert_true(self, a):
        if a == T:
            return
        if a == F:
            self.add()          # empty clause
        else:
            self.add(a)

    def assert_false(self, a):
        self.assert_true(self.neg(a))

    def count_ge(self, terms, jmax):
        """Return g[0..jmax] with g[j] equivalent to (at least j of the terms are true)."""
        g = [T] + [F] * jmax
        for t in terms:
            new = [T]
            for j in range(1, jmax + 1):
                new.append(self.OR(g[j], self.AND(t, g[j - 1])))
            g = new
        return g

    def assert_equiv(self, a, b):
        """a <-> b for literals or constants."""
        if a in (T, F) and b in (T, F):
            if a != b:
                self.add()
            return
        if a == T:
            self.assert_true(b)
        elif a == F:
            self.assert_false(b)
        elif b == T:
            self.assert_true(a)
        elif b == F:
            self.assert_false(a)
        else:
            self.add(-a, b)
            self.add(a, -b)


def encode(n, k, lam, mu, fixed):
    """fixed: dict {(u, v): bool} for u < v. Returns (enc, var) with var[(u, v)] a literal or T/F."""
    enc = Enc()
    e = {}
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in fixed:
                e[(u, v)] = T if fixed[(u, v)] else F
            else:
                e[(u, v)] = enc.new()

    def E(u, v):
        return e[(u, v)] if u < v else e[(v, u)]

    # degrees
    for u in range(n):
        g = enc.count_ge([E(u, w) for w in range(n) if w != u], k + 1)
        enc.assert_true(g[k])
        enc.assert_false(g[k + 1])
    # common neighbours
    hi = max(lam, mu)
    for u in range(n):
        for v in range(u + 1, n):
            terms = [enc.AND(E(u, w), E(v, w)) for w in range(n) if w != u and w != v]
            g = enc.count_ge(terms, hi + 1)
            enc.assert_false(g[hi + 1])
            enc.assert_true(g[min(lam, mu)])
            a = e[(u, v)]
            # adjacent <-> exactly lam ; non-adjacent <-> exactly mu
            if lam < mu:
                # count >= lam always, count <= mu always; adjacent <-> not (count >= lam + 1); and count in {lam, mu}
                enc.assert_equiv(a, enc.neg(g[lam + 1]))
                for j in range(lam + 1, mu):
                    # count >= lam + 1 implies count >= mu
                    enc.assert_true(enc.OR(enc.neg(g[lam + 1]), g[mu]))
            else:
                enc.assert_equiv(a, g[mu + 1])
                for j in range(mu + 1, lam):
                    enc.assert_true(enc.OR(enc.neg(g[mu + 1]), g[lam]))
    return enc, e


def write_dimacs(enc, path):
    with open(path, "w") as f:
        f.write("p cnf %d %d\n" % (enc.nv, len(enc.clauses)))
        for c in enc.clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def instance_selftest():
    return 9, 4, 1, 2, {}


def local_view(matching):
    """srg(99,14,1,2) seen from x = vertex 0. Inner vertices 1..14: block b in 0..6, side s in 0,1 -> 1 + 2b + s.
    Outer vertices: unordered pairs of inner vertices in different blocks.
    matching(a, b) -> the inner vertex paired with b by the matching M_a (b not in the block of a)."""
    inner = list(range(1, 15))
    mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in inner}
    outer = [(a, b) for a in inner for b in inner if a < b and mate[a] != b]
    idx = {p: 15 + i for i, p in enumerate(outer)}
    n = 15 + len(outer)
    assert n == 99
    fixed = {}

    def setf(u, v, val):
        if u > v:
            u, v = v, u
        assert fixed.get((u, v), val) == val
        fixed[(u, v)] = val

    for a in inner:
        setf(0, a, True)
        for b in inner:
            if a < b:
                setf(a, b, mate[a] == b)
    for p in outer:
        setf(0, idx[p], False)
        for c in inner:
            setf(c, idx[p], c in p)
    for p, q in itertools.combinations(outer, 2):
        common = set(p) & set(q)
        if len(common) == 1:
            (a,) = common
            (b,) = set(p) - common
            (b2,) = set(q) - common
            setf(idx[p], idx[q], matching(a, b) == b2)
    return n, 14, 1, 2, fixed, mate, outer, idx


def instance_affine():
    mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in range(1, 15)}
    n, k, lam, mu, fixed, _, _, _ = local_view(lambda a, b: mate[b])
    return n, k, lam, mu, fixed


if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    n, k, lam, mu, fixed = {"selftest": instance_selftest, "affine": instance_affine}[name]()
    enc, e = encode(n, k, lam, mu, fixed)
    write_dimacs(enc, out)
    free = sum(1 for x in e.values() if x not in (T, F))
    print("instance %s: n=%d, free pairs=%d, variables=%d, clauses=%d" % (name, n, free, enc.nv, len(enc.clauses)))
