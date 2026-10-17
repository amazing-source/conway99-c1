import subprocess, re, random, collections, sys
from sympy.combinatorics import Permutation, PermutationGroup
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
fn = sys.argv[1]; n = 243
adj = [set() for _ in range(n)]
for line in open(R + fn):
    if line.strip():
        u, v = map(int, line.split()); adj[u].add(v); adj[v].add(u)
cmd = f"n={n} $=0 g\n" + ";\n".join(" ".join(map(str, sorted(adj[i]))) for i in range(n)) + ".\n-m x\n"
out = subprocess.run(['/tmp/solvers/nauty_src/nauty2_8_8/dreadnaut'], input=cmd, capture_output=True, text=True).stdout
gens = []; cur = []
for line in out.splitlines():
    if line.startswith('('):
        if cur: gens.append(" ".join(cur))
        cur = [line.strip()]
    elif line.startswith(' ') and cur:
        cur.append(line.strip())
    else:
        if cur: gens.append(" ".join(cur)); cur = []
if cur: gens.append(" ".join(cur))
perms = []
for gtxt in gens:
    img = list(range(n))
    for cyc in re.findall(r'\(([^)]*)\)', gtxt):
        c = list(map(int, cyc.split()))
        for i in range(len(c)): img[c[i]] = c[(i + 1) % len(c)]
    perms.append(Permutation(img))
G = PermutationGroup(perms); print(fn, '|Aut| =', G.order())
seen = collections.Counter(); random.seed(1)
for _ in range(4000):
    x = G.random_pr()
    o = x.order()
    for p in (3, 5, 7, 11):
        if o % p == 0:
            y = x ** (o // p); img = y.array_form
            fix = [i for i in range(n) if img[i] == i]
            kf = collections.Counter(len(adj[i] & set(fix)) for i in fix)
            a1 = sum(1 for i in range(n) if img[i] != i and img[i] in adj[i])
            seen[(p, len(fix), tuple(sorted(kf.items())), a1)] += 1
for key, c in sorted(seen.items()): print('  p=%d |Fix|=%d Fix-degrees=%s a1=%d   (seen %d)' % (key + (c,)))
