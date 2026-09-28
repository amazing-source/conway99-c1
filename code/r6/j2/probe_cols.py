# J2 probe: for a random admissible star(0) structure S0 (+ P_sigma cap star(0)), count the admissible columns of each
# cut1 label Y (its 2+2 root incidences into star(0)) under: h-profile, s_Y >= 0, Gram{F_perp, rho_V, rho_Y} PSD.
import numpy as np, random, json, itertools
rng = random.Random(3)
pat = json.load(open('j2_patterns.json'))
cells = [(i, j) for i in range(7) for j in range(i + 1, 7)]
labels = [(c, s) for c in cells for s in (1, -1)]
idx = {L: k for k, L in enumerate(labels)}
def rep(L):
    (i, j), s = L; v = np.zeros(7); v[i] = 1; v[j] = s; return v
# star(0) labels in 0-reps: (0,x,s) x=1..6 ; index 0,1 = Z (x=1)
S0labs = [((0, x), s) for x in range(1, 7) for s in (1, -1)]
R0 = np.array([rep(L) for L in S0labs])
Smat = np.array([[1.0 if (L[0] == M[0] and L[1] != M[1]) else 0.0 for M in S0labs] for L in S0labs])
def rand_inv(n=12):
    p = list(range(n)); rng.shuffle(p); inv = [0] * n
    for k in range(0, n, 2): inv[p[k]] = p[k + 1]; inv[p[k + 1]] = p[k]
    return inv
def pinv(A):
    w, V = np.linalg.eigh(A); keep = w > 1e-9; return (V[:, keep] / w[keep]) @ V[:, keep].T
res_all = []
for trial in range(6):
    signs = pat['patterns'][rng.randrange(len(pat['patterns']))]
    a = np.zeros(42)
    for k, s in zip(pat['cut'], signs): a[k] = s
    a[pat['V']] = 2
    alpha = np.array([a[idx[L]] for L in S0labs])          # 0-reps coincide with standard reps for star(0)
    # random S0 passing profile + a-test
    while True:
        Q, P = rand_inv(), rand_inv()
        forced = {1: [], -1: []}; bad = False
        for L in range(2, 12):
            zc = (Q[L] < 2) + (P[L] < 2)
            s0 = alpha[L] * (alpha[Q[L]] - alpha[P[L]]) if Q[L] != P[L] else 0
            if zc == 2 or (zc == 1 and s0 == 1) or (zc == 0 and s0 == 2): forced[alpha[L]].append(L)
        if len(forced[1]) > 2 or len(forced[-1]) > 2: continue
        T = np.zeros((12, 12))
        for i in range(12): T[i, Q[i]] += 1; T[i, P[i]] -= 1
        A0 = 11 * np.eye(12) + Smat - np.ones((12, 12)) - 4 * T
        A0p = pinv(A0)
        q = alpha @ A0p @ alpha
        if q <= 6 / 7 + 1e-9: break
    # P_sigma cap star(0): 2 labels of each alpha, containing the forced ones
    plus = [L for L in range(2, 12) if alpha[L] == 1]; minus = [L for L in range(2, 12) if alpha[L] == -1]
    cp = [c for c in itertools.combinations(plus, 2) if set(forced[1]) <= set(c)]
    cm = [c for c in itertools.combinations(minus, 2) if set(forced[-1]) <= set(c)]
    Ps0 = list(rng.choice(cp)) + list(rng.choice(cm))
    # V row (positive rep e5+e6, h=+2): v ~ -p for p in P_sigma; p = alpha_L * 0rep(L) -> v ~ -alpha_L 0rep(L) -> T = -alpha_L
    rV = rep(((5, 6), 1))
    tV = np.zeros(12)
    for L in Ps0: tV[L] = -alpha[L]
    mV = -4 * tV - R0 @ rV
    phi = 672 - 784 * q
    sV = 10 - mV @ A0p @ mV
    fV = 28 * (2 - alpha @ A0p @ mV)          # <F_perp, rho_V>
    counts = []
    for x in range(2, 7):
        for s in (1, -1):
            Yl = ((1, x), s); aY = a[idx[Yl]]; rY = aY * rep(Yl)       # positive rep
            n_all = n_ok = 0
            for plus2 in itertools.combinations_with_replacement(range(12), 2):
                if plus2[0] == plus2[1]: continue
                for minus2 in itertools.combinations(range(12), 2):
                    t = np.zeros(12)
                    for L in plus2: t[L] += 1
                    for L in minus2: t[L] -= 1
                    n_all += 1
                    zinc = sum(1 for L in plus2 if L < 2) + sum(1 for L in minus2 if L < 2)
                    so = sum(alpha[L] for L in plus2) - sum(alpha[L] for L in minus2)
                    # profile of Y: allowed sigma_other by zinc (P0 or P_sigma)
                    allowed = {2: {-2}, 1: {-3, -1}, 0: {-4, -2, 0}}.get(zinc, set())
                    if so not in allowed: continue
                    m = -4 * t - R0 @ rY
                    sY = 10 - m @ A0p @ m
                    if sY < -1e-9: continue
                    fY = 28 * (aY * aY - alpha @ A0p @ m)    # <F_perp, rho_Y>, a_Y in positive rep = 1
                    ok = False
                    for TVY in (0, -1):
                        g = -4 * TVY - rV @ rY - mV @ A0p @ m
                        G = np.array([[phi, fV, fY], [fV, sV, g], [fY, g, sY]])
                        if np.linalg.eigvalsh(G)[0] >= -1e-7: ok = True; break
                    if ok: n_ok += 1
            counts.append(n_ok)
    print('trial %d: a0 A0+ a0 = %.3f, phi = %.2f, s_V = %.2f, admissible columns per cut1 label: %s (of %d raw)' % (trial, q, phi, sV, counts, n_all), flush=True)
