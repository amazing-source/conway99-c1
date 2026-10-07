"""Exact finite-n moment (flag) hierarchy for srg(n,k,lam,mu), after the injective-moment method of the openai/math
Hadamard-6 paper (notes/161c).  Variables: densities q_Q of the induced t-vertex patterns Q (sum 1).
Constraints, all EXACT for a real srg(n,k,lam,mu):
  * extension identities: for every pattern P on m < t vertices, every vertex u and pair {u,w} of P,
      sum_{S ∋ u} N(P+S) = (k - deg_P u) N(P),  sum_{S ∋ u,w} N(P+S) = (lam|mu - |N_P(u)∩N_P(w)|) N(P),
      sum_S N(P+S) = (n - m) N(P)   (N = injective induced embeddings, P+S = P plus a vertex attached to S);
  * counting Gram  sum_theta c_F(theta) c_F'(theta)  ⪰ 0 for every type sigma and its flags;
  * spectral Grams  sum_theta y_F^T E y_F'  ⪰ 0 for the two nontrivial eigenprojections E (flags with a
    distinguished extra vertex z, y_F(theta, z) = number of extensions sending it to z).
Usage: python3 srg_moments.py n k lam mu t [validate_edges_file]"""
import itertools, math, sys, time
from functools import lru_cache
from fractions import Fraction
import numpy as np


def pid(i, j):
    if i > j: i, j = j, i
    return j * (j - 1) // 2 + i


def nbmasks(m, bits):
    nb = [0] * m
    for j in range(m):
        for i in range(j):
            if (bits >> (j * (j - 1) // 2 + i)) & 1:
                nb[i] |= 1 << j; nb[j] |= 1 << i
    return nb


def relabel(m, bits, p):
    """new vertex i = old vertex p[i]"""
    out = 0
    for j in range(m):
        for i in range(j):
            if (bits >> pid(p[i], p[j])) & 1:
                out |= 1 << (j * (j - 1) // 2 + i)
    return out


def classes(m, nb, fixed=0):
    """ordered partition by iterated colour refinement; the first `fixed` vertices stay singletons in place"""
    col = [(-2, i) if i < fixed else (-1, bin(nb[i]).count("1")) for i in range(m)]
    for _ in range(3):
        col = [col[i] + (tuple(sorted(col[j] for j in range(m) if nb[i] >> j & 1)),) if i >= fixed else col[i]
               for i in range(m)]
        keys = sorted(set(col)); col = [(keys.index(c),) for c in col]
    groups = {}
    for i in range(m):
        groups.setdefault(col[i], []).append(i)
    return [groups[c] for c in sorted(groups)]


def perms_of(parts):
    for combo in itertools.product(*[itertools.permutations(g) for g in parts]):
        yield [v for g in combo for v in g]


@lru_cache(maxsize=None)
def canon(m, bits, fixed=0):
    """canonical form (min relabelling respecting refinement; first `fixed` vertices fixed). Returns (bits, |Aut|)."""
    nb = nbmasks(m, bits)
    parts = classes(m, nb, fixed)
    best, aut = None, 0
    for p in perms_of(parts):
        b = relabel(m, bits, p)
        if best is None or b < best:
            best, aut = b, 1
        elif b == best:
            aut += 1
    return best, aut


def admissible(m, bits, k, lam, mu):
    nb = nbmasks(m, bits)
    for j in range(m):
        if bin(nb[j]).count("1") > k:
            return False
        for i in range(j):
            c = bin(nb[i] & nb[j]).count("1")
            if c > (lam if (nb[i] >> j) & 1 else mu):
                return False
    return True


def extend(m, bits, S):
    return bits | (S << (m * (m - 1) // 2))


def induced(m, bits, sub):
    out = 0
    for b, j in enumerate(sub):
        for a, i in enumerate(sub[:b]):
            if (bits >> pid(i, j)) & 1:
                out |= 1 << (b * (b - 1) // 2 + a)
    return out


class Hierarchy:
    def __init__(self, n, k, lam, mu, t, exact=False):
        self.n, self.k, self.lam, self.mu, self.t = n, k, lam, mu, t
        self.exact = exact
        # eigenvalues
        D = (lam - mu) ** 2 + 4 * (k - mu); di = math.isqrt(D)
        if di * di == D:
            self.r, self.s = Fraction((lam - mu) + di, 2), Fraction((lam - mu) - di, 2)
        else:
            assert not exact, "exact mode needs integral eigenvalues"
            d = math.sqrt(D); self.r, self.s = ((lam - mu) + d) / 2, ((lam - mu) - d) / 2
        # admissible classes by level
        self.levels = {0: [0], 1: [0]}
        for m in range(1, t):
            nxt = set()
            for P in self.levels[m]:
                for S in range(1 << m):
                    B = extend(m, P, S)
                    if admissible(m + 1, B, k, lam, mu):
                        nxt.add(canon(m + 1, B)[0])
            self.levels[m + 1] = sorted(nxt)
        self.top = self.levels[t]; self.index = {Q: i for i, Q in enumerate(self.top)}
        # density map: nu(L) = N(L)/(n)_m as a linear form in q (top densities)
        self.dens = {}
        for m in range(0, t + 1):
            for P in self.levels[m]:
                self.dens[(m, P)] = self.Z()
        for qi, Q in enumerate(self.top):
            for m in range(0, t + 1):
                for sub in itertools.combinations(range(t), m):
                    P = canon(m, induced(t, Q, sub))[0]
                    self.dens[(m, P)][qi] += Fraction(1, math.comb(t, m)) if exact else 1.0 / math.comb(t, m)

    def Z(self):
        return np.array([Fraction(0)] * len(self.top), dtype=object) if self.exact else np.zeros(len(self.top))

    def nu(self, m, bits):
        """N(L)/(n)_m for a labelled graph L (zero vector if inadmissible)"""
        if not admissible(m, bits, self.k, self.lam, self.mu):
            return None
        P, aut = canon(m, bits)
        return self.dens[(m, P)] * (Fraction(aut, math.factorial(m)) if self.exact else aut / math.factorial(m))

    def equalities(self):
        rows = []
        n, k = self.n, self.k
        for m in range(1, self.t):
            for P in self.levels[m]:
                base = self.nu(m, P); nb = nbmasks(m, P)
                ext = {}
                for S in range(1 << m):
                    v = self.nu(m + 1, extend(m, P, S))
                    if v is not None:
                        ext[S] = v * (n - m)
                tot = sum(ext.values(), self.Z())
                rows.append(tot - (n - m) * base)
                for u in range(m):
                    acc = sum((v for S, v in ext.items() if S >> u & 1), self.Z())
                    rows.append(acc - (k - bin(nb[u]).count("1")) * base)
                    for w in range(u + 1, m):
                        acc = sum((v for S, v in ext.items() if (S >> u & 1) and (S >> w & 1)), self.Z())
                        c = self.lam if (nb[u] >> w) & 1 else self.mu
                        rows.append(acc - (c - bin(nb[u] & nb[w]).count("1")) * base)
        return np.array(rows, dtype=object) if self.exact else np.array(rows)

    def flags(self, s, sigma, a, distinguished):
        """sigma-flags with a extra vertices (vertices s..s+a-1), canonical up to permutations of the extras
        (of extras 2..a if distinguished)."""
        out = set()
        fixed = s + (1 if distinguished else 0)
        for S in itertools.product(range(1 << s), repeat=a):
            for E in range(1 << (a * (a - 1) // 2)):
                bits, m = sigma, s
                for x in range(a):
                    inner = 0
                    for y in range(x):
                        if E >> (x * (x - 1) // 2 + y) & 1:
                            inner |= 1 << (s + y)
                    bits = extend(m, bits, S[x] | inner); m += 1
                if admissible(m, bits, self.k, self.lam, self.mu):
                    out.add(canon(m, bits, fixed)[0])
        return sorted(out)

    def joint(self, s, a, F1, F2, mode):
        """sum over joint configurations of two flags (same sigma on vertices 0..s-1) of nu(L), scaled by
        (n)_{|L|}/(n)_{s+2a}.  mode: 'all' | 'same' (first extras identified) | 'adj' (first extras distinct, adjacent)"""
        n = self.n; tot = self.Z()
        e1 = list(range(s, s + a))
        for kk in range(0, a + 1):
            for A_ in itertools.combinations(range(a), kk):
                for B_ in itertools.permutations(range(a), kk):
                    pi = dict(zip(A_, B_))
                    if mode == 'same' and pi.get(0) != 0:
                        continue
                    if mode == 'adj' and pi.get(0) == 0:
                        continue
                    # consistency on identified vertices: adjacency to roots and among identified
                    ok = True
                    for i, j in pi.items():
                        for r in range(s):
                            if ((F1 >> pid(r, s + i)) & 1) != ((F2 >> pid(r, s + j)) & 1):
                                ok = False; break
                        if not ok: break
                    if not ok: continue
                    for (i, j), (i2, j2) in itertools.combinations(pi.items(), 2):
                        if ((F1 >> pid(s + i, s + i2)) & 1) != ((F2 >> pid(s + j, s + j2)) & 1):
                            ok = False; break
                    if not ok: continue
                    # vertex list of L: roots, F1 extras (s..s+a-1), F2 non-identified extras appended
                    rest = [j for j in range(a) if j not in pi.values()]
                    m = s + a + len(rest)
                    pos2 = {j: s + i for i, j in pi.items()}
                    for idx, j in enumerate(rest):
                        pos2[j] = s + a + idx
                    base = 0
                    for jj in range(s + a):
                        for ii in range(jj):
                            if (F1 >> pid(ii, jj)) & 1:
                                base |= 1 << pid(ii, jj)
                    for j in range(a):          # F2 edges (roots-extras, extras-extras)
                        for r in range(s):
                            if (F2 >> pid(r, s + j)) & 1:
                                base |= 1 << pid(r, pos2[j])
                        for j2 in range(j):
                            if (F2 >> pid(s + j2, s + j)) & 1:
                                base |= 1 << pid(pos2[j2], pos2[j])
                    free = [(s + i, pos2[j]) for i in range(a) if i not in pi for j in rest]
                    forced = None
                    if mode == 'adj':
                        forced = (s + 0, pos2[0])
                    for fb in range(1 << len(free)):
                        bits = base
                        okf = True
                        for b, (x, y) in enumerate(free):
                            if fb >> b & 1:
                                bits |= 1 << pid(x, y)
                        if forced is not None and not (bits >> pid(*forced)) & 1:
                            continue
                        v = self.nu(m, bits)
                        if v is not None:
                            # (n)_m / (n)_{s+2a} = 1 / (n-m)_{s+2a-m}
                            sc = Fraction(1) if self.exact else 1.0
                            for z in range(m, s + 2 * a):
                                sc /= (n - z)
                            tot += v * sc
        return tot

    def blocks(self):
        """list of (name, list-of-flags, function (i,j)->coefficient vector)"""
        n, k, r, s_ = self.n, self.k, self.r, self.s
        # eigenprojection coefficients E_theta = (aI + bA + cJ)
        def proj(th, eta):
            den = (th - eta) * (th - k)
            return ((k - self.mu + eta * k) / den, (self.lam - self.mu - eta - k) / den, Fraction(self.mu) / den)
        E = {'E_r': proj(r, s_), 'E_s': proj(s_, r)}
        out = []
        for s in range(0, self.t + 1):
            for a in range(1, (self.t - s) // 2 + 1):
                for sigma in self.levels[s]:
                    F = self.flags(s, sigma, a, False)
                    if len(F) >= 1:
                        out.append((f"count s={s} a={a} sigma={sigma}", s, a, F, None))
                    Fd = self.flags(s, sigma, a, True)
                    for nm, coef in E.items():
                        out.append((f"{nm} s={s} a={a} sigma={sigma}", s, a, Fd, coef))
        return out

    def block_matrices(self, s, a, F, coef):
        d = len(F); nq = len(self.top)
        Bm = np.empty((d, d, nq), dtype=object) if self.exact else np.zeros((d, d, nq))
        for i in range(d):
            for j in range(i, d):
                if coef is None:
                    v = self.joint(s, a, F[i], F[j], 'all')
                else:
                    ca, cb, cc = coef
                    v = ca * self.joint(s, a, F[i], F[j], 'same') + cb * self.joint(s, a, F[i], F[j], 'adj') \
                        + cc * self.joint(s, a, F[i], F[j], 'all')
                Bm[i, j] = v; Bm[j, i] = v
        return Bm


def actual_densities(H, edges_path, n):
    """exact top-level densities of a real graph (small n only)"""
    adj = [[0] * n for _ in range(n)]
    for line in open(edges_path):
        if line.strip():
            i, j = map(int, line.split()); adj[i][j] = adj[j][i] = 1
    q = np.zeros(len(H.top)); t = H.t
    for sub in itertools.combinations(range(n), t):
        bits = 0
        for b in range(t):
            for a_ in range(b):
                if adj[sub[a_]][sub[b]]:
                    bits |= 1 << (b * (b - 1) // 2 + a_)
        q[H.index[canon(t, bits)[0]]] += 1
    return q / math.comb(n, t)


if __name__ == "__main__":
    n, k, lam, mu, t = map(int, sys.argv[1:6])
    t0 = time.time()
    H = Hierarchy(n, k, lam, mu, t)
    print(f"srg({n},{k},{lam},{mu}) t={t}: admissible classes per level",
          {m: len(v) for m, v in H.levels.items()}, f"{time.time() - t0:.1f}s", flush=True)
    Aeq = H.equalities()
    print("equality rows", Aeq.shape, "rank", np.linalg.matrix_rank(Aeq), flush=True)
    blks = H.blocks()
    mats = []
    for name, s, a, F, coef in blks:
        mats.append((name, H.block_matrices(s, a, F, coef)))
    print("PSD blocks", len(mats), "sizes", sorted(m.shape[0] for _, m in mats), f"{time.time() - t0:.1f}s", flush=True)
    np.savez_compressed(f"/tmp/claude-0/-home-user/899e78f1-d1e3-5aeb-b4c1-585fa11b4ff7/scratchpad/mom_{n}_{t}.npz",
                        Aeq=Aeq, **{f"B{i}": m for i, (_, m) in enumerate(mats)})
    if len(sys.argv) > 6:
        q = actual_densities(H, sys.argv[6], n)
        print("validation on", sys.argv[6], ": max |Aeq q| =", np.abs(Aeq @ q).max())
        ev = [(np.linalg.eigvalsh(np.tensordot(m, q, axes=([2], [0]))).min(), nm) for nm, m in mats]
        print("   min eigenvalue over all PSD blocks at the true point:", min(ev))
        for e, nm in ev:
            if e < -1e-12:
                print("      NEGATIVE", e, nm)
    import cvxpy as cp
    q = cp.Variable(len(H.top)); tau = cp.Variable()
    cons = [q >= 0, cp.sum(q) == 1, Aeq @ q == 0, tau <= 1]
    for name, m in mats:
        d = m.shape[0]
        M = cp.reshape(m.reshape(d * d, -1) @ q, (d, d), order="C")
        cons.append((M + M.T) / 2 - tau * np.eye(d) >> 0)
    prob = cp.Problem(cp.Maximize(tau), cons)
    prob.solve(solver="CLARABEL")
    print("SDP status", prob.status, "max min-eigen slack tau =", prob.value, f"{time.time() - t0:.1f}s", flush=True)
