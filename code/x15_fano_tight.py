r"""X15 -- Fano-tight vertex: exact generic block counts, flow balance, kappa constraint, and Rayleigh tests on
block-constant subspaces (note E2 section 5, notes/115 section 5).

Model at x: classes = points of PG(2,2); tau_u sends class j to Phi(class u, j) (Fano third point); tight regime:
sigma_P(v) lies in the quadrangle C4(P, class v) (no sigma edge inside a Fano-line family).
For y = {e,f} (classes P, P', M = Phi(P,P')), the 7 tight 3-eigenvectors give: 2 neighbours in its own line family,
1 in each family through exactly one of P, P', 3 in each family through M.  With the class slot equations this fixes
g_R'(y) = number of generic neighbours of y in every block R' disjoint from {P,P'}  (solved here as a linear system,
not from the closed formulas, as an independent check).
Then for any family Fam of pairwise intersecting blocks (triangle or star) the compression of 3I + (11/99)J - A
(and of A + 4I - (18/99)J) to  span(e_x, e_labels, e_y (y in Fam), 1_R (R not in Fam))  is exactly computable.
Both must be PSD in any srg(99,14,1,2).
"""
import sys, random, itertools, math
import numpy as np
sys.path.insert(0, 'scripts')

FANO = [(0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 0), (5, 6, 1), (6, 0, 2)]
PHI = {}
for L in FANO:
    for i, j in itertools.permutations(L, 2):
        PHI[(i, j)] = [c for c in L if c not in (i, j)][0]
LINE_OF = {frozenset((i, j)): frozenset(L) for L in FANO for i, j in itertools.combinations(L, 2)}
LAB = [(c, s) for c in range(7) for s in (0, 1)]
mate = lambda l: (l[0], 1 - l[1])
BLOCKS = [frozenset(b) for b in itertools.combinations(range(7), 2)]
PAIRS = [frozenset({(c, s), (d, t)}) for c, d in itertools.combinations(range(7), 2) for s in (0, 1) for t in (0, 1)]
PI = {p: i for i, p in enumerate(PAIRS)}
blk = lambda y: frozenset(l[0] for l in y)


def fano_tau(rng):
    tau = {}
    for u in LAB:
        t = {}
        for L in FANO:
            if u[0] in L:
                j, k = [c for c in L if c != u[0]]
                flip = rng.randint(0, 1)
                for s in (0, 1):
                    t[(j, s)], t[(k, s ^ flip)] = (k, s ^ flip), (j, s)
        tau[u] = t
    return tau


def allowed(P, v):
    """sigma_P(v) must avoid the classes of the line through P and class(v)."""
    L = LINE_OF[frozenset((P, v[0]))]
    return [w for w in LAB if w[0] not in L]


def random_sigma_tight(P, rng):
    dom = [l for l in LAB if l[0] != P]
    while True:
        img, used, ok = {}, set(), True
        order = dom[:]; rng.shuffle(order)
        for v in order:
            cand = [w for w in allowed(P, v) if w not in used]
            if not cand:
                ok = False; break
            w = rng.choice(cand); img[v] = w; used.add(w)
        if ok:
            return img


def special(y, tau, sigma, sinv):
    """the 4 special neighbours of y in Delta_x (2 tau, 2 sigma)."""
    e, f = tuple(y)
    out = [frozenset({e, tau[e][f]}), frozenset({f, tau[f][e]})]
    for u, v in ((e, f), (f, e)):
        P = u[0]
        w = sigma[P][v] if u[1] == 0 else sinv[P][v]
        out.append(frozenset({mate(u), w}))
    return out


def landing(y, tau, sigma, sinv):
    """(a, b): classes where sigma lands, via class(e) and via class(f), with e, f ordered by class."""
    e, f = sorted(y)
    a = (sigma[e[0]][f] if e[1] == 0 else sinv[e[0]][f])[0]
    b = (sigma[f[0]][e] if f[1] == 0 else sinv[f[0]][e])[0]
    return e[0], f[0], a, b


def generic_counts(y, spec):
    """solve the tight-count + slot system for g_R'(y), R' disjoint from blk(y). Returns dict or None."""
    P, Pp = sorted(blk(y)); M = PHI[(P, Pp)]
    dis = [R for R in BLOCKS if not (R & {P, Pp})]
    rows, rhs = [], []
    for L in FANO:
        Ls = frozenset(L)
        if Ls == LINE_OF[frozenset((P, Pp))]:
            continue
        inter = len(Ls & {P, Pp})
        target = 1 if inter == 1 else 3
        s = sum(1 for z in spec if blk(z) <= Ls)
        rows.append([1 if R <= Ls else 0 for R in dis]); rhs.append(target - s)
    for c in range(7):
        if c in (P, Pp):
            continue
        hits = sum(1 for z in spec for l in z if l[0] == c)
        rows.append([1 if c in R else 0 for R in dis]); rhs.append(4 - hits)
    Am, b = np.array(rows, float), np.array(rhs, float)
    sol, res, rk, _ = np.linalg.lstsq(Am, b, rcond=None)
    if rk != len(dis) or np.abs(Am @ sol - b).max() > 1e-9:
        return None
    g = np.rint(sol)
    if np.abs(g - sol).max() > 1e-9:
        return None
    return {R: int(v) for R, v in zip(dis, g)}


def config_data(tau, sigma):
    sinv = {P: {w: v for v, w in sigma[P].items()} for P in range(7)}
    spec = {y: special(y, tau, sigma, sinv) for y in PAIRS}
    # symmetry of special adjacency (sanity)
    for y in PAIRS:
        for z in spec[y]:
            assert y in spec[z], (y, z)
    kappa_bad = 0
    for y in PAIRS:
        P, Pp, a, b = landing(y, tau, sigma, sinv)
        M = PHI[(P, Pp)]
        if b == PHI[(M, a)]:
            kappa_bad += 1
    gen, neg = {}, 0
    for y in PAIRS:
        g = generic_counts(y, spec[y])
        if g is None:
            return dict(ok=False, kappa_bad=kappa_bad, spec=spec)
        gen[y] = g
        neg += sum(-v for v in g.values() if v < 0)
    # block edge counts from both sides
    N = np.zeros((21, 21), dtype=int)
    BI = {R: i for i, R in enumerate(BLOCKS)}
    for y in PAIRS:
        for z in spec[y]:
            N[BI[blk(y)], BI[blk(z)]] += 1
        for R, v in gen[y].items():
            N[BI[blk(y)], BI[R]] += v
    imbalance = int(np.abs(N - N.T).sum() // 2)
    # label-level balance: every far vertex w (class(u) not in blk(w)) has exactly 2 neighbours containing u,
    # so sum_{y containing u} #N(y) cap R' = 8 for every block R' avoiding class(u)
    lab_bad = 0
    for u in LAB:
        Xu = [y for y in PAIRS if u in y]
        for R in BLOCKS:
            if u[0] in R:
                continue
            tot = 0
            for y in Xu:
                if R & blk(y):
                    tot += sum(1 for z in spec[y] if blk(z) == R)
                else:
                    tot += gen[y][R]
            lab_bad += abs(tot - 8)
    return dict(ok=True, kappa_bad=kappa_bad, neg=neg, spec=spec, gen=gen, N=N, BI=BI, imbalance=imbalance,
                lab_bad=lab_bad)


def rayleigh(D, fam):
    """compressions for the family fam (list of blocks): returns (lmin of 3I+11J/99-A, lmin of A+4I-18J/99)."""
    spec, gen, N, BI = D['spec'], D['gen'], D['N'], D['BI']
    free = [y for y in PAIRS if blk(y) in fam]
    const = [R for R in BLOCKS if R not in fam]
    basis = [('x', None)] + [('l', u) for u in LAB] + [('y', y) for y in free] + [('R', R) for R in const]
    n = len(basis)
    size = np.array([1] * (15 + len(free)) + [4] * len(const), float)
    Mx = np.zeros((n, n))
    def cnt(y, R):  # neighbours of pair y inside block R
        if R & blk(y):
            return sum(1 for z in spec[y] if blk(z) == R)
        return gen[y][R]
    for i, (ti, a) in enumerate(basis):
        for j, (tj, b) in enumerate(basis):
            if j < i:
                continue
            v = 0
            if ti == 'x':
                v = 1 if tj == 'l' else 0
            elif ti == 'l':
                if tj == 'l':
                    v = 1 if b == mate(a) else 0
                elif tj == 'y':
                    v = 1 if a in b else 0
                elif tj == 'R':
                    v = 2 if a[0] in b else 0
            elif ti == 'y':
                if tj == 'y':
                    v = 1 if b in spec[a] else 0
                elif tj == 'R':
                    v = cnt(a, b)
            elif ti == 'R':
                v = N[BI[a], BI[b]]
            Mx[i, j] = Mx[j, i] = v
    J = np.outer(size, size)
    S1 = 3 * np.diag(size) + (11 / 99) * J - Mx
    S2 = Mx + 4 * np.diag(size) - (18 / 99) * J
    return np.linalg.eigvalsh(S1).min(), np.linalg.eigvalsh(S2).min()


def anneal(rng, tau, steps=20000, T0=1.0):
    sigma = {P: random_sigma_tight(P, rng) for P in range(7)}
    def cost(sig):
        D = config_data(tau, sig)
        if not D['ok']:
            return 10 ** 6, D
        return D['kappa_bad'] * 10 + D['neg'] * 10 + D['imbalance'] + D['lab_bad'], D
    c, D = cost(sigma)
    for step in range(steps):
        if c == 0:
            break
        P = rng.randrange(7)
        dom = [l for l in LAB if l[0] != P]
        v, w = rng.sample(dom, 2)
        sv, sw = sigma[P][v], sigma[P][w]
        if sw not in allowed(P, v) or sv not in allowed(P, w):
            continue
        sigma[P][v], sigma[P][w] = sw, sv
        c2, D2 = cost(sigma)
        T = T0 * (1 - step / steps) + 1e-3
        if c2 <= c or rng.random() < math.exp(-(c2 - c) / T):
            c, D = c2, D2
        else:
            sigma[P][v], sigma[P][w] = sv, sw
    return sigma, c, D


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    rng = random.Random(seed)
    tri = [frozenset(BLOCKS[i] for i in range(21) if BLOCKS[i] <= frozenset(t)) for t in itertools.combinations(range(7), 3)]
    stars = [frozenset(R for R in BLOCKS if c in R) for c in range(7)]
    for tr in range(trials):
        tau = fano_tau(rng)
        sigma, c, D = anneal(rng, tau)
        print(f'trial {tr}: final cost {c} (kappa_bad {D.get("kappa_bad")}, imbalance {D.get("imbalance")}, '
              f'label imbalance {D.get("lab_bad")})', flush=True)
        if c != 0:
            continue
        worst1 = min(rayleigh(D, list(f))[0] for f in tri + stars)
        worst2 = min(rayleigh(D, list(f))[1] for f in tri + stars)
        print(f'   Rayleigh: min eig (3I+11J/99-A) = {worst1:.6f}, min eig (A+4I-18J/99) = {worst2:.6f}', flush=True)
