"""Check euclid_gram against a direct computation with actual eigenspace vectors (small SRGs)."""
import itertools, math, time
import numpy as np
import networkx as nx
import graphs
from subgraph_lp import Types, brute_counts
from euclid_gram import make_bases, make_recipes, make_recipes_general, embeddings, coefficients, gram_from_counts

def direct_gram(A, kernel_scale, s, bases, recipes, D):
    A = np.asarray(A, dtype=float); n = len(A)
    ev, U = np.linalg.eigh(A)
    sel = np.abs(ev - s) < 1e-8
    P = U[:, sel] * math.sqrt(kernel_scale)          # rows p_v, Gram = kernel_scale * E_s
    Gg = nx.from_numpy_array(A)
    W = []
    for bi, slots in recipes:
        w = np.zeros((P.shape[1],) * D)
        for e in embeddings(Gg, bases[bi]):
            vecs = [P[e[j]] for j in slots]
            sym = 0
            for p in itertools.permutations(range(D)):
                t = vecs[p[0]]
                for j in range(1, D):
                    t = np.multiply.outer(t, vecs[p[j]])
                sym = sym + t
            w = w + sym / math.factorial(D)
        W.append(np.ravel(w))
    W = np.array(W)
    return W @ W.T

def run(name, A, n, k, lam, mu, r, s, D=4):
    t0 = time.time()
    kernel_scale = None
    # kernel values from E_s = (rI - A + ((k-r)/n) J)/(r - s), scaled to make the diagonal an integer-ish
    c = (k - r) / n
    E0, E1, E2 = (r + c) / (r - s), (-1 + c) / (r - s), c / (r - s)
    scale = 1 / E2                                   # non-adjacent value 1
    kernel = (E0 * scale, E1 * scale, E2 * scale)
    T = Types(lam, mu, k, 2 * D)
    bases = make_bases(T, D)
    rec = make_recipes(bases, D)
    coef = coefficients(T.reps, bases, rec, kernel, D)
    z = brute_counts(np.asarray(A).tolist(), 2 * D, T)
    Gc = gram_from_counts(coef, len(rec), z)
    Gd = direct_gram(A, scale, s, bases, rec, D)
    err = np.abs(Gc - Gd).max() / max(1, np.abs(Gd).max())
    print(f'{name}: kernel {tuple(round(x, 4) for x in kernel)}, {len(rec)} recipes, relative error {err:.2e}, '
          f'min eig {np.linalg.eigvalsh(Gd).min():.3e} ({time.time()-t0:.0f}s)', flush=True)

pass
pass

def run_general(name, A, n, k, lam, mu, r, s, d):
    t0 = time.time()
    c = (k - r) / n
    E0, E1, E2 = (r + c) / (r - s), (-1 + c) / (r - s), c / (r - s)
    scale = 1 / E2
    kernel = (E0 * scale, E1 * scale, E2 * scale)
    T = Types(lam, mu, k, 8)
    bases = make_bases(T, 4)
    rec = make_recipes_general(bases, d)
    coef = coefficients(T.reps, bases, rec, kernel, 4)
    z = brute_counts(np.asarray(A).tolist(), 8, T)
    Gc = gram_from_counts(coef, len(rec), z)
    Gd = direct_gram(A, scale, s, bases, rec, d)
    err = np.abs(Gc - Gd).max() / max(1, np.abs(Gd).max())
    print(f'{name} degree {d} with witnesses: {len(rec)} recipes, relative error {err:.2e} ({time.time()-t0:.0f}s)', flush=True)

if __name__ == '__main__':
    run_general('srg(9,4,1,2)', graphs.srg9(), 9, 4, 1, 2, 1, -2, 3)
    run_general('Petersen', nx.to_numpy_array(nx.petersen_graph(), dtype=int), 10, 3, 0, 1, 1, -2, 3)
    run_general('Petersen', nx.to_numpy_array(nx.petersen_graph(), dtype=int), 10, 3, 0, 1, 1, -2, 2)
