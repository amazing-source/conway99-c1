"""C1, lab session, 2026-10-10. Probe (floating point, exploration, NOT a classification): how restrictive are the
rank-free positivity conditions on the double vertices of a short eigenvector of norm 18 or 20?

World (Codex's notes 171, 176): f = 1_P - 1_Q, |P| = |Q| = m (9 or 10), supports independent here; B = incidence P-Q
(row and column sums 4, two rows or two columns share at most 2). Defect multigraphs M_P = 2I + 2J - B B^t,
M_Q = 2I + 2J - B^t B: a pair of P with defect k lies in k outside vertices with at least two neighbours in P.
A DOUBLE vertex d has two neighbours T in P and two neighbours U in Q, with at most a matching between T and U.
With no triple or quadruple vertex the doubles are a bijection between the defect edges of P and those of Q.

Positivity (rank-free): for outside vertices v, v' with core columns a_v, a_v',
    7 Schur(E_{-4})(v,v') = 3 [v=v'] - A_vv' - k4(v,v'),   k4 = (a_v - 1/9)^t M4^-1 (a_v' - 1/9) - 1/9,
    7 Schur(E_3)(v,v')    = 4 [v=v'] + A_vv' - k3(v,v'),   k3 = (a_v - 2/11)^t M3^+ (a_v' - 2/11) + 2/11,
M4 = 3I - A_core + J/9 (positive definite), M3 = 4I + A_core - (2/11) J (kernel f). Both Schur matrices must be
positive semidefinite on every set of outside vertices; E_{-4} has rank 44, so the first has rank <= 44 - 2m.

The script takes a symmetric core, lists the candidate doubles, and searches the complete sets of doubles
(every defect edge of P and of Q used once) with D INDEPENDENT (A = 0 inside D), by depth-first search with the two
positivity tests at every node. It prints the number of nodes by depth. A zero count of complete sets says that, for
this core, the branch "no triple vertex, D independent" is impossible; it says nothing about the other branches.

python core_psd_probe.py <petersen20 | grid18> [node cap]"""
import sys, itertools, time
import numpy as np
TOL = 1e-9

def core(name):
    if name == "petersen20":                        # P_i ~ Q_j iff i = j or i ~ j in the Petersen graph
        V = list(itertools.combinations(range(5), 2)); m = 10; B = np.zeros((m, m), dtype=int)
        for i, a in enumerate(V):
            for j, b in enumerate(V):
                if i == j or not set(a) & set(b): B[i, j] = 1
        return B
    if name == "grid18":                            # P = the 9 cells of a 3 x 3 grid, Q = the 9 two-by-two subgrids
        cells = [(i, j) for i in range(3) for j in range(3)]; subs = [(r, c) for r in itertools.combinations(range(3), 2) for c in itertools.combinations(range(3), 2)]
        B = np.zeros((9, 9), dtype=int)
        for i, (a, b) in enumerate(cells):
            for j, (r, c) in enumerate(subs):
                if a in r and b in c: B[i, j] = 1
        return B
    raise SystemExit("unknown core")

def run(name, cap):
    B = core(name); m = len(B); n = 2 * m
    assert (B.sum(0) == 4).all() and (B.sum(1) == 4).all()
    GP = B @ B.T; GQ = B.T @ B
    assert (GP - 4 * np.eye(m, dtype=int)).max() <= 2 and (GQ - 4 * np.eye(m, dtype=int)).max() <= 2
    MP = 2 * np.eye(m, dtype=int) + 2 - GP; MQ = 2 * np.eye(m, dtype=int) + 2 - GQ
    print("core %s: m = %d; defect degrees %s / %s; eigenvalues of M_P: %s" % (name, m, sorted(set(MP.sum(0))), sorted(set(MQ.sum(0))), np.round(np.linalg.eigvalsh(MP.astype(float)), 3)))
    A = np.zeros((n, n)); A[:m, m:] = B; A[m:, :m] = B.T
    M4 = 3 * np.eye(n) - A + np.ones((n, n)) / 9; M3 = 4 * np.eye(n) + A - 2 / 11 * np.ones((n, n))
    print("   least eigenvalue of the E_-4 block of the core %.4f, of the E_3 block %.4f (kernel f)" % (np.linalg.eigvalsh(M4)[0], np.linalg.eigvalsh(M3)[0]))
    I4 = np.linalg.inv(M4); I3 = np.linalg.pinv(M3, rcond=1e-10, hermitian=True)
    EP = [(a, b) for a in range(m) for b in range(a + 1, m) for _ in range(MP[a, b])]      # defect edges with multiplicity
    EQ = [(a, b) for a in range(m) for b in range(a + 1, m) for _ in range(MQ[a, b])]
    print("   defect edges: %d on P, %d on Q (with multiplicity); double edges %d / %d" % (len(EP), len(EQ), sum(1 for a in range(m) for b in range(a + 1, m) if MP[a, b] == 2), sum(1 for a in range(m) for b in range(a + 1, m) if MQ[a, b] == 2)))
    # candidate doubles (T, U): at most a matching between T and U
    cand = []; col = []
    for iT, T in enumerate(EP):
        for iU, U in enumerate(EQ):
            sub = B[np.ix_(T, U)]
            if sub.sum(0).max() > 1 or sub.sum(1).max() > 1: continue
            a = np.zeros(n); a[list(T)] = 1; a[[m + u for u in U]] = 1
            cand.append((iT, iU, T, U)); col.append(a)
    col = np.array(col); nc = len(cand)
    K4 = (col - 1 / 9) @ I4 @ (col - 1 / 9).T - 1 / 9; K3 = (col - 2 / 11) @ I3 @ (col - 2 / 11).T + 2 / 11
    d4 = 3 - np.diag(K4); d3 = 4 - np.diag(K3)
    print("   candidate doubles %d of %d; diagonal Schur values: E_-4 in [%.3f, %.3f], E_3 in [%.3f, %.3f]" % (nc, len(EP) * len(EQ), d4.min(), d4.max(), d3.min(), d3.max()))
    ok1 = (d4 > -TOL) & (d3 > -TOL)
    # pairs (D independent): 2 x 2 blocks; combinatorial rule: at most two common core neighbours
    cc = col @ col.T
    p4 = (d4[:, None] * d4[None, :] - K4 ** 2 > -TOL); p3 = (d3[:, None] * d3[None, :] - K3 ** 2 > -TOL)
    comb = (cc <= 2); np.fill_diagonal(comb, False)
    pair_ok = comb & p4 & p3 & ok1[:, None] & ok1[None, :]
    print("   single candidates allowed %d; ordered pairs: combinatorially compatible %d, of which spectrally allowed %d (%.1f %%)" % (ok1.sum(), comb.sum(), pair_ok.sum(), 100.0 * pair_ok.sum() / max(1, comb.sum())))
    # depth-first search of complete independent sets of doubles
    byT = {}
    for c, (iT, iU, T, U) in enumerate(cand):
        if ok1[c]: byT.setdefault(iT, []).append(c)
    order = sorted(range(len(EP)), key=lambda t: len(byT.get(t, [])))
    nodes = [0] * (len(EP) + 1); sols = [0]; t0 = time.time(); total = [0]; stop = [False]
    S4 = 3 * np.eye(nc) - K4; S3 = 4 * np.eye(nc) - K3
    def rec(depth, chosen, usedU, alive):
        if stop[0]: return
        if depth == len(EP): sols[0] += 1; return
        t = order[depth]
        for c in byT.get(t, []):
            if not alive[c] or cand[c][1] in usedU: continue
            sel = chosen + [c]
            total[0] += 1
            if total[0] > cap: stop[0] = True; return
            ix = np.ix_(sel, sel)
            if np.linalg.eigvalsh(S4[ix])[0] < -TOL or np.linalg.eigvalsh(S3[ix])[0] < -TOL: continue
            nodes[depth + 1] += 1
            rec(depth + 1, sel, usedU | {cand[c][1]}, alive & pair_ok[c])
    rec(0, [], set(), ok1.copy())
    print("   search (D independent, no triple vertex): nodes passing both tests by depth: %s" % " ".join(str(x) for x in nodes[1:]))
    print("   complete sets of %d doubles: %d%s  [%d tests, %.0f s]" % (len(EP), sols[0], " (STOPPED at the node cap)" if stop[0] else "", total[0], time.time() - t0))

if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2000000)
