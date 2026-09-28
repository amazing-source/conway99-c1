# J1a type (iii) (P4): generate every base configuration (alpha, groups) of the support label graph -> base_iii.bin.
# Model (hand-derived, notes/151 s7-8), blocks: 1=d, 2=e, 3=f, 4=g (the path), 5=h, 6=i; coordinate 0 = c.
#   rho1 = e_d - e_e, rho2 = e_e - e_f, rho3 = e_f - e_g (normalised by inner flips); net_d = +1, net_g = -1.
#   X-type cells d, g with a_d = -1, a_g = +1: h(c^sig, K^tau) = a_K tau.  S-type cells e, f, h, i: h = a_K sig,
#   a_e + a_f + a_h + a_i = 0.  Label (K,s) has rep e_c + s e_K; alpha_L = h(rep) = a_K (S-type) or a_K s (X-type);
#   positive rep r_L = alpha_L (e_c + s e_K).  The A-root of L lies in O_{K^(-alpha_L s)}.
#   Groups: 2 labels with alpha=+1 and 2 with alpha=-1 each.  Line rules (A-root in an inner vertex of v_k):
#     v1 = (d+, e-): Q_e(v1) = sigma v2  -> A-root in O_{e-} not in G1;  Q_d(v1) not an S-vertex -> at most one
#                    of the two A-roots of O_{d+} (labels (d,+),(d,-)) in G1.
#     v2 = (e+, f-): Q_e(v2) = sigma v1, Q_f(v2) = sigma v3 -> A-roots in O_{e+} and O_{f-} not in G2.
#     v3 = (f+, g-): Q_f(v3) = sigma v2 -> A-root in O_{f+} not in G3; at most one of (g,+),(g,-) in G3.
import itertools, struct
D, E, F, Gb, H, I = 1, 2, 3, 4, 5, 6
def lab(K, s): return 2 * (K - 1) + (0 if s == 1 else 1)
bases = []
for aS in itertools.product((1, -1), repeat=4):
    if sum(aS) != 0: continue
    a = {D: -1, Gb: 1, E: aS[0], F: aS[1], H: aS[2], I: aS[3]}
    alpha = [0] * 12; ainner = {}
    for K in range(1, 7):
        for s in (1, -1):
            L = lab(K, s)
            alpha[L] = a[K] * s if K in (D, Gb) else a[K]
            ainner[L] = (K, -alpha[L] * s)          # (block, sign) of the inner vertex containing the A-root
    forb = {L: set() for L in range(12)}
    for L in range(12):
        K, t = ainner[L]
        if (K, t) == (E, -1): forb[L].add(0)
        if (K, t) in ((E, 1), (F, -1)): forb[L].add(1)
        if (K, t) == (F, 1): forb[L].add(2)
    Ap = [L for L in range(12) if alpha[L] == 1]; Am = [L for L in range(12) if alpha[L] == -1]
    def assigns(labels):
        out = []
        for g in itertools.product(range(3), repeat=6):
            if sorted(g) != [0, 0, 1, 1, 2, 2]: continue
            if any(gg in forb[L] for L, gg in zip(labels, g)): continue
            out.append(dict(zip(labels, g)))
        return out
    for gp in assigns(Ap):
        for gm in assigns(Am):
            g = [0] * 12
            for L, v in gp.items(): g[L] = v
            for L, v in gm.items(): g[L] = v
            if g[lab(D, 1)] == 0 and g[lab(D, -1)] == 0: continue      # at most one A-root of O_{d+} in G1
            if g[lab(Gb, 1)] == 2 and g[lab(Gb, -1)] == 2: continue    # at most one A-root of O_{g-} in G3
            bases.append((alpha, g))
V = [[0, 1, -1, 0, 0, 0, 0], [0, 0, 1, -1, 0, 0, 0], [0, 0, 0, 1, -1, 0, 0]]
print('type (iii) base configurations:', len(bases), ' x 162000 =', len(bases) * 162000)
with open('base_iii.bin', 'wb') as f:
    f.write(struct.pack('<i', len(bases)))
    for row in V: f.write(struct.pack('<7b', *row))
    for alpha, g in bases:
        f.write(struct.pack('<12b', *alpha)); f.write(struct.pack('<12b', *g))
