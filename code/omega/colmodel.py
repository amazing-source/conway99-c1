"""Column stage of Route Omega in symmetric 3-layer form (notes/163).

Triangle T = {v,a,a'} of an srg(n,k,1,2).  Layers (index set E = N(v) - {a,a'}, size m = k-2):
  layer 0 = E itself, layer 1 = L_a = N(a)-{v,a'}, layer 2 = L_a' = N(a')-{v,a}; a label l in L_a (L_a') is identified
  with the unique z in E adjacent to it.  C is encoded by four maps on E:
  M (mates in E), ta (matching of L_a), tb (matching of L_a'), s (cross bijection L_a -> L_a': {a,z} ~ {a',s(z)}).
Far vertices (not adjacent to T) meet each layer in exactly 2 non-matched vertices: a far vertex is a triple of pairs
  (p0, p1, p2), p_i an edge of the cocktail-party graph CP_i (K_m minus the layer matching), each edge used once.
Claim (checked here exactly on real graphs): the cross-layer incidence matrices are
  N01[x][z] = 2 - [x=z] - [x=Mz] - [x=ta z] - [x=s z]
  N02[x][y] = 2 - [x=y] - [x=My] - [x=tb y] - [x=s^-1 y]
  N12[z][y] = 2 - [y=z] - [y=s z] - [y=s ta z] - [y=tb s z]
where Nij[u][u'] = #{far w : u in p_i(w), u' in p_j(w)}."""
import sys, itertools, json
import numpy as np


def load_edges(path, n):
    adj = [set() for _ in range(n)]
    for line in open(path):
        if line.strip():
            i, j = map(int, line.split()); adj[i].add(j); adj[j].add(i)
    return adj


def triangle_structure(adj, v, a, a2):
    E = sorted(adj[v] - {a, a2}); idx = {x: i for i, x in enumerate(E)}; m = len(E)
    La = sorted(adj[a] - {v, a2}); Lb = sorted(adj[a2] - {v, a})
    def ident(l):
        z = [x for x in E if x in adj[l]]
        assert len(z) == 1; return idx[z[0]]
    ia = {l: ident(l) for l in La}; ib = {l: ident(l) for l in Lb}
    assert sorted(ia.values()) == list(range(m)) and sorted(ib.values()) == list(range(m))
    M = [None] * m; ta = [None] * m; tb = [None] * m; s = [None] * m
    for x in E:
        y = [u for u in E if u in adj[x]]; assert len(y) == 1; M[idx[x]] = idx[y[0]]
    for l in La:
        y = [u for u in La if u in adj[l]]; assert len(y) == 1; ta[ia[l]] = ia[y[0]]
        w = [u for u in Lb if u in adj[l]]; assert len(w) == 1; s[ia[l]] = ib[w[0]]
    for l in Lb:
        y = [u for u in Lb if u in adj[l]]; assert len(y) == 1; tb[ib[l]] = ib[y[0]]
    ball = {v, a, a2} | set(E) | set(La) | set(Lb)
    far = [w for w in range(len(adj)) if w not in ball]
    triples = []
    for w in far:
        p0 = tuple(sorted(idx[x] for x in E if x in adj[w]))
        p1 = tuple(sorted(ia[l] for l in La if l in adj[w]))
        p2 = tuple(sorted(ib[l] for l in Lb if l in adj[w]))
        assert len(p0) == len(p1) == len(p2) == 2
        triples.append((p0, p1, p2))
    return dict(m=m, M=M, ta=ta, tb=tb, s=s, triples=triples)


def predicted(C):
    m, M, ta, tb, s = C["m"], C["M"], C["ta"], C["tb"], C["s"]
    sinv = [0] * m
    for z in range(m): sinv[s[z]] = z
    N01 = [[2 - (x == z) - (x == M[z]) - (x == ta[z]) - (x == s[z]) for z in range(m)] for x in range(m)]
    N02 = [[2 - (x == y) - (x == M[y]) - (x == tb[y]) - (x == sinv[y]) for y in range(m)] for x in range(m)]
    N12 = [[2 - (y == z) - (y == s[z]) - (y == s[ta[z]]) - (y == tb[s[z]]) for y in range(m)] for z in range(m)]
    return N01, N02, N12


def observed(C):
    m = C["m"]; N = {k: [[0] * m for _ in range(m)] for k in ("01", "02", "12")}
    for p0, p1, p2 in C["triples"]:
        for (P, Q, key) in ((p0, p1, "01"), (p0, p2, "02"), (p1, p2, "12")):
            for u in P:
                for u2 in Q:
                    N[key][u][u2] += 1
    return N["01"], N["02"], N["12"]


def check_bijective(C):
    m = C["m"]; out = []
    for i, mt in enumerate((C["M"], C["ta"], C["tb"])):
        used = [t[i] for t in C["triples"]]
        cp = {(x, y) for x in range(m) for y in range(x + 1, m) if mt[x] != y}
        out.append(len(set(used)) == len(used) and set(used) == cp)
    return out


if __name__ == "__main__":
    path, n = sys.argv[1], int(sys.argv[2])
    adj = load_edges(path, n)
    tested = 0
    for v in range(0, n, max(1, n // 12)):
        for a in sorted(adj[v]):
            a2 = [u for u in adj[v] if u in adj[a]][0]
            if a2 < a: continue
            C = triangle_structure(adj, v, a, a2)
            ok_pred = predicted(C) == observed(C)
            ok_bij = check_bijective(C)
            assert ok_pred and all(ok_bij), (v, a, a2, ok_bij)
            tested += 1
    print(f"{path}: {tested} triangles, formulas N01/N02/N12 exact and far triples bijective on all three layers")
