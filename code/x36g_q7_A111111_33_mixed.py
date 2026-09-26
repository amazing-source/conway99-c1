"""A111111 type (3,3), mixed torsion Y = Y1 + Y2 on the two (6,6)-components C1, C2 (isomorphic).
Each far vertex's shadow = t1 u t2 (admissible triples on C1, C2) with layer counts (2,2,2) overall.
Balanced Y: every shadow has Y1(t1) + Y2(t2) = 0 mod 7.  Necessary coverage: every pair {n,n'} (inside a component
or across) lies in >= far(n,n') admissible zero-sum 6-sets.  Cross pairs: far = 2 - [same layer]."""
import itertools
import numpy as np
exec(open('x36f_q7_A111111_33_balance.py', encoding='utf-8').read().split("best = None")[0].replace("print(", "(lambda *a, **k: None)("))
T = np.array(triples); nt = len(T)
lay = np.array(layer)
lc = np.zeros((nt, 3), dtype=int)
for i, t in enumerate(triples):
    for x in t: lc[i, lay[x]] += 1
compat = np.zeros((nt, nt), dtype=bool)
for i in range(nt):
    need = 2 - lc[i]
    compat[i] = np.all(lc == need, axis=1)
Inc = np.zeros((nt, n), dtype=np.int64)
for i, t in enumerate(triples):
    for x in t: Inc[i, x] = 1
FARm = np.array([[FAR[a][b] if a != b else 0 for b in range(n)] for a in range(n)])
cross_need = np.array([[2 - (1 if lay[a] == lay[b] else 0) for b in range(n)] for a in range(n)])
Evec = [np.array(v) for v in E]
def combos():
    for c in itertools.product(range(P), repeat=2 * len(E)):
        if not any(c) or next(x for x in c if x) != 1: continue
        yield c
res = []; npass = 0
for c in combos():
    Y1 = sum(ci * Evec[k] for k, ci in enumerate(c[:len(E)])) % P
    Y2 = sum(ci * Evec[k] for k, ci in enumerate(c[len(E):])) % P
    s1 = (Inc @ Y1) % P; s2 = (Inc @ Y2) % P
    mask = compat & (((s1[:, None] + s2[None, :]) % P) == 0)
    M = mask.astype(np.int64)
    # coverage inside C1: pairs in t1, any compatible zero-sum t2
    row_cnt = M.sum(axis=1)                   # per t1
    cov11 = (Inc.T * row_cnt) @ Inc           # n x n: sum over t1 containing both
    col_cnt = M.sum(axis=0)
    cov22 = (Inc.T * col_cnt) @ Inc
    cov12 = Inc.T @ M @ Inc                   # n1 in t1, n2 in t2
    bad = 0
    iu = np.triu_indices(n, 1)
    bad += int(np.sum(FARm[iu] > cov11[iu])); bad += int(np.sum(FARm[iu] > cov22[iu]))
    bad += int(np.sum(cross_need > cov12))
    pure = (not Y1.any()) or (not Y2.any())
    res.append((bad, pure))
    if bad == 0: npass += 1
print('projective (Y1,Y2):', len(res), ' passing:', npass, ' min failing (mixed only):', min(b for b, p in res if not p), ' min failing (pure):', min(b for b, p in res if p))
