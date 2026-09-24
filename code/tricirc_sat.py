"""General tri-circulant local-axiom geometries (falsification test for F17).
Parts P0,P1,P2 = Z_N; edges P_i -> P_{i+1} by an arbitrary (t+1)-set D_i. Exact conditions (derived in notes):
  (a) r_i(g) = #{(x,y) in D_{i+1} x D_{i+2} : x + y = g}  is 1 if -g in D_i, else in {0, 2}      (lambda, mu across)
  (b) F_i(g) = f_{D_i}(g) + f_{D_{i+2}}(g) in {0, 2} for g != 0, f_D(g) = #{(d,d') : d - d' = g}   (mu inside a part)
Symmetry breaking: 0 in D_0 and 0 in D_1 (shifts of parts 1 and 2).
All solutions are enumerated with blocking clauses (up to --max per N) and classified (twisted or not).
Usage: python tricirc_sat.py k Nmin Nmax [max_solutions_per_N]
"""
import sys, time
import numpy as np
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153


def build(N, k):
    pool = IDPool()
    cnf = CNF()
    x = lambda i, g: pool.id(('x', i % 3, g % N))
    for i in range(3):
        cnf.extend(CardEnc.equals([x(i, g) for g in range(N)], bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)
    cnf.append([x(0, 0)])
    cnf.append([x(1, 0)])

    def prod(a, b, key):
        p = pool.id(key)
        cnf.extend([[-p, a], [-p, b], [p, -a, -b]])
        return p
    for i in range(3):
        for g in range(N):
            lits = [prod(x(i + 1, h), x(i + 2, g - h), ('r', i, g, h)) for h in range(N)]
            s = x(i, -g)
            # s -> exactly 1 ; not s -> 0 or 2 (at most 2, and not exactly 1)
            for cl in CardEnc.equals(lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses:
                cnf.append([-s] + cl)
            cnf.extend(CardEnc.atmost(lits, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
            for j, l in enumerate(lits):
                cnf.append([s, -l] + lits[:j] + lits[j + 1:])
        for g in range(1, N):
            lits = []
            for D in (i, i + 2):
                for h in range(N):
                    lits.append(prod(x(D, h + g), x(D, h), ('f', i, D % 3, g, h)))
            cnf.extend(CardEnc.atmost(lits, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
            for j, l in enumerate(lits):
                cnf.append([-l] + lits[:j] + lits[j + 1:])
    return cnf, pool, x


def graph(N, Ds):
    n = 3 * N
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(3):
        j = (i + 1) % 3
        for a in range(N):
            for d in Ds[i]:
                u, v = i * N + a, j * N + (a + d) % N
                A[u, v] = A[v, u] = 1
    return A


def main():
    import rooted
    k, Nmin, Nmax = map(int, sys.argv[1:4])
    mx = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    for N in range(Nmin, Nmax + 1):
        t0 = time.time()
        cnf, pool, x = build(N, k)
        S = Cadical153(bootstrap_with=cnf.clauses)
        nsol, ntw, seen = 0, 0, set()
        while nsol < mx and S.solve():
            m = set(l for l in S.get_model() if l > 0)
            Ds = [sorted(g for g in range(N) if x(i, g) in m) for i in range(3)]
            A = graph(N, Ds)
            A2 = A @ A
            off = ~np.eye(len(A), dtype=bool)
            lam = set(A2[(A == 1) & off].tolist()); mu = set(A2[(A == 0) & off].tolist())
            assert lam == {1} and mu <= {0, 2}, (Ds, lam, mu)
            tw = not rooted.Rooted(A, 0).is_mate_system()
            nsol += 1
            ntw += tw
            if nsol <= 3:
                print(f'   N={N} sol: D={Ds} {"TWISTED" if tw else "untwisted"}', flush=True)
            S.add_clause([-x(i, g) for i in range(3) for g in Ds[i]])
        print(f'k={k} N={N}: {nsol} solutions (cap {mx}), twisted {ntw}  [{time.time()-t0:.1f}s]', flush=True)
        S.delete()


if __name__ == '__main__':
    main()
