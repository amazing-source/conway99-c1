"""Search for strongly regular graphs by Elser's RRR (reflect-reflect-relax) projection algorithm.

Two constraint sets on symmetric n x n matrices:
  A = { 0/1 symmetric, zero diagonal }                         (projection: entrywise rounding)
  B = { (k/n) J + r P + s (Q - P) : P rank-f projection <= Q }  (Q = I - J/n; projection: top-f eigenvectors)
A matrix in A and B is exactly the adjacency matrix of an srg with eigenvalues k, r^f, s^g.
RRR iteration:  x <- x + beta * ( P_A(2 P_B(x) - x) - P_B(x) ).
Any candidate is verified exactly in integers:  A 1 = k 1  and  A^2 + (mu - lam) A + (mu - k) I = mu J.
"""
import sys, time, math
import numpy as np


def srg_eigen(n, k, lam, mu):
    D = (lam - mu) ** 2 + 4 * (k - mu)
    r = ((lam - mu) + math.sqrt(D)) / 2
    s = ((lam - mu) - math.sqrt(D)) / 2
    f = round((-k - (n - 1) * s) / (r - s))
    return r, s, f


class RRR:
    def __init__(self, n, k, lam, mu, beta=0.5, seed=0, fixed=None):
        self.n, self.k, self.lam, self.mu = n, k, lam, mu
        self.r, self.s, self.f = srg_eigen(n, k, lam, mu)
        self.beta = beta
        self.rng = np.random.default_rng(seed)
        # orthonormal basis of 1-perp
        M = np.eye(n)[:, 1:] - np.ones((n, n - 1)) / n
        U, _ = np.linalg.qr(np.hstack([np.ones((n, 1)), np.eye(n)[:, 1:]]))
        self.U = U[:, 1:]
        self.Jk = np.full((n, n), k / n)
        self.fixed = fixed            # optional (mask, values): entries forced in P_A
        x = self.rng.random((n, n))
        self.x = (x + x.T) / 2
        np.fill_diagonal(self.x, 0)

    def PB(self, x):
        C = self.U.T @ x @ self.U
        C = (C + C.T) / 2
        w, V = np.linalg.eigh(C)
        W = V[:, -self.f:]
        P = self.U @ W @ W.T @ self.U.T
        Q = np.eye(self.n) - np.full((self.n, self.n), 1 / self.n)
        return self.Jk + self.r * P + self.s * (Q - P)

    def PA(self, x):
        y = (x + x.T) / 2
        a = (y > 0.5).astype(float)
        np.fill_diagonal(a, 0)
        if self.fixed is not None:
            mask, vals = self.fixed
            a[mask] = vals[mask]
        return a

    def is_srg(self, a):
        A = a.astype(np.int64)
        n, k, lam, mu = self.n, self.k, self.lam, self.mu
        if not (A == A.T).all() or A.diagonal().any() or not (A.sum(1) == k).all():
            return False
        return (A @ A + (mu - lam) * A + (mu - k) * np.eye(n, dtype=np.int64) == mu).all()

    def step(self):
        pb = self.PB(self.x)
        pa = self.PA(2 * pb - self.x)
        self.x = self.x + self.beta * (pa - pb)
        return pa, float(np.abs(pa - pb).sum())

    def run(self, maxit, report=0):
        t0 = time.time()
        best = None
        for it in range(1, maxit + 1):
            pa, err = self.step()
            if best is None or err < best:
                best = err
            if self.is_srg(pa):
                return it, pa, time.time() - t0
            if report and it % report == 0:
                print(f'   it {it}: err {err:.2f} (best {best:.2f}) {time.time()-t0:.0f}s', flush=True)
        return None, None, time.time() - t0


if __name__ == '__main__':
    n, k, lam, mu = (int(a) for a in sys.argv[1:5])
    maxit = int(sys.argv[5]) if len(sys.argv) > 5 else 20000
    tries = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    beta = float(sys.argv[7]) if len(sys.argv) > 7 else 0.5
    for seed in range(tries):
        R = RRR(n, k, lam, mu, beta=beta, seed=seed)
        it, a, dt = R.run(maxit)
        print(f'srg({n},{k},{lam},{mu}) seed {seed}: ' + (f'FOUND at iteration {it} ({dt:.1f}s)' if it else f'not found in {maxit} its ({dt:.1f}s)'), flush=True)
