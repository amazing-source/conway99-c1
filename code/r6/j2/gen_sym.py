# Pattern orbits + star(0) symmetry files for the 2|5 cut cells.
#   R5 : a = +-1 on the 20 cut labels, R^T a = 0 (no V).   Group: S5 on X, swap 0<->1, flips of all 7 coordinates, h -> -h.
#   J2 : a = +-1 on the cut, +2 on V=(5,6,+).               Group of j2_orbits.py.
# For each orbit representative: stabiliser elements with perm[0] = 0 (they map star(0) to itself), written as permutations
# of the 12 star(0) labels (0 = e0+e1, 1 = e0-e1, 2+2(x-2)+(s<0) = e0 + s e_x).
import itertools, json, sys, numpy as np
cells = [(i, j) for i in range(7) for j in range(i + 1, 7)]
labels = [(c, s) for c in cells for s in (1, -1)]
idx = {L: k for k, L in enumerate(labels)}
R = np.zeros((42, 7), dtype=int)
for k, ((i, j), s) in enumerate(labels): R[k, i] = 1; R[k, j] = s
cut = [idx[((i, x), s)] for i in (0, 1) for x in range(2, 7) for s in (1, -1)]
def lab_image(k, perm, sg):
    v = np.zeros(7, dtype=int)
    for c in range(7):
        if R[k, c]: v[perm[c]] += sg[c] * R[k, c]
    nz = np.nonzero(v)[0]; f = 1 if v[nz[0]] > 0 else -1
    return idx[((nz[0], nz[1]), int(f * v[nz[1]]))], f
def act(g, a):
    perm, sg, hs = g; b = np.zeros(42, dtype=int)
    for k in range(42):
        if a[k] == 0: continue
        k2, f = lab_image(k, perm, sg); b[k2] = hs * f * a[k]
    return tuple(b)
def star0_local(k):
    (i, j), s = labels[k]; assert i == 0
    return 0 if (j == 1 and s == 1) else 1 if j == 1 else 2 + 2 * (j - 2) + (0 if s == 1 else 1)
def run(kind):
    if kind == 'R5':
        G = []
        for sw in (0, 1):
            for pX in itertools.permutations(range(2, 7)):
                for fl in itertools.product((1, -1), repeat=7):
                    for hs in (1, -1):
                        perm = ([1, 0] if sw else [0, 1]) + list(pX); G.append((perm, list(fl), hs))
        pats = []
        for signs in itertools.product((1, -1), repeat=20):
            a = np.zeros(42, dtype=int)
            for k, s in zip(cut, signs): a[k] = s
            if np.any(R.T @ a): continue
            pats.append(tuple(a))
    else:
        G = []
        for sw01 in (0, 1):
            for p234 in itertools.permutations((2, 3, 4)):
                for sw56 in (0, 1):
                    for fl in itertools.product((1, -1), repeat=5):
                        for f56 in (0, 1):
                            perm = ([1, 0] if sw01 else [0, 1]) + list(p234) + ([6, 5] if sw56 else [5, 6])
                            G.append((perm, list(fl) + ([-1, -1] if f56 else [1, 1]), -1 if f56 else 1))
        pats = [tuple(o['a']) for o in json.load(open('j2_orbits.json'))]
        # expand to all patterns (orbits recomputed below)
        allp = set()
        for a in pats:
            for g in G: allp.add(act(g, np.array(a)))
        pats = sorted(allp)
    Pset = set(pats); seen = set(); orbs = []
    for a in pats:
        if a in seen: continue
        orb = set(); stab = []
        for g in G:
            b = act(g, np.array(a)); orb.add(b)
            if b == a: stab.append(g)
        seen |= orb; orbs.append((a, len(orb), stab))
    print(kind, 'group', len(G), 'patterns', len(pats), 'orbits', len(orbs))
    out = []
    for n, (a, osz, stab) in enumerate(orbs):
        a = np.array(a)
        typ = ''.join('S' if a[idx[((0, x), 1)]] == a[idx[((0, x), -1)]] else 'X' for x in range(2, 7)) + '/' + \
              ''.join('S' if a[idx[((1, x), 1)]] == a[idx[((1, x), -1)]] else 'X' for x in range(2, 7))
        perms = set()
        for (perm, sg, hs) in stab:
            if perm[0] != 0: continue
            pm = [0] * 12
            for k in range(42):
                (i, j), s = labels[k]
                if i != 0: continue
                k2, f = lab_image(k, perm, sg)
                pm[star0_local(k)] = star0_local(k2)
            perms.add(tuple(pm))
        fn = '%s_sym_%d.txt' % (kind, n)
        with open(fn, 'w') as f:
            for pm in sorted(perms): f.write(' '.join(map(str, pm)) + '\n')
        print('  orbit %d: size %d  stabiliser %d  star0-fixing perms %d  types %s' % (n, osz, len(stab), len(perms), typ))
        out.append({'a': a.tolist(), 'size': osz, 'stab': len(stab), 'nperm': len(perms), 'types': typ, 'symfile': fn})
    json.dump(out, open('%s_orbits.json' % kind, 'w'))
run(sys.argv[1])
