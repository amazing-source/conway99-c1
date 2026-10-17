"""c = 1 cases closed by the 2-adic RANK condition (exploration, LAB 17/10/2026).  No positivity is used.
Necessary condition (c1_rank2adic.py, validated on data): Conway => rank_F2(N(Gamma)) <= 22, where
N(Gamma) = D' + U_r (I + Gamma) V_r (mod 2) is a 36 x 36 matrix over F_2, affine in Gamma.  The images s_0..s_3 of the
four star indicators always lie in its radical, so Conway needs K = 10 FURTHER radical vectors.
SAT model (CryptoMiniSat, native XOR clauses):
  local axioms of the four-star block (CNF of stars_rank.build: exact star counts, letter caps, common-neighbour caps);
  c(l) = 1: the rectangle multigraph M_0 at the root l is connected (one clause per cut of the 6 rectangles);
  E3: no rectangle with exactly 3 internal edges at the roots l and m (Codex's lemma);
  case: the rectangle profile at l (c1_cases.all_cases);
  rank: x_1..x_K in F_2^36, reduced echelon form (pivots increasing, zero at the pivots of the reduced star images),
        N(Gamma) x_k = 0 written with w = V_r x, g = Gamma w (AND gates Gamma_ij & w_j), rows U_r (w + g) + D' x = 0.
UNSAT => no four-star block of this case has rank <= 30: the case is IMPOSSIBLE in a Conway graph.
usage: python c1_sat2adic.py <case index | -> <seconds> [K=10] [--fix structure.json]"""
import itertools
import json
import os
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
import c1_sv1_cuts as C  # noqa: E402
import c1_cases as CS  # noqa: E402
import c1_rank2adic as R2  # noqa: E402
from stars_rank import build  # noqa: E402


def inv_mod2(M):
    n = len(M)
    A = [list(map(int, row)) + [int(i == j) for j in range(n)] for i, row in enumerate(np.array(M) % 2)]
    for c in range(n):
        pv = next(i for i in range(c, n) if A[i][c])
        A[c], A[pv] = A[pv], A[c]
        for i in range(n):
            if i != c and A[i][c]:
                A[i] = [a ^ b for a, b in zip(A[i], A[c])]
    return np.array([row[n:] for row in A], dtype=np.int64)


VINV = inv_mod2([[R2.V[i][j] % 2 for j in range(C.n)] for i in range(C.n)])
STAR_IMG = []
for y in C.STARS:
    z = np.array([1 if y in l else 0 for l in C.S], dtype=np.int64)
    STAR_IMG.append((VINV @ z % 2)[R2.REST] % 2)


def star_pivots():
    A = [list(map(int, s)) for s in STAR_IMG]
    piv = []
    r = 0
    for c in range(36):
        pv = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pv is None:
            continue
        A[r], A[pv] = A[pv], A[r]
        for i in range(len(A)):
            if i != r and A[i][c]:
                A[i] = [a ^ b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    return piv


class Model:
    def __init__(self, seed=1):
        rng = random.Random(seed)
        S, idx, e, F = build(list(C.STARS), rng)
        assert S == C.S
        self.e = e
        self.nv = F.n
        self.clauses = list(F.clauses)
        self.xors = []

    def var(self):
        self.nv += 1
        return self.nv

    def E(self, i, j):
        return self.e[(i, j)]

    def add_c1(self):
        """M_0 connected: every proper cut of the 6 root-l rectangles is crossed by an edge of H_l."""
        roots = [(2 * j, 2 * j + 1) for j in range(1, 7)]
        Q = [[C.IDX[frozenset((r, t))] for r in (0, 1) for t in rt] for rt in roots]
        for size in range(1, 6):
            for Sub in itertools.combinations(range(6), size):
                if 0 not in Sub:
                    continue
                ins = [i for k in Sub for i in Q[k]]
                out = [i for k in range(6) if k not in Sub for i in Q[k]]
                self.clauses.append([self.E(i, j) for i in ins for j in out])

    def add_e3_and_case(self, case):
        for (a0, a1) in ((0, 1), (2, 3)):
            roots = [(x, x + 1) for x in range(0, 14, 2) if x not in (a0, a1)]
            for k, rt in enumerate(roots):
                q = [C.IDX[frozenset((r, t))] for r in (a0, a1) for t in rt]
                prs = [self.E(i, j) for i, j in itertools.combinations(q, 2)]
                allowed = {0, 1, 2, 4} if case is None or (a0, a1) != (0, 1) else {case[k]}
                for bits in itertools.product((0, 1), repeat=6):
                    if sum(bits) not in allowed:
                        self.clauses.append([-v if b else v for v, b in zip(prs, bits)])

    def add_rank(self, K):
        n = C.n
        sp = star_pivots()
        x = [[self.var() for _ in range(36)] for _ in range(K)]
        # reduced echelon form
        free = [a for a in range(36) if a not in sp]
        p = [[self.var() for _ in free] for _ in range(K)]
        for k in range(K):
            for a in sp:
                self.clauses.append([-x[k][a]])
            self.clauses.append(list(p[k]))
            for u, v in itertools.combinations(p[k], 2):
                self.clauses.append([-u, -v])
            for ai, a in enumerate(free):
                self.clauses.append([-p[k][ai], x[k][a]])
                for kk in range(K):
                    if kk != k:
                        self.clauses.append([-p[k][ai], -x[kk][a]])
                for a2 in free[:ai]:
                    self.clauses.append([-p[k][ai], -x[k][a2]])
            if k + 1 < K:
                for ai in range(len(free)):
                    for bi in range(ai + 1):
                        self.clauses.append([-p[k][ai], -p[k + 1][bi]])
        # N(Gamma) x_k = 0
        for k in range(K):
            w = [self.var() for _ in range(n)]
            for i in range(n):
                self.xors.append(([w[i]] + [x[k][a] for a in range(36) if R2.V2[i, a]], False))
            g = [self.var() for _ in range(n)]
            for i in range(n):
                ands = []
                for j in range(n):
                    if j == i:
                        continue
                    a_ = self.var()
                    ge = self.E(i, j)
                    self.clauses += [[-a_, ge], [-a_, w[j]], [a_, -ge, -w[j]]]
                    ands.append(a_)
                self.xors.append(([g[i]] + ands, False))
            for r in range(36):
                vs = [x[k][r]] if R2.DP[r, r] else []
                for i in range(n):
                    if R2.U2[r, i]:
                        vs += [w[i], g[i]]
                self.xors.append((vs, False))
        return x

    def fix(self, G):
        for i, j in C.PAIRS:
            self.clauses.append([self.E(i, j) if G[i, j] else -self.E(i, j)])

    def solve(self, secs):
        s = Solver(time_limit=secs, threads=1)
        for c in self.clauses:
            s.add_clause(c)
        for vs, rhs in self.xors:
            # repeated variables cancel in a XOR
            cnt = {}
            for v in vs:
                cnt[v] = cnt.get(v, 0) ^ 1
            vv = [v for v, b in cnt.items() if b]
            if vv:
                s.add_xor_clause(vv, rhs)
            elif rhs:
                return False, None
        return s.solve()


def main():
    args = sys.argv[1:]
    fix = None
    if "--fix" in args:
        fix = args[args.index("--fix") + 1]
        del args[args.index("--fix"):args.index("--fix") + 2]
    ci = None if args[0] == "-" else int(args[0])
    secs = float(args[1])
    K = int(args[2]) if len(args) > 2 else 10
    t0 = time.time()
    M = Model()
    case = None if ci is None else CS.all_cases()[ci]
    if fix:
        d = json.load(open(fix))
        lab = [frozenset(t) for t in d["labels"]]
        eset = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for i, j in C.PAIRS:
            if frozenset((C.S[i], C.S[j])) in eset:
                G[i, j] = G[j, i] = 1
        M.fix(G)
        print("fixed structure: rank_F2(N) = %d -> radical %d, extra vectors beyond the stars %d" % (
            R2.rank2(R2.n_mod2(G)), 36 - R2.rank2(R2.n_mod2(G)), 32 - R2.rank2(R2.n_mod2(G))), flush=True)
        for s in STAR_IMG:
            assert not np.any((R2.n_mod2(G) @ s) % 2), "star image not in the radical"
    else:
        M.add_c1()
        M.add_e3_and_case(case)
    M.add_rank(K)
    print("case %s: %d vars, %d clauses, %d xors (%.0f s to build)" % (
        case, M.nv, len(M.clauses), len(M.xors), time.time() - t0), flush=True)
    sat, sol = M.solve(secs)
    status = "SAT" if sat is True else ("UNSAT" if sat is False else "UNKNOWN")
    print("result: %s (%.0f s)" % (status, time.time() - t0), flush=True)
    if sat:
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for i, j in C.PAIRS:
            if sol[M.E(i, j)]:
                G[i, j] = G[j, i] = 1
        T8 = 24 * np.eye(C.n, dtype=np.int64) - 8 * G - C.K8
        print("  witness: rank_F2(N) %d, rank_Q(T_S) %d, lambda_min T %.3f" % (
            R2.rank2(R2.n_mod2(G)), np.linalg.matrix_rank(T8.astype(float), tol=1e-6),
            C.perp_eigs(T8 / 8.0)[0].min()), flush=True)
        if not fix:
            fn = os.path.join(HERE, "unbiased_walks", "sat2adic_case%s.json" % ci)
            json.dump({"labels": [sorted(l) for l in C.S], "case": case,
                       "edges": [[i, j] for i, j in C.PAIRS if G[i, j]]}, open(fn, "w"))
            print("  saved", fn)


if __name__ == "__main__":
    main()
