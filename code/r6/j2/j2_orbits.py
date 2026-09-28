# J2 pattern orbits under the symmetries fixing the setup: cut {0,1}|X, V = (5,6,+) with a_V = +2.
# Group: swap 0<->1, permutations of {2,3,4}, swap 5<->6, sign flips of coordinates 0..4, and (flip 5 & 6 together with h -> -h).
import itertools, json, numpy as np
pat = json.load(open('j2_patterns.json'))
cells = [(i, j) for i in range(7) for j in range(i + 1, 7)]
labels = [(c, s) for c in cells for s in (1, -1)]
idx = {L: k for k, L in enumerate(labels)}
R = np.zeros((42, 7), dtype=int)
for k, ((i, j), s) in enumerate(labels): R[k, i] = 1; R[k, j] = s
def act(perm, sg, hsign, a):
    # coordinate map e_c -> sg[c] e_{perm[c]}; new h(g r) = hsign * h(r)
    b = np.zeros(42, dtype=int)
    for k in range(42):
        v = np.zeros(7, dtype=int)
        for c in range(7):
            if R[k, c]: v[perm[c]] += sg[c] * R[k, c]
        nz = np.nonzero(v)[0]; f = 1 if v[nz[0]] > 0 else -1
        v2 = f * v
        (i, j) = nz[0], nz[1]; key = ((i, j), int(v2[j]))
        b[idx[key]] = hsign * f * a[k]
    return b
G = []
for sw01 in (0, 1):
    for p234 in itertools.permutations((2, 3, 4)):
        for sw56 in (0, 1):
            for fl in itertools.product((1, -1), repeat=5):
                for f56 in (0, 1):
                    perm = [1, 0] if sw01 else [0, 1]
                    perm += list(p234) + ([6, 5] if sw56 else [5, 6])
                    sg = list(fl) + ([-1, -1] if f56 else [1, 1])
                    G.append((perm, sg, -1 if f56 else 1))
def full(signs):
    a = np.zeros(42, dtype=int)
    for k, s in zip(pat['cut'], signs): a[k] = s
    a[pat['V']] = 2; return a
P = [tuple(full(s)) for s in pat['patterns']]
Pset = set(P)
seen = set(); orbits = []
for a in P:
    if a in seen: continue
    orb = set(); stab = 0
    for g in G:
        b = tuple(act(g[0], g[1], g[2], np.array(a)))
        assert b in Pset, 'group does not preserve the pattern set'
        orb.add(b)
        if b == a: stab += 1
    seen |= orb; orbits.append((a, len(orb), stab))
print('group order', len(G), ' patterns', len(P), ' orbits', len(orbits))
out = []
for a, n, st in orbits:
    a = np.array(a)
    typ = []
    for i in (0, 1):
        t = ''
        for x in range(2, 7):
            u, w = a[idx[((i, x), 1)]], a[idx[((i, x), -1)]]
            t += ('S' if u == w else 'X')
        typ.append(t)
    print('orbit size %3d  stabilizer %3d  cell types star0=%s star1=%s' % (n, st, typ[0], typ[1]))
    out.append({'a': a.tolist(), 'size': n, 'stab': st})
json.dump(out, open('j2_orbits.json', 'w'))
