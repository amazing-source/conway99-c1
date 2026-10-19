# Symmetry-invariance test of py_extend (frontier only, no SAT): write a cover file holding a boundary and its images
# under random elements of (core stabiliser) x (Y relabellings); run py_extend --all-attachments; compare counts.
import gzip, json, random, subprocess, sys
from itertools import permutations, product
W, codex, cover, fam, idx, nimg, outdir = sys.argv[1:8]
idx = [int(i) for i in idx.split(',')]; nimg = int(nimg)
GR = {"K3": ((0, 1), (0, 2), (1, 2)), "P3": ((0, 1), (0, 2)), "P3N": ((0, 1), (0, 2)), "K2": ((0, 1),),
      "2K2": ((0, 1), (2, 3)), "2K2N": ((0, 1), (2, 3))}[fam]
NR = 4 if fam.startswith("2K2") else 3; NG = len(GR)
CORE = tuple((s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2))
src = json.loads(gzip.decompress(open(cover, 'rb').read()))
core = src['core']
E = {tuple(sorted(e)) for e in core['edges']}
look = {q: i for i, q in enumerate(CORE)}
stabs = []
for swap in (0, 1):
    roots = (0, 2, 1) if swap else (0, 1, 2)
    for fl in product(range(2), repeat=3):
        p = [look[tuple(sorted(2*roots[l//2] + ((l % 2) ^ fl[l//2]) for l in q))] for q in CORE]
        if {tuple(sorted((p[u], p[v]))) for u, v in E} == E:
            stabs.append(p)
YG = []
for p in permutations(range(NR)):
    if {tuple(sorted((p[a], p[b]))) for a, b in GR} != set(GR): continue
    for f in product(range(2), repeat=NR):
        m = {}
        for g, (a, b) in enumerate(GR):
            na, nb = sorted((p[a], p[b])); ng = GR.index((na, nb))
            for s, t in product(range(2), repeat=2):
                let = {p[a]: s ^ f[a], p[b]: t ^ f[b]}
                m[(g, 2*s+t)] = (ng, 2*let[na] + let[nb])
        YG.append(m)
rnd = random.Random(7)
hexes = []; groups = []
for bi in idx:
    b = bytes.fromhex(src['boundaries_hex'][bi])
    grp = [len(hexes)]; hexes.append(b.hex())
    for _ in range(nimg):
        p = rnd.choice(stabs); m = rnd.choice(YG)
        s = [sum(1 << p[v] for v in range(8) if x >> v & 1) for x in b]
        img = [0] * (4*NG)
        for g in range(NG):
            for c in range(4):
                ng, nc = m[(g, c)]; img[4*ng + nc] = s[4*g + c]
        grp.append(len(hexes)); hexes.append(bytes(img).hex())
    groups.append((bi, grp))
fake = dict(src); fake['boundaries_hex'] = hexes; fake['boundary_count'] = len(hexes)
fp = outdir + '/fake_%s.json.gz' % fam
open(fp, 'wb').write(gzip.compress(json.dumps(fake).encode()))
op = outdir + '/inv_%s.json.gz' % fam
r = subprocess.run([sys.executable, '-I', W + '/py_extend.py', codex, fam, fp, '0', str(len(hexes)), '--all-attachments',
                    '--outside-c2', '--inclusion', '--out=' + op] + sys.argv[8:], capture_output=True, text=True, timeout=280)
if r.returncode:
    print(r.stderr[-2000:]); sys.exit(1)
d = json.loads(gzip.decompress(open(op, 'rb').read()))
cases = {c['boundary_index']: c for c in d['cases']}
for bi, grp in groups:
    cs = [cases[i] for i in grp]
    keyf = lambda c: (c['status'], json.dumps({k: v for k, v in sorted(c['counts'].items()) if k != 'max_conflicts'}))
    ks = [keyf(c) for c in cs]
    print(json.dumps({'boundary_index': bi, 'images': len(grp) - 1, 'all_equal': len(set(ks)) == 1,
                      'canonical': ks[0], 'distinct': len(set(ks))}))
