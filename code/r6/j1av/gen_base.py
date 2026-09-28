# J1a type (v): generate every base configuration (a, groups) of the support label graph, and write base.bin for the C kernel.
# Model (hand-derived, notes/151 s6-7):
#   blocks 1,2,3 = triangle (v_k = e_k - e_{k+1 mod 3}), 4,5,6 = the others; star label (K,s) has rep e_c + s e_K,
#   a_K = h(rep) with sum a = 0; positive rep r_L = a_K (e_c + s e_K); V labels W1..W3 with v1=e1-e2, v2=e2-e3, v3=e3-e1.
#   Each group G_k (star nbrs of v_k) has 2 labels with a=+1 and 2 with a=-1.
#   Line rules (A-root of L in an inner vertex of v_k => L not in G_k):
#     (1,s): s=-a1 -> not G1, s=a1 -> not G3;  (2,s): s=a2 -> not G1, s=-a2 -> not G2;  (3,s): s=a3 -> not G2, s=-a3 -> not G3.
import itertools, struct, sys
def lab(K, s): return 2 * (K - 1) + (0 if s == 1 else 1)
def forbidden(a):
    fb = {}
    a1, a2, a3 = a[0], a[1], a[2]
    fb[lab(1, -a1)] = 0; fb[lab(1, a1)] = 2
    fb[lab(2, a2)] = 0;  fb[lab(2, -a2)] = 1
    fb[lab(3, a3)] = 1;  fb[lab(3, -a3)] = 2
    return fb
def group_assignments(labels, fb):
    # assign each of the 6 labels a group 0..2, exactly two per group, respecting forbidden groups
    out = []
    for g in itertools.product(range(3), repeat=6):
        if sorted(g) != [0, 0, 1, 1, 2, 2]: continue
        if any(fb.get(L) == gg for L, gg in zip(labels, g)): continue
        out.append(dict(zip(labels, g)))
    return out
bases = []
for a in itertools.product((1, -1), repeat=6):
    if sum(a) != 0: continue
    fb = forbidden(a)
    Ap = [lab(K, s) for K in range(1, 7) for s in (1, -1) if a[K - 1] == 1]
    Am = [lab(K, s) for K in range(1, 7) for s in (1, -1) if a[K - 1] == -1]
    GP = group_assignments(Ap, fb); GM = group_assignments(Am, fb)
    for gp in GP:
        for gm in GM:
            g = [0] * 12
            for L, v in gp.items(): g[L] = v
            for L, v in gm.items(): g[L] = v
            bases.append((a, g))
print('base configurations (a, groups):', len(bases), '  x 720 Q x 225 P =', len(bases) * 720 * 225)
with open('base.bin', 'wb') as f:
    f.write(struct.pack('<i', len(bases)))
    for a, g in bases:
        f.write(struct.pack('<6b', *a)); f.write(struct.pack('<12b', *g))
