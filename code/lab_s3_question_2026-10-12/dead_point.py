"""Lab session, 2026-10-12. Local problem at P = 0 with a DEAD POINT u in N(P): the 18 blocks through u are flat and the
18 inner pairs through u are flat (this is what a trivial neighbour u of P imposes on P). All solutions with a split
block are enumerated.
python dead_point.py <tmp dir> <seconds per call>"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv, cl, x, y = L.build(["nontrivial"])
u = L.NP[0]
for r in L.far:
    if u in L.C[r]: cl.append([x[r][0]])
for p in L.pairs:
    if u in p:
        for t in y[p]: cl.append([-t])
path = os.path.join(tmp, "dead_%d.cnf" % os.getpid()); nsol = 0; t0 = time.time(); status = "complete (UNSAT after the last one)"
while True:
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: status = "TIMEOUT"; break
    if "s UNSATISFIABLE" in out: break
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    st = {r: [s for s in range(11) if x[r][s] in model][0] for r in L.far}
    nsol += 1; print("  solution %d: %s" % (nsol, L.identify(st)), flush=True)
    cl.append([-x[r][st[r]] for r in L.far])
print("dead point u = %s: %d solution(s) with a split block; %s; %.1f s" % (L.V[u], nsol, status, time.time() - t0))
