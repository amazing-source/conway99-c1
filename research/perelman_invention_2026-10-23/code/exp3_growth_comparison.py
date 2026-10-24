"""Expérience 3 : comparaison de croissance « à la Bishop–Gromov » dans la classe K_{2n}
(chaque arête dans un unique triangle, mu = 2 à distance 2, valence 2n).
Conjecture testée : |S_i(x)| <= C(n,i) 2^i (sphères de H(n,3)), et la propriété (L) :
tout y dans S_i est sur au moins i droites qui rencontrent S_{i-1}.
Exemples : géométries tordues de l'équipe (t=2 : 20 sommets ; t=3 : 39 sommets), Hamming,
produits cartésiens, revêtements triples des srg(243) tordus (via le cocycle d'étalement)."""
import sys, json, itertools
from math import comb
from collections import deque, Counter
sys.path.insert(0, '.')
from srg_tools import load_edges, lines_of

def adj_from_matrix(A):
    n = len(A)
    return n, [set(j for j in range(n) if A[i][j]) for i in range(n)]

def hamming(n, q=3):
    V = list(itertools.product(range(q), repeat=n))
    idx = {v: i for i, v in enumerate(V)}
    adj = [set() for _ in V]
    for v in V:
        for c in range(n):
            for a in range(q):
                if a != v[c]:
                    w = list(v); w[c] = a
                    adj[idx[v]].add(idx[tuple(w)])
    return len(V), adj

def product(G, H):
    n1, a1 = G; n2, a2 = H
    adj = [set() for _ in range(n1 * n2)]
    for u in range(n1):
        for v in range(n2):
            i = u * n2 + v
            for u2 in a1[u]: adj[i].add(u2 * n2 + v)
            for v2 in a2[v]: adj[i].add(u * n2 + v2)
    return n1 * n2, adj

def check_K(n, adj):
    k = len(adj[0])
    for x in range(n):
        if len(adj[x]) != k: return False, 'irregular'
        for y in adj[x]:
            if len(adj[x] & adj[y]) != 1: return False, 'lambda'
    # mu = 2 at distance 2
    for x in range(n):
        d2 = set().union(*[adj[y] for y in adj[x]]) - adj[x] - {x}
        for z in d2:
            if len(adj[x] & adj[z]) != 2: return False, 'mu'
    return True, k

def spheres(n, adj, x):
    dist = [-1] * n; dist[x] = 0; dq = deque([x])
    while dq:
        u = dq.popleft()
        for w in adj[u]:
            if dist[w] < 0:
                dist[w] = dist[u] + 1; dq.append(w)
    return dist

def analyse(name, n, adj):
    ok, k = check_K(n, adj)
    assert ok, (name, k)
    m = k // 2
    bound = [comb(m, i) * 2 ** i for i in range(m + 1)]
    worst_ratio = 0.0; profiles = Counter(); Lviol = 0; tested = 0
    # droites
    tri = {}
    for u in range(n):
        for v in adj[u]:
            if v > u:
                for w in adj[u] & adj[v]:
                    if w > v:
                        for p in (u, v, w): tri.setdefault(p, []).append((u, v, w))
    for x in range(n):
        dist = spheres(n, adj, x)
        prof = tuple(Counter(dist).get(i, 0) for i in range(max(dist) + 1))
        profiles[prof] += 1
        for i, s in enumerate(prof):
            if i <= m:
                worst_ratio = max(worst_ratio, s / bound[i])
            else:
                worst_ratio = float('inf')
        # propriété (L)
        for y in range(n):
            i = dist[y]
            if i >= 1:
                tested += 1
                ell = sum(1 for L in tri[y] if any(dist[p] == i - 1 for p in L if p != y))
                if ell < i: Lviol += 1
    print(f'{name}: |V|={n} k={k} borne Hamming={bound} profils={dict(profiles)} '
          f'max |S_i|/borne={worst_ratio:.3f} violations de (L)={Lviol}/{tested}', flush=True)
    return dict(n=n, k=k, bound=bound, profiles={str(p): c for p, c in profiles.items()},
                max_ratio=worst_ratio, L_violations=Lviol, L_tested=tested)

if __name__ == '__main__':
    res = {}
    R = '/home/user/conway99-c1/data/'
    t2 = adj_from_matrix(json.load(open(R + 't2_twisted.json')))
    t3 = adj_from_matrix(json.load(open(R + 't3_twisted.json')))
    res['t2_twisted(k=6)'] = analyse('t2_twisted(k=6)', *t2)
    res['t3_twisted(k=8)'] = analyse('t3_twisted(k=8)', *t3)
    res['H(3,3)'] = analyse('H(3,3)', *hamming(3))
    res['H(4,3)'] = analyse('H(4,3)', *hamming(4))
    res['t2 x t3 (k=14)'] = analyse('t2 x t3 (k=14)', *product(t2, t3))
    res['t2 x t2 (k=12)'] = analyse('t2 x t2 (k=12)', *product(t2, t2))
    json.dump(res, open('../data/exp3_growth_comparison.json', 'w'), indent=1)
