import numpy as np
from collections import Counter
exec(open('postfilter.py').read().split('recs = [tuple')[0])
recs = [tuple(map(int, l.split())) for l in open('mshell_survivors.txt')]
kinds = Counter(r[4] for r in recs); ntr = Counter(r[5] for r in recs)
acase = Counter(); cyc = Counter(); ekk = Counter(); rk = Counter(); samec = Counter()
for (b, q, p1, p2, kind, nt) in recs:
    alpha, g, ed = config(b, q, p1, p2)
    a = bases[b][:6]; acase[''.join(str(K) for K in range(1, 7) if a[K - 1] == 1)] += 1
    adj = {L: [] for L in range(12)}
    for x, y in ed: adj[x].append(y); adj[y].append(x)
    seen = set(); cl = []
    for L in range(12):
        if L in seen: continue
        n = 0; st = [L]
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); n += 1; st += adj[x]
        cl.append(n)
    cyc[tuple(sorted(cl))] += 1
    e = [0, 0, 0]
    for x, y in ed:
        if g[x] == g[y]: e[g[x]] += 1
    ekk[tuple(e)] += 1
    R, G = mats(alpha, g, ed)
    w = np.linalg.eigvalsh(12 * np.eye(15) + 4 * G - R @ R.T); rk[int(np.sum(w > 1e-7))] += 1
    samec[sum(1 for x, y in ed[6:] if x // 2 == y // 2)] += 1
print('M-shell survivors:', len(recs), ' record kinds', dict(kinds), ' #consistent triples', dict(ntr))
print('B+ blocks', dict(acase)); print('cycles', dict(cyc)); print('e_kk', dict(ekk)); print('odd rank', dict(rk)); print('same-cell P', dict(samec))
b, q, p1, p2, kind, nt = recs[0]; alpha, g, ed = config(b, q, p1, p2)
print('example: b=%d q=%d p1=%d p2=%d  a=%s  groups=%s  edges=%s' % (b, q, p1, p2, bases[b][:6], g, ed))
