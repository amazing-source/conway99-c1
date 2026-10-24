"""Outils communs (lecture seule des données du dépôt) pour la campagne Perelman -> Conway.

Graphes : listes d'arêtes 0-indexées (format de data/srg243/*.edges).
Tout est exact (entiers, rangs mod p via python-flint).
"""
import itertools
from collections import defaultdict

import numpy as np


def load_edges(path):
    edges = []
    for line in open(path):
        line = line.strip()
        if line:
            i, j = map(int, line.split())
            edges.append((min(i, j), max(i, j)))
    n = 1 + max(max(e) for e in edges)
    adj = [set() for _ in range(n)]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    return n, sorted(set(edges)), adj


def check_srg(n, adj, k, lam, mu):
    for x in range(n):
        if len(adj[x]) != k:
            return False
    for x in range(n):
        for y in range(x + 1, n):
            c = len(adj[x] & adj[y])
            if (y in adj[x] and c != lam) or (y not in adj[x] and c != mu):
                return False
    return True


def lines_of(n, adj):
    """Triangles (= droites quand lambda = 1)."""
    L = set()
    for x in range(n):
        for y in adj[x]:
            if y > x:
                for z in adj[x] & adj[y]:
                    if z > y:
                        L.add((x, y, z))
    return sorted(L)


def squares_of(n, adj):
    """Quadrangles induits x-a-y-b (x,y non adjacents, a,b voisins communs).
    Avec mu = 2 chaque paire non adjacente est diagonale d'un unique quadrangle ;
    chaque quadrangle a deux diagonales. On renvoie (x, a, y, b) avec x < y, x = min."""
    Q = set()
    for x in range(n):
        for y in range(x + 1, n):
            if y in adj[x]:
                continue
            com = sorted(adj[x] & adj[y])
            for a, b in itertools.combinations(com, 2):
                cyc = (x, a, y, b)
                # forme canonique : rotation/réflexion minimale
                rots = []
                c = list(cyc)
                for r in range(4):
                    cc = c[r:] + c[:r]
                    rots.append(tuple(cc))
                    rots.append(tuple([cc[0]] + cc[1:][::-1]))
                Q.add(min(rots))
    return sorted(Q)


def edge_index(edges):
    return {e: i for i, e in enumerate(edges)}


def boundary_2_rows(edges, lines, squares):
    """Lignes du cobord delta_1 (une par 2-cellule) : liste de (indices, signes).
    Arête (i,j) orientée i<j. Une 2-cellule de bord v0 v1 ... v_{m-1} donne
    la somme orientée des arêtes."""
    eidx = edge_index(edges)
    rows = []
    for cell in list(lines) + list(squares):
        m = len(cell)
        idx, sg = [], []
        for t in range(m):
            u, v = cell[t], cell[(t + 1) % m]
            if u < v:
                idx.append(eidx[(u, v)]); sg.append(1)
            else:
                idx.append(eidx[(v, u)]); sg.append(-1)
        rows.append((idx, sg))
    return rows


def rank_mod_p_rows(rows, ncols, p):
    import flint
    M = flint.nmod_mat(len(rows), ncols, p)
    for r, (idx, sg) in enumerate(rows):
        for c, s in zip(idx, sg):
            M[r, c] = (int(M[r, c]) + s) % p
    return M.rank()


def betti1_mod_p(n, edges, adj, p, lines=None, squares=None):
    """dim H_1(X; F_p) pour X = complexe triangles + quadrangles (graphe connexe)."""
    if lines is None:
        lines = lines_of(n, adj)
    if squares is None:
        squares = squares_of(n, adj)
    rows = boundary_2_rows(edges, lines, squares)
    rk = rank_mod_p_rows(rows, len(edges), p)
    cyc = len(edges) - n + 1
    return cyc - rk, dict(cycle_space=cyc, rank_boundary=rk, n_lines=len(lines), n_squares=len(squares))


def nonedge_transport_parity(n, adj):
    """Pour chaque paire non adjacente {x,y} de voisins communs a,b :
    graphe biparti B_xy entre X = N(x)\\{a,b} et Y = N(y)\\{a,b} (arêtes de Gamma).
    Dans un srg(v,k,1,2), degrés (1,1,2,...,2) de chaque côté : 2 chemins + cycles.
    eps = 1 si les deux sommets de degré 1 de X sont reliés par un chemin (pas de couplage parfait).
    Courbure d'Ollivier (marche simple, sans paresse) : kappa = 1 - W1/2,
    W1 = (m + 2(k-2-m))/k, m = couplage maximum.
    Renvoie un dict (x,y) -> (eps, nb_cycles, longueurs des cycles, longueurs des chemins)."""
    out = {}
    for x in range(n):
        for y in range(x + 1, n):
            if y in adj[x]:
                continue
            ab = adj[x] & adj[y]
            X = adj[x] - ab
            Y = adj[y] - ab
            # graphe biparti
            nb = defaultdict(set)
            for u in X:
                for w in adj[u] & Y:
                    nb[('X', u)].add(('Y', w))
                    nb[('Y', w)].add(('X', u))
            deg1 = [v for v in [('X', u) for u in X] + [('Y', w) for w in Y] if len(nb[v]) == 1]
            # composantes
            seen = set()
            comps = []
            for v in [('X', u) for u in X] + [('Y', w) for w in Y]:
                if v in seen:
                    continue
                stack = [v]; comp = []
                seen.add(v)
                while stack:
                    z = stack.pop(); comp.append(z)
                    for t in nb[z]:
                        if t not in seen:
                            seen.add(t); stack.append(t)
                comps.append(comp)
            paths, cycles = [], []
            eps = 0
            for comp in comps:
                ends = [v for v in comp if len(nb[v]) == 1]
                if ends:
                    paths.append(len(comp))
                    if len(ends) == 2 and ends[0][0] == ends[1][0]:
                        eps = 1
                else:
                    cycles.append(len(comp))
            out[(x, y)] = (eps, tuple(sorted(paths)), tuple(sorted(cycles)))
    return out


def hamming_profile(n, adj, lines):
    """Pour chaque sommet x : nombre de paires de droites par x qui engendrent une grille 3x3 induite.
    (x 'point de Hamming' si toutes les paires le font.)"""
    lines_at = defaultdict(list)
    for L in lines:
        for v in L:
            lines_at[v].append(L)
    prof = []
    for x in range(n):
        Ls = lines_at[x]
        g = 0
        for L, M in itertools.combinations(Ls, 2):
            a, a2 = [v for v in L if v != x]
            b, b2 = [v for v in M if v != x]
            def comp(p, q):
                cn = (adj[p] & adj[q]) - {x}
                return next(iter(cn)) if len(cn) == 1 else None
            e = [comp(a, b), comp(a, b2), comp(a2, b), comp(a2, b2)]
            if None in e:
                continue
            S = [x, a, a2, b, b2] + e
            if len(set(S)) == 9 and all(len(adj[s] & set(S)) == 4 for s in S):
                g += 1
        prof.append(g)
    return prof
