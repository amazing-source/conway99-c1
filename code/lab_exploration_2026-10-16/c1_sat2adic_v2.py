"""2-adic rank condition, encoding v2 (exploration, LAB 17/10/2026).
Same necessary condition as c1_sat2adic.py (Conway => radical of N(Gamma) has dimension >= 14), written in LABEL space:
  W36 = column space of V_r (mod 2) = row space of U_r, Z8 = ker U_r = W36^perp (8-dim: 1, d_p + d_p', ...);
  y in W36 is a radical vector  <=>  (Gamma - F) y in Z8,   F = I + R D' P   (R: right inverse of U_r, P: left inverse
  of V_r on W36).  F is FIXED (no Gamma), so each radical vector costs: 8 XORs (y in W36), 8 pattern bits, 44 XORs
  (Gamma y)_i = (F y)_i + (Z p)_i, and the AND gates Gamma_ij & y_j.
Radical vectors beyond the stars: y_k = 0 on the star pivots 04, 14, 24, 34, reduced echelon form on the other 40 labels.
Incremental: K = 1, 2, ... radical vectors are added to the SAME solver (learnt clauses kept); the run reports the
largest K reached (SAT) and stops at UNSAT (=> radical < 4 + K for every structure of the case: K <= 10 closes it).
Symmetry breaking: lex-leader (on a prefix) for the 7 involutions (0 1), (2 3), mate flips of the five outer pairs.
usage: python c1_sat2adic_v2.py <case index> <seconds per step> [Kmax=10] [lex prefix=60]"""
import itertools
import json
import os
import sys
import time

import numpy as np
from pycryptosat import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402
import c1_cases as CS  # noqa: E402
import c1_rank2adic as R2  # noqa: E402
from c1_sat2adic import Model, inv_mod2  # noqa: E402

n = C.n


def gauss_inverse_parts():
    """W36 basis (columns of V_r), Z8 basis, and F = I + R D' P over F_2."""
    Vr = R2.V2 % 2                       # 44 x 36
    Ur = R2.U2 % 2                       # 36 x 44
    # P: left inverse of V_r (36 x 44): pick 36 independent rows of V_r
    rows = []
    A = []
    for i in range(n):
        cand = A + [list(Vr[i])]
        if R2.rank2(np.array(cand)) > len(A):
            A = cand
            rows.append(i)
        if len(rows) == 36:
            break
    Vsub = Vr[rows, :]                   # 36 x 36 invertible
    Vinv = inv_mod2(Vsub)
    P = np.zeros((36, n), dtype=np.int64)
    P[:, rows] = Vinv
    assert not np.any((P @ Vr - np.eye(36, dtype=np.int64)) % 2)
    # R: right inverse of U_r (44 x 36)
    cols = []
    A = []
    for j in range(n):
        cand = A + [list(Ur[:, j])]
        if R2.rank2(np.array(cand)) > len(A):
            A = cand
            cols.append(j)
        if len(cols) == 36:
            break
    Usub = Ur[:, cols]
    Uinv = inv_mod2(Usub)
    Rm = np.zeros((n, 36), dtype=np.int64)
    Rm[cols, :] = Uinv
    assert not np.any((Ur @ Rm - np.eye(36, dtype=np.int64)) % 2)
    F = (np.eye(n, dtype=np.int64) + Rm @ R2.DP @ P) % 2
    # Z8 = ker U_r
    from c1_sat2adic import star_pivots  # noqa: F401
    M = [list(r) for r in Ur]
    Z = []
    for v in itertools.product((0, 1), repeat=0):
        pass
    # nullspace of U_r
    A = [list(map(int, r)) for r in Ur]
    piv, r = [], 0
    for c in range(n):
        pv = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pv is None:
            continue
        A[r], A[pv] = A[pv], A[r]
        for i in range(len(A)):
            if i != r and A[i][c]:
                A[i] = [a ^ b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    for f in [c for c in range(n) if c not in piv]:
        v = [0] * n
        v[f] = 1
        for i, c in enumerate(piv):
            if A[i][f]:
                v[c] = 1
        Z.append(v)
    Z = np.array(Z, dtype=np.int64)       # 8 x 44
    return Vr, Z, F


VR, Z8, FM = gauss_inverse_parts()
ZPIV = [C.IDX[frozenset((s, 4))] for s in (0, 1, 2, 3)]


def check_formulation(G):
    """radical dimension from the label-space formulation, to compare with 36 - rank_F2(N)."""
    # y in W36 with (G - F) y in Z8  <=>  y = V_r x and U_r (G - F) V_r x = 0
    M = (R2.U2 @ ((G - FM) % 2) @ VR) % 2
    return 36 - R2.rank2(M)


class IncModel(Model):
    def __init__(self, case, lex=60):
        super().__init__(seed=1)
        self.add_c1()
        self.add_e3_and_case(case)
        self.add_lex(lex)
        opts = json.loads(os.environ.get("CMS_OPTS", "{}"))
        self.solver = Solver(threads=1, options=opts) if opts else Solver(threads=1)
        for c in self.clauses:
            self.solver.add_clause(c)
        self.clauses = []
        self.vecs = []
        self.pivs = []

    def add_lex(self, L):
        """Gamma <=lex g(Gamma) on the first L pairs (in PAIRS order) for the 7 generating involutions."""
        gens = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
        order = C.PAIRS[:L]
        for a, b in gens:
            sw = {a: b, b: a}
            img = {}
            for i in range(n):
                img[i] = C.IDX[frozenset(sw.get(t, t) for t in C.S[i])]
            seq = []
            for (i, j) in order:
                gi, gj = img[i], img[j]
                seq.append((self.E(i, j), self.E(min(gi, gj), max(gi, gj))))
            # standard lex chain: eq_k = (prefix equal); Gamma <= g(Gamma): if eq_{k-1} then x_k <= y_k
            prev = None
            for x, y in seq:
                if x == y:
                    continue
                if prev is None:
                    self.clauses.append([-x, y])
                    e = self.var()
                    # e <-> (x == y)
                    self.clauses += [[-e, -x, y], [-e, x, -y], [e, x, y], [e, -x, -y]]
                    prev = e
                else:
                    self.clauses.append([-prev, -x, y])
                    e = self.var()
                    self.clauses += [[-e, prev], [-e, -x, y], [-e, x, -y], [e, -prev, x, y], [e, -prev, -x, -y]]
                    prev = e

    def add_vector(self):
        k = len(self.vecs)
        y = [self.var() for _ in range(n)]
        p = [self.var() for _ in range(len(Z8))]
        cl, xs = [], []
        for i in ZPIV:
            cl.append([-y[i]])
        # y in W36: y . z = 0 for z in Z8
        for z in Z8:
            xs.append(([y[i] for i in range(n) if z[i]], False))
        # (Gamma y)_i + (F y)_i + (Z^t p)_i = 0
        for i in range(n):
            terms = []
            for j in range(n):
                if j == i:
                    continue
                a = self.var()
                g = self.E(i, j)
                cl += [[-a, g], [-a, y[j]], [a, -g, -y[j]]]
                terms.append(a)
            terms += [y[j] for j in range(n) if FM[i, j]]
            terms += [p[t] for t in range(len(Z8)) if Z8[t][i]]
            xs.append((terms, False))
        # reduced echelon form against the previous vectors: pivot of y_k = first nonzero label among FREE
        free = [i for i in range(n) if i not in ZPIV]
        b = [self.var() for _ in free]
        cl.append(list(b))
        for u, v in itertools.combinations(b, 2):
            cl.append([-u, -v])
        # BASIS=free: only "y_k = 1 at its own pivot, every other basis vector = 0 there" (independence, no canonical
        # form: easier to extend incrementally, still sound).  Default: reduced echelon form (canonical).
        rref = os.environ.get("BASIS", "rref") == "rref"
        for ai, i in enumerate(free):
            cl.append([-b[ai], y[i]])
            if rref:
                for i2 in free[:ai]:
                    cl.append([-b[ai], -y[i2]])
            for (yy, bb) in zip(self.vecs, self.pivs):        # previous vectors vanish at my pivot ...
                cl.append([-b[ai], -yy[i]])
        for (yy, bb) in zip(self.vecs, self.pivs):            # ... I vanish at theirs (and pivots increase)
            for ai, i in enumerate(free):
                cl.append([-bb[ai], -y[i]])
                if rref:
                    for ai2 in range(ai + 1):
                        cl.append([-bb[ai], -b[ai2]])
        for c in cl:
            self.solver.add_clause(c)
        for vs, rhs in xs:
            cnt = {}
            for v in vs:
                cnt[v] = cnt.get(v, 0) ^ 1
            vv = [v for v, t in cnt.items() if t]
            if vv:
                self.solver.add_xor_clause(vv, rhs)
        self.vecs.append(y)
        self.pivs.append(b)

    def solve(self, secs):
        self.solver.set_max_time(secs) if hasattr(self.solver, "set_max_time") else None
        return self.solver.solve()


def main():
    ci, step = int(sys.argv[1]), float(sys.argv[2])
    kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    lex = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    case = CS.all_cases()[ci]
    t0 = time.time()
    M = IncModel(case, lex)
    print("case %d %s: base model ready (%.0f s)" % (ci, case, time.time() - t0), flush=True)
    best = 0
    for K in range(1, kmax + 1):
        M.add_vector()
        sat, sol = M.solver.solve() if step <= 0 else solve_limited(M, step)
        status = "SAT" if sat is True else ("UNSAT" if sat is False else "UNKNOWN")
        msg = "  K = %2d extra radical vectors: %s (%.0f s)" % (K, status, time.time() - t0)
        if sat:
            best = K
            G = np.zeros((n, n), dtype=np.int64)
            for i, j in C.PAIRS:
                if sol[M.E(i, j)]:
                    G[i, j] = G[j, i] = 1
            msg += "; witness radical %d (check %d)" % (36 - R2.rank2(R2.n_mod2(G)), check_formulation(G))
        print(msg, flush=True)
        if sat is not True:
            break
    print("largest K reached: %d (Conway needs 10)" % best, flush=True)


def solve_limited(M, secs):
    return M.solver.solve(time_limit=secs)


if __name__ == "__main__":
    main()
