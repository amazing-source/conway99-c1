"""Well-scaled conic formulation of the moment hierarchy (srg_moments.Hierarchy), solved by Clarabel directly.
Variables w >= 0 with q = diag(rho^{e(Q)}) w (rho = k/n), PSD blocks congruence-scaled by rho^{-e(flag)}.
Usage: python3 msolve.py n k lam mu t [range]"""
import sys, math, time, numpy as np, scipy.sparse as sp, clarabel
from srg_moments import Hierarchy, canon, pid, nbmasks


def popc(x):
    return bin(x).count("1")


def build(H):
    rho = H.k / H.n
    sc = np.array([rho ** popc(Q) for Q in H.top])
    Aeq = H.equalities() * sc[None, :]
    U, Sv, Vt = np.linalg.svd(Aeq, full_matrices=False)
    Aeq = Vt[Sv > 1e-9 * Sv.max()]          # orthonormal basis of the row space (drops noise rows and redundancy)
    blocks = []
    for name, s, a, F, coef in H.blocks():
        B = H.block_matrices(s, a, F, coef) * sc[None, None, :]
        sig_e = popc(F[0] & ((1 << (s * (s - 1) // 2)) - 1)) if s > 1 else 0
        fe = np.array([popc(f) - sig_e for f in F], dtype=float)
        S = rho ** (-fe / 1.0)
        B = B * S[:, None, None] * S[None, :, None]
        mx = np.abs(B).max()
        if mx > 0:
            blocks.append((name, B / mx))
    return sc, Aeq, blocks


def solve(H, sc, Aeq, blocks, obj=None, sense=1, tol=1e-9, eps=0.0):
    """obj None: maximise tau with every block >= tau*I (returns tau*); else optimise obj.q with blocks >= -eps*I."""
    nq = len(H.top); nv = nq + 1          # last variable = tau
    rows_A, rows_b, cones = [], [], []
    E = np.hstack([np.vstack([sc[None, :], Aeq]), np.zeros((len(Aeq) + 1, 1))])
    rows_A.append(sp.csr_matrix(E)); rows_b.append(np.r_[1.0, np.zeros(len(Aeq))]); cones.append(clarabel.ZeroConeT(E.shape[0]))
    rows_A.append(sp.hstack([-sp.identity(nq), sp.csr_matrix((nq, 1))]).tocsr()); rows_b.append(np.zeros(nq))
    cones.append(clarabel.NonnegativeConeT(nq))
    # tau <= 1 ; and in optimisation mode tau = -eps
    if obj is None:
        rows_A.append(sp.csr_matrix(([1.0], ([0], [nq])), shape=(1, nv))); rows_b.append(np.array([1.0]))
        cones.append(clarabel.NonnegativeConeT(1))
    else:
        rows_A.append(sp.csr_matrix(([1.0], ([0], [nq])), shape=(1, nv))); rows_b.append(np.array([-eps]))
        cones.append(clarabel.ZeroConeT(1))
    for name, B in blocks:
        d = B.shape[0]; rr, tt = [], []
        for j in range(d):
            for i in range(j + 1):
                f = 1.0 if i == j else math.sqrt(2)
                rr.append(B[i, j] * f); tt.append(1.0 if i == j else 0.0)
        M = np.hstack([-np.array(rr), np.array(tt)[:, None]])     # s = svec(B w) - tau svec(I)
        rows_A.append(sp.csr_matrix(M)); rows_b.append(np.zeros(len(rr))); cones.append(clarabel.PSDTriangleConeT(d))
    A = sp.vstack(rows_A).tocsc(); b = np.concatenate(rows_b)
    c = np.zeros(nv)
    if obj is None:
        c[nq] = -1.0
    else:
        c[:nq] = sense * obj * sc
    st = clarabel.DefaultSettings(); st.verbose = False
    st.tol_gap_abs = st.tol_gap_rel = st.tol_feas = tol; st.max_iter = 500
    sol = clarabel.DefaultSolver(sp.csc_matrix((nv, nv)), c, A, b, cones, st).solve()
    x = np.array(sol.x)
    val = x[nq] if obj is None else sense * sol.obj_val
    return str(sol.status), val, x[:nq] * sc


if __name__ == "__main__":
    n, k, lam, mu, t = map(int, sys.argv[1:6])
    t0 = time.time(); H = Hierarchy(n, k, lam, mu, t); sc, Aeq, blocks = build(H)
    print(f"srg({n},{k},{lam},{mu}) order {t}: {len(H.top)} classes, {Aeq.shape[0]} eq rows, {len(blocks)} PSD blocks "
          f"(max {max(B.shape[0] for _, B in blocks)}), built {time.time() - t0:.0f}s", flush=True)
    st, tau, q = solve(H, sc, Aeq, blocks)
    print(f"max margin tau* = {tau:.3e} ({st})", f"{time.time() - t0:.0f}s", flush=True)
    if len(sys.argv) > 6 and t >= 6:
        bits = 0
        for (i, j) in [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]:
            bits |= 1 << pid(i, j)
        dens = H.dens[(6, canon(6, bits)[0])]
        lo = solve(H, sc, Aeq, blocks, dens, +1, eps=1e-7); hi = solve(H, sc, Aeq, blocks, dens, -1, eps=1e-7)
        print(f"prisms P in [{lo[1] * math.comb(n, 6):.4f}, {hi[1] * math.comb(n, 6):.4f}]  ({lo[0]}, {hi[0]})",
              f"{time.time() - t0:.0f}s", flush=True)
