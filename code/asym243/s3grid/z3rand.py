"""Random Z3-cover instances of BH (full S3 model of s3full.py restricted to A3 gains, plus a few random fixed gains).
python3 z3rand.py SEED NFIX OUT.cnf  -- appends units to full_control.cnf (must exist)"""
import sys, random, pickle, itertools
seed, nfix, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
mp = pickle.load(open('full_control.cnf.map', 'rb')); X, G = mp['X'], mp['G']
EVEN = [g for g in range(6) if sum(G[g][i] > G[g][j] for i in range(3) for j in range(i + 1, 3)) % 2 == 0]
ODD = [g for g in range(6) if g not in EVEN]
units = []
for e, vs in X.items():
    for g in ODD: units.append(-vs[g])
random.seed(seed); edges = sorted(X)
for e in random.sample(edges, nfix):
    g = random.choice(EVEN); units.append(X[e][g])
head = open('full_control.cnf').readline().split(); nv, nc = int(head[2]), int(head[3])
with open(out, 'w') as f:
    f.write(f"p cnf {nv} {nc + len(units)}\n")
    with open('full_control.cnf') as src:
        next(src)
        for line in src: f.write(line)
    for u in units: f.write(f"{u} 0\n")
print('units', len(units))
