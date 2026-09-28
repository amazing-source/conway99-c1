"""Free-star spectra (C1, 28/09). Star c: 12 orbits (6 cells x 2), Pi = cell matching. mu = mate matching, tau = cross matching,
free star = mu, tau disjoint. w-frame star Gram D = 11I + Pi - J + 4(tau - mu); beta-frame star Gram G = 5I - Pi - 2(mu + tau).
mu is taken up to Aut(Pi) (11 classes = cycle types of mu u Pi), tau over all 10395 perfect matchings."""
import itertools
import numpy as np
from collections import Counter
def matchings(pts):
    if not pts: yield []; return
    a = pts[0]
    for i in range(1, len(pts)):
        rest = pts[1:i] + pts[i + 1:]
        for m in matchings(rest): yield [(a, pts[i])] + m
ALL = list(matchings(list(range(12))))
Pi = [(2 * i, 2 * i + 1) for i in range(6)]
def mat(m):
    M = np.zeros((12, 12), dtype=np.int64)
    for a, b in m: M[a, b] = M[b, a] = 1
    return M
def ctype(m):                                   # cycle type of m u Pi on the 6 cells
    adj = {i: set() for i in range(6)}
    for a, b in m: adj[a // 2].add(b // 2); adj[b // 2].add(a // 2)
    seen, t = set(), []
    for s in range(6):
        if s in seen: continue
        comp, st = set(), [s]
        while st:
            x = st.pop()
            if x in comp: continue
            comp.add(x); st.extend(adj[x] - comp)
        seen |= comp; t.append(len(comp))
    return tuple(sorted(t, reverse=True))
reps = {}
for m in ALL:
    reps.setdefault(ctype(m), m)
print('perfect matchings', len(ALL), '| mu classes under Aut(Pi):', len(reps))
I, J, P = np.eye(12, dtype=np.int64), np.ones((12, 12), dtype=np.int64), mat(Pi)
Q1 = np.eye(12) - np.ones((12, 12)) / 12
spec_w, spec_b, n, minw, maxw, ranks_b = set(), set(), 0, 99, -99, Counter()
for ct, mu in reps.items():
    Mu, se = mat(mu), set(mu)
    for tau in ALL:
        if se & set(tau): continue              # free star only
        n += 1; T = mat(tau)
        D = 11 * I + P - J + 4 * (T - Mu)
        ev = np.linalg.eigvalsh(Q1 @ D @ Q1); ev = np.sort(ev)[1:]   # drop the kernel vector 1
        spec_w.add(tuple(np.round(ev, 6))); minw = min(minw, ev.min()); maxw = max(maxw, ev.max())
        G = 5 * I - P - 2 * (Mu + T)
        eb = np.linalg.eigvalsh(G); spec_b.add(tuple(np.round(eb, 6))); ranks_b[int((eb > 1e-9).sum())] += 1
print('free (mu-class, tau) combos:', n)
print('w-frame star spectra: distinct', len(spec_w), '| eigenvalues on 1-perp in [%.3f, %.3f] -> rank 11 always' % (minw, maxw))
print('beta-frame star spectra: distinct', len(spec_b), '| rank distribution (= 12 - #clusters):', dict(sorted(ranks_b.items())))
