"""Lab session, 2026-10-12. Completions of a region by ALTERNATING PROJECTIONS (difference map), no SAT solver.

Support criterion (NOTE_SPREADFREE.md section 3): if a srg(243,22,1,2) A' agrees with A outside the pairs of a region F,
then A'_F = A_F + 9 B (Q - Q0) B^t, where the columns of B are an orthonormal basis of the eigenvectors of A supported
in F (w4 for the eigenvalue 4, then w5 for -5), Q0 = diag(1,...,1,0,...,0) and Q is ANY orthogonal projector of rank w4
in dimension d = w4 + w5. Conversely such a matrix with entries 0/1 and zero diagonal is a completion (same spectrum,
all-ones eigenvector). So the completions are the 0/1 points of a Grassmannian.
Two sets: S1 = {A_F + 9 B (Q - Q0) B^t}, S2 = {symmetric 0/1 matrices with zero diagonal}. Projection on S1: Q = projector on
the top w4 eigenvectors of B^t (M - A_F) B / 9 + Q0. Projection on S2: rounding. Difference map
x <- x + P1(2 P2(x) - x) - P2(x) from a random projector Q; a fixed point with P1 = P2 is a completion. Each completion
is checked (A^2 = 20I - A + 2J), compared with the references by isomorphism, and its automorphism group is computed.
This is a heuristic search: finding nothing proves nothing.

python dm_trade.py <out dir> <edge file> <region a-b[,c-d]> <number of starts> <iterations per start> <seed> [references ...]
environment: BETA (step, default 1), NEAR (if > 0: start from a random rotation of that size of the input), VERBOSE=1
Memory: small (matrices of size |F|)."""
import sys, os, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T
n = 243

if __name__ == "__main__":
    outdir, path, spec, nstart, niter, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    A0 = T.load(path); refs = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[7:]]
    F = [v for part in spec.split(",") for v in range(int(part.split("-")[0]), int(part.split("-")[1]) + 1)]; Fs = set(F); R = [v for v in range(n) if v not in Fs]
    w, U = np.linalg.eigh(A0.astype(float)); cols = []
    for ev in (4, -5):
        Ue = U[:, np.abs(w - ev) < 1e-6]; _, s, Vt = np.linalg.svd(Ue[R, :]); rank = int((s > 1e-8).sum()); N = Vt[rank:].T
        cols.append(Ue @ N)
    w4, w5 = cols[0].shape[1], cols[1].shape[1]; d = w4 + w5
    Bm = np.hstack(cols)[F, :]; assert np.allclose(Bm.T @ Bm, np.eye(d), atol=1e-8)
    AF = A0[np.ix_(F, F)].astype(float); Q0 = np.diag([1.0] * w4 + [0.0] * w5); m = len(F)
    print("region of %d vertices: w4 = %d, w5 = %d, Grassmannian of dimension %d" % (m, w4, w5, w4 * w5), flush=True)
    def P1(M):
        C = Bm.T @ (M - AF) @ Bm / 9.0 + Q0; C = (C + C.T) / 2; ev, V = np.linalg.eigh(C); Vt = V[:, d - w4:]
        return AF + 9.0 * Bm @ (Vt @ Vt.T - Q0) @ Bm.T
    def P2(M):
        X = ((M + M.T) / 2 > 0.5).astype(float); np.fill_diagonal(X, 0.0); return X
    beta = float(os.environ.get("BETA", "1.0")); near = float(os.environ.get("NEAR", "0"))
    rng = np.random.default_rng(seed); tally = collections.Counter(); t0 = time.time()
    for st in range(nstart):
        if near > 0:                                                    # start near the input: rotate Q0 by a random small rotation
            K = rng.standard_normal((d, d)) * near; K = K - K.T; ev, V = np.linalg.eigh(1j * K); Rot = (V @ np.diag(np.exp(-1j * ev)) @ V.conj().T).real
            Qm = Rot[:, :w4]
        else:
            G = rng.standard_normal((d, w4)); Qm, _ = np.linalg.qr(G)
        x = AF + 9.0 * Bm @ (Qm @ Qm.T - Q0) @ Bm.T; found = None; best = 1e9; ts = time.time()
        for it in range(niter):
            p2 = P2(x); p1 = P1(2 * p2 - x); gap = np.abs(p1 - p2).max(); best = min(best, float(np.abs(p1 - p2).sum()))
            if gap < 1e-6: found = p2; break
            x = x + beta * (p1 - p2)
        if os.environ.get("VERBOSE"): print("   start %d: %s after %d iterations (%.0f s), smallest distance between the two projections %.2f" % (st, "CONVERGED" if found is not None else "no convergence", it + 1, time.time() - ts, best), flush=True)
        if found is None: tally["no convergence"] += 1; continue
        A = A0.copy(); A[np.ix_(F, F)] = found.astype(np.int64)
        ok = bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all())
        if not ok: tally["fixed point, NOT strongly regular"] += 1; continue
        name = next((nm for nm, Rm in refs if T.find_iso(A, Rm) is not None), None)
        if name is None:
            name = "dm_%d_%d.edges" % (seed, st); refs.append((name, A))
            with open(os.path.join(outdir, name), "w", newline="\n") as f:
                for a in range(n):
                    for b in range(a + 1, n):
                        if A[a, b]: f.write("%d %d\n" % (a, b))
            o, gens, base, sizes = T.aut_group(A)
            print("   NEW GRAPH %s (start %d, %d iterations): |Aut| = %d, vertex orbits %s" % (name, st, it, o, [len(q) for q in T.vertex_orbits(n, gens)] if o > 1 else "243 orbits of size 1"), flush=True)
        tally[name + (" (the input itself)" if (A == A0).all() else "")] += 1
    print("%d starts, %d iterations at most, %.0f s: %s" % (nstart, niter, time.time() - t0, tally.most_common()), flush=True)
