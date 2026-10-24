"""Expérience 10 : graphes de transport B_xy (paires à distance 2) dans des membres de K_k de diamètre > 2, et
déplacement minimal des transformations de revêtement.

Pour {x, y} à distance 2, de voisins communs a, b : B_xy est biparti entre N(x)\\{a,b} et N(y)\\{a,b}. Les sommets
a' (partenaire de a dans N(x)) et b' ont degré 1 ; les autres sommets de N(x)\\{a,b} ont degré 2 si leur distance à y
vaut 2, et 0 si elle vaut 3. eps(x,y) = 1 si le chemin issu de a' revient du côté de x (il finit en b').
Pour un srg (diamètre 2), kappa_0(x,y) = (k+2)/(2k) si eps = 0 et (k+1)/(2k) si eps = 1.
On compte aussi les composantes cycliques (porteuses de H^1 dans la jauge radiale).

Déplacement : pour un revêtement triple de sommets 3u+s (g : s -> s+1), min d(x, gx) ; la théorie donne >= 5, et
les orbites sont alors des codes parfaits de rayon 2 si la base est de diamètre 2."""
import sys, json
from collections import deque, Counter
sys.path.insert(0, '.')
import srg_tools as T
from exp5_cover_invariants import cover, files


def bfs(N, adj, x):
    d = [-1] * N; d[x] = 0; q = deque([x])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if d[w] < 0:
                d[w] = d[u] + 1; q.append(w)
    return d


def partner(adj, x, a):
    (t,) = adj[x] & adj[a]
    return t


def transport_stats(N, adj, sample=None):
    eps = Counter(); cyc = Counter(); acyclic_roots = 0
    roots = range(N) if sample is None else sample
    for x in roots:
        d = bfs(N, adj, x)
        root_acyclic = True
        for y in range(N):
            if d[y] != 2:
                continue
            a, b = sorted(adj[x] & adj[y])
            X = adj[x] - {a, b}; Y = adj[y] - {a, b}
            nb = {('X', u): {('Y', w) for w in adj[u] & Y} for u in X}
            for w in Y:
                nb[('Y', w)] = {('X', u) for u in adj[w] & X}
            # chemin depuis a'
            prev, cur = None, ('X', partner(adj, x, a))
            while True:
                nxt = [z for z in nb[cur] if z != prev]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
            e = 1 if cur[0] == 'X' else 0
            eps[e] += 1
            # composantes cycliques
            seen = set(); ncyc = 0
            for v in nb:
                if v in seen or not nb[v]:
                    continue
                comp = []; st = [v]; seen.add(v)
                while st:
                    z = st.pop(); comp.append(z)
                    for t in nb[z]:
                        if t not in seen:
                            seen.add(t); st.append(t)
                if all(len(nb[z]) == 2 for z in comp):
                    ncyc += 1
            cyc[ncyc] += 1
            if ncyc:
                root_acyclic = False
        acyclic_roots += root_acyclic
    return dict(eps=dict(eps), cycle_components=dict(sorted(cyc.items())), roots=len(list(roots)),
                roots_with_all_B_acyclic=acyclic_roots)


def displacement(N, adj):
    best = None
    for u in range(0, N, 3 * 7):
        d = bfs(N, adj, u)
        g = 3 * (u // 3) + ((u % 3) + 1) % 3
        best = d[g] if best is None else min(best, d[g])
    return best


if __name__ == '__main__':
    out = {}
    for name in ('t2_twisted', 't3_twisted'):
        A = json.load(open(f'../../../data/{name}.json'))
        n = len(A); adj = [set(j for j in range(n) if A[i][j]) for i in range(n)]
        out[name] = transport_stats(n, adj)
        print(name, out[name], flush=True)
    for name, f in files.items():
        n, _, adj = T.load_edges(f)
        out[name] = transport_stats(n, adj, sample=range(0, n, 9))
        N, cadj = cover(f)
        out[name + '_cover3'] = transport_stats(N, cadj, sample=range(0, N, 27))
        out[name + '_cover3']['min_displacement'] = displacement(N, cadj)
        print(name, out[name], '\n ', name + '_cover3', out[name + '_cover3'], flush=True)
    json.dump(out, open('../data/exp10_transport_graphs.json', 'w'), indent=1)
