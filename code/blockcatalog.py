# Block-type catalog of Borcherds' odd unimodular 24-dim lattices (C1 27/09 night, triage for route (C)). Light: roots, new roots, norm 3.
import json, sys, time
import numpy as np
sys.path.insert(0, r'C:\Users\RESEARCHER\Desktop\c1_recherche\code')
from y_pairs import setup
ENV = r'C:\Users\RESEARCHER\Desktop\c99_structures_lab\involution\envelopes\U\%03d.json'

def canon(V):
    out = {}
    for v in V:
        k = np.nonzero(np.abs(v) > 1e-9)[0][0]
        w = -v if v[k] < 0 else v
        out[tuple(np.round(w, 6))] = w
    return np.array(list(out.values())) if out else np.zeros((0, 24))

def comps(V):
    n = len(V)
    G = np.abs(V @ V.T) > 1e-6
    lab = -np.ones(n, int); cs = []
    for s in range(n):
        if lab[s] >= 0: continue
        lab[s] = len(cs); st = [s]; cur = [s]
        while st:
            i = st.pop()
            for j in np.nonzero(G[i] & (lab < 0))[0]:
                lab[j] = len(cs); st.append(j); cur.append(j)
        cs.append(cur)
    return cs

def rtype(V):
    N = 2 * len(V); rk = np.linalg.matrix_rank(V, tol=1e-6)
    if N == rk * (rk + 1): return 'A%d' % rk
    if N == 2 * rk * (rk - 1): return 'D%d' % rk
    return {72: 'E6', 126: 'E7', 240: 'E8'}.get(N, '?%d/%d' % (N, rk))

def one(i):
    rec = json.load(open(ENV % i))
    B, Gi, Bf, R, X3, Snew = setup(rec['gens'])
    R = canon(R) if len(R) else np.zeros((0, 24))
    out = {'id': i, 'r': 2 * len(R), 'n3': len(X3), 'nb': [], 'm0': [], 'mmin': []}
    if len(Snew):
        b0 = Snew[0]
        ip = Snew @ b0
        cls = np.abs(ip - np.round(ip)) < 1e-6
        parts = [Snew[cls], Snew[~cls]]
    else:
        parts = [np.zeros((0, 24)), np.zeros((0, 24))]
    for P in parts:
        if len(P) == 0:
            out['nb'].append([]); out['m0'].append(len(X3)); out['mmin'].append(0); continue
        m = (np.abs(np.abs(X3 @ P.T) - 1.5) < 1e-6).sum(axis=1) // 2
        out['m0'].append(int((m == 0).sum())); out['mmin'].append(int(m.min()))
        Pn = canon(P)
        Phi = np.vstack([R, Pn]) if len(R) else Pn
        isnew = np.array([False] * len(R) + [True] * len(Pn))
        blocks = []
        for c in comps(Phi):
            c = np.array(c)
            if not isnew[c].any(): continue
            Xt = rtype(Phi[c])
            Yc = c[~isnew[c]]
            Yt = sorted(rtype(Phi[Yc][cc]) for cc in comps(Phi[Yc])) if len(Yc) else []
            blocks.append('%s>%s' % (Xt, '+'.join(Yt) if Yt else '0'))
        out['nb'].append(sorted(blocks))
    return out

a, b = int(sys.argv[1]), int(sys.argv[2])
fo = open(sys.argv[3], 'a')
for i in range(a, b):
    t0 = time.time()
    try:
        o = one(i)
    except Exception as e:
        o = {'id': i, 'error': repr(e)[:200]}
    o['s'] = round(time.time() - t0, 1)
    fo.write(json.dumps(o) + '\n'); fo.flush()
    print(json.dumps(o)[:300], flush=True)
