"""Assemble rows of the Hoffman-boundary reconstruction.  Pair conditions (exact, dossier model):
   d_w(u) = d_u(w),   |N(w) & N(u) & F| + |B_w & B_u| = 1 if w~u else 2.
Exhaustive backtracking with forward checking (no symmetry reduction): every completion is a labelled graph
with the boundary (coclique + blocks) fixed.  Writes each completion's F-adjacency as rows of indices.
  python3 assemble.py BLOCKS DOMDIR OUT [maxsol]"""
import sys, os, time
blocks_path, domdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
maxsol = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
lines = open(blocks_path).read().split("\n")
nb, c, deg = map(int, lines[0].split())
M = []
for l in lines[1:1 + nb]:
    a = list(map(int, l.split())); M.append(sum(1 << s for s in a[1:]))
inter = [[bin(M[i] & M[j]).count("1") for j in range(nb)] for i in range(nb)]
dom = []
for w in range(nb):
    D = []
    for l in open(os.path.join(domdir, f"dom_{w}.txt")):
        if l.strip(): D.append(sum(1 << int(x) for x in l.split()))
    dom.append(D)
print("domain sizes: min", min(map(len, dom)), "max", max(map(len, dom)), "total", sum(map(len, dom)), flush=True)
def compat(w, a, u, b):
    e = (a >> u) & 1
    if e != (b >> w) & 1: return False
    return bin(a & b).count("1") + inter[w][u] == (1 if e else 2)
sols = []; nodes = [0]; t0 = time.time()
def rec(assign, doms):
    nodes[0] += 1
    free = [w for w in range(nb) if w not in assign]
    if not free:
        sols.append(dict(assign)); return len(sols) >= maxsol
    w = min(free, key=lambda x: len(doms[x]))
    for a in doms[w]:
        nd = {}
        ok = True
        for u in free:
            if u == w: continue
            f = [b for b in doms[u] if compat(w, a, u, b)]
            if not f: ok = False; break
            nd[u] = f
        if not ok: continue
        assign[w] = a
        if rec(assign, nd): return True
        del assign[w]
    return False
rec({}, {w: dom[w] for w in range(nb)})
print(f"completions: {len(sols)}  nodes: {nodes[0]}  time {time.time() - t0:.1f}s", flush=True)
with open(out, "w") as f:
    for s in sols:
        f.write(";".join(" ".join(str(u) for u in range(nb) if (s[w] >> u) & 1) for w in range(nb)) + "\n")
