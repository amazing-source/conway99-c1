"""Lab session, 2026-10-12. Local problem at P = 0 (local_cnf2.py) with "at least k of the 60 blocks are flat" and "some
block is split": all solutions are enumerated (blocking clauses) and identified (line solutions have exactly 36 flat
blocks). If, for some k, the only solutions are line solutions, then (line solutions being excluded globally) every
vertex of a non-trivial parity skeleton has at most k - 1 flat pairs.
python local_flatcount.py <tmp dir> <seconds per call> <k> [<k> ...]"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2]); ks = [int(a) for a in sys.argv[3:]]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv0, base, x, y = L.build(["nontrivial"])
flats = [x[r][0] for r in L.far]
for k in ks:
    nvv = [nv0]; cl = list(base)
    def new(): nvv[0] += 1; return nvv[0]
    prev = None
    for i, l in enumerate(flats):
        cur = [None] + [new() for _ in range(k)]
        for j in range(1, k + 1):
            pj = prev[j] if prev else None; pj1 = (prev[j - 1] if j > 1 else "T") if prev else ("T" if j == 1 else None)
            c = [-cur[j]] + ([pj] if pj is not None else [])
            cl.append(c + [l])
            if pj1 != "T": cl.append(c + ([pj1] if pj1 is not None else []))
        prev = cur
    cl.append([prev[k]])
    path = os.path.join(tmp, "lfc_%d.cnf" % os.getpid()); nsol = 0; kinds = {}; t0 = time.time(); status = "complete"
    while True:
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nvv[0], len(cl)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
        try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: status = "NO DECISION on the last call"; break
        if "s UNSATISFIABLE" in out: break
        if "s SATISFIABLE" not in out: status = "NO DECISION on the last call"; break
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        st = {r: [s for s in range(11) if x[r][s] in model][0] for r in L.far}
        nsol += 1; kd = L.identify(st); kd = "line" if kd.startswith("line") else kd; kinds[kd] = kinds.get(kd, 0) + 1
        cl.append([-x[r][st[r]] for r in L.far])
        if nsol >= 40: status = "stopped at 40 solutions"; break
    print("at least %d flat blocks: %d non-trivial solution(s) %s; %s; %.1f s" % (k, nsol, kinds, status, time.time() - t0), flush=True)
