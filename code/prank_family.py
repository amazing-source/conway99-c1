# notes/110 sec. 6.
# p-ranks of A - rI for existing SRGs of the (0,2) and (1,2) families, vs the van Eijl bound min(f,g)+1,
# at primes p | (r - s).  Question: are existing (twisted or not) graphs "p-special" (rank below the bound)?
import sys, numpy as np, sympy as sp
sys.path.insert(0, '.')
import graphs

def rank_mod(M, p):
    M = np.array(M, dtype=np.int64) % p
    r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0: continue
        i = r + nz[0]; M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        col = M[:, c].copy(); col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size: M[nzr] = (M[nzr] - np.outer(col[nzr], M[r])) % p
        r += 1
        if r == rows: break
    return r

for name, A in [('clebsch (16,5,0,2)', graphs.clebsch()), ('gewirtz (56,10,0,2)', graphs.gewirtz()),
                ('srg9 (9,4,1,2)', graphs.srg9()), ('bvls (243,22,1,2)', graphs.bvls())]:
    A = np.array(A); n = len(A); k = int(A[0].sum())
    ev = np.round(np.linalg.eigvalsh(A)).astype(int)
    vals, cnt = np.unique(ev, return_counts=True)
    d = dict(zip(vals.tolist(), cnt.tolist())); d.pop(k)
    (s, g), (r, f) = sorted(d.items())
    out = []
    for p in sp.primefactors(r - s):
        out.append(f'p={p}: rank(A-{r}I)={rank_mod(A - r*np.eye(n, dtype=np.int64), p)}')
    print(f'{name}: r={r} (f={f}), s={s} (g={g}), bound min(f,g)+1={min(f,g)+1}; ' + '; '.join(out))
