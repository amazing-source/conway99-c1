import sys, pickle, itertools, subprocess, collections
sys.argv_saved = list(sys.argv); sys.argv = ['x']
exec(open('s3grid.py').read().split('if __name__')[0]); sys.argv = sys.argv_saved
mp = pickle.load(open(sys.argv[1] + '.map', 'rb')); X, G = mp['X'], mp['G']
val = set()
for line in open(sys.argv[2]):
    if line.startswith('v '): val |= {int(t) for t in line.split()[1:] if int(t) > 0}
gain = {}
for (i, j), vs in X.items():
    g = [k for k in range(6) if vs[k] in val]; assert len(g) == 1; gain[(i, j)] = G[g[0]]
N = 243; A = [set() for _ in range(N)]
def vid(P, a): return 3 * P + a
for P in range(n):
    for a in range(3):
        for b in range(3):
            if a != b: A[vid(P, a)].add(vid(P, b))
for (i, j), g in gain.items():
    for a in range(3): A[vid(i, a)].add(vid(j, g[a])); A[vid(j, g[a])].add(vid(i, a))
deg = {len(a) for a in A}; lam = set(); mu = set()
for u in range(N):
    for v in range(u + 1, N):
        c = len(A[u] & A[v]); (lam if v in A[u] else mu).add(c)
print('degrees', deg, 'lambda', lam, 'mu', mu)
odd = sum(1 for g in gain.values() if sum(g[i] > g[j] for i in range(3) for j in range(i+1, 3)) % 2)
print('odd gains (after tree gauge):', odd)
with open(sys.argv[3], 'w') as f:
    for u in range(N):
        for v in A[u]:
            if u < v: f.write(f"{u} {v}\n")
cmd = f"n={N} $=0 g\n" + ";\n".join(" ".join(map(str, sorted(A[i]))) for i in range(N)) + ".\n-m x\n"
out = subprocess.run(['/tmp/solvers/nauty_src/nauty2_8_8/dreadnaut'], input=cmd, capture_output=True, text=True).stdout
print([l for l in out.splitlines() if 'grpsize' in l or 'orbits' in l][:2])
