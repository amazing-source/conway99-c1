"""Gram view of the column stage (notes/163): B_C (far x 3m, rows = 2+2+2 incidence) must satisfy
B_C^T B_C = G_C, a matrix fixed by C.  Necessary: G_C PSD of rank 3m-2; every far row r has leverage r^T G^+ r <= 1."""
import sys, os, random, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from colmodel import load_edges, triangle_structure, predicted
from coldrive import random_C


def gram(C):
    m = C["m"]; N01, N02, N12 = map(np.array, predicted(C))
    def diag(mt):
        P = np.zeros((m, m)); P[np.arange(m), mt] = 1
        return (m - 3) * np.eye(m) + np.ones((m, m)) - P
    G = np.block([[diag(C["M"]), N01, N02], [N01.T, diag(C["ta"]), N12], [N02.T, N12.T, diag(C["tb"])]])
    return G.astype(float)


def row_vec(m, p0, p1, p2):
    r = np.zeros(3 * m)
    for u in p0: r[u] = 1
    for u in p1: r[m + u] = 1
    for u in p2: r[2 * m + u] = 1
    return r


def analyse(C, true_triples=None):
    m = C["m"]; G = gram(C); ev = np.linalg.eigvalsh(G)
    psd = ev.min() > -1e-9; rank = int((ev > 1e-9).sum())
    out = dict(min_eig=round(float(ev.min()), 6), rank=rank, psd=bool(psd))
    if psd:
        Gp = np.linalg.pinv(G, rcond=1e-10)
        edges = [[(x, y) for x in range(m) for y in range(x + 1, m) if mt[x] != y] for mt in (C["M"], C["ta"], C["tb"])]
        N01, N02, N12 = predicted(C)
        tot = ok = 0
        for p0 in edges[0]:
            for p1 in edges[1]:
                if min(N01[x][z] for x in p0 for z in p1) <= 0: continue
                for p2 in edges[2]:
                    if min(N02[x][y] for x in p0 for y in p2) <= 0 or min(N12[z][y] for z in p1 for y in p2) <= 0:
                        continue
                    tot += 1; r = row_vec(m, p0, p1, p2)
                    if r @ Gp @ r <= 1 + 1e-9: ok += 1
        out.update(options=tot, leverage_ok=ok)
        if true_triples:
            lev = [row_vec(m, *t) @ Gp @ row_vec(m, *t) for t in true_triples]
            out.update(true_max_leverage=round(max(lev), 6), true_sum=round(sum(lev), 6))
    return out


if __name__ == "__main__":
    if sys.argv[1] == "real":
        adj = load_edges(sys.argv[2], 243)
        for v, a in ((0, sorted(adj[0])[0]), (50, sorted(adj[50])[3])):
            a2 = [u for u in adj[v] if u in adj[a]][0]
            C = triangle_structure(adj, v, a, a2); G = gram(C); ev = np.linalg.eigvalsh(G)
            Gp = np.linalg.pinv(G, rcond=1e-10)
            lev = [row_vec(20, *t) @ Gp @ row_vec(20, *t) for t in C["triples"]]
            B = np.array([row_vec(20, *t) for t in C["triples"]])
            print(f"{sys.argv[2]} triangle ({v},{a},{a2}): B^T B == G_C: {np.allclose(B.T @ B, G)}; min eig {ev.min():.2e};"
                  f" rank {(ev > 1e-9).sum()}; true leverages max {max(lev):.4f} sum {sum(lev):.4f}")
    else:
        rng = random.Random(int(sys.argv[2])); cnt = int(sys.argv[3])
        for i in range(cnt):
            C, _ = random_C(12, rng)
            print(f"random C #{i}:", analyse(C), flush=True)
