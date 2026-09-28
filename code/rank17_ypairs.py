r"""Rank-17 switch: y-pair types in the 8 non-Z^17 unimodular lattices V = core + Z^m (C1's lane, agreed 27/09 night).
A y-pair = orthogonal y1, y2 in V of norm 7 with the unit bound Y(e) = (y1,e)^2 + (y2,e)^2 <= 4 on every unit vector e of V
(handoff Cor. 6.2 argument; needs min U >= 2), flag rootless_U_allowed when Y(e) <= 2 on every unit (min U >= 3, Cor. 6.3).
Classification up to Aut(V) x (independent signs of y1, y2) x (swap y1 <-> y2).
Aut(V) = Aut(core) x Aut(Z^m): the unit vectors of V are exactly the +-e_j of Z^m (the cores have none), so both factors are
preserved. Aut(core) = W(core roots) x| Gamma_core, with Gamma_core = {1} (E8, D12+, D16+), {1, -w0} (A15+, A11E6+: -w0 is
already covered by the global sign of (y1, y2), since -1 lies in Aut(V)), {1, swap} (E8^2, E7^2+, D8^2+).
Canonical form of a pair:
  core part (c1, c2): reflect both until c1 is dominant, then reflect both in the simple roots orthogonal to c1 until c2 is
  dominant for that parabolic subgroup (= Stab_W(c1)): unique per W-orbit of pairs; then min over Gamma_core;
  Z^m part (z1, z2): multiset of the columns (z1_j, z2_j) up to simultaneous sign, sorted;
  global: min over the 8 sign/swap variants.
Completeness: every orthogonal norm-7 pair of V with the unit bound is enumerated (all core vectors of norm <= 7, all
z in Z^m with |z_j| <= 2), then reduced; nothing is filtered except by the stated hypotheses.
Usage: python rank17_ypairs.py <core name|all> [out_dir]"""
import itertools, json, math, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rank17_cores import cores, int_basis
from h_stage2 import short_vectors_fast
from y_pairs import root_system

UNITS = {'E8': 9, 'D12+': 5, 'E7^2+': 3, 'A15+': 2, 'E8^2': 1, 'D16+': 1, 'D8^2+': 1, 'A11E6+': 0}
SWAP = {'E8^2': (8, 8), 'E7^2+': (8, 8), 'D8^2+': (8, 8)}           # the two components are the two 8-coordinate blocks


FP_EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fp_short.exe')
FAST_SV = os.environ.get('R17_FAST_SV', '1') == '1'
_fp_calls = [0]


def _fp_short(n, bound, d, Q):
    """fp_short.exe: the recursion below, compiled (same float operations in the same order, same output order)"""
    import struct, subprocess, tempfile
    tmp = os.path.join(tempfile.gettempdir(), 'r17fp')
    os.makedirs(tmp, exist_ok=True)
    _fp_calls[0] += 1
    fi = os.path.join(tmp, 'in_%d_%d.bin' % (os.getpid(), _fp_calls[0]))
    fo = os.path.join(tmp, 'out_%d_%d.bin' % (os.getpid(), _fp_calls[0]))
    with open(fi, 'wb') as f:
        f.write(struct.pack('<i', n) + struct.pack('<d', bound))
        f.write(np.array(d, dtype='<f8').tobytes())
        f.write(np.array(Q, dtype='<f8').tobytes())
    r = subprocess.run([FP_EXE, fi, fo], capture_output=True)
    assert r.returncode == 0, 'fp_short failed: %r' % r.stderr[-300:]
    raw = open(fo, 'rb').read()
    cnt = struct.unpack('<i', raw[:4])[0]
    X = np.frombuffer(raw[4:], dtype=np.int8).reshape(cnt, n).copy()
    os.remove(fi); os.remove(fo)
    return X


def short_vectors_chunked(Gi, bound, chunk=200000):
    """h_stage2.short_vectors_fast (same Fincke-Pohst, same output set: all x != 0 up to sign with x G x <= bound), but the
    output is kept as int8 array chunks instead of one Python list of tuples (memory: A11E6+ has ~1M such vectors)"""
    n = len(Gi)
    Gf = np.array(Gi, dtype=float)
    L = np.linalg.cholesky(Gf)
    d = [float(L[i, i] ** 2) for i in range(n)]
    Q = [[float(L[j, i] / L[i, i]) if j > i else 0.0 for j in range(n)] for i in range(n)]
    chunks, buf = [], []
    x = [0] * n
    eps = 1e-7

    def rec(k, rem):
        s_ = 0.0
        Qk = Q[k]
        for j in range(k + 1, n):
            if x[j]:
                s_ += Qk[j] * x[j]
        c = -s_
        sp = math.sqrt(max(rem, 0.0) / d[k]) + eps
        lo, hi = math.ceil(c - sp), math.floor(c + sp)
        dk = d[k]
        for xi in range(lo, hi + 1):
            t = xi - c
            r2 = rem - dk * t * t
            if r2 < -eps:
                continue
            x[k] = xi
            if k == 0:
                buf.append(tuple(x))
                if len(buf) >= chunk:
                    chunks.append(np.array(buf, dtype=np.int8)); buf.clear()
            else:
                rec(k - 1, r2)
        x[k] = 0
    if FAST_SV and os.path.exists(FP_EXE):
        X = _fp_short(n, float(bound), d, Q)                           # compiled, same arithmetic and order
    else:
        rec(n - 1, float(bound) + eps)
        if buf:
            chunks.append(np.array(buf, dtype=np.int8))
        X = np.vstack(chunks) if chunks else np.zeros((0, n), dtype=np.int8)
    # keep one of +-x (first nonzero coordinate positive) and drop 0, as short_vectors_fast's output
    X = X[(X != 0).any(axis=1)]
    first = X[np.arange(len(X)), (X != 0).argmax(axis=1)]
    X = X[first > 0]
    Gi64 = np.array(Gi, dtype=np.int64)
    nrm = np.empty(len(X), dtype=np.int64)
    for s0 in range(0, len(X), 100000):                               # no (n x 17 x 17) intermediate
        Xb = X[s0:s0 + 100000].astype(np.int64)
        nrm[s0:s0 + 100000] = ((Xb @ Gi64) * Xb).sum(axis=1)
    keep = nrm <= bound
    return X[keep], nrm[keep]


def needed_norms(m):
    """core norms n for which 7 - n is a norm of some z in Z^m with |z_j| <= 2 (plus 2, for the roots)"""
    sq = {0}
    for _ in range(m):
        sq = {a + b for a in sq for b in (0, 1, 4)}
    return sorted({7 - t for t in sq if t <= 7} | {2})


def core_vectors(name, norms):
    """core vectors of the given norms (both signs; the zero vector for norm 0), scaled integer ambient coordinates (scale S).
    Memory-lean: only the needed norms are expanded (A11E6+ needs norm 7 only)."""
    gens, dim = cores()[name]
    B = int_basis(gens)
    Gm = [[int(sum(a * b for a, b in zip(u, v))) for v in B] for u in B]
    S = 1
    for row in B:
        for x in row:
            S = S * x.denominator // math.gcd(S, x.denominator)
    BS = np.array([[int(x * S) for x in row] for row in B], dtype=np.int64)
    X, nrm = short_vectors_chunked(Gm, max(norms))
    byn = {}
    for n in norms:
        if n == 0:
            byn[0] = np.zeros((1, dim), dtype=np.int32)
            continue
        Xn = X[nrm == n].astype(np.int64)
        Vn = (Xn @ BS).astype(np.int32)
        del Xn
        assert np.array_equal((Vn.astype(np.int64) ** 2).sum(axis=1), np.full(len(Vn), n * S * S))
        byn[n] = np.vstack([Vn, -Vn])
    del X
    return byn, S, dim


def simple_roots(R2, S):
    R = R2.astype(float) / S
    Sr, comp, marks, A, P = root_system(R)
    return np.rint(Sr * S).astype(np.int64)                           # simple roots, scaled


def reduce_pairs(C1, C2, SR, S):
    """vectorised: reflect rows of (C1, C2) until C1 is dominant, then (with the simple roots orthogonal to C1) until C2 is
    dominant for that parabolic. Reflection in a root a (norm 2): x -> x - (x.a)/2 * 2a/ (a.a)... scaled: x.a is S^2 * (x,a);
    s_a(x) = x - (x,a) a  (norm-2 roots), i.e. x - (x_s . a_s) / S^2 * a_s."""
    C1 = np.array(C1, dtype=np.int64); C2 = np.array(C2, dtype=np.int64)      # int64 copies: keys must share one dtype
    S2 = S * S
    for _ in range(10000):
        ip = C1 @ SR.T                                                # S^2 (c1, alpha)
        neg = ip < 0
        rows = np.nonzero(neg.any(axis=1))[0]
        if len(rows) == 0:
            break
        j = np.argmax(neg[rows], axis=1)
        a = SR[j]
        k1 = ip[rows, j] // S2
        k2 = (C2[rows] * a).sum(axis=1) // S2
        C1[rows] -= k1[:, None] * a
        C2[rows] -= k2[:, None] * a
    else:
        raise RuntimeError('dominance loop')
    for _ in range(10000):
        ip1 = C1 @ SR.T
        ip2 = C2 @ SR.T
        neg = (ip1 == 0) & (ip2 < 0)
        rows = np.nonzero(neg.any(axis=1))[0]
        if len(rows) == 0:
            break
        j = np.argmax(neg[rows], axis=1)
        a = SR[j]
        k2 = ip2[rows, j] // S2
        C2[rows] -= k2[:, None] * a
    else:
        raise RuntimeError('parabolic loop')
    return C1, C2


def z_key(z1, z2):
    cols = []
    for a, b in zip(z1, z2):
        if a < 0 or (a == 0 and b < 0):
            a, b = -a, -b
        if a or b:
            cols.append((int(a), int(b)))
    return tuple(sorted(cols, reverse=True))


def classify(name, out_dir=None):
    t0 = time.time()
    m = UNITS[name]
    byn, S, dim = core_vectors(name, needed_norms(m))
    SR = simple_roots(byn[2], S)
    S2 = S * S
    for n in range(8):
        byn.setdefault(n, np.zeros((0, dim), dtype=np.int32))
    if m:
        Z = np.array(list(itertools.product(range(-2, 3), repeat=m)), dtype=np.int64)
        Z = Z[(Z * Z).sum(axis=1) <= 7]
    else:
        Z = np.zeros((1, 0), dtype=np.int64)
    zn = (Z * Z).sum(axis=1)
    swap = SWAP.get(name)

    def sw(X):
        p, q = swap
        return np.concatenate([X[:, p:p + q], X[:, :p], X[:, p + q:]], axis=1)

    def keys_batch(C1, Z1, C2, Z2):
        """canonical keys of a batch of pairs up to Aut(V) x signs x swap (8 variants, x2 with the core swap)"""
        best = [None] * len(C1)
        variants = []
        for (a1, b1, a2, b2) in ((C1, Z1, C2, Z2), (C2, Z2, C1, Z1)):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    variants.append((s1 * a1, s1 * b1, s2 * a2, s2 * b2))
                    if swap:
                        variants.append((sw(s1 * a1), s1 * b1, sw(s2 * a2), s2 * b2))
        for (a1, b1, a2, b2) in variants:
            D1, D2 = reduce_pairs(a1, a2, SR, S)
            for i in range(len(D1)):
                k = (D1[i].tobytes() + D2[i].tobytes(), z_key(b1[i], b2[i]))
                if best[i] is None or k < best[i]:
                    best[i] = k
        return best
    reps = {}
    stats = {'y1_types': 0, 'candidates': 0}
    for n1 in range(8):
        if len(byn[n1]) == 0:
            continue
        Z1 = Z[zn == 7 - n1]
        if len(Z1) == 0:
            continue
        C1all = byn[n1]
        dom1 = C1all[((C1all @ SR.T) >= 0).all(axis=1)]                 # the dominant member of each W-orbit
        z1s = sorted({tuple(sorted((abs(int(v)) for v in z), reverse=True)) for z in Z1})
        for c1 in dom1:
            J = SR[(SR @ c1) == 0]
            for z1t in z1s:
                z1 = np.array(z1t, dtype=np.int64)
                stats['y1_types'] += 1
                for n2 in range(8):
                    if len(byn[n2]) == 0:
                        continue
                    Z2 = Z[zn == 7 - n2]
                    if m and len(Z2):
                        Z2 = Z2[((z1[None, :] ** 2 + Z2 ** 2) <= 4).all(axis=1)]
                    if len(Z2) == 0:
                        continue
                    zt = Z2 @ z1
                    C2all = byn[n2]
                    ct = (C2all @ c1) // S2
                    for t in np.unique(zt):
                        C2 = C2all[ct == -t]
                        if len(J) and len(C2):
                            C2 = C2[((C2 @ J.T) >= 0).all(axis=1)]           # W_J-orbit reps (W_J = Stab_W(c1))
                        if len(C2) == 0:
                            continue
                        zreps = {}
                        for z2 in Z2[zt == t]:
                            zreps.setdefault(z_key(z1, z2), z2)
                        zr = (np.array(list(zreps.values()), dtype=np.int64).reshape(-1, m) if m
                              else np.zeros((len(zreps), 0), dtype=np.int64))
                        nb = len(C2) * len(zr)
                        stats['candidates'] += nb
                        C1b = np.repeat(c1[None, :], nb, axis=0)
                        C2b = np.repeat(C2, len(zr), axis=0)
                        Z1b = np.repeat(z1[None, :], nb, axis=0)
                        Z2b = np.tile(zr, (len(C2), 1))
                        for s0 in range(0, nb, 20000):
                            sl = slice(s0, s0 + 20000)
                            ks = keys_batch(C1b[sl], Z1b[sl], C2b[sl], Z2b[sl])
                            for i, k in enumerate(ks):
                                if k not in reps:
                                    reps[k] = (C1b[sl][i], Z1b[sl][i], C2b[sl][i], Z2b[sl][i])
    out = []
    for i, (key, (c1, z1, c2, z2)) in enumerate(sorted(reps.items())):
        Ymax = max([int(a * a + b * b) for a, b in zip(z1, z2)] + [0])
        y1 = [F(int(v), S) for v in c1] + [F(int(v)) for v in z1]
        y2 = [F(int(v), S) for v in c2] + [F(int(v)) for v in z2]
        assert sum(a * a for a in y1) == 7 and sum(a * a for a in y2) == 7 and sum(a * b for a, b in zip(y1, y2)) == 0
        out.append({'id': i, 'core_norms': [int(c1 @ c1) // S2, int(c2 @ c2) // S2],
                    'y1_core': [str(x) for x in y1[:dim]], 'y1_units': [int(v) for v in z1],
                    'y2_core': [str(x) for x in y2[:dim]], 'y2_units': [int(v) for v in z2],
                    'max_unit_Y': Ymax, 'rootless_U_allowed': Ymax <= 2})
    res = {'V': name + (' + Z^%d' % m if m else ''), 'core': name, 'units': m,
           'status': 'Necessary-condition representatives, not exclusions',
           'hypotheses': 'Switched V = %s + Z^%d; original U has minimum >= 2 (unit bound Y(e) <= 4); '
                         'rootless_U_allowed marks the pairs with Y(e) <= 2 (U minimum >= 3)' % (name, m),
           'equivalence': 'Aut(V) = Aut(core) x signed permutations of Z^m, independent signs of y1, y2, swap y1 <-> y2',
           'coordinates': 'core part in the ambient coordinates of rank17_cores.py (%d coordinates), then the %d unit '
                          'coordinates' % (dim, m),
           'n_pairs': len(out), 'n_rootless_allowed': sum(p['rootless_U_allowed'] for p in out),
           'stats': stats, 'seconds': round(time.time() - t0, 1), 'pairs': out}
    print(json.dumps({k: v for k, v in res.items() if k != 'pairs'}), flush=True)
    if out_dir:
        fn = os.path.join(out_dir, 'ypairs_%s.json' % name.replace('^', '').replace('+', 'p'))
        json.dump(res, open(fn, 'w'), indent=1)
    return res


if __name__ == '__main__':
    names = list(UNITS) if sys.argv[1] == 'all' else [sys.argv[1]]
    od = sys.argv[2] if len(sys.argv) > 2 else None
    if od:
        os.makedirs(od, exist_ok=True)
    for nm in names:
        classify(nm, od)
