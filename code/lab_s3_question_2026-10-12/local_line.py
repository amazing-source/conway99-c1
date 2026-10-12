"""Lab session, 2026-10-12. Local problem at P = 0 (local_vertex.py) with the split set prescribed: R is split iff R is far from
the line l through P in the direction delta = (0,0,0,1). All solutions are enumerated (cadical + blocking clauses) and, for
each split R, the three labels of its common neighbours with P in the next layer (B(x,delta) = +1) and in the previous layer
are printed as a pattern: U = label of the "up" neighbours, D = label of the "down" ones.
python local_line.py <tmp dir>"""
import sys, os, subprocess, collections, importlib.util
tmp = sys.argv[1]
spec = importlib.util.spec_from_file_location("lv", os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_vertex.py"))
lv = importlib.util.module_from_spec(spec); keep = sys.argv; sys.argv = ["x"]; spec.loader.exec_module(lv); sys.argv = keep
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
Bf = lambda x, y: (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3
delta = (0, 0, 0, 1); P = 0
l = [P, lv.I[delta], lv.I[lv.add(delta, delta)]]
farl = [r for r in lv.far if not any(r in lv.nbs[x] for x in l)]; assert len(farl) == 24
cl = lv.build("free")
for r in lv.far:
    vs = [lv.var[(z, r)] for z in lv.C[r][1:]]
    if r in farl: cl.append(vs)
    else: cl += [[-v] for v in vs]
path = os.path.join(tmp, "locl.cnf"); nsol = 0; pats = collections.Counter(); sols = []
while True:
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (lv.nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=200).stdout
    if "s UNSATISFIABLE" in out: break
    assert "s SATISFIABLE" in out
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    nsol += 1; key = []
    for r in farl:
        lab = {z: (lv.var.get((z, r), 0) in model) for z in lv.C[r]}
        up = sorted(int(lab[z]) for z in lv.C[r] if Bf(lv.V[z], delta) == 1); dn = sorted(int(lab[z]) for z in lv.C[r] if Bf(lv.V[z], delta) == 2)
        assert len(up) == 3 and len(dn) == 3
        key.append((tuple(up), tuple(dn)))
    pats.update(("U%s D%s" % ("".join(map(str, u)), "".join(map(str, d)))) for u, d in key)
    sols.append(frozenset(v for v in model if v <= 300))
    cl.append([(-v if (v in model) else v) for v in range(1, 301)])
    if nsol >= 40: print("stopped at 40 solutions"); break
print("solutions with split set = far(l): %d" % nsol)
print("patterns (labels of the three up neighbours, of the three down neighbours), over all solutions and split R: %s" % sorted(pats.items()))
