"""Exhaustive: max over all (tau, eta) (fixed-point-free involutions on X = 6 blocks x 2) of
t = dim_F7 ker Q, Q = P_tau - P_eta - 2 P_pi - I.  Used for g >= 18 - min_c t_c (notes/129).
tau is taken up to conjugacy by Aut(X, pi) = (Z/2)^6 x| S_6 (rank of Q is invariant); eta runs over all 10395."""
import itertools, time
P = 7
X = list(range(12))            # point 2d+s : block d, sign s
pi = [x ^ 1 for x in X]
def fpf_involutions(pts):
    if not pts: yield {}; return
    a = pts[0]
    for i in range(1, len(pts)):
        b = pts[i]; rest = pts[1:i] + pts[i+1:]
        for m in fpf_involutions(rest):
            m = dict(m); m[a] = b; m[b] = a; yield m
ALL = [tuple(m[x] for x in X) for m in fpf_involutions(X)]
print('fpf involutions:', len(ALL))
# group Aut(X,pi): signed permutations of blocks
G = []
for perm in itertools.permutations(range(6)):
    for flips in range(64):
        g = [0]*12
        for d in range(6):
            for s in range(2):
                g[2*d+s] = 2*perm[d] + (s ^ ((flips >> d) & 1))
        G.append(tuple(g))
def conj(t, g):
    ginv = [0]*12
    for i, gi in enumerate(g): ginv[gi] = i
    return tuple(g[t[ginv[x]]] for x in X)
seen = set(); reps = []
for t in ALL:
    if t in seen: continue
    orb = {conj(t, g) for g in G}
    seen |= orb; reps.append(t)
print('tau classes:', len(reps))
def rank_mod(M):
    M = [r[:] for r in M]; n = len(M); r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if M[i][c] % P), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = pow(M[r][c] % P, P-2, P)
        M[r] = [x*inv % P for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] % P:
                f = M[i][c]; M[i] = [(a - f*b) % P for a, b in zip(M[i], M[r])]
        r += 1
    return r
t0 = time.time(); hist = {}; best = None
for tau in reps:
    for eta in ALL:
        Q = [[(tau[w] == v) - (eta[w] == v) - 2*(pi[w] == v) - (w == v) for v in X] for w in X]
        t = 12 - rank_mod(Q)
        hist[t] = hist.get(t, 0) + 1
        if best is None or t > best[0]: best = (t, tau, eta)
print('nullity histogram (tau reps x all eta):', dict(sorted(hist.items())))
print('max nullity', best[0], 'example tau', best[1], 'eta', best[2]); print('time %.1fs' % (time.time()-t0))

# per tau-class detail: cycle type of pi u tau (alternating cycles), max nullity, counts
def cycle_type(t):
    seen = set(); lens = []
    for x in X:
        if x in seen: continue
        L = 0; y = x; use_pi = True
        while True:
            seen.add(y); L += 1
            y = pi[y] if use_pi else t[y]; use_pi = not use_pi
            if y == x and use_pi: break
        lens.append(L)
    return tuple(sorted(lens))
for tau in reps:
    h = {}
    for eta in ALL:
        Q = [[(tau[w] == v) - (eta[w] == v) - 2*(pi[w] == v) - (w == v) for v in X] for w in X]
        t = 12 - rank_mod(Q); h[t] = h.get(t, 0) + 1
    print('pi u tau cycles', cycle_type(tau), 'nullity hist', dict(sorted(h.items())))
