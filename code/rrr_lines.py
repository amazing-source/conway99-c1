"""RRR search for srg(n, k, 1, mu) in the LINE formulation: unknown point-line incidence N (n x b, b = n k / 6).
  A = { 0/1 matrices, every column (line) has exactly 3 ones }      (projection: top-3 per column)
  B = { N : singular values sqrt(k+2+? ) ... }: N N^T = 3I + A_graph + ... ; for an srg with lambda = 1,
      N N^T = (k/2) I + A, so N N^T has eigenvalues k/2 + k (x1), k/2 + r (x f), k/2 + s (x g), and N has
      b - n further zero singular values.  Projection: SVD, replace singular values by the targets (sorted),
      keep the singular vectors.
A matrix in A and B gives N N^T with the SRG spectrum; we verify exactly that A = N N^T - (k/2) I is an
srg(n,k,1,mu) adjacency matrix (0/1, zero diagonal, A^2 + (mu-1)A + (mu-k)I = mu J).
"""
import sys, time, json, math
import numpy as np
from rrr_srg import srg_eigen


class LinesRRR:
    def __init__(self, n, k, mu, beta=0.1, seed=0):
        self.n, self.k, self.mu = n, k, mu
        r, s, f = srg_eigen(n, k, 1, mu)
        g = n - 1 - f
        self.b = n * k // 6
        h = k // 2
        vals = [h + k] + [h + r] * f + [h + s] * g
        assert min(vals) >= -1e-9, vals
        self.target = np.sqrt(np.maximum(np.array(sorted(vals, reverse=True)), 0))
        self.beta = beta
        self.rng = np.random.default_rng(seed)
        self.x = self.rng.random((n, self.b)) * (3 / n) * 2

    def PB(self, x):
        U, sv, Vt = np.linalg.svd(x, full_matrices=False)       # sv descending, length n (n <= b)
        return (U * self.target[:len(sv)]) @ Vt

    def PA(self, x):
        a = np.zeros_like(x)
        idx = np.argpartition(-x, 3, axis=0)[:3]                # top-3 rows per column
        a[idx, np.arange(x.shape[1])[None, :]] = 1.0
        return a

    def check(self, Nm):
        N = Nm.astype(np.int64)
        G = N @ N.T
        h = self.k // 2
        if not (np.diag(G) == h).all():
            return False
        A = G - h * np.eye(self.n, dtype=np.int64)
        if A.max() > 1:
            return False
        n, k, mu = self.n, self.k, self.mu
        return (A @ A + (mu - 1) * A + (mu - k) * np.eye(n, dtype=np.int64) == mu).all()

    def run(self, seconds, report=0):
        t0 = time.time(); it = 0; best = None
        while time.time() - t0 < seconds:
            it += 1
            pb = self.PB(self.x)
            pa = self.PA(2 * pb - self.x)
            self.x = self.x + self.beta * (pa - pb)
            err = float(np.abs(pa - pb).sum())
            best = err if best is None or err < best else best
            if it % 20 == 0 and self.check(pa):
                return it, pa, time.time() - t0, best
            if report and it % report == 0:
                print(f'   it {it}: err {err:.1f} best {best:.1f} ({time.time()-t0:.0f}s)', flush=True)
        return None, None, time.time() - t0, best


if __name__ == '__main__':
    n, k, mu = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    secs = float(sys.argv[4]); seeds = int(sys.argv[5]); beta = float(sys.argv[6]) if len(sys.argv) > 6 else 0.1
    for seed in range(seeds):
        R = LinesRRR(n, k, mu, beta=beta, seed=seed)
        it, N, dt, best = R.run(secs)
        if it:
            print(f'srg({n},{k},1,{mu}) lines-RRR seed {seed}: FOUND at iteration {it} ({dt:.1f}s)', flush=True)
            if n == 99:
                json.dump(N.astype(int).tolist(), open(f'../data/FOUND_srg99_lines_seed{seed}.json', 'w'))
        else:
            print(f'srg({n},{k},1,{mu}) lines-RRR seed {seed}: not found ({dt:.0f}s, best err {best:.1f})', flush=True)
