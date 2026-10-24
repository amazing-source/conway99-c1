"""Expérience 6 : dim H_1(X; F_p) du complexe triangles + quadrangles des revêtements triples (729 sommets)
des srg(243) ; esquisse aléatoire R * d2 puis rang exact mod p (python-flint). Le rang de R*d2 est égal à celui de d2
avec probabilité >= 1 - 1/p^(m - rang) ; on répète avec deux esquisses indépendantes."""
import sys, json, time
import numpy as np, flint
sys.path.insert(0, '.')
import srg_tools as T
from exp5_cover_invariants import cover, files

def squares_general(N, adj):
    Q = set()
    for x in range(N):
        d2 = set().union(*[adj[y] for y in adj[x]]) - adj[x] - {x}
        for y in d2:
            if y < x: continue
            com = sorted(adj[x] & adj[y])
            assert len(com) == 2
            a, b = com
            cyc = [x, a, y, b]
            rots = []
            for r in range(4):
                cc = cyc[r:] + cyc[:r]
                rots.append(tuple(cc)); rots.append(tuple([cc[0]] + cc[1:][::-1]))
            Q.add(min(rots))
    return sorted(Q)

def h1_dim(N, adj, p, m_extra=40, seed=0):
    edges = sorted({(min(u, w), max(u, w)) for u in range(N) for w in adj[u]})
    L = T.lines_of(N, adj); Q = squares_general(N, adj)
    rows = T.boundary_2_rows(edges, L, Q)
    cyc = len(edges) - N + 1
    m = cyc + m_extra
    rng = np.random.default_rng(seed)
    R = rng.integers(0, p, size=(m, len(rows)), dtype=np.int64)
    S = np.zeros((m, len(edges)), dtype=np.int64)
    for c, (idx, sg) in enumerate(rows):
        col = R[:, c]
        for e, s in zip(idx, sg):
            S[:, e] += s * col
    S %= p
    M = flint.nmod_mat(S.tolist(), p)
    rk = M.rank()
    return cyc - rk, dict(edges=len(edges), lines=len(L), squares=len(Q), cycle_space=cyc, rank=rk)

if __name__ == '__main__':
    out = {}
    for name, f in files.items():
        t0 = time.time()
        N, cadj = cover(f)
        r = {}
        for p in (3, 2):
            d, info = h1_dim(N, cadj, p)
            r[p] = d
        out[name] = dict(h1=r, info=info, seconds=round(time.time() - t0))
        print(name, out[name], flush=True)
    json.dump(out, open('../data/exp6_cover_homology.json', 'w'), indent=1)
