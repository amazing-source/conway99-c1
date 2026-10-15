"""Low-rank projection walk (LAB 15/10/2026, task T3): a search for PSD four-star structures of nullity 14 with NO
symmetry imposed and no symmetric seed (to test the bias of the group searches behind (H-MATCH) / (H-INV)).

Step: T = 3I - Gamma - K.  Target T* = a PSD matrix of rank <= 30 with 7 Pi - T* PSD, obtained by a few alternating
projections (keep the 30 largest non-negative eigenvalues of T; clip U = 7 Pi - T to its PSD part).  Gamma* = 3I - K - T*
(real).  The SAT model (C1, C1', C2 of stars_rank.build) is re-solved under the assumptions 'pair p takes the value
[Gamma*_p > 1/2]' for the q pairs with the largest confidence |Gamma*_p - 1/2| (+ noise), q shrunk until satisfiable.
Score (lower is better): sum of the 14 smallest |eigenvalues| of T + 3 (negative parts of T and of U on the complement
of the star vectors).  Metropolis acceptance; restart from a random admissible structure when the best does not improve.
Records PSD structures of numerical nullity >= 13; for nullity >= 14 reports whether the star matchings are h-related
and whether the structure is h-invariant (h = (0 1)(2 3) is NOT imposed).
usage: python projwalk.py <out prefix> <seconds> [seed] [init json]"""
import itertools
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS

out, maxsec = sys.argv[1], float(sys.argv[2])
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
initf = sys.argv[4] if len(sys.argv) > 4 else None
rng = random.Random(seed)
nrng = np.random.default_rng(seed)
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
pairs = list(itertools.combinations(range(n), 2))
pi_, pj_ = np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs])
Kf = np.array([[kval(a, b) for b in S] for a in S])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
P7 = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]


def to_G(model):
    G = np.zeros((n, n))
    for p in pairs:
        if model[e[p]]:
            G[p] = 1
            G[p[1], p[0]] = 1
    return G


def evaluate(G):
    T = 3 * np.eye(n) - G - Kf
    w = np.linalg.eigvalsh(T)
    small = float(np.sort(np.abs(w))[:14].sum())
    lt = np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))
    lu = np.linalg.eigvalsh(Pp @ (P7 - T) @ Pp + 50 * (np.eye(n) - Pp))
    neg = float(-lt[lt < 0].sum() - lu[lu < 0].sum())
    nul = int(np.sum(np.abs(w) < 1e-8))
    return small + 3 * neg, nul, bool(lt[0] > -1e-9 and lu[0] > -1e-9)


def target(G, rounds=4):
    T = 3 * np.eye(n) - G - Kf
    for _ in range(rounds):
        w, V = np.linalg.eigh(T)
        w = np.clip(w, 0, None)
        w[: n - 30] = 0                       # keep the 30 largest
        T = (V * w) @ V.T
        U = P7 - T
        wu, Vu = np.linalg.eigh(U)
        U = (Vu * np.clip(wu, 0, None)) @ Vu.T
        T = P7 - U
    return 3 * np.eye(n) - Kf - T


def project(G, noise):
    """Move towards the projected target: force a few of the changes it asks for, fix the most confident other pairs."""
    Gs = target(G)
    vals = Gs[pi_, pj_]
    pref = vals > 0.5
    curv = G[pi_, pj_] > 0.5
    conf = np.abs(vals - 0.5) + noise * nrng.standard_normal(len(pairs))
    want = [k for k in np.argsort(-conf) if pref[k] != curv[k]]
    keep = [k for k in np.argsort(-conf) if pref[k] == curv[k]]
    nforce = min(len(want), rng.randint(1, 12))
    frac = 0.55 + 0.35 * rng.random()
    q = int(frac * len(keep))
    forced = want[:nforce]
    while True:
        assum = [e[pairs[k]] if pref[k] else -e[pairs[k]] for k in forced + keep[:q]]
        ok, m = sol.solve(assum)
        if ok:
            return to_G(m), len(forced)
        if forced:
            forced = forced[:-1]
        elif q > 0:
            q = int(q * 0.8)
        else:
            ok, m = sol.solve()
            return to_G(m), 0


def random_start():
    assum = [e[p] if rng.random() < 0.13 else -e[p] for p in rng.sample(pairs, 60)]
    ok, m = sol.solve(assum)
    if not ok:
        ok, m = sol.solve()
    return to_G(m)


if initf:
    d = json.load(open(initf))
    G = np.zeros((n, n))
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
else:
    G = random_start()
cur, nul, psd = evaluate(G)
best, best_t = cur, time.time()
t0 = time.time()
step = 0
temp = 0.5
found = {}
hist = {}
print("start: score %.3f nullity %d PSD %s" % (cur, nul, psd), flush=True)
while time.time() - t0 < maxsec:
    step += 1
    noise = 0.05 + 0.25 * rng.random()
    G2, q = project(G, noise)
    s2, nul2, psd2 = evaluate(G2)
    if psd2:
        hist[nul2] = hist.get(nul2, 0) + 1
    if psd2 and nul2 >= 13:
        key = hash(G2[np.triu_indices(n, 1)].tobytes())
        if key not in found:
            broken = any(G2[i, j] != G2[hp[i], hp[j]] for (i, j) in sl)
            hinv = bool(np.array_equal(G2[np.ix_(hp, hp)], G2))
            found[key] = (nul2, broken, hinv)
            k = len(found)
            json.dump({"labels": [sorted(l) for l in S], "edges": [[i, j] for i, j in pairs if G2[i, j]],
                       "nullity_numeric": nul2, "matchings_broken": broken, "h_invariant": hinv},
                      open("%s_P%d_%d.json" % (out, nul2, k), "w"))
            print("step %d: PSD nullity %d, matchings %s, h-invariant %s (saved %s_P%d_%d.json), %.0f s"
                  % (step, nul2, "BROKEN" if broken else "h-related", hinv, out, nul2, k, time.time() - t0), flush=True)
            if nul2 >= 14 and broken:
                print("step %d: PROJWALK TARGET: PSD nullity >= 14 with broken matchings" % step, flush=True)
    if s2 <= cur or rng.random() < math.exp(-(s2 - cur) / temp):
        G, cur = G2, s2
    if cur < best - 1e-6:
        best, best_t = cur, time.time()
    if time.time() - best_t > 60:
        G = random_start()
        cur, _, _ = evaluate(G)
        best, best_t = cur, time.time()
        print("step %d: restart" % step, flush=True)
    if step % 200 == 0:
        print("step %d: %.0f s, current score %.3f, best %.3f, PSD nullity histogram %s, found %d"
              % (step, time.time() - t0, cur, best, dict(sorted(hist.items())), len(found)), flush=True)
print("end: %d steps, PSD nullity histogram %s, structures of nullity >= 13 found: %d, of which nullity >= 14 broken: %d"
      % (step, dict(sorted(hist.items())), len(found), sum(1 for v in found.values() if v[0] >= 14 and v[1])), flush=True)
