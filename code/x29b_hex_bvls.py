# Check the hand-derived 6-cycle bookkeeping on BvLS (srg(243,22,1,2)): count prisms P and induced hexagons H directly,
# compare with the general formula H = c6 - L - S - SSo - SSa - SL - SSL derived by hand for srg(v,k,1,2).
import itertools, numpy as np
exec(open('code/x29_bvls_triangle.py').read().split('# a triangle through 0')[0])
v, k = 243, 22
nb = [set(np.nonzero(A[i])[0]) for i in range(v)]
# triangles
tris = set()
for a in range(v):
    for b in nb[a]:
        if b > a:
            c = (nb[a] & nb[b]).pop()
            tris.add(frozenset((a, b, c)))
tris = list(tris); t = len(tris)
# prisms: pairs of disjoint triangles with a perfect matching of 3 edges
P = 0
tri_of_v = {i: [T for T in tris if i in T] for i in range(v)}
for T in tris:
    a0 = min(T)
    others = sorted(T - {a0})
    for x in nb[a0]:
        if x in T: continue
        for T2 in tri_of_v[x]:
            if T2 & T or a0 in T2: continue
            # count edges between T and T2
            e = sum(1 for p in T for q in T2 if q in nb[p])
            if e == 3: P += 1
P //= 2 * 3  # each prism found from both triangles' min vertex? recount below instead
# direct prism count: for each unordered pair of disjoint triangles with 3 rungs
P2 = 0
for T in tris:
    cand = set()
    for p in T:
        for q in nb[p]:
            if q not in T:
                cand.update(tri_of_v[q])
    for T2 in cand:
        if T2 & T: continue
        e = sum(1 for p in T for q in T2 if q in nb[p])
        if e == 3: P2 += 1
P2 //= 2
# induced hexagons: count via antipodal non-adjacent pairs (a,b): pairs of internally disjoint 3-paths with no chords
def induced_hex_count():
    tot = 0
    for a in range(v):
        for b in range(a + 1, v):
            if b in nb[a]: continue
            paths = [(c, d) for c in nb[a] for d in nb[c] & nb[b] if d != a and c != b]
            for (c1, d1), (c2, d2) in itertools.combinations(paths, 2):
                S6 = [a, c1, d1, b, d2, c2]
                if len(set(S6)) < 6: continue
                edges = sum(1 for i, j in itertools.combinations(S6, 2) if j in nb[i])
                if edges == 6: tot += 1
    return tot // 3
H = induced_hex_count()
# formula
Nna = v * (v - k - 1) // 2; Na = v * k // 2
c6 = (Nna * (2*k*k - 7*k + 5) + Na * (k - 2) * (k - 3) // 2) // 3
long_tot = Na * (k - 2) * (k - 3) // 2
SSL = 3 * P2
SSo = (3 * (k - 2) * t - 6 * P2) // 2
SSa = v * (k // 2) * (k // 2 - 1) // 2 * 4
SL = v * (k // 2) * (k - 2) - 6 * P2
L = long_tot - SL - SSL
W = (k - 2) * (2 * k - 5)
S = 3 * t * W - 2 * SSa - 2 * SSo - SL - 2 * SSL
Hf = c6 - L - S - SSo - SSa - SL - SSL
print('triangles', t, ' prisms P =', P2, ' induced hexagons H =', H, ' formula H =', Hf)
