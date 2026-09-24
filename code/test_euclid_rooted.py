"""Validate rooted and harmonic Gram coefficients against direct computation (srg(9), Petersen)."""
import itertools, math, time
import numpy as np
import networkx as nx
import graphs
from subgraph_lp import Types, brute_counts
from euclid_gram import (make_bases, make_rooted_recipes, make_recipes_general, embeddings,
                         coefficients_general, gram_from_counts)

def sym_tensor(vecs):
    D = len(vecs); sym = 0
    for p in itertools.permutations(range(D)):
        t = vecs[p[0]]
        for j in range(1, D):
            t = np.multiply.outer(t, vecs[p[j]])
        sym = sym + t
    return sym / math.factorial(D)

def harmonic(t):
    """Traceless projection of a symmetric tensor of degree 2 or 3 (numerically)."""
    d = t.ndim; n = t.shape[0]; I = np.eye(n)
    if d == 1:
        return t
    if d == 2:
        return t - np.trace(t) / n * I
    if d == 3:
        v = np.einsum('iik->k', t)
        g_v = (np.einsum('ij,k->ijk', I, v) + np.einsum('ik,j->ijk', I, v) + np.einsum('jk,i->ijk', I, v)) / 3
        return t - 3.0 / (n + 2) * g_v
    raise NotImplementedError

def eig_vectors(A, s, scale):
    A = np.asarray(A, dtype=float)
    ev, U = np.linalg.eigh(A)
    sel = np.abs(ev - s) < 1e-8
    return U[:, sel] * math.sqrt(scale)

def run(name, A, n, k, lam, mu, r, s, d, rooted, harm):
    t0 = time.time()
    c = (k - r) / n
    E0, E1, E2 = (r + c) / (r - s), (-1 + c) / (r - s), c / (r - s)
    scale = 1 / E2
    kernel = (E0 * scale, E1 * scale, E2 * scale)
    P = eig_vectors(A, s, scale); dim = P.shape[1]
    T = Types(lam, mu, k, 8)
    bases = make_bases(T, 4)
    rec = make_rooted_recipes(bases, d) if rooted else make_recipes_general(bases, d)
    coef = coefficients_general(T.reps, bases, rec, kernel, 7 if rooted else 8, rooted=rooted,
                                harmonic_dim=dim if harm else None)
    z = brute_counts(np.asarray(A).tolist(), 8, T)
    Gc = gram_from_counts(coef, len(rec), z)
    Gg = nx.from_numpy_array(np.asarray(A, dtype=float))
    N = len(A)
    Gd = np.zeros((len(rec), len(rec)))
    if rooted:
        for x in range(N):
            W = []
            for bi, rho, slots in rec:
                w = np.zeros((dim,) * d)
                for e in embeddings(Gg, bases[bi]):
                    if e[rho] != x:
                        continue
                    t = sym_tensor([P[e[j]] for j in slots])
                    w = w + (harmonic(t) if harm else t)
                W.append(np.ravel(w))
            W = np.array(W); Gd += W @ W.T
    else:
        W = []
        for bi, slots in rec:
            w = np.zeros((dim,) * d)
            for e in embeddings(Gg, bases[bi]):
                t = sym_tensor([P[e[j]] for j in slots])
                w = w + (harmonic(t) if harm else t)
            W.append(np.ravel(w))
        W = np.array(W); Gd = W @ W.T
    err = np.abs(Gc - Gd).max() / max(1, np.abs(Gd).max())
    print(f'{name} d={d} rooted={rooted} harmonic={harm}: {len(rec)} recipes, rel. error {err:.2e} ({time.time()-t0:.0f}s)', flush=True)

Pet = nx.to_numpy_array(nx.petersen_graph(), dtype=int)
run('Petersen', Pet, 10, 3, 0, 1, 1, -2, 3, True, False)
run('Petersen', Pet, 10, 3, 0, 1, 1, -2, 3, False, True)
run('Petersen', Pet, 10, 3, 0, 1, 1, -2, 2, True, True)
run('srg(9)', graphs.srg9(), 9, 4, 1, 2, 1, -2, 3, True, True)
