"""3K2_or14 (0-based): sink c = 2 (full pivot), sib pairs A = {0,4}, B = {1,3}, C = {5,6}.
At c: Q_c^-1 = 5I + 4P_pi (mod 7), g- = 20, K_c anisotropic.  For a sib orbit u disjoint from c whose shadow on star(c)
has one label per block (true here by the disjoint-sib Alt identity), Z_uu = 3 + 5*2 + s~^T W s~ = 13 + 20 + 16 = 0 mod 7,
so k_u = 0 and the whole T-row of u is forced: T_{u,f} = Z_{u,f} (mod 7) for every far orbit f.
Test on the 6 sib orbits only:  T_{u,u'} = 0 for sisters;  between two sib pairs a signed perfect matching.
Shadow of u (rep: pair's first block +, second block +/-): one label per block outside its pair and outside c, two +1 two -1;
the sister's shadow uses the other label of each block (8.1: each label w is adjacent to exactly one orbit of the pair).
Labels of X_c: block b in {0,1,3,4,5,6}, sign s -> key (b, s)."""
import itertools

P = 7
blocks = [0, 1, 3, 4, 5, 6]
pairs = {'A': (0, 4), 'B': (1, 3), 'C': (5, 6)}


def W(l1, l2):
    """(5I + 4P_pi) entry between labels l1 = (b, s), l2."""
    if l1[0] != l2[0]:
        return 0
    return 5 if l1[1] == l2[1] else 4


def dot(u, v):
    return sum(cu * cv * W(lu, lv) for lu, cu in u.items() for lv, cv in v.items())


def delta(rep):
    """delta of an orbit with representative rep = ((b1,s1),(b2,s2)): e_rep - e_sigma(rep) on X_c."""
    d = {}
    for (b, s) in rep:
        d[(b, s)] = d.get((b, s), 0) + 1
        d[(b, -s)] = d.get((b, -s), 0) - 1
    return d


def add(u, v, k=1):
    w = dict(u)
    for l, c in v.items():
        w[l] = w.get(l, 0) + k * c
    return {l: c for l, c in w.items() if c}


def B_dot(rep1, rep2):
    """(B^T B) between two far orbits (block coordinates other than c; c not in either)."""
    t = 0
    for (b, s) in rep1:
        for (b2, s2) in rep2:
            if b == b2:
                t += s * s2
    return t


def shadow_options(pair):
    others = [b for b in blocks if b not in pair]
    out = []
    for signs_lab in itertools.product((1, -1), repeat=4):          # which label of each block
        labs = [(b, s) for b, s in zip(others, signs_lab)]
        for plus in itertools.combinations(range(4), 2):
            sh = {labs[i]: (1 if i in plus else -1) for i in range(4)}
            out.append(sh)
    return out


def orbit_data(name):
    """the two orbits of sib pair `name`: reps and delta."""
    b1, b2 = pairs[name]
    reps = [((b1, 1), (b2, 1)), ((b1, 1), (b2, -1))]
    return reps


def Z(rep1, sh1, rep2, sh2):
    st1 = add(sh1, delta(rep1), 2)
    st2 = add(sh2, delta(rep2), 2)
    val = 5 * B_dot(rep1, rep2) + dot(st1, st2)
    if rep1 == rep2:
        val += 3
    return val % P


# per sib pair: valid (shadow, sister shadow) with complementary labels and Z_{u,u'} = 0, Z_uu = 0
per = {}
for name in 'ABC':
    reps = orbit_data(name)
    opts = shadow_options(pairs[name])
    good = []
    for s0 in opts:
        if Z(reps[0], s0, reps[0], s0) != 0:
            continue
        for s1 in opts:
            if set((b, -s) for (b, s) in s0) != set(s1):
                continue
            if Z(reps[1], s1, reps[1], s1) != 0:
                continue
            if Z(reps[0], s0, reps[1], s1) != 0:      # sisters: T = 0 (D-partners)
                continue
            good.append((s0, s1))
    per[name] = good
    print(name, 'valid sister-shadow pairs:', len(good))


def match_ok(nameX, gx, nameY, gy):
    rx, ry = orbit_data(nameX), orbit_data(nameY)
    Zm = [[Z(rx[i], gx[i], ry[j], gy[j]) for j in range(2)] for i in range(2)]
    # need T in {0,+-1} with exactly one nonzero per row and per column (signed perfect matching), T = Z mod 7
    for perm in ((0, 1), (1, 0)):
        ok = True
        for i in range(2):
            for j in range(2):
                v = Zm[i][j]
                if j == perm[i]:
                    if v not in (1, 6):
                        ok = False
                elif v != 0:
                    ok = False
        if ok:
            return True
    return False


cnt = 0
AB = {(i, j) for i, ga in enumerate(per['A']) for j, gb in enumerate(per['B']) if match_ok('A', ga, 'B', gb)}
print('compatible (A,B):', len(AB))
BC = {(j, k) for j, gb in enumerate(per['B']) for k, gc in enumerate(per['C']) if match_ok('B', gb, 'C', gc)}
print('compatible (B,C):', len(BC))
CA = {(k, i) for k, gc in enumerate(per['C']) for i, ga in enumerate(per['A']) if match_ok('C', gc, 'A', ga)}
print('compatible (C,A):', len(CA))
for (i, j) in AB:
    for k in range(len(per['C'])):
        if (j, k) in BC and (k, i) in CA:
            cnt += 1
print('complete assignments of the 6 sib shadows:', cnt)


# ---- cross orbits: rows of the 6 sib orbits are forced (k_u = 0) -> conditions on each cross orbit's shadow ----
groups = {'A': (0, 4), 'B': (1, 3), 'C': (5, 6)}
cross_pairs = [(0, 1), (0, 3), (4, 1), (4, 3),      # A-B
               (1, 5), (1, 6), (3, 5), (3, 6),      # B-C
               (5, 0), (5, 4), (6, 0), (6, 4)]      # C-A
def grp(b):
    return next(g for g, bs in groups.items() if b in bs)


def cross_shadow_options(p):
    """shadow on star(2) of an orbit of pair p: by the sink balance, 1 label in each of the two groups met by p,
    2 labels in the third group; two +1 and two -1."""
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


def sib_T_pattern(p, name):
    """required T between the two orbits of sib pair `name` and an orbit of cross pair p:
    'zero' if p meets the sib pair (8.1), else 'one-of' (exactly one of the two sib orbits has T = +-1)."""
    return 'zero' if set(p) & set(groups[name]) else 'one-of'


import random
random.seed(1)
assign = [(i, j, k) for (i, j) in AB for k in range(len(per['C'])) if (j, k) in BC and (k, i) in CA]
bad_assign = 0
min_opts_seen = []
for (i, j, k) in assign:
    sib = {'A': per['A'][i], 'B': per['B'][j], 'C': per['C'][k]}
    dead = False
    minopt = 10 ** 9
    for p in cross_pairs:
        reps = [((p[0], 1), (p[1], 1)), ((p[0], 1), (p[1], -1))]
        opts = cross_shadow_options(p)
        for rep in reps:
            nok = 0
            for sh in opts:
                good = True
                for name in 'ABC':
                    zs = [Z(orbit_data(name)[t], sib[name][t], rep, sh) for t in range(2)]
                    if sib_T_pattern(p, name) == 'zero':
                        if zs != [0, 0]:
                            good = False
                            break
                    else:
                        if sorted(1 if z in (1, 6) else (0 if z == 0 else 9) for z in zs) != [0, 1]:
                            good = False
                            break
                if good:
                    nok += 1
            minopt = min(minopt, nok)
            if nok == 0:
                dead = True
                break
        if dead:
            break
    if dead:
        bad_assign += 1
    min_opts_seen.append(minopt)
print('sib assignments killed by the cross-orbit rows:', bad_assign, 'of', len(assign))
print('min number of shadow options of a cross orbit (over assignments):', min(min_opts_seen), 'max', max(min_opts_seen))
