"""Check, on BvLS = srg(243,22,1,2), the mechanism of lemma L17 (notes/80): the local lattice
K = {v in Z^X : label sums zero} (X = Gamma_2(x)) splits p-adically, for every prime p not dividing r - s, into the two
H-eigenlattices K_r (H = r) and K_s (H = s), and the p-part of disc(K) goes entirely to the eigenlattice on which H acts
non-invertibly mod p, because H acts on disc(K) = disc(K^perp) through the label operator Phi = J - I - M, whose
eigenvalues are k - mu (const), -2 (class-symmetric), 0 (antisymmetric).
For 99 (r = 3, s = -4, glue prime 7) this gives: K_3 even, 2-adically unimodular, det 3^8 5^6 7^k; K_-4 det 2^21 7^k.
For BvLS (r = 4, s = -5, glue prime 3) the same argument predicts, at p = 5: disc(K)_5 = (Z/5)^12 lies in K_-5
(H = -5 = 0 mod 5), i.e. the Gram of K_4 mod 5 has full rank 110 and that of K_-5 has rank 88 - 12 = 76;
at p = 2: disc(K_-5)_2 = 0 (H = -5 invertible), i.e. the Gram of K_-5 mod 2 has full rank 88.
Everything below is modular linear algebra on 220 x 220 matrices (instantaneous).
"""
import numpy as np
import graphs


def nullspace_mod(M, p):
    """Basis (rows) of the right null space of M over F_p."""
    M = np.array(M, dtype=np.int64) % p
    rows, cols = M.shape
    A = M.copy()
    piv_cols = []
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i, c] % p:
                piv = i
                break
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        for i in range(rows):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        piv_cols.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv_cols]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv_cols):
            v[c] = (-A[i, f]) % p
        basis.append(v)
    return np.array(basis, dtype=np.int64).reshape(len(basis), cols)


def rank_mod(M, p):
    M = np.array(M, dtype=np.int64) % p
    if M.size == 0:
        return 0
    return M.shape[1] - len(nullspace_mod(M, p))


def main():
    A = graphs.bvls()
    n = len(A)
    x = 0
    Nx = [v for v in range(n) if A[x, v]]
    mate = {a: next(b for b in Nx if b != a and A[a, b]) for a in Nx}
    X = [v for v in range(n) if v != x and not A[x, v]]
    lab = {a: i for i, a in enumerate(Nx)}
    B = np.zeros((len(X), len(Nx)), dtype=np.int64)
    for i, z in enumerate(X):
        for a in Nx:
            if A[z, a]:
                B[i, lab[a]] = 1
    assert (B.sum(1) == 2).all()
    H = A[np.ix_(X, X)].astype(np.int64)
    print(f'BvLS vertex {x}: |N(x)| = {len(Nx)}, |X| = {len(X)}, H regular of degree {set(H.sum(1))}')
    for p, pred in ((5, 'K_4 full rank 110, K_-5 rank 76'), (2, 'K_-5 full rank 88'), (7, 'both full'), (11, 'both full')):
        Kb = nullspace_mod(B.T, p)                      # basis of K / pK (rows)
        # restrict H to K: H Kb^T expressed in K coordinates is not needed; eigen-subspaces inside K:
        out = []
        for ev in (4, -5):
            # vectors v in span(Kb) with (H - ev) v = 0 mod p:  solve c : (H - ev) Kb^T c = 0
            Mv = ((H - ev * np.eye(len(X), dtype=np.int64)) @ Kb.T) % p
            C = nullspace_mod(Mv, p)
            V = (C @ Kb) % p                               # basis of the eigen-subspace (rows)
            G = (V @ V.T) % p                              # standard Gram restricted
            out.append(f'H={ev:+d}: dim {len(V)}, Gram rank {rank_mod(G, p)}')
        print(f'  p={p:2d}: dim K/pK = {len(Kb)} | ' + ' | '.join(out) + f'   (prediction: {pred})')


if __name__ == '__main__':
    main()
