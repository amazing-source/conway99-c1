"""C1, lab session, 2026-10-12. Norm 18, rank-free: which outside vertices can a core carry?

World of an integral (-4)-eigenvector f = 1_P - 1_Q of norm 18 of a srg(99,14,1,2): P, Q independent 9-sets
(NOTE 17.98), B = incidence P x Q with row and column sums 4, two rows or two columns sharing at most 2 (26 cores,
work/c1_cost37_2026-10-09/cores_norm18_independent.json). An outside vertex v has the same number j of neighbours
in P and in Q (A f = -4 f); its core column is a_v = (T, U), |T| = |U| = j, with at most a matching between T and U
(an edge v - t lies in one triangle) and every pair of T (of U) of defect >= 1 (defect of a pair = 2 - number of its
common neighbours in the other support).

Rank-free positivity (floating point here; NOTE 17.97): with M4 = 3I - A_core + J/9 (positive definite) and
M3 = 4I + A_core - (2/11) J (kernel f),
    s4(v) = 3 - k4(v,v) >= 0,   k4 = (a - 1/9)^t M4^-1 (a - 1/9) - 1/9          (Schur complement of E_-4, times 7)
    s3(v) = 4 - k3(v,v) >= 0,   k3 = (a - 2/11)^t M3^+ (a - 2/11) + 2/11        (Schur complement of E_3 + <1>, times 7)
This script lists, for every core and j = 0..4, the number of candidate columns and how many pass the two
single-vertex tests, with the ranges of s4 and s3. j >= 5 is impossible for every core (s4 < 0, hand: NOTE of today).

python n18_types.py <cores_norm18_independent.json>          One process, seconds."""
import sys, json, itertools
import numpy as np
TOL = 1e-9


def analyse(B):
    m = len(B); n = 2 * m
    A = np.zeros((n, n)); A[:m, m:] = B; A[m:, :m] = B.T
    M4 = 3 * np.eye(n) - A + np.ones((n, n)) / 9; M3 = 4 * np.eye(n) + A - 2 / 11 * np.ones((n, n))
    I4 = np.linalg.inv(M4); I3 = np.linalg.pinv(M3, rcond=1e-10, hermitian=True)
    GP = B @ B.T; GQ = B.T @ B
    defP = 2 - GP + 0 * np.eye(m, dtype=int); defQ = 2 - GQ
    out = []
    for j in range(0, 6):
        tot = 0; ok = 0; r4 = [1e9, -1e9]; r3 = [1e9, -1e9]
        Ts = [T for T in itertools.combinations(range(m), j) if all(defP[a, b] >= 1 for a, b in itertools.combinations(T, 2))]
        Us = [U for U in itertools.combinations(range(m), j) if all(defQ[a, b] >= 1 for a, b in itertools.combinations(U, 2))]
        for T in Ts:
            for U in Us:
                if j:
                    sub = B[np.ix_(T, U)]
                    if sub.sum(0).max() > 1 or sub.sum(1).max() > 1: continue
                a = np.zeros(n); a[list(T)] = 1; a[[m + u for u in U]] = 1
                s4 = 3 - ((a - 1 / 9) @ I4 @ (a - 1 / 9) - 1 / 9); s3 = 4 - ((a - 2 / 11) @ I3 @ (a - 2 / 11) + 2 / 11)
                tot += 1
                r4 = [min(r4[0], s4), max(r4[1], s4)]; r3 = [min(r3[0], s3), max(r3[1], s3)]
                if s4 > -TOL and s3 > -TOL: ok += 1
        out.append((j, tot, ok, r4, r3))
    return out


def main():
    data = json.load(open(sys.argv[1])); classes = data["classes"]
    print("norm 18: %d cores; for every core and every j: candidate columns / passing both single-vertex tests; ranges of s4, s3" % len(classes))
    summary = {}
    for c in classes:
        B = np.array(c["incidence_rows_points_columns_blocks"], dtype=int)
        assert (B.sum(0) == 4).all() and (B.sum(1) == 4).all()
        res = analyse(B)
        line = "core %2d (aut %3d):" % (c["index"], c["automorphisms"])
        for j, tot, ok, r4, r3 in res:
            if tot == 0: line += "  j=%d: none" % j
            else: line += "  j=%d: %d/%d s4[%.2f,%.2f] s3[%.2f,%.2f]" % (j, ok, tot, r4[0], r4[1], r3[0], r3[1])
            summary.setdefault(j, [0, 0]); summary[j][0] += tot; summary[j][1] += ok
        print(line, flush=True)
    print("totals over the cores (candidates, passing): " + "; ".join("j=%d: %d, %d" % (j, v[0], v[1]) for j, v in sorted(summary.items())))


if __name__ == "__main__":
    main()
