"""Exact rooted CNF for srg(v, 2m, 1, 2) (diameter 2): x = 0; N(x) = 1..2m with mates (1,2),(3,4),...;
Delta_x = all non-mate pairs {u,w} of N(x), vertex z_uw adjacent to u and w.  Unknown: edges inside Delta_x only.
Every pair: #common neighbours = 1 if adjacent else 2; degree 2m.  Optional units (file of lines 'p q 0|1' on vertex ids
or 'pi a u w' meaning z_au ~ z_aw, i.e. pi_a(u) = w).
python3 gen_rooted.py m OUT.cnf [units-file]"""
import sys, itertools
m = int(sys.argv[1]); out = sys.argv[2]; ufile = sys.argv[3] if len(sys.argv) > 3 else None
k = 2 * m; Nx = list(range(1, k + 1)); mate = {u: u + 1 if u % 2 else u - 1 for u in Nx}
pairs = [(u, w) for u, w in itertools.combinations(Nx, 2) if mate[u] != w]
Z = {p: 1 + k + i for i, p in enumerate(pairs)}; zid = lambda u, w: Z[(min(u, w), max(u, w))]
V = 1 + k + len(pairs)
nv = 0; cls = []
def new():
    global nv; nv += 1; return nv
TRUE = new(); cls.append([TRUE])
X = {}
def fixed(p, q):
    """return None if variable, else 0/1"""
    if p > q: p, q = q, p
    if p == 0: return 1 if q <= k else 0
    if q <= k: return 1 if mate[p] == q else 0
    if p <= k: return 1 if p in pairs[q - k - 1] else 0
    return None
for p in range(k + 1, V):
    for q in range(p + 1, V): X[(p, q)] = new()
def e(p, q):
    if p > q: p, q = q, p
    f = fixed(p, q)
    if f is None: return X[(p, q)]
    return TRUE if f else -TRUE
def counter(lits, cap):
    prev = [None] * (cap + 1)
    for l in lits:
        cur = [None] * (cap + 1)
        for j in range(1, cap + 1):
            vv = new(); cur[j] = vv
            if prev[j] is not None: cls.append([-prev[j], vv])
            if j == 1: cls.append([-l, vv])
            elif prev[j - 1] is not None: cls.append([-prev[j - 1], -l, vv])
            a = [] if prev[j] is None else [prev[j]]
            if j == 1: cls.append([-vv] + a + [l])
            elif prev[j - 1] is None: cls.append([-vv] + a)
            else: cls.append([-vv] + a + [l]); cls.append([-vv] + a + [prev[j - 1]])
        prev = cur
    return prev
def exactly(lits, t, cap):
    ge = counter(lits, cap)
    if t >= 1: cls.append([ge[t]])
    if t + 1 <= cap: cls.append([-ge[t + 1]])
# degrees
for p in range(V):
    exactly([e(p, q) for q in range(V) if q != p], k, k + 1)
# pair conditions
for p in range(V):
    for q in range(p + 1, V):
        ys = []
        for r in range(V):
            if r in (p, q): continue
            a, b = e(p, r), e(q, r)
            if a == -TRUE or b == -TRUE: continue
            if a == TRUE and b == TRUE: ys.append(TRUE); continue
            y = new(); cls.append([-y, a]); cls.append([-y, b]); cls.append([y, -a, -b]); ys.append(y)
        ge = counter(ys, 3); ee = e(p, q)
        cls.append([-ee, ge[1]]); cls.append([-ee, -ge[2]])          # adjacent: exactly 1
        cls.append([ee, ge[2]]); cls.append([ee, -ge[3]])            # non-adjacent: exactly 2
if ufile:
    for line in open(ufile):
        t = line.split()
        if not t: continue
        if t[0] == 'pi':
            a, u, w = map(int, t[1:]); cls.append([e(zid(a, u), zid(a, w))])
        else:
            p, q, b = map(int, t); cls.append([e(p, q)] if b else [-e(p, q)])
with open(out, 'w') as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
import pickle; pickle.dump({'Z': Z, 'X': X, 'V': V, 'k': k}, open(out + '.map', 'wb'))
print(f"m={m} V={V} vars={nv} clauses={len(cls)}")
