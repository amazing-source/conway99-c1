"""notes/103 sec. 12b: mixed certificate.  Class-triangle functions with degree-2 cherry terms f(phi_{P->R}, phi_{P'->R})
that cancel exactly against mu-with-labels groups at (R, m): g(a, a') = f(a^-1, a'^-1).
Unknowns: f (576) | h1 (24) | h3min (24) | h3max (24) | alpha | beta | c1 | c2.
C-local:  sum_{18 cherries} f + sum_{18 ribs} h1 + sum_{3 spines} h2 = c1,  h2 = h1 + h1.inv + H + H.inv + alpha sgn + beta,
          H = h3min + h3max.     Z-groups: sum_{6 pairs} f(a^-1, a'^-1) + sum_4 h3role(a) = c2.
Certificate iff a solution has c1 + c2 + beta = 1.  (Only the class triangle {1,2,3} pattern is sampled: a relaxation.)"""
import itertools, random, sys
exec(open('ct_certificate.py', encoding='utf-8').read().split("rng = random.Random(5)")[0])

oF, oH1, oMn, oMx = 0, 576, 600, 624
oA, oB, oC1, oC2 = 648, 649, 650, 651
NV = 652
rows = {}
def add_eq(v):
    x = v
    while x:
        p = x.bit_length() - 1
        if p in rows: x ^= rows[p]
        else: rows[p] = x; return True
    return False
def fbit(a, b): return 1 << (oF + 24 * a + b)

# Z-groups, all 5 order patterns: a_s maps X -> R_s ; pattern r: m first in R_s iff s >= r
nz = 0
for r in range(5):
    first = [s >= r for s in range(4)]
    for tup in itertools.product(range(24), repeat=4):
        if any(sum(1 for s in range(4) if (V[P[tup[s]][w]][0] if first[s] else V[P[tup[s]][w]][1]) == 0) != 2
               for w in range(4)):
            continue
        nz += 1
        v = 1 << oC2
        for s in range(4):
            v ^= 1 << ((oMn if first[s] else oMx) + tup[s])
            for t in range(s + 1, 4):
                v ^= fbit(inv(tup[s]), inv(tup[t]))
        add_eq(v)
print('Z-valid tuples', nz, '; rank after Z-groups', len(rows), flush=True)

# class-triangle {1,2,3} local solutions
rng = random.Random(11)
got = tries = 0
cher = [('12', '13'), ('12', '23'), ('13', '23')]
while got < int(sys.argv[1]) if len(sys.argv) > 1 else got < 3000:
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
    if not ok: continue
    got += 1
    v = 1 << oC1
    for (pa, pb) in cher:
        for R in Rs: v ^= fbit(phiR[pa][R], phiR[pb][R])
    for Pg in phiR:
        for R in Rs: v ^= 1 << (oH1 + phiR[Pg][R])
    for s in spines:
        v ^= (1 << (oH1 + s)) ^ (1 << (oH1 + inv(s)))
        for q in (s, inv(s)):
            v ^= (1 << (oMn + q)) ^ (1 << (oMx + q))
        if sgn(s): v ^= 1 << oA
        v ^= 1 << oB
    add_eq(v)
print('C-local samples', got, 'from', tries, '; total rank', len(rows), 'of', NV, flush=True)
# does the system force c1 + c2 + beta = 0 ?  (i.e. is the vector e_c1 + e_c2 + e_beta in the row space?)
x = (1 << oC1) ^ (1 << oC2) ^ (1 << oB)
while x:
    p = x.bit_length() - 1
    if p in rows: x ^= rows[p]
    else: break
print('certificate possible (c1+c2+beta = 1 consistent)?', x != 0)
