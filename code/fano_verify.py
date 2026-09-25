"""notes/104: independent checks of every finite step of the Fano route to L8.
(V1) edge classification: at any Kneser edge P-P' (phi = phi_{PP'} iso or not), the triples of page
     holonomies theta_R (P -> R -> P' -> P) with sum Perm(theta_R) = 2J - I - Sib_P - phi^{-1} Sib_{P'} phi
     never contain a 3-cycle; ell-profiles (|Fix|) are {4,0,0} or {2,2,0};
(V2) in profile {2,2,0} the two ell=2 holonomies induce the same transposition of the 3 partitions of Q_P,
     fixing A if phi is isometric, fixing A or pi_u (u = partition sent to A(P') ... i.e. phi(pi_u) = A')
     if not, never the third partition;
(V3) Petersen graph: 6 perfect matchings, each edge in exactly 2, two of them share exactly 1 edge;
(V4) the 30 ell-skeletons are exactly the 30 Fano planes (l=4 pencils, 2 no-line, 0 one-line);
(V5) the linear kappa system is inconsistent for all 21 surviving (C, statuses)."""
import itertools, pickle
from collections import Counter

pts = [(a, b) for a in (0, 1) for b in (0, 1)]
def add(u, v): return (u[0] ^ v[0], u[1] ^ v[1])
S4 = [dict(zip(pts, img)) for img in itertools.permutations(pts)]
def comp(f, g): return {u: f[g[u]] for u in pts}
def inv(f): return {v: u for u, v in f.items()}
parts = {'A': [{(0, 0), (1, 1)}, {(0, 1), (1, 0)}],
         'p1': [{(0, 0), (0, 1)}, {(1, 0), (1, 1)}],      # same first coordinate
         'p2': [{(0, 0), (1, 0)}, {(0, 1), (1, 1)}]}
def part_of(blocks):
    for k, b in parts.items():
        if {frozenset(x) for x in b} == {frozenset(x) for x in blocks}:
            return k
def act(f, k): return part_of([{f[u] for u in b} for b in parts[k]])
def iso(f): return act(f, 'A') == 'A'
def is3cycle(f): return sum(1 for u in pts if f[u] == u) == 1
sib = lambda u, v: u != v and (u[0] == v[0] or u[1] == v[1])

bad = 0
prof_stats = Counter()
for phi in S4:
    target = {}
    for y in pts:
        for z in pts:
            t = 2 - (y == z) - sib(y, z) - sib(phi[y], phi[z])
            target[(y, z)] = t
    u_part = next(k for k in parts if act(phi, k) == 'A')        # partition of P sent to A(P')
    for th in itertools.combinations_with_replacement(range(24), 3):
        cnt = Counter()
        for i in th:
            for y in pts:
                cnt[(y, S4[i][y])] += 1
        if any(cnt[k] != target[k] for k in target):
            continue
        hs = [S4[i] for i in th]
        if any(is3cycle(h) for h in hs):
            bad += 1
        fix = sorted((sum(1 for y in pts if h[y] == y) for h in hs), reverse=True)
        key = ('iso' if iso(phi) else 'non-iso', tuple(fix))
        if fix == [2, 2, 0]:
            tr = [h for h in hs if sum(1 for y in pts if h[y] == y) == 2]
            fixed_parts = [tuple(k for k in parts if act(h, k) == k) for h in tr]
            key = key + (fixed_parts[0] == fixed_parts[1],
                         'fixes A' if fixed_parts[0] == ('A',) else
                         ('fixes u' if fixed_parts[0] == (u_part,) else 'fixes w'))
        prof_stats[key] += 1
print('(V1) 3-cycles found:', bad)
for k, v in sorted(prof_stats.items(), key=str):
    print('   ', k, v)

# (V3)
pairs7 = list(itertools.combinations(range(7), 2))
def disjoint(a, b): return not set(a) & set(b)
W = [2, 3, 4, 5, 6]
link = list(itertools.combinations(W, 2))
pe = [(R, S) for R, S in itertools.combinations(link, 2) if disjoint(R, S)]
PM = [c for c in itertools.combinations(pe, 5) if len({v for e in c for v in e}) == 10]
edge_in = Counter(e for m in PM for e in m)
inter = Counter(len(set(a) & set(b)) for a, b in itertools.combinations(PM, 2))
print('(V3) perfect matchings:', len(PM), ' edge multiplicities:', set(edge_in.values()), ' pairwise intersections:', dict(inter))

# (V4)
sols = pickle.load(open('../data/ell_skeletons.pkl', 'rb'))
tris = [t for t in itertools.combinations(range(21), 3)
        if all(disjoint(pairs7[a], pairs7[b]) for a, b in itertools.combinations(t, 2))]
fanos = set()
for T in itertools.combinations(itertools.combinations(range(7), 3), 7):
    if all(len(set(a) & set(b)) == 1 for a, b in itertools.combinations(T, 2)):
        fanos.add(T)
def fano_ell(T):
    lines = [set(L) for L in T]
    out = {}
    for n, t in enumerate(tris):
        Ps = [pairs7[a] for a in t]
        v = next(c for c in range(7) if all(c not in P for P in Ps))
        k = sum(1 for P in Ps if set(P) | {v} in lines)
        out[n] = {3: 4, 0: 2, 1: 0}[k]
    return out
fano_skels = [fano_ell(T) for T in fanos]
match = sum(1 for s in sols if any(all(s[n] == f[n] for n in range(105)) for f in fano_skels))
print('(V4) Fano planes:', len(fanos), ' skeletons:', len(sols), ' skeletons equal to a Fano skeleton:', match)

# (V5)
from kappa_linear_system import system, consistent
surv = pickle.load(open('../data/fano_bc_survivors.pkl', 'rb'))
res = Counter()
for C, st in surv:
    nu = {e for e, s in st.items() if s == 1}
    eqs, var = system(nu)
    res[consistent(eqs)[0]] += 1
print('(V5) survivors:', len(surv), ' consistency of the kappa system:', dict(res))

# (V1b) at an isometric edge every page holonomy fixes the partition A (=> triangle rule and rule (i))
viol = 0
for phi in S4:
    if not iso(phi):
        continue
    target = {(y, z): 2 - (y == z) - sib(y, z) - sib(phi[y], phi[z]) for y in pts for z in pts}
    for th in itertools.combinations_with_replacement(range(24), 3):
        cnt = Counter()
        for i in th:
            for y in pts:
                cnt[(y, S4[i][y])] += 1
        if all(cnt[k] == target[k] for k in target):
            viol += sum(1 for i in th if act(S4[i], 'A') != 'A')
print('(V1b) page holonomies moving A at isometric edges:', viol)
