"""notes/103 sec. 12: class-triangle level parity certificate (degree 1 in edge maps).
Class triangle C = {1,2,3}, F = {4,5,6,7}.  Local solutions: rib maps phi_{P->R} (P in 12,13,23; R in pairs(F)),
spine maps phi_{R->Rb} for the couples (45,67), (46,57), (47,56), satisfying fact C (3 T7 pairs) and the 3 spine rules
(with the true sibling structures).  Test: for which h(phi) = eps*(t1+t2) + psi(L) and alpha is
B = sum_ribs h(phi) + sum_spines [h(phi) + h(phi^-1) + alpha*sgn(phi)] constant on local solutions?"""
import itertools, random
from collections import Counter

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
Vi = {v: n for n, v in enumerate(V)}
P = list(itertools.permutations(range(4)))
pid = {p: n for n, p in enumerate(P)}
def cmp(f, g): return pid[tuple(P[f][P[g][x]] for x in range(4))]
def inv(f): return pid[tuple(sorted(range(4), key=lambda x: P[f][x]))]
def sgn(f):
    p = P[f]; return sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2
def lin(f):
    t = V[P[f][0]]
    L = tuple(tuple((V[P[f][Vi[v]]][c] + t[c]) % 2 for c in range(2)) for v in [(0, 1), (1, 0)])
    return L, t
Ls = sorted({lin(f)[0] for f in range(24)})
Lidx = {L: n for n, L in enumerate(Ls)}
SIB = [[1 if (a != b and sum(x != y for x, y in zip(V[a], V[b])) == 1) else 0 for b in range(4)] for a in range(4)]

def fc(same):
    out = []
    for ms in itertools.combinations_with_replacement(range(24), 6):
        ok = True
        for u in range(4):
            c = [0] * 4
            for t in ms: c[P[t][u]] += 1
            if any(c[z] != (1 if same(V[u], V[z]) else 2) for z in range(4)): ok = False; break
        if ok: out.append(ms)
    return out
FCi = fc(lambda u, z: u[0] == z[0]); FCj = fc(lambda u, z: u[1] == z[0]); FCk = set(fc(lambda u, z: u[1] == z[1]))
joint = []
for A in FCi:
    for B in FCj:
        seen = set()
        for perm in set(itertools.permutations(B)):
            pairs = tuple(sorted(zip(A, perm)))
            if pairs in seen: continue
            seen.add(pairs)
            if tuple(sorted(cmp(b, inv(a)) for a, b in pairs)) in FCk: joint.append(pairs)
print('joint composite multisets:', len(joint))

Rs = [(4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
couples = [((4, 5), (6, 7)), ((4, 6), (5, 7)), ((4, 7), (5, 6))]
def perm_mat(f):
    M = [[0] * 4 for _ in range(4)]
    for x in range(4): M[x][P[f][x]] += 1
    return M
def spine_ok(phiR, s):       # phiR[P][R] maps; s = phi_{R->Rb}
    R, Rb = cur
    S = [[0] * 4 for _ in range(4)]
    for Pg in ('12', '13', '23'):
        th = cmp(inv(s), cmp(phiR[Pg][Rb], inv(phiR[Pg][R])))       # R -> P -> Rb -> R
        M = perm_mat(th)
        for x in range(4):
            for y in range(4): S[x][y] += M[x][y]
    pull = [[SIB[P[s][x]][P[s][y]] for y in range(4)] for x in range(4)]
    T = [[2 - (1 if x == y else 0) - SIB[x][y] - pull[x][y] for y in range(4)] for x in range(4)]
    return S == T

rng = random.Random(5)
samples = []
tries = 0
while len(samples) < 400 and tries < 200000:
    tries += 1
    pairs = list(rng.choice(joint)); rng.shuffle(pairs)
    asg = dict(zip(Rs, pairs))
    g = {R: rng.randrange(24) for R in Rs}
    phiR = {'12': {R: g[R] for R in Rs},
            '13': {R: cmp(g[R], inv(asg[R][0])) for R in Rs},
            '23': {R: cmp(g[R], inv(asg[R][1])) for R in Rs}}
    spines, ok = [], True
    for cur in couples:
        good = [s for s in range(24) if spine_ok(phiR, s)]
        if not good: ok = False; break
        spines.append(rng.choice(good))
    if ok:
        samples.append((phiR, spines))
print('local solutions sampled:', len(samples), 'from', tries, 'tries')

def feats(f):
    L, t = lin(f); return Lidx[L], (t[0] + t[1]) % 2
# parameters: eps (1), psi (6 values on the linear parts), alpha (1): brute force
const_params = []
for eps in (0, 1):
    for psi in itertools.product((0, 1), repeat=len(Ls)):
        for alpha in (0, 1):
            def h(f):
                l, d = feats(f); return (eps * d + psi[l]) % 2
            vals = set()
            for phiR, spines in samples:
                B = sum(h(phiR[Pg][R]) for Pg in phiR for R in Rs)
                B += sum(h(s) + h(inv(s)) + alpha * sgn(s) for s in spines)
                vals.add(B % 2)
                if len(vals) > 1: break
            if len(vals) == 1:
                const_params.append((eps, psi, alpha, vals.pop()))
print('parameter choices with constant bracket:', len(const_params))
print('  with constant 1 (certificate candidates):', [p for p in const_params if p[3] == 1][:6])

# general h (24 free values): linear system over F_2, unknowns h(0..23), alpha (24), gamma (25)
rows = {}
def add_eq(bits):
    x = bits
    while x:
        p = x.bit_length() - 1
        if p in rows: x ^= rows[p]
        else: rows[p] = x; return True
    return False
for phiR, spines in samples:
    v = 1 << 25                                             # gamma
    for Pg in phiR:
        for R in Rs: v ^= 1 << phiR[Pg][R]
    for s in spines:
        v ^= (1 << s) ^ (1 << inv(s))
        if sgn(s): v ^= 1 << 24
    add_eq(v)
print('general h: rank', len(rows), 'of 26')
# is there a solution with gamma = 1?  Solutions of M x = 0 with x_25 = 1 exist iff e_25 not in rowspace-orthogonal...
# i.e. iff no row combination equals (only gamma bit).  Check whether the vector with only bit 25 lies in the row space:
x = 1 << 25
while x:
    p = x.bit_length() - 1
    if p in rows: x ^= rows[p]
    else: break
print('gamma forced to 0 by the samples?' , x == 0)
