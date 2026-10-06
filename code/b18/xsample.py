"""Random complete X-configurations (uniform over random DFS paths that succeed) and the PSD margin of
K = 27I - 9A + J on support u X with no X-X edge.  X-X edges form a forest of <= 9 edges (spectral norm <= 2), so
lambda_min(K) < -18 kills the configuration whatever the X-X edges are."""
import json, random, sys, itertools
import numpy as np
sups = json.load(open('supports18.json'))

def sample_x(rows, rng, tries=100000):
    rows = [set(r) for r in rows]
    cols = [set(p for p in range(9) if v in rows[p]) for v in range(9)]
    D = [[1 if v in rows[p] else 0 for v in range(9)] for p in range(9)]
    Ps = []; Ns = []
    for a, b in itertools.combinations(range(9), 2):
        Ps += [(a, b)] * (2 - len(rows[a] & rows[b])); Ns += [(a, b)] * (2 - len(cols[a] & cols[b]))
    for _ in range(tries):
        Nleft = list(Ns); chosen = []; x = [[0]*9 for _ in range(9)]; ok = True
        order = list(range(18)); rng.shuffle(order)
        for i in order:
            pi = Ps[i]
            cand = []
            for nu in set(Nleft):
                if any(len(set(nu) & rows[p]) > 1 for p in pi) or any(len(set(pi) & cols[v]) > 1 for v in nu): continue
                if any(x[p][v] + 1 > 2 - D[p][v] for p in pi for v in nu): continue
                if any(len(set(pi) & set(pk)) + len(set(nu) & set(nk)) > 2 for pk, nk in chosen): continue
                cand.append(nu)
            if not cand: ok = False; break
            nu = rng.choice(cand); Nleft.remove(nu); chosen.append((pi, nu))
            for p in pi:
                for v in nu: x[p][v] += 1
        if ok: return chosen, D
    return None

def kmin(chosen, D):
    n = 36; A = np.zeros((n, n))
    for p in range(9):
        for v in range(9):
            if D[p][v]: A[p, 9 + v] = A[9 + v, p] = 1
    for k, (pi, nu) in enumerate(chosen):
        u = 18 + k
        for p in pi: A[u, p] = A[p, u] = 1
        for v in nu: A[u, 9 + v] = A[9 + v, u] = 1
    K = 27 * np.eye(n) - 9 * A + 1
    return np.linalg.eigvalsh(K).min()

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
for s in range(len(sups)):
    vals = []
    for t in range(40):
        r = sample_x(sups[s], rng)
        if r is None: continue
        vals.append(kmin(*r))
    vals = np.array(vals)
    print(s, 'samples', len(vals), 'lambda_min: min %.1f median %.1f max %.1f' % (vals.min(), np.median(vals), vals.max()),
          'dead(<-18):', int((vals < -18).sum()), flush=True)
