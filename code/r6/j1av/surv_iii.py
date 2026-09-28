import numpy as np, sys
from collections import Counter
sys.argv = ['x', 'iii', 'base_iii.bin', 'iii_records.txt']
exec(open('pipeline_gen.py').read().split("if __name__ == '__main__':")[0])
recs = [tuple(map(int, l.split()[:5])) for l in open('iii_records_pipeline_survivors.txt')]
for (b, q, p1, p2, kind) in recs:
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed)
    w = np.linalg.eigvalsh(12 * np.eye(15) + 4 * G - R @ R.T); rk = int(np.sum(w > 1e-7))
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
    e = [0, 0, 0]
    for x, y in ed:
        if g[x] == g[y]: e[g[x]] += 1
    aS = {K: alpha[2 * (K - 1)] for K in range(1, 7)}
    print('b=%d q=%d p1=%d p2=%d kind=%d rank=%d cycles=%s e_kk=%s alpha(+labels)=%s groups=%s' % (b, q, p1, p2, kind, rk, sorted(cl), e, [alpha[L] for L in range(12)], g))
