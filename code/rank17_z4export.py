r"""Rank-17 pass 2 (C1, 28/09 night): export one (V, y-pair) for the compiled skeleton + mod-4 engine rank17_z4.c.
Everything the Python engine uses is exported, in the same order, so that the C enumeration and cell signature sets can be
compared one to one with rank17_skeleton.skeleton_exists (masks=None) and rank17_engine.Case.domains:
  classes U (usable, kmax-0 dual filter applied, ordered by (H-orbit min, class)), orbit-min flags, the mod-2 form (functional
  masks), parity bits of the kmax 1/2 duals and of the units, the 0/1 representative of each class in V/2V (17-bit mask);
  per class: its norm-10 vectors (V coordinates, up to sign, as in Case.class_data), the 15-bit functionals
  f(x) = (x G_V K_V^T) mod 2 of s(+w), s(-w) (s(q) = ((q - q mod 2) mod 4)/2) and of the refined-L1 vectors v = (r - w)/2.
File layout (little endian int32 unless noted): see write()."""
import json, os, sys, struct, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank17_skeleton as sk
import rank17_engine as eng

MAGIC = 0x5A344B31                                                          # 'Z4K1'


def mask15(X):
    """rows of 0/1 (or any int) matrix with 15 columns -> 15-bit ints of the parities"""
    return ((np.asarray(X) % 2).astype(np.int64) << np.arange(X.shape[1])).sum(axis=1)


def export(tag, pid, path):
    t0 = time.time()
    case = eng.Case(tag, pid, with_masks=False)                          # the C engine does not use the M1 masks
    GK, Kv, Gv, nB = case.GK, case.Kv, case.Gv, case.nB
    # --- skeleton-level data, exactly as skeleton_exists(orbits=...) builds it
    orbits = sk.root_orbits(GK, list(case.usable.keys()))
    U = np.array(sorted(case.usable, key=lambda x: (orbits[x], x)), dtype=np.int64)
    duals = case.duals
    k0 = [x for x, km, _ in duals if km == 0]
    if k0:
        bits = ((U[:, None] >> np.arange(15)) & 1)
        keep = np.ones(len(U), bool)
        for x in k0:
            keep &= (bits @ x) % 2 == 0
        U = U[keep]
    dk = [(x, km) for x, km, _ in duals if km > 0]
    assert len(dk) <= 30 and len(case.units) <= 30, 'too many duals/units for the int32 bit masks'
    n = len(U)
    bits = ((U[:, None] >> np.arange(15)) & 1).astype(np.int64)
    Gm2 = (GK % 2).astype(np.int64)
    Fm = mask15((bits @ Gm2) % 2)                                           # (U_i, U_j) odd <=> popcount(Fm_i & U_j) odd
    FK = np.zeros(n, dtype=np.int64)
    for t, (x, km) in enumerate(dk):
        FK |= ((bits @ x) % 2) << t
    FU = np.zeros(n, dtype=np.int64)
    for t, d in enumerate(case.units):
        FU |= ((bits @ d) % 2) << t
    GVK = Gv @ Kv.T                                                         # nB x 15: f(x) = (x @ GVK) mod 2
    rep17 = ((bits @ Kv) % 2)                                               # 0/1 representative in V coordinates
    gvm = (rep17 << np.arange(nB)).sum(axis=1)
    orbmin = np.array([orbits[int(x)] == int(x) for x in U], dtype=np.int64)
    # --- per-class vector data (all norm-10 vectors of the class, as Case.class_data)
    roots = case.roots                                                      # both signs, V coordinates
    rkey = (((roots % 2) << np.arange(nB)).sum(axis=1))
    order = np.argsort(rkey, kind='stable')
    rkey_s, roots_s = rkey[order], roots[order]
    corder = np.argsort(case.cls, kind='stable')                            # stable: in-class order = class_data order
    cls_s = case.cls[corder]
    with open(path, 'wb') as f:
        w32 = lambda *v: f.write(struct.pack('<%di' % len(v), *[int(x) for x in v]))
        w32(MAGIC, nB, n, len(dk), len(case.units))
        f.write(np.ascontiguousarray(Gv, dtype='<i4').tobytes())
        f.write(np.ascontiguousarray(GVK, dtype='<i4').tobytes())
        w32(*[km for _, km in dk])
        for i in range(n):
            w32(U[i], orbmin[i], Fm[i], FK[i], FU[i], gvm[i])
        tot_vec = tot_v = 0
        for i in range(n):
            C = int(U[i])
            a0, a1 = np.searchsorted(cls_s, C, side='left'), np.searchsorted(cls_s, C, side='right')
            Wc = case.W[corder[a0:a1]].astype(np.int64) @ Kv                # V coordinates, same order as class_data
            m = len(Wc)
            assert m == 0 or np.abs(Wc).max() <= 127
            rep = Wc % 2
            sp = ((Wc - rep) % 4) // 2
            sm = ((-Wc - rep) % 4) // 2
            fsp = mask15((sp @ GVK) % 2); fsm = mask15((sm @ GVK) % 2)
            key = (rep << np.arange(nB)).sum(axis=1)
            lo = np.searchsorted(rkey_s, key, side='left'); hi = np.searchsorted(rkey_s, key, side='right')
            w32(C, m)
            f.write(np.ascontiguousarray(Wc, dtype=np.int8).tobytes())
            # per vector k: fsp_k, fsm_k, cnt_k, then its cnt_k L1 functionals (vectorised; same stream as a loop)
            cnt = hi - lo
            tot = int(cnt.sum())
            off = np.cumsum(cnt) - cnt
            stream = np.empty(3 * m + tot, dtype=np.int64)
            start = 3 * np.arange(m) + off
            stream[start] = fsp; stream[start + 1] = fsm; stream[start + 2] = cnt
            if tot:
                owner = np.repeat(np.arange(m), cnt)
                e_ = np.arange(tot)
                ridx = lo[owner] + (e_ - off[owner])
                vs = (roots_s[ridx] - Wc[owner]) // 2
                stream[3 * owner + 3 + e_] = mask15((vs @ GVK) % 2)
            f.write(np.ascontiguousarray(stream, dtype='<i4').tobytes())
            tot_v += tot
            tot_vec += m
        # trailer: generators of H = <reflections in the roots of K> as permutations of the class indices 0..n-1
        # (action mod 2K: sigma -> sigma + (sigma, r)[r]); H preserves U (usable, kmax-0 filter), checked
        from rank17_ypairs import short_vectors_chunked
        X, nrm = short_vectors_chunked(GK.tolist(), 2)
        R = X[nrm == 2].astype(np.int64)
        pos = {int(c): k for k, c in enumerate(U)}
        gens = {}
        for r in R:
            rc = int(((r & 1) << np.arange(15)).sum())
            rf = int(((((r & 1) @ Gm2) % 2) << np.arange(15)).sum())
            p = np.array([pos[int(c) ^ rc] if bin(int(c) & rf).count('1') & 1 else k for k, c in enumerate(U)], dtype=np.int64)
            if not (p == np.arange(n)).all():
                gens[p.tobytes()] = p
        w32(len(gens))
        for p in gens.values():
            f.write(np.ascontiguousarray(p, dtype='<i4').tobytes())
    info = {'V': case.V, 'pair': pid, 'classes': n, 'duals_k12': len(dk), 'units': len(case.units), 'vectors': tot_vec,
            'l1_vectors': tot_v, 'H_generators': len(gens), 'export_s': round(time.time() - t0, 1),
            'bytes': os.path.getsize(path)}
    return info


if __name__ == '__main__':
    tag, pid, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    print(json.dumps(export(tag, pid, path)), flush=True)
