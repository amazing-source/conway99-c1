# J2 probe: budget in the direction of F.  For Y outside star(0): a_perp(Y) = a_Y - alpha^T A0^+ m_Y, and
#   sum_{Y outside star(0)} a_perp(Y)^2 = 24 - 28 q   (q = alpha^T A0^+ alpha)   [identity from T^2+T = 12I-RR^T]
# so the 10 cut1 labels + V must fit: cost_V + sum_Y min_col cost_Y <= 24 - 28q.
# Columns: 2 incidences in O_0+ (a non-Q0 pair) and 2 in O_0- (a non-Q0 pair, negated); h-profile of Y.
import numpy as np, random, json, itertools
rng = random.Random(5)
pat = json.load(open('j2_patterns.json'))
cells = [(i, j) for i in range(7) for j in range(i + 1, 7)]
labels = [(c, s) for c in cells for s in (1, -1)]
idx = {L: k for k, L in enumerate(labels)}
def rep(L):
    (i, j), s = L; v = np.zeros(7); v[i] = 1; v[j] = s; return v
S0labs = [((0, x), s) for x in range(1, 7) for s in (1, -1)]
R0 = np.array([rep(L) for L in S0labs])
Smat = np.array([[1.0 if (L[0] == M[0] and L[1] != M[1]) else 0.0 for M in S0labs] for L in S0labs])
def rand_inv(n=12):
    p = list(range(n)); rng.shuffle(p); inv = [0] * n
    for k in range(0, n, 2): inv[p[k]] = p[k + 1]; inv[p[k + 1]] = p[k]
    return inv
def pinv(A):
    w, V = np.linalg.eigh(A); keep = w > 1e-9; return (V[:, keep] / w[keep]) @ V[:, keep].T
stats = {'tried': 0, 'profile': 0, 'atest': 0, 'Vtest': 0, 'budget': 0}
mins = []
for trial in range(4000):
    signs = pat['patterns'][rng.randrange(len(pat['patterns']))]
    a = np.zeros(42)
    for k, s in zip(pat['cut'], signs): a[k] = s
    a[pat['V']] = 2
    alpha = np.array([a[idx[L]] for L in S0labs])
    Q, P = rand_inv(), rand_inv(); stats['tried'] += 1
    forced = {1: [], -1: []}
    for L in range(2, 12):
        zc = (Q[L] < 2) + (P[L] < 2)
        s0 = alpha[L] * (alpha[Q[L]] - alpha[P[L]]) if Q[L] != P[L] else 0
        if zc == 2 or (zc == 1 and s0 == 1) or (zc == 0 and s0 == 2): forced[alpha[L]].append(L)
    if len(forced[1]) > 2 or len(forced[-1]) > 2: continue
    stats['profile'] += 1
    T = np.zeros((12, 12))
    for i in range(12): T[i, Q[i]] += 1; T[i, P[i]] -= 1
    A0 = 11 * np.eye(12) + Smat - np.ones((12, 12)) - 4 * T
    A0p = pinv(A0); q = alpha @ A0p @ alpha
    if q > 6 / 7 + 1e-9: continue
    stats['atest'] += 1
    Qpairs = set(frozenset((i, Q[i])) for i in range(12))
    pairs = [p for p in itertools.combinations(range(12), 2) if frozenset(p) not in Qpairs]
    plus = [L for L in range(2, 12) if alpha[L] == 1]; minus = [L for L in range(2, 12) if alpha[L] == -1]
    rV = rep(((5, 6), 1))
    best_total = None
    budget0 = 24 - 28 * q
    # min over P_sigma choices of [cost_V + sum_Y mincost_Y]; mincost_Y does not depend on P_sigma here (T_VY ignored)
    # column min costs
    colmin = []
    for x in range(2, 7):
        for s in (1, -1):
            Yl = ((1, x), s); aY = a[idx[Yl]]; rY = aY * rep(Yl)
            best = 1e9
            for pp in pairs:
                for pm in pairs:
                    t = np.zeros(12); t[list(pp)] += 1; t[list(pm)] -= 1
                    zinc = sum(1 for L in pp if L < 2) + sum(1 for L in pm if L < 2)
                    so = alpha[list(pp)].sum() - alpha[list(pm)].sum()
                    allowed = {2: {-2}, 1: {-3, -1}, 0: {-4, -2, 0}}.get(zinc, set())
                    if so not in allowed: continue
                    m = -4 * t - R0 @ rY
                    if 10 - m @ A0p @ m < -1e-9: continue
                    c = (1 - alpha @ A0p @ m) ** 2
                    best = min(best, c)
            colmin.append(best)
    ok_any = False
    for cp in itertools.combinations(plus, 2):
        if not set(forced[1]) <= set(cp): continue
        for cm in itertools.combinations(minus, 2):
            if not set(forced[-1]) <= set(cm): continue
            tV = np.zeros(12)
            for L in list(cp) + list(cm): tV[L] = -alpha[L]
            mV = -4 * tV - R0 @ rV
            sV = 10 - mV @ A0p @ mV
            costV = (2 - alpha @ A0p @ mV) ** 2
            if sV < -1e-9 or costV > budget0 + 1e-9: continue
            stats['Vtest'] += 1
            tot = costV + sum(colmin)
            if best_total is None or tot < best_total: best_total = tot
            if tot <= budget0 + 1e-9: ok_any = True
    if best_total is not None: mins.append(best_total - budget0)
    if ok_any: stats['budget'] += 1
print(stats)
mins = np.array(mins)
print('min(total cost - budget) over P_sigma choices: min %.3f, quantiles %s' % (mins.min(), np.quantile(mins, [0.01, 0.1, 0.5, 0.9])))
