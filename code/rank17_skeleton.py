r"""Rank-17 pilot (C1, 27/09 night): the class skeleton test in K (necessary condition, handoff Prop. 5.1).
rho: E7 -> K/2K is linear and injective, rho(e_c + e_d) = [w_cd], and preserves the forms. So with g_d = [w_1d] (d = 2..7):
  [w_cd] = g_c + g_d (2 <= c < d), the g's are independent, (g_c, g_d) is odd for c != d, and every one of the 21 classes
  g_d, g_c + g_d contains two norm-10 vectors w, w' (w' != +-w) with (w, w') in {0, +-4} (w+- of that cell: (w+, w-) = 4t).
A class with such a pair is called usable. If no skeleton (g_2..g_7) exists, the (V, y-pair) cannot carry the frame.
Also recorded: every pairwise inner product of two frame w's has |.| <= 5 (from (w_u,w_v) = 4(u,v) - r_u.r_v).
Usage: python rank17_skeleton.py <K_tag> [first_k_pairs]"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rank17_ypairs import short_vectors_chunked

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rank17')
USE_DUALS = os.environ.get('SKELETON_DUALS', '1') == '1'
USE_M1 = os.environ.get('SKELETON_M1', '1') == '1'


def root_keys_mod4(Gv):
    """V/4V classes of the roots (norm-2 vectors) of V, as packed int64 keys (2 bits per V-coordinate)"""
    X, nrm = short_vectors_chunked(Gv.tolist(), 2)
    R = X[nrm == 2].astype(np.int64)
    R = np.vstack([R, -R])
    return np.unique(((R % 4) << (2 * np.arange(R.shape[1]))).sum(axis=1))


def usable_classes(GK, Kv=None, rootkeys=None, W10=None, with_masks=True):
    """norm-10 vectors of K by class in K/2K; with Kv (K basis in V coordinates) and rootkeys, Lemma L1 (structures,
    27/09 night) removes every w with w = r mod 4V for a root r of V (u + (r - w)/2 = (r + r_u)/2 would be a norm-1 vector
    of U). A class is usable when it keeps two vectors w, w' (w' != +-w) with (w, w') in {0, +-4}."""
    if W10 is None:
        X, nrm = short_vectors_chunked(GK.tolist(), 10)
        W = X[nrm == 10].astype(np.int32)                   # norm-10 vectors up to sign, K coordinates
        del X, nrm
    else:
        W = W10.astype(np.int32)
    n_all = len(W)
    if Kv is not None:
        keep = np.ones(len(W), dtype=bool)
        sh = 2 * np.arange(Kv.shape[1])
        for s0 in range(0, len(W), 100000):                  # chunks (memory)
            k = (((W[s0:s0 + 100000].astype(np.int64) @ Kv) % 4) << sh).sum(axis=1)
            keep[s0:s0 + 100000] = ~np.isin(k, rootkeys)
        W = W[keep]
    cls = np.zeros(len(W), dtype=np.int64)
    for i in range(15):
        cls |= ((W[:, i] & 1).astype(np.int64) << i)       # class mod 2K as a 15-bit integer
    order = np.argsort(cls, kind='stable')
    W, cls = W[order], cls[order]
    bounds = np.flatnonzero(np.diff(cls)) + 1
    starts = np.concatenate([[0], bounds]); ends = np.concatenate([bounds, [len(cls)]])
    WG = W @ GK.astype(np.int32)
    usable, masks = {}, {}
    G2 = (GK % 2).astype(np.int64)
    pw = (1 << np.arange(15)).astype(np.int64)
    for s, e in zip(starts, ends):
        if e - s < 2:
            continue
        found = set()
        for b0 in range(s, e, 512):                          # blocks: some classes hold thousands of vectors
            ip = WG[b0:min(e, b0 + 512)] @ W[s:e].T          # inner products inside the class (up to sign)
            rows = np.arange(ip.shape[0])
            ip[rows, rows + (b0 - s)] = 99                   # the vector with itself
            if not with_masks:                               # usable <=> one pair exists (no M1 masks needed)
                if np.isin(np.abs(ip), (0, 4)).any():
                    found.add(-1)
                    break
                continue
            hi, hj = np.nonzero(np.isin(np.abs(ip), (0, 4)))
            del ip
            for h0 in range(0, len(hi), 50000):              # chunks: a block can hold ~10^6 usable pairs
                A = W[b0 + hi[h0:h0 + 50000]].astype(np.int64); Bv = W[s + hj[h0:h0 + 50000]].astype(np.int64)
                for S_ in ((A + Bv) // 2, (A - Bv) // 2):    # s = (w +- w')/2 = a or b of the cell (M1 masks)
                    m = ((S_ @ G2) % 2) @ pw
                    found.update(np.unique(m).tolist())
        if found:
            usable[int(cls[s])] = e - s
            if with_masks:
                masks[int(cls[s])] = np.array(sorted(found), dtype=np.int64)
    return usable, (n_all, len(W), len(starts)), masks


def short_duals(GK):
    """kappa in K* with |kappa|^2 <= 5/7, in dual-basis coordinates (pairing with K coordinates = dot product), with the
    parity-energy bound on k(p(kappa)): (PE) 7|kappa|^2 >= k(7-k)/2, i.e. k = 0 if |k|^2 <= 2/7, k <= 1 if <= 4/7,
    k <= 2 if = 5/7. |kappa|^2 is in (1/7)Z (K*/K = (Z/7)^2, anisotropic). Up to sign."""
    from fractions import Fraction as Fr
    from envelope_trap import inverse_exact
    Gi = inverse_exact([[int(x) for x in row] for row in GK])
    D = np.array([[int(x * 49) for x in row] for row in Gi], dtype=np.int64)
    assert all((x * 49).denominator == 1 for row in Gi for x in row)
    X, nrm = short_vectors_chunked(D.tolist(), 35)
    out = []
    for x, n in zip(X, nrm):
        n = int(n)
        if n == 0:
            continue
        assert n % 7 == 0, 'dual norm not in (1/7)Z'
        kmax = 0 if n <= 14 else (1 if n <= 28 else 2)
        out.append((np.array(x, dtype=np.int64), kmax, n // 7))
    return out


def root_orbits(GK, classes):
    """orbits of H = <reflections in the roots of K> on the given classes of K/2K (H fixes y1, y2, so every filter and the
    vector level are H-equivariant). Action mod 2K: sigma -> sigma + (sigma, r)[r]. Returns {class: orbit min}."""
    X, nrm = short_vectors_chunked(GK.tolist(), 2)
    R = X[nrm == 2].astype(np.int64)
    G2 = (GK % 2).astype(np.int64)
    rc = [int(((r & 1) << np.arange(15)).sum()) for r in R]
    rf = [int((((r & 1) @ G2) % 2 << np.arange(15)).sum()) for r in R]          # functional sigma -> (sigma, r) mod 2
    cls = set(int(c) for c in classes)
    orb = {}
    for c in sorted(cls):
        if c in orb:
            continue
        comp, fr = {c}, [c]
        while fr:
            nf = []
            for x in fr:
                for a, f in zip(rc, rf):
                    y = x ^ a if bin(x & f).count('1') & 1 else x
                    if y not in comp:
                        comp.add(y); nf.append(y)
            fr = nf
        mn = min(comp)
        for x in comp:
            orb[x] = mn
    return orb


def skeleton_exists(usable, GK, limit=10 ** 8, duals=(), units=(), masks=None, on_leaf=None, orbits=None,
                    perm_seed=None):
    """search g_2..g_7 (classes as 15-bit ints): pairwise odd forms, independent, all 21 classes usable, with the
    short-dual (parity energy) rules and the unit rule; M1 (oriented cell usability) is checked on each full skeleton,
    and the search goes on when it fails. v5 (28/09 night): candidate sets are Python-int bitsets.
    Rules (o / z = numbers of chosen g with odd / even pairing with kappa): kmax 0: o = 0; kmax 1: o <= 1 or z = 0;
    kmax 2: o <= 2 or z <= 1 (i.e. min(o, z + 1) <= kmax at depth 6); unit rule at depth 6: o >= 1.
    Returns (skeleton or None, nodes, leaves_rejected_by_M1)."""
    if orbits is not None:                                            # order by (orbit min, class): H-reduction
        U = np.array(sorted(usable, key=lambda x: (orbits[x], x)), dtype=np.int64)
    else:
        U = np.array(sorted(usable), dtype=np.int64)
    if len(duals):
        k0 = [x for x, km, _ in duals if km == 0]
        if k0:
            bits = ((U[:, None] >> np.arange(15)) & 1)
            keep = np.ones(len(U), bool)
            for x in k0:
                keep &= (bits @ x) % 2 == 0
            U = U[keep]
        duals = [(x, km) for x, km, _ in duals if km > 0]
    if perm_seed is not None:                                         # random candidate order (sampling mode)
        U = U[np.random.RandomState(perm_seed).permutation(len(U))]
        orbits = None
    n = len(U)
    if n < 6:
        return None, 0, 0
    umask = np.zeros(1 << 15, dtype=bool)
    umask[U] = True
    bits = ((U[:, None] >> np.arange(15)) & 1).astype(np.int64)
    Gm2 = (GK % 2).astype(np.int64)
    Fm = (((bits @ Gm2) % 2) << np.arange(15)).sum(axis=1).astype(np.int16)   # functional masks of the classes
    P = (np.bitwise_count(Fm[:, None] & U.astype(np.int16)[None, :]) & 1).astype(bool)   # P[i, j]: (U_i, U_j) odd
    # neighbour bitsets: j > i, odd pairing, U_i ^ U_j usable
    nbr = []
    for i in range(n):
        ok = P[i].copy()
        ok[:i + 1] = False
        ok &= umask[U ^ U[i]]
        nbr.append(int.from_bytes(np.packbits(ok, bitorder='little').tobytes(), 'little'))   # bit j = ok[j]
    FK = [tuple(int(((bits[i] @ x) % 2)) for x, _ in duals) for i in range(n)]
    KM = [km for _, km in duals]
    FU = [tuple(int(((bits[i] @ d) % 2)) for d in units) for i in range(n)]
    nd, nu = len(KM), len(units)
    nodes = [0]
    rejected = [0]
    Ul = U.tolist()

    def m1_full(G):
        if masks is None:
            return True
        Ga = np.array(G, dtype=np.int64)
        for i in range(6):
            M = masks[G[i]]
            Par = np.bitwise_count(M[:, None] & Ga[None, :]) & 1
            onlyi = (Par[:, i] == 1) & (Par.sum(axis=1) == 1)
            if not (Par.all(axis=1) | onlyi).any():
                return False
            for i2 in range(i + 1, 6):
                M = masks[G[i] ^ G[i2]]
                Par = np.bitwise_count(M[:, None] & Ga[None, :]) & 1
                one = Par.sum(axis=1) == 1
                if not (one & ((Par[:, i] == 1) | (Par[:, i2] == 1))).any():
                    return False
        return True

    def rec(chosen, span, cand, o, ou):
        nodes[0] += 1
        if nodes[0] > limit:
            raise TimeoutError
        depth = len(chosen)
        need = 5 - depth                                              # further elements needed after this one
        c = cand
        while c:
            low = c & -c
            i = low.bit_length() - 1
            c ^= low
            x = Ul[i]
            if x in span:
                continue
            if depth == 0 and orbits is not None and orbits[x] != x:
                continue                                                  # the smallest element must be an orbit min
            if nd:
                fk = FK[i]
                o2 = tuple(a + b for a, b in zip(o, fk))
                z2 = depth + 1
                bad = False
                for t in range(nd):
                    oo = o2[t]; zz = z2 - oo
                    if KM[t] == 1:
                        if oo > 1 and zz > 0:
                            bad = True; break
                    else:
                        if oo > 2 and zz > 1:
                            bad = True; break
                if bad:
                    continue
            else:
                o2 = o
            ou2 = tuple(a + b for a, b in zip(ou, FU[i])) if nu else ou
            if depth + 1 == 6:
                if nu and min(ou2) < 1:
                    continue
                G = [Ul[t] for t in chosen] + [x]
                if m1_full(G):
                    if on_leaf is None or on_leaf(G):
                        return G
                    continue
                rejected[0] += 1
                continue
            c2 = cand & nbr[i]
            if c2.bit_count() < need:
                continue
            r = rec(chosen + [i], span | {s_ ^ x for s_ in span}, c2, o2, ou2)
            if r:
                return r
        return None
    allc = (1 << n) - 1
    r = rec([], {0}, allc, tuple([0] * nd), tuple([0] * nu))
    return r, nodes[0], rejected[0]


def all_skeletons(usable, GK, duals=(), units=(), masks=None, max_count=200, limit=2 * 10 ** 7, orbits=None):
    """every skeleton passing the class-level filters and M1, up to max_count; exhaustive flag"""
    out = []

    def leaf(G):
        out.append(list(G))
        return len(out) >= max_count
    try:
        r, nodes, rej = skeleton_exists(usable, GK, limit=limit, duals=duals, units=units, masks=masks, on_leaf=leaf,
                                        orbits=orbits)
        exhaustive = r is None
    except TimeoutError:
        exhaustive = False
    return {'list': out, 'exhaustive': exhaustive and len(out) < max_count}


def main(tag, first=None, ids=None, limit=10 ** 8):
    from fractions import Fraction as Fr
    from rank17_K import v_basis, solve_coeffs
    K = json.load(open(os.path.join(DATA, 'K_%s.json' % tag)))
    B, dim, m = v_basis(K['core'])
    Gv = np.array([[int(sum(a * b for a, b in zip(u, v))) for v in B] for u in B], dtype=np.int64)
    rootkeys = root_keys_mod4(Gv)
    outf = os.path.join(DATA, 'skeleton_%s.jsonl' % tag)
    done = set()
    if os.path.exists(outf):
        done = {json.loads(l)['pair'] for l in open(outf) if l.strip()}
    for rec_ in K['K'][:first]:
        if rec_['id'] in done or (ids is not None and rec_['id'] not in ids):
            continue
        t0 = time.time()
        GK = np.array(rec_['K_gram'], dtype=np.int64)
        Kv = np.array([solve_coeffs(B, [Fr(x) for x in row]) for row in rec_['K_basis']], dtype=np.int64)
        usable, (n10, n10L1, ncls), masks = usable_classes(GK, Kv, rootkeys)
        duals = short_duals(GK) if USE_DUALS else ()
        # kappa_e = P_W e for the units e of V: dual coordinates (e, K_i) = column of Kv Gv at e's V-coordinate
        KG = Kv @ Gv
        units = [KG[:, len(B) - m + j].copy() for j in range(m)] if USE_DUALS else []
        try:
            sk, nodes, m1rej = skeleton_exists(usable, GK, limit=limit, duals=duals, units=units,
                                               masks=masks if USE_M1 else None)
            verdict = 'SKELETON' if sk else 'NO SKELETON'
        except TimeoutError:
            sk, nodes, m1rej, verdict = None, -1, -1, 'LIMIT'
        row = {'V': K['V'], 'pair': rec_['id'], 'norm10_up_to_sign': n10, 'norm10_after_L1': n10L1, 'classes': ncls,
               'usable_classes': len(usable), 'short_duals': [[int(n7), km] for _, km, n7 in duals],
               'verdict': verdict, 'nodes': nodes, 'm1_rejected_leaves': m1rej, 'skeleton': sk, 'rootless_U_allowed': rec_['rootless_U_allowed'],
               's': round(time.time() - t0, 1)}
        print(json.dumps(row), flush=True)
        with open(outf, 'a') as f:
            f.write(json.dumps(row) + chr(10))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)

def witnesses(GK, nmax=8, nmin=5):
    """kappa in K* with nmin <= n = 7|kappa|^2 <= nmax, up to sign, in dual-basis coordinates x ((kappa, w) = x . w_K);
    returns [(x, n)] sorted by n.  Used by the per-vector VALUE filter (C1 + structures, 28/09 evening): for every frame
    vector w_u, a_u = (kappa, w_u) is the label value of an integer sigma-odd (-4)-eigenvector of type n (F9), so
      n = 5 : |a_u| <= 1   (the only n=5 cell is the 2|5 cut with 20 x +-1: k=0 min N*, k=1 row capacity, k>=3 PE)
      n = 8 : |a_u| <= 2   (+-3 killed by row capacity in every k; |a| <= 3 by Cauchy-Schwarz)
      n = 6, 7: no per-vector restriction beyond Cauchy-Schwarz (the k-dependent parts are per skeleton)."""
    from envelope_trap import inverse_exact
    Gi = inverse_exact([[int(x) for x in row] for row in GK])
    D = np.array([[int(x * 49) for x in row] for row in Gi], dtype=np.int64)
    assert all((x * 49).denominator == 1 for row in Gi for x in row)
    X, nrm = short_vectors_chunked(D.tolist(), 7 * nmax)
    out = []
    for x, v in zip(X, nrm):
        v = int(v)
        if v == 0:
            continue
        assert v % 7 == 0, 'dual norm not in (1/7)Z'
        n = v // 7
        if n < nmin:
            raise AssertionError('witness with n=%d < %d: class should be excluded by F11' % (n, nmin))
        out.append((np.array(x, dtype=np.int64), n))
    out.sort(key=lambda t: t[1])
    return out


def value_filter_keep(W, wit):
    """boolean mask of the norm-10 vectors W (K coordinates) passing the per-vector value filter for the witnesses wit"""
    keep = np.ones(len(W), dtype=bool)
    Wl = W.astype(np.int64)
    for x, n in wit:
        v = np.abs(Wl @ x)
        if n == 5:
            keep &= v <= 1
        elif n == 8:
            keep &= v <= 2
    return keep
