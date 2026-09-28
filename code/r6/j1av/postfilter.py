# Post-filter of the J1a (v) run records (survivors + marginal kills), exact where it matters.
# Filters (all hand-derived necessary conditions, notes/151 s7-8):
#   T3o: 21 P_3 restricted to U:  12I - 3G - RR^T  must be PSD            (odd 3-eigenprojector, 21 P3 = 12I + 3T - RR^T)
#   T3e: 105 P3+ restricted to U: 60I + 15G - 3|R||R|^T - 4J must be PSD  (even 3-eigenprojector)
#   R7 : label W (group j), k != j: #(G_star nbrs of W in group k) + [pos rep of W shares an inner vertex with v_k] <= 1
#   R7': label W (group j):         #(G_star nbrs of W in group j) + [pos rep shares an inner vertex with v_j]    <= 2
#   C4 : labels L, M of one group with A-roots on opposite c-sides: #(common G_star nbrs) + [A-roots share an inner] <= 1
import struct, sys, numpy as np
from collections import Counter
recfile = sys.argv[1] if len(sys.argv) > 1 else 'full_records.txt'
raw = open('base.bin', 'rb').read(); nb = struct.unpack('<i', raw[:4])[0]
bases = [struct.unpack('<6b12b', raw[4 + 18 * i: 22 + 18 * i]) for i in range(nb)]
perms = []
def gen(arr, k):
    if k == 6: perms.append(arr[:]); return
    for i in range(k, 6):
        arr[k], arr[i] = arr[i], arr[k]; gen(arr, k + 1); arr[k], arr[i] = arr[i], arr[k]
gen(list(range(6)), 0)
match6 = []
for j in range(1, 6):
    rest = [x for x in range(1, 6) if x != j]
    for t in [((rest[0], rest[1]), (rest[2], rest[3])), ((rest[0], rest[2]), (rest[1], rest[3])), ((rest[0], rest[3]), (rest[1], rest[2]))]:
        match6.append([(0, j), t[0], t[1]])
VIN = {0: {(1, 1), (2, -1)}, 1: {(2, 1), (3, -1)}, 2: {(3, 1), (1, -1)}}   # inner vertices (block, sign) of v1, v2, v3
def config(b, q, p1, p2):
    rec = bases[b]; a, g = rec[:6], rec[6:]
    alpha = [a[L // 2] for L in range(12)]
    Ap = [L for L in range(12) if alpha[L] == 1]; Am = [L for L in range(12) if alpha[L] == -1]
    ed = [(Ap[i], Am[perms[q][i]]) for i in range(6)] + [(Ap[x], Ap[y]) for x, y in match6[p1]] + [(Am[x], Am[y]) for x, y in match6[p2]]
    return alpha, list(g), ed
def mats(alpha, g, ed):
    R = np.zeros((15, 7))
    for L in range(12):
        K = L // 2 + 1; s = 1 if L % 2 == 0 else -1
        R[L, 0] = alpha[L]; R[L, K] = alpha[L] * s
    R[12, 1], R[12, 2], R[13, 2], R[13, 3], R[14, 3], R[14, 1] = 1, -1, 1, -1, 1, -1
    G = np.zeros((15, 15))
    for L in range(12): G[L, 12 + g[L]] = G[12 + g[L], L] = 1
    for x, y in [(12, 13), (13, 14), (12, 14)]: G[x, y] = G[y, x] = 1
    for x, y in ed: G[x, y] = G[y, x] = 1
    return R, G
def lam_mu_ok(alpha, g, ed):
    nbr = {L: [] for L in range(12)}
    for x, y in ed: nbr[x].append(y); nbr[y].append(x)
    def pos_inner(L):   # (block, sign) of the K-inner vertex of the positive rep alpha(e_c + s e_K)
        K = L // 2 + 1; s = 1 if L % 2 == 0 else -1; return (K, alpha[L] * s)
    def neg_inner(L):
        K, t = pos_inner(L); return (K, -t)
    for W in range(12):
        j = g[W]
        for k in range(3):
            n_in_k = sum(1 for X in nbr[W] if g[X] == k)
            sh = 1 if pos_inner(W) in VIN[k] else 0
            if k != j and n_in_k + sh > 1: return 'R7'
            if k == j and n_in_k + sh > 2: return "R7'"
    for L in range(12):
        for M in range(L + 1, 12):
            if g[L] != g[M] or alpha[L] == alpha[M]: continue      # same group, A-roots on opposite c-sides
            common = len(set(nbr[L]) & set(nbr[M]))
            sh = 1 if neg_inner(L) == neg_inner(M) else 0
            if common + sh > 1: return 'C4'
    return None
recs = [tuple(map(int, line.split())) for line in open(recfile)]
print('records:', len(recs), Counter(r[4] for r in recs))
out = Counter(); keep = []
I = np.eye(15); J = np.ones((15, 15))
for (b, q, p1, p2, kind) in recs:
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed); Ra = np.abs(R)
    w3o = np.linalg.eigvalsh(12 * I - 3 * G - R @ R.T)[0]
    w3e = np.linalg.eigvalsh(60 * I + 15 * G - 3 * Ra @ Ra.T - 4 * J)[0]
    lm = lam_mu_ok(alpha, g, ed)
    tag = []
    if w3o < -1e-6: tag.append('T3o')
    if w3e < -1e-6: tag.append('T3e')
    if lm: tag.append(lm)
    key = (kind, tuple(tag) if tag else 'SURVIVES')
    out[key] += 1
    if not tag: keep.append((b, q, p1, p2, kind))
for k, v in sorted(out.items(), key=lambda z: -z[1]): print('  kind %2d  %-22s %d' % (k[0], k[1], v))
print('left after all filters:', len(keep), Counter(k[4] for k in keep))
with open(recfile.replace('.txt', '_left.txt'), 'w') as f:
    for r in keep: f.write('%d %d %d %d %d\n' % r)
