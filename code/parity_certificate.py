"""notes/103 sec. 11: degree-2 parity certificate for L8 (Hamming point).
Sum fact C over the 105 T7 pairs with f in F (constant parity c_f per pair) and regroup by (X, m): each group is
Phi(a) = sum_{n<n'} f(c_{n n'}) over the 4 maps a_n = phi_{X,{m,n}}.  If for some h, d:
   Phi(a) + sum_n h(a_n) = d   for every Z-valid 4-tuple (mu(w, a_m^0) = 2 for all w in Q_X), all 5 order patterns,
then 105 c_f = 105 d + (h terms, which cancel globally), so c_f = d.  A solution with c_f != d proves L8."""
import itertools
import numpy as np

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
Vi = {v: n for n, v in enumerate(V)}
P = list(itertools.permutations(range(4)))
pid = {p: n for n, p in enumerate(P)}
def cmp(f, g): return pid[tuple(P[f][P[g][x]] for x in range(4))]          # f o g
def inv(f): return pid[tuple(sorted(range(4), key=lambda x: P[f][x]))]
SW = pid[tuple(Vi[(v[1], v[0])] for v in V)]                                # coordinate swap

# --- fact C solutions (shared class = first coordinate on both sides) and the space F ---
sols = []
for ms in itertools.combinations_with_replacement(range(24), 6):
    ok = True
    for u in range(4):
        c = [0] * 4
        for t in ms:
            c[P[t][u]] += 1
        if any(c[z] != (1 if V[u][0] == V[z][0] else 2) for z in range(4)):
            ok = False; break
    if ok:
        v = np.zeros(24, dtype=np.int64)
        for t in ms: v[t] += 1
        sols.append(v % 2)
S = np.array(sols)
def nullspace(M):
    M = M.copy() % 2; n = M.shape[1]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, M.shape[0]) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] = (M[i] + M[r]) % 2
        piv.append(c); r += 1
    out = []
    for fc in [c for c in range(n) if c not in piv]:
        v = np.zeros(n, dtype=np.int64); v[fc] = 1
        for i, pc in enumerate(piv):
            if M[i, fc]: v[pc] = 1
        out.append(v)
    return out
Fb = nullspace((S[1:] + S[0]) % 2)                  # basis of F (constant parity functions)
cF = [int(f @ S[0]) % 2 for f in Fb]
nF = len(Fb)
print('dim F =', nF, ' constants:', cF)

# --- equations: unknowns = lambda (nF), h (24), d (1) ---
NV = nF + 24 + 1
rows = {}                                            # pivot -> row (python int bitmask)
def add_eq(bits):
    x = bits
    while x:
        p = x.bit_length() - 1
        if p in rows:
            x ^= rows[p]
        else:
            rows[p] = x; return True
    return False
m_rank = None
cnt = 0
for r in range(5):                                   # m's rank among the 5 classes {m} u N
    first = [s >= r for s in range(4)]               # for n_s: m < n_s  <=>  m first in R_{n_s} coords
    def mcoord(img_idx, s):
        v = V[img_idx]; return v[0] if first[s] else v[1]
    def to_mfirst(s):                                # sigma_s : canonical -> m-first
        return None if first[s] else SW
    for tup in itertools.product(range(24), repeat=4):
        ok = True
        for w in range(4):
            if sum(1 for s in range(4) if mcoord(P[tup[s]][w], s) == 0) != 2:
                ok = False; break
        if not ok:
            continue
        cnt += 1
        bits = 1 << (NV - 1)                          # d
        for s in range(4):
            bits ^= 1 << (nF + tup[s])                # h(a_s)
        fsum = [0] * nF
        for s in range(4):
            for t in range(s + 1, 4):
                c = cmp(tup[t], inv(tup[s]))          # a_t o a_s^{-1} : R_s -> R_t (canonical coords)
                if not first[s]: c = cmp(c, SW)       # precompose with sigma_s^{-1} = SW
                if not first[t]: c = cmp(SW, c)
                for i in range(nF):
                    fsum[i] ^= int(Fb[i][c])
        for i in range(nF):
            if fsum[i]: bits ^= 1 << i
        add_eq(bits)
print('Z-valid 4-tuples (all patterns):', cnt, ' ; rank of the equation system:', len(rows), 'of', NV)
# solve: find solutions of the homogeneous system, check whether c_lambda + d can be 1
basis_rows = list(rows.values())
M = np.array([[(b >> j) & 1 for j in range(NV)] for b in basis_rows], dtype=np.int64)
sol = nullspace(M)
print('solution space dimension:', len(sol))
good = [v for v in sol if (sum(cF[i] * v[i] for i in range(nF)) + v[NV - 1]) % 2 == 1]
print('solutions with c_f + d = 1 (a certificate for L8):', 'YES' if good else 'none',
      '' if not good else [int(x) for x in good[0]])
