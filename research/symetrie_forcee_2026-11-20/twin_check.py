"""Échange de jumeaux u <-> u' dans un bord positif : test sur les srg(v,k,1,2) connus.

Pour une non-arête (u,u'), X = N(u)\\N(u'), Y = N(u')\\N(u), Ag = sommets qui voient u et u' pareil.
On vérifie : (1) les w de Ag ∪ {u,u'} engendrent E_s ; (2) la réflexion R_z, z = w_u - w_u', envoie w_x
(x dans X) sur un vecteur de produit scalaire 1 - (w1-w2)^2/(1-w2) avec w_x (Gram normalisé, diagonale 1) ;
(3) R_z(w_x) est-il un w_y ? (4) dans un bord positif S' ∪ {u,u'} ⊂ Ag ∪ {u,u'}, combien de couples (x,y)
ont le même motif sur S' ?
"""
import os, sys
from fractions import Fraction
import numpy as np

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
sys.path.insert(0, R + 'research/perelman_invention_2026-10-23/code')
from srg_tools import load_edges, check_srg

FILES = ['data/srg243/bvls243.edges', 'data/srg243/twin243_switched.edges',
         'data/srg243/family/gamma3_aut864.edges', 'data/srg243/family/gamma4_aut3888.edges',
         'code/lab_spreadfree_243_2026-10-12/new243_trade_aut108.edges',
         'code/lab_spreadfree_243_2026-10-12/new243_trade_aut108_b.edges',
         'code/lab_spreadfree_243_2026-10-12/new243_trade_aut162.edges',
         'code/lab_spreadfree_243_2026-10-12/new243_tricayley_Z3x4_grids25.edges']


def rook3():
    adj = [set() for _ in range(9)]
    for a in range(9):
        for b in range(9):
            if a != b and (a // 3 == b // 3 or a % 3 == b % 3):
                adj[a].add(b)
    return 9, adj


def predicted(k):
    # s = plus petite valeur propre de x^2 + x - (k-2) ; cosinus w1 = s/k, w2 = (s^2 - s - k)/(k(k-2))
    m = int(round((4 * k - 7) ** 0.5)); s = Fraction(-1 - m, 2)
    w1 = s / k; w2 = (s * s - s - k) / (k * (k - 2))
    return w1, w2, 1 - (w1 - w2) ** 2 / (1 - w2)


def analyze(name, n, adj, k, npairs=40, seed=1):
    assert check_srg(n, adj, k, 1, 2), name
    A = np.zeros((n, n))
    for i in range(n):
        for j in adj[i]:
            A[i, j] = 1
    ev, U = np.linalg.eigh(A)
    sel = np.abs(ev - ev.min()) < 1e-6
    g = int(sel.sum())
    W = U[:, sel] * np.sqrt(n / g)          # Gram = (n/g) E_s : diagonale 1
    w1, w2, val = predicted(k)
    rng = np.random.default_rng(seed)
    nonedges = [(a, b) for a in range(n) for b in range(a + 1, n) if b not in adj[a]]
    pairs = [nonedges[i] for i in rng.choice(len(nonedges), size=min(npairs, len(nonedges)), replace=False)]
    out = dict(rank_ok=0, refl=set(), hits=0, agree=0, mind=10**9, extends=0)
    for (u, v) in pairs:
        X = [x for x in range(n) if x in adj[u] and x not in adj[v]]
        Y = [y for y in range(n) if y in adj[v] and y not in adj[u]]
        Ag = [a for a in range(n) if a not in (u, v) and ((a in adj[u]) == (a in adj[v]))]
        if np.linalg.matrix_rank(W[Ag + [u, v]], tol=1e-8) == g:
            out['rank_ok'] += 1
        # bord positif glouton contenant u, v
        basis = [u, v]; Q = np.linalg.qr(W[[u, v]].T)[0]
        for a in Ag:
            r = W[a] - Q @ (Q.T @ W[a])
            if np.linalg.norm(r) > 1e-7:
                basis.append(a); Q = np.column_stack([Q, r / np.linalg.norm(r)])
            if len(basis) == g:
                break
        Sp = basis[2:]
        z = W[u] - W[v]
        refl = lambda w: w - 2 * (w @ z) / (z @ z) * z
        for x in X:
            out['refl'].add(round(float(W[x] @ refl(W[x])), 9))
            if np.min(np.linalg.norm(W - refl(W[x]), axis=1)) < 1e-7:
                out['hits'] += 1
        # la réflexion préserve-t-elle toute la configuration ?
        RW = np.array([refl(W[t]) for t in range(n)])
        img = [int(np.argmin(np.linalg.norm(W - RW[t], axis=1))) for t in range(n)]
        if all(np.linalg.norm(W[img[t]] - RW[t]) < 1e-7 for t in range(n)):
            out['extends'] += 1
        pat = {t: tuple(int(a in adj[t]) for a in Sp) for t in X + Y}
        for x in X:
            for y in Y:
                d = sum(p != q for p, q in zip(pat[x], pat[y]))
                out['agree'] += (d == 0); out['mind'] = min(out['mind'], d)
    print(f"{name:34s} v={n:3d} g={g:3d} | paires {len(pairs)} : engendrent E_s {out['rank_ok']}/{len(pairs)} | "
          f"<w_x,R w_x> observé {sorted(out['refl'])} prédit {float(val):.9f} = {val} "
          f"(permis : 1, {w1}, {w2}) | R(w_x) sommet : {out['hits']} | R préserve tout : {out['extends']} | "
          f"couples (x,y) même motif sur S' : {out['agree']}, distance min {out['mind']}")


n, adj = rook3()
analyze('srg(9,4,1,2) grille 3x3', n, adj, 4)
for f in FILES:
    n, edges, adj = load_edges(R + f)
    analyze(f.split('/')[-1], n, adj, 22, npairs=20)
w1, w2, val = predicted(14)
print(f"srg(99,14,1,2) : prédit <w_x,R w_x> = {val} ; permis 1, {w1}, {w2} ; en Gram 27I-9A+J : {val*28} contre 28, -8, 1")
