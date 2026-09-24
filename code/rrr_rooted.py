"""RRR search for srg(n, 2(t+1), 1, 2) with the forced structure at a vertex x built in.

Vertex 0 = x; vertices 1..2(t+1) = N(x) in mate pairs (1,2), (3,4), ...; the remaining vertices are the
non-mate pairs of N(x) (Gamma_2(x)), each adjacent exactly to its two labels.  Unknown: the graph H on
Gamma_2(x).  P_A enforces: all forced entries; for each label a, the X-vertices containing a are perfectly
matched (the transition tau_a), other label-sharing pairs are non-adjacent; label-disjoint pairs are rounded.
P_B enforces the spectrum {k, r^f, s^g}.  Intersection = srg(n,k,1,2).  Candidates verified exactly.
Usage: rrr_rooted.py t maxit seeds beta [match|round]
"""
import sys, time, math, itertools, json
import numpy as np
from rrr_srg import srg_eigen


def perfect_matchings(m):
    """All perfect matchings of range(m) as arrays of pairs (m even)."""
    if m == 0:
        return [[]]
    out = []
    for j in range(1, m):
        rest = [v for v in range(1, m) if v != j]
        for pm in perfect_matchings(len(rest)):
            out.append([(0, j)] + [(rest[a], rest[b]) for a, b in pm])
    return out


class RootedRRR:
    def __init__(self, t, beta=0.1, seed=0, mode='match', noprism=False):
        self.t = t
        k = 2 * (t + 1)
        n = 1 + k + k * (k - 2) // 2
        self.n, self.k = n, k
        self.r, self.s, self.f = srg_eigen(n, k, 1, 2)
        self.beta, self.mode = beta, mode
        self.rng = np.random.default_rng(seed)
        labels = list(range(1, k + 1))
        mate = {a: a + 1 if a % 2 == 1 else a - 1 for a in labels}
        self.pairs = [(a, b) for a, b in itertools.combinations(labels, 2) if mate[a] != b]
        X = list(range(k + 1, n))
        assert len(X) == len(self.pairs)
        self.lab = {X[i]: set(p) for i, p in enumerate(self.pairs)}
        # forced entries
        mask = np.zeros((n, n), dtype=bool); val = np.zeros((n, n))
        mask[0, :] = mask[:, 0] = True
        val[0, 1:k + 1] = val[1:k + 1, 0] = 1
        for a in labels:
            for b in labels:
                mask[a, b] = True
                val[a, b] = 1.0 if mate[a] == b else 0.0
            for E in X:
                mask[a, E] = mask[E, a] = True
                val[a, E] = val[E, a] = 1.0 if a in self.lab[E] else 0.0
        np.fill_diagonal(mask, True); np.fill_diagonal(val, 0)
        self.mask, self.val = mask, val
        # label blocks
        self.blocks = []
        pm = np.array(perfect_matchings(2 * t)) if 2 * t <= 12 else None
        for a in labels:
            V = [E for E in X if a in self.lab[E]]
            self.blocks.append((a, np.array(V)))
            for E in V:
                for F in V:
                    if E != F:
                        mask[E, F] = True            # decided by the matching
        self.pm = pm                                  # (M, t, 2) local indices
        self.pm_blocks = None
        if noprism and pm is not None:
            # maximal twisting (P = 0): tau_a never pairs {a,b} with {a,mate(b)}
            self.pm_blocks = []
            for lab_, V in self.blocks:
                other = [next(iter(self.lab[E] - {lab_})) for E in V]
                okm = np.array([all(mate[other[i]] != other[j] for i, j in m) for m in pm])
                self.pm_blocks.append(pm[okm])
        # label-disjoint pairs are free
        U, _ = np.linalg.qr(np.hstack([np.ones((n, 1)), np.eye(n)[:, 1:]]))
        self.U = U[:, 1:]
        self.Jk = np.full((n, n), k / n)
        self.Q = np.eye(n) - np.full((n, n), 1 / n)
        x = self.rng.random((n, n)); x = (x + x.T) / 2
        x[mask] = val[mask]
        self.x = x

    def PB(self, x):
        C = self.U.T @ x @ self.U
        w, V = np.linalg.eigh((C + C.T) / 2)
        W = V[:, -self.f:]
        P = self.U @ W @ W.T @ self.U.T
        return self.Jk + self.r * P + self.s * (self.Q - P)

    def PA(self, x):
        y = (x + x.T) / 2
        a = (y > 0.5).astype(float)
        a[self.mask] = self.val[self.mask]
        for bi, (lab, V) in enumerate(self.blocks):
            B = y[np.ix_(V, V)]
            if self.pm is not None and self.mode == 'match':
                pmb = self.pm if self.pm_blocks is None else self.pm_blocks[bi]
                sc = B[pmb[:, :, 0], pmb[:, :, 1]].sum(1)
                best = pmb[int(np.argmax(sc))]
            else:   # greedy matching
                best, used = [], set()
                order = np.dstack(np.unravel_index(np.argsort(-B, axis=None), B.shape))[0]
                for i, j in order:
                    if i < j and i not in used and j not in used:
                        best.append((i, j)); used.update((i, j))
                best = np.array(best)
            for i, j in best:
                a[V[i], V[j]] = a[V[j], V[i]] = 1.0
        np.fill_diagonal(a, 0)
        return a

    def is_srg(self, a):
        A = a.astype(np.int64); n, k = self.n, self.k
        if not (A == A.T).all() or not (A.sum(1) == k).all():
            return False
        return (A @ A + A + (2 - k) * np.eye(n, dtype=np.int64) == 2).all()

    def run(self, maxit, report=0, stop_time=None):
        t0 = time.time(); best = None
        for it in range(1, maxit + 1):
            pb = self.PB(self.x)
            pa = self.PA(2 * pb - self.x)
            self.x = self.x + self.beta * (pa - pb)
            err = float(np.abs(pa - pb).sum())
            best = err if best is None or err < best else best
            if self.is_srg(pa):
                return it, pa, time.time() - t0, best
            if report and it % report == 0:
                print(f'   it {it}: err {err:.1f} best {best:.1f} ({time.time()-t0:.0f}s)', flush=True)
            if stop_time and time.time() - t0 > stop_time:
                break
        return None, None, time.time() - t0, best


if __name__ == '__main__':
    t = int(sys.argv[1]); maxit = int(sys.argv[2]); seeds = int(sys.argv[3])
    beta = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
    mode = sys.argv[5] if len(sys.argv) > 5 else 'match'
    stop = float(sys.argv[6]) if len(sys.argv) > 6 else None
    noprism = len(sys.argv) > 7 and sys.argv[7] == 'noprism'
    for seed in range(seeds):
        R = RootedRRR(t, beta=beta, seed=seed, mode=mode, noprism=noprism)
        it, a, dt, best = R.run(maxit, report=max(1, maxit // 10), stop_time=stop)
        if it:
            print(f'FOUND srg({R.n},{R.k},1,2), t={t}, seed {seed}, iteration {it} ({dt:.1f}s)', flush=True)
            json.dump(a.astype(int).tolist(), open(f'../data/FOUND_srg{R.n}_seed{seed}.json', 'w'))
        else:
            print(f't={t} seed {seed}: not found ({dt:.0f}s, best err {best:.1f})', flush=True)
