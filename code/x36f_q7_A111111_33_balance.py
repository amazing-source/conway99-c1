"""C2 free-star cube A111111 (mu = sigma), type (3,3): G(L_c) = two (6,6)-components.
Test (C1's method, notes/126 sec. 3 bis): can a 7-torsion vector supported on ONE component be balanced?
far(n,n') = #far common neighbours = (1 if n~n' else 2) - [same layer] - #common G-neighbours.
Each far vertex meets a component in exactly 3 points (equilibrium |C|/6); admissible triple: not 3 in one layer,
no pair with far(.,.) = 0, at most one G-edge.  Balanced Y (L_G Y = 0 mod 7, layer sums 0) needs every admissible
triple actually used to have Y-sum 0; necessary: each pair {n,n'} lies in >= far(n,n') zero-sum admissible triples."""
import itertools
P = 7
blocks = [2, 3, 4]
Xp = [(d, s) for d in blocks for s in (1, -1)]
pi = {(d, s): (d, -s) for (d, s) in Xp}
eta = {}
for a, b in [((2, -1), (3, 1)), ((3, -1), (4, 1)), ((4, -1), (2, 1))]:
    eta[a] = b; eta[b] = a
h = {w: pi[eta[w]] for w in Xp}          # U -> Ubar holonomy
tau_u = pi                                 # A111111: mu = sigma (U-mates are sisters)
tau_ub = {w: pi[tau_u[pi[w]]] for w in Xp}
V = [('X', w) for w in Xp] + [('U', w) for w in Xp] + [('B', w) for w in Xp]
idx = {v: i for i, v in enumerate(V)}; n = len(V)
layer = [0]*6 + [1]*6 + [2]*6
adj = [[0]*n for _ in range(n)]
def e(a, b): adj[idx[a]][idx[b]] = adj[idx[b]][idx[a]] = 1
for w in Xp:
    e(('X', w), ('X', pi[w])); e(('U', w), ('U', tau_u[w])); e(('B', w), ('B', tau_ub[w]))
    e(('X', w), ('U', w)); e(('X', w), ('B', w)); e(('U', w), ('B', h[w]))
assert all(sum(r) == 3 for r in adj)
def far(a, b):
    cn = sum(1 for k in range(n) if adj[a][k] and adj[b][k])
    return (1 if adj[a][b] else 2) - (1 if layer[a] == layer[b] else 0) - cn
FAR = [[far(a, b) if a != b else None for b in range(n)] for a in range(n)]
assert all(FAR[a][b] >= 0 for a in range(n) for b in range(n) if a != b)
L = [[(3 if i == j else 0) - adj[i][j] for j in range(n)] for i in range(n)]
def nullspace(M):
    M = [[v % P for v in r] for r in M]; rr, cols = len(M), len(M[0]); r = 0; piv = []
    for c in range(cols):
        pr = next((i for i in range(r, rr) if M[i][c]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; inv = pow(M[r][c], P-2, P); M[r] = [v*inv % P for v in M[r]]
        for i in range(rr):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f*b) % P for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    B = []
    for fc in [c for c in range(cols) if c not in piv]:
        v = [0]*cols; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-M[i][fc]) % P
        B.append(v)
    return B
rows = [r[:] for r in L] + [[1 if layer[j] == p else 0 for j in range(n)] for p in range(3)]
E = nullspace(rows)
sig = {i: idx[('X', pi[V[i][1]])] if V[i][0] == 'X' else idx[('B' if V[i][0] == 'U' else 'U', pi[V[i][1]])] for i in range(n)}
odd = [v for v in E]  # report parity of basis under sigma
print('dim E_C =', len(E))
triples = []
for a, b, c in itertools.combinations(range(n), 3):
    if layer[a] == layer[b] == layer[c]: continue
    if min(FAR[a][b], FAR[a][c], FAR[b][c]) == 0: continue
    if sum(adj[x][y] for x, y in ((a, b), (a, c), (b, c))) > 1: continue
    triples.append((a, b, c))
print('admissible triples:', len(triples), ' pairs with far>0:', sum(1 for a, b in itertools.combinations(range(n), 2) if FAR[a][b] > 0))
best = None; passing = 0; tested = 0
for coeffs in itertools.product(range(P), repeat=len(E)):
    if not any(coeffs) or next(c for c in coeffs if c) != 1: continue
    Y = [sum(c*v[i] for c, v in zip(coeffs, E)) % P for i in range(n)]
    tested += 1
    zs = [t for t in triples if (Y[t[0]] + Y[t[1]] + Y[t[2]]) % P == 0]
    cov = {}
    for t in zs:
        for x, y in ((t[0], t[1]), (t[0], t[2]), (t[1], t[2])): cov[(x, y)] = cov.get((x, y), 0) + 1
    bad = sum(1 for x, y in itertools.combinations(range(n), 2) if FAR[x][y] > cov.get((x, y), 0))
    oddY = all((Y[sig[i]] + Y[i]) % P == 0 for i in range(n))
    if bad == 0: passing += 1
    if best is None or bad < best[0]: best = (bad, oddY, Y)
print('projective Y tested:', tested, ' passing coverage:', passing, ' min failing pairs:', best[0], ' (that Y sigma-odd?', best[1], ')')
