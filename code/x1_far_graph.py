r"""X1 -- far graph of a line in a srg(v,k,1,2), and its far eigenlattices (IDEES.md, X1).  Heavy algebra in C.

Setting.  L = {p0,p1,p2} a line, X_i = N(p_i) \ L (|X_i| = k-2), N(L) = X_0 u X_1 u X_2, F = far set (distance 2 from
all of L).  G = G(L) = graph induced on N(L) (cubic), M = A[N(L), F], A_F = A[F, F].

Hand derivation (to be OBSERVED here):
  (a) every far vertex has exactly 2 neighbours in each X_i;
  (b) A_F M^T = M^T (J/3 - A_G - I) and (A_F - r)(A_F - s) = 0 on ker M, hence
      spec(A_F) = {k-6} u {-alpha-1 : alpha in spec(A_G) minus {3,0,0}} u {r^a, s^b};
  (c) Y = Z^F cap ker M, C = Y^perp (saturation of the row lattice of M): D(Y) ~ -D(C), D(C)_q ~ coker(M M^T)_tors,q
      when q does not divide [C : R_M]; Y = K_s (+) K_r glued only at q | r - s; A_F acts on D(C) through -A_G - I, so
      for q not dividing r - s and not dividing the U-part numbers:
          D(K_s)_q ~ coker(A_G - r)_q (on U^perp),      D(K_r)_q ~ coker(A_G - s)_q (on U^perp).
      For 99, r = 3 = degree of G, so D(K_{-4}(L))_q is the q-part of the critical group of G(L).
Negative control: the swapped comparison must fail whenever the two sides differ.
All local computations: padic.exe (Smith forms and saturated kernels over Z_q, truncated mod q^E, q^E ~ 2^50).
"""
import sys, os, time
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'c1_recherche', 'code'))
import graphs
import padic_py as pp


def find_line(A):
    n = len(A)
    for u in range(n):
        for v in np.nonzero(A[u])[0]:
            if v > u:
                w = np.nonzero(A[u] & A[v])[0]
                if len(w) == 1:
                    return [u, int(v), int(w[0])]
    raise ValueError


def components(Ad):
    n = len(Ad); seen = [False] * n; c = 0
    for s0 in range(n):
        if seen[s0]:
            continue
        c += 1; st = [s0]; seen[s0] = True
        while st:
            u = st.pop()
            for v in np.nonzero(Ad[u])[0]:
                if not seen[v]:
                    seen[v] = True; st.append(v)
    return c


def analyse(A, r, s, label, primes=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)):
    n = len(A); k = int(A[0].sum())
    L = find_line(A)
    X = [[int(u) for u in np.nonzero(A[p])[0] if u not in L] for p in L]
    N = X[0] + X[1] + X[2]
    F = [u for u in range(n) if u not in L and u not in N]
    AF = A[np.ix_(F, F)]; M = A[np.ix_(N, F)]; AG = A[np.ix_(N, N)]
    cnt = Counter(tuple(int(A[w, X[i]].sum()) for i in range(3)) for w in F)
    print(f'[{label}] v={n} k={k} r={r} s={s} |N(L)|={len(N)} |F|={len(F)}  G(L): {components(AG)} components')
    print(f'  (a) neighbours of far vertices in (X0,X1,X2): {dict(cnt)}')
    assert set(AG.sum(1).tolist()) == {3}
    ev_G = list(np.sort(np.linalg.eigvalsh(AG.astype(float))))
    rest = ev_G[:]
    for x in (3.0, 0.0, 0.0):
        rest.pop(int(np.argmin([abs(y - x) for y in rest])))
    rkM = int(np.linalg.matrix_rank(M.astype(float))); kerdim = len(F) - rkM
    tr_rest = (k - 6) + sum(-y - 1 for y in rest)
    a = (-tr_rest - s * kerdim) / (r - s); b = kerdim - a
    pred = np.sort(np.array([k - 6] + [-y - 1 for y in rest] + [r] * int(round(a)) + [s] * int(round(b)), dtype=float))
    ev_F = np.sort(np.linalg.eigvalsh(AF.astype(float)))
    err = float(np.max(np.abs(pred - ev_F))) if len(pred) == len(ev_F) else float('inf')
    print(f'  (b) rank M = {rkM}; mult r on ker M = {a:.3f}, s = {b:.3f}; max |spec(A_F) - prediction| = {err:.2e}')
    I_F = np.eye(len(F), dtype=np.int64); I_N = np.eye(len(N), dtype=np.int64)
    Ms = np.vstack([M, AF - s * I_F]); Mr = np.vstack([M, AF - r * I_F])
    dimKs = len(F) - int(np.linalg.matrix_rank(Ms.astype(float)))
    dimKr = len(F) - int(np.linalg.matrix_rank(Mr.astype(float)))
    MMt = M @ M.T
    unit_nums = [3 - r, r, 3 - s, s, 2 * k - 8, 6 * k - 24, r - s]
    t0 = time.time(); ok = True; neg_inf = neg_fail = 0
    print(f'  (c) far lattices: dim K_s = {dimKs}, dim K_r = {dimKr}, dim Y = {kerdim}')
    for q in primes:
        Y, E = pp.kernel(M, q)
        C, _ = pp.kernel(np.array(Y, dtype=object), q) if Y else ([], E)
        Ks, _ = pp.kernel(Ms, q); Kr, _ = pp.kernel(Mr, q)
        assert len(Y) == kerdim and len(Ks) == dimKs and len(Kr) == dimKr, (q, len(Y), len(Ks), len(Kr))
        dY = pp.summary(pp.gram_vals(Y, q)[0], E); dC = pp.summary(pp.gram_vals(C, q)[0], E)
        dKs = pp.summary(pp.gram_vals(Ks, q)[0], E); dKr = pp.summary(pp.gram_vals(Kr, q)[0], E)
        cM = pp.summary(pp.smith_vals(MMt, q)[0], E)
        cr = pp.summary(pp.smith_vals(AG - r * I_N, q)[0], E); cs = pp.summary(pp.smith_vals(AG - s * I_N, q)[0], E)
        cM.pop('inf', None)   # the kernel of M M^T (rank defect) is not torsion
        if not any((dY, dC, dKs, dKr, cM, cr, cs)):
            continue
        clean = all(x % q for x in unit_nums)
        merged = Counter(dKs) + Counter(dKr)
        line = (f'   q={q:2d}: D(Y)={dY} D(C)={dC} tors coker(MM^T)={cM} | D(K_s)={dKs} D(K_r)={dKr} '
                f'| coker(A_G-r)={cr} coker(A_G-s)={cs}')
        checks = [f'D(Y)=D(C):{dY == dC}']
        if (r - s) % q:
            checks.append(f'D(Y)=D(K_s)+D(K_r):{dict(merged) == dY}')
        if clean:
            m = (dKs == cr) and (dKr == cs)
            checks.append(f'prediction:{"MATCH" if m else "differs"}')
            ok &= m
            if cr != cs:
                neg_inf += 1; neg_fail += not ((dKs == cs) and (dKr == cr))
        else:
            checks.append('prediction: q divides a U-part number, not tested')
        print(line + '\n          ' + '  '.join(checks))
    print(f'  prediction at clean primes: {"all match" if ok else "FAILED"}; negative control: '
          f'{neg_fail}/{neg_inf} informative primes reject the swap   [{time.time() - t0:.1f}s]')
    return ok


if __name__ == '__main__':
    A = graphs.bvls()
    analyse(A, 4, -5, 'BvLS srg(243,22,1,2)')
