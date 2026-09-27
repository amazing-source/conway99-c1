r"""Finish line (C), C1 27/09 night: Gamma = Aut(U)/W(R) for ANY envelope, as the stabiliser of the Weyl vector.
Gamma = Stab_{O(U)}(chamber) = Stab_{O(U)}(rho), rho = the Weyl vector of the chamber that y_pairs.root_system picks
((rho, s) = 1 for every simple root s): an isometry fixing rho permutes the positive roots, hence the chamber; conversely a
chamber-preserving isometry permutes the positive roots, hence fixes rho.
Search (Plesken-Souvignier style): V = all vectors of norm <= 3 (both signs). Every v in V gets an invariant fingerprint
(norm, (v, rho), sorted multiset of (v, s) over the simple roots s), since g in Gamma permutes the simple roots. Pick 24
vectors b_i of V spanning Q^24 with the rarest fingerprints; an element g is determined by the images g(b_i), which must have
the same fingerprint and the same inner products with the earlier images. At a leaf, M = Bc^-1 Ic must be integral and preserve
the Gram matrix (exact integer check). Every element of Gamma is found (it maps each b_i into its fingerprint class with the
right inner products), and every leaf that passes the check is in Gamma.
Output: same format as gamma_general.py ('matrices' act on coefficient rows of the LLL basis of y_pairs.setup: a -> a @ M),
plus 'basis' (that LLL basis, rows as fraction strings): y_pairs_gamma converts the matrices when its own basis differs.
Usage: python gamma_ps.py <envelope.json> [out.json]"""
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y_pairs import setup as ysetup, root_system
from envelope_trap import inverse_exact
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
    # (v, s_j) for the simple roots, and (v, rho) * den exactly
    Binv = np.linalg.inv(Bf)
    Sc = np.rint(S @ Binv).astype(np.int64)                           # simple roots as coefficient rows
    assert np.allclose(Sc.astype(float) @ Bf, S, atol=1e-6)
    VS = V @ G @ Sc.T                                                 # N x rank, integers
    w = [sum(r) for r in inverse_exact([[int(x) for x in row] for row in A])] if rank else []   # rho = sum_j w_j s_j
    den = 1
    for x in w:
        den = den * x.denominator // np.gcd(den, x.denominator)
    wI = np.array([int(x * den) for x in w], dtype=np.int64)
    vr = VS @ wI if rank else np.zeros(len(V), dtype=np.int64)       # den * (v, rho)
    fp = [(int(nV[k]), int(vr[k]), tuple(sorted(VS[k].tolist()))) for k in range(len(V))]
    classes = {}
    for k, f in enumerate(fp):
        classes.setdefault(f, []).append(k)
    # choose 24 vectors spanning Q^24, rarest fingerprint first
    order = sorted(range(len(V)), key=lambda k: (len(classes[fp[k]]), int(nV[k]), k))
    basis, Mb = [], np.zeros((0, 24))
    for k in order:
        M2 = np.vstack([Mb, V[k].astype(float)])
        if np.linalg.matrix_rank(M2) > len(basis):
            basis.append(k); Mb = M2
            if len(basis) == 24:
                break
    assert len(basis) == 24, 'norm <= 3 vectors do not span'
    Bc = V[basis]
    target = Bc @ G @ Bc.T
    VG = V @ G
    cand0 = [np.array(classes[fp[k]], dtype=np.int64) for k in basis]
    BcInv = inverse_exact([[int(x) for x in row] for row in Bc])
    lcm = 1
    for row in BcInv:
        for x in row:
            lcm = lcm * x.denominator // np.gcd(lcm, x.denominator)
    BcInvI = np.array([[int(x * lcm) for x in row] for row in BcInv], dtype=object)
    mats, leaves, nodes = [], [0], [0]

    def bt(level, cands, imgs):
        nodes[0] += 1
        if level == 24:
            leaves[0] += 1
            Ic = V[imgs].astype(object)
            num = BcInvI.dot(Ic)
            if any(int(x) % lcm for x in num.flat):
                return
            M = np.array([[int(x) // lcm for x in row] for row in num], dtype=np.int64)
            if np.array_equal(M @ G @ M.T, G) and abs(round(np.linalg.det(M.astype(float)))) == 1:
                mats.append(M)
            return
        for v in cands[0]:
            # filter the deeper levels by the inner products with the new image v
            ip = VG[v]
            nxt = []
            ok = True
            for m, c in enumerate(cands[1:], start=level + 1):
                c2 = c[(V[c] @ ip) == target[m, level]]
                if len(c2) == 0:
                    ok = False; break
                nxt.append(c2)
            if ok:
                bt(level + 1, nxt, imgs + [int(v)])

    # level 0 candidates are the class of b_0; deeper levels start as their classes
    bt(0, cand0, [])
    out = {'id': rec_['id'], 'roots': rec_['roots'], 'rank': rank, 'gamma_order': len(mats), 'leaves': leaves[0],
           'nodes': nodes[0], 'short_vectors': int(len(V)), 'basis_class_sizes': [len(c) for c in cand0],
           'seconds': round(time.time() - t0, 1), 'method': 'gamma_ps (Stab(rho), Plesken-Souvignier style)',
           'basis': [[str(x) for x in row] for row in B], 'matrices': [m.tolist() for m in mats]}
    return out


if __name__ == '__main__':
    res = main()
    table = {L['id']: L for L in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'borcherds_odd24.json')))}
    res['table_group'] = table[res['id']]['group']
    print(json.dumps({k: v for k, v in res.items() if k != 'matrices'}), flush=True)
    if len(sys.argv) > 2:
        json.dump(res, open(sys.argv[2], 'w'))
