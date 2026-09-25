"""Line-triple model for PQ(2,t,2) strongly regular graphs, general t (notes/99). Validated on BvLS (t = 10).

Relations between two lines: s (same), m (meet), 0, 1, 2, 3 (disjoint, number of edges between them).
Exact constants as functions of t; X[r1,r2,r3] = #{(L,M,N): rel(L,M)=r1, rel(L,N)=r2, rel(M,N)=r3} is built from
P (prisms), Q2 = sum_L pi(L)^2, the distance-2 distribution n_a (a = 0..3), and unknown counts of triples of
pairwise disjoint lines (9 points).  pi[key] = entries of the four projections of the line space (eigenvalues
3t+3, t+1+r, t+1+s of G_L, and its kernel 'ker').
"""
import itertools, math
import sympy as sp

R = ['s', 'm', 0, 1, 2, 3]


class Model:
    def __init__(self, t):
        self.t = t
        n = 2 * t * t + 4 * t + 3
        k = 2 * t + 2
        d = math.isqrt(1 + 8 * t)
        assert d * d == 1 + 8 * t
        r, s = sp.Rational(-1 + d, 2), sp.Rational(-1 - d, 2)
        f = sp.Rational(-(k + (n - 1) * s), r - s)
        g = n - 1 - f
        Lam = sp.Rational(n * (t + 1), 3)
        self.n, self.k, self.r, self.s, self.f, self.g, self.Lam = n, k, r, s, f, g, Lam

        def E(mult, th):   # idempotent entries: equal, adjacent, non-adjacent
            c = sp.Rational(mult, n)
            return (c, c * th / k, c * (-1 - th) / (n - k - 1))
        Es = {'0': (sp.Rational(1, n),) * 3, 'r': E(f, r), 's': E(g, s)}
        ev = {'0': 3 * t + 3, 'r': t + 1 + r, 's': t + 1 + s}

        def lineform(e3):
            e0, e1, e2 = e3
            return {'s': 3 * e0 + 6 * e1, 'm': e0 + 4 * e1 + 4 * e2,
                    0: 9 * e2, 1: e1 + 8 * e2, 2: 2 * e1 + 7 * e2, 3: 3 * e1 + 6 * e2}
        self.pi = {}
        for key in ('0', 'r', 's'):
            lf = lineform(Es[key])
            self.pi[key] = {rel: sp.nsimplify(lf[rel] / ev[key]) for rel in R}
        self.pi['ker'] = {rel: (1 if rel == 's' else 0) - sum(self.pi[kk][rel] for kk in ('0', 'r', 's')) for rel in R}

        self.P, self.Q2 = sp.symbols('P Q2')
        P = self.P
        self.na = sp.symbols('n0:4')
        self.alpha = {'s': 1, 'm': 3 * t, 0: Lam - 1 - 3 * t - 6 * t * t + 6 * t, 1: 6 * t * t - 12 * t, 2: 6 * t, 3: 0}
        self.beta = {'s': 0, 'm': 0, 0: -1, 1: 3, 2: -3, 3: 1}
        self.Npairs = {rel: Lam * self.alpha[rel] + self.beta[rel] * 2 * P for rel in R}
        nA, nB = 6 * P, Lam * 6 * t - 6 * P
        self.ndist2 = Lam * (n - 3 - 6 * t)
        abc = [(a, 6 - 2 * a, t - 5 + a) for a in range(4)]

        def S(fn):
            return sum(fn(a, b, c) * self.na[a] for (a, b, c) in abc)
        self.Xm = {(3, 1): (t - 1) * nA, (3, 0): 0, (3, 2): 0, (3, 3): 0,
                   (2, 2): 2 * nB + S(lambda a, b, c: a * (a - 1)),
                   (2, 1): 2 * (t - 2) * nB + S(lambda a, b, c: a * b),
                   (1, 1): (t - 1) * (t - 2) * nA + (t - 2) * (t - 3) * nB + S(lambda a, b, c: b * (b - 1)),
                   (2, 0): S(lambda a, b, c: a * c),
                   (1, 0): S(lambda a, b, c: b * c),
                   (0, 0): S(lambda a, b, c: c * (c - 1))}
        self.Xmm = {e: e * self.Npairs[e] for e in range(4)}
        self.Xmmm = n * (t + 1) * t * (t - 1)
        self.X9 = {ms: sp.Symbol('x' + ''.join(map(str, ms)))
                   for ms in itertools.combinations_with_replacement(range(4), 3)}

    def X(self, r1, r2, r3):
        tt = [r1, r2, r3]
        if 's' in tt:
            rest = [x for x in tt if x != 's']
            if len(rest) == 0:
                return self.Lam
            if len(rest) == 1:
                return 0
            return self.Npairs[rest[0]] if rest[0] == rest[1] else 0
        km = tt.count('m')
        e = sorted(x for x in tt if x != 'm')
        if km == 3:
            return self.Xmmm
        if km == 2:
            return self.Xmm[e[0]]
        if km == 1:
            return self.Xm[(e[1], e[0])]
        return self.X9[tuple(e)]

    def equations(self):
        P, Q2 = self.P, self.Q2
        eqs = []
        for r1 in R:
            for r2 in R:
                lhs = sum(self.X(r1, r2, r3) for r3 in R)
                rhs = (self.Lam * self.alpha[r1] * self.alpha[r2]
                       + (self.alpha[r1] * self.beta[r2] + self.alpha[r2] * self.beta[r1]) * 2 * P
                       + self.beta[r1] * self.beta[r2] * Q2)
                eqs.append(('marg', r1, r2, sp.expand(lhs - rhs)))
        for key in ('r', 's', 'ker'):
            for r3 in R:
                lhs = sum(self.pi[key][r1] * self.pi[key][r2] * self.X(r1, r2, r3) for r1 in R for r2 in R)
                eqs.append(('idem', key, r3, sp.expand(lhs - self.pi[key][r3] * self.Npairs[r3])))
        eqs.append(('na0', None, None, sum(self.na) - self.ndist2))
        eqs.append(('na1', None, None, sum(a * self.na[a] for a in range(4)) - self.Npairs[2]))
        return eqs

    def gram(self, key):
        return [[sum(self.pi[key][r3] * self.X(r1, r2, r3) for r3 in R) for r2 in R] for r1 in R]


if __name__ == '__main__':
    import sys
    t = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    M = Model(t)
    eqs = [e for e in M.equations() if e[3] != 0]
    unknowns = list(M.X9.values()) + list(M.na) + [M.Q2]
    A, b = sp.linear_eq_to_matrix([e[3] for e in eqs], unknowns)
    print(f't = {t}: {len(M.equations())} equations ({len(M.equations()) - len(eqs)} identically true), '
          f'rank {A.rank()} (augmented {A.row_join(b).rank()}) in {len(unknowns)} unknowns, P symbolic')
