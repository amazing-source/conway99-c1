"""Gram QUOTIENT of the rectangles for partial component templates around a c = 1 line (exploration, LAB 17/10/2026).
Codex's quotient (c1-asymmetry-audit/notes/QUOTIENT_COMPOSANTES_RACINE_2026_10_16.txt, sections 2-4), extended to
PARTIAL templates.  Seven lines 0..6 through the root o, 21 rectangles Q_ij.  R = P^t T P (21 x 21), exactly:
  R_ee = 8 - 2 e(Q_e),  e in {0,1,2,4} (e != 3: Codex's lemma; e = 4 is a grid, R_ee = 0, row zero by positivity);
  R_ef = -W_ef in [-8,0] if e, f share a line;  R_ef = 4 - W_ef in [-8,4] if e, f are disjoint;  R_ef^2 <= R_ee R_ff;
  0 <= R <= 28 I;  for a component (or union of components) S of line i:  sum_{j in S} R[Q_ij, .] = 0   (T sigma = 0);
  two different components of line i: R[Q_ij, Q_ik] = 0 (no edges between them);  a singleton component is a grid.
A line with status 'c1' (and line 0) is connected: no grid among its rectangles, and every proper cut of its six
rectangles carries W >= 2 (degrees 8 - 2e are even).  An unassigned line only gives its star relation.
PSD cuts are lazy, with exact integer witnesses (rational elimination).  INFEASIBLE here = the node is impossible in
a Conway graph (all constraints are necessary).
usage: python c1_quotient.py '<json assignment>' [seconds]"""
import itertools
import json
import sys
import time
from fractions import Fraction

import numpy as np
from ortools.sat.python import cp_model

PAIRS7 = list(itertools.combinations(range(7), 2))
RID = {p: k for k, p in enumerate(PAIRS7)}


def rid(i, j):
    return RID[(i, j) if i < j else (j, i)]


def psd_witness(M):
    """exact: None if the integer symmetric matrix M is PSD, else an integer vector x with x^t M x < 0."""
    n = len(M)
    A = [[Fraction(int(M[i][j])) for j in range(n)] for i in range(n)]
    basis = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        p = A[i][i]
        if p < 0:
            v = basis[i]
            return _intvec(v)
        if p == 0:
            j = next((j for j in range(i + 1, n) if A[i][j] != 0), None)
            if j is not None:
                t = -(A[j][j] + 1) / (2 * A[i][j])
                v = [basis[j][k] + t * basis[i][k] for k in range(n)]
                return _intvec(v)
            continue
        for j in range(i + 1, n):
            f = A[j][i] / p
            if f == 0:
                continue
            for k in range(n):
                basis[j][k] -= f * basis[i][k]
            for k in range(i + 1, n):
                A[j][k] -= f * A[i][k]
    return None


def _intvec(v):
    from math import lcm, gcd
    den = lcm(*[x.denominator for x in v])
    w = [int(x * den) for x in v]
    g = gcd(*w) or 1
    return [x // g for x in w]


def build(assign, cuts=()):
    """assign: dict line(1..6) -> 'c1' or list block (with 0).  Returns (model, R vars)."""
    m = cp_model.CpModel()
    R = [[None] * 21 for _ in range(21)]
    status = {0: "c1"}
    status.update(assign)
    nongrid_forced = set()
    grid_forced = set()
    for i, st in status.items():
        if st == "c1":
            for j in range(7):
                if j != i:
                    nongrid_forced.add(rid(i, j))
        else:
            B = set(st)
            rest = [k for k in range(7) if k != i and k not in B]
            for blk in (sorted(B), rest):
                if len(blk) == 1:
                    grid_forced.add(rid(i, blk[0]))
    for e in range(21):
        dom = [0, 4, 6, 8]
        if e in nongrid_forced:
            dom = [4, 6, 8]
        if e in grid_forced:
            dom = [0]
        R[e][e] = m.NewIntVarFromDomain(cp_model.Domain.FromValues(dom), "d%d" % e)
    for e, f in itertools.combinations(range(21), 2):
        share = set(PAIRS7[e]) & set(PAIRS7[f])
        R[e][f] = R[f][e] = m.NewIntVar(-8, 0 if share else 4, "r%d_%d" % (e, f))
    allowed = [(a, b, c) for a in (0, 4, 6, 8) for b in (0, 4, 6, 8) for c in range(-8, 5) if c * c <= a * b]
    for e, f in itertools.combinations(range(21), 2):
        m.AddAllowedAssignments([R[e][e], R[f][f], R[e][f]], allowed)
    # relations and orthogonality
    for i in range(7):
        st = status.get(i)
        blocks = [[k for k in range(7) if k != i]]
        if st is not None and st != "c1":
            B = sorted(st)
            blocks = [B, [k for k in range(7) if k != i and k not in B]]
            for j in blocks[0]:
                for k in blocks[1]:
                    m.Add(R[rid(i, j)][rid(i, k)] == 0)
        for blk in blocks:
            for f in range(21):
                m.Add(sum(R[rid(i, j)][f] for j in blk) == 0)
    # connectivity of M_i for c1 lines (W = -R between rectangles of line i)
    for i, st in status.items():
        if st != "c1":
            continue
        others = [k for k in range(7) if k != i]
        for size in range(1, 6):
            for S in itertools.combinations(others, size):
                if others[0] not in S:
                    continue
                Sc = [k for k in others if k not in S]
                m.Add(sum(-R[rid(i, j)][rid(i, k)] for j in S for k in Sc) >= 2)
    for kind, vec in cuts:
        expr = sum(vec[a] * vec[b] * R[a][b] for a in range(21) for b in range(21) if vec[a] and vec[b])
        if kind == "lower":
            m.Add(expr >= 0)
        else:
            m.Add(expr <= 28 * sum(x * x for x in vec))
    return m, R


def _round_cuts(M, kind):
    """integer directions from the negative eigenvectors of M (kind 'lower') or 28I - M ('upper'), checked exactly."""
    A = np.array(M, dtype=float) if kind == "lower" else 28 * np.eye(21) - np.array(M, dtype=float)
    ev, V = np.linalg.eigh(A)
    out = []
    Ai = np.array(M, dtype=np.int64) if kind == "lower" else 28 * np.eye(21, dtype=np.int64) - np.array(M, dtype=np.int64)
    for k in range(21):
        if ev[k] > -1e-9:
            break
        v = V[:, k]
        for scale in (2, 3, 5, 8, 13):
            x = np.rint(v / np.max(np.abs(v)) * scale).astype(np.int64)
            if int(x @ Ai @ x) < 0:
                out.append((kind, [int(t) for t in x]))
                break
    return out


def add_cut(m, R, kind, vec):
    expr = sum(vec[a] * vec[b] * R[a][b] for a in range(21) for b in range(21) if vec[a] and vec[b])
    if kind == "lower":
        m.Add(expr >= 0)
    else:
        m.Add(expr <= 28 * sum(x * x for x in vec))


def quotient_status(assign, seconds=10.0, extra=None):
    """extra(model, R): optional additional constraints (e.g. the profile at line 0)."""
    t0 = time.time()
    m, R = build(assign)
    if extra is not None:
        extra(m, R)
    ncuts = 0
    while True:
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 1
        sv.parameters.max_time_in_seconds = max(0.5, seconds - (time.time() - t0))
        st = sv.Solve(m)
        if st == cp_model.INFEASIBLE:
            return "INFEASIBLE", ncuts, None
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return "UNKNOWN", ncuts, None
        M = [[sv.Value(R[a][b]) for b in range(21)] for a in range(21)]
        new = _round_cuts(M, "lower")
        if not new:
            w = psd_witness(M)
            if w is not None:
                new = [("lower", w)]
        if not new:
            new = _round_cuts(M, "upper")
            if not new:
                w = psd_witness([[28 * (a == b) - M[a][b] for b in range(21)] for a in range(21)])
                if w is not None:
                    new = [("upper", w)]
        if not new:
            return "FEASIBLE", ncuts, M
        for kind, vec in new:
            add_cut(m, R, kind, vec)
        ncuts += len(new)
        if time.time() - t0 > seconds:
            return "UNKNOWN", ncuts, None


def main():
    assign = {int(k): v for k, v in json.loads(sys.argv[1]).items()}
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    t0 = time.time()
    st, nc, M = quotient_status(assign, secs)
    print("quotient of %s: %s (%d PSD cuts, %.1f s)" % (assign, st, nc, time.time() - t0))
    if M is not None:
        print("  rank R =", np.linalg.matrix_rank(np.array(M, dtype=float)), " diag:", [M[e][e] for e in range(21)])


if __name__ == "__main__":
    main()
