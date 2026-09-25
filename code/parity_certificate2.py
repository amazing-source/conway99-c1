"""notes/103 sec. 11 (relaxed): role-dependent h0/h1 (position of m in the target pair), and per-edge residual
H(phi) = h0(phi)+h1(phi)+h0(phi^-1)+h1(phi^-1) required to equal alpha*sgn(phi) + beta (the transport rules force
sum_e sgn(phi_e) = 0, so the residual sums to 105*beta = beta).  Certificate iff a solution has c_f + d + beta = 1."""
import itertools
import numpy as np
exec(open('parity_certificate.py', encoding='utf-8').read().split('# --- equations')[0])   # reuse F, helpers

sgn = [0] * 24
for f in range(24):
    p = P[f]; s = 0
    for a in range(4):
        for b in range(a + 1, 4):
            if p[a] > p[b]: s ^= 1
    sgn[f] = s
# unknown layout: lambda (nF) | h0 (24) | h1 (24) | d | alpha | beta
o_h0, o_h1 = nF, nF + 24
o_d, o_a, o_b = nF + 48, nF + 49, nF + 50
NV = nF + 51
rows = {}
def add_eq(bits):
    x = bits
    while x:
        p = x.bit_length() - 1
        if p in rows: x ^= rows[p]
        else: rows[p] = x; return True
    return False
for phi in range(24):                                  # residual equations
    ip = inv(phi)
    bits = (1 << (o_h0 + phi)) ^ (1 << (o_h1 + phi)) ^ (1 << (o_h0 + ip)) ^ (1 << (o_h1 + ip)) ^ (1 << o_b)
    if sgn[phi]: bits ^= 1 << o_a
    add_eq(bits)
for r in range(5):
    first = [s >= r for s in range(4)]
    for tup in itertools.product(range(24), repeat=4):
        ok = True
        for w in range(4):
            if sum(1 for s in range(4) if (V[P[tup[s]][w]][0] if first[s] else V[P[tup[s]][w]][1]) == 0) != 2:
                ok = False; break
        if not ok: continue
        bits = 1 << o_d
        for s in range(4):
            bits ^= 1 << ((o_h0 if first[s] else o_h1) + tup[s])
        fsum = [0] * nF
        for s in range(4):
            for t in range(s + 1, 4):
                c = cmp(tup[t], inv(tup[s]))
                if not first[s]: c = cmp(c, SW)
                if not first[t]: c = cmp(SW, c)
                for i in range(nF): fsum[i] ^= int(Fb[i][c])
        for i in range(nF):
            if fsum[i]: bits ^= 1 << i
        add_eq(bits)
M = np.array([[(b >> j) & 1 for j in range(NV)] for b in rows.values()], dtype=np.int64)
sol = nullspace(M)
print('rank', len(rows), 'of', NV, '; solution space dim', len(sol))
good = [v for v in sol if (sum(cF[i] * v[i] for i in range(nF)) + v[o_d] + v[o_b]) % 2 == 1]
print('certificate (c_f + d + beta = 1):', 'YES' if good else 'none')
if good:
    v = good[0]
    print('  lambda', [int(x) for x in v[:nF]], ' d', int(v[o_d]), ' alpha', int(v[o_a]), ' beta', int(v[o_b]))
