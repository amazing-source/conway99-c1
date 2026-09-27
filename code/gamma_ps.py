r"""Finish line (C), C1 27/09 night: Gamma = Aut(U)/W(R) for ANY envelope, as the stabiliser of the Weyl vector.
Gamma = Stab_{O(U)}(chamber) = Stab_{O(U)}(rho), rho = the Weyl vector of the chamber that y_pairs.root_system picks
((rho, s) = 1 for every simple root s): an isometry fixing rho permutes the positive roots, hence the chamber; conversely a
chamber-preserving isometry permutes the positive roots, hence fixes rho.
Search (Plesken-Souvignier): V = all vectors of norm <= 3 (both signs). Each v in V gets an invariant fingerprint
(norm, (v, rho), sorted multiset of (v, s) over the simple roots s [Gamma permutes them], histogram of (norm x, (v, x)) over
x in V [O(U)-invariant]). The base b_1..b_L is a GENERATING SET of U over Z taken from V, rarest fingerprints first: then an
assignment b_i -> v_i with equal fingerprints and equal inner products is exactly an element of Gamma (it preserves the Gram
matrix on a Z-generating set, maps U into U and fixes rho), so no branch dies late on integrality.
Generators by a stabiliser chain (Schreier-Sims style): for i = L..1, the orbit of b_i under the group found so far that fixes
b_1..b_{i-1}; every candidate image outside that orbit is searched for ONE element (identity on b_1..b_{i-1}, b_i -> c);
|Gamma| = product of the orbit lengths. All elements are then listed by closure.
Output: as gamma_general.py ('matrices' act on coefficient rows of the LLL basis of y_pairs.setup: a -> a @ M), plus 'basis'
(that LLL basis, rows as fraction strings): y_pairs_gamma converts the matrices when its own basis differs, and verifies them.
Usage: python gamma_ps.py <envelope.json> [out.json]"""
import json, math, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y_pairs import setup as ysetup, root_system
from envelope_trap import inverse_exact, hnf_rows
from h_stage2 import short_vectors_fast


def main():
    rec_ = json.load(open(sys.argv[1]))
    t0 = time.time()
    B, Gi, Bf, R, X3, Snew = ysetup(rec_['gens'])
    G = np.array(Gi, dtype=np.int64)
    S, comp, marks, A, P = root_system(R)
    rank = len(S)
    X, nrm = short_vectors_fast(Gi, 3)
    X = np.array(X, dtype=np.int64)
    V = np.vstack([X, -X])
    nV = np.concatenate([nrm, nrm]).astype(np.int64)
    N = len(V)
    VG = V @ G
    Binv = np.linalg.inv(Bf)
    Sc = np.rint(S @ Binv).astype(np.int64)
    assert np.allclose(Sc.astype(float) @ Bf, S, atol=1e-6)
    VS = VG @ Sc.T                                                     # (v, s_j), integers
    w = [sum(r) for r in inverse_exact([[int(x) for x in row] for row in A])] if rank else []
    den = 1
    for x in w:
        den = den * x.denominator // math.gcd(den, x.denominator)
    wI = np.array([int(x * den) for x in w], dtype=np.int64)
    vr = VS @ wI if rank else np.zeros(N, dtype=np.int64)            # den * (v, rho)
    # histogram of (norm x, (v, x)) over x in V: |(v, x)| <= 3 by Cauchy-Schwarz
    H = np.zeros((N, 2, 7), dtype=np.int64)
    n2 = (nV == 2)
    for s0 in range(0, N, 512):
        IP = VG[s0:s0 + 512] @ V.T
        for t in range(-3, 4):
            E = (IP == t)
            H[s0:s0 + 512, 0, t + 3] = E[:, n2].sum(axis=1)
            H[s0:s0 + 512, 1, t + 3] = E[:, ~n2].sum(axis=1)
    fp = [(int(nV[k]), int(vr[k]), tuple(sorted(VS[k].tolist())), tuple(H[k].ravel().tolist())) for k in range(N)]
    classes = {}
    for k, f in enumerate(fp):
        classes.setdefault(f, []).append(k)
    # base = Z-generating set of U from V, rarest fingerprints first (track rank, then index)
    order = sorted(range(N), key=lambda k: (len(classes[fp[k]]), int(nV[k]), k))
    base, Hrows, indep = [], [], []
    rk, idx = 0, None
    Qb, Hinv_f = np.zeros((0, 24)), None                             # float pre-checks (exact HNF decides)
    for k in order:
        vk = V[k].astype(float)
        if rk < 24:
            if len(Qb):
                res = vk - Qb.T @ (Qb @ vk)
                if res @ res < 1e-6:
                    continue                                          # in the Q-span: no rank gain
        else:
            co = vk @ Hinv_f
            if np.allclose(co, np.rint(co), atol=1e-6):
                continue                                              # already in the Z-span
        H2 = hnf_rows(Hrows + [[int(x) for x in V[k]]])
        r2 = len(H2)
        if r2 > rk:
            base.append(k); indep.append(k); Hrows, rk = H2, r2
        elif r2 == 24:
            i2 = abs(math.prod(H2[i][next(c for c in range(24) if H2[i][c])] for i in range(24)))
            if i2 < idx:
                base.append(k); Hrows = H2
        else:
            continue
        if rk < 24:
            Qb = np.linalg.qr(V[indep].astype(float).T)[0].T          # orthonormal basis of the Q-span
        else:
            idx = abs(math.prod(Hrows[i][next(c for c in range(24) if Hrows[i][c])] for i in range(24)))
            Hinv_f = np.linalg.inv(np.array(Hrows, dtype=float))
            if idx == 1:
                break
    assert rk == 24 and idx == 1, 'norm <= 3 vectors do not generate U'
    L = len(base)
    Bv = V[base]
    target = Bv @ G @ Bv.T
    cand0 = [np.array(classes[fp[k]], dtype=np.int64) for k in base]
    # exact M from the images of the 24 independent base vectors: M = Bc^-1 Ic
    pos_indep = [base.index(k) for k in indep]
    BcInv = inverse_exact([[int(x) for x in V[k]] for k in indep])
    lcm = 1
    for row in BcInv:
        for x in row:
            lcm = lcm * x.denominator // math.gcd(lcm, x.denominator)
    BcInvI = np.array([[int(x * lcm) for x in row] for row in BcInv], dtype=object)

    def matrix(imgs):
        Ic = V[[imgs[p] for p in pos_indep]].astype(object)
        num = BcInvI.dot(Ic)
        assert all(int(x) % lcm == 0 for x in num.flat)
        M = np.array([[int(x) // lcm for x in row] for row in num], dtype=np.int64)
        assert np.array_equal(M @ G @ M.T, G) and np.array_equal(Bv @ M, V[imgs])
        return M

    def filt(cands, lev, v):
        """candidate lists for levels lev+1.. after fixing level lev -> v (None if one becomes empty)"""
        ip = VG[v]
        out = []
        for m, c in enumerate(cands, start=lev + 1):
            c2 = c[(V[c] @ ip) == target[m, lev]]
            if len(c2) == 0:
                return None
            out.append(c2)
        return out
    nodes = [0]

    def complete(lev, imgs, cands):
        """first full consistent assignment extending imgs (levels lev..L-1 with candidate lists cands), or None"""
        nodes[0] += 1
        if lev == L:
            return imgs
        for v in cands[0]:
            nxt = filt(cands[1:], lev, int(v))
            if nxt is not None:
                r = complete(lev + 1, imgs + [int(v)], nxt)
                if r is not None:
                    return r
        return None
    # identity-prefix candidate lists
    pref = [cand0]
    for i in range(L):
        nxt = filt(pref[i][1:], i, base[i])
        assert nxt is not None
        pref.append(nxt)
    vkey = {tuple(v): k for k, v in enumerate(V.tolist())}
    gens = []                                                           # (level, M)

    def orbit_of(start, mats):
        orb, fr = {start}, [start]
        while fr:
            nf = []
            for k in fr:
                for M in mats:
                    j = vkey[tuple((V[k] @ M).tolist())]
                    if j not in orb:
                        orb.add(j); nf.append(j)
            fr = nf
        return orb
    orbit_lengths = []
    for i in range(L - 1, -1, -1):
        mats_i = [M for lev, M in gens if lev >= i]
        orb = orbit_of(base[i], mats_i)
        for c in pref[i][0]:
            c = int(c)
            if c in orb:
                continue
            nxt = filt(pref[i][1:], i, c)
            if nxt is None:
                continue
            imgs = complete(i + 1, list(base[:i]) + [c], nxt)
            if imgs is not None:
                M = matrix(imgs)
                gens.append((i, M)); mats_i.append(M)
                orb = orbit_of(base[i], mats_i)
        orbit_lengths.append(len(orb))
    order_g = math.prod(orbit_lengths)
    # all elements by closure
    Ms = [M for _, M in gens]
    I = np.eye(24, dtype=np.int64)
    elems = {I.tobytes(): I}
    fr = [I]
    while fr:
        nf = []
        for X_ in fr:
            for M in Ms:
                Y_ = X_ @ M
                kb = Y_.tobytes()
                if kb not in elems:
                    elems[kb] = Y_; nf.append(Y_)
        fr = nf
    mats = list(elems.values())
    assert len(mats) == order_g, (len(mats), order_g)
    out = {'id': rec_['id'], 'roots': rec_['roots'], 'rank': rank, 'gamma_order': len(mats), 'generators': len(gens),
           'orbit_lengths': orbit_lengths[::-1], 'base_size': L, 'nodes': nodes[0], 'short_vectors': int(N),
           'base_class_sizes': [len(c) for c in cand0], 'seconds': round(time.time() - t0, 1),
           'method': 'gamma_ps v2 (Stab(rho); Z-generating base; Schreier-Sims generators; closure)',
           'basis': [[str(x) for x in row] for row in B], 'generator_matrices': [M.tolist() for _, M in gens],
           'matrices': [m.tolist() for m in mats]}
    return out


if __name__ == '__main__':
    res = main()
    table = {L_['id']: L_ for L_ in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'borcherds_odd24.json')))}
    res['table_group'] = table[res['id']]['group']
    print(json.dumps({k: v for k, v in res.items() if k not in ('matrices', 'basis', 'generator_matrices')}), flush=True)
    if len(sys.argv) > 2:
        json.dump(res, open(sys.argv[2], 'w'))
