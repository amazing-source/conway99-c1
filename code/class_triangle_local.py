"""notes/103 sec. 10: local structure around a class triangle {i,j,k} at a Hamming point.
Q_ij = (s_i, s_j), Q_ik = (s_i, s_k), Q_jk = (s_j, s_k).  For the 6 class pairs R of F = [7] minus {i,j,k}:
a_R = phi_{ik,R}^{-1} o phi_{ij,R} : Q_ij -> Q_ik,  b_R = phi_{jk,R}^{-1} o phi_{ij,R} : Q_ij -> Q_jk,
c_R = b_R o a_R^{-1} : Q_ik -> Q_jk.
Fact C for (ij,ik), (ij,jk), (ik,jk) (shared class i, j, k).  Books: for each complementary couple {R, Rb} (spine edge
R-Rb, pages ij, ik, jk), with alpha = a_R^{-1} a_Rb, beta = b_R^{-1} b_Rb, the three page holonomies are
theta, alpha theta, beta theta (conjugated to Q_ij), and the spine transport rule demands
Perm(theta) + Perm(alpha theta) + Perm(beta theta) = 2J - I - C1 - C2 for some 4-cycles C1, C2 (C1 = C2: isometric spine).
Question: does any local configuration exist?"""
import itertools
from collections import Counter

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
P = list(itertools.permutations(range(4)))          # permutation p: index -> index (maps as index tuples)
pidx = {p: n for n, p in enumerate(P)}
comp = [[pidx[tuple(P[f][P[g][x]] for x in range(4))] for g in range(24)] for f in range(24)]   # f o g
inv = [pidx[tuple(sorted(range(4), key=lambda x: P[f][x]))] for f in range(24)]


def fc_solutions(same):
    """multisets (sorted 6-tuples) of maps m with: for each u, images hit z with same(u,z) once, others twice"""
    out = []
    for ms in itertools.combinations_with_replacement(range(24), 6):
        ok = True
        for u in range(4):
            c = [0] * 4
            for t in ms:
                c[P[t][u]] += 1
            if any(c[z] != (1 if same(V[u], V[z]) else 2) for z in range(4)):
                ok = False; break
        if ok:
            out.append(ms)
    return out


FCi = fc_solutions(lambda u, z: u[0] == z[0])      # ij -> ik, class i
FCj = fc_solutions(lambda u, z: u[1] == z[0])      # ij -> jk, class j
FCk = set(fc_solutions(lambda u, z: u[1] == z[1])) # ik -> jk, class k
print('fact C solutions:', len(FCi), len(FCj), len(FCk))

# valid books: (alpha, beta) with exists theta, C1, C2
def pm(f):
    M = [[0] * 4 for _ in range(4)]
    for x in range(4):
        M[x][P[f][x]] += 1
    return M
matchings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
def mat_of_matching(m):
    M = [[0] * 4 for _ in range(4)]
    for a, b in m:
        M[a][b] = M[b][a] = 1
    return M
Mm = [mat_of_matching(m) for m in matchings]
targets = set()
for a in range(3):
    for b in range(3):
        for c in range(3):
            if b == a or c == a:
                continue
            # C1 = Ma + Mb, C2 = Ma + Mc ; target = 2J - I - C1 - C2
            T = tuple(tuple(2 - (1 if x == y else 0) - Mm[a][x][y] - Mm[b][x][y] - Mm[a][x][y] - Mm[c][x][y]
                            for y in range(4)) for x in range(4))
            targets.add(T)
VB = set()
for th in range(24):
    for al in range(24):
        for be in range(24):
            S = tuple(tuple(pm(th)[x][y] + pm(comp[al][th])[x][y] + pm(comp[be][th])[x][y] for y in range(4)) for x in range(4))
            if S in targets:
                VB.add((al, be))
VB2 = {(a, b) for (a, b) in VB if (inv[a], inv[b]) in VB}
print('valid (alpha,beta) pairs:', len(VB), ' symmetric under inversion:', len(VB2))

pairings = [((0, 1), (2, 3), (4, 5)), ((0, 1), (2, 4), (3, 5)), ((0, 1), (2, 5), (3, 4)),
            ((0, 2), (1, 3), (4, 5)), ((0, 2), (1, 4), (3, 5)), ((0, 2), (1, 5), (3, 4)),
            ((0, 3), (1, 2), (4, 5)), ((0, 3), (1, 4), (2, 5)), ((0, 3), (1, 5), (2, 4)),
            ((0, 4), (1, 2), (3, 5)), ((0, 4), (1, 3), (2, 5)), ((0, 4), (1, 5), (2, 3)),
            ((0, 5), (1, 2), (3, 4)), ((0, 5), (1, 3), (2, 4)), ((0, 5), (1, 4), (2, 3))]
joint, withbook = 0, 0
examples = []
for A in FCi:
    for B in FCj:
        seen = set()
        for perm in set(itertools.permutations(B)):
            pairs = tuple(sorted(zip(A, perm)))
            if pairs in seen:
                continue
            seen.add(pairs)
            C = tuple(sorted(comp[b][inv[a]] for a, b in pairs))
            if C not in FCk:
                continue
            joint += 1
            for pr in pairings:
                if all((comp[inv[pairs[s][0]]][pairs[t][0]], comp[inv[pairs[s][1]]][pairs[t][1]]) in VB2 for s, t in pr):
                    withbook += 1
                    if len(examples) < 3:
                        examples.append((pairs, pr))
                    break
print('joint fact-C multisets (all three classes):', joint, ' ; with a valid book pairing:', withbook)
for e in examples:
    print('  example', e)
