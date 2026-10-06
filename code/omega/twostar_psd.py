"""Conway, rooted at v: two mate stars L_a, L_a' (24 labels {a,x}, {a',x}, x in E, |E| = 12 = 6 mate pairs).
Gamma on them = tau (matching on L_a) + tau' (matching on L_a') + sigma ({a,x} ~ {a',sigma(x)}).
T_S = 3I - Gamma - K_S must be PSD (7 x Gram of frame vectors), with kernel containing the two star sums.
Random (tau, tau', sigma) satisfying the local lambda/mu caps: fraction PSD, rank distribution."""
import random, itertools, numpy as np, sys
E = list(range(12)); mate = lambda x: x ^ 1
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
def rand_matching():
    p = E[:]; rng.shuffle(p); m = {}
    for i in range(0, 12, 2): m[p[i]] = p[i + 1]; m[p[i + 1]] = p[i]
    return m
def caps_ok(t, tp, s):
    si = {s[x]: x for x in E}
    for x in E:
        for z in E:
            if z == s[x]: continue
            if (z == x) + (s[t[x]] == z) + (s[x] == tp[z]) > 2: return False
    for x in E:
        for y in E:
            if y == x: continue
            if (y == t[x]) + (s[y] == x) + (y == mate(x)) > 2: return False
            if (y == tp[x]) + (si[y] == x) + (y == mate(x)) > 2: return False
    return True
def TS(t, tp, s):
    lab = [("a", x) for x in E] + [("ap", x) for x in E]
    n = 24; G = np.zeros((n, n)); K = np.zeros((n, n))
    for i, (si_, x) in enumerate(lab):
        for j, (sj, y) in enumerate(lab):
            if si_ == sj == "a" and t[x] == y: G[i, j] = 1
            if si_ == sj == "ap" and tp[x] == y: G[i, j] = 1
            if si_ == "a" and sj == "ap" and s[x] == y: G[i, j] = 1
            if si_ == "ap" and sj == "a" and s[y] == x: G[i, j] = 1
            # labels {a or a', x}: intersection and mate relations (a, a' are mates)
            e1 = {si_, ("x", x)}; e2 = {sj, ("x", y)}
            inter = (si_ == sj) + (x == y)
            m = (si_ != sj) + (y == mate(x))
            K[i, j] = 3 / 8 * inter + 1 / 8 * m - 1 / 4
    return 3 * np.eye(n) - G - K
tot = ok = 0; ranks = {}; minev = []
while tot < 20000:
    t, tp = rand_matching(), rand_matching(); s = dict(zip(E, rng.sample(E, 12)))
    if not caps_ok(t, tp, s): continue
    tot += 1
    ev = np.linalg.eigvalsh(TS(t, tp, s)); minev.append(ev.min())
    if ev.min() > -1e-9:
        ok += 1; r = int((ev > 1e-9).sum()); ranks[r] = ranks.get(r, 0) + 1
print("random admissible (tau,tau',sigma):", tot, " T_S PSD:", ok, " ranks:", ranks, " min eig range:", round(min(minev), 3), round(max(minev), 3))
