"""Euclidean-representation test of local configurations (note 176).
For srg(v,k,1,2) with eigenvalues r=t, s=-(t+1):  G_s = c_s[(rI - A) + ((k-r)/v) J] and G_r = c_r[(A - sI) - ((k-s)/v) J]
are PSD; so are their principal submatrices on any vertex set S whose induced subgraph is known."""
import numpy as np, itertools
PARAMS = {99: (14, 3, -4), 243: (22, 4, -5)}
def mins(Asub, v):
    k, r, s = PARAMS[v]; n = len(Asub); I = np.eye(n); J = np.ones((n, n))
    Gs = (r * I - Asub) + (k - r) / v * J
    Gr = (Asub - s * I) - (k - s) / v * J
    return np.linalg.eigvalsh(Gs).min(), np.linalg.eigvalsh(Gr).min()
def build(names, edges):
    idx = {n: i for i, n in enumerate(names)}; A = np.zeros((len(names), len(names)))
    for u, w in edges: A[idx[u], idx[w]] = A[idx[w], idx[u]] = 1
    return A
def report(title, names, edges):
    A = build(names, edges)
    for v in (99, 243):
        ms, mr = mins(A, v)
        flag = 'IMPOSSIBLE' if min(ms, mr) < -1e-9 else 'allowed'
        print(f"  {title:55s} v={v}: min eig G_s={ms:+.4f}, G_r={mr:+.4f} -> {flag}")
# (G) non-grid 4-cycle in F_x
def G_config(case):
    a = ['a0', 'a1', 'a2', 'a3']; z = ['z0', 'z1', 'z2', 'z3']
    names = ['x'] + a + z + ['w02', 'w13']
    E = [('x', u) for u in a]
    for i in range(4): E += [(z[i], a[i]), (z[i], a[(i + 1) % 4]), (z[i], z[(i + 1) % 4])]
    E += [('w02', 'a0'), ('w02', 'a2'), ('w13', 'a1'), ('w13', 'a3')]
    if case == 'grid':  # a2 = mate(a0), a3 = mate(a1): w's do not exist
        names = ['x'] + a + z; E = [e for e in E if 'w' not in e[0]] + [('a0', 'a2'), ('a1', 'a3')]
    elif case == 'B':   # a2 = mate(a0), a1,a3 non-mates
        names = [nm for nm in names if nm != 'w02']; E = [e for e in E if e[0] != 'w02'] + [('a0', 'a2')]
    return names, E
print("(G) 4-cycles of F_x:")
for case in ('grid', 'B', 'C'): report(f"case {case}", *G_config(case))
# (L2) alternating square at a: pi_a(b)=c, pi_a(b')=c'
names = ['x', 'a', "a'", 'b', "b'", 'c', "c'", 'P', "P'", 'Q', "Q'"]
E = [('x', u) for u in ['a', "a'", 'b', "b'", 'c', "c'"]] + [('a', "a'"), ('b', "b'"), ('c', "c'")]
E += [('a', u) for u in ['P', "P'", 'Q', "Q'"]] + [('b', 'P'), ("b'", "P'"), ('c', 'Q'), ("c'", "Q'"), ('P', 'Q'), ("P'", "Q'")]
print("(L2) alternating square:")
report("pi_a(b)=c, pi_a(b')=c'", names, E)
# control: grid-like at a for two pairs: pi_a(b)=b', pi_a(c)=c'
E2 = [('x', u) for u in ['a', "a'", 'b', "b'", 'c', "c'"]] + [('a', "a'"), ('b', "b'"), ('c', "c'")]
E2 += [('a', u) for u in ['P', "P'", 'Q', "Q'"]] + [('b', 'P'), ("b'", "P'"), ('c', 'Q'), ("c'", "Q'"), ('P', "P'"), ('Q', "Q'")]
report("control: pi_a(b)=b', pi_a(c)=c' (grid-like)", names, E2)
