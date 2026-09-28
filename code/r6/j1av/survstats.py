# Structure of the 98,784 J1a(v) support-level survivors (exploratory statistics, not a proof).
import struct
from collections import Counter
exec(open('postfilter.py').read().split('recs = [tuple')[0])
recs = [tuple(map(int, l.split())) for l in open('vertex_even_left.txt')]
st = Counter(); cyc = Counter(); ekk = Counter(); acase = Counter(); samecell = Counter(); qtype = Counter()
for (b, q, p1, p2, kind) in recs:
    alpha, g, ed = config(b, q, p1, p2)
    a = bases[b][:6]
    Bp = ''.join(str(K) for K in range(1, 7) if a[K - 1] == 1)
    acase['B+=' + Bp] += 1
    adj = {L: [] for L in range(12)}
    for x, y in ed: adj[x].append(y); adj[y].append(x)
    seen = set(); cl = []
    for L in range(12):
        if L in seen: continue
        n = 0; stck = [L]
        while stck:
            x = stck.pop()
            if x in seen: continue
            seen.add(x); n += 1; stck += adj[x]
        cl.append(n)
    cyc[tuple(sorted(cl))] += 1
    e = [0, 0, 0]
    for x, y in ed:
        if g[x] == g[y]: e[g[x]] += 1
    ekk[tuple(sorted(e))] += 1
    samecell[sum(1 for x, y in ed[6:] if x // 2 == y // 2)] += 1
    # triangle/other crossing count X
    typ = lambda L: L // 2 + 1 <= 3
    qtype[sum(1 for x, y in ed if typ(x) != typ(y))] += 1
print('survivors', len(recs))
print('a-cases        ', sorted(acase.items()))
print('G_star cycles  ', cyc.most_common())
print('e_kk (sorted)  ', ekk.most_common())
print('same-cell P    ', sorted(samecell.items()))
print('#cross tri|oth ', sorted(qtype.items()))
