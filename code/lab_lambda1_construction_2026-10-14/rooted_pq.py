"""Rooted SAT model of a strongly regular graph srg(v,k,1,mu) (a partial quadrangle PQ(2, k/2 - 1, mu)), 14/10/2026.

Vertex x = 0; its k neighbours 1..k form k/2 fixed lines {1,2}, {3,4}, ...; the other n = v - 1 - k vertices are
"outer" (all at distance 2 from x since the diameter is 2). Exact consequences used as constraints:
  * an outer vertex has exactly mu neighbours among 1..k, at most one per line (two would give lambda = 2);
  * every vertex has degree k; every pair has lambda = 1 or mu common neighbours according to adjacency.
Variables: a[i][o] (inner i ~ outer o) and e[o][p] (outer o ~ outer p). Products for the common-neighbour counts;
counts by sequential counters (Sinz) with conditional bounds. Symmetry breaking: the outer vertices are unlabelled,
so their columns (a[1..k][o], as bit vectors with inner vertex 1 most significant) are required to be lexicographically
non-increasing.
usage: python rooted_pq.py v k mu out.cnf       (prints the size; decode with rooted_decode.py)
"""
import itertools
import json
import sys


class CNF:
    def __init__(self, path=None):
        self.n = 0
        self.m = 0
        self.path = path
        self.fh = open(path + ".body", "w") if path else None
        self.cl = [] if path is None else None

    def var(self):
        self.n += 1
        return self.n

    def add(self, c):
        self.m += 1
        if self.fh:
            self.fh.write(" ".join(map(str, c)) + " 0\n")
        else:
            self.cl.append(c)

    def finish(self):
        """write the header and the streamed clauses into self.path"""
        import os
        self.fh.close()
        with open(self.path, "w") as out:
            out.write("p cnf %d %d\n" % (self.n, self.m))
            with open(self.path + ".body") as body:
                for line in body:
                    out.write(line)
        os.remove(self.path + ".body")

    def AND(self, a, b):
        if a is True:
            return b
        if b is True:
            return a
        if a is False or b is False:
            return False
        y = self.var()
        self.add([-y, a])
        self.add([-y, b])
        self.add([y, -a, -b])
        return y

    def counter(self, lits, upto):
        """sequential counter: returns R[m] (m = 1..upto+1) with R[m] <-> (at least m of lits true); constants handled"""
        const = sum(1 for l in lits if l is True)
        lits = [l for l in lits if l is not True and l is not False]
        # R[j][m] for prefix j
        prev = {}
        for j, x in enumerate(lits):
            cur = {}
            for m in range(1, upto + 2):
                # at least m among first j+1 = (at least m among first j) or (x and at least m-1 among first j)
                a = prev.get(m, False)
                b = True if m == 1 else prev.get(m - 1, False)
                bx = self.AND(x, b) if b is not False else False
                if a is False and bx is False:
                    cur[m] = False
                    continue
                if a is False:
                    cur[m] = bx
                    continue
                if bx is False:
                    cur[m] = a
                    continue
                y = self.var()
                self.add([-y, a, bx])
                self.add([y, -a])
                self.add([y, -bx])
                cur[m] = y
            prev = cur
        out = {}
        for m in range(1, upto + 2):
            mm = m - const
            out[m] = True if mm <= 0 else prev.get(mm, False)
        return out

    def bound(self, R, c, pre):
        """with R = counter outputs: sum == c under the premise list pre (literals that must fail for the bound to
        be waived, i.e. clauses pre + [...])"""
        if c >= 1:
            r = R[c]
            if r is False:
                self.add(list(pre))
            elif r is not True:
                self.add(list(pre) + [r])
        r = R[c + 1]
        if r is True:
            self.add(list(pre))
        elif r is not False:
            self.add(list(pre) + [-r])

    def exactly(self, lits, c, cond=None):
        """sum(lits) == c, under the condition cond (a literal) if given"""
        R = self.counter(lits, c)
        pre = [] if cond is None else [-cond]
        # at least c
        if c >= 1:
            r = R[c]
            if r is False:
                self.add(pre if pre else [])
            elif r is not True:
                self.add(pre + [r])
        # at most c
        r = R[c + 1]
        if r is True:
            self.add(pre if pre else [])
        elif r is not False:
            self.add(pre + [-r])


def lex_geq(F, x, y):
    """bit vectors x, y (most significant first): x >= y lexicographically"""
    # eq_j: x and y equal on the first j bits
    eq = True
    for xi, yi in zip(x, y):
        # if equal so far, then not (xi = 0 and yi = 1)
        if eq is True:
            F.add([xi, -yi])
        else:
            F.add([-eq, xi, -yi])
        # new eq = eq and (xi <-> yi)
        same = F.var()
        F.add([-same, -xi, yi])
        F.add([-same, xi, -yi])
        F.add([same, xi, yi])
        F.add([same, -xi, -yi])
        eq = same if eq is True else F.AND(eq, same)


def build(v, k, mu, path=None):
    F = CNF(path)
    n = v - 1 - k
    inner = list(range(k))                    # inner index i <-> vertex i+1
    mate = {i: i ^ 1 for i in inner}
    a = [[F.var() for o in range(n)] for i in inner]
    e = {}
    for o, p in itertools.combinations(range(n), 2):
        e[(o, p)] = e[(p, o)] = F.var()

    def E(o, p):
        return e[(o, p)]
    # outer: exactly mu inner neighbours, at most one per line
    for o in range(n):
        F.exactly([a[i][o] for i in inner], mu)
        for i in range(0, k, 2):
            F.add([-a[i][o], -a[i + 1][o]])
    # inner degree: k - 2 outer neighbours
    for i in inner:
        F.exactly([a[i][o] for o in range(n)], k - 2)
    # outer degree
    for o in range(n):
        F.exactly([a[i][o] for i in inner] + [E(o, p) for p in range(n) if p != o], k)
    # inner pairs (non-mates, non-adjacent): mu - 1 outer common neighbours
    for i, j in itertools.combinations(inner, 2):
        if mate[i] == j:
            continue
        F.exactly([F.AND(a[i][o], a[j][o]) for o in range(n)], mu - 1)
    # inner-outer pairs
    for i in inner:
        for o in range(n):
            prods = [F.AND(a[i][p], E(o, p)) for p in range(n) if p != o] + [a[mate[i]][o]]
            R = F.counter(prods, mu)
            F.bound(R, 1, [-a[i][o]])     # adjacent: lambda = 1 (the mate term is 0 by transversality)
            F.bound(R, mu, [a[i][o]])     # non-adjacent: mu (the mate counts if it is adjacent to o)
    # outer-outer pairs
    for o, p in itertools.combinations(range(n), 2):
        prods = [F.AND(a[i][o], a[i][p]) for i in inner] + [F.AND(E(o, q), E(p, q)) for q in range(n) if q not in (o, p)]
        R = F.counter(prods, mu)
        F.bound(R, 1, [-E(o, p)])
        F.bound(R, mu, [E(o, p)])
    # symmetry breaking: columns lexicographically non-increasing
    for o in range(n - 1):
        lex_geq(F, [a[i][o] for i in inner], [a[i][o + 1] for i in inner])
    return F, a, e, n


if __name__ == "__main__":
    v, k, mu, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    assert k * (k - 2) == mu * (v - k - 1), "parameters"
    F, a, e, n = build(v, k, mu, out)
    F.finish()
    meta = {"v": v, "k": k, "mu": mu, "n": n, "a": a, "e": {"%d,%d" % key: val for key, val in e.items() if key[0] < key[1]}}
    json.dump(meta, open(out + ".meta.json", "w"))
    print("srg(%d,%d,1,%d): %d outer vertices; %d variables, %d clauses" % (v, k, mu, n, F.n, F.m), flush=True)
