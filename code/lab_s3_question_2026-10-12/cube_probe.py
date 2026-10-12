"""Lab session, 2026-10-12. Probe: how fast does a CDCL solver refute the parity-skeleton instance of parity_line.py
(mode all: u0 has three negative edges to L_1) once the signs of the 18 transversal lines of the nine grids through
the line l are fixed for the first k grids (random balanced patterns, or the cube implied by u0)?
python cube_probe.py <all.cnf> <k grids fixed> <seed> <out.cnf>"""
import sys, random, importlib.util, os
spec = importlib.util.spec_from_file_location("pl", os.path.join(os.path.dirname(os.path.abspath(__file__)), "parity_line.py"))
sys.argv_backup = sys.argv; sys.argv = ["x", "none"]
pl = importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(pl)
except SystemExit: pass
sys.argv = sys.argv_backup
src, k, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rnd = random.Random(seed)
trans = [t for t in pl.lines if all(x in pl.lay for x in t) and len({pl.lay[x] for x in t}) == 3]
assert len(trans) == 18
# group the transversal lines by grid: two transversal lines are in the same grid iff their points are joined by tangent lines
grids = []
for t in trans:
    for g in grids:
        if any(a in pl.nbs[b] for a in t for b in g[0] if pl.lay[a] == pl.lay[b]): g.append(t); break
    else: grids.append([t])
assert len(grids) == 9 and all(len(g) == 2 for g in grids)
units = []
for g in grids[:k]:
    for t in g:
        a, b, c = t; pat = rnd.choice([(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)])
        for (x, y), val in zip(((a, b), (b, c), (a, c)), pat):
            v = pl.E(x, y) + 1; units.append(v if val else -v)
lines_ = open(src).read().split("\n"); head = lines_[0].split()
head[3] = str(int(head[3]) + len(units))
open(out, "w", newline="\n").write(" ".join(head) + "\n" + "\n".join(lines_[1:]).rstrip("\n") + "\n" + "".join("%d 0\n" % u for u in units))
print("grids fixed: %d; unit clauses added: %d" % (k, len(units)))
