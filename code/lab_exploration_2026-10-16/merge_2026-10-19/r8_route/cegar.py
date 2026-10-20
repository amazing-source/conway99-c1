"""CEGAR pilot (LAB 20/10/2026): combinatorial model (C1, C1', C2') + spectral cuts on the label block.

Model: four exact stars 0..3 plus the first nx labels {4,t} (nx = 8: R8; --five: letter 4 exact too).
Spectral facts used (spectral.py, verified on real srg(243)): T_S = T0_S - Gamma_S >= 0 and U_S = U0_S + Gamma_S >= 0 in
every srg(n,k,1,2), for every set S of labels (principal submatrices of PSD Schur complements).  For an integer vector
q on a label subset Y:  q^T (D_T T_Y) q >= 0  <=>  sum_{i<j in Y} q_i q_j x_ij <= floor(q^T (D_T T0_Y) q / (2 D_T)),
and q^T (D_U U_Y) q >= 0  <=>  sum_{i<j} (-q_i q_j) x_ij <= floor(q^T (D_U U0_Y) q / (2 D_U))   (D_T T0, D_U U0
integral; integer rounding of the right-hand side is valid because the left-hand side is an integer).
Loop: SAT solve (incremental CaDiCaL 1.9.5 in pysat) -> model -> independent combinatorial check -> eigenvalues of
T_S, U_S -> for each negative direction, a sparse cut (greedy sub-block, integer rounding, exact violation check)
-> PB-to-CNF (pbenc.py) -> repeat.  A model with T_S, U_S >= 0 is reported with rank_Q T_S (<= g-k needed), rank_Q U_S
(<= f-k) and rank_7(8 T_S) (<= 28 needed for Conway, archive window r_7 <= 43).
--planted F1,F2,...: real structures (K = 22) on the same labels; every new cut is evaluated on them and must hold
(validity control of the cut generator).  --cuts-in/--cuts-out: cuts are stored by labels (reusable by any model that
contains those labels).
usage: python cegar.py <out jsonl> [--K 14] [--nx 0] [--five] [--implied L4B,XPAIR] [--tsolve 60] [--budget 280]
                        [--cuts-in f] [--cuts-out f] [--percut 6] [--planted files] [--continue N]"""
import itertools
import json
import os
import sys
import threading
import time

import numpy as np
from pysat.solvers import Solver

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pbenc  # noqa: E402
import r8lib  # noqa: E402
import spectral  # noqa: E402


def opt(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def rank_mod(Mx, p):
    A = [[int(x) % p for x in row] for row in Mx]
    rows, cols = len(A), len(A[0]) if A else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


class Cegar:
    def __init__(self):
        self.K = int(opt("--K", "14"))
        nx = int(opt("--nx", "0"))
        self.M = M = r8lib.Model(self.K, nx=nx, exact_extra=(4,) if "--five" in sys.argv else ())
        implied = [t for t in opt("--implied", "").split(",") if t]
        F, info = r8lib.encode(M, implied=implied)
        self.nv = F.n
        self.sv = Solver(name="cadical195", bootstrap_with=F.clauses)
        del F
        T0, U0, Pi, t, self.rkT, self.rkU = spectral.label_blocks(self.K, M.S)
        self.DT, self.DU = spectral.integral_scale(T0), spectral.integral_scale(U0)
        self.T0i = np.round(self.DT * T0).astype(np.int64)
        self.U0i = np.round(self.DU * U0).astype(np.int64)
        self.T0, self.U0, self.t = T0, U0, t
        if self.K == 14:
            # cross-check with the archive's closed form T = 3I - Gamma - K, 8K_ab = -2 + 3|a n b| + m_ab
            for i, a in enumerate(M.S):
                for j, b in enumerate(M.S):
                    inter = len(a & b)
                    mm = sum(1 for y in a for z in b if z == (y ^ 1))
                    assert abs(T0[i, j] - ((3 if i == j else 0) - (-0.25 + 0.375 * inter + 0.125 * mm))) < 1e-9
        self.cuts = []
        self.planted = []
        if opt("--planted"):
            for f in opt("--planted").split(","):
                d = json.load(open(f))
                labs = [frozenset(x) for x in d["labels"]]
                G = np.zeros((M.n, M.n), dtype=np.int64)
                for i, j in d["edges"]:
                    if labs[i] in M.idx and labs[j] in M.idx:
                        a, b = M.idx[labs[i]], M.idx[labs[j]]
                        G[a, b] = G[b, a] = 1
                self.planted.append((os.path.basename(f), G))
        if opt("--cuts-in") and os.path.exists(opt("--cuts-in")):
            for line in open(opt("--cuts-in")):
                c = json.loads(line)
                if all(frozenset(p[0]) in M.idx and frozenset(p[1]) in M.idx for p in c["terms"]):
                    self.add_cut(c, store=False)

    def newvar(self):
        self.nv += 1
        return self.nv

    def add_cut(self, c, store=True):
        M = self.M
        lits, ws = [], []
        for la, lb, w in c["terms"]:
            i, j = M.idx[frozenset(la)], M.idx[frozenset(lb)]
            lits.append(M.var(i, j))
            ws.append(w)
        cl, ok = pbenc.pb_le(self.newvar, lits, ws, c["bound"])
        for cc in cl:
            self.sv.add_clause(cc)
        self.cuts.append(c)
        if store and opt("--cuts-out"):
            with open(opt("--cuts-out"), "a") as fh:
                fh.write(json.dumps(c) + "\n")
        return len(cl)

    def solve(self, T):
        # CaDiCaL 1.9.5 in pysat has no interrupt: time limit by slices of 20 000 conflicts (resumable)
        t0 = time.time()
        while True:
            self.sv.conf_budget(20000)
            st = self.sv.solve_limited()
            if st is not None or time.time() - t0 >= T:
                return st, round(time.time() - t0, 2)

    def make_cut(self, kind, Gm, z):
        """sparse integer cut from direction z (negative for T or U at the current model Gm)."""
        n = self.M.n
        base = self.T0i if kind == "T" else self.U0i
        D = self.DT if kind == "T" else self.DU
        sgn = -1 if kind == "T" else 1
        Mi = base + sgn * D * Gm                    # D * T_S or D * U_S, integral

        def bad(Y):
            return np.linalg.eigvalsh(Mi[np.ix_(Y, Y)].astype(float)).min() < -1e-7

        order = list(np.argsort(-np.abs(z)))
        Y = []
        for y in order:
            Y.append(int(y))
            if len(Y) >= 2 and bad(Y):
                break
        if not bad(Y):
            return None
        changed = True
        while changed:
            changed = False
            for y in list(Y):
                Z = [u for u in Y if u != y]
                if len(Z) >= 2 and bad(Z):
                    Y = Z
                    changed = True
                    break
        ev, V = np.linalg.eigh(Mi[np.ix_(Y, Y)].astype(float))
        zz = V[:, 0] / np.abs(V[:, 0]).max()
        for s in range(1, 60):
            q = np.round(s * zz).astype(np.int64)
            if not q.any():
                continue
            val = int(q @ Mi[np.ix_(Y, Y)] @ q)
            if val < 0:
                break
        else:
            return None
        # cut: q^T (base_Y + sgn D Gamma_Y) q >= 0  <=>  sum_{i<j} (-sgn q_i q_j) x_ij <= floor(q^T base_Y q / (2D))
        c0 = int(q @ base[np.ix_(Y, Y)] @ q)
        bound = c0 // (2 * D)
        terms = []
        S = self.M.S
        for a, b in itertools.combinations(range(len(Y)), 2):
            w = int(-sgn * q[a] * q[b])
            if w:
                terms.append([sorted(S[Y[a]]), sorted(S[Y[b]]), w])
        lhs = sum(w * int(Gm[self.M.idx[frozenset(la)], self.M.idx[frozenset(lb)]]) for la, lb, w in terms)
        assert lhs > bound, "cut not violated"
        cut = {"kind": kind, "Y": [sorted(S[y]) for y in Y], "q": [int(x) for x in q], "terms": terms,
               "bound": bound, "viol": lhs - bound}
        for name, Gp in self.planted:
            lp = sum(w * int(Gp[self.M.idx[frozenset(la)], self.M.idx[frozenset(lb)]]) for la, lb, w in terms)
            if lp > bound:
                raise SystemExit("INVALID CUT on planted %s: %s" % (name, json.dumps(cut)))
        return cut


def main():
    out = sys.argv[1]
    C = Cegar()
    M = C.M
    tsolve = float(opt("--tsolve", "60"))
    budget = float(opt("--budget", "280"))
    percut = int(opt("--percut", "6"))
    cont = int(opt("--continue", "0"))
    t_start = time.time()
    it = 0
    psd_found = 0
    print(json.dumps({"labels": M.n, "K": C.K, "D_T": C.DT, "D_U": C.DU, "cuts_loaded": len(C.cuts),
                      "planted": [p[0] for p in C.planted]}), flush=True)
    while time.time() - t_start < budget:
        it += 1
        st, ts = C.solve(min(tsolve, max(5.0, budget - (time.time() - t_start))))
        rec = {"it": it, "solve": {True: "SAT", False: "UNSAT", None: "TIMEOUT"}[st], "solve_s": ts,
               "cuts_total": len(C.cuts)}
        if st is not True:
            print(json.dumps(rec), flush=True)
            with open(out, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            break
        model = C.sv.get_model()
        E = [p for p in M.pairs if model[M.var(*p) - 1] > 0]
        bad = M.check(E)
        assert not bad, bad[:3]
        Gm = np.zeros((M.n, M.n), dtype=np.int64)
        for i, j in E:
            Gm[i, j] = Gm[j, i] = 1
        Tm = C.T0 - Gm
        Um = C.U0 + Gm
        evT, VT = np.linalg.eigh(Tm)
        evU, VU = np.linalg.eigh(Um)
        rec.update({"minT": round(float(evT[0]), 4), "negT": int((evT < -1e-7).sum()), "minU": round(float(evU[0]), 4),
                    "negU": int((evU < -1e-7).sum())})
        newc = []
        for kind, ev, V in (("T", evT, VT), ("U", evU, VU)):
            for k in range(min(percut, int((ev < -1e-7).sum()))):
                c = C.make_cut(kind, Gm, V[:, k])
                if c and all(c["terms"] != d["terms"] or c["bound"] != d["bound"] for d in newc):
                    newc.append(c)
        if not newc and (rec["negT"] or rec["negU"]):
            rec["note"] = "no integral cut found"
        if rec["negT"] == 0 and rec["negU"] == 0:
            T8 = np.round(C.DT * Tm).astype(np.int64)
            rq = max(rank_mod(T8.tolist(), 1000003), rank_mod(T8.tolist(), 998244353))
            U8 = np.round(C.DU * Um).astype(np.int64)
            ru = max(rank_mod(U8.tolist(), 1000003), rank_mod(U8.tolist(), 998244353))
            r7 = rank_mod((np.round(8 * Tm).astype(np.int64) % 7).tolist(), 7) if C.K == 14 else None
            rec.update({"PSD": True, "rankT": rq, "rankU": ru, "rank7_8T": r7, "need": [C.rkT, C.rkU, 28]})
            psd_found += 1
            json.dump({"K": C.K, "labels": [sorted(l) for l in M.S], "edges": [list(p) for p in E]},
                      open(out + ".psd%d.json" % psd_found, "w"))
            if psd_found > cont:
                print(json.dumps(rec), flush=True)
                with open(out, "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
                break
            C.sv.add_clause([-M.var(*p) if p in set(E) else M.var(*p) for p in M.pairs])   # no-good, next model
        ncl = 0
        for c in newc:
            ncl += C.add_cut(c)
        rec.update({"new_cuts": len(newc), "new_clauses": ncl, "supports": sorted(len(c["Y"]) for c in newc)})
        print(json.dumps(rec), flush=True)
        with open(out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("iterations %d, cuts %d, total %.1f s" % (it, len(C.cuts), time.time() - t_start), flush=True)


if __name__ == "__main__":
    main()
