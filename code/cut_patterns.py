"""notes/103 §13: the cut case of L8 (no all-non-isometric triangle <=> the non-isometric edges form a cut
delta(V0) of K(7,2), since H^1 = 0).  Enumerate the cuts V0 (up to complement and S_7) that pass the
combinatorial necessary conditions proved so far:
 (a) local §6: for each class i, at most 2 of the 6 pairs containing i have all 10 Kneser edges across;
 (b) local L7: for each class triple T, the 3 pairs inside T and the 6 pairs inside F = [7] - T are not
     all on one side;
 (d) (Z_A): at each pair P, the across-edges at P, seen as a graph on the 5 classes outside P, admit an
     orientation (R -> kappa(P->R) in R) with all in-degrees even  <=>  every connected component of that
     graph has an even number of edges."""
import itertools
import numpy as np

pairs = list(itertools.combinations(range(7), 2))
pid = {P: n for n, P in enumerate(pairs)}
nbrs = [[pid[R] for R in pairs if not set(R) & set(P)] for P in pairs]

def even_components(P, sub):
    """sub: list of pairs R (edges of K5 on the classes outside P); True iff each component has even size"""
    parent = {}
    def f(a):
        while parent.setdefault(a, a) != a:
            a = parent[a]
        return a
    for (u, v) in sub:
        parent[f(u)] = f(v)
    cnt = {}
    for (u, v) in sub:
        r = f(u)
        cnt[r] = cnt.get(r, 0) + 1
    return all(c % 2 == 0 for c in cnt.values())

# lookup tables per P: 10-bit across-pattern -> ok for (d)
tab = []
for Pn, P in enumerate(pairs):
    t = np.zeros(1024, dtype=bool)
    for s in range(1024):
        sub = [pairs[nbrs[Pn][b]] for b in range(10) if s >> b & 1]
        t[s] = even_components(P, sub)
    tab.append(t)

masks = np.arange(1 << 20, dtype=np.uint32) << 1 | 1          # V0 contains pair 0 (complement symmetry)
masks = masks[masks != (1 << 21) - 1]                        # V1 nonempty
side = [(masks >> n) & 1 for n in range(21)]
ok = np.ones(len(masks), dtype=bool)
for Pn in range(21):
    idx = np.zeros(len(masks), dtype=np.uint32)
    for b, Rn in enumerate(nbrs[Pn]):
        idx |= (side[Rn] ^ side[Pn]) << b
    ok &= tab[Pn][idx]
print('cuts passing (d):', int(ok.sum()))
# (a): for each class i, number of pairs containing i with all 10 edges across <= 2
for i in range(7):
    cnt = np.zeros(len(masks), dtype=np.int32)
    for P in pairs:
        if i in P:
            Pn = pid[P]
            allx = np.ones(len(masks), dtype=bool)
            for Rn in nbrs[Pn]:
                allx &= (side[Rn] != side[Pn])
            cnt += allx
    ok &= cnt <= 2
print('cuts passing (d)+(a):', int(ok.sum()))
for T in itertools.combinations(range(7), 3):
    F = [c for c in range(7) if c not in T]
    group = [pid[P] for P in itertools.combinations(T, 2)] + [pid[P] for P in itertools.combinations(F, 2)]
    s = sum(side[n].astype(np.int32) for n in group)
    ok &= (s != 0) & (s != len(group))
print('cuts passing (d)+(a)+(b):', int(ok.sum()))

# orbits under S_7
good = masks[ok]
perm_maps = []
for g in itertools.permutations(range(7)):
    perm_maps.append([pid[tuple(sorted((g[a], g[b])))] for (a, b) in pairs])
def canon(m):
    best = None
    for pm in perm_maps:
        img = 0
        for n in range(21):
            if m >> n & 1:
                img |= 1 << pm[n]
        c = min(img, ((1 << 21) - 1) ^ img)
        if best is None or c < best:
            best = c
    return best
reps = {}
for m in good.tolist():
    c = canon(m)
    reps.setdefault(c, 0)
    reps[c] += 1
print('S7-orbits:', len(reps))
for c, n in sorted(reps.items()):
    V0 = [pairs[k] for k in range(21) if c >> k & 1]
    print(len(V0), n, V0)
