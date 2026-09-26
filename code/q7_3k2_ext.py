"""3K2_or14, q:7 kill WITHOUT the 24 uncertified cases of step 1 (notes/131 sec. 7).
Step 1 (48 pair-level MILPs) forced perm type (phi = 1) for every sib orbit on every sink pair {2, m}.  C2 certified exactly
the 24 cases 'sib pair X on the blocks of the PREVIOUS group' (X = A, B, C = {0,4}, {1,3}, {5,6}; previous of A is C,
of B is A, of C is B); the 24 cases 'X on the NEXT group' (A -> B -> C -> A) resist certify.py.
Here the sib shadows are allowed to be of (2,0) type on the next group: both labels of one block m of the next group
(then Z_uu = s_{m+} s_{m-} = +-1, the orbit is NOT rigid: k_u on the circle of norm -Z_uu, anisotropic r = I).
Full-pivot block c = 2: T_FF = Z + K K^T (mod 7) with k_f in F_7^2, k_f . k_f = -Z_ff.
Conditions used (all necessary): sisters T = 0 (D-partners); between two sib pairs T is a signed permutation (8.1);
cross orbit f (pair meeting two groups): shadow with 1 label in each met group and 2 in the third (sink balance, 576 options),
T_{u,f} = 0 for both orbits of a sib pair met by f, exactly one of the two orbits of the other sib pair at +-1 (8.1)."""
import itertools, sys, time
import numpy as np

P = 7
ONLY_PERM = '--perm' in sys.argv
if ONLY_PERM:
    sys.argv.remove('--perm')
blocks = [0, 1, 3, 4, 5, 6]
LAB = [(b, s) for b in blocks for s in (1, -1)]
LI = {l: i for i, l in enumerate(LAB)}
pairs = {'A': (0, 4), 'B': (1, 3), 'C': (5, 6)}
nxt = {'A': 'B', 'B': 'C', 'C': 'A'}
prv = {'A': 'C', 'B': 'A', 'C': 'B'}
W = np.zeros((12, 12), dtype=np.int64)
for i, (b, s) in enumerate(LAB):
    for j, (b2, s2) in enumerate(LAB):
        if b == b2:
            W[i, j] = 5 if s == s2 else 4


def vec(d):
    v = np.zeros(12, dtype=np.int64)
    for l, c in d.items():
        v[LI[l]] += c
    return v


def delta_vec(rep):
    d = {}
    for (b, s) in rep:
        d[(b, s)] = d.get((b, s), 0) + 1
        d[(b, -s)] = d.get((b, -s), 0) - 1
    return vec(d)


def B_dot(rep1, rep2):
    return sum(s * s2 for (b, s) in rep1 for (b2, s2) in rep2 if b == b2)


def st_vec(rep, sh):
    return (vec(sh) + 2 * delta_vec(rep)) % P


def Zval(rep1, sh1, rep2, sh2):
    a, b = st_vec(rep1, sh1), st_vec(rep2, sh2)
    return int((5 * B_dot(rep1, rep2) + a @ W @ b + (3 if rep1 == rep2 else 0)) % P)


def reps_of(p):
    return [((p[0], 1), (p[1], 1)), ((p[0], 1), (p[1], -1))]


VECS = [np.array([a, b], dtype=np.int64) for a in range(P) for b in range(P)]
CIRCLE = {}
for v in VECS:
    CIRCLE.setdefault(int(v @ v) % P, []).append(v)


def sib_label_sets(X):
    Nb, Pb = pairs[nxt[X]], pairs[prv[X]]
    nsets = [((Nb[0], s1), (Nb[1], s2)) for s1 in (1, -1) for s2 in (1, -1)]          # perm on next group
    if not ONLY_PERM:
        nsets += [((m, 1), (m, -1)) for m in Nb]                                     # (2,0) on next group
    psets = [((Pb[0], s1), (Pb[1], s2)) for s1 in (1, -1) for s2 in (1, -1)]         # perm on previous group
    all8 = [(b, s) for b in Nb + Pb for s in (1, -1)]
    out = []
    for ns in nsets:
        for ps in psets:
            labs = list(ns) + list(ps)
            comp = [l for l in all8 if l not in labs]
            out.append((labs, comp))
    return out


def signings(labs):
    for plus in itertools.combinations(range(4), 2):
        yield {labs[i]: (1 if i in plus else -1) for i in range(4)}


def sib_pair_options(X):
    """(s_u, k_u, s_ubar, k_ubar) with k's on the right circles and T_{u,ubar} = 0."""
    ru, rb = reps_of(pairs[X])
    out = []
    for labs, comp in sib_label_sets(X):
        for su in signings(labs):
            zu = Zval(ru, su, ru, su)
            ku_list = CIRCLE[(-zu) % P]
            for sb in signings(comp):
                zb = Zval(rb, sb, rb, sb)
                kb_list = CIRCLE[(-zb) % P]
                zub = Zval(ru, su, rb, sb)
                for ku in ku_list:
                    for kb in kb_list:
                        if (zub + int(ku @ kb)) % P == 0:
                            out.append((su, ku, sb, kb))
    return out


def T_block(X, ox, Y, oy):
    rx, ry = reps_of(pairs[X]), reps_of(pairs[Y])
    sx, kx = (ox[0], ox[2]), (ox[1], ox[3])
    sy, ky = (oy[0], oy[2]), (oy[1], oy[3])
    return [[(Zval(rx[i], sx[i], ry[j], sy[j]) + int(kx[i] @ ky[j])) % P for j in range(2)] for i in range(2)]


def signed_perm(M):
    for perm in ((0, 1), (1, 0)):
        if all((M[i][j] in (1, 6)) if j == perm[i] else (M[i][j] == 0) for i in range(2) for j in range(2)):
            return True
    return False


groups = pairs
cross_pairs = [(0, 1), (0, 3), (4, 1), (4, 3), (1, 5), (1, 6), (3, 5), (3, 6), (5, 0), (5, 4), (6, 0), (6, 4)]


def grp(b):
    return next(g for g, bs in groups.items() if b in bs)


def cross_options(p):
    g1, g2 = grp(p[0]), grp(p[1])
    g3 = next(g for g in 'ABC' if g not in (g1, g2))
    L1 = [(b, s) for b in groups[g1] for s in (1, -1)]
    L2 = [(b, s) for b in groups[g2] for s in (1, -1)]
    L3 = [(b, s) for b in groups[g3] for s in (1, -1)]
    out = []
    for a in L1:
        for b in L2:
            for cc in itertools.combinations(L3, 2):
                labs = [a, b, cc[0], cc[1]]
                for plus in itertools.combinations(range(4), 2):
                    out.append({labs[i]: (1 if i in plus else -1) for i in range(4)})
    return out


# precompute cross-orbit data: for each cross orbit (pair p, rep r): matrix of W s~_f over options, Z_ff, B_dot with sib reps
CROSS = []
for p in cross_pairs:
    for r in reps_of(p):
        opts = cross_options(p)
        St = np.array([st_vec(r, sh) for sh in opts]).T              # 12 x n
        WS = (W @ St) % P
        zff = np.array([(5 * B_dot(r, r) + int(St[:, j] @ W @ St[:, j]) + 3) % P for j in range(St.shape[1])])
        meets = {X: bool(set(p) & set(pairs[X])) for X in 'ABC'}
        CROSS.append({'p': p, 'r': r, 'WS': WS, 'zff': zff, 'meets': meets})


def cross_ok(assign):
    """assign: X -> (su, ku, sb, kb).  For every cross orbit: some (shadow, k_f) satisfies the 8.1 pattern."""
    S = []
    Kv = []
    Bd = []
    names = []
    for X in 'ABC':
        ru, rb = reps_of(pairs[X])
        su, ku, sb, kb = assign[X]
        S.append(st_vec(ru, su)); Kv.append(ku); names.append((X, ru))
        S.append(st_vec(rb, sb)); Kv.append(kb); names.append((X, rb))
    S = np.array(S)                  # 6 x 12
    Kv = np.array(Kv)                # 6 x 2
    for cf in CROSS:
        base = (S @ cf['WS'] + 5 * np.array([[B_dot(r, cf['r'])] for (_, r) in names])) % P    # 6 x n
        found = False
        for k in VECS:
            mask = cf['zff'] == (-(int(k @ k))) % P
            if not mask.any():
                continue
            Tm = (base[:, mask] + (Kv @ k)[:, None]) % P
            ok = np.ones(Tm.shape[1], dtype=bool)
            for xi, X in enumerate('ABC'):
                t0, t1 = Tm[2 * xi], Tm[2 * xi + 1]
                if cf['meets'][X]:
                    ok &= (t0 == 0) & (t1 == 0)
                else:
                    nz0 = (t0 == 1) | (t0 == 6)
                    nz1 = (t1 == 1) | (t1 == 6)
                    ok &= ((nz0 & (t1 == 0)) | (nz1 & (t0 == 0)))
                if not ok.any():
                    break
            if ok.any():
                found = True
                break
        if not found:
            return False
    return True


def stack(X, opts):
    ru, rb = reps_of(pairs[X])
    Su = np.array([st_vec(ru, o[0]) for o in opts]); Ku = np.array([o[1] for o in opts])
    Sb = np.array([st_vec(rb, o[2]) for o in opts]); Kb = np.array([o[3] for o in opts])
    return (ru, Su, Ku), (rb, Sb, Kb)


def compat(X, Y, opt):
    """boolean n_X x n_Y: the 2x2 T block between sib pairs X and Y is a signed permutation."""
    ox, oy = stack(X, opt[X]), stack(Y, opt[Y])
    T = [[None, None], [None, None]]
    for i in range(2):
        rx, Sx, Kx = ox[i]
        for j in range(2):
            ry, Sy, Ky = oy[j]
            T[i][j] = ((Sx @ W @ Sy.T) + 5 * B_dot(rx, ry) + Kx @ Ky.T) % P
    nz = [[(T[i][j] == 1) | (T[i][j] == 6) for j in range(2)] for i in range(2)]
    z = [[T[i][j] == 0 for j in range(2)] for i in range(2)]
    return (nz[0][0] & nz[1][1] & z[0][1] & z[1][0]) | (nz[0][1] & nz[1][0] & z[0][0] & z[1][1])


CANON = {a: CIRCLE[a][0] for a in CIRCLE}


def canonical(assign):
    for X in 'ABC':
        for k in (assign[X][1], assign[X][3]):
            if k.any():
                return bool(np.array_equal(k, CANON[int(k @ k) % P]))
    return True


if __name__ == '__main__':
    t0 = time.time()
    tcap = float(sys.argv[1]) if len(sys.argv) > 1 else 270
    opt = {X: sib_pair_options(X) for X in 'ABC'}
    for X in 'ABC':
        n20 = sum(1 for o in opt[X] if o[1].any() or o[3].any())
        print(X, 'sister options:', len(opt[X]), ' of which non-rigid ((2,0) type):', n20, flush=True)
    AB = compat('A', 'B', opt); BC = compat('B', 'C', opt); CA = compat('C', 'A', opt)
    print('compatible A-B, B-C, C-A:', int(AB.sum()), int(BC.sum()), int(CA.sum()), '(%.0fs)' % (time.time() - t0), flush=True)
    tri = []
    for i in range(AB.shape[0]):
        js = np.nonzero(AB[i])[0]
        if not len(js):
            continue
        ks_ok = np.nonzero(CA[:, i])[0]
        if not len(ks_ok):
            continue
        sub = BC[np.ix_(js, ks_ok)]
        for a, b in zip(*np.nonzero(sub)):
            tri.append((i, int(js[a]), int(ks_ok[b])))
    print('complete sib assignments:', len(tri), '(%.0fs)' % (time.time() - t0), flush=True)
    tri = [x for x in tri if canonical({'A': opt['A'][x[0]], 'B': opt['B'][x[1]], 'C': opt['C'][x[2]]})]
    print('after fixing the global SO(2) (first nonzero k canonical):', len(tri), flush=True)
    alive = 0
    n_20 = 0
    n = -1
    for n, (i, j, k) in enumerate(tri):
        if time.time() - t0 > tcap:
            print('TIME CAP after', n, 'assignments'); break
        assign = {'A': opt['A'][i], 'B': opt['B'][j], 'C': opt['C'][k]}
        if any(o[1].any() or o[3].any() for o in assign.values()):
            n_20 += 1
        if cross_ok(assign):
            alive += 1
            print('ALIVE assignment', i, j, k, flush=True)
    print('assignments checked:', n + 1, 'of', len(tri), '; with a (2,0) sib pair:', n_20, '; ALIVE:', alive,
          '(%.0fs)' % (time.time() - t0))
